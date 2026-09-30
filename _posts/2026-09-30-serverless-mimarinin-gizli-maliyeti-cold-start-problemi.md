---
layout: post
title: "Serverless Mimarinin Gizli Maliyeti: Cold Start Problemi"
math: true
categories: 
  - Bilgi
tags: 
  - serverless
  - cold-start
  - aws-lambda
  - bulut-bilişim
  - performans
  - devops
toc: true
image: /img/serverless-mimarinin-gizli-26.png
---

Serverless mimari, sunucu yönetimini sağlayıcıya bırakarak kodu hızlıca üretime çıkarmamızı sağlar. Ancak “yalnızca kullandığın kadar öde” sloganının gölgesinde kalan bir performans maliyeti vardır: **soğuk başlangıç**. Uzun süre çağrılmayan bir işlev yeniden çalıştırıldığında ortamın hazırlanması gerekir ve kullanıcı, bazen saniyelere ulaşabilen bu gecikmenin faturasını bekleyerek öder.


![serverless-mimarinin-gizli-26](/img/serverless-mimarinin-gizli-26.svg)

``

## Cold start sırasında neler oluyor?

AWS Lambda, Azure Functions veya Google Cloud Functions üzerindeki bir işlev çağrıldığında sağlayıcı önce uygun bir çalışma ortamı arar. Hazır bir ortam yoksa yeni bir konteyner ya da mikro sanal makine oluşturulur. Ardından runtime başlatılır, uygulama paketi yüklenir ve global başlangıç kodları çalıştırılır.

Toplam yanıt süresini basitçe şöyle modelleyebiliriz:

$$T_{toplam} = T_{altyapi} + T_{runtime} + T_{init} + T_{islem}$$

Sıcak bir çağrıda ilk üç bileşenin büyük bölümü ortadan kalkar. Bu nedenle aynı işlev bir isteğe 80 ms, başka bir isteğe 1,5 saniyede yanıt verebilir. Ortalama süre iyi görünürken p95 veya p99 değerleri kullanıcı deneyimini bozabilir.

| Çağrı türü | Ortam durumu | Tipik gecikme | Risk |
|---|---|---:|---|
| Sıcak başlangıç | Konteyner hazır | 10–200 ms | Düşük |
| Soğuk başlangıç | Ortam sıfırdan hazırlanır | 300 ms–5 sn | Yüksek |
| Provisioned concurrency | Ortam önceden hazır | Tutarlı | Ek maliyet |

Beklenen gecikme de yaklaşık olarak $E[T] = p_c T_c + (1-p_c)T_w$ şeklinde hesaplanabilir. Burada $p_c$ cold start olasılığını, $T_c$ soğuk, $T_w$ ise sıcak çağrı süresini temsil eder.

## Gecikmeyi büyüten etkenler

Paket boyutu, seçilen dil, bağımlılık sayısı ve başlangıç sırasında yapılan işler sonucu doğrudan etkiler. Java ve .NET gibi runtime’lar çoğu senaryoda Node.js veya Python’dan daha fazla başlangıç süresine ihtiyaç duyabilir. VPC bağlantısı, büyük framework’ler, sır yönetimi ve ilk çağrıda açılan veritabanı bağlantıları da tabloya yeni milisaniyeler ekler.

Ayrıca ani trafik artışında tek bir sıcak konteyner yeterli olmaz. On eşzamanlı istek için platform birden fazla ortam oluşturabilir. Yani dakikada bir “uyandırma” isteği göndermek, ölçeklenme sırasında oluşan cold start’ları tamamen engellemez.

## Başlangıç kodunu hafifletmek

Aşağıdaki Python örneğinde istemci global kapsamda oluşturulur. Böylece her sıcak çağrıda yeniden hazırlanmaz:

```python
import boto3

# Konteyner başlatılırken yalnızca bir kez oluşturulur.
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("products")

def handler(event, context):
    product_id = event["pathParameters"]["id"]
    response = table.get_item(Key={"id": product_id})
    return {
        "statusCode": 200,
        "body": str(response.get("Item", {}))
    }
```

Bu yöntem ilk açılışı tamamen yok etmez; ancak sonraki çağrıları hızlandırır. Kullanılmayan kütüphaneleri paketten çıkarmak, modüler import kullanmak ve başlangıçta uzak servislere gereksiz istek göndermemek de önemlidir.

## Cold start önleme stratejileri

**Provisioned Concurrency**, belirli sayıda Lambda ortamını sürekli hazır tutar. Kritik API’lerde en güvenilir çözümdür fakat trafik olmasa bile ücret üretir. Zamanlanmış “keep-warm” çağrıları daha ucuz görünebilir, ancak sağlayıcının aynı konteyneri koruyacağı garanti edilmez.

| Strateji | Avantaj | Dezavantaj |
|---|---|---|
| Küçük dağıtım paketi | Ücretsiz ve etkili | Optimizasyon emeği ister |
| Provisioned Concurrency | Öngörülebilir gecikme | Sürekli maliyet oluşturur |
| Zamanlanmış çağrı | Kurulumu kolaydır | Ölçeklenmeyi garanti etmez |
| Daha fazla bellek | CPU gücünü de artırabilir | Çağrı maliyeti yükselir |
| Trafiği kuyruklamak | Ani yükü dengeler | Senkron API’ye uygun değildir |

Bellek artırmak yalnızca kapasite sağlamakla kalmaz; birçok platformda CPU payını da yükselterek başlatmayı hızlandırır. En doğru değer, tahminle değil yük testiyle bulunmalıdır.

Sonuç olarak serverless kötü ya da yavaş değildir; yalnızca performans modeli geleneksel sunuculardan farklıdır. Kullanıcıya dönük kritik uçlarda p95 ve p99 metriklerini izlemek, provisioned kapasiteyi yoğun saatlere göre planlamak ve başlangıç kodunu sadeleştirmek gerekir. Bazen en iyi çözüm Lambda’yı optimize etmek, bazen de sürekli çalışan bir konteyner hizmetine geçmektir. Mimari romantizm yerine ölçüm kazansın!

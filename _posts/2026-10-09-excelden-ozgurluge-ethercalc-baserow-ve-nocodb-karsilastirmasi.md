---
layout: post
title: "Excel’den Özgürlüğe: EtherCalc, Baserow ve NocoDB Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - ethercalc
  - baserow
  - nocodb
  - veritabanı
  - no-code
  - açık-kaynak
toc: true
image: /img/excelden-ozgurluge-ethercalc-70.png
---

Elektronik tablolar küçük ekiplerin İsviçre çakısıdır: stok tutulur, görevler izlenir, hatta müşteri ilişkileri yönetilmeye çalışılır. Ancak dosyalar büyüdükçe formüller kırılır, kopyalar çoğalır ve “son sürüm hangisi?” sorusu yankılanmaya başlar. Açık kaynaklı EtherCalc, Baserow ve NocoDB; bu karmaşaya farklı seviyelerde düzen getiren, tarayıcı üzerinden kullanılabilen üç güçlü alternatiftir.

``

## Aynı tablo, farklı düşünce biçimleri

Bu araçları karşılaştırmadan önce elektronik tablo ile veritabanı arasındaki temel farkı anlamalıyız. Elektronik tabloda hücreler merkezdedir; veritabanında ise kayıtlar, alanlar ve aralarındaki ilişkiler önemlidir.

Bir sipariş tablosunun toplam tutarı basitçe şöyle hesaplanabilir:

$$T = \sum_{i=1}^{n} q_i \times p_i$$

Burada $q_i$ ürün miktarını, $p_i$ birim fiyatı temsil eder. EtherCalc bu hesabı doğrudan hücre formülleriyle yapar. Baserow ve NocoDB ise miktar ile fiyatı yapılandırılmış alanlarda saklayıp hesaplanan alanlar veya sorgular üzerinden işler. Veri büyüdüğünde bu ayrım oldukça önemlidir.

| Özellik | EtherCalc | Baserow | NocoDB |
|---|---|---|---|
| Temel yaklaşım | Ortak elektronik tablo | No-code veritabanı | Veritabanına tablo arayüzü |
| Öğrenme eğrisi | Çok düşük | Düşük | Orta |
| İlişkisel veri | Sınırlı | Güçlü | Çok güçlü |
| Mevcut SQL desteği | Yok | Ana odak değil | Temel kullanım amacı |
| İdeal kullanıcı | Hızlı iş birliği isteyen ekip | Teknik olmayan ürün ekipleri | SQL altyapısı bulunan ekipler |

![excelden-ozgurluge-ethercalc-70](/img/excelden-ozgurluge-ethercalc-70.svg)


## EtherCalc: Hemen aç, birlikte yaz

EtherCalc, Google Sheets benzeri gerçek zamanlı bir çalışma deneyimi sunar. Hesap oluşturma zorunluluğu olmadan tablo paylaşabilmesi, toplantılar, geçici listeler ve ortak hesaplamalar için büyük kolaylıktır. Formül bilen biri araca neredeyse anında uyum sağlar.

Bununla birlikte EtherCalc bir veritabanı değildir. Karmaşık kayıt ilişkileri, ayrıntılı yetkilendirme veya gelişmiş otomasyon gerektiğinde sınırlarına çabuk ulaşır. Kısacası hızlıdır; fakat kurumsal veri mimarisinin omurgası olmaya çalışmaz.

## Baserow: Tablodan uygulamaya geçiş

Baserow, elektronik tablo rahatlığını ilişkisel veritabanı disipliniyle birleştirir. Metin, sayı, seçim, dosya ve bağlantılı kayıt gibi alan türleri tanımlanabilir. Örneğin müşteriler ile siparişleri ayrı tablolarda tutup birbirine bağlayabilirsiniz. Böylece müşteri adı değiştiğinde yüzlerce satırı elle düzeltmeniz gerekmez.

Basit bir otomasyon istemcisi şu şekilde kayıt ekleyebilir:

```python
import requests

url = "https://baserow.example/api/database/rows/table/42/"
headers = {"Authorization": "Token API_ANAHTARI"}
data = {"Musteri": "Ada Yazılım", "Tutar": 4800, "Durum": "Yeni"}

response = requests.post(url, headers=headers, json=data)
response.raise_for_status()
print(response.json())
```

Bu kod, Baserow API’sine yeni bir satış kaydı gönderir. Gerçek projelerde anahtarın kaynak kod yerine ortam değişkeninde saklanması gerekir.

## NocoDB: SQL veritabanına kullanıcı dostu yüz

NocoDB’nin yıldızlaştığı nokta, mevcut SQL veritabanlarını anlaşılır bir tablo arayüzüne dönüştürmesidir. PostgreSQL veya MySQL kullanan bir ekip, teknik olmayan çalışanlara doğrudan SQL öğretmeden veriye erişim sağlayabilir. Görünümler, ilişkiler, API erişimi ve rol tabanlı izinler operasyon araçları geliştirmeyi kolaylaştırır.

| Senaryo | En uygun seçim | Neden? |
|---|---|---|
| Anlık ortak bütçe hesabı | EtherCalc | Kurulum ve öğrenme yükü azdır |
| İçerik takvimi veya CRM | Baserow | Alan türleri ve ilişkiler pratiktir |
| Mevcut PostgreSQL’i yönetmek | NocoDB | SQL altyapısını görsel arayüze taşır |

## Hangisini seçmelisiniz?

Karar formülünü basitleştirirsek, seçim puanı $S$; kullanım kolaylığı $K$, veri ilişkisi ihtiyacı $R$ ve mevcut altyapıyla uyum $U$ üzerinden düşünülebilir:

$$S = 0.3K + 0.4R + 0.3U$$

Sadece birlikte hücre düzenlemek istiyorsanız EtherCalc yeterlidir. Kod yazmadan düzenli bir iş uygulaması kuracaksanız Baserow daha dengeli bir seçimdir. Halihazırda SQL veritabanınız varsa NocoDB en doğal köprüdür. Üçü de kendi sunucunuza kurulabildiği için veri kontrolü sağlar; ancak yedekleme, güncelleme ve erişim güvenliği sorumluluğunu da size bırakır. Yani özgürlük ücretsizdir, fakat sistem yöneticisi kahvesi bütçeye dahildir!

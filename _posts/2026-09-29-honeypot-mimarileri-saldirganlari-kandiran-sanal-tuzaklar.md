---
layout: post
title: "Honeypot Mimarileri: Saldırganları Kandıran Sanal Tuzaklar"
math: true
categories: 
  - Bilgi
tags: 
  - siber güvenlik
  - honeypot
  - tehdit istihbaratı
  - ağ güvenliği
  - olay müdahalesi
toc: true
image: /img/honeypot-mimarileri-saldirganlari-91.png
---

Bir saldırgan ağınıza girdiğinde gerçek sunucularınızla ilgilenmesini istemezsiniz. Bunun yerine karşısına eski sürüm izlenimi veren servisler, sahte kullanıcı hesapları ve dokunulmayı bekleyen sözde gizli dosyalar çıkarabilirsiniz. **Honeypot**, gerçek hedefleri taklit eden fakat temel amacı saldırıyı gözlemlemek olan kontrollü bir tuzaktır. Kısacası dijital peynir ücretsizdir; kapanın telemetrisi ise güvenlik ekibine kalır.

![honeypot-mimarileri-saldirganlari-91](/img/honeypot-mimarileri-saldirganlari-91.svg)

``

## Honeypot mantığı

Normal bir üretim sistemi kullanıcılara hizmet sunarken honeypot, kendisiyle kurulan şüpheli etkileşimleri kaydeder. Sistemin meşru bir işlevi bulunmadığından alınan bağlantıların büyük bölümü tarayıcılardan, otomatik botlardan veya saldırganlardan gelir. Bu özellik sinyal-gürültü oranını yükseltir.

Bir uyarının değerini basitçe şöyle düşünebiliriz:

$$
Değer = \frac{Şüpheli\ Etkileşim}{Toplam\ Etkileşim + 1}
$$

Üretim sunucusunda binlerce normal istek gürültü yaratırken honeypot üzerindeki tek bir oturum bile araştırmaya değer olabilir. Ancak tuzağın keşfedilmesi veya başka sistemlere saldırmak için kullanılması ihtimali nedeniyle izolasyon şarttır.

## Etkileşim seviyeleri

| Mimari | Taklit seviyesi | Sağladığı veri | Risk ve maliyet |
|---|---:|---|---|
| Düşük etkileşimli | Sınırlı protokol yanıtları | IP, zaman, istek kalıpları | Düşük |
| Orta etkileşimli | İnandırıcı servis akışları | Komut ve oturum davranışları | Orta |
| Yüksek etkileşimli | Gerçek işletim sistemi | Araçlar, teknikler ve kalıcılık girişimleri | Yüksek |
| Honeynet | Birden fazla sahte sistem | Yanal hareket ve saldırı zinciri | Çok yüksek |

Düşük etkileşimli sistemler internet taramalarını sınıflandırmak için idealdir. Yüksek etkileşimli sistemler ise bilinmeyen davranışları ve olası sıfır gün göstergelerini yakalayabilir; fakat saldırgana gerçek çalışma ortamı sundukları için sıkı biçimde denetlenmelidir.

## Güvenli mimari nasıl kurulur?

Sağlam bir tasarım üç düzlemden oluşur: **tuzak**, **izleme** ve **kontrol**. Tuzak ayrı bir VLAN veya bulut hesabında çalıştırılır. İzleme katmanı ağ akışlarını ve olay günlüklerini merkezi, tercihen değiştirilemez bir depoya yollar. Kontrol katmanıysa dışarı doğru bağlantıları güvenlik duvarı ve oran sınırlama kurallarıyla engeller.

Önerilen veri akışı şöyledir:

```text
İnternet → WAF/Güvenlik Duvarı → Honeypot VLAN'ı
                                  ↓
                           Salt yazılır günlük
                                  ↓
                           SIEM ve alarm sistemi
```

Honeypot hiçbir zaman hassas üretim verisi, gerçek parola veya müşteri kaydı içermemelidir. Sahte kimlik bilgileri benzersiz olmalı; başka ortamlarda çalışmamalıdır. Ayrıca kurulum yalnızca sahibi olduğunuz ya da açıkça yetkilendirildiğiniz altyapıda yapılmalıdır.

## Zararsız bir gözlem servisi

Aşağıdaki Python örneği yalnızca yerel arayüzde çalışan basit bir HTTP gözlem noktasıdır. Gelen isteğin zamanını ve yolunu kaydeder; gerçek bir servis açığı üretmez.

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone
import json

class TrapHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        event = {
            "time": datetime.now(timezone.utc).isoformat(),
            "client": self.client_address[0],
            "path": self.path,
            "agent": self.headers.get("User-Agent", "unknown")
        }
        print(json.dumps(event, ensure_ascii=False))
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Not Found")

HTTPServer(("127.0.0.1", 8080), TrapHandler).serve_forever()
```

Bu örnek eğitim laboratuvarı için başlangıçtır; internete doğrudan açılmamalıdır. Üretim benzeri gözlemlerde günlük bütünlüğü, kişisel veri mevzuatı, saklama süresi ve saat senkronizasyonu ayrıca ele alınmalıdır.

## Veriyi istihbarata dönüştürmek

Tek bir IP adresi kalıcı kanıt değildir. IP'ler değişebilir, paylaşılabilir veya ele geçirilmiş cihazlara ait olabilir. Bunun yerine istek sırası, kullanıcı aracısı, dosya adları, zamanlama ve kullanılan teknikler birlikte değerlendirilmelidir. Gözlemler MITRE ATT&CK gibi bir çerçeveyle eşleştirilerek savunma kurallarına dönüştürülebilir.

Başarılı honeypot, en çok saldırı alan değil, en anlamlı veriyi güvenli biçimde üreten sistemdir. Tuzak gerçekçi, ortam kontrollü ve ölçüm hedefleri açık olduğunda saldırganın merakı savunma ekibinin erken uyarı sistemine dönüşür.

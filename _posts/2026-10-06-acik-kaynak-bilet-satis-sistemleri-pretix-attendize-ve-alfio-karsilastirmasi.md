---
layout: post
title: "Açık Kaynak Bilet Satış Sistemleri: Pretix, Attendize ve Alf.io Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - bilet-satış
  - pretix
  - attendize
  - alfio
  - açık-kaynak
  - etkinlik-yönetimi
toc: true
image: /img/acik-kaynak-bilet-56.png
---

Konser, konferans veya atölye düzenlerken biletleri elektronik tabloyla takip etmek, küçük bir etkinliği bile hızla kaosa çevirebilir. Pretix, Attendize ve Alf.io; satış, kapasite, ödeme ve katılımcı yönetimini tek merkezde toplamayı amaçlayan açık kaynaklı çözümlerdir. Ancak benzer görünen bu üç sistem, teknoloji yığını ve kullanım yaklaşımı bakımından farklı karakterlere sahiptir.
``
## Bilet satış sisteminin temel mantığı

Bir bilet platformu yalnızca güzel bir ödeme sayfasından ibaret değildir. Sistemin aynı anda envanter yönetimi, sipariş oluşturma, ödeme doğrulama, bilet üretme ve giriş kontrolü yapması gerekir. En kritik konu, aynı son biletin iki kişiye satılmasını engellemektir.

Toplam kapasiteyi $C$, satılmış biletleri $S$, geçici olarak ayrılmış biletleri ise $R$ ile gösterirsek kullanılabilir bilet sayısı:

$$A = C - S - R$$

şeklinde hesaplanır. Kullanıcı ödeme ekranına geçtiğinde bilet genellikle birkaç dakika boyunca rezerve edilir. Ödeme tamamlanırsa $R$ azalırken $S$ artar; süre dolarsa rezervasyon serbest bırakılır. Bu işlemlerin atomik olması gerekir. Aksi hâlde sistem, matematiksel olarak imkânsız olan $A < 0$ durumuna düşebilir.

Gelir tahmini için daha basit bir model kullanılabilir. Bilet türü $i$ için fiyat $p_i$, satılan miktar $q_i$ ve ödeme sağlayıcısının değişken komisyon oranı $f$ olsun:

$$G_{net} = \sum_i p_i q_i (1-f) - G_{sabit}$$

Bu formül, platform seçerken yalnızca sunucu maliyetine değil ödeme komisyonlarına da bakılması gerektiğini gösterir.

## Üç adayın karşılaştırması

| Özellik | Pretix | Attendize | Alf.io |
|---|---|---|---|
| Temel teknoloji | Python, Django | PHP, Laravel | Java, Spring tabanlı yapı |
| Kullanım modeli | Bulut hizmeti ve self-hosted | Ağırlıklı olarak self-hosted | Self-hosted ve yönetilen seçenekler |
| Güçlü yönü | Gelişmiş biletleme ve eklenti ekosistemi | Geleneksel web hosting ortamlarına yakınlık | Etkinlik odaklı sade satış akışı |
| Uygun senaryo | Karmaşık ve çok oturumlu etkinlikler | PHP ekibine sahip küçük organizasyonlar | Teknik ekibi bulunan konferanslar |
| Dikkat edilmesi gereken | Kurulum ve yapılandırma ayrıntılı olabilir | Proje güncelliği ve eklenti uyumluluğu incelenmeli | Java altyapısı daha fazla kaynak isteyebilir |

### Pretix

Pretix; ürün çeşitleri, kuponlar, bekleme listeleri, koltuk planları ve giriş kontrolü gibi gelişmiş ihtiyaçlarda öne çıkar. Birden fazla etkinlik düzenleyen kuruluşlar için güçlü bir yönetim modeli sunar. API ve eklenti desteği sayesinde muhasebe, CRM veya özel raporlama araçlarıyla bütünleştirilebilir. Buna karşılık self-hosted kurulumunda veritabanı, önbellek, görev kuyruğu ve güncelleme süreçleri dikkatle yönetilmelidir.

### Attendize

Attendize, Laravel dünyasına aşina geliştiriciler için anlaşılır bir seçenektir. Etkinlik sayfası oluşturma, bilet kategorileri, siparişler ve katılımcı listeleri gibi temel özellikleri karşılar. Klasik PHP barındırma deneyimine yakın olsa da üretim kurulumu öncesinde aktif bakım durumu, güvenlik güncellemeleri ve kullanılan ödeme eklentileri mutlaka kontrol edilmelidir. Açık kaynak olmak, otomatik olarak güncel ve risksiz olmak anlamına gelmez.

### Alf.io

Alf.io, özellikle konferans ve topluluk etkinlikleri için pratik bir yaklaşım sunar. Bilet satışı, indirim kodları, bekleme listesi ve katılımcı yönetimi gibi işlevleri tek uygulamada birleştirir. Java ekosistemi kurumsal ekipler için avantaj sağlayabilir; ancak küçük bir VPS üzerinde PHP uygulamasına kıyasla daha dikkatli kaynak planlaması gerekebilir.

## Webhook ile sipariş işleme

Ödeme sonucunu tarayıcıdaki dönüş sayfasına güvenerek kaydetmek hatalıdır. Kullanıcı sekmeyi kapatabilir; buna karşın ödeme sağlayıcısının webhook bildirimi sunucuya ulaşabilir. Aşağıdaki Python örneği, bildirimin imzasını doğrulayıp siparişi tekrar işlememek için temel bir yaklaşım gösterir:

```python
from flask import Flask, request, abort
import hmac
import hashlib

app = Flask(__name__)
SECRET = b"webhook-secret"
processed = set()

@app.post("/payment-webhook")
def payment_webhook():
    body = request.get_data()
    received = request.headers.get("X-Signature", "")
    expected = hmac.new(SECRET, body, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(received, expected):
        abort(401)

    order_id = request.json["order_id"]
    if order_id not in processed:
        mark_order_as_paid(order_id)
        issue_ticket(order_id)
        processed.add(order_id)

    return {"status": "ok"}
```

Gerçek projede `processed` kümesi yerine veritabanında benzersiz kısıt kullanılmalıdır. Böylece uygulama yeniden başlatılsa bile aynı bildirimin ikinci kez bilet üretmesi engellenir.

## Hangisini seçmeli?

Gelişmiş özellikler ve genişletilebilirlik öncelikliyse Pretix güçlü bir başlangıçtır. Laravel bilen küçük bir ekip için Attendize değerlendirilebilir; ancak bakım geçmişi ayrıntılı incelenmelidir. Java altyapısına hâkim, sade fakat kapsamlı bir etkinlik akışı isteyen ekipler ise Alf.io’ya bakabilir. Son karardan önce ödeme sağlayıcısı desteği, yerel vergi kuralları, e-posta teslimatı, yedekleme ve QR kodlu giriş süreci gerçek bir deneme etkinliğiyle test edilmelidir.

![acik-kaynak-bilet-56](/img/acik-kaynak-bilet-56.svg)


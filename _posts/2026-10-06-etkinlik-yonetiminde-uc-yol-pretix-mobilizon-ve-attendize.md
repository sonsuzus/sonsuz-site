---
layout: post
title: "Etkinlik Yönetiminde Üç Yol: Pretix, Mobilizon ve Attendize"
math: true
categories: 
  - Program
tags: 
  - etkinlik yönetimi
  - pretix
  - mobilizon
  - attendize
  - açık kaynak
  - self-hosted
toc: true
image: /img/etkinlik-yonetiminde-uc-28.png
---

Bir etkinlik düzenlemek dışarıdan yalnızca tarih belirlemek ve katılımcıları çağırmak gibi görünebilir. Oysa biletleme, ödeme, kapasite, iletişim, gizlilik ve topluluk yönetimi işin içine girdiğinde küçük bir festival kadar karmaşık hâle gelir. Açık kaynak dünyasında Pretix, Mobilizon ve Attendize bu probleme farklı açılardan yaklaşan üç güçlü seçenektir.
``
## Önce problemi modelleyelim

Bir etkinlik yönetim sisteminin temel görevi; organizatör, etkinlik, katılımcı ve ödeme arasındaki ilişkileri tutarlı biçimde yönetmektir. Basit bir kapasite hesabı şöyle gösterilebilir:

$$Kalan\ Kapasite = Toplam\ Kontenjan - Onaylanan\ Kayıtlar$$

Ancak gerçek hayatta bekleme listeleri, iptaller, indirim kodları ve farklı bilet türleri bulunur. Bu nedenle sistem seçerken yalnızca özellik sayısına değil, ihtiyaçların ağırlığına bakmak gerekir. Örneğin ağırlıklı bir karar puanı şu şekilde hesaplanabilir:

$$Puan = 0.4B + 0.3T + 0.2G + 0.1K$$

Burada $B$ biletleme, $T$ topluluk özellikleri, $G$ gizlilik ve $K$ kurulum kolaylığı puanıdır. Katsayıları kendi projenize göre değiştirebilirsiniz; sonuçta bir konferans ile mahalle buluşmasının beklentileri aynı değildir.

## Üç platformun karakteri

| Platform | Ana yaklaşım | Güçlü olduğu alan | Dikkat edilmesi gereken nokta |
|---|---|---|---|
| Pretix | Profesyonel biletleme | Ödeme, kota, kupon ve giriş kontrolü | Kurulum ve yapılandırma daha kapsamlıdır |
| Mobilizon | Topluluk odaklı etkinlik ağı | Gruplar, federasyon ve gizlilik | Gelişmiş ticari biletleme temel amacı değildir |
| Attendize | Klasik etkinlik ve bilet satışı | Sade yönetim paneli ve özelleştirme | Sürüm güncelliği ve bakım durumu incelenmelidir |

![etkinlik-yonetiminde-uc-28](/img/etkinlik-yonetiminde-uc-28.svg)


### Pretix: Bilet gişesinin İsviçre çakısı

Pretix, ücretli konferanslar, atölyeler ve festivaller için öne çıkar. Birden fazla bilet kategorisi, kontenjan, indirim kodu, ödeme sağlayıcısı ve katılımcı kontrolü yönetilebilir. API desteği sayesinde CRM veya muhasebe araçlarıyla entegrasyon kurulabilir.

Pretix tercih edildiğinde sunucu kaynakları, e-posta teslimatı, ödeme web kancaları ve kişisel verilerin saklanma süresi ayrıca planlanmalıdır. Güçlü olması, varsayılan kurulumun her ihtiyaca otomatik olarak uyacağı anlamına gelmez.

### Mobilizon: Etkinlikten önce topluluk

Mobilizon, merkezi sosyal ağlara alternatif olmayı hedefleyen federasyonlu bir platformdur. ActivityPub kullanarak farklı Mobilizon sunucularının birbirleriyle iletişim kurmasına izin verir. Gruplar etkinlik yayımlayabilir, üyeler kaynak paylaşabilir ve kullanıcılar tek bir ticari platforma bağımlı kalmaz.

Bu yaklaşım özellikle dernekler, gönüllü topluluklar ve yerel oluşumlar için değerlidir. Önceliğiniz ödeme almaktan çok insanları düzenli biçimde bir araya getirmekse Mobilizon oldukça mantıklıdır.

### Attendize: Geleneksel ve anlaşılır

Attendize, PHP tabanlı bir etkinlik ve biletleme uygulamasıdır. Etkinlik sayfaları oluşturma, bilet satma ve katılımcı listelerini yönetme gibi tanıdık işlevler sunar. Laravel ekosistemine aşina ekipler kodu özelleştirmeyi daha rahat bulabilir.

Kurulumdan önce projenin güncel sürümü, bağımlılıkları, güvenlik yamaları ve topluluk hareketliliği kontrol edilmelidir. İnternete açık ödeme uygulamalarında eski bir dağıtımı doğrudan çalıştırmak iyi bir macera türü değildir.

## Küçük bir entegrasyon örneği

Etkinlik verisini başka bir servise aktaran basitleştirilmiş Python kodu şöyle olabilir:

```python
import requests

endpoint = 'https://ornek-etkinlik-sistemi.test/api/events'
response = requests.get(endpoint, timeout=10)
response.raise_for_status()

for event in response.json():
    print(event['name'], event.get('date', 'Tarih belirtilmemiş'))
```

Bu kod API uç noktasından etkinlikleri alır, HTTP hatalarını yakalar ve adlarıyla tarihlerini listeler. Gerçek projede erişim anahtarı çevre değişkeninde tutulmalı, sayfalama uygulanmalı ve hassas katılımcı verileri günlüklere yazılmamalıdır.

## Hangisini seçmeli?

Gelir üreten ve karmaşık bilet kuralları bulunan bir organizasyon için Pretix en güçlü adaydır. Topluluk bağımsızlığı, federasyon ve grup iletişimi önemliyse Mobilizon öne çıkar. Daha geleneksel, PHP tabanlı ve özelleştirilebilir bir başlangıç aranıyorsa Attendize değerlendirilebilir. Son kararı vermeden önce küçük bir deneme kurulumu yapmak, gerçek iş akışını canlandırmak ve yedekleme planını sınamak en sağlıklı yöntemdir.

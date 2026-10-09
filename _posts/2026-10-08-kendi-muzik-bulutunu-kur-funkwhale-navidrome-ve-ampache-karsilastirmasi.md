---
layout: post
title: "Kendi Müzik Bulutunu Kur: Funkwhale, Navidrome ve Ampache Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - müzik
  - self-hosted
  - funkwhale
  - navidrome
  - ampache
  - docker
toc: true
image: /img/kendi-muzik-bulutunu-29.png
---

Spotify rahat olabilir; ancak arşivinizin kontrolünü, dinleme geçmişinizi ve sunucunuzu başkasına bırakmak istemiyorsanız kendi müzik paylaşım sisteminizi kurabilirsiniz. Funkwhale, Navidrome ve Ampache bu işin üç güçlü adayıdır. Üçü de müziğinizi tarayıcıya ve mobil istemcilere ulaştırır, fakat mimarileri ve hedefledikleri kullanım biçimleri epey farklıdır.

``

## Temel mantık: Dosyadan müzik servisine

Bir müzik sunucusu yalnızca MP3 dosyalarını internete açmaz. Önce belirlediğiniz klasörleri tarar, ID3 veya Vorbis etiketlerinden sanatçı, albüm ve tür bilgilerini çıkarır, kapak görsellerini indeksler ve sonuçları bir veritabanına kaydeder. Kullanıcı oynat düğmesine bastığında dosya doğrudan gönderilebilir veya cihazın desteklediği formata **transcode** edilebilir.

Aynı anda dinleyen kullanıcıların ihtiyaç duyduğu yaklaşık bant genişliği şöyle hesaplanır:

$$B_{toplam} = n \times b$$

Burada $n$ eş zamanlı dinleyici sayısı, $b$ ise parça başına bit hızıdır. Örneğin 5 kullanıcı 320 kbps ses dinliyorsa gereken yükleme kapasitesi yaklaşık $5 \times 320 = 1600$ kbps olur. FLAC arşivlerinde bu değer hızla büyüdüğü için mobil kullanıcılara 128 veya 192 kbps dönüştürme yapmak mantıklıdır.

## Üç sistemin karakteri

| Özellik | Funkwhale | Navidrome | Ampache |
|---|---|---|---|
| Temel teknoloji | Python, Django, PostgreSQL | Go, SQLite | PHP, MySQL/MariaDB |
| Kaynak tüketimi | Görece yüksek | Çok düşük | Orta |
| Federasyon | ActivityPub ile güçlü | Yok | Sınırlı/yok |
| Subsonic istemcileri | Desteklenir | En güçlü yönlerinden biri | Desteklenir |
| İdeal kullanım | Topluluk ve paylaşım | Kişisel müzik sunucusu | Kapsamlı web arşivi |

![kendi-muzik-bulutunu-29](/img/kendi-muzik-bulutunu-29.svg)


**Funkwhale**, müzik dünyasının federasyon meraklısıdır. ActivityPub sayesinde farklı Funkwhale sunucuları birbirleriyle iletişim kurabilir. Kanallar, kütüphaneler, takip ve paylaşım özellikleriyle yalnızca kişisel oynatıcı değil, küçük bir bağımsız müzik topluluğu oluşturabilirsiniz. Bunun bedeli daha fazla servis, daha karmaşık kurulum ve daha yüksek RAM tüketimidir.

**Navidrome**, “klasörümü göster, gerisini hallet” yaklaşımını benimser. Go ile yazıldığı için tek çalıştırılabilir dosyayla bile ayağa kalkabilir. Subsonic ve OpenSubsonic uyumluluğu sayesinde Symfonium, Ultrasonic veya play:Sub gibi istemcilerle çalışır. Federasyon ya da sosyal ağ özellikleri sunmaz; buna karşılık hızlı, sade ve düşük güçlü ev sunucuları için idealdir.

**Ampache** ise bu üçlünün deneyimli arşiv yöneticisidir. PHP tabanlı yapısı klasik bir web sunucusu ortamına kolayca yerleşir. Geniş katalog yönetimi, kullanıcı yetkileri, çalma listeleri ve API seçenekleri sunar. Arayüzü Navidrome kadar minimalist değildir; fakat büyük ve düzenli koleksiyonlarda güçlü kontrol sağlar.

## Navidrome ile hızlı başlangıç

En hafif seçeneği denemek için aşağıdaki Docker Compose dosyası yeterlidir:

```yaml
services:
  navidrome:
    image: deluan/navidrome:latest
    user: "1000:1000"
    ports:
      - "4533:4533"
    environment:
      ND_SCANSCHEDULE: "1h"
      ND_LOGLEVEL: "info"
      ND_ENABLETRANSCODINGCONFIG: "true"
    volumes:
      - ./data:/data
      - /srv/music:/music:ro
    restart: unless-stopped
```

`/srv/music` arşivi salt okunur bağlanır; böylece uygulama yanlışlıkla parçalarınızı değiştiremez. `./data` ise veritabanını ve ayarları kalıcı tutar. `docker compose up -d` komutundan sonra `http://sunucu-adresi:4533` üzerinden ilk yönetici hesabı oluşturulur.

## Hangisini seçmeli?

Raspberry Pi, mini PC veya NAS üzerinde kişisel Spotify alternatifiniz olsun istiyorsanız **Navidrome** en pratik tercihtir. Müzik paylaşımını sosyal ve federatif bir yapıya taşımak istiyorsanız **Funkwhale** daha heyecan vericidir. PHP ekosistemine hâkimseniz, ayrıntılı kullanıcı ve katalog yönetimi arıyorsanız **Ampache** güçlü bir seçenektir.

Hangi sistemi kurarsanız kurun HTTPS, güçlü parolalar, düzenli yedekleme ve mümkünse ters proxy kullanın. Ayrıca yalnızca paylaşma hakkına sahip olduğunuz içerikleri yayımlayın. Kendi müzik bulutunuzu kurmak özgürlük getirir; sunucu yöneticiliği sorumluluğunu da çalma listesine ekler.

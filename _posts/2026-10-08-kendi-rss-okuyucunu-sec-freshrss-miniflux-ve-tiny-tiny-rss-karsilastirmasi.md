---
layout: post
title: "Kendi RSS Okuyucunu Seç: FreshRSS, Miniflux ve Tiny Tiny RSS Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - rss
  - freshrss
  - miniflux
  - tiny-tiny-rss
  - self-hosted
  - docker
toc: true
image: /img/kendi-rss-okuyucunu-93.png
---

İnternette sevdiğiniz siteleri tek tek ziyaret etmek yerine yeni içerikleri merkezi bir gelen kutusunda görmek ister misiniz? RSS okuyucuları tam olarak bunu sağlar. FreshRSS, Miniflux ve Tiny Tiny RSS ise verilerinizi üçüncü taraf platformlara teslim etmeden kendi sunucunuzda çalıştırabileceğiniz üç güçlü seçenektir. Gelin bu araçların çalışma mantığını, farklarını ve hangi senaryoda öne çıktıklarını inceleyelim.
``
## RSS okuyucu nasıl çalışır?

RSS, bir internet sitesinin güncel içeriklerini XML biçiminde yayımlamasını sağlayan standarttır. Akış içerisinde genellikle başlık, bağlantı, yayın tarihi, yazar ve içerik özeti bulunur. Okuyucu uygulama belirli aralıklarla bu XML belgesini indirir, daha önce görmediği kayıtları veritabanına ekler ve kullanıcıya okunabilir bir arayüz sunar.

Bir RSS sisteminin yaklaşık günlük istek sayısını şöyle düşünebiliriz:

$$I = N \times \frac{24 \times 60}{T}$$

Burada $N$ takip edilen akış sayısını, $T$ dakika cinsinden yenileme aralığını temsil eder. Örneğin 100 akışı 30 dakikada bir kontrol etmek teorik olarak günde $100 \times 48 = 4800$ HTTP isteği oluşturur. Bu nedenle çok sık güncelleme yapmak her zaman daha iyi değildir; hem sunucunuzu hem de içerik sağlayıcıları gereksiz yere yorabilir.

## Üç okuyucunun karakteri

| Özellik | FreshRSS | Miniflux | Tiny Tiny RSS |
|---|---|---|---|
| Temel teknoloji | PHP | Go | PHP |
| Arayüz yaklaşımı | Geleneksel ve esnek | Minimalist ve hızlı | Yoğun özellikli |
| Veritabanı | SQLite, MySQL, PostgreSQL | PostgreSQL | PostgreSQL |
| Eklenti desteği | Güçlü | Sınırlı | Güçlü |
| Kurulum kolaylığı | Kolay | Kolay | Orta |
| Kaynak tüketimi | Düşük | Çok düşük | Orta |
| İdeal kullanıcı | Özelleştirme sevenler | Sadelik arayanlar | İleri düzey kullanıcılar |

![kendi-rss-okuyucunu-93](/img/kendi-rss-okuyucunu-93.svg)


### FreshRSS

FreshRSS, dengeli bir çözüm arayanlar için güvenli tercihtir. Birden fazla veritabanını destekler, tema ve eklentilerle kişiselleştirilebilir. Klasörler, etiketler, filtreler ve çoklu kullanıcı desteği bakımından zengindir. Arayüzü ilk bakışta biraz klasik görünse de çok sayıda akışı yönetirken oldukça pratiktir.

### Miniflux

Miniflux, “az özellik, temiz deneyim” felsefesini benimser. Go ile geliştirildiği için hızlı çalışır ve düşük kaynak tüketir. Klavye kısayolları, sade okuma görünümü ve içerik temizleme yetenekleri başarılıdır. Ancak PostgreSQL zorunluluğu, yalnızca küçük bir SQLite dosyasıyla ilerlemek isteyen kullanıcılar için fazladan operasyon demektir.

### Tiny Tiny RSS

Tiny Tiny RSS, kısaca TT-RSS, ayrıntılı filtreleme ve eklenti seçenekleri isteyen deneyimli kullanıcılara hitap eder. Makaleleri kurallara göre etiketlemek, puanlamak veya işlemek mümkündür. Buna karşılık kurulumu ve bakımı diğer iki seçeneğe göre daha fazla dikkat ister. Güçlüdür; fakat kontrol panelindeki düğmelerle dostluk kurmanız biraz zaman alabilir.

## Docker ile örnek FreshRSS kurulumu

Aşağıdaki `compose.yaml` dosyası FreshRSS’i kalıcı veri alanı ve otomatik yeniden başlatma politikasıyla çalıştırır:

```yaml
services:
  freshrss:
    image: freshrss/freshrss:latest
    container_name: freshrss
    ports:
      - 8080:80
    volumes:
      - freshrss_data:/var/www/FreshRSS/data
      - freshrss_extensions:/var/www/FreshRSS/extensions
    environment:
      TZ: Europe/Istanbul
      CRON_MIN: '*/20'
    restart: unless-stopped

volumes:
  freshrss_data:
  freshrss_extensions:
```

`CRON_MIN` değeri akışların 20 dakikada bir yenilenmesini sağlar. Servisi başlatmak için dosyanın bulunduğu dizinde şu komut yeterlidir:

```bash
docker compose up -d
```

Ardından `http://sunucu-adresi:8080` adresini açarak kurulum sihirbazını tamamlayabilirsiniz. İnternet üzerinden erişim verecekseniz ters proxy, HTTPS ve düzenli yedekleme kullanmayı unutmayın.

## Hangisini seçmelisiniz?

Hızlı karar formülü basit: Esneklik ve kolay kurulum istiyorsanız **FreshRSS**, dikkat dağıtmayan hafif bir sistem arıyorsanız **Miniflux**, ayrıntılı kurallar ve eklentiler sizin için vazgeçilmezse **Tiny Tiny RSS** seçin. Kararsız kalan çoğu kullanıcı için FreshRSS iyi bir başlangıç noktasıdır; minimalistlerin gönlünü ise büyük olasılıkla Miniflux çalacaktır.

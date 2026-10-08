---
layout: post
title: "Kendi RSS Yayın Sistemini Kur: RSSHub, Feedgen ve WordPress RSS Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - rss
  - rsshub
  - feedgen
  - wordpress
  - xml
  - python
  - otomasyon
toc: true
image: /img/kendi-rss-yayin-12.png
---

İnternetteki içerikleri tek tek ziyaret etmek yerine hepsini kronolojik bir akışta okumak kulağa küçük bir süper güç gibi gelir. RSS, tam olarak bunu sağlayan açık ve sade bir yayın standardıdır. Bu rehberde hazır WordPress akışlarından Python Feedgen ile özel yayın üretmeye, RSSHub sayesinde akışı bulunmayan siteleri takip etmeye kadar uzanan pratik bir sistem kuracağız.

``

## RSS nasıl çalışır?

RSS yayını, çoğunlukla XML biçiminde sunulan ve içerik kayıtlarını belirli kurallarla sıralayan bir belgedir. Bir RSS okuyucu, yayının URL’sini düzenli aralıklarla sorgular; yeni bir `guid` veya daha güncel bir tarih gördüğünde kaydı kullanıcıya gösterir.

Basitleştirilmiş bir RSS belgesi şöyledir:

```xml
<rss version="2.0">
  <channel>
    <title>Teknoloji Günlüğü</title>
    <link>https://ornek.com</link>
    <item>
      <title>Yeni Yazı</title>
      <link>https://ornek.com/yeni-yazi</link>
      <guid>yazi-42</guid>
    </item>
  </channel>
</rss>
```

Sorgulama aralığı $T$, günlük istek sayısı ise yaklaşık $N$ olsun. Tek bir okuyucu için yük şu şekilde düşünülebilir:

$$N = \frac{86400}{T}$$

Örneğin her 30 dakikada bir kontrol yapıldığında $T=1800$ olur ve günde yaklaşık 48 istek gönderilir. Çok sık sorgulamak güncelliği artırır; ancak sunucu yükünü de büyütür. Önbellekleme bu dengenin gizli kahramanıdır.

## Üç yaklaşımın karşılaştırması

| Araç | En uygun senaryo | Güçlü yanı | Dikkat edilmesi gereken |
|---|---|---|---|
| WordPress RSS | WordPress içeriklerini yayınlamak | Yerleşik ve zahmetsizdir | Tema veya eklenti akışı değiştirebilir |
| Feedgen | Kendi verinden RSS üretmek | Tam kontrol sağlar | Barındırma ve güncelleme sana aittir |
| RSSHub | RSS sunmayan kaynakları izlemek | Çok sayıda hazır rota içerir | Kaynak değişince rota bozulabilir |

## WordPress RSS akışını kullanmak

WordPress çoğu kurulumda RSS üretimini otomatik yapar. Ana yayın genellikle aşağıdaki adrestedir:

```text
https://siteadresi.com/feed/
```

Kategoriye özel yayın için `/category/yazilim/feed/`, yorumlar için `/comments/feed/` kullanılabilir. `functions.php` veya SEO eklentileriyle özet, görsel ve özel alanlar akışa eklenebilir. Ancak çekirdek dosyaları düzenlemek yerine çocuk tema ya da özel eklenti kullanmak güncellemelerde yaşanacak sürprizleri önler.

## Python Feedgen ile özel yayın

Veriler bir API’den, veritabanından veya küçük bir otomasyon betiğinden geliyorsa Feedgen oldukça kullanışlıdır:

```python
from feedgen.feed import FeedGenerator

feed = FeedGenerator()
feed.title("Haftalık Python Notları")
feed.link(href="https://ornek.com", rel="alternate")
feed.description("Otomatik oluşturulan yazılım notları")

entry = feed.add_entry()
entry.id("python-101")
entry.title("Generator Mantığı")
entry.link(href="https://ornek.com/generator")
entry.description("Bellek dostu yineleyicilere giriş.")

feed.rss_file("rss.xml")
```

Bu kod bir kanal oluşturur, kanala tek bir kayıt ekler ve sonucu `rss.xml` dosyasına yazar. Üretim ortamında her kayda benzersiz kimlik, yayın tarihi ve kalıcı bağlantı eklemek gerekir. Betiği cron ile periyodik çalıştırarak tamamen otomatik bir yayın hattı kurulabilir.

## RSSHub ile akışı olmayan kaynaklar

RSSHub, desteklediği platformları “rota” adı verilen adreslerle RSS’e dönüştürür. Docker ile yerel kurulum yapılabilir:

```bash
docker run -d --name rsshub -p 1200:1200 diygod/rsshub
```

Ardından akışlara `http://localhost:1200/rota/parametre` biçiminde erişilir. Gerçek rota, takip edilen platforma göre RSSHub belgelerinden seçilir. Herkese açık örnek sunucular deneme için uygundur; düzenli kullanımda kendi örneğini barındırmak hız, gizlilik ve kota kontrolü sağlar.

## Sağlam bir yayın için son dokunuşlar

RSS çıktısını bir XML doğrulayıcıyla test et, açıklamalardaki HTML’i güvenli biçimde temizle ve `ETag` ile `Last-Modified` başlıklarını etkinleştir. Böylece okuyucular değişmeyen dosyayı tekrar indirmez. Kısacası WordPress hızlı başlangıç, Feedgen özel üretim, RSSHub ise keşif ve dönüştürme aracıdır. Üçünü birlikte kullandığında dağınık internet, düzenli ve sana ait bir haber merkezine dönüşür.

![kendi-rss-yayin-12](/img/kendi-rss-yayin-12.svg)


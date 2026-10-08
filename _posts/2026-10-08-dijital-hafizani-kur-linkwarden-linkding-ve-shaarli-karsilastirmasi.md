---
layout: post
title: "Dijital Hafızanı Kur: Linkwarden, Linkding ve Shaarli Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - yer imi
  - linkwarden
  - linkding
  - shaarli
  - self-hosted
  - docker
toc: true
image: /img/dijital-hafizani-kur-71.png
---

Tarayıcı yer imleri bir süre sonra çekmecedeki kablolara benzer: Hepsinin önemli olduğuna eminsindir ama hangisinin ne işe yaradığını bulamazsın. Linkwarden, Linkding ve Shaarli; bağlantıları etiketleyerek saklamayı, aramayı ve kendi sunucunda yönetmeyi sağlayan açık kaynaklı yer imi araçlarıdır. Böylece tarayıcıya veya ticari bir servise bağımlı kalmadan kişisel bir dijital kütüphane kurabilirsin.
``
## Yer imi sistemi aslında ne yapar?

İyi bir bookmark sistemi yalnızca URL depolamaz. Bir bağlantıyı; başlık, açıklama, etiket, eklenme tarihi ve arşivlenmiş içerikle birlikte saklar. Teorik olarak her kaydı şu kümeyle gösterebiliriz:

$$B = \{u, t, d, E, z, a\}$$

Burada $u$ adresi, $t$ başlığı, $d$ açıklamayı, $E$ etiketler kümesini, $z$ eklenme zamanını ve $a$ arşiv kopyasını temsil eder. Etiketleme sayesinde arama alanı küçülür. Toplam $N$ bağlantının yalnızca belirli bir etikete ait $k$ tanesini incelemek, zihinsel yükü kabaca $N$ öğeden $k$ öğeye indirir.

Örneğin `python`, `veritabanı` ve `okunacak` etiketlerinin kesişimi şöyle düşünülebilir:

$$S = E_{python} \cap E_{veritabanı} \cap E_{okunacak}$$

Bu yaklaşım klasörlerden daha esnektir; çünkü aynı bağlantı birden fazla bağlama ait olabilir.

## Üç aracın karakteri

| Özellik | Linkwarden | Linkding | Shaarli |
|---|---|---|---|
| Arayüz | Modern ve görsel | Sade ve hızlı | Minimal, klasik |
| Sayfa arşivleme | Güçlü; ekran görüntüsü ve belge | Temel kullanım odaklı | Sınırlı |
| Çoklu kullanıcı | Uygun | Daha çok kişisel kullanım | Temelde kişisel |
| Kaynak tüketimi | Görece yüksek | Düşük | Çok düşük |
| Teknoloji | Next.js, PostgreSQL | Python, SQLite | PHP, dosya tabanlı |
| En iyi senaryo | Ekip ve kalıcı arşiv | Hızlı kişisel koleksiyon | Küçük sunucu |

![dijital-hafizani-kur-71](/img/dijital-hafizani-kur-71.svg)


### Linkwarden

Linkwarden, bağlantı çürümesine karşı en güçlü seçenektir. Bir web sayfası silinse bile ekran görüntüsü veya PDF benzeri arşivleri koruyabilir. Koleksiyon paylaşımı ve kullanıcı yönetimi sayesinde ekipler için de uygundur. Bunun bedeli daha fazla RAM, depolama ve kurulum bileşenidir.

### Linkding

Linkding, “yer imimi ekleyeyim ve hemen bulayım” yaklaşımını benimser. Arayüzü dikkat dağıtmaz; etiketleme, arama, içe aktarma ve tarayıcı eklentileri günlük kullanımda oldukça yeterlidir. SQLite kullanması yedeklemeyi de kolaylaştırır: Çoğu durumda veritabanı dosyasını güvenli biçimde kopyalamak yeterlidir.

### Shaarli

Shaarli, eski bir dizüstünü sunucuya dönüştürenlerin kahramanıdır. PHP çalıştırabilen mütevazı bir sunucuda yaşayabilir ve veritabanı sunucusu gerektirmez. Arayüzü rakipleri kadar modern değildir; fakat taşınabilirlik ve sadelik konusunda oldukça güçlüdür.

## Docker ile Linkding kurulumu

Aşağıdaki `compose.yaml`, Linkding servisini başlatır ve verileri kalıcı bir klasörde tutar:

```yaml
services:
  linkding:
    image: sissbruecker/linkding:latest
    container_name: linkding
    ports:
      - "9090:9090"
    volumes:
      - ./data:/etc/linkding/data
    environment:
      - LD_SUPERUSER_NAME=admin
      - LD_SUPERUSER_PASSWORD=guclu-bir-parola
    restart: unless-stopped
```

Dosyanın bulunduğu dizinde şu komutu çalıştır:

```bash
docker compose up -d
```

Ardından `http://sunucu-adresi:9090` üzerinden giriş yapabilirsin. `volumes` bölümü, konteyner silinse bile kayıtların `data` klasöründe kalmasını sağlar. Gerçek kullanımda güçlü parola, HTTPS ve düzenli yedekleme şarttır; yönetim panelini doğrudan internete açmak iyi bir macera türü değildir.

## Hangisini seçmelisin?

Kalıcı web arşivi ve ekip paylaşımı istiyorsan **Linkwarden**, hızlı ve dengeli bir kişisel sistem arıyorsan **Linkding**, en düşük kaynak tüketimiyle bağımsızlık hedefliyorsan **Shaarli** seç. En iyi araç, yüzlerce özelliği olan değil, yeni bağlantı eklemeyi erteletmeyecek kadar rahat olandır. Sistemi seçtikten sonra az sayıda tutarlı etiket belirle, tarayıcıdaki eski yer imlerini içe aktar ve otomatik yedekleme kur. Dijital çekmecen sonunda gerçekten düzenli kalabilir.

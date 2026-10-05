---
layout: post
title: "Kendi Podcast Üssünü Kur: Castopod, Funkwhale ve Podcast Generator Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - podcast
  - castopod
  - funkwhale
  - podcast-generator
  - rss
  - açık-kaynak
  - self-hosted
toc: true
image: /img/kendi-podcast-ussunu-34.png
---

Podcast yayımlamak yalnızca bir MP3 dosyasını internete bırakmak değildir. Bölümlerin düzenlenmesi, RSS akışının üretilmesi, kapak görsellerinin sunulması ve Spotify ya da Apple Podcasts gibi dizinlere doğru bilgilerin gönderilmesi gerekir. Bu işi kendi sunucunda yapmak istiyorsan Castopod, Funkwhale ve Podcast Generator üç güçlü açık kaynak seçenektir. Gel, mikrofonu açıp bu sistemlerin perde arkasına bakalım.
``
## Podcast yayıncılığının temel mantığı

Bir podcast sisteminin kalbinde **RSS akışı** bulunur. RSS dosyası; program adı, açıklama, bölüm tarihi ve ses dosyasının adresi gibi bilgileri XML biçiminde taşır. Her bölüm genellikle bir `<item>`, ses dosyası ise bir `<enclosure>` etiketiyle tanımlanır.

```xml
<item>
  <title>Yapay Zekâ ile Kodlama</title>
  <enclosure
    url="https://podcast.example.com/bolum-1.mp3"
    type="audio/mpeg"
    length="24576000" />
</item>
```

Bu örnekte `enclosure`, podcast uygulamasına indirilecek dosyanın adresini, biçimini ve bayt cinsinden boyutunu bildirir. Dinleyici uygulaması RSS akışını belirli aralıklarla kontrol eder; yeni bir `<item>` gördüğünde bölümü kullanıcıya sunar.

Sunucu kapasitesi planlanırken trafik hesabı önemlidir. Bir bölümün ortalama boyutu $S$, indirilme sayısı $N$ ise yaklaşık veri transferi:

$$B = S \times N$$

Örneğin 50 MB büyüklüğündeki bir bölüm 2.000 kez indirilirse yaklaşık $100\,000$ MB, yani 100 GB trafik oluşur. Kısacası mikrofon küçük olabilir ama bant genişliği iştahlıdır!

## Üç sistemin karşılaştırması

| Özellik | Castopod | Funkwhale | Podcast Generator |
|---|---|---|---|
| Temel amaç | Profesyonel podcast yayını | Merkeziyetsiz ses platformu | Basit podcast üretimi |
| Kurulum zorluğu | Orta | Orta-ileri | Kolay |
| Çoklu podcast | Var | Kanal mantığıyla var | Sınırlı |
| Analitik | Gelişmiş | Temel/orta | Basit |
| ActivityPub | Var | Var | Yok |
| Kaynak ihtiyacı | Orta | Orta-yüksek | Düşük |
| İdeal kullanıcı | Yayıncı ve ekipler | Topluluklar | Bireysel üreticiler |

![kendi-podcast-ussunu-34](/img/kendi-podcast-ussunu-34.svg)


### Castopod

Castopod doğrudan podcast yayıncılığı için tasarlanmıştır. Çoklu program yönetimi, bölüm planlama, ayrıntılı istatistikler ve sosyal medya benzeri etkileşim özellikleri sunar. ActivityPub desteği sayesinde Mastodon gibi Fediverse platformlarındaki kullanıcılar programı takip edebilir.

Docker tabanlı kurulum, bileşenleri düzenli biçimde ayağa kaldırmayı kolaylaştırır:

```bash
# Yapılandırmada tanımlanan web, veritabanı ve önbellek
# servislerini arka planda başlatır.
docker compose up -d
```

Castopod; markalı bir yayın sitesi, ekip yönetimi ve ayrıntılı dinleme verileri isteyenler için en dengeli seçenektir. Buna karşılık veritabanı, depolama ve güncelleme süreçleri düzenli bakım ister.

### Funkwhale

Funkwhale yalnızca podcast değil, müzik ve genel ses içeriği barındırabilen merkeziyetsiz bir platformdur. ActivityPub federasyonu sayesinde farklı Funkwhale sunucuları birbirleriyle iletişim kurabilir. Bu yapı, tek bir yayın sitesinden çok topluluk tabanlı bir ses ağı kurmak isteyenlere hitap eder.

Mimarisinde web uygulaması, PostgreSQL, Redis ve görev kuyruğu gibi birden fazla bileşen bulunur. Bu nedenle küçük bir kişisel podcast için biraz ağır kalabilir. Ancak bağımsız sanatçıların, topluluk radyolarının ve ortak ses arşivlerinin aynı çatı altında buluşacağı projelerde oldukça güçlüdür.

### Podcast Generator

Podcast Generator, PHP tabanlı hafif bir çözümdür. Ses dosyalarını yükleyip bölüm bilgilerini girerek hızlıca RSS akışı oluşturabilirsin. Karmaşık sosyal özelliklere veya ileri analitiklere ihtiyaç duymayan kullanıcılar için “kur ve yayınla” yaklaşımı sunar.

Basitliği en büyük avantajı olduğu kadar sınırıdır. Büyük ekiplerde yetkilendirme, ayrıntılı raporlama ve federasyon beklentilerini karşılamaz. Buna rağmen düşük kaynaklı bir VPS, okul projesi veya kişisel yayın için ekonomik ve anlaşılırdır.

## Hangisini seçmelisin?

Profesyonel podcast yönetimi ve analitik istiyorsan **Castopod**, merkeziyetsiz bir ses topluluğu kuruyorsan **Funkwhale**, en az uğraşla klasik bir RSS yayını hazırlamak istiyorsan **Podcast Generator** daha uygundur. Seçim yaparken yalnızca özellik listesini değil; sunucu belleğini, yedekleme planını, beklenen trafiği ve bakım için ayırabileceğin zamanı da hesaba kat. Sonuçta iyi bir podcast sistemi sessiz çalışmalı; asıl duyulan senin içeriğin olmalıdır.

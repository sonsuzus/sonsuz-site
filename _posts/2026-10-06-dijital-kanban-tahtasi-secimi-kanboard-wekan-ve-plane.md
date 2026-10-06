---
layout: post
title: "Dijital Kanban Tahtası Seçimi: Kanboard, Wekan ve Plane"
math: true
categories: 
  - Program
tags: 
  - kanban
  - kanboard
  - wekan
  - plane
  - proje yönetimi
  - açık kaynak
toc: true
image: /img/dijital-kanban-tahtasi-75.png
---

![dijital-kanban-tahtasi-75](/img/dijital-kanban-tahtasi-75.svg)


Yapılacak işler büyüyüp yapışkan notlar monitörün kenarından taşmaya başladığında dijital bir Kanban tahtası hayat kurtarabilir. Açık kaynak dünyasında bu ihtiyaca farklı karakterlerle cevap veren üç güçlü seçenek bulunuyor: sade ve dayanıklı Kanboard, Trello benzeri Wekan ve modern ürün geliştirme deneyimi sunan Plane. Gelin bu araçların hangi ekipler için uygun olduğunu birlikte inceleyelim.
``

## Kanban’ın Arkasındaki Mantık

Kanban, işi görünür hâle getirerek akışı iyileştiren bir yönetim yöntemidir. En temel tahta `Yapılacak`, `Devam Ediyor` ve `Tamamlandı` sütunlarından oluşur. Kartlar soldan sağa ilerler; ancak amaç kartları yalnızca sürüklemek değil, darboğazları fark etmektir.

Sistemin önemli kavramı **WIP limiti**, yani aynı anda devam edebilecek iş sayısıdır. Beş geliştiricili bir ekip “Devam Ediyor” sütununu 12 kartla doldurursa herkes meşgul görünebilir, fakat işler tamamlanmak yerine bekler. WIP limiti 5 olduğunda ekip yeni işe başlamadan mevcut işi bitirmeye yönelir.

Kanban akışı Little Yasası ile özetlenebilir:

$$
WIP = Throughput \times CycleTime
$$

Burada **WIP** sistemdeki iş miktarı, **Throughput** belirli sürede tamamlanan kart sayısı, **Cycle Time** ise bir kartın tamamlanma süresidir. Haftada 10 kart tamamlayan ve ortalama çevrim süresi 2 hafta olan bir ekip için beklenen iş miktarı $10 \times 2 = 20$ karttır. Bu sayı sürekli yükseliyorsa süreçte trafik sıkışıklığı vardır.

## Üç Aracın Kısa Karşılaştırması

| Özellik | Kanboard | Wekan | Plane |
|---|---|---|---|
| Yaklaşım | Minimal Kanban | Görsel ve Trello benzeri | Modern ürün yönetimi |
| Kurulum | Hafif ve kolay | Orta düzey | Daha fazla servis gerektirir |
| Arayüz | Sade, işlevsel | Tanıdık, renkli | Şık ve geliştirici odaklı |
| Planlama | Temel | Orta | Döngü, modül ve görünüm desteği |
| Uygun ekip | Küçük ve teknik ekipler | Genel amaçlı ekipler | Yazılım ve ürün ekipleri |
| Kaynak ihtiyacı | Düşük | Orta | Görece yüksek |

## Kanboard: Az Konuşur, Çok İş Yapar

Kanboard; düşük kaynak tüketimi, otomatik eylemleri ve sade arayüzüyle öne çıkar. Eski bir mini sunucuda veya küçük VPS üzerinde çalıştırılabilir. Gösterişli raporlardan çok güvenilir bir görev tahtası arayan ekipler için idealdir.

Aşağıdaki Docker Compose yapılandırması Kanboard’u hızlıca ayağa kaldırır:

```yaml
services:
  kanboard:
    image: kanboard/kanboard:latest
    ports:
      - "8080:80"
    volumes:
      - kanboard_data:/var/www/app/data
      - kanboard_plugins:/var/www/app/plugins

volumes:
  kanboard_data:
  kanboard_plugins:
```

Bu yapılandırma uygulama verilerini ve eklentileri kalıcı volume’larda saklar. Tarayıcıdan `http://localhost:8080` adresine gidilerek arayüze erişilebilir.

## Wekan: Trello Hissini Sevenlere

Wekan; kart kapakları, etiketler, kontrol listeleri, yüzme kulvarları ve sürükle-bırak deneyimiyle kullanıcıların hızla alışabileceği bir araçtır. Teknik olmayan ekip üyeleri için geçiş süreci genellikle rahattır. İnsan kaynakları, içerik takvimi veya etkinlik planlaması gibi yazılım dışı süreçlerde de başarılıdır.

Buna karşılık MongoDB bağımlılığı ve bildirim ayarları nedeniyle Kanboard’dan biraz daha fazla operasyonel bakım isteyebilir. Çok sayıda pano açmayı seven ekipler ayrıca düzenli arşivleme kuralları belirlemelidir; aksi hâlde dijital masa da fiziksel masa kadar dağılabilir.

## Plane: Yeni Nesil Ürün Yönetimi

Plane yalnızca bir Kanban panosu değildir. Issue takibi, sprint benzeri **Cycles**, büyük işleri gruplamak için **Modules** ve farklı proje görünümleri sunar. Linear veya Jira yaklaşımına yakın, modern bir açık kaynak alternatif arayan yazılım ekiplerine hitap eder.

Plane’in güçlü özellikleri beraberinde daha karmaşık dağıtım ve daha yüksek kaynak ihtiyacı getirir. Bu nedenle tek kişinin alışveriş listesi için biraz roket motoru sayılabilir; ancak bir ürün ekibi için yol haritası ile günlük görevleri aynı ortamda birleştirmek ciddi avantajdır.

## Hangisini Seçmelisiniz?

Yalnızca güvenilir ve hafif bir pano gerekiyorsa **Kanboard**, Trello benzeri kolay kullanım önemliyse **Wekan**, yazılım geliştirme döngülerini ve ürün planlamasını birlikte yönetmek istiyorsanız **Plane** daha mantıklıdır. Son kararı vermeden önce aynı örnek projeyi üç araçta kurup kart oluşturma, filtreleme ve raporlama sürelerini ölçün. En iyi Kanban aracı en fazla özelliğe sahip olan değil, ekibin düzenli kullanarak işleri gerçekten tamamladığı araçtır.

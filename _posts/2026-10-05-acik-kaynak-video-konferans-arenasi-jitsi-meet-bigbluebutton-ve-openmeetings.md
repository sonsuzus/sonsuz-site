---
layout: post
title: "Açık Kaynak Video Konferans Arenası: Jitsi Meet, BigBlueButton ve OpenMeetings"
math: true
categories: 
  - Bilgi
tags: 
  - video konferans
  - jitsi meet
  - bigbluebutton
  - openmeetings
  - webrtc
  - açık kaynak
toc: true
image: /img/acik-kaynak-video-68.png
---

Uzaktan çalışma, çevrim içi eğitim ve dijital toplantılar artık günlük hayatın doğal parçaları. Ancak kendi video konferans altyapısını kurmak isteyenlerin karşısına üç güçlü açık kaynak seçeneği çıkıyor: Jitsi Meet, BigBlueButton ve Apache OpenMeetings. Üçü de görüntülü iletişim sağlasa da hedefleri, mimarileri ve sundukları araçlar oldukça farklı. Kısacası aynı yarış pistindeler, fakat araç sınıfları aynı değil.

![acik-kaynak-video-68](/img/acik-kaynak-video-68.svg)

``

## Video konferansın teorik temeli

Bir video konferans sistemi yalnızca kameradan gelen görüntüyü diğer kullanıcıya aktaran bir uygulama değildir. Ses ve görüntünün kodlanması, ağ üzerinden taşınması, gecikmenin yönetilmesi ve katılımcılar arasında dağıtılması gerekir. Modern sistemlerde bu iş için çoğunlukla **WebRTC** kullanılır.

Ham verinin ihtiyaç duyduğu bant genişliği yaklaşık olarak şöyle düşünülebilir:

$$B_{toplam} = B_{video} + B_{ses} + B_{protokol}$$

Örneğin video akışı $1.5\ Mbps$, ses akışı $0.1\ Mbps$ ve protokol yükü $0.1\ Mbps$ ise tek akış yaklaşık $1.7\ Mbps$ tüketir. Katılımcı sayısı arttığında sunucu mimarisi kritik hâle gelir.

**P2P** modelinde kullanıcılar doğrudan haberleşir. Bu yöntem küçük görüşmelerde ekonomiktir. **SFU** mimarisinde ise istemciler görüntülerini merkezi bir sunucuya gönderir; sunucu akışları diğer katılımcılara yönlendirir. Yaklaşık sunucu çıkış yükü, $n$ katılımcı için şu şekilde büyüyebilir:

$$B_{çıkış} \approx n(n-1)b$$

Buradaki $b$, katılımcı başına ortalama akış hızıdır. Bu nedenle “Sunucuyu kurdum, artık bin kişi girer!” yaklaşımı genellikle kısa sürede işlemci fanlarının protestosuyla sonuçlanır.

## Üç platformun karşılaştırması

| Özellik | Jitsi Meet | BigBlueButton | OpenMeetings |
|---|---|---|---|
| Temel amaç | Hızlı toplantı | Çevrim içi eğitim | Toplantı ve iş birliği |
| Kullanım kolaylığı | Çok yüksek | Orta | Orta |
| Sanal sınıf araçları | Sınırlı | Çok güçlü | Güçlü |
| LMS entegrasyonu | Harici çözümlerle | Moodle ve benzerleriyle güçlü | Eklentilerle mümkün |
| Kayıt | Yapılandırma gerektirir | Yerleşik ve gelişmiş | Desteklenir |
| Kurulum yükü | Görece düşük | Yüksek | Orta-yüksek |

## Jitsi Meet: Toplantıya hızlı giriş

Jitsi Meet, kullanıcıların tarayıcı üzerinden kolayca toplantı oluşturmasını hedefler. Hesapsız oda açma, ekran paylaşımı, sohbet, el kaldırma ve mobil uygulama desteği sunar. Jitsi Videobridge bileşeni bir SFU gibi çalışarak medya akışlarını dağıtır.

Docker ile temel bir kurulum hazırlığı şu şekilde başlatılabilir:

```bash
git clone https://github.com/jitsi/docker-jitsi-meet.git
cd docker-jitsi-meet
cp env.example .env
./gen-passwords.sh
docker compose up -d
```

Bu komutlar projeyi indirir, örnek ortam ayarlarını kopyalar, güvenli parolalar üretir ve servisleri arka planda çalıştırır. Üretim ortamında HTTPS, alan adı, güvenlik duvarı ve kullanıcı doğrulaması ayrıca yapılandırılmalıdır.

## BigBlueButton: Dijital sınıfın ağır sıkleti

BigBlueButton özellikle eğitim için tasarlanmıştır. Sunum yükleme, ortak beyaz tahta, anket, grup odaları, ders kaydı, katılım takibi ve moderatör kontrolleri sunar. Bir öğretmenin ihtiyaç duyabileceği araçların çoğu aynı arayüzde bulunur.

Bunun karşılığında kurulum ve kaynak ihtiyacı daha yüksektir. Temiz bir Ubuntu sunucusu, doğru DNS kayıtları ve yeterli işlemci kapasitesi önemlidir. Çok sayıda eş zamanlı sınıf planlanıyorsa yük dengeleme ve izleme çözümleri de hesaba katılmalıdır.

## OpenMeetings: Esnek iş birliği merkezi

Apache OpenMeetings; görüntülü görüşme, beyaz tahta, dosya paylaşımı, takvim ve toplantı kaydı özelliklerini bir araya getirir. Eğitimde kullanılabilse de genel ekip çalışmasına daha yakın, geleneksel bir toplantı odası deneyimi sunar. Java tabanlı yapısı nedeniyle uygulama sunucusu, veritabanı ve medya bileşenlerinin dikkatle yönetilmesi gerekir.

## Hangisini seçmeli?

Hızlı ve sade toplantılar için **Jitsi Meet**, kapsamlı sanal sınıflar için **BigBlueButton**, toplantı ile ortak çalışma araçlarını birleştirmek için **OpenMeetings** daha uygundur. Son karar yalnızca özellik listesine göre verilmemelidir; eş zamanlı kullanıcı sayısı, kayıt ihtiyacı, yönetim deneyimi ve sunucu bütçesi birlikte değerlendirilmelidir. En iyi platform, en fazla düğmeye sahip olan değil, ekibin gerçek ihtiyacını en az operasyonel baş ağrısıyla karşılayandır.

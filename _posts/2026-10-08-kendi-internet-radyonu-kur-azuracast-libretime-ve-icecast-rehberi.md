---
layout: post
title: "Kendi İnternet Radyonu Kur: AzuraCast, LibreTime ve Icecast Rehberi"
math: true
categories: 
  - Proje
tags: 
  - internet radyo
  - azuracast
  - libretime
  - icecast
  - linux
  - docker
  - yayıncılık
toc: true
image: /img/kendi-internet-radyonu-19.png
---

İnternet radyosu kurmak, bir mikrofonu sunucuya bağlayıp müzik çalmaktan biraz daha fazlasıdır. Sesin kodlanması, yayın akışının yönetilmesi, dinleyicilere dağıtılması ve programların zamanlanması gerekir. Neyse ki AzuraCast, LibreTime ve Icecast sayesinde küçük bir odadan dünyanın dört bir yanına yayın yapmak artık oldukça erişilebilir.

``

## İnternet radyosu nasıl çalışır?

Tipik bir sistemde ses önce bir **kaynak istemci** tarafından MP3, AAC veya Opus biçiminde kodlanır. Kodlanmış veri Icecast gibi bir yayın sunucusuna gönderilir. Dinleyiciler ise belirli bir bağlantıya bağlanarak aynı akışı küçük bir tampon gecikmesiyle alır.

Temel mimari şöyledir:

```text
Mikrofon / Otomasyon
        |
        v
Kodlayıcı veya AutoDJ
        |
        v
Icecast Yayın Sunucusu
        |
        +----> Web oynatıcı
        +----> Mobil uygulama
        +----> Masaüstü oynatıcı
```

![kendi-internet-radyonu-19](/img/kendi-internet-radyonu-19.svg)


Gerekli bant genişliği yaklaşık olarak şu formülle hesaplanabilir:

$$B = N \times R$$

Burada $N$ eş zamanlı dinleyici sayısını, $R$ ise kişi başına bit hızını ifade eder. Örneğin 100 dinleyiciye 128 kbps yayın yaparsak:

$$100 \times 128 = 12800\text{ kbps} \approx 12.8\text{ Mbps}$$

Sunucunun diğer trafiğini de düşünerek bunun üzerinde bir bağlantı kapasitesi seçmek gerekir.

## Üç araç arasındaki fark

Bu yazılımlar aynı problemi farklı katmanlarda çözer. Icecast dağıtım motorudur; AzuraCast ve LibreTime ise otomasyon, takvim ve yönetim özellikleri sunar.

| Özellik | AzuraCast | LibreTime | Icecast |
|---|---|---|---|
| Web yönetim paneli | Gelişmiş | Gelişmiş | Temel durum sayfası |
| AutoDJ | Var | Var | Yok |
| Program takvimi | Var | Var | Yok |
| Canlı yayın desteği | Var | Var | Var |
| Docker kurulumu | Çok kolay | Kuruluma bağlı | Mümkün |
| Ana rol | Hepsi bir arada radyo | Yayın otomasyonu | Ses dağıtımı |

**AzuraCast**, hızlı başlangıç isteyenler için en pratik seçenektir. İstasyon oluşturma, müzik yükleme, çalma listeleri, DJ hesapları, istatistikler ve web oynatıcı tek panelde bulunur. Arka planda genellikle Liquidsoap ve Icecast gibi bileşenleri birlikte yönetir.

**LibreTime**, radyo programcılığı ve yayın akışı planlamasına odaklanır. Saatlik programlar, tekrarlar, önceden kaydedilmiş içerikler ve canlı stüdyo geçişleri için güçlüdür. Özellikle ekip halinde çalışan topluluk radyolarına uygundur.

**Icecast** ise daha yalındır. Otomasyon sağlamaz; kendisine gönderilen sesi `/radio.mp3` gibi bir bağlama noktası, yani *mount point* üzerinden dinleyicilere ulaştırır. Kendi panelini geliştirmek veya yalnızca dağıtım katmanı kurmak isteyenler için idealdir.

## AzuraCast ile hızlı kurulum

Docker destekli güncel bir Linux sunucusunda AzuraCast kurulum betiği kullanılabilir:

```bash
mkdir -p /var/azuracast
cd /var/azuracast
curl -fsSL https://get.azuracast.com | bash
```

Bu komut kurulum yöneticisini indirir ve gerekli konteynerleri hazırlar. İşlem tamamlandığında tarayıcıdan sunucunun adresine giderek yönetici hesabı ve ilk istasyon oluşturulur. Çalma listesine parçalar eklendiğinde AutoDJ yayına başlayabilir.

Alan adı kullanıyorsanız HTTPS yapılandırmayı unutmayın. Yönetim panelini doğrudan internete açmak yerine güçlü parolalar, güvenlik duvarı ve düzenli yedekleme kullanmak önemlidir.

## Icecast bağlantısını test etmek

Sunucunun yayın durumunu terminalden kontrol etmek için şu komut kullanılabilir:

```bash
curl -I https://radyo.example.com/radio.mp3
```

Başarılı bir bağlantıda `200 OK` yanıtı görülür. Akışı VLC ile denemek için bağlantıyı doğrudan açabilir veya şu komutu çalıştırabilirsiniz:

```bash
vlc https://radyo.example.com/radio.mp3
```

## Hangisini seçmelisin?

Tek sunucuda hızla çalışan modern bir istasyon istiyorsan **AzuraCast**, ayrıntılı yayın takvimi ve ekip iş akışı arıyorsan **LibreTime**, özel bir sistem geliştiriyor ve yalnızca güvenilir ses dağıtımı istiyorsan **Icecast** seçebilirsin. Küçük başlayıp ölçüm yapmak en sağlıklısıdır: düşük bit hızında deneme yayını aç, gecikmeyi gözlemle, ardından dinleyici sayısına göre işlemci ve bant genişliğini artır. Böylece dijital frekansın parazitsiz, sunucun da dumansız çalışır!

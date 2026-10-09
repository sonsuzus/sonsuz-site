---
layout: post
title: "Kendi Dijital Karargâhını Kur: Heimdall, Homer ve Flame Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - self-hosted
  - heimdall
  - homer
  - flame
  - docker
  - homelab
  - dashboard
toc: true
image: /img/kendi-dijital-karargahini-96.png
---

Ev sunucunuzda onlarca uygulama çalışıyor, fakat hangisinin hangi portta olduğunu hatırlamak için tarayıcı geçmişinde arkeolojik kazı yapıyorsanız kişisel portal zamanı gelmiş demektir. Heimdall, Homer ve Flame; servislerinizi düzenli kartlar, simgeler ve kategoriler altında toplayan popüler self-hosted başlangıç sayfalarıdır.
``
## Kişisel portal ne işe yarar?

Portal sistemi, uygulamalarınızın kendisini barındırmaz; onlara ulaşabileceğiniz merkezi bir navigasyon katmanı oluşturur. Örneğin Jellyfin, Home Assistant, Grafana ve Portainer farklı adreslerde çalışırken portalınız tek bir URL üzerinden hepsine bağlantı sunar.

Bu yapıyı basitçe bir fonksiyon gibi düşünebiliriz:

$$P: S \rightarrow U$$

Burada $S$ servis adlarını, $U$ ise ilgili URL'leri temsil eder. Portalın asıl değeri bağlantı sayısı arttıkça ortaya çıkar. Kullanıcının ezberlemesi gereken adres sayısı $n$ iken iyi tasarlanmış bir portal bu zihinsel yükü yaklaşık olarak tek giriş noktasına indirir:

$$L_{portal} \approx 1, \qquad L_{ezber} = n$$

Elbette portal güvenlik duvarı veya kimlik doğrulama sistemi değildir. İnternete açılacaksa HTTPS, ters vekil sunucu ve mümkünse Authelia ya da Authentik gibi bir erişim katmanı kullanılmalıdır.

## Üç adayın karakteri

| Özellik | Heimdall | Homer | Flame |
|---|---|---|---|
| Yapı | Dinamik web uygulaması | Statik arayüz | Dinamik web uygulaması |
| Yapılandırma | Web paneli | YAML dosyası | Web paneli ve Docker etiketleri |
| Kaynak tüketimi | Orta | Çok düşük | Düşük-orta |
| Uygulama entegrasyonu | Güçlü | Temel bağlantılar | Otomatik keşif odaklı |
| İdeal kullanıcı | Görsel yönetim isteyen | GitOps ve sadelik seven | Docker ağırlıklı homelab sahibi |

### Heimdall: Gösterişli ve kullanışlı

Heimdall, uygulama kartlarını tarayıcı üzerinden eklemeyi kolaylaştırır. Bazı servisler için geliştirilmiş uygulama desteği sayesinde kartlarda ek bilgiler gösterilebilir. Dosya düzenlemek istemeyen, portalını aile üyelerine de kullandıracak kişiler için iyi bir seçimdir. Buna karşılık veritabanı ve uygulama çalışma zamanı nedeniyle Homer'dan daha fazla kaynak tüketir.

### Homer: YAML seven minimaliste

Homer büyük ölçüde statik çalışır ve yapılandırmasını YAML dosyasından alır. Bu dosyayı Git deposunda saklayabilir, değişiklik geçmişini izleyebilir ve farklı sunuculara kolayca taşıyabilirsiniz.

```yaml
---
title: Ev Laboratuvarım
services:
  - name: Medya
    items:
      - name: Jellyfin
        subtitle: Film ve diziler
        url: https://jellyfin.example.com
        icon: fas fa-play-circle
```

Bu yapılandırma bir **Medya** bölümü ve Jellyfin kartı oluşturur. Homer'ın sadeliği performans avantajıdır; ancak bağlantı eklemek için dosyayı düzenlemek, YAML girintilerine dikkat etmek gerekir. Tek bir hatalı boşluk küçük bir sabır sınavına dönüşebilir.

### Flame: Docker ile yakın arkadaş

Flame, görsel yönetim paneliyle uygulama ve yer imi eklemeyi kolaylaştırır. En dikkat çekici taraflarından biri, uygun Docker etiketleri kullanıldığında çalışan konteynerleri portalda gösterebilmesidir.

```yaml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    labels:
      - flame.type=application
      - flame.name=Uptime Kuma
      - flame.url=https://status.example.com
```

Etiketler, Flame'e konteynerin adını ve açılacak adresi bildirir. Böylece servis tanımı uygulamanın Docker Compose dosyasıyla birlikte yaşar; yeni kurulumlarda portal kartını ayrıca oluşturmanız gerekmez.

## Hangisini seçmelisiniz?

Sadece hızlı, taşınabilir ve sürüm kontrolüne uygun bir ana sayfa istiyorsanız **Homer** öne çıkar. Zengin uygulama kartları ve tamamen görsel yönetim arıyorsanız **Heimdall** daha rahattır. Servislerinizi Docker Compose ile yönetiyor ve otomatik keşif fikrini seviyorsanız **Flame** oldukça pratiktir.

Seçiminiz ne olursa olsun portalı yalnızca iç ağda yayınlamak, düzenli yedek almak ve yönetim arayüzünü güçlü parolayla korumak önemlidir. Sonuçta dijital karargâhınızın kapısını açık bırakmak, anahtarı paspasın altına koymanın teknolojik karşılığıdır.

![kendi-dijital-karargahini-96](/img/kendi-dijital-karargahini-96.svg)


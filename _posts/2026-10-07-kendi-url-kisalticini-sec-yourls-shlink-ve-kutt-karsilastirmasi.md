---
layout: post
title: "Kendi URL Kısaltıcını Seç: YOURLS, Shlink ve Kutt Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - url-kısaltma
  - yourls
  - shlink
  - kutt
  - self-hosted
  - web-geliştirme
toc: true
image: /img/kendi-url-kisalticini-51.png
---

Uzun bağlantıları birkaç karakterlik adreslere dönüştürmek basit görünür; ancak işin arkasında yönlendirme, benzersiz kod üretimi, analitik, önbellekleme ve güvenlik gibi önemli bileşenler bulunur. YOURLS, Shlink ve Kutt, bu sistemi kendi sunucusunda çalıştırmak isteyenler için öne çıkan açık kaynak seçeneklerdir. Gelin, bağlantıların küçüldüğü fakat mimari kararların büyüdüğü bu dünyaya yakından bakalım.
``
## URL kısaltma sistemi nasıl çalışır?

Bir kullanıcı `https://kisa.site/abc42` adresini ziyaret ettiğinde uygulama `abc42` anahtarını veri tabanında arar. Eşleşen uzun URL bulunduğunda sunucu genellikle `301`, `302`, `307` veya `308` yanıtıyla tarayıcıyı hedefe yönlendirir. Aynı sırada ziyaret zamanı, IP adresinin anonimleştirilmiş biçimi, yönlendiren sayfa ve kullanıcı aracısı gibi analitik bilgiler kaydedilebilir.

Rastgele üretilen bir kodun olası kombinasyon sayısı, kullanılan alfabe büyüklüğü $A$ ve kod uzunluğu $L$ ile yaklaşık olarak şöyle hesaplanır:

$$N = A^L$$

Örneğin 62 karakterlik `a-z`, `A-Z` ve `0-9` alfabesiyle altı karakter kullanılırsa $62^6 \approx 56{,}8$ milyar kombinasyon elde edilir. Fakat doğum günü paradoksu nedeniyle rastgele üretimde çakışma olasılığı beklenenden önce yükselir. Bu nedenle sistem kodu veri tabanında doğrulamalı, benzersiz indeks kullanmalı ve çakışma durumunda yeniden üretmelidir.

## Üç aracın kısa karşılaştırması

| Özellik | YOURLS | Shlink | Kutt |
|---|---|---|---|
| Temel teknoloji | PHP, MySQL | PHP, çeşitli veri tabanları | Node.js, PostgreSQL |
| Kurulum yaklaşımı | Geleneksel hosting dostu | Docker ve CLI odaklı | Modern web uygulaması |
| Yönetim arayüzü | Dahili ve sade | Ayrı web istemcisi kullanılabilir | Dahili, kullanıcı dostu |
| API | Eklentilerle genişletilebilir | Güçlü REST API | REST API |
| Güçlü tarafı | Basitlik ve eklenti ekosistemi | Otomasyon, analitik ve ölçeklenebilirlik | Modern görünüm ve kolay kullanım |
| Uygun senaryo | Kişisel veya küçük ekip | Profesyonel servis ve entegrasyon | Hızlı, görsel odaklı kurulum |

![kendi-url-kisalticini-51](/img/kendi-url-kisalticini-51.svg)


## YOURLS: Klasik ve hafif

YOURLS, özellikle PHP tabanlı paylaşımlı hosting kullananlar için pratik bir seçenektir. WordPress benzeri kurulumu, sade yönetim paneli ve eklenti sistemi sayesinde hızlıca kişiselleştirilebilir. Küçük bir marka, kişisel alan adında bağlantı üretmek istiyorsa gereksiz karmaşıklık yaratmaz.

Buna karşılık gelişmiş yetkilendirme, ayrıntılı analitik veya yüksek trafikli dağıtık mimari gerektiğinde ek geliştirme isteyebilir. Gücü sadeliğidir; aynı özellik büyük projelerde sınır hâline gelebilir.

## Shlink: API önce gelir

Shlink, komut satırı araçları ve kapsamlı API’siyle otomasyon seven geliştiricilere göz kırpar. QR kod üretimi, etiketleme, ziyaret analitiği, alan adı yönetimi ve webhook benzeri entegrasyon ihtiyaçlarında güçlüdür. Arka uç ile yönetim arayüzünün ayrılması, servisi farklı istemcilerden yönetmeyi kolaylaştırır.

Docker ile örnek bir başlangıç şöyle yapılabilir:

```bash
docker run --name shlink \
  -p 8080:8080 \
  -e DEFAULT_DOMAIN=kisa.example.com \
  -e IS_HTTPS_ENABLED=true \
  shlinkio/shlink:stable
```

Bu komut Shlink sunucusunu `8080` portunda başlatır. Gerçek kullanımda kalıcı veri tabanı, HTTPS sağlayan ters proxy ve güçlü API anahtarları ayrıca yapılandırılmalıdır.

## Kutt: Modern arayüz isteyenlere

Kutt, Node.js ekosistemi ve temiz arayüzüyle kullanıcıların hızla adapte olabileceği bir çözümdür. Özel kısa kodlar, hesap yönetimi, istatistikler ve API desteği sunar. Bununla birlikte kurulumdan önce projenin güncel bakım durumunu, bağımlılıklarını ve güvenlik yamalarını kontrol etmek önemlidir; açık kaynak projelerde geliştirme temposu zaman içinde değişebilir.

## Hangisini seçmeli?

Basit PHP hosting ve eklenti esnekliği için **YOURLS**, API merkezli otomasyon ve ciddi analitik ihtiyaçları için **Shlink**, modern bir kullanıcı deneyimi için **Kutt** mantıklı adaydır. Hangi aracı seçerseniz seçin HTTPS, kötü amaçlı URL engelleme, hız sınırlama, yedekleme ve gizlilik politikası zorunlu kabul edilmelidir. Çünkü kısa bağlantı küçük olabilir, fakat taşıdığı güvenlik sorumluluğu hiç de kısa değildir.

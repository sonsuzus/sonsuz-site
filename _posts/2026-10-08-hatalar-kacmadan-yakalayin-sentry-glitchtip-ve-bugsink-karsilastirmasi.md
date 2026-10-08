---
layout: post
title: "Hatalar Kaçmadan Yakalayın: Sentry, GlitchTip ve Bugsink Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - sentry
  - glitchtip
  - bugsink
  - hata-takibi
  - observability
  - python
toc: true
image: /img/hatalar-kacmadan-yakalayin-56.png
---

Uygulamanız geliştirme ortamında kusursuz çalışırken üretimde beklenmedik bir hata verebilir. Kullanıcının yalnızca “sayfa açılmadı” diye tarif ettiği bu olayın nedenini bulmak ise samanlıkta istisna aramaya benzer. Hata takip sistemleri; istisnaları, çağrı yığınlarını, kullanıcı etkileşimlerini ve ortam bilgilerini merkezi bir yerde toplayarak bu süreci hızlandırır. Bu alandaki popüler seçeneklerden Sentry, GlitchTip ve Bugsink aynı probleme farklı ölçek ve sadelik seviyeleriyle yaklaşır.


![hatalar-kacmadan-yakalayin-56](/img/hatalar-kacmadan-yakalayin-56.svg)

``

## Hata takip sistemi nasıl çalışır?

Uygulamaya eklenen SDK, yakalanmamış bir istisna oluştuğunda bir **hata olayı** üretir. Bu olay genellikle hata mesajını, stack trace bilgisini, sürümü, çalışma ortamını ve isteğe bağlı kullanıcı bağlamını içerir. Veriler bir DSN adresi üzerinden sunucuya gönderilir.

Sistem, benzer olayları tek bir sorun altında gruplandırmaya çalışır. Böylece aynı `NullReferenceException` hatası bin kez oluştuğunda panelde bin bağımsız kayıt yerine, gerçekleşme sayacı yükselen tek bir sorun görürüz.

Belirli sürede oluşan olay sayısını $E$, süreyi dakika cinsinden $t$ kabul edersek hata yoğunluğu şöyle ifade edilebilir:

$$R = \frac{E}{t}$$

Örneğin 10 dakikada 500 olay alınması, $R = 50$ olay/dakika anlamına gelir. Ancak yüksek sayı her zaman daha kritik hata demek değildir. Etkilenen kullanıcı sayısı, hata oranı ve işlemin önemi birlikte değerlendirilmelidir.

## Üç aracın kısa karşılaştırması

| Özellik | Sentry | GlitchTip | Bugsink |
|---|---|---|---|
| Temel yaklaşım | Kapsamlı gözlemlenebilirlik platformu | Açık kaynaklı, Sentry uyumlu alternatif | Hafif ve sade hata takibi |
| Barındırma | Bulut veya self-hosted | Bulut veya self-hosted | Özellikle self-hosted kullanım |
| Kurulum yükü | Self-hosted sürümde daha yüksek | Orta düzey | Görece düşük |
| Performans izleme | Gelişmiş | Temel ve orta seviye ihtiyaçlara uygun | Hata takibine odaklı |
| İdeal kullanım | Büyük ekipler ve ayrıntılı analiz | Açık kaynak ve maliyet dengesi | Küçük ekipler, kişisel sunucular |

**Sentry**, hata takibinin yanında performans izleme, dağıtık tracing, sürüm takibi ve oturum tekrarı gibi geniş özellikler sunar. Yönetilen bulut hizmeti operasyon yükünü azaltır; fakat yoğun trafik, veri kotası ve gizlilik gereksinimleri dikkatle değerlendirilmelidir.

**GlitchTip**, Sentry SDK’larıyla uyumlu açık kaynaklı bir deneyim sağlamayı amaçlar. Arayüzü daha sade, self-hosted kurulumu ise genellikle daha ulaşılabilirdir. Sentry’nin bütün ileri analiz özelliklerini beklemeyen ekipler için güçlü bir dengedir.

**Bugsink**, “önce hatayı yakalayalım” yaklaşımına yakındır. Daha az bileşenle çalışması, küçük sunucularda yönetimi kolaylaştırabilir. Kapsamlı observability platformu yerine anlaşılır bir hata kutusu isteyen projelere uygundur.

## Python uygulamasına SDK eklemek

Üç ürün de Sentry protokolüyle uyumlu kurulum senaryoları sunabildiğinden Python tarafında çoğunlukla resmi SDK kullanılabilir:

```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://anahtar@hata-sunucusu.example/1",
    environment="production",
    release="magaza-api@2.4.0",
    traces_sample_rate=0.1,
)

def fiyat_hesapla(toplam, adet):
    return toplam / adet

fiyat_hesapla(250, 0)
```

Bu kodda DSN, olayların gideceği projeyi belirtir. `environment` üretim ve test kayıtlarını ayırır; `release` ise hatanın hangi sürümde başladığını bulmayı kolaylaştırır. `traces_sample_rate=0.1`, performans işlemlerinin yaklaşık yüzde 10’unu örnekler. Ürün ve sürüme göre desteklenen SDK özellikleri değişebileceğinden uyumluluk belgeleri kontrol edilmelidir.

## Hangisini seçmeli?

Hazır servis, gelişmiş analiz ve minimum bakım istiyorsanız Sentry mantıklı başlangıçtır. Veriyi kendi altyapınızda tutmak, açık kaynak kullanmak ve daha ölçülü kaynak tüketmek istiyorsanız GlitchTip değerlendirilebilir. Yalnızca temel hata toplama, gruplama ve bildirim özelliklerine ihtiyacınız varsa Bugsink sadeliğiyle öne çıkar.

Seçimden önce günlük olay hacmini, saklama süresini ve örnekleme oranını hesaplayın. Ayrıca parola, erişim belirteci ve kişisel veri gibi hassas bilgileri SDK filtreleriyle temizleyin. Çünkü iyi bir hata takip sistemi yalnızca çok veri toplayan değil, doğru veriyi güvenli biçimde anlamlı hale getiren sistemdir.

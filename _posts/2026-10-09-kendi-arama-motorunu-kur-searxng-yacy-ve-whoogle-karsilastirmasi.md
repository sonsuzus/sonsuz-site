---
layout: post
title: "Kendi Arama Motorunu Kur: SearXNG, YaCy ve Whoogle Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - arama motoru
  - searxng
  - yacy
  - whoogle
  - gizlilik
  - açık kaynak
toc: true
image: /img/kendi-arama-motorunu-25.png
---

Arama kutusuna birkaç kelime yazıp Enter tuşuna bastığımızda perde arkasında oldukça büyük bir sistem çalışır. SearXNG, YaCy ve Whoogle ise bu sistemi farklı yöntemlerle kontrolümüze almamızı sağlayan açık kaynaklı araçlardır. Biri birçok kaynaktan sonuç toplar, biri dağıtık bir indeks oluşturur, diğeri Google sonuçlarını daha sade ve mahremiyet odaklı biçimde sunar. Kısacası üçü de arama yapar; fakat aynı yoldan gitmez.
``

## Önce temel teori: Arama motoru ne yapar?

Klasik bir arama motoru üç ana aşamadan oluşur:

1. **Tarama:** Botlar web sayfalarını ziyaret eder.
2. **İndeksleme:** Sayfalardaki kelimeler, bağlantılar ve meta veriler kaydedilir.
3. **Sıralama:** Kullanıcının sorgusuyla en alakalı belgeler seçilir.

Basitleştirilmiş bir alaka puanı şöyle düşünülebilir:

$$S(d,q) = \alpha T(d,q) + \beta L(d) + \gamma F(d)$$

Burada $T(d,q)$ belgenin sorguyla metinsel uyumunu, $L(d)$ bağlantı otoritesini, $F(d)$ ise güncelliğini temsil eder. $\alpha$, $\beta$ ve $\gamma$ katsayıları sistemin nelere önem verdiğini belirler. Ancak incelediğimiz araçların hepsi bu zincirin tamamını kendisi gerçekleştirmez.

| Araç | Temel yaklaşım | Kendi indeksi | Sonuç kaynağı | Güçlü yanı |
|---|---|---:|---|---|
| SearXNG | Meta arama | Hayır | Birden çok motor | Kaynak çeşitliliği |
| YaCy | Dağıtık arama | Evet | Eşler ve yerel tarayıcı | Merkeziyetsizlik |
| Whoogle | Google vekili | Hayır | Google | Sadelik ve mahremiyet |

## SearXNG: Arama motorlarının orkestra şefi

SearXNG, sorguyu yapılandırılmış biçimde Google, Bing, Brave, Wikipedia ve başka servislere göndererek sonuçları tek ekranda birleştiren bir **meta arama motorudur**. Kendisi tüm web’i taramaz; farklı kaynaklardan gelen sonuçları normalize eder ve sıralar.

Bu yaklaşım tek bir sağlayıcının bakış açısına bağlı kalmayı azaltır. Ayrıca kendi sunucunuza kurduğunuzda sorgu kayıtları ve çerez politikası üzerinde daha fazla denetim elde edersiniz. Yine de isteklerin hedef arama servislerine ulaştığını unutmamak gerekir; SearXNG sihirli görünmezlik pelerini değildir.

Docker ile hızlı bir deneme yapılabilir:

```bash
docker run -d --name searxng \
  -p 8080:8080 \
  searxng/searxng
```

Bu komut, SearXNG konteynerini çalıştırır ve arayüzü `8080` portundan erişilebilir hâle getirir. Gerçek kullanımda gizli anahtar, ters proxy, HTTPS ve hız sınırlaması ayrıca yapılandırılmalıdır.

## YaCy: Her bilgisayar küçük bir kütüphaneci

YaCy, diğer ikisinden daha maceracıdır. Kendi web tarayıcısına ve indeksine sahiptir; ayrıca eşler arası ağ üzerinden başka YaCy düğümleriyle veri paylaşabilir. Böylece merkezî bir şirket yerine birçok katılımcının katkısıyla arama altyapısı oluşturulabilir.

| Özellik | Merkezî indeks | YaCy ağı |
|---|---|---|
| Yönetim | Tek kuruluş | Dağıtık düğümler |
| Kaynak ihtiyacı | Kullanıcı için düşük | Disk, RAM ve bant genişliği ister |
| Kapsam | Genellikle çok geniş | Ağa ve taramaya bağlı |
| Denetim | Sağlayıcıda | Düğüm sahibinde |

YaCy özellikle intranet, akademik arşiv veya belirli sitelerden oluşan özel koleksiyonlar için ilgi çekicidir. Buna karşılık tüm web’de büyük ticari motorlarla aynı hız ve kaliteyi beklemek gerçekçi değildir. Özgürlük menüdeyse, yanında kaynak tüketimi de ikram edilir.

## Whoogle: Google, fakat daha az süslemeli

Whoogle, Google sonuçları için çalışan bir vekil arayüzdür. JavaScript ağırlığını, reklamları ve bazı takip mekanizmalarını azaltmayı hedefler. Kullanımı kolaydır; fakat doğrudan Google’a bağımlı olduğu için istek engelleme, CAPTCHA veya HTML değişikliklerinden etkilenebilir.

```bash
docker run -d --name whoogle \
  -p 5000:5000 \
  benbusby/whoogle-search
```

Bu örnek servisi yerel `5000` portunda başlatır. Herkese açık örnek çalıştırmak yerine erişimi sınırlandırmak daha güvenlidir; aksi hâlde sunucunuz kısa sürede robotların ücretsiz taksisine dönüşebilir.

## Hangisini seçmeli?

Çok kaynaklı ve özelleştirilebilir günlük arama için **SearXNG**, bağımsız indeksleme ve dağıtık deneyler için **YaCy**, sade Google sonuçları için **Whoogle** uygundur. En dengeli genel tercih çoğu kullanıcı açısından SearXNG’dir. Hangi aracı seçerseniz seçin HTTPS, güncel konteyner imajları, erişim kontrolü ve günlük politikası gibi güvenlik ayrıntılarını ihmal etmeyin. Mahremiyet yalnızca yazılım kurmakla değil, doğru yapılandırmakla kazanılır.

![kendi-arama-motorunu-25](/img/kendi-arama-motorunu-25.svg)


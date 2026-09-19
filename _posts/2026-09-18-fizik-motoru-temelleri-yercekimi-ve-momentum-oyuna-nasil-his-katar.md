---
layout: post
title: "Fizik Motoru Temelleri: Yerçekimi ve Momentum Oyuna Nasıl His Katar?"
math: true
categories: 
  - Bilgi
tags: 
  - fizik motoru
  - oyun geliştirme
  - yerçekimi
  - momentum
  - unity
  - vektörler
toc: true
image: /img/fizik-motoru-temelleri-65.png
---

Bir karakterin zıpladığında süzülmesi, bir sandığın darbeyle kayması veya yarış arabasının virajda ağırlığını hissettirmesi yalnızca güzel animasyonlarla açıklanamaz. Oyuncunun “Bu nesne gerçekten ağır!” demesini sağlayan görünmez kahraman, fizik motorudur. Ancak iyi oyun fiziği her zaman gerçek dünyanın birebir kopyası değildir; çoğu zaman gerçekliğin kontrollü biçimde abartılmış, hızlandırılmış ve eğlenceli hâlidir.

``

## Hareketin temel tarifi

Bir fizik motoru, nesnelerin konumunu her karede doğrudan değiştirmek yerine hız ve ivme üzerinden hesaplar. Temel ilişkiler şöyledir:

$$\vec{a} = \frac{\vec{F}}{m}$$

$$\vec{v}_{yeni} = \vec{v}_{eski} + \vec{a}\Delta t$$

$$\vec{x}_{yeni} = \vec{x}_{eski} + \vec{v}\Delta t$$

Burada $\vec{F}$ kuvveti, $m$ kütleyi, $\vec{a}$ ivmeyi ve $\Delta t$ geçen süreyi temsil eder. Ok işaretleri bu değerlerin birer **vektör** olduğunu, yani hem büyüklük hem yön taşıdığını belirtir.

Bu yaklaşım sayısal integrasyon olarak bilinir. Basit oyunlarda Euler integrasyonu yeterlidir. Çok hızlı nesneler veya hassas simülasyonlar söz konusu olduğunda daha kararlı yöntemlere ihtiyaç duyulabilir.

| Kavram | Ne anlatır? | Oyundaki hissi |
|---|---|---|
| Konum | Nesnenin bulunduğu yer | Görsel sonuç |
| Hız | Konumun değişim oranı | Akıcılık ve yön |
| İvme | Hızın değişim oranı | Ağırlık ve tepki |
| Kütle | Kuvvete karşı direnç | Hafiflik veya hantallık |

## Yerçekimi neden sadece aşağı çekmek değildir?

Dünya yüzeyinde yerçekimi ivmesi yaklaşık $9.81\,m/s^2$ değerindedir. Bir oyunda bunu basitçe aşağı yönlü sabit bir vektör olarak uygulayabiliriz:

$$\vec{F}_g = m\vec{g}$$

Kütle sadeleştiği için hava direnci yoksa bütün nesneler aynı ivmeyle düşer. Fakat oyun tasarımında “doğru” değer yerine “doğru his” önemlidir. Platform oyunlarında karakterin zıplarken biraz yavaş yükselmesi, tepe noktasında kısa süre asılı kalması ve ardından hızlı düşmesi daha kontrollü bir deneyim sağlar.

| Ayar | Gerçekçi sonuç | Oyun odaklı sonuç |
|---|---|---|
| Sabit yerçekimi | Doğal parabol | Tutarlı fakat bazen ağır |
| Düşerken güçlü yerçekimi | Gerçek dışı | Daha keskin iniş |
| Tepe noktasında düşük çekim | Fazla süzülme | Zıplamayı yönlendirme fırsatı |
| Maksimum düşüş hızı | Hava direncini taklit eder | Kontrolsüz hızlanmayı önler |

Unity benzeri bir yapıda özel düşüş hissi şöyle kurulabilir:

```csharp
void FixedUpdate()
{
    float gravityScale = velocity.y < 0 ? 2.5f : 1.0f;
    velocity += Physics.gravity * gravityScale * Time.fixedDeltaTime;
    velocity.y = Mathf.Max(velocity.y, -20f);
    transform.position += velocity * Time.fixedDeltaTime;
}
```

Bu kod, nesne düşerken yerçekimini güçlendirir ve düşüş hızını sınırlar. Hesaplamanın `FixedUpdate` içinde yapılması, fiziğin ekran yenileme hızından daha az etkilenmesini sağlar.

## Momentum: hareketin inadı

Momentum, bir nesnenin hareketini sürdürme eğilimini ifade eder:

$$\vec{p} = m\vec{v}$$

Aynı hızla giden bir bowling topu ile tenis topunun çarpışma etkisi aynı değildir; çünkü kütleleri farklıdır. Momentum ani bir kuvvetle değiştiğinde **itme** kavramı ortaya çıkar:

$$\vec{J} = \Delta\vec{p} = \vec{F}\Delta t$$

Silah geri tepmesi, patlama dalgası ve karakterin hasar alınca savrulması bu mantıkla üretilebilir. Kısa sürede büyük kuvvet uygulamak sert bir darbe, uzun sürede küçük kuvvet uygulamak ise yumuşak bir itiş hissettirir.

## İyi fizik için küçük hileler

Çarpışmalarda sekme katsayısı, sürtünme ve kütle oranları dikkatle ayarlanmalıdır. Çok yüksek sekme değeri dünyayı langırt masasına, aşırı sürtünme ise buz üstündeki kutuları halıya saplanmış mobilyalara dönüştürür. Ayrıca ekran sarsıntısı, ses perdesi, parçacıklar ve kısa animasyon duraklamaları fiziksel etkinin algısını güçlendirir.

Sonuç olarak yerçekimi hareketin ritmini, momentum ise darbelerin ağırlığını belirler. Formüller temel iskeleti kurar; eğlenceli “his” ise bu değerleri bilinçli biçimde bükmekten doğar. Fizik motorunun görevi gerçeği kusursuzca kopyalamak değil, oyuncuyu ikna etmektir.

![fizik-motoru-temelleri-65](/img/fizik-motoru-temelleri-65.svg)


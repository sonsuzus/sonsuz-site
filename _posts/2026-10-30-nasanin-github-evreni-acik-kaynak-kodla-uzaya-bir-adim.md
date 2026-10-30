---
layout: post
title: "NASA’nın GitHub Evreni: Açık Kaynak Kodla Uzaya Bir Adım"
math: true
categories: 
  - Bilgi
tags: 
  - nasa
  - açık kaynak
  - github
  - uzay yazılımları
  - bilimsel hesaplama
toc: true
image: /img/nasanin-github-evreni-19.png
---

Uzay yazılımı deyince gözünüzde yalnızca gizli laboratuvarlar ve dev ekranlar canlanıyorsa, tarayıcınızda yeni bir sekme açın: GitHub! NASA’nın paylaştığı projeler, uçuş yazılımı mimarisinden telemetri görselleştirmeye kadar uzanıyor. Üstelik bu depolar, yalnızca kod indirmek için değil, bilimsel düşünme ve güvenilir sistem geliştirme yöntemlerini öğrenmek için de değerli.


![nasanin-github-evreni-19](/img/nasanin-github-evreni-19.svg)

``

## Kodun paylaşılması neden bilimsel bir mesele?

Bilimde bir sonucun güçlü olması, başkalarının onu inceleyebilmesine ve uygun koşullarda yeniden üretebilmesine bağlıdır. Yazılım araştırmanın parçası olduğunda, yalnızca makaleyi paylaşmak yeterli olmayabilir: Kullanılan algoritmalar, bağımlılıklar ve hesaplama varsayımları da sonucu etkiler.

Açık kaynak depolar bu görünürlüğü artırır. Araştırmacılar uygulamayı denetleyebilir, geliştiriciler hataları bildirebilir, öğrenciler gerçek mimarilerden öğrenebilir. Ancak önemli bir ayrıntı var: Açık kod, tek başına yeniden üretilebilirlik garantisi değildir. Veri, sürüm bilgisi, yapılandırma ve çalışma ortamı da gerekir.

## NASA’nın GitHub raflarında neler var?

NASA ve JPL ekosistemindeki şu projeler, farklı mühendislik ihtiyaçlarını temsil ediyor:

| Proje | Temel amaç | Öğrenilecek yaklaşım |
|---|---|---|
| [cFS](https://github.com/nasa/cFS) | Yeniden kullanılabilir uçuş yazılımı altyapısı | Modüler uygulamalar ve mesajlaşma |
| [F´](https://github.com/nasa/fprime) | Bileşen tabanlı gömülü sistem geliştirme | Arayüzler, komutlar ve telemetri |
| [Open MCT](https://github.com/nasa/openmct) | Web tabanlı görev verisi görselleştirme | Zaman serileri ve operatör arayüzleri |
| [Trick](https://github.com/nasa/trick) | Simülasyon geliştirme ortamı | Modelleri çalıştırma ve deney tasarımı |

Bu araçlar birbirinin alternatifi değildir. Uçuş yazılımı cihaz üzerinde çalışırken, görselleştirme aracı operatörün veriyi anlamasını sağlar; simülasyon ortamı ise tasarım kararlarını sınamak için kullanılır. Aynı uzay macerasının farklı ekip arkadaşları gibi düşünebilirsiniz.

Özellikle uçuş sistemlerinde işlemci süresi ve bellek sınırlıdır. Bu yüzden modülerlik sadece temiz kod tercihi değildir; davranışın izlenmesini ve bileşenlerin ayrı ayrı test edilmesini kolaylaştırır. Buna karşılık bir telemetri arayüzünde zaman damgalarının tutarlılığı ve verinin anlaşılır sunulması öne çıkar.

## Teori molası: Bir uydu ne kadar sürede döner?

Kodun arkasındaki fiziği anlamadan simülasyon çıktısına güvenmek, pusulayı okumadan yürümeye benzer. İki cisim yaklaşımında yörünge periyodu şöyle hesaplanır:

$$
T = 2\pi\sqrt{\frac{a^3}{\mu}}
$$

Burada $T$ saniye cinsinden periyot, $a$ metre cinsinden yörüngenin büyük yarı ekseni, $\mu$ ise merkezî cismin kütleçekim parametresidir. Dairesel yörüngede $a = R + h$ olur: Gezegen yarıçapına irtifayı ekleriz.

Denklemin sezgisel mesajı güzel: Daha yüksek yörünge, daha uzun tur demektir. Ayrıca $T \propto a^{3/2}$ ilişkisi, artışın doğrusal olmadığını gösterir.

## Küçük bir Python deneyi

Aşağıdaki örnek herhangi bir NASA API’sini kullanmaz; depolardaki modelleme yaklaşımına hazırlanmak için bağımsız bir alıştırmadır:

```python
from dataclasses import dataclass
from math import isfinite, pi, sqrt

EARTH_RADIUS_M = 6_371_000
EARTH_MU = 3.986004418e14  # m^3 / s^2

@dataclass(frozen=True)
class CircularOrbit:
    altitude_km: float

    def period_minutes(self) -> float:
        if not isfinite(self.altitude_km) or self.altitude_km <= 0:
            raise ValueError("İrtifa pozitif ve sonlu olmalı.")

        radius_m = EARTH_RADIUS_M + self.altitude_km * 1000
        period_s = 2 * pi * sqrt(radius_m**3 / EARTH_MU)
        return period_s / 60

for altitude in (400, 800):
    orbit = CircularOrbit(altitude)
    print(f"{altitude} km: {orbit.period_minutes():.1f} dakika")
```

`dataclass`, yörünge girdisini düzenli bir nesnede tutar; `frozen=True` yanlışlıkla değiştirilmesini engeller. Girdi kontrolü geçersiz irtifaları reddeder. Birim dönüşümleri açıkça yapılır: Kilometreyi metreye çevirmeyi unutmak, sonucu ciddi biçimde bozar. Yaklaşık çıktılar sırasıyla **92,4** ve **100,7 dakika** olur.

## Katkı vermenin gerçekçi rotası

İlk katkınızın roket yönlendirme algoritması olması gerekmiyor. Önce deponun README, lisans ve katkı rehberini okuyun. Örnek uygulamayı çalıştırın; ardından küçük ve doğrulanabilir bir iyileştirme seçin: Bozuk belge bağlantısı, eksik test veya anlaşılmayan hata mesajı gibi.

Bir hata bildirirken kullanılan sürümü, işletim sistemini, yeniden üretme adımlarını ve beklenen davranışı yazın. Böylece bakımcılar tahmin yürütmek yerine sorunu inceleyebilir. Çekme isteğinize ilgili testleri eklemek de katkının güvenle değerlendirilmesini kolaylaştırır.

| Test yaklaşımı | Neyi yakalayabilir? | Tek başına neyi kanıtlamaz? |
|---|---|---|
| Birim testi | Yerel hesaplama hatalarını | Sistemin bütün davranışını |
| Simülasyon | Model kapsamındaki etkileşimleri | Gerçek donanım koşullarını |
| Donanımlı test | Fiziksel arayüz sorunlarını | Bütün görev senaryolarını |

## Açık kaynak, uçuş onayı değildir

Örneğimiz atmosferik sürüklenmeyi, Dünya’nın basıklığını ve diğer bozucu etkileri ihmal eder. Benzer şekilde, GitHub’da yayımlanmış bir proje de kendiliğinden uçuşa hazır veya güvenlik açısından sertifikalı sayılmaz. Lisansı ve kullanım koşullarını depo bazında inceleyin.

Asıl kazanım, uzayı birkaç satırla fethetmek değil; varsayımları görünür kılmak, sonuçları sınamak ve ortak bilgiye katkıda bulunmaktır. Bazen bilime açılan kapı, küçük ama iyi belgelenmiş bir düzeltmedir.

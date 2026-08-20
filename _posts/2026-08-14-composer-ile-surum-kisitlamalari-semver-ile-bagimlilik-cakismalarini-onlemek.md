---
layout: post
title: "Composer ile Sürüm Kısıtlamaları: SemVer ile Bağımlılık Çakışmalarını Önlemek"
math: true
categories: 
  - Bilgi
tags: 
  - php
  - composer
  - semver
---

PHP projesinde `composer update` komutunun bir paketi güncellerken başka bir kütüphaneyi bozması, çoğu geliştiricinin en az bir kez yaşadığı küçük bir bağımlılık dramıdır. Composer bu dramı sihirle değil; sürüm kısıtlamaları, paket metadatası ve Semantik Versiyonlama (SemVer) kurallarıyla yönetir. Doğru yazılmış bir `composer.json`, hem güvenli güncellemeye alan açar hem de ekipteki herkesin aynı bağımlılık ağını kurmasına yardımcı olur.
``

## SemVer: Üç sayının anlattığı sözleşme

SemVer biçimi `MAJOR.MINOR.PATCH` şeklindedir. Örneğin `2.4.7` sürümünde sayıların anlamı yalnızca kronolojik değildir; paketin dışarıya sunduğu API için bir sözleşmedir.

$$\text{Sürüm} = M.m.p$$

- **MAJOR (`M`)**: Geriye dönük uyumsuz değişiklik vardır. Bir metodun kaldırılması veya imzasının değişmesi buna örnektir.
- **MINOR (`m`)**: Yeni özellik eklenmiştir, ancak mevcut çalışan kod kırılmamalıdır.
- **PATCH (`p`)**: Hata düzeltmesi ya da güvenli, küçük iyileştirme yapılmıştır.

Bu yaklaşım, Composer'ın “hangi sürümler aynı projede güvenle yaşayabilir?” sorusunu çözmesini sağlar. Elbette paket yazarı SemVer kurallarına uymazsa en iyi kısıtlama bile kusursuz koruma sağlayamaz; sürüm numarası bir teknik işaret kadar bir güven taahhüdüdür.

| Kısıtlama | Kabul edilen örnekler | Tipik kullanım | Risk düzeyi |
|---|---|---|---|
| `1.2.3` | Yalnızca `1.2.3` | Tam tekrar üretilebilir sürüm | Güncelleme yok |
| `^1.2.3` | `>=1.2.3 <2.0.0` | Kararlı kütüphaneler | Düşük-orta |
| `~1.2.3` | `>=1.2.3 <1.3.0` | Daha dar güncelleme aralığı | Düşük |
| `>=1.2 <2.0` | `1.x` ailesi | Açık aralık gerektiğinde | Orta |
| `*` | Her sürüm | Deneysel çalışmalar | Çok yüksek |

## Şapka ve tilde neden farklı davranır?

Composer'da en sık kullanılan operatör `^` işaretidir. `^2.3` ifadesi, `2.3.0` ile başlayıp `3.0.0` öncesine kadar olan sürümleri kabul eder. Çünkü SemVer'e göre API'yi kırabilecek değişim, normalde bir sonraki major sürümdedir. Buna karşılık `~2.3.4`, yalnızca `2.3.x` düzeltme sürümlerini kapsar; `2.4.0` gelince durur.

Önemli bir istisna vardır: `0.x` sürümlerinde paket henüz tam kararlı kabul edilmez. Bu nedenle `^0.3.2`, sanılanın aksine `1.0.0` öncesinin tamamını değil, `>=0.3.2 <0.4.0` aralığını kabul eder. Sıfırın solundaki major değer, uyumluluk garantisi için yeterli değildir.

```json
{
  "require": {
    "guzzlehttp/guzzle": "^7.8",
    "monolog/monolog": "~3.5.0",
    "vendor/eski-paket": ">=2.1 <3.0"
  }
}
```

Bu örnekte Guzzle, 8.0.0 çıkana dek uyumlu minor ve patch güncellemelerini alabilir. Monolog ise yalnızca `3.5.x` hata düzeltmelerinde kalır. Son satırdaki aralık, özellikle paketin belgelerinde desteklenen major ailesi açıkça belirtilmişse yararlıdır.

## Çakışma nasıl ortaya çıkar ve Composer ne yapar?

Diyelim ki uygulamanız `paket-a` için `^2.0`, `paket-b` ise aynı ortak bağımlılık için `<2.5` istiyor. Ortak paketin `2.3.0` sürümü varsa çözüm bulunur. Fakat A `>=2.6` isterken B `<2.5` istiyorsa kesişim kümesi boştur:

$$[2.6, \infty) \cap (-\infty, 2.5) = \varnothing$$

Composer böyle bir durumda rastgele seçim yapmak yerine ayrıntılı bir çözümleme hatası verir. Bu davranış can sıkıcı görünse de çalışma anındaki gizemli hatalardan çok daha değerlidir. Çözüm; paketi güncellemek, uyumlu bir sürümünü seçmek veya gerçekten gerekliyse bağımlılık ağını yeniden tasarlamaktır.

`composer.lock` dosyası da bu denklemin pratik tamamlayıcısıdır. `composer.json` izin verilen aralığı tanımlar; lock dosyası ise seçilmiş kesin sürümleri kaydeder. Uygulamalarda lock dosyasını Git'e ekleyin, yeni sürümleri kontrollü almak için `composer update`, kayıtlı sürümleri kurmak için `composer install` kullanın. Böylece “benim makinemde çalışıyordu” cümlesi, bağımlılık listenizden hızla silinir.

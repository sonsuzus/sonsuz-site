---
layout: post
title: "ConvertAll ve MathJS ile Akıllı Birim Dönüştürme Sitesi Geliştirmek"
math: true
categories: 
  - Proje
tags: 
  - javascript
  - mathjs
  - birim-dönüştürme
  - web-geliştirme
  - convertall
toc: true
image: /img/convertall-ve-mathjs-59.png
---

![convertall-ve-mathjs-59](/img/convertall-ve-mathjs-59.svg)


Birim dönüştürme uygulamaları ilk bakışta yalnızca “metreyi kilometreye böl” seviyesinde görünür. Ancak sıcaklık, alan, hacim, hız ve türetilmiş bilimsel birimler işin içine girince küçük hesap makinemiz adeta laboratuvar önlüğü giymeye başlar. ConvertAll yaklaşımını örnek alan ve MathJS kullanan bir web sitesi; kullanıcıya esnek, güvenilir ve genişletilebilir bir dönüştürme deneyimi sunabilir.
``
## Birim dönüşümünün temel mantığı

Aynı fiziksel büyüklüğü temsil eden birimler arasında genellikle bir ölçek katsayısı bulunur. Örneğin metre ile santimetre arasındaki ilişki şöyledir:

$$1\,m = 100\,cm$$

Dolayısıyla $x$ metreyi santimetreye dönüştürmek için $x \times 100$ hesaplanır. Genel doğrusal dönüşüm modeli şu şekilde ifade edilebilir:

$$y = ax + b$$

Burada $a$ ölçek katsayısı, $b$ ise başlangıç noktası farkıdır. Uzunluk dönüşümlerinde çoğunlukla $b=0$ olur. Sıcaklıkta ise durum farklıdır. Celsius’tan Fahrenheit’a dönüşüm:

$$F = C \times 1.8 + 32$$

Bu ayrım önemlidir; her birimi yalnızca bir sayıyla çarpmak doğru sonuç üretmez.

| Dönüşüm türü | Örnek | Matematiksel yapı |
|---|---|---|
| Ölçek tabanlı | metre → santimetre | $y=ax$ |
| Ofsetli | Celsius → Fahrenheit | $y=ax+b$ |
| Ters orantılı | yakıt ekonomisi gösterimleri | $y=a/x$ |
| Bileşik | km/saat → m/saniye | birden fazla katsayı |

## ConvertAll yaklaşımı nedir?

ConvertAll, kullanıcının kaynak ve hedef birimleri özgürce seçebilmesini sağlayan masaüstü odaklı bir dönüştürme aracıdır. En güçlü fikri, yalnızca hazır dönüşüm düğmeleri sunmak yerine birim ifadelerini ayrıştırmasıdır. Böylece `km/hour`, `meter/second` veya `kg*m/s^2` gibi bileşik ifadeler anlamlandırılabilir.

Bir web projesinde aynı yaklaşımı uygulamak için üç temel katman gerekir:

1. Kullanıcı ifadesini ayrıştıran giriş katmanı,
2. Birimlerin uyumluluğunu denetleyen hesaplama motoru,
3. Sonucu anlaşılır biçimde gösteren arayüz.

Kütle ile uzunluğu dönüştürmeye çalışmak matematiksel olarak anlamsızdır. Sistem, `5 kg → metre` isteğine rastgele bir sayı vermek yerine boyut uyuşmazlığı hatası göstermelidir.

## MathJS ile dönüşüm motoru

MathJS; JavaScript için ifadeler, matrisler, büyük sayılar ve birimler konusunda kapsamlı özellikler sunar. Tarayıcıda veya Node.js ortamında kullanılabilir. Temel bir dönüşüm oldukça kısa yazılır:

```javascript
import { create, all } from "mathjs";

const math = create(all);

function donustur(deger, kaynak, hedef) {
  const miktar = math.unit(deger, kaynak);
  return miktar.toNumber(hedef);
}

console.log(donustur(10, "km", "m")); // 10000
console.log(donustur(25, "degC", "degF")); // 77
```

`math.unit()` sayıyı birimiyle birlikte temsil eder. `toNumber()` ise miktarı hedef birime çevirerek sayısal sonucu döndürür. Bu yöntem, dönüşüm katsayılarını elle yazmaktan daha güvenlidir.

Kullanıcı girişleri doğrudan işlenmemeli; hata yakalama mekanizması eklenmelidir:

```javascript
function guvenliDonustur(deger, kaynak, hedef) {
  try {
    if (!Number.isFinite(deger)) {
      throw new Error("Geçerli bir sayı girilmedi.");
    }

    const sonuc = math.unit(deger, kaynak).toNumber(hedef);
    return { basarili: true, sonuc };
  } catch (hata) {
    return { basarili: false, mesaj: hata.message };
  }
}
```

Bu fonksiyon arayüzün çökmesini önler ve kullanıcıya açıklayıcı geri bildirim sağlar.

## Arayüz ve geliştirme fikirleri

Başarılı bir dönüştürme sitesi; kategori seçimi, iki birim listesi, değer alanı ve birimleri ters çevirme düğmesi içermelidir. Son kullanılan dönüşümleri yerel depolamada saklamak da kullanıcı deneyimini iyileştirir.

| Özellik | Basit sistem | Gelişmiş sistem |
|---|---|---|
| Birim seçimi | sabit liste | arama ve filtreleme |
| Hesaplama | elle yazılmış katsayılar | MathJS motoru |
| Sonuç | tek sayı | hassasiyet ve bilimsel gösterim |
| Geçmiş | yok | favoriler ve son işlemler |

Özel birimler `math.createUnit()` ile tanımlanabilir. Böylece uygulamaya yerel ölçüler veya projeye özgü teknik birimler eklenebilir. Son aşamada otomatik testlerle bilinen eşitlikler doğrulanmalıdır: $1\,inch=2.54\,cm$ ve $0\,^{\circ}C=32\,^{\circ}F$ gibi. Böylece siteniz yalnızca şık görünmez; hesap yaparken de cetveli ters tutmaz.

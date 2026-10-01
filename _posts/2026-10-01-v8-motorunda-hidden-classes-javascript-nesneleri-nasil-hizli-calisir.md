---
layout: post
title: "V8 Motorunda Hidden Classes: JavaScript Nesneleri Nasıl Hızlı Çalışır?"
math: true
categories: 
  - Bilgi
tags: 
  - javascript
  - v8
  - hidden-classes
  - performans
  - optimizasyon
  - jit
toc: true
image: /img/v8-motorunda-hidden-57.png
---

JavaScript nesneleri çalışma sırasında özgürce değişebilir: Yeni özellikler eklenir, eskileri silinir ve türler aniden dönüşebilir. Bu esneklik kullanışlı olsa da işlemci açısından pek romantik değildir. V8 motoru, nesnelere **Hidden Class** adı verilen dahili şekil haritaları atayarak bu belirsizliği azaltır ve özellik erişimini statik dillere şaşırtıcı derecede yaklaştırır.


![v8-motorunda-hidden-57](/img/v8-motorunda-hidden-57.svg)

``

## Nesne erişimindeki temel problem

C++ gibi statik bir dilde derleyici, bir alanın bellekteki konumunu önceden bilir. Örneğin `x` alanı nesnenin başlangıcından 8 bayt ilerideyse erişim doğrudan bu adrese yapılabilir. JavaScript'te ise aşağıdaki nesnenin daha sonra nasıl değişeceği bilinmez:

```javascript
const nokta = {};
nokta.x = 10;
nokta.y = 20;
```

Naif bir motor, her `nokta.x` erişiminde özellik adını sözlükte aramak zorunda kalabilir. Yaklaşık maliyet modeli şöyle düşünülebilir:

$$
T_{erişim} = T_{arama} + T_{adresleme} + T_{okuma}
$$

V8'in hedefi, tekrarlanan erişimlerde $T_{arama}$ maliyetini mümkün olduğunca ortadan kaldırmaktır. Hidden Class mekanizması tam olarak burada sahneye çıkar.

## Hidden Class nasıl oluşur?

V8, her nesneye özellik adlarını ve bellek ofsetlerini tanımlayan gizli bir sınıf bağlar. Bu sınıf JavaScript içinden görülemez; `class` sözdizimiyle de aynı şey değildir.

```javascript
function Nokta(x, y) {
  this.x = x;
  this.y = y;
}

const a = new Nokta(3, 5);
const b = new Nokta(8, 13);
```

Her iki nesne de özellikleri aynı sırayla aldığı için aynı şekil geçişlerini izler:

```text
C0 -- x eklendi --> C1 -- y eklendi --> C2
```

`C2`, kabaca `x` özelliğinin birinci, `y` özelliğinin ikinci alanda bulunduğunu söyler. Böylece V8, `a.x` ve `b.x` işlemlerinde aynı optimize edilmiş yolu kullanabilir.

| Yaklaşım | Özellik bulma yöntemi | Muhtemel sonuç |
|---|---|---|
| Sözlük tabanlı erişim | İsme göre arama | Esnek fakat daha maliyetli |
| Hidden Class | Sınıf ve sabit ofset | Hızlı, öngörülebilir erişim |
| Statik dil yapısı | Derleme zamanında ofset | Çok düşük erişim maliyeti |

## Özellik sırası neden önemlidir?

Aynı alanlara sahip iki nesne, alanlar farklı sırayla eklenirse farklı Hidden Class zincirleri oluşturabilir:

```javascript
const a = {};
a.x = 1;
a.y = 2;

const b = {};
b.y = 2;
b.x = 1;
```

İnsan gözüyle `a` ve `b` aynı şekildedir. V8 açısından ise geçiş yolları farklıdır. Bir fonksiyon sürekli farklı şekiller görürse optimizasyon kalitesi düşebilir.

## Inline Cache ile ekip çalışması

Hidden Class tek başına çalışmaz. V8, özellik erişim noktalarında **Inline Cache** kullanarak daha önce karşılaştığı sınıfı ve ofseti hatırlar:

```javascript
function xDegeri(nokta) {
  return nokta.x;
}
```

Fonksiyon hep aynı şekle sahip nesneler alırsa erişim **monomorfik** olur. Birkaç şekil görülürse **polimorfik**, çok fazla şekil görülürse **megamorfik** hale gelebilir.

| Durum | Görülen şekil sayısı | Optimizasyon potansiyeli |
|---|---:|---|
| Monomorfik | 1 | Çok yüksek |
| Polimorfik | Birkaç | Orta veya yüksek |
| Megamorfik | Çok fazla | Düşük |

Basitleştirilmiş kazanç şu oranla ifade edilebilir:

$$
Hızlanma \approx \frac{T_{arama}+T_{okuma}}{T_{sınıf\ kontrolü}+T_{ofset\ okuma}}
$$

## Dictionary Mode ve deoptimizasyon

Nesneye sürekli alan eklemek, alan silmek veya yapıyı aşırı değiştirmek V8'in nesneyi **dictionary mode** biçimine geçirmesine yol açabilir. Özellikle `delete`, düzenli şekil varsayımlarını bozabilir:

```javascript
const kullanici = {
  id: 42,
  aktif: true
};

delete kullanici.aktif;
```

Performansın kritik olduğu sıcak kodlarda alanı silmek yerine değeri `null` yapmak şeklin korunmasına yardımcı olabilir. Ancak bunu her yerde uygulamak gerekmez; önce profil çıkarmak daha doğrudur.

## Pratik öneriler

- Benzer nesnelerin özelliklerini aynı sırayla oluşturun.
- Constructor içinde temel alanları baştan tanımlayın.
- Sıcak döngülerde nesne şekillerini sık sık değiştirmeyin.
- Aynı fonksiyona tamamen alakasız şekiller göndermekten kaçının.
- Mikro optimizasyondan önce Chrome DevTools veya Node.js profilleyicisini kullanın.

Hidden Classes, JavaScript'i statik bir dile dönüştürmez. Bunun yerine V8'e, dinamik nesneler hakkında tekrar kullanılabilir varsayımlar kurma fırsatı verir. Kodunuz tutarlı nesne şekilleri ürettiğinde motor da daha az dedektiflik yapar ve daha çok hızlanır.

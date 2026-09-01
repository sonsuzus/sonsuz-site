---
layout: post
title: "Burnside Lemması ile Boyama Problemleri: Simetrileri Saymanın Akıllı Yolu"
math: true
categories: 
  - Bilgi
tags: 
  - burnside lemması
  - kombinatorik
  - simetri
toc: true
---

Bir kolyenin boncuklarını boyadığınızı düşünün. Kırmızı-mavi-yeşil dizilimi ilk bakışta yüzlerce farklı sonuç üretebilir; ancak kolyeyi döndürdüğünüzde veya ters çevirdiğinizde bazı boyamalar aslında aynıdır. İşte Burnside Lemması, bu simetri karmaşasını düzenleyerek gerçekten farklı olan boyamaların sayısını bulmamızı sağlar.

``

## Neden normal sayma yeterli değil?

$n$ konumun her biri $q$ renkten biriyle boyanabiliyorsa, konumları sabit kabul ettiğimizde toplam boyama sayısı

$$q^n$$

olur. Fakat nesne döndürülebiliyor veya yansıtılabiliyorsa farklı görünen bazı dizilimler aynı fiziksel boyamayı temsil eder. Bu nedenle sonucu doğrudan simetri sayısına bölmek de genellikle yanlıştır. Çünkü her boyama, bütün simetrilerden aynı biçimde etkilenmez.

| Yaklaşım | Neyi farklı kabul eder? | Kullanım durumu |
|---|---|---|
| Doğrudan sayma | Her konumu etiketli kabul eder | Sabit sıra veya tablo |
| Yalnız dönmeler | Döndürmeyle oluşanları aynı sayar | Yönü çevrilemeyen kolye |
| Dönme ve yansıma | Dönen ve ters çevrilenleri aynı sayar | Bileklik, çokgen süsleme |

## Burnside Lemması

Bir $G$ simetri grubu, boyamalar kümesi üzerinde işlem yapsın. Her $g \in G$ simetrisi için $\operatorname{Fix}(g)$, bu işlemden sonra değişmeden kalan boyamaların sayısı olsun. Burnside Lemması şöyle der:

$$
N=\frac{1}{\vert G\vert }\sum_{g\in G}\vert \operatorname{Fix}(g)\vert 
$$

Başka bir deyişle, her simetrinin sabit bıraktığı boyamaları sayar ve bunların ortalamasını alırız. Buradaki “sabit kalmak”, boyamanın simetri uygulandıktan sonra birebir aynı görünmesi demektir.

## Altı konumlu bileklik örneği

Altı boncuklu bir bilekliği $q$ renkle boyayalım. Dönme ve yansımalar aynı kabul edildiğinde simetri grubumuz $D_6$ olur ve toplam $12$ eleman içerir: altı dönme, altı yansıma.

Bir döndürme, konumları döngülere ayırır. $k$ adımlık dönüşte döngü sayısı $\gcd(6,k)$ olduğundan sabit boyama sayısı

$$q^{\gcd(6,k)}$$

olur. Altı dönüşün katkısı şöyledir:

$$q^6+2q^2+q^3+2q$$

Yansımalarda ise iki farklı durum vardır:

| Yansıma ekseni | Adet | Döngü sayısı | Sabit boyama |
|---|---:|---:|---:|
| Karşılıklı boncuklardan geçer | 3 | 4 | $q^4$ |
| Karşılıklı kenarlardan geçer | 3 | 3 | $q^3$ |

Dolayısıyla sonuç

$$
N=\frac{q^6+2q^2+q^3+2q+3q^4+3q^3}{12}
$$

şeklindedir. Üç renk için hesap yaparsak:

$$
N=\frac{729+18+27+6+243+81}{12}=92
$$

Yani başlangıçtaki $3^6=729$ etiketli boyama, simetriler hesaba katıldığında yalnızca **92 farklı bilekliğe** dönüşür.

## Python ile genelleştirme

Aşağıdaki fonksiyon, yalnızca dönmelerin aynı kabul edildiği dairesel boyamaları hesaplar. Her dönüşte oluşan döngü sayısını `gcd` ile bulur:

```python
from math import gcd

def donel_boyama_sayisi(konum, renk):
    sabitlerin_toplami = 0

    for kaydirma in range(konum):
        dongu_sayisi = gcd(konum, kaydirma)
        sabitlerin_toplami += renk ** dongu_sayisi

    return sabitlerin_toplami // konum

print(donel_boyama_sayisi(6, 3))  # 130
```

Sonucun 130 olması şaşırtıcı değildir: Bu kod yansımaları aynı saymaz. Yansımaları da eklediğimiz bileklik probleminde sonuç 92’ye düşer.

Burnside Lemması’nın asıl gücü formülü ezberlemekten değil, her simetrinin oluşturduğu döngüleri doğru analiz etmekten gelir. Çokgen köşeleri, kolyeler, küp yüzleri veya periyodik desenler değişse bile tarif aynıdır: simetrileri listele, sabit kalan boyamaları bul, ortalamayı al. Simetri canavarını yenmenin yolu, onun kaç şeyi yerinden oynatamadığını saymaktır!

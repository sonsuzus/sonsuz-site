---
layout: post
title: "Fraktal Geometri: Koch Eğrisi ve Sierpinski Üçgeni"
math: true
categories: 
  - Bilgi
tags: 
  - fraktal
  - geometri
  - koch-eğrisi
  - sierpinski-üçgeni
  - python
  - özyineleme
toc: true
image: /img/fraktal-geometri-koch-45.png
---

Bir kar tanesinin kıyısında yürüdüğünüzü ve attığınız her adımda önünüzde yeni girintiler belirdiğini düşünün. Fraktallar tam olarak bu tuhaf dünyayı temsil eder: Basit bir kural tekrar tekrar uygulandığında, göz alıcı ve teorik olarak sonsuz ayrıntıya sahip şekiller ortaya çıkar. Koch eğrisi ile Sierpinski üçgeni bunun en ünlü örneklerindendir.
``
## Fraktal nedir?

Klasik Öklid geometrisinde doğru tek boyutlu, kare iki boyutlu ve küp üç boyutludur. Fraktal geometrideyse boyut her zaman tam sayı olmak zorunda değildir. Çünkü fraktallar, bir şeklin küçük parçalarının bütün şekle benzemesi anlamına gelen **öz-benzerlik** özelliğine sahiptir.

Bir fraktalın benzerlik boyutu genel olarak şu formülle hesaplanır:

$$D = \frac{\log N}{\log s}$$

Burada $N$, her adımda oluşan benzer parça sayısını; $s$ ise küçültme oranının tersini ifade eder. Örneğin bir şekil, yarı boyutta üç kopyadan oluşuyorsa boyutu $\log(3)/\log(2)$ olur. Yani fraktallar, doğru ile yüzey arasında yaşıyormuş gibi davranabilir.

| Özellik | Klasik geometrik şekil | Fraktal şekil |
|---|---|---|
| Boyut | Genellikle tam sayı | Kesirli olabilir |
| Ayrıntı | Yaklaştıkça sınırlanır | Her ölçekte devam eder |
| Üretim | Sabit tanım | Tekrarlanan kurallar |
| Öz-benzerlik | Genellikle yoktur | Temel özelliklerden biridir |

![fraktal-geometri-koch-45](/img/fraktal-geometri-koch-45.svg)


## Koch eğrisi: Uzayan kıyı şeridi

Koch eğrisi bir doğru parçasıyla başlar. Her yinelemede doğru üç eşit parçaya ayrılır, ortadaki parça kaldırılır ve yerine eşkenar üçgenin iki kenarı eklenir. Böylece bir parça yerine dört küçük parça oluşur.

$n$ yineleme sonrasında parça sayısı ve her parçanın uzunluğu şöyledir:

$$N_n = 4^n, \qquad L_n = \frac{L_0}{3^n}$$

Toplam uzunluk ise:

$$P_n = L_0\left(\frac{4}{3}\right)^n$$

olur. $n$ sonsuza giderken uzunluk da sonsuza gider! Buna rağmen eğri sonlu bir alan içinde kalır. Koch eğrisinin fraktal boyutu yaklaşık $1{,}262$ değerindedir:

$$D_K = \frac{\log 4}{\log 3}$$

Aşağıdaki Python kodu, `turtle` modülüyle bu kuralı özyinelemeli olarak çizer:

```python
import turtle

def koch(uzunluk, seviye):
    if seviye == 0:
        turtle.forward(uzunluk)
        return

    for aci in (0, 60, -120, 60):
        koch(uzunluk / 3, seviye - 1)
        turtle.left(aci)

turtle.speed(0)
koch(500, 4)
turtle.done()
```

Fonksiyon temel seviyede düz çizgi çizer. Daha yüksek seviyelerdeyse aynı görevi dört küçük Koch eğrisine devreder. Bu yaklaşım, matematikteki yinelemeyi programlamadaki **özyineleme** ile doğrudan eşleştirir.

## Sierpinski üçgeni: Boşluklardan doğan desen

Sierpinski üçgeni dolu bir eşkenar üçgenle başlar. Üçgen dört eş parçaya bölünür ve ortadaki parça çıkarılır. Kalan üç üçgene aynı işlem uygulanır. Her adımda üç kopya oluştuğu ve kenarlar yarıya indiği için boyutu şöyledir:

$$D_S = \frac{\log 3}{\log 2} \approx 1{,}585$$

$n$ adımından sonra kalan üçgen sayısı $3^n$, her küçük üçgenin alanı başlangıç alanının $1/4^n$ katıdır. Dolayısıyla toplam alan:

$$A_n = A_0\left(\frac{3}{4}\right)^n$$

olur ve limitte sıfıra yaklaşır.

| Fraktal | Her adımda parça | Ölçek | Boyut |
|---|---:|---:|---:|
| Koch eğrisi | 4 | $1/3$ | $\log 4/\log 3$ |
| Sierpinski üçgeni | 3 | $1/2$ | $\log 3/\log 2$ |

Bu iki şekil, karmaşıklığın mutlaka karmaşık kurallardan doğmadığını gösterir. Birkaç satırlık algoritma; doğadaki kıyıları, damar ağlarını, bitki dallarını ve anten tasarımlarını anlamaya açılan sonsuz ayrıntılı bir pencereye dönüşebilir.

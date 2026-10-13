---
layout: post
title: "L-Sistemleri ile Bitki Simülasyonu: Matematikten Dijital Bahçelere"
math: true
categories: 
  - Proje
tags: 
  - l-sistemleri
  - bitki-simülasyonu
  - python
  - fraktallar
  - üretken-tasarım
  - matematik
toc: true
image: /img/l-sistemleri-ile-52.png
---

Bir eğrelti otunun kıvrımlarını veya ağacın dallanma biçimini birkaç harf ve matematiksel kuralla oluşturabileceğinizi düşünün. L-Sistemleri, karmaşık doğal formları tek tek çizmek yerine onların büyüme mantığını tarif eder. Böylece küçük bir başlangıç ifadesi, birkaç yineleme sonunda dijital bir bahçeye dönüşebilir.

![l-sistemleri-ile-52](/img/l-sistemleri-ile-52.svg)

``
## L-Sistemi nedir?

L-Sistemi ya da Lindenmayer Sistemi, biyolog Aristid Lindenmayer tarafından hücrelerin ve bitkilerin gelişimini modellemek amacıyla geliştirilmiş biçimsel bir gramer türüdür. Bir sistem genel olarak şu üçlüyle gösterilir:

$$G=(V, \omega, P)$$

Burada $V$ kullanılabilecek sembollerin alfabesi, $\omega$ başlangıç dizisi veya aksiyom, $P$ ise üretim kurallarıdır. Klasik gramerlerden en önemli farkı, bir dizideki uygun sembollerin sırayla değil **eş zamanlı** değiştirilmesidir. Bu paralel davranış, bitkinin farklı bölgelerinin aynı büyüme döneminde gelişmesini taklit eder.

| Bileşen | Görevi | Örnek |
|---|---|---|
| Alfabe | Sistemin sembollerini belirler | `F`, `+`, `-`, `[`, `]` |
| Aksiyom | Büyümenin başladığı ilk durumdur | `F` |
| Kural | Sembollerin nasıl dönüşeceğini söyler | `F → F[+F]F[-F]F` |
| Yineleme | Kuralların kaç kez uygulanacağını belirler | 4 |

Örneğin aksiyomumuz $\omega=F$ ve kuralımız $F \rightarrow F[+F]F[-F]F$ olsun. İlk adımda tek `F`, kuralın sağ tarafına dönüşür. İkinci adımda ortaya çıkan bütün `F` sembolleri aynı kuralla yeniden yazılır. Eğer bir kural her adımda yaklaşık $k$ yeni dal parçası üretiyorsa, sembol sayısı kabaca

$$N_n \approx N_0 k^n$$

şeklinde büyür. Bu üstel büyüme etkileyici sonuçlar üretir; ancak yüksek yineleme değerlerinde bilgisayarınızı küçük bir ormana çevirmeden önce bellek tüketimini düşünmek gerekir.

## Harfler nasıl bitkiye dönüşüyor?

Üretilen metin tek başına görsel değildir. Çizim için genellikle kaplumbağa grafiği yorumlaması kullanılır. Hayali bir kalem, sembolleri soldan sağa okuyarak ilerler.

| Sembol | Çizim davranışı |
|---|---|
| `F` | İleri git ve çizgi çiz |
| `+` | Belirlenen açı kadar sağa dön |
| `-` | Belirlenen açı kadar sola dön |
| `[` | Konumu ve yönü yığına kaydet |
| `]` | Son kaydedilen duruma geri dön |

Köşeli parantezler dallanmanın sırrıdır. `[` görüldüğünde mevcut konum saklanır; `]` görüldüğünde bu konuma dönülür. Böylece ana gövde kaybolmadan yan dallar üretilebilir.

## Python ile üretim dizisini hazırlamak

Aşağıdaki fonksiyon, aksiyomu belirtilen sayıda paralel olarak dönüştürür. `dict.get` sayesinde kuralı bulunmayan `+` ve `[` gibi semboller değişmeden korunur.

```python
def l_system(axiom, rules, iterations):
    current = axiom

    for _ in range(iterations):
        current = ''.join(
            rules.get(symbol, symbol)
            for symbol in current
        )

    return current

rules = {'F': 'F[+F]F[-F]F'}
plant = l_system('F', rules, 4)
print(plant[:120])
```

Fonksiyonun çıktısı daha sonra `turtle`, Pygame veya bir SVG çizim motoruna aktarılabilir. Her `F` için örneğin 5 piksel ilerlemek ve dönüş açısını $25^\circ$ seçmek, çalı benzeri dengeli bir şekil oluşturur.

## Aynı kural, farklı bitkiler

| Değişiklik | Görsel sonuç |
|---|---|
| Açı küçülürse | Daha dik ve sık bir bitki |
| Açı büyürse | Genişleyen, yayvan dallar |
| Yineleme artarsa | Daha yoğun ve ayrıntılı yapı |
| Dal uzunluğu rastgeleleşirse | Daha organik görünüm |
| Birden fazla kural kullanılırsa | Tür çeşitliliği ve asimetri |

Tamamen deterministik bir L-Sistemi kusursuz simetri üretebilir; doğa ise rüzgâr, ışık ve besin gibi etkenlerle küçük sapmalar gösterir. Dönüş açısına $\pm 3^\circ$ rastgelelik eklemek veya her adımda dal uzunluğunu $r$ oranında küçültmek daha gerçekçi sonuç verir:

$$L_n=L_0r^n, \qquad 0<r<1$$

L-Sistemlerinin büyüsü, görüntüyü değil büyüme sürecini kodlamasında yatar. Birkaç üretim kuralı; ağaçlardan mercanlara, damarlardan fantastik uzay bitkilerine kadar pek çok formun temelini oluşturabilir. Kısacası burada bahçıvan sizsiniz, toprağınız matematik ve tohumunuz yalnızca bir karakter dizisi!

---
layout: post
title: "Büyük O, Teta ve Omega: Algoritma Karmaşıklığının Üç Farklı Yüzü"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - büyük-o
  - karmaşıklık
  - performans
  - veri-yapıları
  - python
toc: true
image: /img/buyuk-o-teta-62.png
---

Bir algoritmanın hızlı olduğunu söylemek tek başına pek anlamlı değildir. Hangi girdide, ne kadar hızlı ve büyüyen veri karşısında nasıl davranıyor? İşte Büyük O, Teta ve Omega notasyonları bu soruları matematiksel sınırlarla yanıtlar. Ancak yaygın inanışın aksine Büyük O doğrudan “en kötü”, Omega “en iyi”, Teta da “ortalama” durum demek değildir. Durum analizi ile asimptotik sınır, birbiriyle ilişkili ama farklı kavramlardır.

``

## Önce asimptotik analiz nedir?

Asimptotik analiz, girdi boyutu $n$ büyürken algoritmanın zaman veya bellek ihtiyacının nasıl değiştiğini inceler. Donanım, programlama dili ve birkaç milisaniyelik sabit farklar yerine büyüme eğilimine odaklanır.

Örneğin çalışma süresi

$$T(n)=3n^2+5n+20$$

olan bir algoritmada, büyük $n$ değerleri için $n^2$ terimi baskındır. Sabit katsayılar ve düşük dereceli terimler göz ardı edildiğinde büyüme $n^2$ ile ifade edilir.

## Üç notasyonun temel farkı

| Notasyon | Anlamı | Verdiği sınır | Basit yorum |
|---|---|---|---|
| $O(g(n))$ | En fazla bu hızda büyür | Üst sınır | “Bundan daha kötü büyümez.” |
| $\Omega(g(n))$ | En az bu hızda büyür | Alt sınır | “En az bunun kadar büyür.” |
| $\Theta(g(n))$ | Aynı mertebede büyür | Sıkı sınır | “Büyüme hızı tam olarak budur.” |

![buyuk-o-teta-62](/img/buyuk-o-teta-62.svg)


### Büyük O: Üst sınır

$f(n)=O(g(n))$ diyebilmek için yeterince büyük $n$ değerlerinde

$$0 \leq f(n) \leq c\,g(n)$$

olacak pozitif bir $c$ sabiti bulunmalıdır. Örneğin $3n^2+5n+20$, hem $O(n^2)$ hem de teknik olarak $O(n^3)$ içindedir. Fakat $O(n^2)$ daha bilgilendirici ve daha sıkı bir üst sınırdır.

### Omega: Alt sınır

$f(n)=\Omega(g(n))$, fonksiyonun en az $g(n)$ kadar hızlı büyüdüğünü belirtir:

$$0 \leq c\,g(n) \leq f(n)$$

Örneğin $3n^2+5n+20$, $\Omega(n^2)$ sınıfındadır. Bu notasyon algoritmanın belirli bir maliyetin altına inemeyeceğini anlatır.

### Teta: Sıkı sınır

Teta, alt ve üst sınırın birleşimidir:

$$c_1g(n) \leq f(n) \leq c_2g(n)$$

Dolayısıyla $f(n)=\Theta(g(n))$ ise fonksiyon hem $O(g(n))$ hem de $\Omega(g(n))$ olur. Örneğimiz için en açıklayıcı ifade $T(n)=\Theta(n^2)$ biçimindedir.

## En iyi, ortalama ve en kötü durum

Durumlar, girdinin algoritmayı nasıl etkilediğini; notasyonlar ise seçilen durumdaki büyümeye ilişkin sınırı belirtir.

| Durum | Doğrusal aramadaki örnek | Karmaşıklık |
|---|---|---|
| En iyi | Aranan değer ilk elemandır | $\Theta(1)$ |
| Ortalama | Değer genellikle listenin ortalarındadır | $\Theta(n)$ |
| En kötü | Değer sondadır veya hiç yoktur | $\Theta(n)$ |

Burada her durum için Teta kullanabildiğimize dikkat edin. “En kötü durum $O(n)$” doğrudur; fakat sıkı sınır biliniyorsa “en kötü durum $\Theta(n)$” daha güçlü bir ifadedir. Ortalama durum analizi ise girdilerin olasılık dağılımını gerektirir. Her girdinin eşit olasılıklı olduğunu varsaymak her zaman gerçekçi değildir.

## Kod üzerinde görelim

Aşağıdaki Python fonksiyonu, doğrusal arama yaparken kaç karşılaştırma gerçekleştirildiğini de döndürür:

```python
def linear_search(values, target):
    comparisons = 0

    for index, value in enumerate(values):
        comparisons += 1
        if value == target:
            return index, comparisons

    return -1, comparisons

numbers = [8, 3, 12, 7, 21]
print(linear_search(numbers, 8))   # En iyi durum: 1 karşılaştırma
print(linear_search(numbers, 21))  # En kötü durum: 5 karşılaştırma
```

İlk çağrıda maliyet girdi boyutundan bağımsızdır. İkinci çağrıda karşılaştırma sayısı $n$ ile birlikte doğrusal büyür.

## Hangisini kullanmalıyız?

Bir algoritmayı tanıtırken analiz edilen durumu açıkça söylemek en güvenli yaklaşımdır: “en kötü durumda $\Theta(n^2)$” gibi. Yalnızca güvenli bir üst sınır biliniyorsa Büyük O, kaçınılmaz bir alt sınır gösteriliyorsa Omega, büyüme kesin biçimde sınırlandırılabiliyorsa Teta kullanılmalıdır. Kısacası notasyonlar yarışmıyor; algoritmanın performansını farklı açılardan aydınlatıyor.

---
layout: post
title: "Kök Avcıları: Yarıya Bölme ve Babil Yöntemiyle Sayısal Çözümler"
math: true
categories: 
  - Bilgi
tags: 
  - sayısal yöntemler
  - kök bulma
  - yarıya bölme
  - babil yöntemi
  - python
  - matematik
toc: true
image: /img/kok-avcilari-yariya-10.png
---

Bir denklemin kökünü bulmak, $f(x)=0$ eşitliğini sağlayan $x$ değerini aramak demektir. Bazı denklemler kalem ve kâğıtla kolayca çözülürken, karmaşık fonksiyonlar analitik çözümlere pek yanaşmaz. Böyle durumlarda bilgisayarlar sonucu sihirle değil, gittikçe iyileşen tahminlerle bulur. Yarıya bölme ve Babil karekök yöntemi, bu yaklaşımın hem güvenilir hem de öğretici iki örneğidir.
``

## Sayısal kök bulmanın temel fikri

Sayısal yöntemlerde çoğunlukla kesin sonuç yerine belirli bir hata payına sahip yaklaşık sonuç aranır. Bir tahmin $x_n$ ile gerçek kök $r$ arasındaki fark

$$
e_n = \vert x_n-r\vert 
$$

şeklinde ifade edilir. Gerçek kök bilinmiyorsa ardışık tahminlerin farkı veya $\vert f(x_n)\vert $ değeri hata göstergesi olarak kullanılabilir. Sonuç yeterince küçük olduğunda algoritma durdurulur. Bu sınır, genellikle $\varepsilon$ ile gösterilen toleranstır.

## Yarıya bölme yöntemi

Yarıya bölme, yani **bisection**, sürekli bir fonksiyonun işaret değiştirdiği aralıkta en az bir kök bulunduğunu söyleyen Ara Değer Teoremi'ne dayanır. $[a,b]$ aralığında

$$
f(a)f(b)<0
$$

ise uçlardaki değerler farklı işaretlidir. Önce orta nokta hesaplanır:

$$
c=\frac{a+b}{2}
$$

Ardından kökün $[a,c]$ veya $[c,b]$ aralıklarından hangisinde kaldığı işaret kontrolüyle belirlenir. Her turda aralık yarıya indiği için yöntem yavaş ama kararlı biçimde köke yaklaşır. Başlangıç aralığının uzunluğu $L$ ise $n$ adım sonrasındaki hata en fazla yaklaşık $L/2^n$ olur.

```python
def bisection(f, a, b, tolerance=1e-8, max_steps=100):
    if f(a) * f(b) >= 0:
        raise ValueError("Uç noktalar farklı işaretli olmalı.")

    for _ in range(max_steps):
        middle = (a + b) / 2

        if abs(f(middle)) < tolerance or (b - a) / 2 < tolerance:
            return middle

        if f(a) * f(middle) < 0:
            b = middle
        else:
            a = middle

    return (a + b) / 2

root = bisection(lambda x: x**3 - x - 2, 1, 2)
print(root)
```

Kod, $x^3-x-2=0$ denkleminin kökünü 1 ile 2 arasında arar. Aralık şartı sağlanmazsa yanlış güven vermek yerine hata üretir.

## Babil karekök yöntemi

Babil yöntemi, bir $S$ sayısının karekökünü hesaplamak için kullanılır. Amaç $x^2-S=0$ denklemini çözmektir. Pozitif bir $x_n$ tahmini seçilir ve şu yineleme uygulanır:

$$
x_{n+1}=\frac{1}{2}\left(x_n+\frac{S}{x_n}\right)
$$

Tahmin büyükse $S/x_n$ küçük, tahmin küçükse $S/x_n$ büyük olur. Bu iki değerin ortalaması alınarak dengeli ve daha doğru bir tahmin elde edilir. Yöntem aslında Newton-Raphson algoritmasının $f(x)=x^2-S$ fonksiyonuna uygulanmış hâlidir.

```python
def babylonian_sqrt(number, tolerance=1e-12):
    if number < 0:
        raise ValueError("Gerçek sayılarda negatif sayının karekökü yoktur.")
    if number == 0:
        return 0.0

    estimate = number if number >= 1 else 1.0

    while True:
        next_estimate = (estimate + number / estimate) / 2
        if abs(next_estimate - estimate) < tolerance:
            return next_estimate
        estimate = next_estimate

print(babylonian_sqrt(10))
```

Buradaki döngü, iki ardışık tahmin arasındaki fark toleranstan küçük olduğunda sona erer. Babil yöntemi köke yaklaştığında doğru basamak sayısını çok hızlı artırır.

## Yöntemleri karşılaştıralım

| Özellik | Yarıya bölme | Babil yöntemi |
|---|---|---|
| Kullanım alanı | Genel sürekli denklemler | Pozitif karekök hesabı |
| Başlangıç gereksinimi | İşaret değiştiren aralık | Pozitif tahmin |
| Yakınsama | Doğrusal ve düzenli | Çok hızlı, karesel |
| Güvenilirlik | Aralık doğruysa çok yüksek | Uygun pozitif tahminle yüksek |
| Türev gereksinimi | Yok | Formül türevden üretilse de kodda yok |

Yarıya bölme, “yavaş ama emin adımlarla” ilerleyen bir kâşiftir. Babil yöntemi ise özel görevinde hızlanan bir sprinter gibidir. İkisinin ortak dersi açıktır: Bilgisayarlar kökü tek hamlede bilmez; hatayı sistemli biçimde küçülterek ona yaklaşır.

![kok-avcilari-yariya-10](/img/kok-avcilari-yariya-10.svg)


---
layout: post
title: "Monte Carlo ve Las Vegas Algoritmaları: Yanlış Cevap mı, Değişken Süre mi?"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - olasılıksal algoritmalar
  - monte carlo
  - las vegas
  - python
  - karmaşıklık
toc: true
---

Rastgelelik yalnızca zar atarken işimize yaramaz; bazen bir algoritmayı daha hızlı, daha basit veya pratik hâle getirir. Olasılıksal algoritmaların iki ünlü ailesi olan **Monte Carlo** ve **Las Vegas**, rastgeleliği farklı bedeller karşılığında kullanır: İlki çalışma süresini sınırlar fakat küçük bir yanlışlık riskini kabul eder; ikincisi ise doğru cevabı garanti eder ancak ne zaman biteceği konusunda biraz gizemli davranır.

``

## Temel ayrım: Neyi feda ediyoruz?

Monte Carlo algoritması belirli ya da öngörülebilir bir süre içinde cevap verir. Buna karşılık sonuç, düşük de olsa bir olasılıkla yanlış olabilir. Las Vegas algoritması ise yalnızca doğru sonuç üretir; rastgelelik, cevabın doğruluğunu değil çalışma süresini etkiler.

| Özellik | Monte Carlo | Las Vegas |
|---|---|---|
| Sonucun doğruluğu | Olasılıksal | Garantili |
| Çalışma süresi | Genellikle sınırlı | Değişken |
| Başarısızlık biçimi | Yanlış cevap | Uzun bekleme |
| Tekrarlamanın etkisi | Hata olasılığını azaltır | Ortalama süreyi değiştirebilir |
| Tipik kullanım | Asallık testi, yaklaşık hesaplama | Rastgele QuickSort, arama |

Bir Monte Carlo algoritmasının tek çalıştırmada hata olasılığı $p$ olsun. Bağımsız biçimde $k$ kez çalıştırılıp çoğunluk kararı alınırsa hata ihtimali hızla küçülür. Basitleştirilmiş bazı senaryolarda bu davranış

$$P(\text{tüm denemelerin hatalı olması}) = p^k$$

şeklinde görülebilir. Örneğin $p=0.1$ ve $k=5$ için değer $10^{-5}$ olur. Rastgelelik burada bir kusurdan çok, ayarlanabilir bir doğruluk düğmesidir.

## Monte Carlo örneği: $\pi$ tahmini

Birim karenin içine rastgele noktalar atalım. Noktanın çeyrek dairenin içinde kalma olasılığı yaklaşık $\pi/4$ olduğundan oranı dörtle çarparak $\pi$ tahmini elde edebiliriz.

```python
import random

def pi_tahmini(deneme_sayisi):
    dairede = 0

    for _ in range(deneme_sayisi):
        x = random.random()
        y = random.random()

        if x * x + y * y <= 1:
            dairede += 1

    return 4 * dairede / deneme_sayisi

print(pi_tahmini(100_000))
```

Kod kesin $\pi$ değerini vermez; deneme sayısı arttıkça genellikle daha iyi bir yaklaşım üretir. İstatistiksel hata çoğunlukla yaklaşık olarak

$$O\left(\frac{1}{\sqrt{n}}\right)$$

hızında azalır. Yani hatayı yarıya indirmek için yaklaşık dört kat nokta gerekebilir. Monte Carlo’nun faturası burada açıkça görülür: hızlı ve kolay tahmin, fakat mutlak doğruluk garantisi yoktur.

## Las Vegas örneği: Rastgele seçimle arama

Aşağıdaki algoritma listedeki hedefi rastgele indisler deneyerek arar. Hedef bulunduğunda verilen cevap kesinlikle doğrudur; ancak kaç deneme yapılacağını önceden bilemeyiz.

```python
import random

def rastgele_ara(liste, hedef):
    if hedef not in liste:
        return -1

    while True:
        indis = random.randrange(len(liste))
        if liste[indis] == hedef:
            return indis
```

Baştaki üyelik kontrolü, hedef yoksa sonsuz döngüyü engeller. Hedefin tek bir konumda bulunduğu $n$ elemanlı listede her denemenin başarı olasılığı $1/n$ olur. Beklenen deneme sayısı bu nedenle

$$E[T] = \frac{1}{1/n} = n$$

olsa da algoritma ilk denemede de bitebilir, çok daha uzun da sürebilir. Daha gerçekçi bir Las Vegas örneği olan rastgele QuickSort da doğru sıralamayı garanti eder; rastgele pivot seçimi kötü bölünmelerin sürekli yaşanma riskini azaltır ve beklenen süreyi $O(n\log n)$ yapar.

## Hangisini seçmeliyiz?

Yanlış cevabın maliyeti düşükse veya sonuç tekrar doğrulanabiliyorsa Monte Carlo güçlü bir tercihtir. Grafik işleme, simülasyon, büyük veri tahminleri ve bazı asallık testleri buna uygundur. Hatalı cevabın güvenlik, para veya veri bütünlüğü açısından kabul edilemez olduğu durumlarda Las Vegas yaklaşımı daha güvenlidir.

Kısacası seçim bir mühendislik pazarlığıdır: **Monte Carlo saati kontrol eder, doğruluğu olasılığa bırakır; Las Vegas doğruluğu kontrol eder, saati şansa bırakır.**

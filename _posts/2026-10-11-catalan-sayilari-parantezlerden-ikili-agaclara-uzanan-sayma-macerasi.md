---
layout: post
title: "Catalan Sayıları: Parantezlerden İkili Ağaçlara Uzanan Sayma Macerası"
math: true
categories: 
  - Bilgi
tags: 
  - catalan sayıları
  - kombinatorik
  - algoritma
  - dinamik programlama
  - ikili ağaç
  - python
toc: true
image: /img/catalan-sayilari-parantezlerden-39.png
---

Bazı sayı dizileri matematiğin gizli aktörleri gibidir: Farklı görünen problemlerde tekrar tekrar sahneye çıkarlar. Catalan sayıları da dengeli parantezlerden çokgenlere, ikili arama ağaçlarından dağ yollarına kadar şaşırtıcı sayıda yapıyı sayar. İlk terimleri $1, 1, 2, 5, 14, 42, 132$ olan bu dizi, “Kaç farklı geçerli yapı oluşturabilirim?” sorusunun en renkli cevaplarından biridir.
``

## Catalan sayısının matematiksel tanımı

Sıfırıncı Catalan sayısı $C_0=1$ kabul edilir. Genel formül şöyledir:

$$
C_n = \frac{1}{n+1}\binom{2n}{n} = \frac{(2n)!}{(n+1)!n!}
$$

Buradaki merkezi binom katsayısı, $2n$ konum içinden $n$ tanesini seçer. Ancak seçilen her dizilim geçerli değildir. Örneğin açılan parantez sayısının hiçbir noktada kapanan parantez sayısından az olmaması gerekir. Formüldeki $n+1$ bölümü, bu geçersiz düzenlemeleri ayıklayan kombinatorik düzeltmedir.

Catalan sayıları özyinelemeli olarak da hesaplanabilir:

$$
C_{n+1}=\sum_{i=0}^{n} C_iC_{n-i}
$$

Bu bağıntının arkasındaki fikir bölüp birleştirmedir. Bir yapı kökünden iki parçaya ayrılıyorsa sol tarafta $i$, sağ tarafta $n-i$ eleman bulunabilir. Olasılıkların çarpılması ve bütün bölünmelerin toplanması Catalan sonucunu verir.

| $n$ | $C_n$ | Dengeli parantez çifti sayısı |
|---:|---:|---:|
| 0 | 1 | Boş dizi |
| 1 | 1 | `()` |
| 2 | 2 | `(())`, `()()` |
| 3 | 5 | Beş farklı dizilim |
| 4 | 14 | On dört farklı dizilim |

## Dengeli parantezler neden Catalan sayısıdır?

$n$ çift açma ve kapama parantezi içeren bir dizide toplam $2n$ karakter vardır. Geçerli bir dizilim iki kurala uyar:

1. Toplam açma ve kapama parantezi sayıları eşittir.
2. Soldan sağa ilerlerken kapanan parantez sayısı, açılanlardan fazla olamaz.

Örneğin `(()())` geçerliyken `())(()` geçersizdir. İkinci dizi toplamda eşit sayıda parantez içerse bile üçüncü karakterde henüz açılmamış bir parantezi kapatmaya çalışır. Matematik bile “Önce aç, sonra kapat!” der.

## İkili ağaçlarla bağlantısı

$n$ düğümlü farklı ikili ağaç biçimlerinin sayısı da $C_n$ değeridir. Kök düğümü seçtikten sonra kalan düğümler sol ve sağ alt ağaçlar arasında dağıtılır. Sol alt ağaçta $i$ düğüm varsa sağ tarafta $n-1-i$ düğüm bulunur.

| Problem | Ayrıştırma biçimi | Sonuç |
|---|---|---:|
| Dengeli parantez | Dış parantezin içi ve sonrası | $C_n$ |
| İkili ağaç | Sol ve sağ alt ağaç | $C_n$ |
| Çokgen üçgenleme | Seçilen üçgenin iki yanı | $C_{n-2}$ |
| Izgara yolu | Köşegeni aşmayan yollar | $C_n$ |

Aynı sayıların ortaya çıkmasının nedeni, bu problemlerin yüzeyde farklı olsa da aynı özyinelemeli bölünme yapısını taşımasıdır.

## Python ile hesaplama

Aşağıdaki dinamik programlama yaklaşımı, özyinelemeli bağıntıyı kullanır. `dp[k]`, $k$ boyutundaki yapıların sayısını saklar:

```python
def catalan(n):
    dp = [0] * (n + 1)
    dp[0] = 1

    for boyut in range(1, n + 1):
        for sol in range(boyut):
            sag = boyut - 1 - sol
            dp[boyut] += dp[sol] * dp[sag]

    return dp[n]

print([catalan(i) for i in range(8)])
# [1, 1, 2, 5, 14, 42, 132, 429]
```

Algoritmanın zaman karmaşıklığı $O(n^2)$, alan karmaşıklığı ise $O(n)$ olur. Yalnızca tek bir $C_n$ değeri gerekiyorsa faktöriyel formülü daha hızlı olabilir; dinamik programlama ise dizinin tüm ara terimlerini üretmek ve mantığı görmek için daha öğreticidir.

Catalan sayıları, farklı problemlerin ortak matematiksel iskeletini fark etmenin harika bir örneğidir. Bir soruda dengeli parantez, ikili ağaç, köşegeni aşmayan yol veya çokgen üçgenleme görürseniz, sahne arkasında bir Catalan sayısının kostümünü giymekte olabileceğini unutmayın.

![catalan-sayilari-parantezlerden-39](/img/catalan-sayilari-parantezlerden-39.svg)


---
layout: post
title: "Kuantum Algoritmaları Kriptografinin Geleceğini Nasıl Değiştirecek?"
math: true
categories: 
  - Bilgi
tags: 
  - kuantum bilgisayarlar
  - shor algoritması
  - kriptografi
toc: true
---

İnternet bankacılığından mesajlaşma uygulamalarına kadar dijital dünyanın güvenliği, bazı matematik problemlerinin klasik bilgisayarlar için aşırı zor olmasına dayanıyor. Ancak yeterince güçlü bir kuantum bilgisayar, Shor algoritması sayesinde bu problemleri beklenenden çok daha hızlı çözebilir. Peki yarın sabah bütün parolalarımız mı ortaya dökülecek? Kısa cevap: Hayır. Uzun cevap ise kuantum fiziği, asal çarpanlar ve ciddi bir kriptografik dönüşüm içeriyor.

``

## Güvenliğin arkasındaki matematik

RSA şifrelemesinde iki büyük asal sayı seçilir ve çarpılır:

$$N = p \times q$$

Açık anahtarın içinde $N$ bulunurken $p$ ve $q$ gizli tutulur. Küçük sayılarda çarpanları bulmak kolaydır; yüzlerce basamaklı bir $N$ içinse klasik yöntemlerin işi son derece zordur. RSA'nın güvenliği kabaca bu **çarpanlara ayırma probleminin** maliyetine yaslanır.

Benzer şekilde eliptik eğri kriptografisi, ayrık logaritma problemini kullanır. Klasik bilgisayarlar bu problemler için bilinen verimli çözümlere sahip değildir. Shor algoritması ise her ikisini de polinom zamanda çözebilen bir kuantum algoritmasıdır.

| Sistem | Dayandığı problem | Kuantum tehdidi |
|---|---|---|
| RSA | Büyük sayıların çarpanlara ayrılması | Shor ile kırılabilir |
| ECC | Eliptik eğri ayrık logaritması | Shor ile kırılabilir |
| AES | Anahtarın aranması | Grover ile güvenlik seviyesi azalır |
| SHA-256 | Özet ve çakışma direnci | Daha uzun özetlerle güçlendirilebilir |

## Shor algoritmasının numarası ne?

Algoritmanın temel fikri, doğrudan çarpan aramak yerine periyodik bir fonksiyonun periyodunu bulmaktır. Rastgele bir $a$ seçilerek şu fonksiyon incelenir:

$$f(x) = a^x \bmod N$$

Bu fonksiyon belirli bir $r$ periyoduyla tekrar eder. Kuantum bilgisayar, süperpozisyon ve Kuantum Fourier Dönüşümü kullanarak $r$ değerini verimli biçimde tahmin eder. Uygun koşullarda çarpanlar şöyle elde edilir:

$$gcd(a^{r/2}-1, N)$$

$$gcd(a^{r/2}+1, N)$$

Aşağıdaki Python kodu Shor algoritmasını çalıştırmaz; yalnızca kuantum bölümünün uygun bir periyot bulduğunu varsayarak klasik son adımı gösterir:

```python
from math import gcd

def extract_factors(n, a, period):
    # Tek periyotlar kullanışlı değildir.
    if period % 2 != 0:
        return None

    value = pow(a, period // 2, n)
    p = gcd(value - 1, n)
    q = gcd(value + 1, n)

    if p not in (1, n) and p * q == n:
        return p, q
    return None

print(extract_factors(15, 2, 4))  # (3, 5)
```

Buradaki sihirli parça `period` değerinin kuantum devresiyle bulunmasıdır. Klasik kod yalnızca sonuçları ortak bölen hesabına dönüştürür.

## Tehdit bugün ne kadar gerçek?

Mevcut kuantum cihazları gürültülü, küçük ve hata üretmeye yatkındır. RSA-2048 gibi gerçek anahtarları kırmak için uzun süre kararlı çalışabilen, hata düzeltmeli ve muhtemelen milyonlarca fiziksel kübit kullanan makineler gerekir. Dolayısıyla “birkaç saniyede bütün interneti kırmak” günümüz donanımıyla mümkün değildir.

Yine de **şimdi topla, sonra çöz** saldırısı önemlidir. Saldırganlar bugün şifreli verileri kaydedip gelecekteki kuantum bilgisayarlarla çözebilir. Sağlık kayıtları, devlet belgeleri ve ticari sırlar yıllarca değerli kalabileceğinden dönüşüm şimdiden başlamalıdır.

## Kuantum sonrası kriptografi

Çözüm, kuantuma dayanıklı matematiksel problemlere geçmektir. NIST tarafından standartlaştırılan ML-KEM anahtar paylaşımı ve ML-DSA dijital imzaları bu dönüşümün önemli parçalarıdır.

| Yaklaşım | Avantaj | Dikkat edilmesi gereken |
|---|---|---|
| Kafes tabanlı algoritmalar | Hızlı ve güçlü adaylar | Daha büyük anahtarlar |
| Hash tabanlı imzalar | Basit güvenlik varsayımları | Büyük imza boyutları |
| Hibrit kullanım | Eski ve yeni sistemi birlikte korur | Ek protokol karmaşıklığı |

Kurumların kriptografik envanter çıkarması, uzun ömürlü verileri belirlemesi ve algoritmaların kolay değiştirilebildiği sistemler tasarlaması gerekiyor. Kuantum kıyameti henüz kapıda olmayabilir; fakat kriptografide hazırlık, alarm çaldıktan sonra değil, matematik hâlâ yanımızdayken yapılır.

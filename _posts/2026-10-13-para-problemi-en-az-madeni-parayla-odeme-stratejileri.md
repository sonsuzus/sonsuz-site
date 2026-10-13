---
layout: post
title: "Para Problemi: En Az Madeni Parayla Ödeme Stratejileri"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - dinamik programlama
  - açgözlü algoritma
  - optimizasyon
  - python
toc: true
image: /img/para-problemi-en-28.png
---

![para-problemi-en-28](/img/para-problemi-en-28.svg)


Cebinizde 1, 5, 10 ve 25 kuruşluk madeni paralar olduğunu düşünün. 37 kuruş ödemek için hangi paraları seçersiniz? İnsan zihni genellikle önce en büyük paraya uzanır. Ancak bu doğal yaklaşım her para sisteminde en iyi sonucu vermez. **Para problemi**, hedeflenen bir miktarı mevcut kupürlerle ve mümkün olan en az sayıda madeni parayla oluşturmayı amaçlayan klasik bir optimizasyon problemidir.

``

## Problemin Matematiksel Modeli

Madeni para değerleri $C = \{c_1, c_2, \ldots, c_n\}$, ödenecek miktar ise $A$ olsun. Her kupürden sınırsız sayıda bulunduğunu varsayarsak amacımız şu toplamı küçültmektir:

$$\min \sum_{i=1}^{n} x_i$$

Bu optimizasyon aşağıdaki koşula tabidir:

$$\sum_{i=1}^{n} x_i c_i = A, \qquad x_i \geq 0$$

Buradaki $x_i$, $c_i$ değerindeki paradan kaç tane kullanılacağını gösterir. Yani mesele yalnızca toplamı tutturmak değil, bunu en az parçayla yapmaktır.

## Açgözlü Yaklaşım

Açgözlü algoritma her adımda kalan miktarı aşmayan en büyük madeni parayı seçer. Örneğin $C = \{1, 5, 10, 25\}$ ve $A = 37$ için seçimler 25, 10, 1 ve 1 olur. Toplam dört para kullanılır ve bu sonuç optimaldir.

Fakat $C = \{1, 3, 4\}$ ve $A = 6$ olduğunda algoritma 4, 1, 1 seçerek üç para kullanır. Oysa 3 ve 3 ile yalnızca iki para yeterlidir. Açgözlü kahramanımız bu kez büyük paranın cazibesine kapılmıştır!

| Yaklaşım | Optimal sonuç garantisi | Zaman maliyeti | Güçlü yönü |
|---|---:|---:|---|
| Açgözlü | Her sistemde yok | Yaklaşık $O(n)$ | Basit ve hızlıdır |
| Dinamik programlama | Evet | $O(A \cdot n)$ | Genel para sistemlerinde güvenilirdir |
| Özyinelemeli arama | Evet | Üstel olabilir | Mantığı anlamak kolaydır |

Açgözlü yöntemin doğru çalıştığı para kümelerine **kanonik para sistemi** denir. Günlük hayatta kullanılan birçok para sistemi pratik ödeme kolaylığı için bu özelliğe yakın biçimde tasarlanmıştır.

## Dinamik Programlama Çözümü

Dinamik programlama, büyük problemi daha küçük miktarların sonuçlarından kurar. $dp[x]$, $x$ miktarını oluşturmak için gereken en az para sayısı olsun. Başlangıç durumumuz $dp[0] = 0$ değeridir. Geçiş bağıntısı şöyledir:

$$dp[x] = 1 + \min_{c \in C,\ c \leq x} dp[x-c]$$

Her $x$ miktarı için kullanılabilecek son parayı deneriz. Seçilen para $c$ ise geriye $x-c$ kalır. Daha önce hesaplanan bu alt problemin sonucuna bir eklenir.

```python
def minimum_coins(coins, amount):
    dp = [float('inf')] * (amount + 1)
    selected = [-1] * (amount + 1)
    dp[0] = 0

    for current in range(1, amount + 1):
        for coin in coins:
            if coin <= current and dp[current - coin] + 1 < dp[current]:
                dp[current] = dp[current - coin] + 1
                selected[current] = coin

    if dp[amount] == float('inf'):
        return -1, []

    result = []
    remaining = amount
    while remaining > 0:
        coin = selected[remaining]
        result.append(coin)
        remaining -= coin

    return dp[amount], result

print(minimum_coins([1, 3, 4], 6))
```

Bu kod yalnızca minimum sayıyı hesaplamaz; `selected` dizisi sayesinde hangi paraların kullanıldığını da geriye doğru çıkarır. Örneğin çıktı `(2, [3, 3])` olur. `dp` dizisi $A+1$ eleman tuttuğu için bellek karmaşıklığı $O(A)$ seviyesindedir.

## Hangi Strateji Seçilmeli?

Para sisteminin kanonik olduğu biliniyorsa açgözlü algoritma hızlı ve pratiktir. Kupürler düzensizse, kullanıcı tarafından belirleniyorsa veya optimal sonuç zorunluysa dinamik programlama daha güvenli seçimdir. Hedef miktar çok büyük olduğunda ise bellek optimizasyonu, matematiksel analiz ya da özel kısa yol yöntemleri düşünülmelidir.

Sonuç olarak para problemi, küçük bir cüzdan hikâyesinin arkasında önemli bir algoritma dersi saklar: **Yerel olarak en iyi görünen seçim, küresel olarak en iyi çözüm olmayabilir.** Bazen büyük parayı hemen seçmek yerine bütün olasılıkların maliyetini düşünmek gerekir.

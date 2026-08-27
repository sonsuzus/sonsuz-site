---
layout: post
title: "Meet in the Middle: Üstel Aramayı İkiye Bölmenin Olimpiyat Hilesi"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - meet-in-the-middle
  - karmaşıklık
  - dinamik programlama
  - olimpiyat
---

Bazı problemler ilk bakışta masum görünür: Elimizde $n$ eleman vardır, her biri için seç veya seçme kararı veririz. Ancak bu küçük kararların toplamı $2^n$ farklı kombinasyon üretir. $n=40$ için yaklaşık bir trilyon olasılık demektir; bilgisayarınızın fanı bu noktada dramatik bir monoloğa başlayabilir. **Ortadan Buluşma** (Meet in the Middle, MITM), arama uzayını iki parçaya ayırarak bu üstel duvarı aşmaya yarayan klasik olimpiyat tekniğidir.

``

Tekniğin temel fikri şaşırtıcı derecede nettir: $n$ elemanlı kümenin tüm alt kümelerini doğrudan gezmek yerine kümeyi yaklaşık eşit iki yarıya ayırırız. Sol yarının tüm sonuçlarını, ardından sağ yarının tüm sonuçlarını üretir; son olarak bu iki sonuç listesini hedefe göre eşleştiririz. Böylece $2^n$ yerine yaklaşık $2 \cdot 2^{n/2}$ aday üretiriz.

Örneğin hedef toplamı $T$ olan bir alt küme aradığımızı düşünelim. Dizi $A$ iki parçaya ayrılsın: $L$ ve $R$. Her alt küme toplamı şu biçimde yazılabilir:

$$S = S_L + S_R$$

Aradığımız koşul $S=T$ ise, sol tarafta üretilen her $S_L$ için sağ tarafta tam olarak $T-S_L$ değerini ararız. Matematik basit görünür; asıl kazanç, aramanın organizasyonundadır.

| Yaklaşım | Zaman Karmaşıklığı | Bellek Karmaşıklığı | $n=40$ için yaklaşık aday sayısı |
|---|---:|---:|---:|
| Kaba kuvvet | $O(2^n)$ | $O(1)$ | $2^{40}$ |
| MITM + sıralama | $O(n2^{n/2})$ | $O(2^{n/2})$ | $2 \cdot 2^{20}$ |
| MITM + hash tablosu | Beklenen $O(2^{n/2})$ | $O(2^{n/2})$ | $2 \cdot 2^{20}$ |

Buradaki sihir, üstel ifadedeki üsse dokunmaktır. $2^{40}$ ile $2^{20}$ arasındaki fark yalnızca “yarı” değildir: yaklaşık bir milyon katlık ölçek farkı yaratır. Buna karşılık bellek maliyeti artar. Bu nedenle MITM, genellikle $n$ değeri 35-50 bandında olan; kaba kuvvetin yavaş, klasik dinamik programlamanın ise hedef değeri çok büyük olduğu problemlerde parıldar.

Aşağıdaki Python örneği, bir dizide hedef toplamı veren alt küme olup olmadığını bulur. Sağ yarının toplamları bir `set` içinde saklanır; böylece tamamlama değerini ortalama sabit zamanda kontrol ederiz.

```python
from itertools import combinations

def subset_sums(numbers):
    sums = []
    m = len(numbers)
    for mask in range(1 << m):
        total = 0
        for i in range(m):
            if mask & (1 << i):
                total += numbers[i]
        sums.append(total)
    return sums

def has_target_subset(nums, target):
    mid = len(nums) // 2
    left, right = nums[:mid], nums[mid:]

    right_sums = set(subset_sums(right))
    for left_sum in subset_sums(left):
        if target - left_sum in right_sums:
            return True
    return False

print(has_target_subset([3, 34, 4, 12, 5, 2], 9))  # True
```

Bu kod karar problemini çözer: cevap yalnızca doğru veya yanlış olur. Alt kümeyi de geri kazanmak isterseniz, toplam yerine `(toplam, maske)` çiftlerini saklayabilirsiniz. Eşleşme bulunduğunda iki maskeyi birleştirip seçilen indeksleri çıkarırsınız.

MITM her problem için otomatik çözüm değildir. Eleman sayısı 100.000 ise iki yarının bile alt kümelerini üretmek imkânsızdır. Hedef toplam küçükse $O(nT)$ maliyetli bitset veya dinamik programlama daha iyi olabilir. Ayrıca çok fazla tekrar eden toplam varsa sıralı liste, hash tablosundan daha az bellek tüketebilir.

| Problem özelliği | Daha uygun yaklaşım |
|---|---|
| $n \le 25$ | Kaba kuvvet veya özyineleme |
| $35 \le n \le 50$, hedef büyük | Meet in the Middle |
| Hedef $T$ küçük | Dinamik programlama / bitset |
| En yakın toplam aranıyor | MITM + sıralama + iki işaretçi |

Özetle MITM, “tüm seçenekleri dene” fikrinden vazgeçmez; onu stratejik biçimde yeniden düzenler. İki küçük üstel liste üretip doğru çifti bulmak, özellikle yarışma programlamasında devasa görünen arama uzaylarını yönetilebilir hâle getirir.

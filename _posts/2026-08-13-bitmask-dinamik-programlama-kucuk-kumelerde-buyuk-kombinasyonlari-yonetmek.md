---
layout: post
title: "Bitmask Dinamik Programlama: Küçük Kümelerde Büyük Kombinasyonları Yönetmek"
math: true
categories: 
  - Bilgi
tags: 
  - Dinamik Programlama
  - Bitmask
  - Algoritmalar
---

Bazı problemler vardır ki eleman sayısı küçük görünür, fakat olası seçimlerin sayısı astronomiktir. Örneğin 20 şehir arasındaki tüm ziyaret sıralamalarını denemek yaklaşık $20!$ olasılık demektir; bu, kahveniz soğumadan bitecek bir hesap değildir. Bitmask Dinamik Programlama (DP), küçük kümelerdeki alt kümeleri bitlerle temsil ederek tekrar eden hesapları saklar ve bu tür kombinasyon patlamalarını yönetilebilir hâle getirir.
``

Bitmask, her elemanın bir bite karşılık geldiği ikili sayı temsilidir. Bir kümede $n$ eleman varsa, tüm alt kümeler $0$ ile $2^n-1$ arasında bir tamsayıyla kodlanabilir. Örneğin dört görev için `0101` maskesi, 0 ve 2 numaralı görevlerin seçildiğini anlatır. Böylece pahalı set nesneleri yerine hızlı bit işlemleri kullanırız.

| İşlem | Bit düzeyi ifadesi | Anlamı |
|---|---|---|
| Elemanı ekle | `mask | (1 << i)` | `i` elemanının bitini 1 yapar |
| Elemanı çıkar | `mask & ~(1 << i)` | `i` elemanının bitini 0 yapar |
| Eleman seçili mi? | `mask & (1 << i)` | Sonuç sıfır değilse seçilidir |
| Alt küme sayısı | `1 << n` | Toplam $2^n$ olası durum |

DP tarafında kritik soru şudur: **Bir alt kümeyi tamamlamak için geçmişten hangi bilgi gerçekten gereklidir?** Gezgin Satıcı Problemi'nin küçük sürümünde bu bilgi, ziyaret edilen şehirler ve bulunulan son şehirdir. Bu nedenle durumu `dp[mask][last]` şeklinde tanımlarız. Değer, `mask` içindeki şehirleri dolaşıp `last` şehrinde bitmenin en düşük maliyetidir.

Başlangıç şehri 0 olsun. Geçişte henüz ziyaret edilmemiş her `next` şehri denenir:

$$dp[mask \cup \{next\}][next] = \min(dp[mask \cup \{next\}][next],\ dp[mask][last] + cost[last][next])$$

Bu formülün gücü, aynı ziyaret kümesine ve aynı son şehre farklı rotalardan ulaşıldığında yalnızca en ucuz olanı tutmasındadır. Brute force yaklaşımı $O(n!)$ iken Held-Karp tarzı bu çözüm yaklaşık $O(n^2 2^n)$ zaman ve $O(n2^n)$ bellek kullanır. Hâlâ büyük $n$ için pahalıdır; ancak $n \approx 15-22$ aralığında çoğu yarışma ve uygulama senaryosunda son derece etkilidir.

```python
from math import inf

def tsp(cost):
    n = len(cost)
    full = 1 << n
    dp = [[inf] * n for _ in range(full)]
    dp[1][0] = 0  # Yalnızca başlangıç şehri ziyaret edildi.

    for mask in range(full):
        for last in range(n):
            if dp[mask][last] == inf:
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue  # Ziyaret edilmiş şehre tekrar gitme.
                new_mask = mask | (1 << nxt)
                dp[new_mask][nxt] = min(
                    dp[new_mask][nxt],
                    dp[mask][last] + cost[last][nxt]
                )

    all_visited = full - 1
    return min(dp[all_visited][last] + cost[last][0] for last in range(n))
```

Kod, her maskede erişilebilir son şehirleri dolaşır ve yeni bir şehir ekleyerek durumu büyütür. Pratikte `cost` matrisi asimetrik de olabilir; yani A'dan B'ye gitmek, B'den A'ya gitmekle aynı maliyette olmak zorunda değildir.

| Yaklaşım | Zaman karmaşıklığı | Ne zaman tercih edilir? |
|---|---:|---|
| Tüm permütasyonlar | $O(n!)$ | Çok küçük, örneğin $n \leq 10$ |
| Backtracking + budama | Probleme bağlı | Güçlü alt sınırlar varsa |
| Bitmask DP | $O(n^2 2^n)$ | Küçük kümeler ve kesin optimum gerektiğinde |

Bitmask DP sadece rota bulmak için değildir: atama problemleri, minimum kapsama, bağımsız görev seçimi, alt küme toplamı ve takım oluşturma gibi alanlarda da kullanılır. Altın kural basittir: Eleman sayısı küçükse ama alt kümeler önem taşıyorsa, maskeyi; kararın son etkisi önemliyse, DP durumuna son konumu eklemeyi düşünün. Bitler küçük olabilir, ama doğru kullanıldıklarında oldukça büyük problemleri hizaya sokarlar.

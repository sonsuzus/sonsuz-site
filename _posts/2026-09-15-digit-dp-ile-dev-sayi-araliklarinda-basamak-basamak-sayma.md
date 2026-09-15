---
layout: post
title: "Digit DP ile Dev Sayı Aralıklarında Basamak Basamak Sayma"
math: true
categories: 
  - Bilgi
tags: 
  - digit dp
  - dinamik programlama
  - algoritma
  - basamak
  - sayma
  - rekabetçi programlama
toc: true
---

Bir aralıkta belirli özelliklere sahip kaç sayı bulunduğunu hesaplamak bazen göründüğünden çok daha zordur. Örneğin, $1$ ile $10^{18}$ arasında rakamları toplamı 42 olan veya içinde hiç 7 geçmeyen sayıları tek tek kontrol edemeyiz. Digit DP, yani basamak dinamik programlama, tam burada devreye girerek sayıları değil, sayıların basamaklarında oluşabilecek durumları sayar.
``
## Temel fikir: Aralığı üst sınıra dönüştürmek

Digit DP problemleri çoğunlukla şu fonksiyonla çözülür:

$$F(N) = [0,N] \text{ aralığında koşulu sağlayan sayı adedi}$$

Böylece $[L,R]$ aralığının cevabı basitçe

$$Cevap = F(R) - F(L-1)$$

olur. Bu dönüşüm önemlidir; çünkü yalnızca “$N$ sayısını aşmadan basamakları nasıl seçerim?” sorusuna odaklanmamızı sağlar.

Sayının basamaklarını soldan sağa gezerken genellikle aşağıdaki durumlar tutulur:

| Durum | Anlamı |
|---|---|
| `pos` | Şu anda işlenen basamağın konumu |
| `tight` | Seçimler hâlâ üst sınırın basamaklarıyla aynı mı? |
| `started` | Sayının anlamlı kısmı başladı mı? |
| `state` | Rakam toplamı, kalan veya önceki rakam gibi probleme özel bilgi |

`tight` doğruysa mevcut basamak en fazla $N$'nin aynı konumdaki rakamı olabilir. Yanlışsa artık sınırdan küçük bir sayı oluşturduğumuz kesindir ve $0$ ile $9$ arasındaki tüm rakamları özgürce deneyebiliriz.

## Neden klasik döngü yetmez?

| Yaklaşım | Zaman karmaşıklığı | Uygun aralık |
|---|---:|---|
| Her sayıyı kontrol etme | $O(N \cdot d)$ | Küçük sınırlar |
| Kombinasyon formülleri | Probleme bağlı | Basit koşullar |
| Digit DP | Yaklaşık $O(d \cdot durum \cdot 10)$ | $10^{18}$ gibi sınırlar |

Burada $d$, basamak sayısıdır. Digit DP aynı `pos`, `tight` ve problem durumuna tekrar ulaşıldığında sonucu önbellekten getirir. Böylece devasa sayı uzayı küçük bir durum grafiğine dönüşür.

## Örnek: Rakamları toplamı hedefe eşit sayılar

Aşağıdaki Python kodu, $0$ ile $N$ arasında rakamları toplamı `target` olan sayıların adedini hesaplar:

```python
from functools import lru_cache

def count_up_to(n, target):
    if n < 0:
        return 0

    digits = list(map(int, str(n)))

    @lru_cache(None)
    def dp(pos, total, tight):
        # Tüm basamaklar seçildiyse toplamı kontrol et.
        if pos == len(digits):
            return int(total == target)

        # Toplam hedefi geçtiyse devam etmek gereksizdir.
        if total > target:
            return 0

        limit = digits[pos] if tight else 9
        answer = 0

        for digit in range(limit + 1):
            next_tight = tight and (digit == limit)
            answer += dp(pos + 1, total + digit, next_tight)

        return answer

    return dp(0, 0, True)

def count_in_range(left, right, target):
    return count_up_to(right, target) - count_up_to(left - 1, target)

print(count_in_range(100, 10000, 10))
```

Fonksiyondaki baştaki sıfırlar sorun oluşturmaz: `0073`, sayısal olarak 73’ü temsil eder ve rakam toplamı değişmez. Ancak “kaç basamaklı?”, “ilk rakam nedir?” veya “yan yana iki eşit rakam var mı?” gibi koşullarda `started` durumu eklenmelidir. Böylece henüz başlamamış sıfırlar gerçek basamaklarla karıştırılmaz.

## Durumu doğru tasarlamak

Digit DP’nin zor kısmı kod değil, geçmişten hangi bilginin geleceği etkilediğini bulmaktır. Bölünebilirlik için `remainder`, yasaklı alt dize için otomat durumu, ardışık rakamlar için `previous_digit` tutulabilir. Örneğin yeni kalan

$$yeni = (eski \cdot 10 + rakam) \bmod K$$

şeklinde güncellenir.

Her ayrıntıyı duruma eklemek belleği şişirir; eksik bilgi eklemek ise yanlış sonuç üretir. Altın kural şudur: Gelecekteki seçimlerin sonucunu etkileyen en küçük bilgiyi sakla. Bu denge kurulduğunda Digit DP, astronomik aralıkları birkaç bin durumla sayan oldukça güçlü ve şaşırtıcı derecede eğlenceli bir tekniğe dönüşür.

---
layout: post
title: "Probabilistic DP: Olasılıklı Olimpiyat Problemlerini Durumlara Ayırma Sanatı"
math: true
categories: 
  - Bilgi
tags: 
  - dinamik programlama
  - olasılık
  - algoritma
  - olimpiyat
  - beklenen değer
  - cpp
toc: true
---

Bir zar atılıyor, yazı gelirse ilerliyor, tura gelirse başa dönüyorsun… İlk bakışta şans oyunu gibi görünen bu problemler, doğru durumlar tanımlandığında gayet düzenli birer dinamik programlama sorusuna dönüşür. **Probabilistic DP**, rastgele olayların sonuçlarını tek tek simüle etmek yerine her durumdan ulaşılabilecek sonuçların olasılıklarını matematiksel olarak birleştirir.
``
## Temel fikir: Rastgeleliği durumlara hapsetmek

Klasik DP'de bir durumun cevabı önceki veya sonraki durumların cevaplarından hesaplanır. Olasılıklı DP'de de aynı yaklaşım geçerlidir; fark, geçişlerin belirli olasılıklarla gerçekleşmesidir.

`dp[s]`, `s` durumundan başlayınca başarıya ulaşma olasılığı olsun. Bu durumdan `i` sonucuna `p_i` olasılığıyla geçiliyorsa temel bağıntı şöyledir:

$$
dp[s] = \sum_i p_i \cdot dp[next(s,i)]
$$

Bu formül aslında toplam olasılık kuralının DP kıyafeti giymiş hâlidir. Her olası sonucu, gerçekleşme ihtimaliyle ağırlıklandırırız.

| Problem türü | Durumun anlamı | Tipik değer |
|---|---|---|
| Başarı olasılığı | Bu noktadan kazanma ihtimali | `dp[s]` |
| Beklenen adım | Bitirmek için gereken ortalama süre | `E[s]` |
| Olasılık dağılımı | Belirli skorla bitirme ihtimali | `dp[s][skor]` |
| İki oyunculu oyun | Sıra ve mevcut konum | `dp[a][b][turn]` |

## Basit bir model

Adil bir para atarak hedefe ilerlediğimizi düşünelim. Yazı gelirse 1, tura gelirse 2 adım ilerliyoruz. Tam olarak `N` konumuna ulaşmak başarı; hedefi aşmak başarısızlık olsun.

Durumumuz yalnızca mevcut konumdur:

$$
dp[x] = 0.5 \cdot dp[x+1] + 0.5 \cdot dp[x+2]
$$

Sınır koşulları ise çözümün pusulasıdır:

- `dp[N] = 1`: Hedefe ulaştık.
- `dp[x] = 0`, eğer `x > N`: Hedef aşıldı.

Bağıntı daha büyük konumlara bağlı olduğu için tabloyu sağdan sola doldurabiliriz.

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int N;
    cin >> N;

    vector<double> dp(N + 2, 0.0);
    dp[N] = 1.0; // Tam hedef: kesin başarı

    for (int x = N - 1; x >= 0; --x) {
        double oneStep = dp[x + 1];
        double twoSteps = (x + 2 <= N ? dp[x + 2] : 0.0);
        dp[x] = 0.5 * oneStep + 0.5 * twoSteps;
    }

    cout << fixed << setprecision(10) << dp[0] << '\n';
}
```

Kod, her konumdan sonraki iki ihtimali hesaplayıp olasılıklarıyla çarpar. Zaman karmaşıklığı $O(N)$, bellek karmaşıklığı da $O(N)$ olur.

## Beklenen değer sorularında “+1” ayrıntısı

Soru başarı ihtimali yerine beklenen hamle sayısını sorabilir. `E[s]`, `s` durumundan bitişe kadar beklenen adım sayısıysa:

$$
E[s] = 1 + \sum_i p_i \cdot E[next(s,i)]
$$

Buradaki `1`, şu anda yaptığımız hamleyi temsil eder. Olasılık DP'sinde en sık unutulan ayrıntılardan biridir.

| Hesaplanan büyüklük | Geçiş formülü | Bitiş değeri |
|---|---|---|
| Başarı olasılığı | Ağırlıklı olasılık toplamı | Başarıda 1 |
| Beklenen süre | `1 +` ağırlıklı toplam | Bitişte 0 |

## Döngülere dikkat

Her geçiş ileri gitmeyebilir. Bir sonuç aynı duruma döndürüyor veya oyuncuyu geriye taşıyorsa basit doldurma sırası bozulabilir. Örneğin:

$$
E[x] = 1 + 0.4E[x] + 0.6E[x+1]
$$

Burada `E[x]` iki tarafta da bulunur. Cebirsel düzenleme yaparak:

$$
E[x] = \frac{1 + 0.6E[x+1]}{0.6}
$$

sonucunu elde ederiz. Daha karmaşık döngüler doğrusal denklem sistemi, Gauss eliminasyonu veya Markov zinciri yaklaşımı gerektirebilir.

## Yarışma kontrol listesi

1. Durum geleceği belirlemek için yeterli mi?
2. Tüm rastgele sonuçların olasılıkları toplamı 1 mi?
3. Başarı, başarısızlık ve bitiş durumları tanımlı mı?
4. Geçiş grafiği yönlü döngüsüz mü?
5. `double` hassasiyeti yeterli mi, yoksa modüler ters mi gerekiyor?

Probabilistic DP'nin sırrı şansı tahmin etmek değil, şansın oluşturduğu dalları eksiksiz modellemektir. Durum doğru seçildiğinde zarlar, paralar ve rastgele yürüyüşler bile disiplinli bir DP tablosuna dönüşür.

---
layout: post
title: "Bilgisayar Olimpiyatlarında Çözümsüzlük Hissiyle Başa Çıkmak"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - bilgisayar olimpiyatları
  - psikolojik dayanıklılık
  - problem çözme
  - stres yönetimi
  - rekabetçi programlama
toc: true
image: /img/bilgisayar-olimpiyatlarinda-cozumsuzluk-56.png
---

Bilgisayar olimpiyatlarında bazen kod değil, zihin kilitlenir. Soruyu defalarca okur, aynı örneği kâğıtta çevirir ve editörün çoktan çözümü yazdığına dair tuhaf bir hisse kapılırsınız. Ekrana bakarak geçen süre arttıkça “Henüz bulamadım” düşüncesi, “Ben bunu bulamam” yargısına dönüşebilir. Psikolojik dayanıklılık, bu duyguyu yok etmek değil; duygu masadayken bile sistemli düşünebilme becerisidir.

``

## Beyin neden kilitlenir?

Stres belirli bir seviyeye kadar dikkati artırır; aşırı yükseldiğinde ise çalışma belleğini daraltır. Olimpiyat sorularında aynı anda kısıtları, örnekleri, olası algoritmaları ve karmaşıklığı düşünmek gerekir. Çalışma belleği stres tarafından işgal edildiğinde yarışmacı aynı düşünce döngüsünü tekrarlar.

Bunu basit bir modelle gösterebiliriz. Performansı yaklaşık olarak

$$P(s) = -a(s-s_0)^2 + P_{max}$$

şeklinde düşünelim. Burada $s$ stres düzeyi, $s_0$ verimli uyarılma noktasıdır. Amaç stresi sıfırlamak değil, yönetilebilir bölgeye geri çekmektir.

| İç konuşma | Zihinsel etkisi | Daha işlevsel karşılık |
|---|---|---|
| “Hiçbir şey bulamıyorum.” | İlerlemeyi görünmez yapar | “Hangi yaklaşımları eledim?” |
| “Bu soru benim seviyemin üstünde.” | Denemeyi erken bitirir | “Küçük kısıtlarda ne oluyor?” |
| “Zaman kalmadı.” | Acele ve hata üretir | “Önümüzdeki 10 dakikanın hedefi ne?” |
| “Çözüm kesin çok karmaşık.” | Basit yapıları kaçırır | “En kaba doğru çözüm nedir?” |

![bilgisayar-olimpiyatlarinda-cozumsuzluk-56](/img/bilgisayar-olimpiyatlarinda-cozumsuzluk-56.svg)


## Önce fizyolojik döngüyü kırın

Takıldığınızı fark ettiğinizde 60–90 saniyelik kontrollü ara verin. Ekrandan uzaklaşın, omuzları gevşetin ve nefesi verirken daha uzun süre kullanın. Örneğin dört saniye nefes alıp altı saniye vermek, bedene acil tehlike bulunmadığı sinyalini iletebilir.

Ardından kâğıda üç şey yazın:

1. **Kesin bildiklerim:** Kısıtlar, hedef ve doğrulanmış gözlemler.
2. **Varsaydıklarım:** Soruda yazmadığı hâlde doğru kabul ettiklerim.
3. **Bilmediğim:** Çözüm için cevaplanması gereken tek küçük soru.

Bu yöntem “Problemi çözemiyorum” gibi dev bir yargıyı, “Optimal alt yapıyı kanıtlayamıyorum” gibi çalışılabilir bir göreve dönüştürür.

## Problemi yeniden modelleme

Aynı modele daha sert bakmak çoğu zaman işe yaramaz; modeli değiştirmek gerekir. Diziyi grafik, işlemleri durum geçişi veya seçimleri maliyet minimizasyonu olarak yorumlamayı deneyin.

| İlk görünüm | Alternatif model | Sorulacak soru |
|---|---|---|
| Alt dizi problemi | Prefix toplamları | İki prefix arasındaki fark ne anlatıyor? |
| İşlem sırası | Grafik kenarları | En kısa yol veya bağlılık var mı? |
| Seçim problemi | Dinamik programlama | Durumu belirleyen en az bilgi nedir? |
| Büyük sayma problemi | Küçük örnek örüntüsü | Sonuçlarda periyot oluşuyor mu? |

Kısıtları geçici olarak küçültmek de güçlüdür. $n \leq 10$ için brute force yazıp çıktıları incelemek, görünmeyen invariantı ortaya çıkarabilir:

```python
from itertools import permutations

def brute(a):
    best = float("inf")
    for order in permutations(a):
        cost = sum(abs(order[i] - order[i - 1])
                   for i in range(1, len(order)))
        best = min(best, cost)
    return best

for n in range(2, 8):
    a = list(range(n))
    print(n, brute(a))
```

Bu kod büyük girdiyi çözmek için değil, küçük örneklerde hipotez üretmek için kullanılır. Bulduğunuz örüntüyü hemen çözüm sanmayın; önce neden doğru olduğunu kanıtlamaya çalışın.

## Yarışma içinde karar vermek

Her 15–20 dakikada kısa bir kontrol noktası belirleyin: Yeni gözlem var mı, karmaşıklık hedefi belli mi, yoksa aynı fikri mi tekrarlıyorum? İlerleme yoksa soruyu bırakmak yenilgi değildir. Başka sorudan alınan puan ve özgüven, geri döndüğünüzde bilişsel esneklik sağlayabilir.

Son olarak sonucu kimliğinizden ayırın. Bir problemi çözememek, problem çözemeyen biri olduğunuz anlamına gelmez. Olimpiyat başarısı yalnızca hızlı fikir bulma değil; belirsizlik altında sakin kalma, yanlış modeli bırakma ve yeniden deneme sanatıdır.

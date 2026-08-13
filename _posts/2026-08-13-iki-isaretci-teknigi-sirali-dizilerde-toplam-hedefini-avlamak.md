---
layout: post
title: "İki İşaretçi Tekniği: Sıralı Dizilerde Toplam Hedefini Avlamak"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - two pointers
  - olimpiyat programlama
---

İki İşaretçi (Two Pointers), özellikle sıralı dizilerde “hangi iki elemanın toplamı hedefe eşit?” sorusunu doğrusal zamanda çözmeye yarayan klasik bir olimpiyat programlama tekniğidir. İlk bakışta tüm ikilileri denemek doğal görünür; ancak bu yaklaşım dizinin büyüklüğü arttıkça pahalılaşır. İki uçtan yürüyen işaretçiler, sıralama bilgisini bir pusula gibi kullanır: toplam küçükse büyütmek, büyükse küçültmek için hangi yönde ilerleyeceğini bilir.
``

Elimizde artan sırada bir $a$ dizisi ve hedef $T$ olsun. Sol işaretçi $l=0$, sağ işaretçi ise $r=n-1$ konumunda başlar. Her adımda $s=a[l]+a[r]$ hesaplanır. Eğer $s=T$ ise cevap bulunmuştur. Eğer $s<T$ ise soldaki değer daha büyük bir değerle değiştirilmelidir; dolayısıyla $l$ artırılır. Eğer $s>T$ ise sağdaki değer küçültülmelidir; bu nedenle $r$ azaltılır.

Bu kararların sihri, **sıralılık değişmezinde** saklıdır. Örneğin $a[l]+a[r]<T$ iken $r$ değerini azaltmak anlamsızdır: Sağdaki elemanı daha da küçültmek toplamı hedefe yaklaştırmaz. Dahası, mevcut $a[l]$ ile $r$ ve onun solundaki hiçbir eleman hedefi oluşturamaz. Bu yüzden $l$ güvenle ilerletilir. Benzer biçimde toplam fazla olduğunda, mevcut $a[r]$ ile $l$ ve onun sağındaki hiçbir eleman çözüm olamaz.

| Yaklaşım | Temel fikir | Zaman karmaşıklığı | Ek bellek |
|---|---|---:|---:|
| Kaba kuvvet | Her eleman çiftini dene | $O(n^2)$ | $O(1)$ |
| Hash tablosu | Görülen tamamlayıcıyı sakla | $O(n)$ beklenen | $O(n)$ |
| İki işaretçi | Sıralı dizinin uçlarını daralt | $O(n)$ | $O(1)$ |

Önemli ayrım şudur: Hash tablosu, dizi sıralı olmasa da çalışır; iki işaretçi ise sıralama ister. Dizi başlangıçta sıralı değilse önce sıralamak gerekir. Bu durumda toplam maliyet $O(n\log n)$ olur. Ayrıca yalnızca toplamı değil, elemanların **orijinal indekslerini** istiyorsanız değerlerle indeksleri birlikte sıralamalısınız.

Aşağıdaki C++ örneği, hedef toplamı veren bir çifti bulur. Kod, sıralı dizide ilk bulduğu çifti döndürür; bulunamazsa `nullopt` üretir.

```cpp
#include <iostream>
#include <optional>
#include <utility>
#include <vector>

std::optional<std::pair<int, int>> twoSumSorted(
    const std::vector<int>& a, int target) {
    int l = 0;
    int r = static_cast<int>(a.size()) - 1;

    while (l < r) {
        long long sum = 1LL * a[l] + a[r];

        if (sum == target) return {{l, r}};
        if (sum < target) ++l;
        else --r;
    }
    return std::nullopt;
}
```

`long long` kullanımı küçük ama profesyonel bir ayrıntıdır: `int` sınırına yakın değerlerin toplamında taşmayı önler. Döngünün koşulu olan $l<r$ da aynı elemanı iki kez seçmeyi engeller. Her iterasyonda en az bir işaretçi hareket ettiğinden, işaretçilerin toplam hareketi en fazla yaklaşık $2n$ olur. Bu nedenle çalışma süresi gerçekten doğrusaldır:

$$T(n) \leq 2n + O(1) = O(n)$$

Teknik, yalnızca “iki sayı toplamı” için değildir. Üçlü toplam problemlerinde bir elemanı sabitleyip kalan bölümde iki işaretçi kullanılır; böylece maliyet $O(n^3)$ yerine $O(n^2)$ olur. Ayrıca sıralı dizide hedefe en yakın toplamı bulma, yinelenen değerleri atlama ve iki dizinin kesişimini çıkarma gibi görevlerde de aynı mantık çalışır.

| Problem türü | İşaretçilerin davranışı | Tipik maliyet |
|---|---|---:|
| Hedefe eşit çift toplamı | Toplama göre sol/sağ kaydır | $O(n)$ |
| Hedefe en yakın çift | En iyi farkı tut, sonra kaydır | $O(n)$ |
| Üçlü toplam | Bir elemanı sabitle, iki uçta ara | $O(n^2)$ |

Sonuç olarak iki işaretçi, “deneme sayısını azaltma” sanatıdır. Sıralı yapı size hangi adayların imkânsız olduğunu kanıtlama gücü verir; algoritma da bu adayları tek tek kontrol etmek yerine bir hamlede eler. Olimpiyat sorularında aranan hız tam olarak budur.

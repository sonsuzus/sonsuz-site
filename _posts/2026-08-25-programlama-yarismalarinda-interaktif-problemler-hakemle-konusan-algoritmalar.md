---
layout: post
title: "Programlama Yarışmalarında İnteraktif Problemler: Hakemle Konuşan Algoritmalar"
math: true
categories: 
  - Bilgi
tags: 
  - programlama yarışmaları
  - interaktif problemler
  - algoritmalar
  - c++
---

Programlama yarışmalarındaki klasik sorularda girdiyi bir kez okur, cevabı yazıp programı kapatırsınız. İnteraktif problemlerde ise karşınızda görünmez bir hakem vardır: Siz soru sorarsınız, hakem cevap verir, siz yeni bilgiye göre stratejinizi güncellersiniz. Bu yapı; ikili arama, bilgi teorisi, durum yönetimi ve iletişim protokolü gibi kavramları aynı sahnede buluşturur.
``

İnteraktif problem çözmenin temel modeli bir **soru-cevap protokolüdür**. Hakem gizli bir sayı, permütasyon, grafik ya da karakter dizisi tutabilir. Programınız belirlenmiş biçimde sorgular gönderir; gelen yanıtlardan gizli yapıyı bulmaya çalışır. Ancak sorgu sayısı sınırlıdır. Bu nedenle amaç yalnızca doğru cevabı bulmak değil, bunu yeterince az soruyla yapmaktır.

En tanıdık örnek, $[1,n]$ aralığında saklanan bir sayıyı bulmaktır. Her sorguda "Gizli sayı $x$'ten küçük mü?" diye sorduğunuzu düşünün. Aralığı her adımda ikiye bölerek belirsizliği azaltırsınız. Başlangıçta $n$ olası değer varken, $q$ adet evet/hayır sorusundan sonra ayırt edilebilecek en fazla durum sayısı $2^q$ olur. Dolayısıyla teorik alt sınır şöyledir:

$$q \geq \lceil \log_2 n \rceil$$

Bu, ikili aramanın neden yalnızca pratikte hızlı değil, çoğu durumda bilgi açısından da optimal olduğunu açıklar.

| Yaklaşım | Sorgu sayısı | Fikir | Ne zaman kullanılır? |
|---|---:|---|---|
| Doğrusal arama | $O(n)$ | Her olasılığı tek tek denemek | Çok küçük sınırlar |
| İkili arama | $O(\log n)$ | Aralığı iki parçaya ayırmak | Sıralı/monoton cevaplar |
| Böl ve yönet | Probleme bağlı | Birden fazla bilgiyi tek sorguda toplamak | Permütasyon ve grafik problemleri |
| Rastgeleleştirme | Beklenen değer | Örnekleme ile aday elemek | Deterministik strateji zor olduğunda |

İnteraktif problemlerde algoritma kadar **I/O disiplini** de önemlidir. Normal bir soruda çıktının en sonda tamponda beklemesi sorun olmayabilir. Burada ise hakem sizden sorguyu görmeden yanıt veremez; siz de yanıt gelmeden ilerleyemezsiniz. Bu karşılıklı bekleme durumuna deadlock denir. Çözüm, her sorgudan sonra çıktıyı flush etmektir.

Aşağıdaki C++ iskeleti, gizli sayıyı karşılaştırma sorgularıyla bulan bir programın iletişim yapısını gösterir. Gerçek yarışmalarda `?` ve `!` sembolleri ile yanıt biçimi problem metninde kesin olarak belirtilir.

```cpp
#include <iostream>
using namespace std;

int main() {
    int low = 1, high;
    cin >> high; // Bazı problemlerde n başlangıçta verilir.

    while (low < high) {
        int mid = low + (high - low) / 2;
        cout << "? " << mid << endl; // endl flush işlemi yapar.

        string response;
        cin >> response;

        if (response == "YES") {
            high = mid;
        } else {
            low = mid + 1;
        }
    }

    cout << "! " << low << endl;
    return 0;
}
```

Buradaki `endl`, satır sonu eklemenin yanında akışı temizlediği için kritiktir. `"\n"` kullanmak isterseniz ayrıca `cout.flush()` çağırmalısınız. Ayrıca hakemden `-1` gibi hata yanıtı gelmesi ihtimalini problem metninden kontrol edin; böyle bir durumda program hemen sonlanmalıdır.

| Yaygın hata | Belirti | Çözüm |
|---|---|---|
| Flush unutmak | Program yanıt beklerken takılır | `endl` veya `cout.flush()` kullanın |
| Yanlış sorgu biçimi | Anında Wrong Answer | Boşlukları, sembolleri ve büyük-küçük harfi doğrulayın |
| Sorgu limitini aşmak | Başarılı mantığa rağmen WA | Her turdaki sorguları sayın |
| Eski yanıta göre karar vermek | Tutarsız aralıklar | Her cevaptan sonra durumu güncelleyin |

Test etmek için çoğu yarışma platformunun sağladığı yerel interactor aracını kullanın. Yoksa küçük bir hakem simülatörü yazın: gizli değeri üretir, sorguları okur ve protokole uygun yanıt döndürür. Özellikle sınır durumlarını deneyin: $x=1$, $x=n$, tek elemanlı aralıklar ve maksimum sorgu sayısı. İnteraktif problemler, algoritmanızın sadece "ne hesapladığını" değil, "bilgiyi nasıl edindiğini" ölçer; bu yüzden her sorguyu değerli bir deney olarak tasarlayın.

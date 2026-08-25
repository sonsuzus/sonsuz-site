---
layout: post
title: "Vector Clock Mekanizması: Dağıtık Sistemlerde Olayların Zamanını Anlamak"
math: true
categories: 
  - Bilgi
tags: 
  - dağıtık sistemler
  - vector clock
  - eşzamanlılık
---

Dağıtık sistemlerde tek bir duvar saati, olayların gerçek sırasını güvenilir biçimde anlatamaz. Sunucuların saatleri kayabilir, ağ paketleri gecikebilir ve iki işlem fiziksel olarak farklı makinelerde aynı anda gerçekleşebilir. Vector Clock, “hangi olay hangisinden sonra oldu?” sorusuna odaklanan mantıksal zamanlama tekniğidir. Özellikle replikasyon, çatışma çözümü ve nedensellik analizi için çok değerlidir.
``
Bir vector clock, sistemdeki her süreç için bir sayaç tutan vektördür. Üç düğümlü bir sistem düşünelim: A, B ve C. A düğümünün saati `[2, 0, 1]` ise ilk değer A’nın bildiği A olaylarını, ikinci değer B olaylarını, üçüncü değer ise C olaylarını temsil eder. Bir düğüm yerel bir olay gerçekleştirdiğinde kendi indeksini artırır. Mesaj gönderirken mevcut vektörü mesaja ekler; mesaj alan düğüm ise iki vektörün her bileşenindeki büyük değeri seçer ve ardından kendi sayacını bir artırır.

Bu yaklaşımın teorik temelinde **happened-before** (önce-gerçekleşti) ilişkisi bulunur. Lamport’un tanımladığı bu ilişki, iki olay arasındaki nedensel bağı ifade eder. Bir mesajın gönderilmesi, alınmasından önce gelir. Aynı süreçte daha önce çalışan kod da sonraki koddan önce gelir. Vector clock’lar bu ilişkiyi şu karşılaştırma ile hesaplar:

$$V \prec W \iff (\forall i, V_i \leq W_i) \land (\exists j, V_j < W_j)$$

Yani `V` vektörünün tüm bileşenleri `W`’den küçük veya eşitse ve en az bir bileşeni gerçekten küçükse, `V` olayı `W` olayından önce gerçekleşmiştir. Ne `V \prec W` ne de `W \prec V` doğruysa olaylar **eşzamanlıdır**; aralarında kanıtlanabilir bir nedensellik yoktur.

| Saat türü | Tutulan bilgi | Eşzamanlı olayları ayırır mı? | Maliyet |
|---|---|---:|---:|
| Fiziksel saat | Gerçek zamana yakın zaman damgası | Hayır | Düşük |
| Lamport Clock | Tek sayı ile mantıksal sıra | Hayır | Düşük |
| Vector Clock | Her süreç için sayaç | Evet | Süreç sayısıyla artar |

Aşağıdaki Python örneği, iki vector clock’u karşılaştırarak nedensel ilişkiyi bulur. Kodda `before`, olayların kesin sırasını; `concurrent` ise birbirinden bağımsız gelişmiş olabilecek olayları belirtir.

```python
def compare(left, right):
    less_or_equal = all(a <= b for a, b in zip(left, right))
    greater_or_equal = all(a >= b for a, b in zip(left, right))

    if left == right:
        return "aynı mantıksal zaman"
    if less_or_equal:
        return "left before right"
    if greater_or_equal:
        return "right before left"
    return "concurrent"

print(compare([2, 1, 0], [2, 3, 1]))
print(compare([3, 0, 1], [2, 2, 1]))
```

İlk çağrıda ilk vektör ikinciden önce gelir: B ve C tarafındaki bilgi ikinci vektörde daha günceldir. İkinci çağrıda ise bir vektör A’da ilerideyken diğeri B’de ileridedir. Bu nedenle tek bir “kazanan zaman” seçmek teorik olarak doğru değildir; olaylar eşzamanlı kabul edilir.

Mesaj alma kuralını küçük bir formülle özetleyebiliriz. Alıcı `R`, göndericiden `M` vektörünü aldığında önce bileşen bazında birleşim alır, sonra kendi sayacını ilerletir:

$$R_i \leftarrow \max(R_i, M_i), \quad R_{self} \leftarrow R_{self} + 1$$

Bu mekanizma, örneğin iki kullanıcı çevrimdışıyken aynı belgeyi düzenlediğinde çok kullanışlıdır. Her düzenleme kendi vector clock’u ile saklanır. Saatler karşılaştırılır; biri diğerini takip ediyorsa yeni sürüm seçilir. Saatler eşzamanlıysa sistem bunun bir çatışma olduğunu anlar ve birleştirme, kullanıcıya seçim sunma ya da CRDT stratejisi uygulama şansı doğar.

Vector clock’ların bedeli, vektör boyutunun katılımcı sayısıyla büyümesidir: $O(n)$. Bu yüzden çok büyük ve dinamik sistemlerde version vector, dotted version vector veya hibrit mantıksal saatler gibi alternatifler tercih edilebilir. Yine de nedenselliği açık, matematiksel ve denetlenebilir biçimde modellemek istediğinizde vector clock, dağıtık sistemler dünyasının en öğretici araçlarından biridir.

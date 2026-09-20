---
layout: post
title: "Floyd’un Çevrim Bulma Algoritması: Kaplumbağa ve Tavşanla Döngü Avı"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - floyd
  - çevrim
  - bağlı-liste
  - dizi
  - c++
toc: true
image: /img/floydun-cevrim-bulma-73.png
---

Bir veri yapısında ilerlerken aynı noktaya tekrar uğruyorsanız, muhtemelen bir çevrimin içine düşmüşsünüzdür. Ziyaret edilen elemanları bir kümede saklamak işe yarar; ancak ek bellek tüketir. Floyd’un çevrim bulma algoritması ise yalnızca iki işaretçi kullanarak döngüyü yakalar. Üstelik bunu hem bağlı listelerde hem de her elemanın bir sonraki konumu gösterdiği dizilerde yapabilir.
``

## Temel fikir: Kaplumbağa ve tavşan

Algoritmada aynı başlangıç noktasından hareket eden iki gezgin bulunur:

- **Yavaş işaretçi**, her turda bir adım ilerler.
- **Hızlı işaretçi**, her turda iki adım ilerler.

Bir çevrim yoksa hızlı işaretçi yapının sonuna ulaşır. Çevrim varsa hızlı işaretçi, dairesel pistte yavaş işaretçiyi mutlaka yakalar. Bu nedenle yöntem genellikle “kaplumbağa ve tavşan algoritması” olarak anılır.

Çevrime kadar olan mesafeyi $\mu$, çevrimin uzunluğunu $\lambda$ ile gösterelim. İşaretçiler buluştuğunda hızlı işaretçinin aldığı yol, yavaş işaretçinin yolunun iki katıdır:

$$2d - d = d = k\lambda$$

Aradaki yol farkı çevrim uzunluğunun tam katı olduğundan iki işaretçi aynı düğüme gelir. Algoritmanın zaman karmaşıklığı $O(\mu + \lambda)$, ek alan karmaşıklığı ise $O(1)$ olur.

| Yaklaşım | Zaman | Ek bellek | Çevrim başlangıcı |
|---|---:|---:|---|
| Ziyaret kümesi | $O(n)$ | $O(n)$ | Kolayca bulunur |
| Floyd algoritması | $O(n)$ | $O(1)$ | İkinci aşamayla bulunur |
| Adım sınırı koyma | Belirsiz | $O(1)$ | Güvenilir değildir |

## Bağlı listede çevrimi yakalamak

Aşağıdaki C++ fonksiyonu önce işaretçileri buluşturur. Ardından bir işaretçiyi listenin başına taşır ve ikisini de birer adım ilerletir. Yeniden buluştukları düğüm, çevrimin girişidir.

```cpp
struct Node {
    int value;
    Node* next;
};

Node* findCycleStart(Node* head) {
    Node* slow = head;
    Node* fast = head;

    do {
        if (fast == nullptr || fast->next == nullptr)
            return nullptr; // Liste sonlandı, çevrim yok.

        slow = slow->next;
        fast = fast->next->next;
    } while (slow != fast);

    slow = head;
    while (slow != fast) {
        slow = slow->next;
        fast = fast->next;
    }

    return slow;
}
```

İkinci aşamanın çalışmasının nedeni, ilk buluşma noktasından çevrim girişine kalan uzaklığın $\mu$ ile modüler olarak aynı olmasıdır. Başlangıçtan gelen işaretçi ile çevrimde bekleyen işaretçi eşit hızla yürüdüğünde girişte karşılaşırlar.

## Dizilerde çevrim nasıl oluşur?

Bir dizinin değerleri bir sonraki indeks olarak yorumlanıyorsa yapı, **fonksiyonel grafik** hâline gelir. Örneğin `next[i]`, `i` konumundan sonra gidilecek indeksi belirlesin:

```cpp
int findMeetingPoint(const vector<int>& next, int start) {
    int slow = start;
    int fast = start;

    do {
        slow = next[slow];
        fast = next[next[fast]];
    } while (slow != fast);

    return slow;
}
```

Örneğin `next = {1, 3, 0, 4, 2}` ve başlangıç `0` olduğunda rota `0 → 1 → 3 → 4 → 2 → 0` biçimindedir. Bütün indeksler çevrimin parçasıdır. Eğer dizi geçersiz indeksi bir bitiş işareti olarak kullanıyorsa, erişimden önce sınır kontrolü yapılmalıdır; aksi hâlde döngü avlarken tanımsız davranış canavarıyla karşılaşabilirsiniz.

## Çevrim uzunluğunu bulmak

Bir buluşma noktası elde edildikten sonra aynı noktaya dönene kadar tek işaretçi ilerletilir:

```cpp
int cycleLength(const vector<int>& next, int meeting) {
    int length = 1;
    int current = next[meeting];

    while (current != meeting) {
        current = next[current];
        ++length;
    }
    return length;
}
```

Floyd’un yöntemi; bağlı listelerde hata ayıklama, yinelenen durumları tespit etme, durum makinelerini inceleme ve sayı dizilerindeki periyotları bulma gibi alanlarda kullanılır. Kısacası veri sürekli “sonraki” konuma gidiyorsa ve hafızayı şişirmeden döngü arıyorsanız, kaplumbağa ile tavşanı yarışa sokmanın tam zamanıdır.

![floydun-cevrim-bulma-73](/img/floydun-cevrim-bulma-73.svg)


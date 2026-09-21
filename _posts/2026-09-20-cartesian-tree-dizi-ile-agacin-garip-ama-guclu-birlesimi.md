---
layout: post
title: "Cartesian Tree: Dizi ile Ağacın Garip Ama Güçlü Birleşimi"
math: true
categories: 
  - Bilgi
tags: 
  - cartesian-tree
  - veri-yapıları
  - algoritma
  - ağaçlar
  - monotonik-yığın
  - cpp
toc: true
image: /img/cartesian-tree-dizi-13.png
---

![cartesian-tree-dizi-13](/img/cartesian-tree-dizi-13.svg)


Bir dizi düşünün: elemanların hem soldan sağa sırasını korumak hem de onları önceliklerine göre bir ağaca yerleştirmek istiyoruz. İlk bakışta “Ağaç mı yapıyoruz, diziyi mi saklıyoruz?” diye sorabilirsiniz. Cartesian Tree tam olarak bu iki dünyayı birleştirir: dizinin sırasını bozmadan heap özelliği taşıyan bir ikili ağaç üretir. Üstelik bunu doğrusal zamanda yapmak mümkündür.

``

## Cartesian Tree nedir?

Bir $A[0\dots n-1]$ dizisinin **min-Cartesian Tree** yapısı iki temel koşulu sağlar:

1. Ağacın inorder dolaşımı dizinin elemanlarını orijinal sırada verir.
2. Her düğümün değeri çocuklarının değerinden küçüktür veya onlara eşittir.

Başka bir ifadeyle kök, dizinin minimum elemanıdır. Minimumun solundaki alt dizi sol alt ağacı, sağındaki alt dizi ise sağ alt ağacı oluşturur.

Örneğin $A=[3,2,6,1,9]$ için minimum değer $1$ olduğundan kök odur. Sol taraftaki $[3,2,6]$ kendi Cartesian Tree’sini, sağdaki $[9]$ ise sağ alt ağacı oluşturur.

| Özellik | Dizi | Min-Heap | Cartesian Tree |
|---|---|---|---|
| Eleman sırası korunur | Evet | Hayır | Inorder’da evet |
| Minimum kökte bulunur | Hayır | Evet | Evet |
| İkili ağaçtır | Hayır | Genellikle | Evet |
| Doğrudan indeks ilişkisi taşır | Evet | Kısmen | Evet |

Elemanlar farklıysa bu iki koşulu sağlayan ağaç tektir. Tekrarlı değerlerde ise eşitliklerin nasıl ele alınacağı belirlenmelidir. Örneğin soldaki eşit elemana öncelik verilmesi tutarlı bir kuraldır.

## Saf yaklaşım ve maliyeti

En doğal yöntem, her alt dizide minimumu bulup ağacı özyinelemeli kurmaktır. Bir aralıktaki minimumu doğrusal taramayla bulursak sıralı bir dizi gibi kötü durumda şu maliyet ortaya çıkar:

$$T(n)=T(n-1)+O(n)=O(n^2)$$

Dengeli bölünmelerde sonuç daha iyi olsa da algoritma garantili biçimde hızlı değildir. Asıl sihir, **monotonik yığın** kullanıldığında başlar.

## Monotonik yığınla doğrusal kurulum

Diziyi soldan sağa gezerken değerleri artan sırada tutan bir yığın kullanırız. Yeni elemandan büyük düğümleri yığından çıkarırız. Son çıkarılan düğüm, yeni düğümün sol çocuğu olur. Yığında kalan tepe varsa yeni düğüm onun sağ çocuğuna bağlanır.

```cpp
#include <iostream>
#include <stack>
#include <vector>
using namespace std;

struct Node {
    int value;
    Node *left = nullptr, *right = nullptr;
    explicit Node(int value) : value(value) {}
};

Node* buildCartesianTree(const vector<int>& a) {
    stack<Node*> st;

    for (int value : a) {
        Node* current = new Node(value);
        Node* lastRemoved = nullptr;

        while (!st.empty() && st.top()->value > value) {
            lastRemoved = st.top();
            st.pop();
        }

        current->left = lastRemoved;

        if (!st.empty()) {
            st.top()->right = current;
        }

        st.push(current);
    }

    while (st.size() > 1) st.pop();
    return st.top();
}
```

Her düğüm yığına yalnızca bir kez girer ve en fazla bir kez çıkar. Bu nedenle toplam karmaşıklık

$$O(n)$$

olur. Ağacın düğümleri ayrıca saklandığı için bellek maliyeti de $O(n)$’dir. `>` yerine `>=` kullanmak, eşit değerlerde hangi düğümün üstte kalacağını değiştirir; yani seçilen karşılaştırma kuralı ağacın tutarlılığı açısından önemlidir.

## Neden kullanışlı?

Cartesian Tree’nin en ünlü kullanım alanlarından biri **Range Minimum Query**, yani belirli bir aralıktaki minimum değeri bulma problemidir. Dizideki iki indeksin Cartesian Tree üzerindeki en düşük ortak atası, bu indeksler arasındaki minimum elemanı temsil eder. Böylece RMQ problemi, LCA problemine dönüştürülebilir.

Ayrıca en büyük dikdörtgen alanı, dizi bölme problemleri, treap mantığı ve bazı string algoritmalarında benzer fikirlerle karşılaşılır. Cartesian Tree biraz tuhaf görünür: yarısı dizi, yarısı heap, tamamı ağaçtır. Fakat sıra bilgisini ve öncelik ilişkisini aynı yapıda koruduğu için algoritma çantanızdaki şaşırtıcı derecede güçlü araçlardan biridir.

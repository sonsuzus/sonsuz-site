---
layout: post
title: "C++ STL’de Iterator Geçersizliği: erase Tuzağından Güvenle Kaçış"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - stl
  - iterator
  - konteynerler
  - erase
  - bellek
toc: true
image: /img/c-stlde-iterator-54.png
---

Bir STL konteynerinde dolaşırken eleman silmek, ilk bakışta son derece masum görünür. Ancak yanlış kullanılan tek bir `erase`, yineleyiciyi geçersiz hâle getirerek tanımsız davranışa, atlanan elemanlara veya yalnızca cuma akşamları ortaya çıkan gizemli çökmelere neden olabilir. Bu tuzağın kaynağı, her konteynerin elemanlarını bellekte farklı biçimde saklamasıdır.

``

## Iterator neden geçersiz olur?

Iterator, çoğu zaman bir elemana ulaşmayı sağlayan adres benzeri bir nesnedir. Bir eleman silindiğinde konteyner, belleğini yeniden düzenleyebilir. Iterator artık yaşayan bir elemana işaret etmiyorsa onu karşılaştırmak, artırmak veya dereference etmek güvenli değildir.

Örneğin `vector`, elemanlarını ardışık bellekte tutar. İndisi $i$ olan eleman silindiğinde arkasındaki yaklaşık

$$n-i-1$$

eleman sola taşınır. Böylece silinen elemanı ve sonrasını gösteren iterator’lar geçersizleşir. İşlemin zaman karmaşıklığı da bu taşıma nedeniyle genel olarak $O(n)$ olur.

```cpp
std::vector<int> sayilar{1, 2, 3, 4, 5};
auto it = sayilar.begin() + 2; // 3

sayilar.erase(it);
// it artık geçersizdir!
// std::cout << *it; // Tanımsız davranış
```

Buradaki yaygın yanılgı, `it` değişkeninin otomatik olarak sıradaki elemana geçeceğini düşünmektir. Oysa `erase`, eski iterator’ı onarmaz; bunun yerine geçerli olan sonraki iterator’ı döndürür.

## Güvenli silme deseni

Dolaşma sırasında silme yapılacaksa `erase` dönüş değeri kullanılmalıdır:

```cpp
std::vector<int> sayilar{1, 2, 3, 4, 5, 6};

for (auto it = sayilar.begin(); it != sayilar.end(); ) {
    if (*it % 2 == 0) {
        it = sayilar.erase(it); // Sonraki geçerli konumu al
    } else {
        ++it;                   // Yalnızca silinmediyse ilerle
    }
}
```

Döngünün üçüncü bölümü özellikle boş bırakılmıştır. Hem `erase` sonrasında hem de döngü sonunda `++it` çalıştırılsaydı bir eleman atlanabilirdi.

## Konteynerlere göre kurallar

| Konteyner | Silme sonrası genel iterator durumu | Silme maliyeti |
|---|---|---:|
| `vector` | Silinen ve sonrasındaki iterator’lar geçersiz | $O(n)$ |
| `deque` | Ortadan silmede çoğunlukla tüm iterator’lar geçersiz | $O(n)$ |
| `list`, `forward_list` | Yalnızca silinen elemana ait iterator geçersiz | $O(1)$ |
| `map`, `set` | Yalnızca silinen elemana ait iterator geçersiz | $O(\log n)$ |
| `unordered_map`, `unordered_set` | Genellikle yalnızca silinen elemana ait iterator geçersiz | Ortalama $O(1)$ |

![c-stlde-iterator-54](/img/c-stlde-iterator-54.svg)


`list` düğüm tabanlı olduğu için bir düğümün çıkarılması diğer düğümlerin adreslerini değiştirmez. `map` ve `set` gibi ağaç tabanlı yapılarda da benzer bir güvence vardır. Buna rağmen silinen iterator’ın kendisini kullanmak her durumda hatadır.

`deque` daha dikkatli ele alınmalıdır: Baştan veya sondan silmenin kuralları daha sınırlı etkiler doğurabilirken ortadan silme, iterator’ları geniş ölçüde geçersizleştirir. Kodun taşınabilir ve anlaşılır olması için daima `erase` dönüş değerini kullanmak en güvenli yaklaşımdır.

## Modern C++ ile erase_if

Amaç yalnızca koşula uyan elemanları temizlemekse C++20, iterator yönetimini gizleyen daha okunaklı bir araç sunar:

```cpp
#include <algorithm>
#include <vector>

std::vector<int> sayilar{1, 2, 3, 4, 5, 6};

std::erase_if(sayilar, [](int deger) {
    return deger % 2 == 0;
});
```

Eski standartlarda `vector` için erase-remove deyimi kullanılır:

```cpp
sayilar.erase(
    std::remove_if(sayilar.begin(), sayilar.end(),
                   [](int x) { return x % 2 == 0; }),
    sayilar.end()
);
```

`remove_if` fiziksel silme yapmaz; korunacak elemanları öne taşır ve mantıksal yeni sonu döndürür. Asıl küçültmeyi `erase` gerçekleştirir.

Kısa kural şudur: Bir silme işleminden sonra eski iterator’ın hâlâ geçerli olduğunu varsayma. Konteynerin geçersizleştirme kurallarını kontrol et, mümkünse `erase` tarafından döndürülen iterator’ı kullan ve toplu koşullu silmelerde `std::erase_if` tercih et. Böylece iterator’ların hayaletlere dönüşmesini engellersin.

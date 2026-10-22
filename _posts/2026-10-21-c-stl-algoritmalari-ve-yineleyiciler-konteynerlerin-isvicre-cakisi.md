---
layout: post
title: "C++ STL Algoritmaları ve Yineleyiciler: Konteynerlerin İsviçre Çakısı"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - stl
  - algoritmalar
  - yineleyiciler
  - konteynerler
  - programlama
toc: true
image: /img/c-stl-algoritmalari-38.png
---

![c-stl-algoritmalari-38](/img/c-stl-algoritmalari-38.svg)


C++ Standart Şablon Kütüphanesi (STL), verileri saklayan konteynerlerle bu veriler üzerinde işlem yapan algoritmaları birbirinden ayırır. Bu iki dünyayı birbirine bağlayan kahramanlar ise yineleyicilerdir. Böylece aynı arama, kopyalama veya sıralama algoritması farklı veri yapılarıyla çalışabilir; her konteyner için yeniden tekerlek icat etmemiz gerekmez.
``
## STL’nin üçlü ittifakı

STL kullanırken genellikle üç temel bileşen birlikte hareket eder:

| Bileşen | Görevi | Örnekler |
|---|---|---|
| Konteyner | Veriyi saklar | `vector`, `list`, `set` |
| Yineleyici | Elemanlara erişim sağlar | `begin()`, `end()` |
| Algoritma | Veriyi işler | `find`, `copy`, `sort` |

Bir yineleyiciyi, konteyner içindeki bir elemanı gösteren akıllı bir işaretçi gibi düşünebiliriz. `begin()` ilk elemanı, `end()` ise son elemandan **bir sonraki** hayali konumu gösterir. STL algoritmaları çoğunlukla yarı açık $[ilk, son)$ aralığını kullanır. Bu gösterimde `ilk` işleme dâhil, `son` ise hariçtir.

Aralıktaki eleman sayısı matematiksel olarak rastgele erişimli yineleyicilerde şöyle ifade edilir:

$$n = son - ilk$$

Bu yaklaşım boş aralıkları göstermeyi ve aralıkları parçalara ayırmayı kolaylaştırır.

## Yineleyici türleri neden önemli?

Her yineleyici aynı yeteneklere sahip değildir. Algoritmanın kullanabileceği işlemler, aldığı yineleyicinin kategorisine bağlıdır.

| Tür | Hareket kabiliyeti | Kullanıldığı yer |
|---|---|---|
| Girdi yineleyicisi | İleri, yalnızca okuma | Veri okuma |
| Çıktı yineleyicisi | İleri, yalnızca yazma | Sonuç üretme |
| İleri yineleyici | İleri, tekrar dolaşılabilir | `forward_list` |
| Çift yönlü yineleyici | İleri ve geri | `list`, `set` |
| Rastgele erişimli yineleyici | Atlama ve çıkarma | `vector`, `deque` |

Örneğin `std::sort`, elemanlara hızlı biçimde atlayabilmek için rastgele erişimli yineleyici ister. Bu nedenle `vector` sıralanabilirken `list` için `std::sort` kullanılamaz; onun yerine `list::sort()` çağrılır.

## Arama: `std::find`

`std::find`, belirtilen aralıkta bir değeri doğrusal olarak arar. En kötü durumda bütün elemanları kontrol ettiği için zaman karmaşıklığı $O(n)$ olur.

```cpp
#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> puanlar{70, 85, 90, 65, 100};

    auto sonuc = std::find(puanlar.begin(), puanlar.end(), 90);

    if (sonuc != puanlar.end()) {
        std::cout << "Bulundu, indeks: "
                  << std::distance(puanlar.begin(), sonuc) << '\n';
    }
}
```

Algoritma başarısız olduğunda `end()` döndürür. Bu yüzden bulunan yineleyiciyi kullanmadan önce sonuç mutlaka kontrol edilmelidir. Koşula göre arama yapmak için `std::find_if` ve lambda ifadesi kullanılabilir.

```cpp
auto ilkCift = std::find_if(puanlar.begin(), puanlar.end(),
                           [](int sayi) { return sayi % 2 == 0; });
```

## Kopyalama: `std::copy`

`std::copy`, kaynak aralıktaki elemanları hedef konuma aktarır. Hedef konteynerde yeterli alan bulunması gerekir. Boyutu önceden bilinmiyorsa `std::back_inserter`, elemanları güvenli biçimde sona ekler.

```cpp
#include <algorithm>
#include <iterator>
#include <vector>

std::vector<int> kaynak{1, 2, 3, 4};
std::vector<int> hedef;

std::copy(kaynak.begin(), kaynak.end(),
          std::back_inserter(hedef));
```

Burada `back_inserter`, her atamayı `push_back` çağrısına dönüştüren bir çıktı yineleyicisidir. Kopyalanan eleman sayısı $n$ ise işlem karmaşıklığı $O(n)$ düzeyindedir.

## Sıralama: `std::sort`

`std::sort`, varsayılan olarak elemanları küçükten büyüğe dizer ve ortalama $O(n\log n)$ karmaşıklığa sahiptir.

```cpp
std::sort(puanlar.begin(), puanlar.end(), std::greater<int>());
```

Bu çağrı puanları büyükten küçüğe sıralar. Özel nesnelerde lambda kullanarak sıralama ölçütünü açıkça tanımlayabiliriz:

```cpp
std::sort(ogrenciler.begin(), ogrenciler.end(),
          [](const auto& a, const auto& b) {
              return a.puan > b.puan;
          });
```

STL’nin asıl gücü, algoritmaların belirli konteynerlere değil yineleyici aralıklarına göre tasarlanmasıdır. Aralık mantığını, yineleyici kategorilerini ve karmaşıklıkları kavradığınızda daha kısa, güvenli ve yeniden kullanılabilir C++ kodları yazabilirsiniz. Kısacası konteyner veriyi taşır, algoritma işi yapar, yineleyici de ikisini tanıştırır.

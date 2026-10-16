---
layout: post
title: "C++ STL Konteynerleri: vector, list ve map ile Veriyi Ustaca Yönetmek"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - stl
  - vector
  - list
  - map
  - veri yapıları
  - algoritmalar
toc: true
image: /img/c-stl-konteynerleri-48.png
---

![c-stl-konteynerleri-48](/img/c-stl-konteynerleri-48.svg)


C++ ile veri işlerken her elemanı elle yönetmek, bellek ayırmak ve bağlantıları takip etmek oldukça yorucu olabilir. Neyse ki Standart Şablon Kütüphanesi (STL), bu işleri güvenli ve düzenli biçimde yapan konteynerler sunar. Bu yazıda `vector`, `list` ve `map` yapılarını inceleyerek hangi durumda hangisinin seçilmesi gerektiğini göreceğiz.

``

## STL konteyneri nedir?

Konteyner, belirli bir türdeki nesneleri saklayan ve bunlara erişmek için ortak operasyonlar sağlayan sınıftır. STL konteynerleri şablon tabanlıdır. Örneğin `vector<int>` tam sayıları, `vector<string>` ise metinleri saklar.

Doğru konteyner seçimi yalnızca kodun görünümünü değil, performansını da etkiler. Bir yapının çalışma maliyetini değerlendirirken genellikle Big-O gösterimi kullanılır. Eleman sayısı $n$ olduğunda doğrusal aramanın maliyeti yaklaşık $O(n)$, dengeli ağaç üzerinde aramanın maliyeti ise $O(\log n)$ olur.

| Konteyner | Temel yapı | Rastgele erişim | Araya ekleme/silme | Arama |
|---|---|---:|---:|---:|
| `vector` | Dinamik dizi | $O(1)$ | Genellikle $O(n)$ | $O(n)$ |
| `list` | Çift bağlı liste | $O(n)$ | Konum biliniyorsa $O(1)$ | $O(n)$ |
| `map` | Dengeli arama ağacı | Anahtarla $O(\log n)$ | $O(\log n)$ | $O(\log n)$ |

## vector: Hızlı ve pratik dinamik dizi

`vector`, elemanları bellekte ardışık olarak saklar. Bu özellik önbellek dostu çalışmasını ve indeksle hızlı erişimi sağlar. Boyutu çalışma sırasında büyüyebilir; kapasite yetersiz kaldığında daha büyük bir bellek alanı ayırıp elemanları oraya taşır.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> puanlar{70, 95, 82};
    puanlar.push_back(88); // Sona eleman ekler

    std::sort(puanlar.begin(), puanlar.end());

    for (int puan : puanlar)
        std::cout << puan << ' ';
}
```

Burada `push_back` sona yeni bir değer ekler. `begin()` ve `end()` ise STL algoritmalarının kullanabileceği iterator sınırlarını üretir. Sona ekleme, yeniden bellek ayırma işlemleri hesaba katıldığında amortize $O(1)$ maliyetindedir:

$$T_{ortalama}(push\_back) = O(1)$$

Sık indeks erişimi, sıralama veya elemanlar üzerinde hızlı dolaşma gerekiyorsa varsayılan tercihiniz çoğu zaman `vector` olmalıdır.

## list: Bağlantılarla gelen esneklik

`list`, her elemanın önceki ve sonraki düğümü gösterdiği çift bağlı listedir. Elemanlar bellekte yan yana bulunmak zorunda değildir. Bu nedenle `liste[3]` gibi indeks erişimi desteklenmez; istenen konuma iterator ile ilerlenir.

```cpp
#include <iostream>
#include <list>

int main() {
    std::list<std::string> görevler{"Kod yaz", "Test et"};
    auto konum = görevler.begin();
    ++konum;

    görevler.insert(konum, "Kahve iç");
    görevler.remove("Test et");

    for (const auto& görev : görevler)
        std::cout << görev << '\n';
}
```

`insert`, bilinen iterator konumuna eleman ekler; `remove` eşleşen değerleri kaldırır. Listenin avantajı, elemanları kaydırmadan ekleme ve silme yapabilmesidir. Ancak her düğüm bağlantı adresleri tuttuğu için bellek tüketimi daha yüksektir. Ayrıca modern işlemcilerin önbellek yapısından `vector` kadar iyi yararlanamaz.

## map: Anahtar ve değerleri eşleştirmek

`map`, her anahtarı bir değerle ilişkilendirir ve anahtarları sıralı tutar. Aynı anahtar yalnızca bir kez bulunabilir. Telefon rehberi, ürün fiyatları veya kullanıcı kimliğiyle profil eşleştirme gibi senaryolara uygundur.

```cpp
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, int> stok;
    stok["klavye"] = 12;
    stok["fare"] = 25;

    if (auto it = stok.find("klavye"); it != stok.end())
        std::cout << "Stok: " << it->second;
}
```

`find`, anahtarı arar ve bulunamazsa `end()` döndürür. Sadece kontrol amacıyla `operator[]` kullanmak istenmeyen yeni bir kayıt oluşturabileceğinden `find` veya modern C++ sürümlerinde `contains` tercih edilmelidir.

## Hangisini seçmeliyiz?

İndeksleme ve genel performans önemliyse `vector`, bilinen konumlarda yoğun ekleme-silme varsa `list`, anahtar-değer ilişkisi ve sıralı anahtarlar gerekiyorsa `map` seçilebilir. Kısacası sihirli bir “en iyi konteyner” yoktur; erişim modeli, bellek maliyeti ve algoritmik karmaşıklık birlikte değerlendirilmelidir. Doğru seçim, kodunuzu hem sadeleştirir hem de veri büyüdüğünde performans sürprizlerini azaltır.

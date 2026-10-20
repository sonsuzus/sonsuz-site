---
layout: post
title: "C++ Şablonlar: Türlerden Bağımsız Jenerik Kod Yazmak"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - templates
  - jenerik programlama
  - fonksiyon şablonları
  - sınıf şablonları
  - programlama
toc: true
image: /img/c-sablonlar-turlerden-70.png
---

Aynı toplama, karşılaştırma veya sıralama işlemini `int`, `double` ve başka veri türleri için tekrar tekrar yazmak pek eğlenceli değildir. C++ şablonları, algoritmayı bir kez tanımlayıp onu farklı türlerle kullanmamızı sağlar. Böylece derleyici, ihtiyaç duyulan türe uygun kodu bizim için üretir; biz de kopyala-yapıştır bataklığından kurtuluruz.
``
## Şablonların temel mantığı

Şablon, henüz kesinleşmemiş bir türü veya değeri parametre olarak alan kod kalıbıdır. `T` gibi bir şablon parametresi başlangıçta gerçek bir tür değildir; derleme sırasında `int`, `double` veya kullanıcı tarafından tanımlanmış bir sınıfla değiştirilir.

Bunu matematikteki genel bir fonksiyona benzetebiliriz:

$$f(x, y) = x + y$$

Burada toplama işlemi, $x$ ve $y$ değerlerinin türünden çok `+` operatörünü destekleyip desteklemediğiyle ilgilenir. Şablonlar da benzer biçimde çalışır. Bir tür, şablonun kullandığı işlemleri sağlıyorsa o şablonla kullanılabilir.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Her tür için ayrı fonksiyon | Okuması kolaydır | Kod tekrarı oluşturur |
| `void*` kullanımı | Türden bağımsız görünebilir | Tür güvenliği zayıftır |
| Şablon kullanımı | Tür güvenli ve yeniden kullanılabilirdir | Hata mesajları karmaşık olabilir |

## Fonksiyon şablonları

İki değerden büyük olanı döndüren jenerik bir fonksiyon yazalım:

```cpp
#include <iostream>
#include <string>

template <typename T>
T buyukOlan(const T& a, const T& b) {
    return (a > b) ? a : b;
}

int main() {
    std::cout << buyukOlan(12, 7) << '\n';
    std::cout << buyukOlan(3.4, 8.1) << '\n';
    std::cout << buyukOlan(std::string("Ali"), std::string("Zeynep"));
}
```

`template <typename T>` ifadesi, `T` adlı bir tür parametresi tanımlar. Derleyici ilk çağrıda `T = int`, ikinci çağrıda `T = double` kabul eder. Bu işleme **şablon örnekleme** denir. Kabaca üretilen fonksiyon sayısını şöyle düşünebiliriz:

$$N_{üretilen} \approx N_{benzersiz\ tür\ birleşimi}$$

Parametreleri `const T&` ile almak, özellikle büyük nesnelerin gereksiz yere kopyalanmasını önler. Ancak kullanılan türün `>` operatörünü desteklemesi gerekir; aksi hâlde derleme hatası alınır.

## Birden fazla tür parametresi

Bazen giriş türleri birbirinden farklı olabilir:

```cpp
template <typename T, typename U>
auto topla(const T& a, const U& b) {
    return a + b;
}

int main() {
    auto sonuc = topla(10, 2.5); // Sonuç double olur
}
```

`auto` dönüş türünü `a + b` ifadesinden çıkarır. Böylece `int` ve `double` birlikte kullanılabilir. Yine de sonuç, ilgili türlerin birbirleriyle toplanabilmesine bağlıdır.

## Sınıf şablonları

Şablonlar yalnızca fonksiyonlar için değildir. Farklı türlerde değer saklayabilen basit bir kutu sınıfı oluşturalım:

```cpp
#include <utility>

template <typename T>
class Kutu {
private:
    T deger;

public:
    explicit Kutu(T yeniDeger)
        : deger(std::move(yeniDeger)) {}

    const T& getir() const {
        return deger;
    }

    void ayarla(const T& yeniDeger) {
        deger = yeniDeger;
    }
};

int main() {
    Kutu<int> puan(100);
    Kutu<std::string> mesaj("Merhaba şablon!");
}
```

`Kutu<int>` ve `Kutu<std::string>`, aynı sınıf şablonundan üretilmiş farklı sınıf türleridir. Derleyici bunların her biri için uygun alanları ve metotları oluşturur.

| Özellik | Fonksiyon şablonu | Sınıf şablonu |
|---|---|---|
| Tür çıkarımı | Genellikle otomatik | Çoğunlukla açıkça belirtilir |
| Kullanım amacı | Jenerik algoritmalar | Jenerik veri yapıları |
| Örnek | `buyukOlan(3, 5)` | `Kutu<int>` |

## Dikkat edilmesi gerekenler

Şablon tanımları çoğunlukla başlık dosyalarında bulunur. Çünkü derleyicinin belirli bir tür için kod üretirken şablonun tüm gövdesini görmesi gerekir. Ayrıca her tür, şablonda kullanılan operatörleri sağlamalıdır. Modern C++20 projelerinde bu beklentiler `concept` yapılarıyla açıkça ifade edilebilir.

Şablonlar; `std::vector`, `std::map` ve `std::sort` gibi Standart Kütüphane araçlarının temelidir. Kısacası doğru kullanıldıklarında daha az tekrar, güçlü tür güvenliği ve genişletilebilir kod sunarlar. Derleyici biraz daha çalışır, fakat programcı çok daha az terler!

![c-sablonlar-turlerden-70](/img/c-sablonlar-turlerden-70.svg)


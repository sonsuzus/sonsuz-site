---
layout: post
title: "C++ Operatör Aşırı Yükleme: Nesnelerin Operatörlerle Dansı"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - operatör aşırı yükleme
  - nesne yönelimli programlama
  - oop
  - sınıflar
toc: true
image: /img/c-operator-asiri-54.png
---

C++ dilinde operatörler yalnızca `int`, `double` veya `char` gibi hazır veri türlerine hizmet etmek zorunda değildir. Operatör aşırı yükleme sayesinde `+`, `-`, `==` ve `<<` gibi tanıdık sembollerin kullanıcı tanımlı sınıflarla nasıl çalışacağını belirleyebiliriz. Böylece nesnelerimiz, dilin doğal bir parçasıymış gibi okunabilir ve anlaşılır ifadelerde rol alır.

![c-operator-asiri-54](/img/c-operator-asiri-54.svg)

``
## Operatör aşırı yükleme nedir?

Operatör aşırı yükleme, bir operatöre kullanıcı tanımlı türler için yeni bir davranış kazandırmaktır. Örneğin iki `Vektor` nesnesini toplamak istediğimizi düşünelim. Aşırı yükleme olmadan `vektor1 + vektor2` ifadesi derleme hatası üretir. Çünkü derleyici iki vektörün nasıl toplanacağını kendiliğinden bilemez.

Matematikte iki boyutlu vektörlerin toplamı şöyledir:

$$
(x_1, y_1) + (x_2, y_2) = (x_1+x_2, y_1+y_2)
$$

Bu kuralı C++ sınıfımıza `operator+` adlı özel bir fonksiyonla öğretebiliriz. Buradaki amaç operatörün anlamını tamamen değiştirmek değil, sınıfın temsil ettiği kavrama uygun bir davranış oluşturmaktır.

| Normal ifade | Fonksiyon karşılığı | Amaç |
|---|---|---|
| `a + b` | `a.operator+(b)` | İki nesneyi toplamak |
| `a == b` | `a.operator==(b)` | Nesneleri karşılaştırmak |
| `cout << a` | `operator<<(cout, a)` | Nesneyi ekrana yazdırmak |
| `++a` | `a.operator++()` | Nesnenin değerini artırmak |

## Bir vektör sınıfında `+` operatörü

Aşağıdaki sınıf, iki vektörü bileşenlerine göre toplar:

```cpp
class Vektor {
private:
    double x;
    double y;

public:
    Vektor(double x, double y) : x(x), y(y) {}

    Vektor operator+(const Vektor& diger) const {
        return Vektor(x + diger.x, y + diger.y);
    }

    void yazdir() const {
        std::cout << "(" << x << ", " << y << ")\n";
    }
};
```

`operator+` fonksiyonu sağ taraftaki nesneyi `const Vektor&` olarak alır. Referans kullanımı gereksiz kopyalamayı önler; `const` ise parametrenin değiştirilmeyeceğini garanti eder. Fonksiyonun sonundaki ikinci `const`, toplama işleminin sol taraftaki nesneyi de değiştirmediğini söyler.

```cpp
Vektor a(2, 3);
Vektor b(4, 5);
Vektor sonuc = a + b;
sonuc.yazdir(); // (6, 8)
```

Burada `a + b`, derleyici tarafından temelde `a.operator+(b)` biçiminde değerlendirilir. Sonuç yeni bir nesnedir; dolayısıyla özgün vektörler korunur.

## Üye fonksiyon mu, global fonksiyon mu?

Operatörler sınıfın üye fonksiyonu veya sınıf dışındaki bir fonksiyon olarak tanımlanabilir.

| Yaklaşım | Avantajı | Uygun kullanım |
|---|---|---|
| Üye fonksiyon | Sınıf üyelerine doğrudan erişir | `+`, `-`, `==`, `++` |
| Global fonksiyon | Sol operand farklı tür olabilir | `<<`, simetrik dönüşümler |
| `friend` fonksiyon | Özel üyelere erişebilir | Akış operatörleri |

Örneğin nesneyi doğrudan `std::cout` ile yazdırmak için sol operand bir `std::ostream` nesnesidir. Bu nedenle `<<` genellikle global ve `friend` olarak tanımlanır:

```cpp
friend std::ostream& operator<<(std::ostream& os, const Vektor& v) {
    os << "(" << v.x << ", " << v.y << ")";
    return os;
}
```

`std::ostream&` döndürülmesi, `std::cout << a << b;` biçiminde zincirleme kullanım sağlar.

## Kurallar ve iyi uygulamalar

C++ yeni operatör sembolleri oluşturmamıza izin vermez. Ayrıca operatör önceliği, operand sayısı ve birleşme yönü değiştirilemez. `::`, `.`, `.*` ve `?:` gibi bazı operatörler de aşırı yüklenemez.

En önemli tasarım ilkesi şaşırtmamaktır. `+` operatörü nesneleri toplamalı, onları silmemeli veya ekrana yazdırmamalıdır. `==` mantıksal eşitliği ölçmeli ve mümkünse `bool` döndürmelidir. Kısacası operatör aşırı yükleme güçlü bir araçtır; doğru kullanıldığında kodu matematiksel ve akıcı, yanlış kullanıldığında ise gizemli bir bulmacaya dönüştürür.

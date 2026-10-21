---
layout: post
title: "C++ Sanal Fonksiyonlar ve Çok Biçimlilik: Tek Arayüz, Farklı Davranışlar"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - polymorphism
  - sanal fonksiyonlar
  - nesne yönelimli programlama
  - kalıtım
  - oop
toc: true
image: /img/c-sanal-fonksiyonlar-84.png
---

Bir oyun geliştirdiğimizi ve ekranda savaşçı, büyücü, okçu gibi farklı karakterlerin bulunduğunu düşünelim. Her karakter saldırır, ancak saldırma biçimleri birbirinden farklıdır. C++ çok biçimliliği, bu nesneleri tek bir ortak arayüz üzerinden yönetirken doğru davranışın çalışma zamanında seçilmesini sağlar. Böylece uzun `if-else` zincirleri yerine genişletilebilir ve bakımı kolay bir tasarım elde ederiz.


![c-sanal-fonksiyonlar-84](/img/c-sanal-fonksiyonlar-84.svg)

``

## Çok biçimlilik nedir?

Polymorphism, kelime anlamıyla **çok biçimlilik** demektir. Nesne yönelimli programlamada aynı fonksiyon çağrısının nesnenin gerçek tipine göre farklı sonuç üretmesini ifade eder. C++ içerisinde bunun iki temel çeşidi vardır:

| Tür | Seçim zamanı | Örnek |
|---|---|---|
| Statik çok biçimlilik | Derleme zamanı | Fonksiyon aşırı yükleme, şablonlar |
| Dinamik çok biçimlilik | Çalışma zamanı | Sanal fonksiyonlar ve kalıtım |

Dinamik çok biçimlilik için genellikle üç bileşen gerekir: bir temel sınıf, bu sınıftan türeyen sınıflar ve `virtual` olarak tanımlanmış bir üye fonksiyon.

Matematiksel olarak ortak bir arayüzü $I$, farklı nesne tiplerini ise $T_1, T_2, \ldots, T_n$ ile gösterelim. Aynı işlem $f$, nesnenin dinamik tipine göre farklı uygulanır:

$$f(I) \rightarrow f_{T_i}(T_i)$$

Yani kod `f` işlemini ortak arayüz üzerinden ister; hangi özel uygulamanın çalışacağına program çalışma zamanında karar verir.

## Sanal fonksiyon nasıl çalışır?

Aşağıdaki örnekte bütün karakterler `saldir()` arayüzünü sunar, fakat her biri kendine özgü davranır:

```cpp
#include <iostream>
#include <memory>
#include <vector>

class Karakter {
public:
    virtual void saldir() const {
        std::cout << "Karakter saldırdı.\n";
    }

    virtual ~Karakter() = default;
};

class Savasci : public Karakter {
public:
    void saldir() const override {
        std::cout << "Savaşçı kılıcını savurdu!\n";
    }
};

class Buyucu : public Karakter {
public:
    void saldir() const override {
        std::cout << "Büyücü ateş topu gönderdi!\n";
    }
};
```

`virtual` anahtar sözcüğü, çağrılacak fonksiyonun nesnenin gerçek tipine bakılarak seçilmesini sağlar. `override` ise türetilmiş sınıftaki fonksiyonun gerçekten bir sanal fonksiyonu ezdiğini derleyiciye doğrulatır. İmza yanlış yazılırsa derleyici hata verir; bu nedenle `override` kullanmak iyi bir güvenlik kemeridir.

Derleyiciler bu mekanizmayı çoğunlukla **vtable** adlı sanal fonksiyon tablosu ve nesnede tutulan gizli bir **vptr** işaretçisiyle gerçekleştirir. C++ standardı bu yöntemi zorunlu kılmaz, fakat yaygın uygulama budur. Sanal çağrının küçük bir dolaylı erişim maliyeti vardır; buna karşılık sağladığı esneklik çoğu uygulamada çok daha değerlidir.

## Nesneleri ortak koleksiyonda yönetmek

Akıllı işaretçiler sayesinde farklı karakterleri aynı koleksiyonda güvenli biçimde saklayabiliriz:

```cpp
int main() {
    std::vector<std::unique_ptr<Karakter>> takim;

    takim.push_back(std::make_unique<Savasci>());
    takim.push_back(std::make_unique<Buyucu>());

    for (const auto& karakter : takim) {
        karakter->saldir();
    }
}
```

Döngü yalnızca `Karakter` arayüzünü bilir. Buna rağmen ilk nesne kılıç kullanır, ikincisi ateş topu fırlatır. İşte dinamik çok biçimliliğin küçük ama etkileyici sihri budur.

## Kritik ayrıntılar

Temel sınıf üzerinden silme yapılacaksa yıkıcı mutlaka sanal olmalıdır. Aksi hâlde türetilmiş sınıfın yıkıcısı çağrılmayabilir ve kaynak sızıntıları oluşabilir. Bu nedenle `virtual ~Karakter() = default;` önemli bir satırdır.

Nesneleri değer olarak kopyalamak da **object slicing** problemine yol açar:

```cpp
Savasci savasci;
Karakter kopya = savasci; // Savasci kısmı kesilir
kopya.saldir();           // Temel sınıf davranışı çalışır
```

Dinamik davranışı korumak için temel sınıf referansı, işaretçisi veya `std::unique_ptr` gibi akıllı işaretçiler kullanılmalıdır.

Sonuç olarak sanal fonksiyonlar, kodu somut sınıflara değil ortak sözleşmelere bağlar. Yeni bir `Okcu` sınıfı eklediğimizde mevcut döngüyü değiştirmemiz gerekmez. Böylece C++ programı hem yeni karakterlere hem de gelecekte gelecek sürpriz gereksinimlere hazırlıklı olur.

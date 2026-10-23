---
layout: post
title: "C++ Nesne Dilimlenmesi: Kopyalama Sırasında Kaybolan Kimlik"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - nesne yönelimli programlama
  - object slicing
  - kalıtım
  - polimorfizm
  - referanslar
toc: true
image: /img/c-nesne-dilimlenmesi-46.png
---

C++’ta kalıtım kullanırken türetilmiş bir nesneyi temel sınıf türündeki değişkene değer olarak atamak ilk bakışta zararsız görünebilir. Kod derlenir, program çalışır ve çoğu zaman hata mesajı da alınmaz. Fakat bu işlem sırasında nesnenin yalnızca temel sınıfa ait bölümü kopyalanır; türetilmiş sınıfın eklediği veriler ve davranış kimliği kaybolur. İşte bu sessiz bilgi kaybına **nesne dilimlenmesi**, yani *object slicing* denir.

``

## Nesne neden “dilimlenir”?

Bir türetilmiş sınıf nesnesini kavramsal olarak iki parçalı düşünebiliriz:

$$Türetilmiş\ Nesne = Temel\ Bölüm + Türetilmiş\ Bölüm$$

Temel sınıf türünde değer saklayan bir değişkenin kapasitesi ise yalnızca temel bölüme uygundur. Dolayısıyla aşağıdaki atamada `Calisan` nesnesinin `Yazilimci` sınıfına özgü kısmı hedef nesneye sığmaz. C++ bu kısmı hata vermeden dışarıda bırakır.

```cpp
#include <iostream>
#include <string>

class Calisan {
public:
    std::string ad;

    virtual void tanit() const {
        std::cout << ad << ": Calisan\n";
    }
};

class Yazilimci : public Calisan {
public:
    std::string dil;

    void tanit() const override {
        std::cout << ad << ": " << dil << " gelistiricisi\n";
    }
};

int main() {
    Yazilimci y;
    y.ad = "Ada";
    y.dil = "C++";

    Calisan c = y; // Nesne dilimlenir
    c.tanit();     // Ada: Calisan
}
```

`tanit()` sanal olmasına rağmen sonuç değişmez. Çünkü `c`, artık bağımsız ve gerçek bir `Calisan` nesnesidir. İçinde `Yazilimci` kimliği bulunmadığından sanal fonksiyon mekanizmasının çağırabileceği türetilmiş davranış da kalmamıştır. `virtual`, dilimlenmeyi önlemez; yalnızca nesneye referans veya işaretçi üzerinden erişildiğinde dinamik türü kullanır.

| Aktarım biçimi | Kopyalama var mı? | Türetilmiş bilgi korunur mu? | Polimorfizm çalışır mı? |
|---|---:|---:|---:|
| `Calisan c = y` | Evet | Hayır | Hayır |
| `Calisan& c = y` | Hayır | Evet | Evet |
| `Calisan* c = &y` | Hayır | Evet | Evet |
| `unique_ptr<Calisan>` | Nesnenin kendisi kopyalanmaz | Evet | Evet |

![c-nesne-dilimlenmesi-46](/img/c-nesne-dilimlenmesi-46.svg)


## Fonksiyon parametrelerindeki gizli tuzak

Dilimlenme yalnızca açık atamalarda oluşmaz. Temel sınıfı değer olarak kabul eden fonksiyonlar da aynı soruna yol açar:

```cpp
void bilgiYaz(Calisan calisan) { // Değer ile alınıyor
    calisan.tanit();
}

Yazilimci y;
bilgiYaz(y); // Parametre oluşturulurken dilimlenir
```

Çözüm, parametreyi çoğunlukla sabit referansla almaktır:

```cpp
void bilgiYaz(const Calisan& calisan) {
    calisan.tanit(); // Gerçek türe göre çağrı yapılır
}
```

Bu yöntem hem türetilmiş kimliği korur hem de gereksiz nesne kopyasını engeller. Fonksiyon nesneyi değiştirmeyecekse `const` kullanılması niyeti açıkça belirtir.

## Koleksiyonlarda doğru tür seçimi

`std::vector<Calisan>` içine `Yazilimci` eklemek de nesneyi dilimler. Farklı türetilmiş türleri aynı koleksiyonda polimorfik olarak saklamak için akıllı işaretçiler kullanılabilir:

```cpp
#include <memory>
#include <vector>

std::vector<std::unique_ptr<Calisan>> ekip;
ekip.push_back(std::make_unique<Yazilimci>());

for (const auto& kisi : ekip) {
    kisi->tanit();
}
```

Burada vektör nesnelerin kendilerini değil, temel sınıf türündeki sahiplik işaretçilerini saklar. Gerçek nesneler türetilmiş türleriyle yaşamaya devam eder. Temel sınıf üzerinden silme yapılacağı için yıkıcının da sanal olması gerekir:

```cpp
virtual ~Calisan() = default;
```

Özetle, değer semantiği bilinçli bir temel sınıf kopyası istendiğinde uygundur; polimorfik davranış istendiğinde ise referanslar, işaretçiler ve akıllı işaretçiler tercih edilmelidir. Derleyicinin sessiz kalması işlemin zararsız olduğu anlamına gelmez: Nesnenin yalnızca üst dilimini servis edip geri kalanını mutfakta unutmuş olabilirsiniz.

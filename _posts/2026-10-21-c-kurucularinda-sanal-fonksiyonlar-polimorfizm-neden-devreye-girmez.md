---
layout: post
title: "C++ Kurucularında Sanal Fonksiyonlar: Polimorfizm Neden Devreye Girmez?"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - constructor
  - sanal-fonksiyon
  - polimorfizm
  - nesne-yönelimli-programlama
toc: true
image: /img/c-kurucularinda-sanal-30.png
---

![c-kurucularinda-sanal-30](/img/c-kurucularinda-sanal-30.svg)


C++ ile nesne yönelimli programlama yaparken kurucu içinde sanal bir fonksiyon çağırmak ilk bakışta gayet mantıklı görünebilir. Sonuçta fonksiyon `virtual` olarak tanımlanmıştır; nesne türetilmiş sınıfa aitse onun sürümü çalışmalıdır, değil mi? Ne yazık ki C++ burada bilinçli biçimde farklı davranır. Kurucu çalışırken sanal çağrı, o anda kurulmakta olan sınıfın uygulamasına bağlanır; henüz hazır olmayan türetilmiş sınıfa gönderilmez.
``
## Temel örnek

Aşağıdaki kod, sık karşılaşılan beklenti ile gerçek davranış arasındaki farkı gösterir:

```cpp
#include <iostream>

class Base {
public:
    Base() {
        std::cout << "Base kuruluyor\n";
        initialize();
    }

    virtual void initialize() {
        std::cout << "Base::initialize\n";
    }

    virtual ~Base() = default;
};

class Derived : public Base {
public:
    Derived() : value(42) {
        std::cout << "Derived kuruluyor\n";
    }

    void initialize() override {
        std::cout << "Derived::initialize, value = "
                  << value << '\n';
    }

private:
    int value;
};

int main() {
    Derived object;
}
```

Programın önemli çıktısı şöyledir:

```text
Base kuruluyor
Base::initialize
Derived kuruluyor
```

`object`, `Derived` türünde olmasına rağmen `Base` kurucusundaki çağrı `Derived::initialize()` fonksiyonuna gitmez. Bu bir derleyici hatası veya polimorfizm arızası değil, nesnenin yaşam döngüsünü koruyan dil kuralıdır.

## Nesne hangi sırayla oluşur?

Bir `Derived` nesnesinin kurulumu basitleştirilmiş biçimde şu sırayı izler:

1. Bellek ayrılır.
2. `Base` alt nesnesi kurulur.
3. `Derived` üyeleri başlatılır.
4. `Derived` kurucusunun gövdesi çalışır.
5. Nesne tam bir `Derived` olarak kullanılabilir.

Kurulum ilerlemesini yaklaşık olarak $P = c / n$ ile düşünebiliriz. Burada $c$ tamamlanan aşama, $n$ toplam aşama sayısıdır. `Base` kurucusu çalışırken $P < 1$ olduğundan, türetilmiş bölüm henüz geçerli durumuna ulaşmamıştır.

Eğer çağrı `Derived::initialize()` fonksiyonuna yönlendirilseydi, bu fonksiyon henüz başlatılmamış `value` üyesini okuyabilirdi. Böyle bir erişim tanımsız veya anlamsal açıdan bozuk davranışlara kapı açardı. C++ bu nedenle kurulum sırasında nesnenin dinamik türünü geçici olarak kurulmakta olan sınıfla sınırlar.

| Çağrının yapıldığı yer | Seçilen uygulama | Türemiş bölüm hazır mı? |
|---|---|---|
| `Base` kurucusu | `Base::initialize()` | Hayır |
| `Derived` kurucusu gövdesi | `Derived::initialize()` | Büyük ölçüde evet |
| Kurulum tamamlandıktan sonra | Dinamik türe göre | Evet |
| `Base` yıkıcısı | `Base` sürümü | Hayır; türemiş bölüm yıkılmıştır |

Aynı kural yıkıcılar için de geçerlidir. Yıkım ters sırada gerçekleştiği için temel sınıf yıkıcısı çalışırken türetilmiş bölüm artık yaşamını tamamlamıştır.

## Daha güvenli tasarım: iki aşamalı başlatma

Polimorfik davranış gerekiyorsa sanal fonksiyonu nesne tamamen kurulduktan sonra çağırabilirsiniz:

```cpp
class Base {
public:
    virtual void initialize() = 0;
    virtual ~Base() = default;
};

class Derived : public Base {
public:
    void initialize() override {
        // Tüm üyeler artık güvenle kullanılabilir.
    }
};

int main() {
    Derived object;
    object.initialize();
}
```

Daha kontrollü bir seçenek fabrika fonksiyonudur. Fabrika önce nesneyi oluşturur, ardından sanal başlatmayı gerçekleştirir:

```cpp
#include <memory>

std::unique_ptr<Base> createDerived() {
    auto object = std::make_unique<Derived>();
    object->initialize();
    return object;
}
```

| Yaklaşım | Avantaj | Risk |
|---|---|---|
| Kurucuda sanal çağrı | Kısa görünür | Beklenen override çalışmaz |
| Açık `initialize()` çağrısı | Basit ve anlaşılır | Çağırmayı unutmak mümkündür |
| Fabrika fonksiyonu | Kurulum adımlarını merkezileştirir | Tasarıma ek katman getirir |
| Kurucuya bağımlılık verme | Nesneyi hemen geçerli kılar | Daha fazla tasarım planlaması ister |

Özetle, kurucu içindeki sanal çağrı polimorfizmi tamamen kapatmaz; çağrıyı nesnenin güvenli biçimde kurulmuş bölümüne sınırlar. Gerçek dinamik gönderim gerekiyorsa işlemi kurulum sonrasına taşımak veya fabrika deseni kullanmak en temiz çözümdür.

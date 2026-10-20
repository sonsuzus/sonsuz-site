---
layout: post
title: "C++’ta Sanal Fonksiyonlar ve Varsayılan Parametreler: İki Farklı Karar Mekanizması"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - oop
  - sanal-fonksiyonlar
  - varsayılan-parametreler
  - polimorfizm
toc: true
image: /img/cta-sanal-fonksiyonlar-41.png
---

C++’ta sanal fonksiyonlar çalışma zamanlı polimorfizmin yıldızıdır; varsayılan parametreler ise çağrıları kısaltan kullanışlı yardımcılardır. Ancak bu iki özellik aynı fonksiyonda buluştuğunda küçük bir sürpriz ortaya çıkar: Çalıştırılan fonksiyon türetilmiş sınıfa aitken kullanılan varsayılan değer temel sınıftan gelebilir. İlk bakışta çelişkili görünse de sebep, C++ derleyicisinin iki kararı farklı zamanlarda vermesidir.

``

## Problemi Bir Örnekle Görelim

Aşağıdaki programda hem temel hem de türetilmiş sınıf aynı sanal fonksiyon için farklı varsayılan değerler tanımlıyor:

```cpp
#include <iostream>

class Base {
public:
    virtual void yazdir(int adet = 1) const {
        std::cout << "Base: " << adet << '\n';
    }

    virtual ~Base() = default;
};

class Derived : public Base {
public:
    void yazdir(int adet = 5) const override {
        std::cout << "Derived: " << adet << '\n';
    }
};

int main() {
    Derived nesne;
    Base* ptr = &nesne;

    ptr->yazdir();
}
```

Pek çok geliştirici çıktının `Derived: 5` olmasını bekler. Gerçek çıktı ise şöyledir:

```text
Derived: 1
```

Burada `Derived::yazdir` çalıştırılmış, fakat `Base::yazdir` bildirimindeki `1` değeri kullanılmıştır. C++ bize adeta “Fonksiyonu dinamik, parametreyi statik seçtim!” demektedir.

## Statik ve Dinamik Bağlama

Sanal fonksiyonun hangi gövdesinin çalışacağı, nesnenin gerçek çalışma zamanı türüne göre belirlenir. `ptr`, `Base*` türünde olmasına rağmen bir `Derived` nesnesini gösterdiği için sanal çağrı `Derived::yazdir` fonksiyonuna yönlendirilir.

Varsayılan parametreler ise polimorfik değildir. Derleyici, eksik argümanı çağrı noktasında ve ifadenin statik türüne bakarak doğrudan ekler. Kavramsal olarak şu dönüşüm yapılır:

```cpp
ptr->yazdir();

// Derleyicinin çağrı noktasındaki yaklaşımı:
ptr->yazdir(1);
```

Ardından sanal çağrı mekanizması hangi fonksiyon gövdesinin çalışacağını seçer. Süreci basitçe şöyle ifade edebiliriz:

$$Çağrı = VarsayılanDeğer(StatikTür) + FonksiyonGövdesi(DinamikTür)$$

| Karar | Kullanılan tür | Belirlenme zamanı |
|---|---|---|
| Varsayılan argüman | Statik tür (`Base*`) | Derleme zamanı |
| Fonksiyon gövdesi | Dinamik tür (`Derived`) | Çalışma zamanı |
| Sonuç | `Derived::yazdir(1)` | İki mekanizmanın birleşimi |

![cta-sanal-fonksiyonlar-41](/img/cta-sanal-fonksiyonlar-41.svg)


Aynı nesneyi doğrudan çağırırsak sonuç değişir:

```cpp
nesne.yazdir(); // Derived::yazdir(5)
ptr->yazdir();  // Derived::yazdir(1)
```

Çünkü ilk ifadenin statik türü `Derived`, ikincisininki `Base*` üzerinden `Base` sınıfıdır.

## Neden Böyle Tasarlanmıştır?

Varsayılan argüman, fonksiyonun çalışma zamanı davranışının değil, bildirimin sunduğu arayüzün parçasıdır. Derleyici çağrı noktasını işlerken nesnenin gelecekte hangi gerçek türe sahip olacağını bilmek zorunda değildir. Ayrıca varsayılan değerlerin sanal tabloya eklenmesi daha karmaşık bir çağrı modeli ve ek çalışma zamanı maliyeti oluştururdu.

| Özellik | Sanal fonksiyon | Varsayılan parametre |
|---|---|---|
| Polimorfik mi? | Evet | Hayır |
| `override` ile denetlenir mi? | Evet | Hayır |
| Dinamik türe bakar mı? | Evet | Hayır |
| Alt sınıfta değiştirmek güvenli mi? | Davranış için evet | Genellikle hayır |

## Güvenli Tasarım Yaklaşımı

En temiz çözüm, varsayılan değeri yalnızca sanal olmayan bir arayüz fonksiyonunda tutmaktır:

```cpp
class Base {
public:
    void yazdir(int adet = 1) const {
        yazdirImpl(adet);
    }

    virtual ~Base() = default;

private:
    virtual void yazdirImpl(int adet) const {
        std::cout << "Base: " << adet << '\n';
    }
};

class Derived : public Base {
private:
    void yazdirImpl(int adet) const override {
        std::cout << "Derived: " << adet << '\n';
    }
};
```

Bu yaklaşımda varsayılan değer tek yerde tanımlanır, sanal uygulama ise yalnızca davranışı değiştirir. Böylece işaretçinin statik türüne bağlı sürprizler ortadan kalkar. Kısa kural şudur: Sanal fonksiyonlarda farklı varsayılan parametreler tanımlamayın; varsayılan seçimini arayüze, polimorfik davranışı ayrı bir sanal fonksiyona bırakın.

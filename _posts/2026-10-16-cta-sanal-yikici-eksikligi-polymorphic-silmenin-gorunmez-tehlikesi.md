---
layout: post
title: "C++’ta Sanal Yıkıcı Eksikliği: Polymorphic Silmenin Görünmez Tehlikesi"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - sanal yıkıcı
  - polymorphism
  - tanımsız davranış
  - bellek yönetimi
toc: true
image: /img/cta-sanal-yikici-22.png
---

C++’ta kalıtım kullanırken küçük görünen bir `virtual` anahtar sözcüğü, programın güvenli çalışması ile tanımsız davranış bataklığı arasındaki sınırı çizebilir. Özellikle türetilmiş bir nesne, temel sınıf işaretçisi üzerinden siliniyorsa temel sınıfın yıkıcısının sanal olmaması ciddi bir tasarım hatasıdır.


![cta-sanal-yikici-22](/img/cta-sanal-yikici-22.svg)

``

## Problem nerede başlıyor?

Çok biçimlilik sayesinde `Derived` türündeki bir nesneyi `Base*` işaretçisiyle yönetebiliriz. Sanal fonksiyon çağrıları nesnenin gerçek, yani dinamik türüne göre çözülür. Ancak aynı davranış yıkıcıya otomatik olarak uygulanmaz: Temel sınıfın yıkıcısı `virtual` değilse `delete basePtr;` ifadesi tanımsız davranış üretir.

```cpp
#include <iostream>

class Base {
public:
    ~Base() {
        std::cout << "Base yok edildi\n";
    }
};

class Derived : public Base {
    int* data;

public:
    Derived() : data(new int[100]) {}

    ~Derived() {
        delete[] data;
        std::cout << "Derived yok edildi\n";
    }
};

int main() {
    Base* object = new Derived();
    delete object; // Tanımsız davranış!
}
```

Burada işaretçinin statik türü `Base*`, nesnenin dinamik türü ise `Derived` olur. Yıkımın doğru sırası şöyledir:

$$Derived::~Derived() \rightarrow Base::~Base()$$

Fakat `Base::~Base()` sanal değilse dil standardı, yalnızca temel yıkıcının çağrılacağını garanti etmez; işlemin tamamını **undefined behavior** olarak sınıflandırır. Örnekte `data` serbest bırakılmayabilir ve bellek sızıntısı oluşabilir. Daha kötüsü, program çalışıyor gibi görünebilir. Tanımsız davranışın en sinsi yanı da budur: Hata vermek zorunda değildir.

## Neden yalnızca bellek sızıntısı değil?

Bir programın olası sonuç kümesini kabaca şöyle düşünebiliriz:

$$UB \Rightarrow \{\text{çökme, sızıntı, bozulma, görünürde doğru çalışma, herhangi bir sonuç}\}$$

Derleyici, tanımsız davranışın gerçekleşmediğini varsayarak optimizasyon yapabilir. Bu nedenle hata; farklı derleyicide, optimizasyon seviyesinde veya işletim sisteminde bambaşka biçimde ortaya çıkabilir.

| Durum | Yıkım davranışı | Sonuç |
|---|---|---|
| Sanal olmayan temel yıkıcı | Temel işaretçiyle silme geçersizdir | Tanımsız davranış |
| Sanal temel yıkıcı | Dinamik türe göre zincirleme yıkım | Güvenli silme |
| Doğrudan `Derived*` ile silme | `Derived`, ardından `Base` yıkılır | Bu örnekte güvenli |
| `protected` sanal olmayan yıkıcı | Temel işaretçiyle dışarıdan silme engellenir | Kontrollü tasarım |

## Doğru çözüm

Polymorphic olarak kullanılacak temel sınıfın yıkıcısını `virtual` tanımlamak yeterlidir:

```cpp
class Base {
public:
    virtual ~Base() = default;

    virtual void run() = 0;
};

class Derived : public Base {
public:
    ~Derived() override {
        // Derived kaynaklarını temizle
    }

    void run() override {
        // Türe özgü davranış
    }
};
```

`virtual ~Base() = default;`, yıkıcının sanal çağrı mekanizmasına katılmasını sağlarken varsayılan temizleme davranışını derleyiciye bırakır. `override` ise türetilmiş yıkıcının gerçekten sanal zinciri geçersiz kıldığını açıkça gösterir.

Modern C++’ta ham `new` ve `delete` yerine akıllı işaretçiler tercih edilmelidir; ancak akıllı işaretçiler hatalı sınıf tasarımını sihirli biçimde düzeltmez:

```cpp
#include <memory>

std::unique_ptr<Base> object = std::make_unique<Derived>();
```

`unique_ptr<Base>` yok edilirken sonuçta `Base*` üzerinden silme gerçekleştirir. Dolayısıyla `Base` yıkıcısı yine sanal olmalıdır.

## Tasarım kuralı

Bir sınıfta sanal fonksiyon bulunuyorsa veya nesneleri temel sınıf işaretçisi üzerinden silinecekse yıkıcıyı da sanal yapın. Alternatif olarak sınıfın polymorphic silinmesini istemiyorsanız yıkıcıyı `protected` ve sanal olmayan biçimde tanımlayarak yanlış kullanımı derleme aşamasında engelleyin. Kısacası: Çok biçimli davranış kapısını açtıysanız, nesnenin o kapıdan güvenli biçimde çıkmasını da sağlamalısınız.

---
layout: post
title: "C++ RTTI ve Güvenli Tür Dönüşümleri: Nesnenin Gerçek Kimliğini Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - rtti
  - dynamic-cast
  - typeid
  - tür-dönüşümü
  - nesne-yönelimli-programlama
toc: true
image: /img/c-rtti-ve-63.png
---

![c-rtti-ve-63](/img/c-rtti-ve-63.svg)


C++ dünyasında bir nesne her zaman göründüğü şey olmayabilir. Elinizde `Karakter*` türünde bir işaretçi bulunurken, işaret edilen gerçek nesne bir `Buyucu` veya `Savasci` olabilir. Çalışma Zamanı Tür Bilgisi, yani RTTI (Run-Time Type Information), program çalışırken bu gerçek kimliği öğrenmemizi ve kalıtım hiyerarşilerinde güvenli dönüşümler yapmamızı sağlar.
``

## RTTI neden gereklidir?

C++ değişkenlerinin çoğu tür bilgisi derleme zamanında bellidir. Ancak polimorfizm kullanıldığında statik tür ile dinamik tür birbirinden ayrılır:

- **Statik tür:** Değişkenin kaynak kodunda bildirilen türdür.
- **Dinamik tür:** Çalışma anında gerçekten oluşturulmuş nesnenin türüdür.

Bir `Karakter*` değişkeninin statik türü `Karakter*`, gösterdiği nesne `Buyucu` ise dinamik türü `Buyucu` olur. Bunu kabaca şu ilişkiyle gösterebiliriz:

$$T_{statik} \neq T_{dinamik}$$

RTTI özellikle taban sınıf üzerinden yönetilen nesnelerin alt sınıflarını ayırt etmek gerektiğinde devreye girer. Bunun çalışabilmesi için taban sınıfın **polimorfik** olması, yani en az bir sanal (`virtual`) fonksiyon içermesi gerekir. Genellikle sanal yıkıcı tanımlamak yeterlidir.

```cpp
class Karakter {
public:
    virtual ~Karakter() = default;
};

class Buyucu : public Karakter {
public:
    void buyuYap() {
        std::cout << "Ateş topu!\n";
    }
};
```

Sanal yıkıcı hem RTTI kullanımını mümkün kılar hem de nesne taban sınıf işaretçisi üzerinden silindiğinde doğru yıkıcının çağrılmasını sağlar.

## `typeid` ile türü incelemek

`typeid` operatörü bir ifade veya tür hakkında `std::type_info` nesnesi döndürür. İki türün aynı olup olmadığı güvenilir biçimde karşılaştırılabilir:

```cpp
#include <iostream>
#include <typeinfo>

Karakter* karakter = new Buyucu();

if (typeid(*karakter) == typeid(Buyucu)) {
    std::cout << "Bu karakter gerçekten bir büyücü.\n";
}

delete karakter;
```

Burada `typeid(*karakter)` dinamik türü bulur. Buna karşılık `typeid(karakter)` işaretçinin kendi türünü, yani `Karakter*` türünü verir. `type_info::name()` da kullanılabilir; ancak döndürdüğü metnin biçimi derleyiciye bağlıdır ve program mantığı için güvenilir değildir.

## `dynamic_cast` ile güvenli dönüşüm

`dynamic_cast`, polimorfik kalıtım hiyerarşilerinde çalışma zamanı kontrolü yapar. İşaretçi dönüşümü başarısız olursa `nullptr` döndürür:

```cpp
Karakter* karakter = new Buyucu();

if (Buyucu* buyucu = dynamic_cast<Buyucu*>(karakter)) {
    buyucu->buyuYap();
} else {
    std::cout << "Bu karakter büyü yapamaz.\n";
}

 delete karakter;
```

Referanslarda başarısızlık `nullptr` ile bildirilemez. Bu nedenle `dynamic_cast<Buyucu&>` başarısız olduğunda `std::bad_cast` istisnası fırlatır.

## Dönüşüm araçlarının karşılaştırması

| Araç | Kontrol zamanı | Başarısızlık davranışı | Tipik kullanım |
|---|---|---|---|
| `dynamic_cast` | Çalışma zamanı | `nullptr` veya `std::bad_cast` | Güvenli aşağı dönüşüm |
| `static_cast` | Derleme zamanı | Otomatik güvenlik kontrolü yok | Bilinen ve mantıksal dönüşümler |
| `const_cast` | Derleme zamanı | `const` niteliğini değiştirir | Eski API uyumluluğu |
| `reinterpret_cast` | Derleme zamanı | Bit düzeyinde riskli yorumlama | Düşük seviyeli sistem kodu |
| `typeid` | Çalışma zamanı | Tür bilgisi döndürür | Gerçek türü karşılaştırma |

`static_cast` ile aşağı dönüşüm yapılabilir, fakat nesne hedef türde değilse davranış tanımsız olabilir. Başka bir deyişle hız uğruna emniyet kemerini çıkarmış olursunuz.

## Tasarım açısından son notlar

RTTI kullanışlıdır ancak her nesnenin türünü sürekli sorgulamak tasarım kokusuna dönüşebilir. Çoğu durumda sanal fonksiyonlar daha temiz bir çözüm sunar: nesneye “Sen büyücü müsün?” diye sormak yerine doğrudan `eylemYap()` çağrısı yapılabilir.

Yine de eklenti sistemleri, nesne editörleri ve heterojen koleksiyonlar gibi alanlarda RTTI oldukça değerlidir. Kural basittir: Tür gerçekten belirsizse `dynamic_cast`, davranış polimorfik biçimde ifade edilebiliyorsa sanal fonksiyon kullanın. Böylece C++ nesneleri maskelerini çıkarsa bile programınız şaşırmaz.

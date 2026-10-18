---
layout: post
title: "C++ Kalıtım: Sınıflar Arasında Akıllı Bir Miras Sistemi"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - kalıtım
  - nesne yönelimli programlama
  - sınıflar
  - oop
toc: true
image: /img/c-kalitim-siniflar-53.png
---

Bir yazılım projesinde aynı özellikleri tekrar tekrar yazmak hem zaman kaybettirir hem de bakım maliyetini artırır. C++ kalıtım (inheritance) mekanizması, mevcut bir sınıfın veri ve davranışlarını yeni sınıflara aktararak bu tekrarı azaltır. Kısacası kalıtım, kod dünyasındaki “aileden gelen özellikler” sistemidir; fakat hangi özelliğin kime kalacağını erişim belirleyicileri kontrol eder.
``

## Kalıtımın temel mantığı

Özellikleri aktarılan sınıfa **temel sınıf** (base class), bu sınıftan yararlanan yeni sınıfa ise **türetilmiş sınıf** (derived class) denir. Örneğin `Hayvan` genel bir sınıfken `Kedi` ve `Kopek`, onun daha özel türleri olabilir.

Bu ilişki matematiksel olarak bir alt küme yaklaşımıyla düşünülebilir:

$$
Kedi \subset Hayvan
$$

Her kedi bir hayvandır; ancak her hayvan bir kedi değildir. Nesne yönelimli tasarımda buna **is-a**, yani “bir türüdür” ilişkisi denir. Kalıtım kullanılmadan önce iki sınıf arasında gerçekten böyle bir ilişki bulunup bulunmadığı sorgulanmalıdır.

C++ kalıtımının temel sözdizimi şöyledir:

```cpp
class TuretilmisSinif : public TemelSinif {
    // Yeni üyeler ve metotlar
};
```

Buradaki `public`, temel sınıf üyelerinin türetilmiş sınıfa hangi görünürlük kurallarıyla aktarılacağını belirten kalıtım türüdür.

## Basit bir kalıtım örneği

```cpp
#include <iostream>
#include <string>
using namespace std;

class Hayvan {
protected:
    string isim;

public:
    Hayvan(string ad) : isim(ad) {}

    void yemekYe() const {
        cout << isim << " yemek yiyor.\n";
    }
};

class Kedi : public Hayvan {
public:
    Kedi(string ad) : Hayvan(ad) {}

    void miyavla() const {
        cout << isim << " miyavlıyor!\n";
    }
};

int main() {
    Kedi tekir("Tekir");
    tekir.yemekYe();
    tekir.miyavla();
}
```

`Kedi`, `Hayvan` sınıfındaki `yemekYe()` metodunu yeniden yazmadan kullanır. Ayrıca kendisine özgü `miyavla()` davranışını ekler. `isim` üyesinin `protected` olması, ona sınıf dışından doğrudan erişilememesini; ancak türetilmiş sınıfların erişebilmesini sağlar. `Kedi` kurucusu da `Hayvan(ad)` ifadesiyle temel sınıf kurucusunu çağırır.

## Erişim belirleyicileri

Temel sınıftaki üyelerin aktarım biçimi, üyenin görünürlüğüne ve kullanılan kalıtım türüne bağlıdır.

| Temel sınıftaki üye | `public` kalıtım | `protected` kalıtım | `private` kalıtım |
|---|---|---|---|
| `public` | `public` kalır | `protected` olur | `private` olur |
| `protected` | `protected` kalır | `protected` kalır | `private` olur |
| `private` | Doğrudan erişilemez | Doğrudan erişilemez | Doğrudan erişilemez |

`private` üyeler türetilmiş nesnenin içinde yer almaya devam eder; fakat türetilmiş sınıf onları doğrudan kullanamaz. Erişim gerekiyorsa temel sınıfta `public` veya `protected` metotlar sunulmalıdır. Bu yaklaşım kapsüllemeyi korur.

## Metot ezme ve sanal fonksiyonlar

Türetilmiş sınıf, temel sınıftaki bir davranışı değiştirmek isteyebilir. Çalışma zamanında doğru metodun seçilmesi için temel sınıf metodu `virtual`, türetilmiş metot ise `override` ile tanımlanır:

```cpp
class Hayvan {
public:
    virtual void sesCikar() const {
        cout << "Genel hayvan sesi\n";
    }

    virtual ~Hayvan() = default;
};

class Kedi : public Hayvan {
public:
    void sesCikar() const override {
        cout << "Miyav!\n";
    }
};
```

Bu mekanizma **çok biçimliliğin** temelidir. Bir `Hayvan*` işaretçisi gerçekte `Kedi` nesnesini gösteriyorsa `sesCikar()` çağrısı kedinin metodunu çalıştırır. Sanal yıkıcı ise nesne temel sınıf işaretçisi üzerinden silindiğinde kaynakların doğru sırayla serbest bırakılmasını sağlar.

## Ne zaman kullanılmalı?

Kalıtım güçlüdür, ancak her kod tekrarının çözümü değildir. “Bir türüdür” ilişkisi varsa kalıtım; “bir şeye sahiptir” ilişkisi varsa composition tercih edilir.

| İlişki | Uygun teknik | Örnek |
|---|---|---|
| Araba bir araçtır | Kalıtım | `Araba : public Arac` |
| Arabanın motoru vardır | Composition | `Araba` içinde `Motor` |

İyi tasarlanmış kalıtım hiyerarşileri kod tekrarını azaltır, ortak davranışları merkezileştirir ve genişletilebilir sistemler oluşturur. Yine de hiyerarşiyi gereksiz yere derinleştirmemek gerekir; aile ağacı büyüdükçe kodun hangi büyükbabadan hangi özelliği aldığı şaşırtıcı hâle gelebilir!

![c-kalitim-siniflar-53](/img/c-kalitim-siniflar-53.svg)


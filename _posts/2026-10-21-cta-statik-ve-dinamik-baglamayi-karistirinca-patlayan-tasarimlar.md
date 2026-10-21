---
layout: post
title: "C++’ta Statik ve Dinamik Bağlamayı Karıştırınca Patlayan Tasarımlar"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - binding
  - polimorfizm
  - oop
  - tasarım-hataları
  - virtual
toc: true
image: /img/cta-statik-ve-16.png
---

C++’ta bir fonksiyon çağrısının hangi gövdeye gideceği her zaman göründüğü kadar basit değildir. Derleyici bazen kararı derleme zamanında verir, bazen de çalışma zamanındaki gerçek nesne türüne bakar. Statik ve dinamik bağlamayı aynı tasarım içinde bilinçsizce karıştırmak; yanlış fonksiyonların çağrılmasına, kaynak sızıntılarına ve “Ama bu sınıfı ezmiştim!” şaşkınlığına yol açabilir.


![cta-statik-ve-16](/img/cta-statik-ve-16.svg)

``

## Bağlama tam olarak nedir?

Bağlama, bir çağrı ifadesinin çalıştırılacak fonksiyon gövdesiyle eşleştirilmesidir. Statik bağlamada karar, değişkenin derleme zamanındaki türüne göre verilir. Dinamik bağlamada ise `virtual` mekanizması üzerinden nesnenin çalışma zamanındaki gerçek türü kullanılır.

Bunu kabaca şöyle düşünebiliriz:

$$
secim = f(T_{statik}, T_{dinamik}, virtual)
$$

Fonksiyon sanal değilse çoğunlukla $T_{statik}$ belirleyicidir. Sanal fonksiyon çağrısında ise uygun koşullarda $T_{dinamik}$ devreye girer.

| Özellik | Statik bağlama | Dinamik bağlama |
|---|---|---|
| Karar zamanı | Derleme zamanı | Çalışma zamanı |
| Temel ölçüt | İfadenin statik türü | Nesnenin gerçek türü |
| Tipik araçlar | Overload, normal metot | `virtual`, `override` |
| Maliyet | Genellikle doğrudan çağrı | Genellikle sanal tablo erişimi |
| Yaygın risk | Yanlış overload seçimi | Hatalı yaşam döngüsü tasarımı |

## Hata 1: Sanal olmayan yıkıcı

Polimorfik bir taban sınıfın yıkıcısını sanal yapmamak, en tehlikeli karışıklıklardan biridir:

```cpp
#include <iostream>

class Kaynak {
public:
    ~Kaynak() { std::cout << "Kaynak kapandı\n"; }
};

class Dosya : public Kaynak {
public:
    ~Dosya() { std::cout << "Dosya kapandı\n"; }
};

int main() {
    Kaynak* kaynak = new Dosya;
    delete kaynak; // Tanımsız davranış!
}
```

`delete` işlemi taban işaretçisi üzerinden yapıldığı için yıkıcının dinamik davranması gerekir. Çözüm basittir:

```cpp
virtual ~Kaynak() = default;
```

Bir sınıfta sanal metot varsa yıkıcının da genellikle sanal olması beklenir.

## Hata 2: Varsayılan argümanların sanal olduğunu sanmak

Sanal fonksiyonun gövdesi dinamik, varsayılan argümanı ise statik olarak seçilir:

```cpp
#include <iostream>

struct Bildirim {
    virtual void gonder(int oncelik = 1) {
        std::cout << oncelik << '\n';
    }
};

struct Alarm : Bildirim {
    void gonder(int oncelik = 9) override {
        std::cout << oncelik << '\n';
    }
};

int main() {
    Alarm alarm;
    Bildirim& b = alarm;
    b.gonder(); // Alarm::gonder çalışır, fakat argüman 1 olur.
}
```

Ortaya hibrit bir sonuç çıkar: gövde alt sınıftan, değer taban sınıftan gelir. Varsayılan değeri tek yerde tanımlamak veya parametresiz ayrı bir sanal olmayan arayüz kullanmak daha güvenlidir.

## Hata 3: Kurucuda sanal çağrı

Kurucu sırasında nesnenin alt sınıf bölümü henüz hazır değildir. Bu nedenle taban kurucusundan yapılan sanal çağrı, alt sınıf sürümüne gitmez:

```cpp
struct Motor {
    Motor() { baslat(); }
    virtual void baslat() { /* taban davranışı */ }
};

struct TurboMotor : Motor {
    void baslat() override { /* turbo henüz hazır olmayabilir */ }
};
```

Nesneyi oluşturduktan sonra çağrılan bir `initialize()` metodu veya fabrika fonksiyonu kullanmak daha açık bir yaşam döngüsü sağlar.

## Hata 4: Nesne dilimleme

Alt sınıf nesnesini değer olarak taban türe kopyalamak dinamik tür bilgisini keser:

```cpp
void calistir(Motor motor) { // Kopyalama ve dilimleme
    motor.baslat();
}
```

Bunun yerine `Motor&`, `Motor*` veya uygun bir akıllı işaretçi kullanılmalıdır.

## Sağlam tasarım kontrol listesi

- Ezilen her metoda `override` ekleyin.
- Polimorfik tabanlarda sanal yıkıcı kullanın.
- Sanal metotlarda farklı varsayılan argümanlardan kaçının.
- Kurucu ve yıkıcılarda sanal dispatch’e güvenmeyin.
- Polimorfik nesneleri değer yerine referans veya işaretçiyle taşıyın.
- Overload ile override kavramlarını aynı şey sanmayın.

Kısacası `virtual`, tasarıma sihir serpiştiren bir kelime değildir. Hangi kararın derleyiciye, hangisinin çalışma zamanına bırakıldığını açıkça belirlemek gerekir; aksi hâlde kod derlenir, çalışır ve tam en kötü anda yanlış şeyi yapar.

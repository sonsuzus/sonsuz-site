---
layout: post
title: "C++ Sınıflar ve Nesnelere Giriş: Kodun Lego Parçaları"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - sınıflar
  - nesneler
  - oop
  - erişim belirleyiciler
  - programlama
toc: true
image: /img/c-siniflar-ve-18.png
---

Bir oyundaki karakterleri düşün: Her karakterin adı, canı ve saldırı gücü vardır; ayrıca saldırabilir veya kendini tanıtabilir. Bütün bunları ayrı değişkenler ve fonksiyonlarla yönetmek mümkün olsa da karakter sayısı arttıkça kod kısa sürede spagettiye dönüşür. C++ sınıfları, ilişkili verileri ve davranışları tek bir anlamlı yapı altında toplayarak bu karmaşayı önler.

``

## Sınıf nedir?

**Sınıf**, üretilecek nesnelerin hangi özelliklere ve davranışlara sahip olacağını belirleyen bir şablondur. **Nesne** ise bu şablondan oluşturulan somut örnektir. Sınıfı bir kurabiye kalıbına, nesneleri de o kalıpla hazırlanmış kurabiyelere benzetebiliriz. Kalıp aynı olsa bile her kurabiyenin süslemesi, yani tuttuğu veriler farklı olabilir.

Bunu basitçe şöyle modelleyebiliriz:

$$Nesne = Veri + Davranış$$

Bir sınıftan $n$ nesne üretildiğinde ortak davranışlar sınıf tarafından tanımlanır, fakat her nesne kendi durumunu taşır:

$$Toplam\ Durum = n \times Nesne\ Verisi$$

| Kavram | Görevi | Örnek |
|---|---|---|
| Sınıf | Şablonu tanımlar | `Karakter` |
| Nesne | Şablonun somut örneğidir | `savasci` |
| Özellik | Nesnenin durumunu saklar | `can` |
| Metot | Nesnenin davranışını tanımlar | `saldir()` |

## İlk sınıfımızı yazalım

Aşağıdaki sınıf, bir oyun karakterinin adını ve can puanını saklar. Kurucu fonksiyon başlangıç değerlerini alırken `bilgiGoster()` metodu nesnenin mevcut durumunu ekrana yazar.

```cpp
#include <iostream>
#include <string>
using namespace std;

class Karakter {
private:
    string ad;
    int can;

public:
    Karakter(string karakterAdi, int baslangicCani) {
        ad = karakterAdi;
        can = baslangicCani;
    }

    void hasarAl(int miktar) {
        if (miktar > 0) {
            can -= miktar;
            if (can < 0) can = 0;
        }
    }

    void bilgiGoster() const {
        cout << ad << " - Can: " << can << '\n';
    }
};
```

`Karakter` ile aynı adı taşıyan ve dönüş tipi bulunmayan fonksiyon bir **constructor**, yani kurucudur. Nesne oluşturulduğu anda otomatik çalışır. `bilgiGoster()` sonundaki `const` ise metodun nesnenin özelliklerini değiştirmeyeceğini bildirir.

## Erişim belirleyiciler

C++, sınıf üyelerine kimlerin erişebileceğini üç temel belirleyiciyle kontrol eder:

| Belirleyici | Sınıf içinden | Türetilmiş sınıftan | Dışarıdan |
|---|:---:|:---:|:---:|
| `public` | Evet | Evet | Evet |
| `protected` | Evet | Evet | Hayır |
| `private` | Evet | Hayır | Hayır |

Özellikleri çoğunlukla `private` tutmak iyi bir alışkanlıktır. Böylece dış kod `can` değerini yanlışlıkla `-9000` yapamaz; değişiklikler doğrulama yapan metotlardan geçirilir. Bu yaklaşım **kapsülleme** olarak adlandırılır. Sınıfın iç ayrıntıları saklanırken güvenli bir `public` arayüz sunulur.

## Nesne nasıl üretilir?

Sınıf tek başına çalışan bir karakter oluşturmaz. Şablonu kullanarak nesne üretmemiz gerekir:

```cpp
int main() {
    Karakter savasci("Ada", 100);
    Karakter buyucu("Linus", 80);

    savasci.hasarAl(25);
    savasci.bilgiGoster(); // Ada - Can: 75
    buyucu.bilgiGoster();  // Linus - Can: 80
}
```

Buradaki `savasci` ve `buyucu`, aynı sınıftan üretilmiş iki bağımsız nesnedir. `savasci` hasar aldığında `buyucu`nun canı değişmez. Nokta operatörü (`.`), nesnenin erişilebilir üyelerini kullanmamızı sağlar.

Nesneler dinamik olarak da oluşturulabilir:

```cpp
Karakter* okcu = new Karakter("Bjarne", 90);
okcu->bilgiGoster();
delete okcu;
```

İşaretçi üzerinden üyeye erişirken `->` kullanılır. `new` ile ayrılan bellek `delete` ile serbest bırakılmalıdır. Modern C++ projelerinde bellek sızıntılarını önlemek için çoğunlukla akıllı işaretçiler tercih edilir.

## Neden sınıflar?

Sınıflar kodu düzenler, tekrarları azaltır ve gerçek dünyadaki kavramları yazılıma taşımayı kolaylaştırır. `Araba`, `BankaHesabi` veya `Robot` gibi modeller; verileriyle davranışlarını aynı çatı altında toplar. Kısacası sınıf planı çizer, nesne o planı hayata geçirir. Bu ayrımı kavradığınızda kalıtım, çok biçimlilik ve soyutlama gibi ileri nesne yönelimli programlama konuları çok daha anlaşılır hâle gelir.

![c-siniflar-ve-18](/img/c-siniflar-ve-18.svg)


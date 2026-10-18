---
layout: post
title: "C++ Fonksiyon Aşırı Yükleme: Tek İsim, Birden Fazla Yetenek"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - fonksiyonlar
  - function-overloading
  - oop
  - programlama
toc: true
image: /img/c-fonksiyon-asiri-87.png
---

Bir hesap makinesindeki “topla” düğmesinin tam sayılar, ondalıklı sayılar ve hatta metinler için farklı davranabildiğini düşünün. C++ fonksiyon aşırı yükleme sayesinde benzer işlemleri yapan fonksiyonlara aynı ismi verebilir, kullanım sırasında hangi sürümün çalışacağını derleyiciye bırakabiliriz. Böylece `toplaTamSayilari`, `toplaOndalikliSayilari` gibi isimler üretmek yerine daha sade ve anlaşılır bir arayüz oluştururuz.

``

## Fonksiyon aşırı yükleme nedir?

Function overloading, aynı kapsam içerisinde aynı isimli fakat farklı parametre listelerine sahip birden fazla fonksiyon tanımlamaktır. Parametre listesindeki tür, sayı veya sıralama değiştiğinde yeni bir overload meydana gelir.

```cpp
#include <iostream>
#include <string>

int topla(int a, int b) {
    return a + b;
}

double topla(double a, double b) {
    return a + b;
}

std::string topla(const std::string& a, const std::string& b) {
    return a + b;
}

int main() {
    std::cout << topla(4, 7) << '\n';
    std::cout << topla(2.5, 1.8) << '\n';
    std::cout << topla(std::string("Merhaba "), std::string("C++"));
}
```

Burada `topla(4, 7)` çağrısı `int` sürümünü, ondalıklı argümanlar `double` sürümünü seçer. Son sürüm ise iki metni birleştirir. `const std::string&` kullanılması, metinlerin gereksiz yere kopyalanmasını önler.

## Derleyici doğru fonksiyonu nasıl seçer?

Derleyici, çağrıdaki argümanları mevcut adayların parametreleriyle karşılaştırır. Bu sürece **overload resolution** denir. Basitleştirilmiş biçimde her aday için bir dönüşüm maliyeti düşünülebilir:

$$S = C_1 + C_2 + \cdots + C_n$$

Burada $C_i$, ilgili argümanın parametre türüne dönüştürülme maliyetidir. En düşük $S$ değerine sahip aday seçilir. Tam eşleşme genellikle standart tür dönüşümünden, standart dönüşüm de kullanıcı tanımlı dönüşümden daha güçlüdür.

| Eşleşme türü | Örnek | Tercih düzeyi |
|---|---|---|
| Tam eşleşme | `int` → `int` | En yüksek |
| Terfi | `char` → `int` | Yüksek |
| Standart dönüşüm | `int` → `double` | Orta |
| Kullanıcı tanımlı dönüşüm | Sınıf dönüşümü | Daha düşük |

![c-fonksiyon-asiri-87](/img/c-fonksiyon-asiri-87.svg)


## Neler overload oluşturur?

Aşağıdaki fonksiyonlar geçerli biçimde aşırı yüklenebilir:

```cpp
void yazdir(int deger);
void yazdir(double deger);
void yazdir(int deger, int tekrar);
void yazdir(const std::string& metin);
```

Birincisi ve ikincisi parametre türüyle, üçüncüsü parametre sayısıyla ayrılır. Ancak yalnızca dönüş türünü değiştirmek yeterli değildir:

```cpp
int hesapla(int x);
// double hesapla(int x); // Hata: Parametre listesi aynı!
```

Çağıran kod yalnızca `hesapla(5)` yazdığında hangi dönüş türünü istediğini derleyici kesin olarak anlayamaz. Bu nedenle dönüş türü, fonksiyon aşırı yükleme imzasının ayırt edici parçası değildir.

## Belirsizlik tuzağı

Dönüşümler eşit derecede uygun olduğunda derleyici seçim yapamaz:

```cpp
void goster(long deger) {}
void goster(double deger) {}

int main() {
    // goster(10); // Belirsiz çağrı
    goster(10L);   // long sürümü
    goster(10.0);  // double sürümü
}
```

`10`, `int` türündedir ve hem `long` hem de `double` türüne dönüştürülebilir. `L` ve `.0` ekleriyle niyet açıkça belirtilir. Benzer sorunlar varsayılan parametrelerle de oluşabilir.

| Yaklaşım | Avantaj | Risk |
|---|---|---|
| Farklı fonksiyon adları | Seçim tamamen açıktır | Gereksiz isim kalabalığı |
| Overloading | Temiz ve doğal API | Belirsiz çağrı ihtimali |
| Şablonlar | Çok sayıda türü destekler | Hata mesajları karmaşıklaşabilir |

## Ne zaman kullanmalıyız?

Aşırı yüklenen fonksiyonlar kavramsal olarak aynı işi yapmalıdır. `yazdir`, `hesapla` veya `ekle` gibi işlemler bunun için uygundur. Bir overload dosya silerken diğeri matematiksel hesap yapıyorsa ortak isim geliştiriciyi şaşırtır.

Kısacası function overloading, C++ arayüzlerini esnek ve okunabilir hâle getirir. Parametre listelerini belirgin tuttuğunuz, örtük dönüşümleri sınırladığınız ve her sürüme aynı kavramsal sorumluluğu verdiğiniz sürece tek bir isim gerçekten birçok yeteneği zarifçe taşıyabilir.

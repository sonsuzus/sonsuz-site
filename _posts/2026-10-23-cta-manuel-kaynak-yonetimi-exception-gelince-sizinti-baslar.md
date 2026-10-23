---
layout: post
title: "C++’ta Manuel Kaynak Yönetimi: Exception Gelince Sızıntı Başlar"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - raii
  - exception
  - bellek yönetimi
  - akıllı işaretçiler
toc: true
image: /img/cta-manuel-kaynak-67.png
---

C++ geliştirirken `new` ile bellek ayırıp işimiz bitince `delete` çağırmak ilk bakışta oldukça düzenli görünür. Fakat kodun ortasında bir istisna fırlatıldığında kontrol akışı planladığımız yolu izlemez. Temizlik satırına ulaşılamaz ve ayrılan kaynak sahipsiz kalır. Program çalışmaya devam etse bile bellekte küçük bir hayalet dolaşmaya başlar.

``

## Sorun yalnızca `delete` unutmak değildir

Manuel kaynak yönetiminde genellikle kaynağın yaşam süresini zihnimizde takip ederiz: kaynağı edin, kullan ve serbest bırak. İdeal akış şöyle düşünülebilir:

$$
T_{yaşam} = T_{serbest\ bırakma} - T_{edinme}
$$

Ancak bir exception oluştuğunda fonksiyon normal dönüş noktasına ulaşmaz. C++ çalışma zamanı stack unwinding işlemini başlatır; yani çağrı yığınındaki yerel nesneler geriye doğru yok edilir. Ham işaretçinin kendisi yok olur fakat işaret ettiği dinamik nesne otomatik olarak silinmez.

```cpp
#include <stdexcept>

void veriyiIsle() {
    int* sayilar = new int[1000];

    sayilar[0] = 42;
    throw std::runtime_error("Dosya okunamadı");

    delete[] sayilar; // Bu satıra hiçbir zaman ulaşılamaz.
}
```

Buradaki sızıntının matematiksel özeti basittir:

$$
Ayrılan\ Kaynaklar - Serbest\ Bırakılan\ Kaynaklar > 0
$$

Fonksiyon her çağrıldığında yeni bir blok ayrılır. Hata tekrarlanırsa kayıp miktarı birikir. Tek çağrıdaki sızıntı $M$ bayt ve hatalı çağrı sayısı $n$ ise toplam kayıp yaklaşık $n \times M$ olur.

## `try-catch` ile temizlik yeterli mi?

Kaynağı `catch` bloğunda temizlemek mümkündür, fakat çözüm hızla kırılganlaşır:

```cpp
void veriyiIsle() {
    int* sayilar = new int[1000];

    try {
        riskliIslem(sayilar);
    } catch (...) {
        delete[] sayilar;
        throw; // Orijinal exception yeniden gönderilir.
    }

    delete[] sayilar;
}
```

Bu kod sızıntıyı önleyebilir; ancak hem normal hem de hatalı yol için aynı temizlik işlemi yazılmıştır. Fonksiyona dosya tanıtıcısı, kilit veya ikinci bir bellek bloğu eklendiğinde olası çıkış yolları çoğalır. Ayrıca yanlış sırada temizlik yapmak ya da bir kaynağı iki kez serbest bırakmak mümkündür.

| Yaklaşım | Exception güvenliği | Bakım maliyeti | Risk |
|---|---:|---:|---|
| Ham işaretçi ve manuel `delete` | Düşük | Yüksek | Sızıntı, çift silme |
| `try-catch` ile manuel temizlik | Orta | Yüksek | Tekrarlı ve kırılgan kod |
| RAII nesnesi | Yüksek | Düşük | Sahiplik daha nettir |
| Akıllı işaretçi | Yüksek | Düşük | Yanlış işaretçi türü seçimi |

![cta-manuel-kaynak-67](/img/cta-manuel-kaynak-67.svg)


## Güvenli çözüm: RAII

RAII, kaynağın yaşam süresini bir nesnenin yaşam süresine bağlar. Kullanıcı manuel olarak yıkıcı çağırmaz; kapsam sona erdiğinde yıkıcı dil tarafından otomatik çağrılır. Exception oluşması da bu davranışı bozmaz.

```cpp
#include <memory>
#include <stdexcept>

void veriyiIsle() {
    auto sayilar = std::make_unique<int[]>(1000);
    sayilar[0] = 42;

    throw std::runtime_error("İşlem başarısız");
}
```

`std::unique_ptr`, dizinin tek sahibidir. Stack unwinding sırasında `sayilar` nesnesinin yıkıcısı çalışır ve dinamik dizi serbest bırakılır. Açık bir `delete[]` satırına ihtiyaç kalmaz.

Çoğu durumda dinamik dizi için daha doğal seçenek `std::vector` kullanmaktır:

```cpp
#include <vector>

void veriyiIsle() {
    std::vector<int> sayilar(1000);
    sayilar.at(0) = 42;
    riskliIslem(sayilar.data());
}
```

RAII yalnızca bellek için değildir. Dosyalar, mutex kilitleri, soketler ve veritabanı bağlantıları da aynı ilkeyle kapsüllenebilir. Temel kural şudur: Kaynağı edinen nesne, onu bırakmaktan da sorumlu olmalıdır. Böylece exception geldiğinde temizlik bir dilek değil, kapsam mekanizmasının garantisi olur.

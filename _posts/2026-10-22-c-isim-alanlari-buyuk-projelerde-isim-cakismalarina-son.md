---
layout: post
title: "C++ İsim Alanları: Büyük Projelerde İsim Çakışmalarına Son"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - namespace
  - isim alanları
  - yazılım mimarisi
  - modüler programlama
toc: true
image: /img/c-isim-alanlari-19.png
---

![c-isim-alanlari-19](/img/c-isim-alanlari-19.svg)


Bir projede yalnızca birkaç değişken ve sınıf varken isim bulmak kolaydır. Ancak kod tabanı büyüdükçe farklı geliştiricilerin aynı `Logger`, `Config` veya `User` adını kullanması kaçınılmaz hâle gelir. C++ isim alanları, yani `namespace` yapıları, bu isimleri mantıksal gruplara ayırarak derleyiciye hangi varlığı kastettiğimizi söyler. Kısacası namespace, kod dünyasının mahalle adresidir: Aynı isimli iki kişi olabilir, yeter ki farklı adreslerde yaşasın!

``

## İsim çakışması neden oluşur?

C++ dilinde bir ismin hangi bölgeden erişilebilir olduğunu belirleyen kurallara **kapsam**, yani scope denir. Global kapsamda tanımlanan isimler projenin birçok noktasından görülebildiği için çakışma olasılığı yükselir. Bir projede birbirinden bağımsız $n$ bileşen ve her bileşende ortalama $k$ genel isim bulunduğunu düşünelim. Karşılaştırılabilecek isim çiftlerinin sayısı yaklaşık olarak şöyledir:

$$
P = \frac{(nk)(nk-1)}{2}
$$

Bu ifade doğrudan kesin çakışma sayısını vermez; proje büyüdükçe riskin neden hızla arttığını gösterir. İsimleri namespace gruplarına bölmek, karşılaştırma alanını küçültür.

| Yaklaşım | Kullanım örneği | Çakışma riski | Okunabilirlik |
|---|---|---:|---|
| Global isim | `Logger` | Yüksek | Orta |
| Namespace içindeki isim | `app::Logger` | Düşük | Yüksek |
| İç içe namespace | `company::app::Logger` | Çok düşük | Yüksek |

## Temel namespace kullanımı

Bir isim alanı `namespace` anahtar sözcüğüyle tanımlanır. Aynı sınıf adı farklı alanlarda güvenle bulunabilir:

```cpp
#include <iostream>
#include <string>

namespace Database {
    class Connection {
    public:
        void open() const {
            std::cout << "Veritabanı bağlantısı açıldı.\n";
        }
    };
}

namespace Network {
    class Connection {
    public:
        void open() const {
            std::cout << "Ağ bağlantısı açıldı.\n";
        }
    };
}

int main() {
    Database::Connection database;
    Network::Connection network;

    database.open();
    network.open();
}
```

Buradaki `::` operatörüne **kapsam çözümleme operatörü** denir. `Database::Connection`, derleyiciye yalnızca `Connection` sınıfını değil, sınıfın tam adresini verir.

## `using` kullanırken dikkat

Uzun isimleri sürekli yazmamak için `using` bildirimi kullanılabilir:

```cpp
using Database::Connection;

int main() {
    Connection connection;
    connection.open();
}
```

Bu yöntem yalnızca ihtiyaç duyulan ismi mevcut kapsama taşır. Buna karşılık aşağıdaki kullanım özellikle başlık dosyalarında risklidir:

```cpp
using namespace std;
```

Bu ifade `std` içindeki çok sayıda ismi görünür yapar. Projede başka bir `count`, `distance` veya `begin` tanımı varsa belirsizlik oluşabilir.

| Yöntem | Avantaj | Dezavantaj | Öneri |
|---|---|---|---|
| `std::string` | Açık ve güvenli | Biraz uzun | Genel olarak tercih edilir |
| `using std::string` | Kısa ve kontrollü | Yerel çakışma olabilir | Dar kapsamda kullanılabilir |
| `using namespace std` | Çok kısa | Pek çok ismi içeri taşır | Başlık dosyalarında kaçınılmalıdır |

## İç içe ve anonim namespace

Modern C++ ile iç içe isim alanları daha kısa yazılabilir:

```cpp
namespace company::project::logging {
    void write(const std::string& message) {
        std::cout << message << '\n';
    }
}
```

Fonksiyonun tam adı `company::project::logging::write` olur. Bu yapı şirket, ürün ve modül katmanlarını ifade etmek için kullanışlıdır.

Anonim namespace ise bir kaynak dosyasındaki isimleri yalnızca o çeviri birimine özel tutar:

```cpp
namespace {
    int calculateSecretValue() {
        return 42;
    }
}
```

Bu fonksiyona başka bir `.cpp` dosyasından erişilemez. Böylece uygulama içi yardımcı fonksiyonlar dış dünyaya sızmaz.

## Pratik kurallar

- Namespace adlarını modül sınırlarına göre seçin.
- Başlık dosyalarında `using namespace` kullanmayın.
- Çok genel `Utils` veya `Common` adları yerine anlamlı alanlar oluşturun.
- Genel API’lerde kısa ama ayırt edici isimler tercih edin.
- Aynı namespace’i birden fazla dosyada genişletebileceğinizi unutmayın.

Doğru namespace tasarımı yalnızca derleyici hatalarını önlemez; kodun sahibini, amacını ve mimari konumunu da anlatır. Büyük bir C++ projesinde düzen, iyi seçilmiş isimlerle; güvenlik ise o isimlere doğru adresleri vermekle başlar.

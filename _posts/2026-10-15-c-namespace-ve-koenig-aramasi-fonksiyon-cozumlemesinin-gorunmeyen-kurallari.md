---
layout: post
title: "C++ Namespace ve Koenig Araması: Fonksiyon Çözümlemesinin Görünmeyen Kuralları"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - namespace
  - adl
  - koenig araması
  - fonksiyon çözümleme
toc: true
image: /img/c-namespace-ve-35.png
---

C++’ta bir fonksiyon çağrısının hangi bildirime bağlanacağı her zaman kodda gördüğümüz isimle sınırlı değildir. `foo(x)` gibi masum bir çağrı; normal isim aramasını, ad alanlarını, aşırı yük çözümlemesini ve Koenig araması olarak da bilinen ADL mekanizmasını harekete geçirir. Bu görünmez süreç doğru kullanıldığında genişletilebilir API’ler oluşturur, yanlış anlaşıldığında ise derleyicinin neden “alakasız” bir fonksiyonu seçtiğini düşündüren hatalara yol açar.


![c-namespace-ve-35](/img/c-namespace-ve-35.svg)

``

## Fonksiyon çözümlemesinin iki perdesi

Niteliksiz bir `f(x)` çağrısında adaylar temel olarak iki kaynaktan gelir:

1. **Normal niteliksiz isim araması:** Çağrının bulunduğu kapsam, üst kapsamlar ve ilgili `using` bildirimleri incelenir.
2. **Argument-Dependent Lookup (ADL):** Argüman türleriyle ilişkili namespace ve sınıflardaki fonksiyonlar aranır.

Bunu kavramsal olarak şöyle gösterebiliriz:

$$
Adaylar = Normal\ Arama \cup ADL
$$

Ardından overload resolution, uygulanabilir adaylar arasından dönüşümler bakımından en iyi olanı seçer. Yani ADL doğrudan kazananı belirlemez; yarışa yeni fonksiyonlar ekler.

| Özellik | Normal arama | ADL / Koenig araması |
|---|---|---|
| Başlangıç noktası | Çağrının yazıldığı kapsam | Argümanların türleri |
| `using` etkisi | Adayları görünür yapabilir | İlişkili namespace esas alınır |
| Nitelikli çağrıda çalışır mı? | Evet | Genellikle hayır |
| Temel amacı | Sözcüksel isim bulma | Türle birlikte tanımlanan işlemleri bulma |

## ADL’nin sahneye çıkışı

Aşağıdaki fonksiyon çağrı noktasında açıkça içeri alınmamıştır:

```cpp
#include <iostream>

namespace grafik {
    struct Nokta {
        int x;
        int y;
    };

    void yazdir(const Nokta& n) {
        std::cout << n.x << ", " << n.y << '\n';
    }
}

int main() {
    grafik::Nokta n{3, 7};
    yazdir(n); // ADL, grafik::yazdir fonksiyonunu bulur.
}
```

`Nokta`, `grafik` namespace’ine ait olduğu için bu namespace çağrıyla ilişkilendirilir. Argüman `int` olsaydı kullanıcı tanımlı ilişkili bir namespace bulunmayacağından aynı numara işe yaramazdı.

Çağrıyı `::yazdir(n)` biçiminde nitelendirmek ise yalnızca global kapsamdaki ismi istemek anlamına gelir ve ADL katkısını ortadan kaldırır. Bu ayrım, hata ayıklarken oldukça değerlidir.

## Gizli arkadaşlar: Kontrollü görünürlük

ADL’nin en güçlü kullanım alanlarından biri sınıf içinde tanımlanan `friend` fonksiyonlardır:

```cpp
#include <compare>

namespace matematik {
    class Kesir {
        int pay;
        int payda;

    public:
        Kesir(int p, int q) : pay(p), payda(q) {}

        friend bool operator==(const Kesir& a, const Kesir& b) {
            return a.pay * b.payda == b.pay * a.payda;
        }
    };
}
```

Bu operatör normal namespace aramasında kolayca görünmez; fakat `Kesir` argümanlarıyla yapılan `a == b` ifadesinde ADL tarafından bulunur. Böylece namespace yüzeyi gereksiz fonksiyonlarla kirletilmeden türe ait işlem sunulur. Buna **hidden friend idiomu** denir.

## `swap` kalıbı neden önemlidir?

Genel kodda yalnızca `std::swap(a, b)` yazmak, kullanıcı türünün kendi optimize edilmiş `swap` fonksiyonunu engelleyebilir. Geleneksel çözüm şöyledir:

```cpp
using std::swap;
swap(a, b);
```

İlk satır standart sürümü yedek aday yapar. İkinci satır niteliksiz çağrı olduğu için ADL’ye izin verir. Türün namespace’inde daha uygun bir `swap` varsa overload resolution onu seçer; yoksa `std::swap` kullanılır.

| Yazım | ADL | Sonuç |
|---|---:|---|
| `std::swap(a, b)` | Hayır | Yalnızca standart adaylar |
| `swap(a, b)` | Evet | Yerel adaylar ve ADL adayları |
| `using std::swap; swap(a, b);` | Evet | Güvenli geri dönüş ve özelleştirme |

## Sürprizlerden korunma rehberi

Aynı isimli fonksiyonları geniş namespace’lere gelişigüzel yerleştirmek beklenmeyen belirsizlikler oluşturabilir. Özellikle bir çağrının argüman türü değiştiğinde ilişkili namespace kümesi de değişebilir. Şablonlarda bu etki daha belirgindir; bağımlı çağrıların bazı adayları ancak şablon örneklendiğinde belirlenir.

Kütüphane tasarlarken işlemleri ilgili türle aynı namespace’e koymak, global kapsamı kirletmemek ve özelleştirilebilir işlemlerde niteliksiz çağrı kullanmak iyi bir dengedir. Bir çağrının gizemli davrandığı durumlarda ise şu soruyu sorun: “Bu fonksiyon normal aramayla mı geldi, yoksa argümanlardan biri ADL için gizli bir kapı mı açtı?”

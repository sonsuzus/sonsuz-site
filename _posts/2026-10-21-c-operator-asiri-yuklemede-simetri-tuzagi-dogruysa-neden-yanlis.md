---
layout: post
title: "C++ Operatör Aşırı Yüklemede Simetri Tuzağı: == Doğruysa != Neden Yanlış?"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - operatör aşırı yükleme
  - eşitlik
  - simetri
  - modern c++
  - api tasarımı
toc: true
image: /img/c-operator-asiri-45.png
---

C++’ta operatör aşırı yükleme, kullanıcı tanımlı türlerin yerleşik türler gibi doğal görünmesini sağlar. Ancak doğal görünen her davranış doğal olmayabilir! Özellikle `==` ile `!=` farklı mantıklarla uygulanırsa veya operand sırası sonucu değiştirirse, kod derlenmesine rağmen kullanıcıyı sessizce yanıltan bir API ortaya çıkar.

![c-operator-asiri-45](/img/c-operator-asiri-45.svg)

``
## Eşitlikten beklediğimiz matematiksel sözleşme

Bir eşitlik operatörü yalnızca `bool` döndüren sıradan bir fonksiyon değildir. Kullanıcılar ondan bazı matematiksel özellikler bekler. Örneğin simetri şu şekilde ifade edilir:

$$a == b \iff b == a$$

Benzer biçimde eşitsizliğin, eşitliğin mantıksal değili olması beklenir:

$$a \neq b \iff \neg(a = b)$$

C++ derleyicisi her sürümde ve her tasarımda bu sözleşmeleri sizin yerinize doğrulamaz. Operatörler bağımsız tanımlandığında aşağıdaki tablo gibi şaşırtıcı sonuçlar üretilebilir:

| İfade | Kullanıcının beklentisi | Hatalı tasarımda sonuç |
|---|---|---|
| `a == b` | `true` | `true` |
| `a != b` | `false` | `true` |
| `b == a` | `true` | Derleme hatası veya `false` |
| `!(a == b)` | `false` | `false` |

Buradaki sorun sentaks değil, anlam sözleşmesinin bozulmasıdır.

## Klasik `==` ve `!=` tutarsızlığı

Aşağıdaki sınıf, kullanıcı adlarını büyük-küçük harfe duyarsız karşılaştırmak istiyor; fakat iki operatör farklı kurallara sahip:

```cpp
#include <algorithm>
#include <cctype>
#include <string>

class Username {
public:
    explicit Username(std::string value) : value_(std::move(value)) {}

    bool operator==(const Username& other) const {
        return normalize(value_) == normalize(other.value_);
    }

    bool operator!=(const Username& other) const {
        return value_ != other.value_; // Hata: farklı karşılaştırma kuralı
    }

private:
    std::string value_;

    static std::string normalize(std::string text) {
        std::transform(text.begin(), text.end(), text.begin(),
            [](unsigned char c) { return std::tolower(c); });
        return text;
    }
};
```

`Username("Ada") == Username("ada")` ifadesi `true` iken `!=` ifadesi de `true` olur. İki operatör tek başına makul görünse de birlikte mantıksal bir çelişki oluşturur. Bu tür hata; testlerde, koşullu dallanmalarda ve arama algoritmalarında hayalet avına dönüşebilir.

C++17 ve öncesini hedefleyen güvenli yaklaşım, `!=` operatörünü doğrudan `==` üzerinden tanımlamaktır:

```cpp
bool operator!=(const Username& other) const {
    return !(*this == other);
}
```

Böylece eşitlik kuralı yalnızca bir yerde tutulur. C++20’de ise uygun bir `operator==` bulunduğunda `a != b` ifadesi yeniden yazma kurallarıyla `!(a == b)` üzerinden çözümlenebilir. Gereksiz yere ayrı bir `!=` yazmamak, tutarsızlık riskini azaltır.

## Operand sırası da önemlidir

Üye operatör tanımları sol operandı sınıf türüne bağlar:

```cpp
class Distance {
public:
    explicit Distance(int meters) : meters_(meters) {}

    bool operator==(int meters) const {
        return meters_ == meters;
    }

private:
    int meters_;
};
```

Bu tasarımda `distance == 10` çalışırken, dil sürümüne ve uygun adaylara bağlı olarak `10 == distance` beklenmedik biçimde başarısız olabilir. Simetrik dönüşüm ve karşılaştırmalar için gizli arkadaş fonksiyon yaklaşımı daha açık bir çözümdür:

```cpp
class Distance {
public:
    explicit Distance(int meters) : meters_(meters) {}

    friend bool operator==(const Distance& left, const Distance& right) {
        return left.meters_ == right.meters_;
    }

private:
    int meters_;
};
```

`explicit` kurucuyla birlikte bu sürüm, hangi dönüşümlerin kabul edildiğini de netleştirir; sürprizli örtük dönüşümlere kapı açmaz.

## Sağlam tasarım için kontrol listesi

- `!=` sonucunu bağımsız mantıkla hesaplamayın; `==` sonucunu tersine çevirin veya C++20 yeniden yazımını kullanın.
- `a == b` ve `b == a` ifadelerini ayrı ayrı test edin.
- Büyük-küçük harf, tolerans ve normalizasyon gibi kuralları tek fonksiyonda merkezileştirin.
- Örtük dönüşümlerin iki operand yönünde aynı sonucu verip vermediğini inceleyin.
- Kayan noktalı yaklaşık eşitliği gerçek eşitlik gibi sunarken dikkatli olun; toleranslı karşılaştırma geçişlilik özelliğini bozabilir.

İyi operatör aşırı yükleme, yalnızca derlenen kod değil, kullanıcı sezgisiyle uyumlu bir sözleşmedir. Operatörünüz matematiksel bir sembol taşıyorsa kullanıcı da matematiksel tutarlılık bekler; aksi hâlde küçük bir `!=`, oldukça büyük bir güven problemine dönüşür.

---
layout: post
title: "C++ Template Tür Çıkarımı: Beklenmedik Instantiation Hatalarını Anlamak"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - template
  - tür çıkarımı
  - instantiation
  - sfinae
  - concepts
toc: true
image: /img/c-template-tur-33.png
---

C++ şablonları, aynı algoritmayı farklı türlerle kullanmayı sağlayan güçlü bir mekanizmadır. Fakat derleyicinin bir türü başarıyla çıkarması, ilgili şablonun sorunsuz biçimde üretileceği anlamına gelmez. Bazen masum görünen bir fonksiyon çağrısı, derleyiciyi henüz hazır olmayan bir gövdeyi örneklemeye zorlar ve ekranı uzun, hiyeroglif benzeri hata mesajlarıyla doldurur.
``

## Tür çıkarımı ile örnekleme aynı şey değildir

Bir fonksiyon şablonu çağrıldığında süreç kabaca üç aşamadan geçer:

1. **Tür çıkarımı:** Şablon parametreleri, fonksiyon argümanlarından belirlenir.
2. **Yerine koyma:** Çıkarılan türler bildirimdeki ilgili konumlara yazılır.
3. **Örnekleme:** Gerekli fonksiyon veya sınıf gövdesi gerçek türlerle üretilir.

Bunu basitleştirilmiş biçimde şöyle gösterebiliriz:

$$
\text{çağrı} \rightarrow \text{deduction} \rightarrow \text{substitution} \rightarrow \text{instantiation}
$$

Sorun, hatanın hangi aşamada oluştuğuna bağlıdır. Yerine koyma sırasında oluşan bazı hatalar SFINAE veya constraint mekanizmasıyla adayın elenmesini sağlar. Şablon gövdesinin örneklenmesi sırasında oluşan hata ise çoğunlukla doğrudan derleme hatasıdır.

| Durum | Hatanın oluştuğu yer | Tipik sonuç |
|---|---|---|
| Parametre veya dönüş türü | Immediate context | SFINAE ile aday elenebilir |
| Fonksiyon gövdesi | Instantiation | Sert derleme hatası |
| `requires` ifadesi | Constraint kontrolü | Kısıt sağlanmaz |
| Seçilmeyen `if constexpr` dalı | Örneklenmez | Hata genellikle oluşmaz |

## `auto` dönüş türünün hazırladığı sürpriz

Aşağıdaki kod, bir türün `foo()` fonksiyonuna sahip olup olmadığını kontrol ediyor gibi görünür:

```cpp
#include <concepts>

template<class T>
auto probe(T value) {
    return value.foo();
}

template<class T>
concept HasFoo = requires(T value) {
    probe(value);
};

static_assert(!HasFoo<int>);
```

Fakat `probe<int>` fonksiyonunun dönüş türünü bulabilmek için derleyici gövdeyi örneklemek zorundadır. `int` üzerinde `foo()` bulunmadığından hata, güvenli bir constraint başarısızlığı yerine fonksiyon gövdesinde patlayabilir. Derleyici adeta “Sadece bakacaktım, bütün evi inşa ettim” der.

Kontrol edilmesini istediğimiz ifadeyi dönüş türüne taşıyarak hatayı uygun bağlama alabiliriz:

```cpp
template<class T>
auto probe(T value) -> decltype(value.foo()) {
    return value.foo();
}

template<class T>
concept HasFoo = requires(T value) {
    probe(value);
};
```

Artık `decltype(value.foo())`, fonksiyon bildirimindeki immediate context içinde değerlendirilir. İfade geçersizse aday kullanılabilir sayılmaz; gereksiz gövde örneklemesi yapılmaz.

## Tembel olmayan tür seçimi

`std::conditional_t` de sık rastlanan bir tuzaktır. Koşul yalnızca bir dalı seçse bile iki tür argümanının da önce geçerli olması gerekir:

```cpp
#include <type_traits>

template<class T>
using ValueOrSelf = std::conditional_t<
    requires { typename T::value_type; },
    typename T::value_type,
    T
>;

// ValueOrSelf<int> x; // int::value_type geçersizdir
```

Burada koşul `false` olsa bile `typename T::value_type` oluşturulmaya çalışılır. Çözüm, seçimi uzmanlaşmalarla tembel hâle getirmektir:

```cpp
template<class T, class = void>
struct value_or_self {
    using type = T;
};

template<class T>
struct value_or_self<T, std::void_t<typename T::value_type>> {
    using type = typename T::value_type;
};

template<class T>
using value_or_self_t = typename value_or_self<T>::type;
```

## Hataları kontrol altında tutmak

Şablon kodunda şu alışkanlıklar hata mesajlarını ciddi ölçüde iyileştirir:

- Gereksinimleri fonksiyon gövdesi yerine `requires`, `concept` veya `decltype` ile bildirimde ifade edin.
- Seçilmeyecek kodu `if constexpr` içinde tutun.
- Tür seçiminin gerçekten tembel olup olmadığını sorgulayın.
- Şablonları yalnızca geçerli türlerle değil, özellikle geçersiz türlerle de test edin.
- Derleyicinin hata izinde ilk kullanıcı kodunu bulun; standart kütüphane satırlarında kaybolmayın.

Kısacası tür çıkarımı yalnızca doğru anahtarı bulur; instantiation ise kapının arkasındaki odanın gerçekten var olup olmadığını kontrol eder. Sağlam template tasarımı, bu kontrolü mümkün olduğunca erken ve kontrollü yapmaktır.

![c-template-tur-33](/img/c-template-tur-33.svg)


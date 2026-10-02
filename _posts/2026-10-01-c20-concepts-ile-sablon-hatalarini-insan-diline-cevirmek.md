---
layout: post
title: "C++20 Concepts ile Şablon Hatalarını İnsan Diline Çevirmek"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - c++20
  - concepts
  - templates
  - generic-programlama
  - constraints
toc: true
image: /img/c20-concepts-ile-12.png
---

C++ şablonları güçlüdür; ancak yanlış bir tür kullandığınızda derleyici bazen küçük bir hatayı yüzlerce satırlık bir destana dönüştürür. C++20 ile gelen **Concepts**, şablon parametrelerinden ne beklendiğini açıkça tanımlayarak bu sorunu büyük ölçüde çözer. Böylece hem derleyici daha anlaşılır hata verir hem de fonksiyonun kabul ettiği türler kaynak koddan okunabilir.
``
## Sorun: Şablonlar Fazla İyimserdir

Klasik bir şablon, kendisine verilen türün gerekli işlemleri desteklediğini baştan doğrulamaz:

```cpp
template <typename T>
T topla(const T& a, const T& b) {
    return a + b;
}
```

Bu fonksiyon `T` türünün `+` operatörüne sahip olduğunu varsayar. `topla(3, 5)` sorunsuzdur; fakat toplama desteklemeyen bir sınıf kullanılırsa hata çoğunlukla fonksiyonun çağrıldığı yeri değil, şablonun derinliklerindeki başarısız işlemleri anlatır.

Concept yaklaşımında şablonun geçerli olma koşulunu bir mantık önermesi gibi düşünebiliriz:

$$
Geçerli(T) = Toplanabilir(T) \land SonuçUyumlu(T)
$$

Koşul `false` olduğunda derleyici fonksiyon gövdesine dalmadan adayı reddeder. Buna **constraint satisfaction**, yani kısıtın sağlanması denir.

| Geleneksel şablon | Concept kullanan şablon |
|---|---|
| Beklentiler fonksiyon gövdesinde gizlidir | Beklentiler imzada görünür |
| Hata geç ve dolaylı oluşabilir | Hata çağrı noktasına yakın oluşur |
| Dokümantasyon ayrıca yazılmalıdır | Kısıt aynı zamanda dokümantasyondur |
| Uygunluk deneme yoluyla anlaşılır | Uygunluk derleme zamanında sorgulanır |

## İlk Concept'imizi Yazalım

Bir türün `+` işlemini desteklemesini ve sonucun yine aynı türe çevrilebilmesini isteyelim:

```cpp
#include <concepts>

// T için gerekli sözdizimini derleme zamanında denetler.
template <typename T>
concept Toplanabilir = requires(T a, T b) {
    { a + b } -> std::convertible_to<T>;
};

template <Toplanabilir T>
T topla(const T& a, const T& b) {
    return a + b;
}
```

`requires` ifadesi içindeki `{ a + b }`, işlemin geçerli olup olmadığını sınar. Ok işaretinden sonraki `std::convertible_to<T>` ise sonucun `T` türüne dönüştürülebilmesini şart koşar. Bu kod işlemi çalıştırmaz; yalnızca sözdizimini ve tür ilişkisini derleme sırasında inceler.

Aynı kısıt farklı biçimlerde uygulanabilir:

```cpp
template <typename T>
requires Toplanabilir<T>
T ikiKat(const T& değer) {
    return değer + değer;
}
```

İlk yazım kısa ve okunaklıdır. `requires` cümleciği kullanılan ikinci yazım ise birden fazla koşulu birleştirirken daha esnektir:

```cpp
template <typename T>
requires Toplanabilir<T> && std::default_initializable<T>
T güvenliToplam(const T& a, const T& b) {
    return a + b;
}
```

Burada tür hem toplanabilir hem de varsayılan biçimde oluşturulabilir olmalıdır. Mantıksal karşılığı şöyledir:

$$
Kabul(T) = Toplanabilir(T) \land VarsayılanOluşturulabilir(T)
$$

## Metot Varlığını Denetlemek

Concepts yalnızca operatörleri değil, üye fonksiyonları da kontrol edebilir. Örneğin bir koleksiyonun `size()` metoduna sahip olmasını isteyelim:

```cpp
#include <concepts>
#include <cstddef>

template <typename T>
concept Boyutlanabilir = requires(const T& nesne) {
    { nesne.size() } -> std::convertible_to<std::size_t>;
};

template <Boyutlanabilir T>
void boyutuYazdır(const T& nesne) {
    std::cout << nesne.size() << '\n';
}
```

Bu tanım, “Herhangi bir `T` kabul ederim” yerine “`size()` çağrılabilen ve sonucu boyut değerine çevrilebilen bir `T` kabul ederim” der. Niyet artık hem kullanıcıya hem derleyiciye açıktır.

## Hazır Concept'leri Unutmayın

`<concepts>` başlığı `std::integral`, `std::floating_point`, `std::same_as`, `std::derived_from` ve `std::convertible_to` gibi hazır araçlar sunar. Örneğin yalnızca tam sayıları kabul etmek son derece kolaydır:

```cpp
template <std::integral T>
T kare(T sayı) {
    return sayı * sayı;
}
```

Concepts, şablonların gücünü azaltmaz; bu gücün giriş kapısına anlaşılır bir güvenlik görevlisi koyar. Sonuç daha kısa hatalar, daha güçlü API sözleşmeleri ve bakım sırasında daha az “Bu derleyici bana ne anlatıyor?” anıdır.

![c20-concepts-ile-12](/img/c20-concepts-ile-12.svg)


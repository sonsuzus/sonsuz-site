---
layout: post
title: "C++ Generic Programming: Fonksiyon ve Sınıf Şablonlarının Tasarım Sınırları"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - generic-programming
  - templates
  - fonksiyon-şablonları
  - sınıf-şablonları
  - concepts
toc: true
image: /img/c-generic-programming-66.png
---

C++ şablonları, aynı algoritmayı veya veri yapısını farklı türlerle çalıştırmanın güçlü bir yoludur. Ancak fonksiyon şablonları ile sınıf şablonları aynı sözdizimsel aileden gelseler de tür çıkarımı, özelleştirme ve hata yönetimi bakımından farklı tasarım kısıtlarına sahiptir. Kısacası biri çoğunlukla “Bu işlemi hangi türlerle yapabilirim?”, diğeri ise “Bu tür ailesinin durumunu ve davranışını nasıl modellemeliyim?” sorusuna odaklanır.

``

## Ortak teorik temel

Bir şablonu, türleri parametre olarak alan bir üretim kuralı gibi düşünebiliriz. $T$ bir tür ve $G$ bir şablon olsun. Derleyici uygun kullanım gördüğünde somut bir örnek üretir:

$$G(T) \rightarrow G_T$$

Bu süreç **örnekleme** olarak adlandırılır. Fakat bir şablonun gerçekten kullanılabilir olması için gövdesindeki işlemlerin seçilen tür üzerinde geçerli olması gerekir. Örneğin `a + b` ifadesi kullanılıyorsa $T$ türü toplama işlemini desteklemelidir. Modern C++’ta bu gereksinimler `concept` ile açıkça belirtilebilir.

| Tasarım özelliği | Fonksiyon şablonu | Sınıf şablonu |
|---|---|---|
| Tür çıkarımı | Genellikle argümanlardan otomatik | C++17 CTAD dışında çoğunlukla açık |
| Kısmi özelleştirme | Desteklenmez | Desteklenir |
| Aşırı yükleme | Doğal ve yaygın | Üye fonksiyonlar üzerinden |
| Durum saklama | Genellikle yok | Temel amaçlardan biri |
| Arayüz kısıtları | Çağrı anında belirginleşir | Sınıf örneği ve üyeler düzeyinde görülür |

## Fonksiyon şablonlarının temel kısıtları

Fonksiyon şablonlarının en büyük avantajı, tür çıkarımıdır. Derleyici parametrelerden `T` türünü bulabilir:

```cpp
#include <concepts>

template<typename T>
requires std::totally_ordered<T>
const T& buyuk(const T& a, const T& b) {
    return a < b ? b : a;
}
```

Buradaki `requires`, fonksiyonun yalnızca tam sıralama ilişkisi sunan türlerle kullanılacağını anlatır. Böylece anlamsız kullanımlar, şablon gövdesindeki karmaşık hatalar yerine arayüz seviyesinde reddedilir.

Bununla birlikte çıkarım, dönüş türünden yapılmaz. `T sonuc = uret();` ifadesindeki hedef tür, klasik fonksiyon şablonu çıkarımını tek başına yönlendiremez. Ayrıca fonksiyon şablonlarında kısmi özelleştirme bulunmaz. Belirli bir tür ailesine farklı davranış vermek için aşırı yükleme, `if constexpr`, yardımcı sınıf şablonu veya concept tabanlı overload kullanmak gerekir.

```cpp
template<typename T>
void yazdir(const T& deger) {
    // Genel davranış
}

template<typename T>
void yazdir(T* adres) {
    // İşaretçiler için overload
}
```

İkinci fonksiyon kısmi özelleştirme değil, ayrı bir aşırı yüklemedir. Bu ayrım overload çözümleme kurallarını etkilediği için önemlidir.

## Sınıf şablonlarının temel kısıtları

Sınıf şablonları veri üyeleriyle birlikte tür politikası, sahiplik ve yaşam süresi tasarlamaya uygundur:

```cpp
#include <cstddef>
#include <stdexcept>

template<typename T, std::size_t N>
class SabitTampon {
    T veri[N]{};

public:
    T& getir(std::size_t i) {
        if (i >= N) throw std::out_of_range("indeks");
        return veri[i];
    }
};
```

Burada hem tür hem de derleme zamanı kapasitesi sınıf kimliğinin parçasıdır. Dolayısıyla `SabitTampon<int, 8>` ile `SabitTampon<int, 16>` tamamen farklı türlerdir. Genel olarak iki örnek ancak tüm şablon argümanları aynıysa aynı türdür:

$$C<T, N> = C<U, M> \iff T=U \land N=M$$

Sınıf şablonlarının önemli üstünlüğü kısmi özelleştirmedir. Örneğin `Depo<T*>`, bütün işaretçi türleri için farklı sahiplik kuralları uygulayabilir. Ancak bu güç, tekrar eden kod ve özelleştirmeler arasında tutarsız arayüz riski doğurur. Genel sürümde bulunan bir üyenin özelleştirilmiş sürümde unutulması şaşırtıcı derleme hatalarına yol açabilir.

## Hangisini ne zaman seçmeli?

Tek bir işlem, argümanlardan çıkarılabilen türler ve doğal overload davranışı gerekiyorsa fonksiyon şablonu seçilmelidir. Durum saklama, politika birleştirme, tür ailesi oluşturma veya kısmi özelleştirme gerekiyorsa sınıf şablonu daha uygundur. İyi bir generic tasarım yalnızca “her türle çalışmak” değildir; desteklenen işlemleri mümkün olduğunca erken, açık ve anlaşılır biçimde sınırlandırmaktır. `concept` kullanımı da bu sınırların üzerindeki nazik ama kararlı güvenlik görevlisidir.

![c-generic-programming-66](/img/c-generic-programming-66.svg)


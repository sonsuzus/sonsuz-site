---
layout: post
title: "C++ Fonksiyonlarında Referans mı, İşaretçi mi? Semantik Belirsizlikleri Çözmek"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - referans
  - işaretçi
  - fonksiyonlar
  - api-tasarımı
  - bellek-yönetimi
toc: true
image: /img/c-fonksiyonlarinda-referans-98.png
---

C++ geliştirirken `T&` ile `T*` arasındaki fark yalnızca sözdiziminden ibaret değildir. Bu iki parametre biçimi; null olasılığı, sahiplik, yeniden bağlanma ve fonksiyonun çağıranın nesnesini değiştirip değiştirmediği hakkında farklı mesajlar verir. Yanlış seçim yapıldığında kod derlenebilir, hatta yıllarca çalışabilir; ancak API’nin niyeti sisli bir İstanbul sabahına döner.

``

## Temel zihinsel model

Referans, var olan bir nesne için alternatif bir ad gibi düşünülebilir. İşaretçi ise bir nesnenin adresini tutan ayrı bir değerdir. Bir nesnenin adresi $A$ ise işaretçi kabaca $p = A$ ilişkisini taşır; `*p` ifadesi de o adresteki nesneye erişir. Referansta ise `r`, doğrudan aynı nesneyi temsil eder:

$$r \equiv x, \qquad p = \&x$$

Bu benzerlik, ikisinin aynı semantiğe sahip olduğu anlamına gelmez.

| Özellik | Referans (`T&`) | İşaretçi (`T*`) |
|---|---|---|
| Null olabilir mi? | Dil seviyesinde hayır | Evet |
| Yeniden bağlanabilir mi? | Hayır | Evet |
| Kullanım sözdizimi | `value.member` | `value->member` |
| İsteğe bağlı parametre mesajı | Uygun değil | Uygun olabilir |
| Sahiplik belirtir mi? | Genellikle hayır | Tek başına belirsiz |

![c-fonksiyonlarinda-referans-98](/img/c-fonksiyonlarinda-referans-98.svg)


## Fonksiyon parametrelerindeki asıl belirsizlik

Aşağıdaki iki fonksiyon teknik olarak aynı nesneyi değiştirebilir:

```cpp
void increase(int& value) {
    ++value;
}

void increase(int* value) {
    if (value != nullptr) {
        ++(*value);
    }
}
```

Çağrı biçimleri ise farklı niyetler taşır:

```cpp
int score = 10;
increase(score);   // Değişiklik ihtimali çağrı noktasında az görünür.
increase(&score);  // Adres verilmesi değişiklik sinyalini güçlendirir.
```

Referans kullanan ilk çağrı, değer ile aktarılıyormuş gibi görünebilir. Fonksiyon bildirimi görülmüyorsa okuyucu `score` değişecek mi diye duraksar. İşaretçili çağrı daha görünürdür; fakat bu kez başka sorular doğar: `nullptr` geçerli mi, fonksiyon belleği serbest bırakacak mı, adres daha sonra saklanacak mı?

Dolayısıyla belirsizlik sözdiziminden çok, belgelenmemiş sözleşmeden kaynaklanır.

## `const` pusulasını kullanmak

`const`, fonksiyonun niyetini belirginleştiren en önemli araçlardan biridir:

| Bildirim | Verdiği mesaj |
|---|---|
| `const T& value` | Nesne zorunlu, kopyalanmayacak ve değiştirilmeyecek |
| `T& value` | Nesne zorunlu ve değiştirilebilir |
| `const T* value` | Nesne isteğe bağlı olabilir, varsa değiştirilmeyecek |
| `T* value` | Nesne isteğe bağlı olabilir ve değiştirilebilir |
| `T*& value` | İşaretçinin kendisi de değiştirilebilir |

Özellikle `T*&` sık karıştırılır. Burada fonksiyon yalnızca nesneyi değil, çağıranın işaretçisini de başka bir adrese yöneltebilir:

```cpp
void selectDefault(User*& current, User& fallback) {
    if (current == nullptr) {
        current = &fallback;
    }
}
```

Bu davranış gerçekten gerekiyorsa bildirim anlamlıdır. Yalnızca nesneyi değiştirmek isteniyorsa `User*` veya `User&` daha doğru olur.

## Sahiplik tuzağı

Ham işaretçi sahipliği açıklamaz. `Widget*` gören kişi nesnenin kim tarafından yok edileceğini bilemez. Modern C++’ta sahiplik için akıllı işaretçiler tercih edilmelidir:

```cpp
void inspect(const Widget& widget);             // Ödünç alır, null olamaz.
void inspect(const Widget* widget);             // Ödünç alır, null olabilir.
void consume(std::unique_ptr<Widget> widget);   // Sahipliği devralır.
void share(std::shared_ptr<Widget> widget);      // Ortak sahiplik kurar.
```

Buradaki isimler ve türler birlikte okununca API’nin sözleşmesi büyük ölçüde anlaşılır.

## Pratik seçim rehberi

Parametre zorunluysa ve sahiplik aktarılmıyorsa referans kullanın. Yokluğu anlamlı bir durumsa işaretçi veya daha açık bir soyutlama seçin. Salt okuma için `const T&`, küçük ve ucuz türler için değer aktarımı tercih edin. Sahiplik aktarımını ham işaretçiyle gizlemeyin; `std::unique_ptr` ya da `std::shared_ptr` ile görünür kılın.

Kısacası referans ve işaretçi birbirinin süslü yazılmış hâli değildir. İyi tasarlanmış bir fonksiyon imzası, yalnızca derleyiciye tür bilgisi vermez; okuyucuya null, değişiklik ve sahiplik hakkında küçük ama güvenilir bir hikâye anlatır.

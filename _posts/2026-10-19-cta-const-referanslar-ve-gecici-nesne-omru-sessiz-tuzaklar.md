---
layout: post
title: "C++’ta const Referanslar ve Geçici Nesne Ömrü: Sessiz Tuzaklar"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - const
  - referanslar
  - nesne-ömrü
  - geçici-nesneler
  - modern-c++
toc: true
image: /img/cta-const-referanslar-21.png
---

![cta-const-referanslar-21](/img/cta-const-referanslar-21.svg)


C++’ta `const T&` gördüğümüzde genellikle “güvenli, değiştirilemez referans” diye düşünürüz. Ancak geçici nesneler devreye girdiğinde konu yalnızca değiştirilebilirlikten ibaret değildir. Referansın neye, nerede ve nasıl bağlandığı; geçici nesnenin hemen yok edilmesini de kapsam sonuna kadar yaşamasını da sağlayabilir. Kısacası `const`, bazen nesneye adeta fazladan can verir.

``

## Geçici nesne nedir?

Bir ifadenin sonucunu taşımak için oluşturulan, genellikle adı olmayan nesneye geçici nesne denir. Örneğin `std::string("merhaba")` bir geçici nesne üretir. Normal koşullarda bu nesne, içinde oluşturulduğu **tam ifadenin** sonunda yok edilir. Çoğu zaman bu nokta noktalı virgüldür.

```cpp
std::string("merhaba"); // Nesne bu satırın sonunda yok edilir.
```

Basitleştirilmiş biçimde geçici nesnenin olağan ömrünü şöyle düşünebiliriz:

$$L_{geçici} = t_{ifade\ sonu} - t_{oluşturma}$$

Fakat uygun bir yerel referansa doğrudan bağlama yapılırsa ömür, referansın kapsamına kadar uzatılabilir:

$$L_{uzatılmış} = t_{kapsam\ sonu} - t_{oluşturma}$$

## `const` referans neden özel?

Lvalue referansları normalde geçici nesnelere bağlanamaz:

```cpp
std::string& a = std::string("C++"); // Hata
```

Bunun nedeni, kısa ömürlü ve isimsiz bir değerin değiştirilebilir bir lvalue referansı üzerinden kullanılmasının riskli kabul edilmesidir. Buna karşılık `const` lvalue referansı bağlanabilir:

```cpp
const std::string& a = std::string("C++");
std::cout << a; // Güvenli: geçicinin ömrü a'nın kapsamına uzatıldı.
```

| Bağlama biçimi | Geçiciye bağlanır mı? | Ömür uzar mı? |
|---|---:|---:|
| `T&` | Hayır | Hayır |
| `const T&` | Evet | Genellikle evet |
| `T&&` | Evet | Yerel değişkense evet |
| Fonksiyon parametresi `const T&` | Evet | Yalnızca çağrının tam ifadesinin sonuna kadar |

Son satır kritik bir ayrıntıdır. Bir fonksiyon parametresine bağlanan geçici, fonksiyon çağrısı bittikten sonra saklanamaz.

```cpp
const std::string* adres;

void sakla(const std::string& metin) {
    adres = &metin;
}

sakla(std::string("kaybolacak"));
// Bu noktadan sonra adres dangling pointer!
```

`metin`, fonksiyon içinde geçerlidir; fakat çağrının bulunduğu tam ifade sona erince geçici nesne yok edilir.

## Referansı döndürmek ömrü uzatmaz

En tehlikeli sürprizlerden biri, fonksiyondan `const` referans döndürmektir:

```cpp
const std::string& üret() {
    return std::string("geçici"); // Hatalı: yok edilecek nesneye referans
}
```

`const` burada koruyucu kalkan değildir. Fonksiyon sona erdiğinde geçici nesne yok edilir ve dönen referans boşa çıkar. Doğru yaklaşım değeri döndürmektir:

```cpp
std::string üret() {
    return std::string("güvenli");
}
```

Modern C++, kopya eleme ve taşıma sayesinde bu kodu çoğunlukla ek maliyet oluşturmadan çalıştırır.

## İkinci referans ikinci bir ömür vermez

Ömür uzatma aktarılabilir bir özellik değildir:

```cpp
const std::string& ilk = std::string("örnek");
const std::string& ikinci = ilk;
```

Nesnenin ömrü `ilk` nedeniyle uzatılmıştır. `ikinci`, aynı nesneye başka bir takma ad verir; ömrü yeniden başlatmaz veya kendi kapsamına göre genişletmez. Eğer `ikinci`, `ilk`ten daha uzun yaşarsa dangling referansa dönüşebilir.

## `const` dönüş değeri her zaman yararlı değildir

Eski kodlarda `const T` döndüren fonksiyonlar görülebilir:

```cpp
const std::string oluştur();
```

Bu kullanım, modern C++’ta taşıma işlemlerini engelleyebilir; çünkü taşıma kurucuları çoğunlukla `T&&` bekler, `const T&&` değil. Değer döndüren fonksiyonlarda genellikle yalnızca `T` tercih edilmelidir.

Özet kural şudur: Yerel `const T&` ve `T&&`, doğrudan bağlandıkları geçicinin ömrünü uzatabilir. Parametreler, döndürülen referanslar ve başka bir referans üzerinden yapılan bağlamalar için aynı güvenceyi varsaymayın. `const`, değişikliği sınırlar; her durumda ömür yönetmez.

---
layout: post
title: "C++ API Tasarımında Değer Semantiği mi, Referans Semantiği mi?"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - api tasarımı
  - değer semantiği
  - referans semantiği
  - bellek yönetimi
  - modern c++
toc: true
image: /img/c-api-tasariminda-87.png
---

![c-api-tasariminda-87](/img/c-api-tasariminda-87.svg)


Bir C++ API’sinin bir nesneyi kopyalaması mı, yoksa mevcut nesneye erişim sağlaması mı gerektiği küçük bir imza tercihi gibi görünebilir. Oysa bu karar; sahiplikten performansa, hata ayıklamadan eşzamanlılığa kadar bütün tasarımı etkiler. Kısacası `Widget` ile `Widget&` arasındaki tek karakterlik fark, bazen bakım maliyetinde destan yazdırır.

``

## İki semantiğin temel fikri

**Değer semantiğinde** değişken, bağımsız bir değeri temsil eder. Kopyalanan iki nesne başlangıçta eşit olabilir; ancak biri değiştirildiğinde diğeri etkilenmez. `int`, `std::string` ve `std::vector` bu modele iyi örneklerdir.

**Referans semantiğinde** ise farklı değişkenler aynı nesnenin kimliğine erişebilir. Nesne üzerindeki değişiklikler tüm gözlemciler tarafından görülebilir. Burada önemli olan yalnızca içerik değil, nesnenin *hangi nesne* olduğudur.

Matematiksel olarak değer kopyalamayı şöyle düşünebiliriz:

$$b = copy(a) \Rightarrow a = b$$

Ancak sonradan `b` değiştirildiğinde genellikle:

$$modify(b) \nRightarrow modify(a)$$

Referanslarda ise `a` ve `b` aynı nesneyi gösteriyorsa durum farklıdır:

$$identity(a) = identity(b) \Rightarrow modify(b) = modify(a)$$

| Ölçüt | Değer semantiği | Referans semantiği |
|---|---|---|
| Sahiplik | Genellikle açık ve yerel | Haricen yönetilebilir |
| Bağımsızlık | Kopyalar bağımsızdır | Aynı nesne paylaşılabilir |
| Yaşam süresi | Değerin kapsamına bağlıdır | Dangling riski taşır |
| Değişiklik etkisi | Yereldir | Uzak kodu etkileyebilir |
| Eşzamanlılık | Daha kolay yönetilir | Senkronizasyon gerekebilir |
| Polimorfizm | Nesne dilimleme riski vardır | Doğal biçimde desteklenir |

## Parametrelerde seçimin anlamı

Bir fonksiyon parametresini değerle almak, fonksiyonun kendi bağımsız nesnesine sahip olacağını anlatır:

```cpp
class Report {
public:
    void addPage(int page);
};

void archive(Report report) {
    report.addPage(42);
    // Çağıranın nesnesi değişmez.
}
```

Bu yaklaşım özellikle fonksiyon nesneyi saklayacaksa veya dönüştürecekse kullanışlıdır. Çağıran geçici bir değer ya da `std::move` ile taşıma sağladığında gereksiz kopyalar azaltılabilir.

Salt okuma amaçlı büyük nesnelerde `const T&`, kopyalama maliyetini önler:

```cpp
void print(const Report& report) {
    // report okunabilir fakat değiştirilemez.
}
```

Buradaki `const`, sahiplik vermez; yalnızca bu erişim yolu üzerinden değişikliği engeller. Fonksiyon referansı saklıyorsa çağıranın nesnesi daha erken yok olabilir. API, bu yaşam süresi sözleşmesini açıkça belirtmelidir.

Değiştirilebilir `T&` ise fonksiyonun çağıranın nesnesini değiştireceğini bildirir:

```cpp
void normalize(Report& report) {
    report.addPage(1);
}
```

Böyle bir API etkili olsa da yan etki üretir. Sonuç döndüren değer tabanlı bir alternatif çoğu zaman daha anlaşılırdır:

```cpp
Report normalized(Report report) {
    report.addPage(1);
    return report;
}
```

Modern C++’ta taşıma semantiği ve kopya eleme sayesinde bu sürüm, göründüğünden daha ucuz olabilir. Yaklaşık maliyeti $C_{copy}$ yerine çoğu durumda $C_{move}$ veya doğrudan $0$ olur.

## Dönüş değerleri ve sahiplik

Yeni bir nesne üreten fonksiyonun `T` döndürmesi genellikle en güvenli seçenektir. `T&` döndürmek ise var olan bir nesneye takma ad verir; nesnenin yaşam süresi çağıranın kullanımından uzun olmalıdır. Yerel değişkene referans döndürmek kesinlikle hatalıdır.

Paylaşılan kimlik gerçekten gerekliyse akıllı işaretçiler sözleşmeyi görünür kılar:

- `std::unique_ptr<T>`: Tekil sahiplik aktarılır.
- `std::shared_ptr<T>`: Sahiplik paylaşılır.
- `std::weak_ptr<T>`: Sahip olmadan gözlem yapılır.
- `T*` veya `T&`: Genellikle sahip olunmayan erişim sunulur.

## Pratik karar rehberi

Para, koordinat, tarih ve yapılandırma gibi bağımsız kavramlarda değer semantiğini tercih edin. Veritabanı bağlantısı, pencere, cihaz, aktör veya polimorfik servis gibi kimliği önemli varlıklarda referans semantiği daha doğaldır.

API’nin davranışını şu sorularla sınayın: Nesne kopyalanınca anlam bozuluyor mu? Fonksiyon sahipliği devralıyor mu? Değişiklik çağırana yansımalı mı? Referansın geçerlilik süresi açık mı? Eşzamanlı erişim mümkün mü?

En iyi seçim her zaman en hızlı görünen seçenek değildir. İyi bir C++ API’si, sahiplik ve değişebilirlik niyetini tür sistemi üzerinden anlatır. Değer semantiği varsayılan güvenli liman; referans semantiği ise kimlik, paylaşım veya polimorfizm gerçekten gerektiğinde kullanılan güçlü ama dikkat isteyen araçtır.

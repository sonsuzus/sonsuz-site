---
layout: post
title: "C++ Akış ve Dosya G/Ç Sistemi: Verinin Yolculuğunu Yönetmek"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - stream
  - dosya işlemleri
  - girdi çıktı
  - oop
  - fstream
toc: true
image: /img/c-akis-ve-62.png
---

C++ programlarında veri bazen klavyeden gelir, bazen ekrana gider, bazen de bir dosyada yıllarca uyumayı bekler. Akış sistemi, verinin kaynağıyla hedefi arasındaki bu yolculuğu ortak ve nesne yönelimli bir arayüz üzerinden yönetir. Böylece geliştirici, klavye ile dosya arasında geçiş yaparken tamamen farklı yöntemler öğrenmek zorunda kalmaz.


![c-akis-ve-62](/img/c-akis-ve-62.svg)

``

## Akış Mantığı Nedir?

Bir **stream**, sıralı biçimde taşınan karakter veya baytların oluşturduğu soyut bir kanaldır. Program çoğu zaman gerçek cihazla doğrudan ilgilenmez; akış nesnesine veri gönderir veya ondan veri ister. `std::cin`, `std::cout`, `std::cerr` ve dosya sınıfları bu yaklaşımın örnekleridir.

Akışların nesne yönelimli yapısı sınıf hiyerarşisine dayanır. `std::ios` biçimlendirme ve durum bilgisini taşırken `std::istream` okuma, `std::ostream` yazma davranışlarını sunar. `std::iostream` ise ikisini birleştirir. Dosya tarafındaki sınıflar aynı arayüzleri dosya tamponlarıyla ilişkilendirir.

| Sınıf | Görevi | Yaygın kullanım |
|---|---|---|
| `std::ifstream` | Dosyadan okuma | Yapılandırma yükleme |
| `std::ofstream` | Dosyaya yazma | Rapor veya günlük oluşturma |
| `std::fstream` | Okuma ve yazma | Kayıt güncelleme |
| `std::stringstream` | Bellekte metin akışı | Ayrıştırma ve dönüştürme |

Tamponlama, her küçük işlemde diske erişilmesini engeller. Kabaca toplam maliyet

$$T \approx n \cdot t_{işlem} + k \cdot t_{G/Ç}$$

şeklinde düşünülebilir. Tampon kullanıldığında pahalı G/Ç sayısı olan $k$ azalır. `flush` işlemi tamponu zorla hedefe aktarır; gereksiz kullanılması performansı düşürebilir.

## Nesne Yönelimli Dosya Okuma ve Yazma

Dosya nesneleri kaynak yönetimini **RAII** yaklaşımıyla gerçekleştirir. Nesne kapsamdan çıktığında dosya otomatik olarak kapatılır. Yine de açılışın başarılı olup olmadığını kontrol etmek gerekir.

```cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    std::ofstream cikti("notlar.txt", std::ios::app);

    if (!cikti) {
        std::cerr << "Dosya açılamadı!\n";
        return 1;
    }

    cikti << "Akışlar nesne yönelimlidir." << '\n';
}
```

Buradaki `std::ios::app`, yeni veriyi dosyanın sonuna ekler. Varsayılan davranışta `ofstream`, mevcut içeriği silebilir. Başlıca kipler şöyledir:

| Kip | Anlamı |
|---|---|
| `std::ios::in` | Okuma için açar |
| `std::ios::out` | Yazma için açar |
| `std::ios::app` | Sona ekler |
| `std::ios::trunc` | İçeriği temizler |
| `std::ios::binary` | İkili kip kullanır |

Metin dosyasını satır satır okumak için `std::getline` güvenli ve anlaşılır bir seçimdir:

```cpp
std::ifstream girdi("notlar.txt");
std::string satir;

while (std::getline(girdi, satir)) {
    std::cout << satir << '\n';
}

if (girdi.bad()) {
    std::cerr << "Fiziksel bir okuma hatası oluştu.\n";
}
```

Döngü, okuma başarılı olduğu sürece çalışır. `while (!girdi.eof())` yaklaşımı önerilmez; çünkü EOF bayrağı ancak başarısız bir okuma denemesinden sonra etkinleşir.

## Durum Bayrakları ve Hata Yönetimi

Akış nesneleri kendi sağlık durumlarını saklar. `good()` sorun olmadığını, `eof()` dosya sonunu, `fail()` biçimsel veya mantıksal başarısızlığı, `bad()` ise daha ciddi G/Ç hatasını bildirir. Hata sonrasında `clear()` bayrakları sıfırlar; fakat hatalı karakterler hâlâ tampondaysa `ignore()` ile temizleme gerekebilir.

```cpp
int sayi;
if (!(std::cin >> sayi)) {
    std::cin.clear();
    std::cin.ignore(10000, '\n');
    std::cout << "Geçersiz sayı girdiniz.\n";
}
```

## Konumlandırma ve İkili Dosyalar

`tellg()` ve `tellp()` mevcut okuma-yazma konumunu verir; `seekg()` ve `seekp()` konumu değiştirir. Bu özellik büyük dosyalarda doğrudan belirli bir kayda erişmeyi sağlar. İkili dosyalar `read()` ve `write()` ile işlenebilir; ancak sınıfları ham baytlarla kaydetmek taşınabilir değildir. Dolgulama, endian düzeni ve işaretçi üyeleri sorun çıkarabilir. Kalıcı veriler için açık bir serileştirme biçimi tasarlamak daha güvenlidir.

Sonuç olarak C++ akış sistemi yalnızca dosya açıp kapatan bir araç değildir. Ortak arayüzler, durum yönetimi, tamponlama ve RAII sayesinde farklı veri kaynaklarını aynı zihinsel model altında birleştiren güçlü bir soyutlamadır.

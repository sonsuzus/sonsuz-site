---
layout: post
title: "C++ İçindeki C Alt Kümesi: Temelden Modern C++’a"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - c
  - sözdizimi
  - programlama temelleri
  - bellek yönetimi
toc: true
image: /img/c-icindeki-c-66.png
---

C++, nesne yönelimli programlama, şablonlar ve standart kütüphane gibi güçlü özelliklere sahip olsa da dilin kalbinde C’den miras alınan önemli bir sözdizimi bulunur. Değişkenler, operatörler, koşullar, döngüler, fonksiyonlar, diziler ve işaretçiler bu ortak temelin parçalarıdır. Bu yapıları öğrenmek yalnızca eski C kodlarını anlamayı değil, C++’ın düşük seviyeli çalışma mantığını kavramayı da kolaylaştırır.

``

## “C alt kümesi” ne demektir?

C alt kümesi, C++ içinde kullanılabilen C benzeri özelliklerin öğretim amaçlı adıdır. Ancak C’nin bütünü teknik olarak C++’ın kusursuz bir alt kümesi değildir. Diller arasında anahtar kelimeler, tür dönüşümleri ve standartlar bakımından bazı uyumsuzluklar vardır. Buna rağmen pek çok temel program aşağı yukarı aynı biçimde derlenebilir.

| Özellik | C yaklaşımı | C++ yaklaşımı |
|---|---|---|
| Temel türler | `int`, `char`, `double` | Aynı türler ve ek tür olanakları |
| Ekrana yazma | `printf` | `printf` veya `std::cout` |
| Bellek ayırma | `malloc` / `free` | `new` / `delete`, tercihen kapsayıcılar |
| Veri modeli | `struct` | `struct` ve `class` |
| Tür güvenliği | Daha esnek | Genellikle daha katı |

![c-icindeki-c-66](/img/c-icindeki-c-66.svg)


Dolayısıyla “C tarzı C++”, modern C++’ın tamamı değil, üzerine yeni katların inşa edildiği temel zemin olarak düşünülmelidir.

## Değişkenler, operatörler ve ifadeler

Temel değişken bildirimi iki dilde de benzerdir:

```cpp
int adet = 5;
double fiyat = 12.5;
char kod = 'A';

// Aritmetik bir ifade hesaplar.
double toplam = adet * fiyat;
```

Bir ifadenin sonucu, operatör önceliğine göre belirlenir. Örneğin `a + b * c` ifadesinde önce çarpma yapılır. Matematiksel karşılığı $a + (b \times c)$ biçimindedir. Tam sayı bölmesinde ise kesirli bölüm atılır: `7 / 2` sonucu `3` olur. Gerçek sayı sonucu için `7.0 / 2.0` kullanılmalıdır.

## Kontrol akışı

C’den aktarılan `if`, `else`, `switch`, `for`, `while` ve `do-while` yapıları C++ programlarının da temel kontrol araçlarıdır.

```cpp
int toplam = 0;

// 1 ile 10 arasındaki çift sayıları toplar.
for (int i = 1; i <= 10; ++i) {
    if (i % 2 == 0) {
        toplam += i;
    }
}
```

Bu döngünün kaç kez çalıştığı $n$ ile ifade edilebilir ve doğrusal karmaşıklığı $O(n)$ olur. İç içe iki benzer döngü kullanıldığında işlem sayısı yaklaşık $n^2$ düzeyine çıkabilir. Böylece basit C sözdizimi, algoritma analizi için de güçlü bir başlangıç sunar.

## Fonksiyonlar ve değer aktarımı

Fonksiyonlar, kodu tekrar kullanılabilir parçalara ayırır. C tarzında parametreler varsayılan olarak değer üzerinden aktarılır; yani fonksiyon değişkenin kopyasını alır.

```cpp
int kare(int sayi) {
    return sayi * sayi;
}

int sonuc = kare(6); // sonuc 36 olur
```

Bir fonksiyon çağrılmadan önce bildirilmeli veya tanımlanmalıdır. C++ buna ek olarak fonksiyon aşırı yükleme ve referans parametreleri sunar; bunlar saf C yaklaşımının ötesindedir.

## Diziler ve işaretçiler

C tarzı diziler sabit uzunluklu, ardışık bellek bölgeleridir:

```cpp
int sayilar[4] = {10, 20, 30, 40};
int* adres = sayilar;

// İşaretçi aritmetiğiyle ikinci elemana erişir.
int ikinci = *(adres + 1);
```

Dizi adı çoğu ifadede ilk elemanın adresine dönüşür. `adres + 1`, bellekte bir bayt değil, bir `int` kadar ilerler. Eğer `sizeof(int) = 4` ise gerçek adres değişimi 4 bayttır. Bu davranış hızlıdır; fakat sınır denetimi yapılmadığından hataya açıktır.

## Manuel bellek yönetimi

C’den gelen yaklaşımda dinamik bellek `malloc` ile ayrılır ve `free` ile bırakılır. C++ bunu desteklese de tür dönüşümü ve nesne yaşam döngüsü nedeniyle doğrudan tercih edilmez. Modern C++’ta `std::vector`, `std::string` ve akıllı işaretçiler daha güvenlidir.

Özetle C alt kümesi; sözdizimini, belleği ve program akışını çıplak hâliyle öğretir. Bu temeli öğrenmek değerlidir, ancak gerçek C++ projelerinde kaynakları otomatik yöneten modern araçlara geçmek hem güvenliği hem de okunabilirliği artırır.

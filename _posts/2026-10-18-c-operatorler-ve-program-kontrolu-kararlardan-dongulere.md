---
layout: post
title: "C# Operatörler ve Program Kontrolü: Kararlardan Döngülere"
math: true
categories: 
  - Bilgi
tags: 
  - c#
  - operatörler
  - if-else
  - döngüler
  - programlama
  - kontrol-akışı
toc: true
image: /img/c-operatorler-ve-81.png
---

Bir C# programı yalnızca yukarıdan aşağıya çalışan komutlardan oluşmaz. Değerleri karşılaştırır, koşullara göre karar verir ve gerektiğinde aynı işlemi tekrarlar. Operatörler bu kararların kelimeleri, kontrol blokları ise programın trafik ışıklarıdır. Gelin C# kodunun nasıl düşündüğünü adım adım inceleyelim.

``

## Operatörlerin temel mantığı

Operatör, bir veya daha fazla değer üzerinde işlem yapan semboldür. Örneğin `+` iki sayıyı toplarken `>=` değerleri karşılaştırır. `=` ile `==` arasındaki fark özellikle önemlidir: İlki atama, ikincisi eşitlik kontrolüdür.

```csharp
int puan = 75;              // Atama
bool gectiMi = puan >= 50;  // Karşılaştırma
int bonusluPuan = puan + 10;
```

Aritmetik operatörler matematiksel işlemleri gerçekleştirir. İki sayı $a$ ve $b$ olmak üzere kalan işlemi $a \bmod b$ biçiminde düşünülebilir. C# dilinde bunun karşılığı `%` operatörüdür.

| Grup | Operatörler | Örnek kullanım |
|---|---|---|
| Aritmetik | `+`, `-`, `*`, `/`, `%` | `sayi % 2` |
| Karşılaştırma | `==`, `!=`, `<`, `>`, `<=`, `>=` | `yas >= 18` |
| Mantıksal | `&&`, `||`, `!` | `aktif && yetkili` |
| Atama | `=`, `+=`, `-=`, `*=`, `/=` | `puan += 5` |
| Artırma/Azaltma | `++`, `--` | `sayac++` |

![c-operatorler-ve-81](/img/c-operatorler-ve-81.svg)


Mantıksal operatörler Boolean cebirine dayanır. `&&` için sonuç yalnızca iki ifade de doğruysa doğrudur:

$$A \land B = true \quad \text{yalnızca A ve B doğruysa}$$

`||` operatöründe ise koşullardan birinin doğru olması yeterlidir. C# kısa devre değerlendirmesi uygular; `A && B` ifadesinde `A` yanlışsa `B` çalıştırılmaz. Bu davranış hem performans sağlar hem de bazı null hatalarını engeller.

## C#'a özgü kullanışlı işleçler

C#, null değerlerle güvenli çalışmayı kolaylaştıran operatörler sunar. `?.` yalnızca nesne null değilse üyeye erişir; `??` ise sol taraf null olduğunda yedek değer üretir.

```csharp
string? kullaniciAdi = null;
int? uzunluk = kullaniciAdi?.Length;
string gorunenAd = kullaniciAdi ?? "Misafir";

Console.WriteLine(gorunenAd); // Misafir
```

`is` tür denetimi ve örüntü eşleştirme için, `as` ise güvenli tür dönüşümü için kullanılır. Ayrıca `nameof(degisken)` değişkenin adını metin olarak verir; böylece yeniden adlandırmalara dayanıklı hata mesajları oluşturulur.

| İşleç | Amaç | Başarısızlık davranışı |
|---|---|---|
| `?.` | Güvenli üye erişimi | Null üretir |
| `??` | Varsayılan değer seçimi | Sağ tarafı kullanır |
| `is` | Tür veya örüntü kontrolü | `false` üretir |
| `as` | Referans türü dönüşümü | Null üretir |

## if-else ile karar vermek

`if` bloğu koşul doğru olduğunda çalışır. Alternatif yollar `else if` ve `else` ile tanımlanır.

```csharp
int not = 82;

if (not >= 85)
{
    Console.WriteLine("Pek iyi");
}
else if (not >= 50)
{
    Console.WriteLine("Geçti");
}
else
{
    Console.WriteLine("Tekrar dene");
}
```

Basit seçimlerde üçlü koşul operatörü kullanılabilir: `sonuc = kosul ? dogruDeger : yanlisDeger;`. Ancak iç içe üçlü ifadeler kodu bulmacaya çevirebilir; okunabilirlik her zaman kısalıktan değerlidir.

## Döngüsel iterasyon mekanizmaları

Döngüler tekrar eden işleri otomatikleştirir. Hangi döngünün seçileceği, tekrar sayısının bilinip bilinmemesine bağlıdır.

| Döngü | Ne zaman tercih edilir? | Özellik |
|---|---|---|
| `for` | Tekrar sayısı biliniyorsa | Sayaç kontrolü sunar |
| `while` | Devam koşulu önemliyse | Koşulu başta sınar |
| `do-while` | İşlem en az bir kez yapılacaksa | Koşulu sonda sınar |
| `foreach` | Koleksiyon gezilecekse | İndeks yönetimi gerektirmez |

```csharp
string[] diller = { "C#", "Java", "Python" };

foreach (string dil in diller)
{
    if (dil == "Java")
        continue; // Bu turu atlar

    Console.WriteLine(dil);
}
```

`continue` mevcut turu atlatırken `break` döngüyü tamamen bitirir. Sonsuz döngülerden kaçınmak için `while` koşulunu etkileyen değerin gerçekten değiştiğinden emin olun. Özetle operatörler veriyi işler, koşullar yolu seçer, döngüler ise işi tekrarlar; bu üçlü, neredeyse bütün C# uygulamalarının kontrol merkezidir.

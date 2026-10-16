---
layout: post
title: "C# Temsilciler ve Olaylar: Metotları Konuşturan Mekanizma"
math: true
categories: 
  - Bilgi
tags: 
  - csharp
  - delegates
  - events
  - dotnet
  - nesne-yönelimli-programlama
toc: true
image: /img/c-temsilciler-ve-83.png
---

Bir düğmeye tıklandığında hangi metodun çalışacağını, indirme tamamlanınca kime haber verileceğini veya hesaplama sonucunun hangi kuralla işleneceğini önceden sabitlemek istemeyiz. C# bu esnekliği **temsilciler (delegates)** ile sağlar; **olaylar (events)** ise temsilcileri güvenli bir bildirim mekanizmasına dönüştürür.

![c-temsilciler-ve-83](/img/c-temsilciler-ve-83.svg)

``
## Temsilci nedir?

Temsilci, belirli bir metot imzasını temsil eden tür güvenli bir nesnedir. C ve C++ dünyasındaki fonksiyon işaretçilerine benzer; ancak hangi dönüş tipini ve parametreleri kabul ettiğini bilir, nesne metotlarıyla çalışabilir ve çalışma zamanında denetlenir.

Bir temsilciyi matematiksel olarak şu dönüşümle düşünebiliriz:

$$f: X \rightarrow Y$$

Burada $X$ metodun parametrelerini, $Y$ ise dönüş değerini temsil eder. Örneğin iki `int` alıp bir `int` döndüren temsilci yalnızca aynı imzaya sahip metotları gösterebilir.

```csharp
public delegate int Islem(int x, int y);

static int Topla(int x, int y)
{
    return x + y;
}

Islem hesapla = Topla;
Console.WriteLine(hesapla(4, 6)); // 10
```

`hesapla`, `Topla` metodunu saklayan ve çağırabilen bir nesnedir. Böylece davranış, veri gibi başka metotlara aktarılabilir.

| Özellik | Fonksiyon işaretçisi | C# temsilcisi |
|---|---|---|
| Tür güvenliği | Sınırlı olabilir | Güçlüdür |
| Nesne metodunu destekleme | Elle yönetilebilir | Doğrudan destekler |
| Birden fazla metot | Ek yapı gerekir | Multicast özelliği vardır |
| Nesne yönelimli kullanım | Zayıf | Güçlü |

## Hazır temsilciler: Action, Func ve Predicate

Her kullanım için yeni bir temsilci türü tanımlamak gerekmez. .NET üç kullanışlı aile sunar:

- `Action<T>` değer döndürmeyen metotları temsil eder.
- `Func<T, TResult>` son türü sonuç olmak üzere değer döndüren metotları temsil eder.
- `Predicate<T>` bir koşulu sınar ve `bool` döndürür.

```csharp
Action<string> yazdir = mesaj => Console.WriteLine(mesaj);
Func<int, int, int> carp = (a, b) => a * b;
Predicate<int> ciftMi = sayi => sayi % 2 == 0;

yazdir($"Çarpım: {carp(3, 5)}");
Console.WriteLine(ciftMi(8)); // True
```

Lambda ifadeleri kısa metotları temsilcilere bağlamayı kolaylaştırır. `ciftMi` için kullanılan koşul matematiksel olarak $n \bmod 2 = 0$ biçimindedir.

## Multicast temsilciler

Bir temsilciye `+=` ile birden fazla metot eklenebilir. Çağrı yapıldığında metotlar eklenme sırasıyla yürütülür. `-=` ise aboneliği kaldırır.

```csharp
Action bildirim = () => Console.WriteLine("Ekrana yazıldı");
bildirim += () => Console.WriteLine("Günlüğe kaydedildi");

bildirim(); // İki metot da çalışır
```

Değer döndüren multicast temsilcilerde çağrı sonucu, son metodun dönüş değeridir. Bu nedenle bildirim senaryolarında çoğunlukla `void` tercih edilir.

## Event neden gerekli?

Temsilci herkese açık bırakılırsa dışarıdaki kod onu çağırabilir veya içindeki aboneleri silebilir. `event` anahtar sözcüğü bu yetkiyi sınırlar: Dış kod yalnızca `+=` ve `-=` kullanabilir; olayı yalnızca onu tanımlayan sınıf tetikleyebilir.

```csharp
public class Indirici
{
    public event EventHandler<string>? Tamamlandi;

    public void Indir()
    {
        Console.WriteLine("Dosya indiriliyor...");
        Tamamlandi?.Invoke(this, "rapor.pdf");
    }
}

var indirici = new Indirici();
indirici.Tamamlandi += (gonderen, dosya) =>
    Console.WriteLine($"Hazır: {dosya}");

indirici.Indir();
```

Burada `Indirici` **yayıncı**, lambda ise **abone** konumundadır. `?.Invoke` ifadesi abone yoksa hata oluşmasını engeller.

| Kavram | Görevi | Tipik kullanım |
|---|---|---|
| Delegate | Metot referansı taşır | Strateji ve geri çağrı |
| Event | Kontrollü bildirim yayınlar | Arayüz ve durum değişikliği |
| Publisher | Olayı tetikler | Düğme veya indirme servisi |
| Subscriber | Olaya tepki verir | Ekran, günlük veya e-posta |

Grafik arayüzlerde `Click`, `MouseMove` ve `TextChanged` gibi olayların temelinde tam olarak bu yayıncı-abone modeli bulunur. Temsilci “hangi davranış çalışacak?” sorusunu, olay ise “bir şey olduğunda kimlere haber verilecek?” sorusunu çözer. Abonelik artık gerekmiyorsa `-=` ile kaldırmak, gereksiz nesne referanslarını ve olası bellek sorunlarını önlemek açısından önemlidir.

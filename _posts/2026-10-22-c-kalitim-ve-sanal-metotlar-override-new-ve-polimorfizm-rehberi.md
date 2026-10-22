---
layout: post
title: "C# Kalıtım ve Sanal Metotlar: override, new ve Polimorfizm Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - csharp
  - kalıtım
  - polimorfizm
  - oop
  - sanal-metotlar
  - dotnet
toc: true
image: /img/c-kalitim-ve-20.png
---

![c-kalitim-ve-20](/img/c-kalitim-ve-20.svg)


Kalıtım, bir sınıfın başka bir sınıftaki veri ve davranışları devralmasını sağlayan nesne yönelimli programlama tekniğidir. C# tarafında bu mekanizma yalnızca kod tekrarını azaltmaz; doğru kullanıldığında değiştirilebilir, genişletilebilir ve test edilebilir sistemlerin temelini oluşturur. Ancak `virtual`, `override` ve `new` anahtar sözcükleri karıştırılırsa masum görünen bir sınıf hiyerarşisi küçük bir sürpriz fabrikasına dönüşebilir.
``

## Kalıtımın temel mantığı

Türetilmiş sınıf, temel sınıfın erişilebilir üyelerini devralır. C# dilinde sınıf türetmek için sınıf adından sonra `:` kullanılır:

```csharp
public class Hayvan
{
    public string Ad { get; set; } = string.Empty;

    public void Beslen()
    {
        Console.WriteLine($"{Ad} besleniyor.");
    }
}

public class Kedi : Hayvan
{
    public void Mirla()
    {
        Console.WriteLine($"{Ad} mırlıyor.");
    }
}
```

`Kedi`, kendi `Mirla` metoduna ek olarak `Hayvan` sınıfındaki `Ad` ve `Beslen` üyelerini kullanabilir. Buradaki ilişki “Kedi bir Hayvan’dır” şeklinde okunur. Bu **is-a** ilişkisi mantıklı değilse kalıtım yerine bileşim tercih edilmelidir.

Bir hiyerarşideki sınıf sayısını $n$, her sınıfta tekrarlanacak ortak davranış miktarını $m$ kabul edersek kaba tekrar maliyeti $n \times m$ olur. Ortak davranışı temel sınıfa taşımak bu miktarı yaklaşık $m + n$ seviyesine indirebilir. Elbette gerçek tasarım kalitesi yalnızca satır sayısıyla ölçülmez.

## Sanal metot ve ezme işlemi

Temel sınıf, alt sınıfların bir davranışı değiştirmesine izin vermek için metodu `virtual` olarak tanımlar. Türetilmiş sınıf ise `override` ile aynı sözleşmenin yeni uygulamasını sunar:

```csharp
public class Hayvan
{
    public virtual void SesCikar()
    {
        Console.WriteLine("Bilinmeyen hayvan sesi");
    }
}

public class Kedi : Hayvan
{
    public override void SesCikar()
    {
        Console.WriteLine("Miyav!");
    }
}

Hayvan dost = new Kedi();
dost.SesCikar(); // Miyav!
```

Değişkenin derleme zamanı türü `Hayvan`, gerçek nesnenin türü ise `Kedi` olmasına rağmen `Kedi.SesCikar` çalışır. Buna çalışma zamanı polimorfizmi denir. Hangi uygulamanın seçileceği nesnenin gerçek türüne göre belirlenir.

## `override` ile `new` arasındaki kritik fark

`new`, temel sınıftaki üyeyi ezmez; onu gizler. Bu nedenle çağrılacak metot, referansın derleme zamanı türüne bağlıdır.

```csharp
public class Temel
{
    public void Yaz() => Console.WriteLine("Temel");
}

public class Turemis : Temel
{
    public new void Yaz() => Console.WriteLine("Türetilmiş");
}

Turemis a = new Turemis();
Temel b = a;

a.Yaz(); // Türetilmiş
b.Yaz(); // Temel
```

| Özellik | `override` | `new` |
|---|---|---|
| Amaç | Sanal davranışı değiştirmek | Üyeyi gizlemek |
| Seçim zamanı | Çalışma zamanı | Derleme zamanı |
| Temel metot gereksinimi | `virtual` veya `abstract` olmalı | Böyle bir gereksinim yok |
| Polimorfizm | Destekler | Gerçek polimorfizm sağlamaz |
| Tipik kullanım | Genişletilebilir tasarım | Bilinçli ad çakışması |

## `base`, `abstract` ve `sealed`

Ezilen metot içinde temel davranışı korumak için `base` kullanılabilir:

```csharp
public override void SesCikar()
{
    base.SesCikar();
    Console.WriteLine("Ardından özel kedi sesi: Miyav!");
}
```

Bir davranışın mutlaka alt sınıflarca uygulanması gerekiyorsa `abstract` daha güçlü bir sözleşme kurar. Daha fazla ezilmesini engellemek içinse metoda `sealed override` yazılabilir.

```csharp
public abstract class Odeme
{
    public abstract bool Gerceklestir(decimal tutar);
}

public class KartlaOdeme : Odeme
{
    public sealed override bool Gerceklestir(decimal tutar)
    {
        return tutar > 0;
    }
}
```

İyi bir polimorfik tasarımda kullanıcı kodu somut sınıflara değil, temel sınıf veya arayüz sözleşmesine bağımlı olur. Alt türler temel türün yerine geçtiğinde programın anlamı bozulmamalıdır; bu yaklaşım Liskov Yerine Geçme İlkesi’nin özüdür. Kısacası davranış gerçekten çeşitlenecekse `virtual/override`, zorunlu uygulanacaksa `abstract`, yalnızca isim çakışması bilinçli biçimde yönetilecekse `new` kullanılmalıdır.

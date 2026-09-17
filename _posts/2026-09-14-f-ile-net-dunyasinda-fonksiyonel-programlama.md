---
layout: post
title: "F# ile .NET Dünyasında Fonksiyonel Programlama"
math: true
categories: 
  - Bilgi
tags: 
  - fsharp
  - dotnet
  - fonksiyonel-programlama
  - immutability
  - pattern-matching
  - yazılım-geliştirme
toc: true
image: /img/f-ile-net-20.png
---

F#, .NET ekosisteminin güçlü araçlarını fonksiyonel programlama yaklaşımıyla buluşturan, kısa fakat etkileyici kodlar yazmayı sağlayan bir dildir. C# ile aynı çalışma zamanını paylaşmasına rağmen problemlere farklı bir gözlükle bakar: Veriyi sürekli değiştirmek yerine dönüştürür, işlemleri küçük fonksiyonlara böler ve olası durumları tür sistemiyle açıkça ifade eder. Kısacası F#, kodun içine biraz matematik, biraz düzen ve bolca huzur katar.


![f-ile-net-20](/img/f-ile-net-20.svg)

``

## Fonksiyonel programlamanın temel fikri

Fonksiyonel programlamada hesaplama, girdileri çıktılara dönüştüren fonksiyonlar üzerinden modellenir. Matematiksel olarak bir fonksiyonu şöyle gösterebiliriz:

$$f: A \rightarrow B$$

Bu ifade, `f` fonksiyonunun `A` türünde bir değer alıp `B` türünde bir değer ürettiğini söyler. Saf bir fonksiyon aynı girdi için daima aynı çıktıyı döndürür ve dış dünyada yan etki oluşturmaz:

$$x_1 = x_2 \Rightarrow f(x_1) = f(x_2)$$

Dosya yazmak veya veritabanına bağlanmak elbette gereklidir. Fonksiyonel yaklaşım bunları yasaklamaz; yalnızca yan etkileri hesaplama mantığından ayırarak kodu daha öngörülebilir hâle getirir.

| Yaklaşım | Değiştirilebilir stil | Fonksiyonel stil |
|---|---|---|
| Veri | Yerinde güncellenir | Yeni değer üretilir |
| Akış | Döngüler ve koşullar | Fonksiyon bileşimi |
| Hata | İstisna veya `null` | `Option` ve `Result` |
| Test | Duruma bağımlı olabilir | Girdi-çıktı odaklıdır |

## Değişmezlik ve pipeline operatörü

F# değerleri varsayılan olarak değişmezdir. Bu özellik, bir değişkenin kodun başka bir köşesinde gizlice değiştirilmesi gibi sürprizleri azaltır. `|>` pipeline operatörü ise veriyi adım adım fonksiyonlardan geçirerek okunabilir bir işlem hattı kurar.

```fsharp
let kare x = x * x
let ciftMi x = x % 2 = 0

let sonuc =
    [1..10]
    |> List.filter ciftMi
    |> List.map kare
    |> List.sum

printfn "Çift sayıların kareleri toplamı: %d" sonuc
```

Burada liste önce filtrelenir, ardından her elemanın karesi alınır ve sonuçlar toplanır. Aynı işlem iç içe çağrılarla da yazılabilirdi; ancak pipeline, verinin yolculuğunu soldan sağa takip etmeyi kolaylaştırır.

## Pattern matching: Koşulların daha zarif hâli

Pattern matching, bir değerin biçimine göre güvenli dallanma sağlar. Özellikle `Option` türüyle birlikte kullanıldığında `null` kontrollerine güçlü bir alternatif sunar.

```fsharp
let kullaniciBul id =
    if id = 42 then Some "Ada" else None

let mesajOlustur kullanici =
    match kullanici with
    | Some ad -> $"Hoş geldin, {ad}!"
    \vert  None -> "Kullanıcı bulunamadı."

kullaniciBul 42
\vert > mesajOlustur
\vert > printfn "%s"
```

`Some` bir değerin bulunduğunu, `None` ise bulunmadığını açıkça belirtir. Böylece “Bu değer acaba null olabilir mi?” sorusu tahmine değil, tür sistemine bırakılır.

## Ayrıştırılmış birleşimler ile alan modelleme

F# ayrıştırılmış birleşimleri, yalnızca geçerli durumların temsil edilmesini sağlar. Örneğin bir ödemenin durumu sınırsız bir metin yerine belirli seçeneklerle modellenebilir:

```fsharp
type OdemeDurumu =
    \vert  Bekliyor
    \vert  Tamamlandi of islemNo: string
    \vert  Reddedildi of neden: string

let aciklama durum =
    match durum with
    \vert  Bekliyor -> "Ödeme bekleniyor."
    \vert  Tamamlandi no -> $"İşlem tamamlandı: {no}"
    | Reddedildi neden -> $"Ödeme reddedildi: {neden}"
```

Derleyici tüm durumları ele alıp almadığımızı denetler. Yeni bir durum eklendiğinde güncellenmesi gereken noktalar görünür hâle gelir; yani derleyici sessiz bir ekip arkadaşından çok, dikkatli bir kod incelemecisine dönüşür.

## .NET ile birlikte çalışma

F#, NuGet paketlerini ve .NET kütüphanelerini doğrudan kullanabilir. ASP.NET Core ile web API, Entity Framework Core ile veri erişimi veya Azure araçlarıyla bulut uygulamaları geliştirilebilir. Ayrıca F# ve C# projeleri aynı çözüm içinde birbirlerini çağırabilir.

Fonksiyonel programlamaya başlarken her şeyi tek gecede saf fonksiyonlara dönüştürmek gerekmez. Küçük dönüşüm fonksiyonları yazmak, değişmez veriyi tercih etmek ve hata durumlarını `Result` ile modellemek iyi bir başlangıçtır. F# burada yalnızca yeni bir sözdizimi değil, daha açık ve güvenilir yazılım tasarlamak için farklı bir düşünme biçimi sunar.

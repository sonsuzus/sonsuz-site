---
layout: post
title: "Sekiz Komutla Sonsuz Hesap: Brainfuck ve Esolang Dünyası"
math: true
categories: 
  - Bilgi
tags: 
  - brainfuck
  - esolang
  - turing-tamlığı
  - programlama-dilleri
  - hesaplama-kuramı
toc: true
---

Bir programlama dilinden değişkenler, fonksiyonlar ve okunabilir hata mesajları bekliyorsanız Brainfuck sizi biraz üzebilir; hatta adı üstünde, zihninize küçük bir düğüm atabilir. Yalnızca sekiz komuttan oluşan bu deneysel dil, programlamanın süslü araçlarını kaldırıp geriye hesaplamanın çıplak mekanizmasını bırakır. Brainfuck ve diğer ezoterik programlama dilleri, yani *esolang*'lar, bilgisayara ne yaptırabileceğimiz ile bunu ne kadar anlaşılır ifade edebileceğimizin tamamen farklı meseleler olduğunu gösterir.

``

## Esolang nedir?

Esolang, pratik yazılım geliştirmekten çok fikirleri, sınırları veya mizahı keşfetmek için tasarlanmış programlama dilidir. Bazıları mümkün olan en az komutla hesaplama yapmayı, bazıları kodu şiire dönüştürmeyi, bazılarıysa programcıyı sabır testine sokmayı amaçlar.

| Dil | Temel fikir | Okunabilirlik | İlginç yönü |
|---|---|---:|---|
| Brainfuck | Bellek şeridi ve sekiz komut | Çok düşük | Minimal olup Turing tamdır |
| Befunge | Kod iki boyutlu alanda ilerler | Düşük | Yürütme yönü değişebilir |
| Piet | Programlar renkli görsellerdir | Alışılmadık | Komutlar renk geçişleriyle belirlenir |
| Whitespace | Yalnızca boşluk karakterleri anlamlıdır | Görünmez | Normal metin içine saklanabilir |
| Shakespeare | Kod tiyatro oyunu gibi yazılır | Komik derecede uzun | Değişkenler karakterlerdir |

Bu diller genellikle üretim ortamları için değildir. Kimse banka sistemini Piet ile yazmak istemez; yazarsa da denetim ekibine şimdiden sabır dileyelim.

## Brainfuck nasıl çalışır?

Brainfuck, hücrelerden oluşan bir bellek şeridi, bu şerit üzerinde duran bir işaretçi ve sekiz komut kullanır. Kuramsal modelde şerit sınırsız kabul edilir. Her hücre genellikle $0$ ile $255$ arasında bir değer taşır.

| Komut | Görevi |
|---|---|
| `>` | İşaretçiyi sağa taşır |
| `<` | İşaretçiyi sola taşır |
| `+` | Mevcut hücreyi artırır |
| `-` | Mevcut hücreyi azaltır |
| `.` | Hücreyi karakter olarak yazdırır |
| `,` | Girdi okuyup hücreye koyar |
| `[` | Hücre sıfırsa döngünün sonuna gider |
| `]` | Hücre sıfır değilse döngünün başına döner |

Örneğin aşağıdaki program ilk hücredeki değeri ikinci hücreye üç katı olarak aktarır:

```brainfuck
+++[>+++<-]
```

Başlangıçta ilk hücre `3` yapılır. Döngünün her turunda sağdaki hücre üç artırılır, soldaki hücre bir azaltılır. Üç tur sonunda bellek kabaca `[0, 9]` olur. Matematiksel olarak süreç

$$b \leftarrow b + 3, \qquad a \leftarrow a - 1$$

işlemlerini $a=0$ olana kadar tekrarlar. Yani küçücük bir sözdizimiyle çarpma davranışı elde edilir.

Bir karakter üretmek için ASCII değerini oluşturup `.` komutu kullanılabilir:

```brainfuck
++++++++[>++++++++<-]>+.
```

Döngü ikinci hücreyi $8 \times 8=64$ yapar; ardından `+` değeri `65`e çıkarır ve `.` ASCII tablosundaki `A` karakterini yazdırır. Kod kısa görünür, fakat niyeti saklamaya son derece heveslidir.

## Turing tamlığı neden önemli?

Bir sistem, yeterli zaman ve sınırsız bellek verildiğinde Turing makinesinin hesaplayabildiği her şeyi hesaplayabiliyorsa **Turing tam** kabul edilir. Kabaca ifade edersek:

$$\text{Programlanabilir bellek} + \text{koşullu tekrar} \Rightarrow \text{genel hesaplama gücü}$$

Brainfuck'ın hücreleri belleği, `[` ve `]` komutlarıysa koşullu tekrar mekanizmasını sağlar. Bu nedenle teorik olarak işletim sistemi, derleyici veya oyun yazabilir. Ancak “yazılabilir” ile “mantıklı biçimde yazılabilir” aynı şey değildir. Gerçek bilgisayarlardaki sonlu bellek de kuramsal sınırsızlık varsayımının pratik karşılığı değildir.

## Neden öğrenelim?

Brainfuck size yeni bir web çatısı öğretmez; daha temel bir şey öğretir: karmaşık görünen hesaplamaların veri taşıma, değer değiştirme ve dallanma gibi basit işlemlerden doğduğunu. Esolang'lar ayrıca dil tasarımındaki ergonominin ne kadar değerli olduğunu gösterir. Sekiz komut hesaplamak için yeterlidir, fakat insan zihni isimlere, yapılara ve açıklamalara ihtiyaç duyar. Brainfuck tam da bu yüzden hem korkunç bir araç hem de harika bir öğretmendir.

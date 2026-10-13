---
layout: post
title: "Boole Cebri ve Mantık Devreleri: Dijital Dünyanın Üç Temel Kapısı"
math: true
categories: 
  - Bilgi
tags: 
  - boole cebri
  - mantık devreleri
  - and kapısı
  - or kapısı
  - not kapısı
  - dijital elektronik
  - verilog
toc: true
image: /img/boole-cebri-ve-29.png
---

Bilgisayarlar, telefonlar ve oyun konsolları dışarıdan son derece karmaşık görünür. Ancak bu cihazların derinliklerine indiğimizde karşımıza yalnızca iki değer çıkar: 0 ve 1. Boole cebri, bu iki değer arasındaki ilişkileri matematiksel olarak açıklarken AND, OR ve NOT kapıları da aynı işlemleri elektronik devrelerde gerçekleştirir. Kısacası milyarlarca transistörün düzenlediği dijital konser, üç temel notayla başlar.

``

## Boole cebri nedir?

George Boole tarafından geliştirilen Boole cebrinde değişkenler yalnızca iki değer alır. Genellikle 0 değeri **yanlış**, 1 değeri ise **doğru** anlamına gelir. Elektronik devrelerde bunlar düşük ve yüksek gerilim seviyelerini temsil eder.

Klasik cebirde $2 + 2 = 4$ gibi işlemler yaparken Boole cebrinde sonuçlar doğruluk durumlarına göre belirlenir. Temel işlemler şöyle gösterilebilir:

- AND: $A \cdot B$
- OR: $A + B$
- NOT: $\overline{A}$

Buradaki toplama ve çarpma sembolleri bildiğimiz aritmetik işlemler değildir. Örneğin Boole cebrinde $1 + 1 = 1$ olur; çünkü iki doğru ifadenin OR sonucu yine doğrudur.

## Üç temel mantık kapısı

| Kapı | Sözel anlamı | Çıkışın 1 olma koşulu | Günlük hayat benzetmesi |
|---|---|---|---|
| AND | VE | Tüm girişler 1 ise | İki anahtar da açıksa lamba yanar |
| OR | VEYA | En az bir giriş 1 ise | Kapılardan biri açılırsa alarm çalar |
| NOT | DEĞİL | Giriş 0 ise | Karanlık olduğunda gece lambası yanar |

### AND kapısı

AND kapısı seçici bir güvenlik görevlisi gibidir: Bütün koşullar sağlanmadan geçişe izin vermez. İki girişli bir AND kapısının denklemi $Y=A \cdot B$ biçimindedir.

| A | B | Y |
|---:|---:|---:|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

Örneğin bir makinenin çalışması için hem güvenlik kapağının kapalı hem de başlatma düğmesinin basılı olması gerekiyorsa AND kapısı kullanılabilir.

### OR kapısı

OR kapısı daha hoşgörülüdür. Girişlerden en az biri doğruysa çıkış doğrudur. Denklem $Y=A+B$ şeklindedir. Yalnızca $A=0$ ve $B=0$ olduğunda çıkış 0 olur. Bir binada duman sensörü veya sıcaklık sensörü tehlike algıladığında alarmın çalışması buna örnektir.

### NOT kapısı

NOT kapısının tek girişi vardır ve aldığı değeri tersine çevirir:

$$Y=\overline{A}$$

Giriş 1 ise çıkış 0, giriş 0 ise çıkış 1 olur. Bu nedenle NOT kapısına **invertör** de denir. Otomatik yanan bir gece lambasında ışık sensörünün sonucu ters çevrilerek karanlıkta enerji verilmesi sağlanabilir.

## Kapıları birleştirince ne olur?

Asıl eğlence kapılar birlikte kullanıldığında başlar. Örneğin aşağıdaki ifade, A ve B girişleri doğruyken veya C girişi yanlışken çıkışı etkinleştirir:

$$Y=(A \cdot B)+\overline{C}$$

Bu ifadeler sadeleştirilerek daha az kapı kullanan devreler üretilebilir. De Morgan kuralları bu noktada oldukça önemlidir:

$$\overline{A \cdot B}=\overline{A}+\overline{B}$$

Daha az kapı; daha düşük maliyet, enerji tüketimi ve gecikme anlamına gelebilir.

## Verilog ile küçük bir devre

Mantık devreleri, donanım tanımlama dilleriyle kodlanabilir. Aşağıdaki Verilog modülü aynı birleşik ifadeyi gerçekleştirir:

```verilog
module mantik_devresi (
    input  wire A,
    input  wire B,
    input  wire C,
    output wire Y
);
    assign Y = (A & B) | ~C;
endmodule
```

Burada `&` AND, `|` OR, `~` ise NOT işlemini temsil eder. `assign` ifadesi girişlerdeki değişikliklerin çıkışa sürekli yansıtılmasını sağlar. Bu kod bir FPGA üzerinde gerçek fiziksel kapılara dönüştürülebilir.

AND, OR ve NOT kapıları tek başlarına basit görünse de toplayıcılar, işlemciler, bellek denetleyicileri ve karar mekanizmaları bu yapıların birleşiminden doğar. Dijital dünyanın görkemli gökdelenleri, aslında 0 ve 1 biçimindeki küçücük tuğlalar üzerine kuruludur.

![boole-cebri-ve-29](/img/boole-cebri-ve-29.svg)


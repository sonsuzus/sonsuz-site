---
layout: post
title: "LLVM IR’a Giriş: Programlama Dilleri Arasında Evrensel Bir Köprü"
math: true
categories: 
  - Bilgi
tags: 
  - llvm
  - llvm-ir
  - derleyici
  - programlama-dilleri
  - optimizasyon
  - ara-dil
toc: true
---

Bir programlama dilinde yazdığımız kodun onlarca farklı işlemci ve işletim sisteminde çalışabilmesi küçük bir mucize gibi görünebilir. LLVM IR (Intermediate Representation), bu mucizenin arkasındaki önemli oyunculardan biridir. Kaynak dil ile makine kodu arasında ortak bir durak oluşturarak dil tasarımcılarının her donanım için ayrı derleyici yazma çilesini büyük ölçüde azaltır.
``
## Ara dil neden gereklidir?

Bir derleyiciyi iki temel parçaya ayırabiliriz: **ön uç** kaynak dili anlar, **arka uç** ise hedef mimariye uygun makine kodu üretir. Ara dil kullanılmadığında $N$ programlama dili ile $M$ donanım mimarisini desteklemek için teorik olarak

$$N \times M$$

farklı dönüşüm gerekebilir. Ortak bir ara dil sayesinde her dil LLVM IR üretir, her hedef de LLVM IR’dan makine koduna çevrilir. Böylece yaklaşık bağlantı sayısı

$$N + M$$

seviyesine iner. İşte LLVM IR’ın “diller arası köprü” olması tam olarak budur: Rust, C, C++, Swift veya kendi geliştirdiğiniz minik dil, aynı ara temsil üzerinden farklı işlemcilere ulaşabilir.

| Katman | Girdi | Temel görevi | Örnek |
|---|---|---|---|
| Ön uç | Kaynak kod | Sözdizimi ve anlam analizi | Clang, rustc |
| Ara temsil | LLVM IR | Taşınabilir analiz ve optimizasyon | `.ll`, `.bc` |
| Arka uç | LLVM IR | Hedefe özel kod üretimi | x86-64, ARM, RISC-V |

## LLVM IR nasıl görünür?

LLVM IR, assembly diline benzer; ancak belirli bir fiziksel işlemciye bağlı değildir. Türleri açıkça belirtilir ve çoğunlukla **Static Single Assignment** (SSA) biçimini kullanır. SSA yaklaşımında her sanal değişkene yalnızca bir kez değer atanır. Bu özellik veri akışını görünür hâle getirerek optimizasyonları kolaylaştırır.

Aşağıdaki fonksiyon iki adet 32 bit tamsayıyı toplar:

```llvm
define i32 @topla(i32 %a, i32 %b) {
entry:
  %sonuc = add i32 %a, %b
  ret i32 %sonuc
}
```

Burada `define` bir fonksiyon tanımlar, `i32` değerin 32 bit tamsayı olduğunu belirtir ve `%sonuc` sanal bir kayıt gibi davranır. `add` toplama işlemini gerçekleştirirken `ret`, hesaplanan değeri çağırana döndürür. Kod düşük seviyelidir ama hâlâ x86 veya ARM komutlarına kilitlenmemiştir.

## Bellek ve kontrol akışı

LLVM IR yalnızca aritmetik işlemlerden ibaret değildir. `alloca` yığın üzerinde alan ayırır, `load` bellekten okur, `store` belleğe yazar. Dallanmalarda `br`, farklı kontrol yollarından gelen değerleri birleştirmek içinse `phi` komutu kullanılır.

```llvm
define i32 @mutlak(i32 %x) {
entry:
  %negatif = icmp slt i32 %x, 0
  br i1 %negatif, label %eksi, label %arti

eksi:
  %ters = sub i32 0, %x
  br label %son

arti:
  br label %son

son:
  %deger = phi i32 [ %ters, %eksi ], [ %x, %arti ]
  ret i32 %deger
}
```

Bu örnekte `icmp`, `%x < 0$ karşılaştırmasını yapar. `phi`, programın hangi bloktan geldiğine göre `%ters` veya `%x` değerini seçer. Böylece klasik bir `if` yapısı açık bir kontrol akış grafiğine dönüşür.

## Metinsel IR, bitcode ve makine kodu

| Biçim | Uzantı | Okunabilirlik | Kullanım |
|---|---|---|---|
| Metinsel LLVM IR | `.ll` | İnsan tarafından okunabilir | Öğrenme, hata ayıklama |
| LLVM bitcode | `.bc` | İkili biçim | Araçlar arası taşıma |
| Nesne dosyası | `.o`, `.obj` | Makineye yönelik | Bağlama aşaması |

Clang ile basit bir C dosyasından LLVM IR üretmek mümkündür:

```bash
clang -S -emit-llvm ornek.c -o ornek.ll
opt -S -O2 ornek.ll -o optimize.ll
llc optimize.ll -o ornek.s
```

İlk komut okunabilir IR üretir. `opt`, sabit katlama ve ölü kod temizleme gibi optimizasyon geçişlerini uygular. `llc` ise sonucu hedef mimarinin assembly koduna dönüştürür.

LLVM IR tamamen donanımdan bağımsız değildir; işaretçi boyutları, veri yerleşimi ve hedef bilgileri önem taşır. Yine de sağladığı ortak sözlük sayesinde yeni bir dil geliştirirken makine kodu üretimini sıfırdan yazmanız gerekmez. Siz dilinizin anlamına odaklanırsınız, LLVM ise optimizasyon ve donanım tarafındaki ağır kutuları taşır. Oldukça çalışkan bir köprü görevlisi!

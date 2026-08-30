---
layout: post
title: "LLVM Altyapısını Tanımak: Modern Derleyicilerin Ortak Temeli"
math: true
categories: 
  - Bilgi
tags: 
  - llvm
  - derleyiciler
  - c++
  - ır
  - yazılım geliştirme
---

Bir programı kaynak koddan çalışabilir makine komutlarına dönüştürmek, yalnızca `if` ifadelerini çevirmekten çok daha büyük bir iştir. Farklı işlemciler, optimizasyonlar, hata mesajları ve hata ayıklama bilgileri derken derleyici geliştirmek hızla devasa bir projeye dönüşür. LLVM, tam bu karmaşıklığı yönetmek için doğmuş; bugün Clang, Rust, Swift ve Julia gibi pek çok teknolojinin kullandığı modüler bir derleyici altyapısıdır.

``

LLVM adı tarihsel olarak **Low Level Virtual Machine** açılımından gelir; ancak günümüzde proje resmî olarak yalnızca LLVM diye anılır. En önemli fikri, programın kaynak dili ile hedef işlemcisi arasına ortak bir ara temsil koymaktır. Bu temsil, **LLVM IR** (*Intermediate Representation*) olarak bilinir. C++, Rust ya da başka bir dilin ön yüzü kodu LLVM IR'a dönüştürür; LLVM'nin arka ucu ise bu IR'ı x86-64, ARM, WebAssembly veya RISC-V gibi hedefler için makine koduna çevirir.

Bir derleyicinin genel akışını aşağıdaki gibi düşünebiliriz:

$$\text{Kaynak Kod} \rightarrow \text{AST} \rightarrow \text{LLVM IR} \rightarrow \text{Optimize Edilmiş IR} \rightarrow \text{Makine Kodu}$$

Buradaki AST (*Abstract Syntax Tree*), kaynak programın sözdizimsel yapısını temsil eder. LLVM IR ise daha düşük seviyeli, tip bilgisi taşıyan ve optimizasyon yapmaya elverişli bir dildir. Örneğin `a + b` gibi masum bir ifade, hedef mimariden bağımsız bir `add` komutuna dönüşebilir. İşlemcinin hangi gerçek komutu kullanacağına daha sonra karar verilir.

| Katman | Temel Sorumluluk | Örnek Araç / Yapı |
|---|---|---|
| Ön uç (frontend) | Kaynak dili analiz etmek | Clang, rustc |
| Ara temsil | Ortak ve taşınabilir program modeli | LLVM IR |
| Optimizasyon geçişleri | Kodu daha hızlı veya küçük yapmak | Dead Code Elimination |
| Arka uç (backend) | Hedef işlemciye kod üretmek | X86, AArch64 backend |

LLVM IR'ın dikkat çekici özelliklerinden biri **SSA** (*Static Single Assignment*) biçimini kullanmasıdır. SSA'da her değer yalnızca bir kez atanır. Bu yaklaşım, veri akışını açık hâle getirir ve optimizasyonların işini kolaylaştırır. Matematiksel olarak bir değişkenin farklı program noktalarındaki değerlerini $x_1, x_2, \dots, x_n$ şeklinde ele alabiliriz; böylece derleyici hangi hesabın hangi değere bağlı olduğunu daha net izler.

Aşağıdaki küçük C kodu buna örnektir:

```c
int kare_toplam(int a, int b) {
    int x = a * a;
    int y = b * b;
    return x + y;
}
```

Clang ile LLVM IR üretmek için şu komut kullanılabilir:

```bash
clang -S -emit-llvm kare.c -o kare.ll
```

Ortaya çıkan IR, sadeleştirilmiş biçimiyle şöyledir:

```llvm
define i32 @kare_toplam(i32 %a, i32 %b) {
entry:
  %x = mul nsw i32 %a, %a
  %y = mul nsw i32 %b, %b
  %sonuc = add nsw i32 %x, %y
  ret i32 %sonuc
}
```

Burada `%x`, `%y` ve `%sonuc` birer SSA değeridir. `mul` çarpma, `add` toplama ve `ret` fonksiyondan dönüş işlemini ifade eder. `nsw` ise işaretli taşmanın beklenmediğine dair ek bir varsayım sunar; bu tür bilgiler optimizatöre daha cesur dönüşümler yapma fırsatı verir.

LLVM'nin gücü yalnızca kod üretmesi değildir. Kod üzerinde çalışan her dönüşüm bir **pass** olarak modellenir. Sabit katlama, kullanılmayan kodun silinmesi, döngü açma ve fonksiyon içi çağrıların gömülmesi bu geçişlere örnektir. Örneğin $3 \times 4$ ifadesi çalışma anında hesaplanmak yerine derleme zamanında $12$ değerine indirgenebilir.

| Yaklaşım | Avantaj | Sınırlama |
|---|---|---|
| Geleneksel tek parça derleyici | Başlangıçta daha basit tasarım | Yeni hedef eklemek maliyetli |
| LLVM tabanlı tasarım | Ön yüz ve arka uç yeniden kullanılabilir | IR ve pass ekosistemini öğrenmek gerekir |
| Doğrudan yorumlama | Hızlı deneme ve etkileşim | Genellikle daha düşük çalışma performansı |

LLVM ekosisteminin pratik araçları da oldukça değerlidir. `opt`, IR üzerinde optimizasyon geçişleri çalıştırır; `llc`, IR'ı hedef mimariye ait assembly'ye çevirir; `lli` ise uygun IR dosyalarını JIT benzeri biçimde çalıştırabilir. Böylece derleyici boru hattının her aşamasını ayrı ayrı gözlemlemek mümkündür.

Sonuç olarak LLVM, tek bir dilin derleyicisi değil; derleyici yazmayı daha erişilebilir kılan bir yapı taşı koleksiyonudur. Modern dil tasarımı, performans analizi, JIT derleme veya özel bir işlemci hedefiyle ilgileniyorsanız LLVM IR'ı okumayı öğrenmek, makinenin kaputunu açmak gibidir: Gürültülü olabilir, ama motorun neden bu kadar hızlı çalıştığını orada görürsünüz.

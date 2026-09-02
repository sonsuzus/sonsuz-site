---
layout: post
title: "LLVM IR ile Ara Kod Optimizasyonu: Döngü Açılımı ve Ölü Kod Eleme"
math: true
categories: 
  - Bilgi
tags: 
  - llvm
  - derleyici
  - llvm ır
  - optimizasyon
  - c++
toc: true
image: /img/llvm-ir-ile-25.png
---

Derleyiciler yalnızca kaynak kodunu makine koduna çeviren araçlar değildir; aynı zamanda programın yaptığı gereksiz işleri ayıklayan, sıcak kod yollarını hızlandıran ve hedef işlemcinin yeteneklerinden yararlanan analiz motorlarıdır. LLVM ekosisteminde bu işin merkezinde **LLVM IR (Intermediate Representation)** bulunur. Platformdan bağımsız olan bu ara temsil, C++, Rust, Swift veya başka bir ön uçtan geldikten sonra aynı optimizasyon boru hattında işlenebilir. Bu yazıda, arka uç optimizasyonlarının iki klasik yıldızını inceleyeceğiz: döngü açılımı (loop unrolling) ve ölü kod eleme (dead code elimination).
``

LLVM IR, SSA (*Static Single Assignment*) biçimini kullanır: Mantıksal olarak her değer yalnızca bir kez atanır. Bu özellik, bir değerin nerede üretildiğini ve kimler tarafından kullanıldığını izlemeyi kolaylaştırır. Örneğin `%sum` değerinin hiç kullanıcısı yoksa, onu hesaplayan komutlar da çoğu durumda gereksizdir. IR ayrıca `br`, `phi`, `load`, `store` ve `call` gibi açık talimatlarla kontrol akışını görünür hâle getirir. Böylece optimizasyonlar, kaynak dilin karmaşık sözdizimine değil, daha düzenli bir programa uygulanır.

## Döngü açılımı neden hızlandırır?

Döngü açılımı, gövdeyi birden çok kez kopyalayarak dal kontrolü ve sayaç artırma maliyetini azaltır. Örneğin her turda çalışan bir `br` talimatı dört işlem birleştirildiğinde daha seyrek çalışır. Basit bir maliyet modeliyle, toplam süreyi şöyle düşünebiliriz:

$$T \approx N \cdot (C_{gövde}+C_{kontrol})$$

Dört kat açılım sonrası yaklaşık maliyet:

$$T_{unroll4} \approx N \cdot C_{gövde}+\frac{N}{4}\cdot C_{kontrol}$$

Kazanç garanti değildir: Büyük gövde daha fazla makine kodu üretir, bu da komut önbelleğini zorlayabilir. LLVM bu nedenle döngü sayısını, gövde maliyetini, bağımlılıkları ve hedef mimarinin vektörleştirme imkânlarını değerlendirir.

| Özellik | Normal döngü | Açılmış döngü |
|---|---|---|
| Dallanma sayısı | Her iterasyonda | Daha seyrek |
| Kod boyutu | Küçük | Daha büyük |
| ILP / vektörleştirme | Sınırlı olabilir | Daha görünür olabilir |
| Önbellek riski | Düşük | Büyük açılımda yüksek |

![llvm-ir-ile-25](/img/llvm-ir-ile-25.svg)


Örneğin dört elemanı aynı turda toplama fikri IR düzeyinde şu yapıya yaklaşır:

```llvm
; %i değeri 4'er ilerler, gövde dört kez yazılmıştır
%a0 = getelementptr i32, ptr %arr, i64 %i
%v0 = load i32, ptr %a0
%j1 = add i64 %i, 1
%a1 = getelementptr i32, ptr %arr, i64 %j1
%v1 = load i32, ptr %a1
%partial = add i32 %v0, %v1
; Gerçek dönüşümde kalan iki eleman ve sınır denetimi de bulunur.
```

Buradaki amaç yalnızca dört satırı kopyalamak değildir. Bağımsız `load` ve `add` işlemleri belirginleştiği için işlemci zamanlayıcısı ya da sonraki LLVM geçişleri daha iyi karar verebilir. Komut satırında `opt -passes='loop-unroll' input.ll -S -o output.ll` ile dönüşümü deneyebilirsiniz. Üretim derlemelerinde `-O2` veya `-O3`, uygun koşullarda bu ve ilişkili geçişleri zaten etkinleştirir.

## Ölü kod eleme: Hesaplanmış ama işe yaramayan değerler

Ölü kod, programın gözlemlenebilir davranışını değiştirmeden kaldırılabilen talimattır. Kullanılmayan saf aritmetik işlemler tipik örnektir. Ancak `store`, dosyaya yazan `call` veya `volatile load` gibi yan etkili talimatlar, sonuçları kullanılmasa bile rastgele silinemez.

```llvm
%tmp = mul i32 %x, 42
%unused = add i32 %tmp, 7
%result = add i32 %x, 1
ret i32 %result
```

`%unused` değerinin kullanıcısı yoktur; dolayısıyla `add` silinir. Ardından `%tmp` da yalnızca silinen talimat tarafından kullanıldığı için ölü hâle gelir. Bu zincirleme temizliğe *dead instruction elimination* denir. LLVM’de `opt -passes='dce' input.ll -S -o output.ll` temel denemeler için yeterlidir; daha agresif sadeleştirme senaryolarında `adce` kullanılabilir.

| Durum | DCE ile kaldırılabilir mi? | Gerekçe |
|---|---:|---|
| Kullanılmayan `add` | Evet | Yan etkisi yoktur |
| Kullanılmayan `store` | Genellikle hayır | Bellek durumunu değiştirir |
| `pure` fonksiyon çağrısı | Koşullu | LLVM yan etki olmadığını bilmelidir |
| `volatile load` | Hayır | Donanım gözlemi olabilir |

Döngü açılımı ve DCE birlikte özellikle güçlüdür: Açılım sonrası sabit kalan veya kullanılmayan ara hesaplar oluşabilir; DCE bunları budar. Yine de başarı ölçütü yalnızca daha kısa IR değildir. `llvm-mca`, profil verileri ve gerçek kıyaslamalarla kod boyutu, dallanma davranışı ve çalışma süresi birlikte değerlendirilmelidir. Derleyici optimizasyonunda altın kural basittir: Daha çok dönüşüm değil, doğru iş yükü için doğru dönüşüm önemlidir.

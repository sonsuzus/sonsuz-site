---
layout: post
title: "Derleyici ve Yorumlayıcı Arasındaki Farklar: Kodun Yolculuğu"
math: true
categories: 
  - Bilgi
tags: 
  - derleyici
  - yorumlayıcı
  - programlama
  - makine dili
toc: true
---

Bir program yazdığınızda bilgisayar aslında `if`, `while` ya da `print` kelimelerinin ne anlama geldiğini doğrudan bilmez. İşlemcinin anlayabildiği şey, makine komutları olarak adlandırılan ikili talimatlardır. Kaynak kod ile işlemci arasındaki tercümanlık görevini ise iki temel yaklaşım üstlenir: **derleme (compilation)** ve **yorumlama (interpretation)**. Bu fark yalnızca programın ne kadar hızlı açıldığını değil; hata ayıklama, dağıtım, taşınabilirlik ve güvenlik tercihlerini de etkiler.
``

En temel haliyle derleyici, programın tamamını veya büyük bir bölümünü çalıştırmadan önce başka bir dile dönüştürür. Çoğu zaman hedef dil makine kodudur. Yorumlayıcı ise kaynak kodu ya da ara kodu çalıştırma anında analiz eder ve yürütür. Ancak modern dünyada bu ayrım, “biri hızlı, diğeri yavaş” cümlesinden daha zengindir: Java, C# ve JavaScript gibi diller ara gösterimler, sanal makineler ve **JIT** (Just-In-Time) derleme kullanabilir.

## Kodun dönüşüm hattı

Klasik bir C programı derlenirken birkaç mantıksal aşamadan geçer. Önce karakterler anlamlı parçalara ayrılır; buna **sözcüksel analiz** denir. Ardından kodun dilbilgisi kuralları incelenir, bir sözdizim ağacı oluşturulur ve tür kontrolleri yapılır. Son olarak derleyici optimizasyon uygulayarak hedef işlemciye uygun komutları üretir.

Bu süreci kabaca şöyle modelleyebiliriz:

$$Kaynak\ Kod \rightarrow AST \rightarrow Ara\ Temsil \rightarrow Makine\ Kodu$$

Bir programın toplam çalışma maliyetini de basitçe şu şekilde düşünebiliriz:

$$T_{toplam} = T_{hazırlık} + n \cdot T_{çalıştırma}$$

Burada $T_{hazırlık}$ derleme veya ilk analiz maliyeti, $n$ programın kaç kez çalıştırıldığıdır. Program milyonlarca kez çalışacaksa başlangıçtaki derleme maliyeti çoğu zaman mantıklı bir yatırımdır.

| Özellik | Derleyici | Yorumlayıcı |
|---|---|---|
| Dönüşüm zamanı | Çalıştırmadan önce | Çalıştırma sırasında |
| Tipik çıktı | Yerel çalıştırılabilir dosya | Anlık sonuç veya ara yürütme |
| İlk çalıştırma | Derleme bekletebilir | Genellikle hemen başlar |
| Tekrarlı çalışma | Çoğunlukla hızlıdır | Yorumlama ek yükü olabilir |
| Hata yakalama | Birçok hata derleme aşamasında | Bazı hatalar ilgili satıra gelince görünür |

## Küçük bir örnek, büyük fark

Aşağıdaki Python kodu yorumlayıcı tarafından yürütülebilir. Kod satırları analiz edilir, nesneler oluşturulur ve sonuç ekrana yazılır:

```python
# Sayıların kareleri toplamını hesaplar.
sayilar = [1, 2, 3, 4]
toplam = sum(sayi * sayi for sayi in sayilar)
print(toplam)
```

C tarafında ise benzer mantık önce derlenir, sonra oluşan ikili dosya çalıştırılır:

```c
#include <stdio.h>

int main(void) {
    int sayilar[] = {1, 2, 3, 4};
    int toplam = 0;

    for (int i = 0; i < 4; i++) {
        toplam += sayilar[i] * sayilar[i];
    }

    printf("%d\n", toplam);
    return 0;
}
```

Bu C dosyası örneğin `gcc kareler.c -o kareler` komutuyla derlenir. Ortaya çıkan `kareler` dosyası, uygun işletim sistemi ve işlemci mimarisinde doğrudan çalışabilir. Python örneğinde ise genellikle `python kareler.py` komutu Python çalışma zamanını devreye sokar.

## Hibrit modeller: İki dünyanın en sevilen özellikleri

Java kaynak kodu önce bytecode'a derlenir, ardından JVM tarafından yürütülür. JVM sık kullanılan kod parçalarını gözlemleyip onları JIT ile yerel makine koduna çevirebilir. Böylece başlangıçta taşınabilirlik, uzun süren işlerde ise performans hedeflenir.

| Yaklaşım | Örnekler | Güçlü yönü |
|---|---|---|
| AOT derleme | C, C++, Rust | Öngörülebilir yüksek performans |
| Saf yorumlama | Bash, klasik Python kullanımı | Hızlı deneme ve etkileşim |
| Bytecode + VM | Java, C# | Platform bağımsızlığı |
| JIT derleme | JavaScript motorları, JVM | Çalışma verisine göre optimizasyon |

Sonuç olarak derleyici ve yorumlayıcı rakip süper kahramanlar değil, farklı problemler için araçlardır. Sistem programlama, gömülü cihazlar ve performans kritik uygulamalar derleme ağırlıklı dünyaya yaklaşırken; otomasyon, veri analizi ve hızlı prototipleme yorumlayıcıların çevikliğinden yararlanır. En iyi seçim, kodun nerede, kaç kez ve hangi kısıtlarla çalışacağına bağlıdır.

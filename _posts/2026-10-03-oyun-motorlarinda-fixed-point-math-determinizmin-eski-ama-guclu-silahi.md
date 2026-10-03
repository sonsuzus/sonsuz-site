---
layout: post
title: "Oyun Motorlarında Fixed-Point Math: Determinizmin Eski Ama Güçlü Silahı"
math: true
categories: 
  - Bilgi
tags: 
  - fixed-point
  - oyun motoru
  - determinizm
  - matematik
  - c++
  - kayan nokta
toc: true
image: /img/oyun-motorlarinda-fixed-90.png
---

Bugün oyunlarda konum, hız ve fizik hesapları çoğunlukla kayan noktalı sayılarla yapılıyor. Ancak eski konsollardan deterministik strateji oyunlarına kadar pek çok sistem, ondalıklı değerleri tam sayıların içine saklayan **fixed-point math** yaklaşımını tercih etti. Bunun nedeni yalnızca işlemcilerin yavaş olması değildi; aynı girdilerden her donanımda aynı sonucu çıkarabilmek, özellikle ağ üzerinden oynanan ve tekrar kaydı tutan oyunlar için altın değerindeydi.
``
## Fixed-point sayı nedir?

Fixed-point, virgülün konumunu önceden sabitleyerek gerçek sayıları tam sayılarla temsil etme yöntemidir. Örneğin ölçek katsayısını $S=1000$ seçersek, $12.345$ değeri bellekte $12345$ olarak tutulur:

$$x_{fixed}=\operatorname{round}(x\cdot S)$$

Değeri yeniden yorumlamak için ise şu dönüşüm kullanılır:

$$x=\frac{x_{fixed}}{S}$$

Burada bilgisayar aslında virgülden habersizdir. Programcı, `12345` sayısının gerçekte `12.345` anlamına geldiğini bilir. İkili sistemlerde ölçek genellikle $2^n$ seçilir. Örneğin **Q16.16** biçiminde 32 bitlik sayının 16 biti tam, 16 biti kesir kısmını temsil eder. Ölçek $2^{16}=65536$ olur ve bölme işlemleri bit kaydırmayla hızlandırılabilir.

| Özellik | Fixed-point | Kayan nokta |
|---|---|---|
| Virgül konumu | Sabit | Üs değerine göre değişken |
| Hassasiyet | Belirlenen aralıkta sabit | Sayının büyüklüğüne bağlı |
| Donanım bağımsızlığı | Daha kolay sağlanır | Uygulamaya göre farklılaşabilir |
| Sayı aralığı | Daha dar | Çok geniş |
| Taşma riski | Açık ve yüksektir | Daha esnek, fakat özel değerler vardır |
| Determinizm | Kontrol edilmesi kolay | Ek önlemler gerektirir |

![oyun-motorlarinda-fixed-90](/img/oyun-motorlarinda-fixed-90.svg)


## Kayan nokta neden farklı sonuç verebilir?

IEEE 754 bir standart olsa da işlem sırası, derleyici optimizasyonları, ara değerlerin hassasiyeti ve işlemcinin kullandığı komut seti sonucu etkileyebilir. Üstelik kayan noktalı toplama birleşme özelliğine tam olarak uymaz:

$$(a+b)+c \neq a+(b+c)$$

Matematik öğretmeni bu satırı görünce kaşını kaldırabilir; fakat sınırlı bit sayısı nedeniyle her işlem yuvarlanır. Bir platform ara sonucu daha yüksek hassasiyetle tutarken diğeri hemen 32 bite indirebilir. Başlangıçta mikroskobik olan fark, binlerce fizik güncellemesinden sonra karakterlerin farklı konumlara gitmesine dönüşebilir.

Bu durum **lockstep** ağ modelinde büyük sorundur. Oyuncuların bütün dünya durumunu göndermek yerine yalnızca komutları paylaştığı bu modelde her makine aynı simülasyonu çalıştırır. Tek bir birim farklı koordinata ulaşırsa oyun durumları ayrışır ve meşhur “desync” canavarı sahneye çıkar.

## Basit bir Q16.16 uygulaması

Aşağıdaki C++ kodu, değerleri 16 kesir bitiyle saklar. Çarpma sırasında geçici olarak 64 bit kullanılması taşma ihtimalini azaltır:

```cpp
#include <cstdint>

struct Fixed {
    static constexpr int FRACTION_BITS = 16;
    static constexpr int64_t SCALE = 1LL << FRACTION_BITS;
    int32_t raw;

    static Fixed fromInt(int32_t value) {
        return {value << FRACTION_BITS};
    }

    static Fixed fromRatio(int32_t numerator, int32_t denominator) {
        return {static_cast<int32_t>(
            (static_cast<int64_t>(numerator) * SCALE) / denominator
        )};
    }

    Fixed operator+(Fixed other) const {
        return {raw + other.raw};
    }

    Fixed operator*(Fixed other) const {
        int64_t product = static_cast<int64_t>(raw) * other.raw;
        return {static_cast<int32_t>(product >> FRACTION_BITS)};
    }
};
```

Toplama doğrudan yapılabilir çünkü iki değer aynı ölçeği kullanır. Çarpmada ölçek karesi oluşur: $(aS)(bS)=abS^2$. Sonucu tekrar $S$ ölçeğine indirmek için 16 bit sağa kaydırırız.

## Bedeli olmayan sihir yok

Fixed-point deterministik olsa da otomatik olarak güvenli değildir. Taşma, yuvarlama biçimi, negatif sayılarda bit kaydırma davranışı ve farklı tamsayı genişlikleri açıkça tanımlanmalıdır. Bölme yapılırken sıfır kontrolü unutulmamalı; trigonometrik işlemler için arama tabloları veya deterministik yaklaşık fonksiyonlar kullanılmalıdır.

Modern işlemciler kayan noktada son derece hızlıdır. Bu yüzden fixed-point artık her oyun için zorunlu değildir. Yine de deterministik fizik, rollback netcode, tekrar sistemleri ve platformlar arası senkronizasyon gerektiğinde önemli bir araçtır. Kısacası fixed-point, virgülü ortadan kaldırmaz; onu programcının sorumluluğuna verir. Bu biraz daha fazla iş, karşılığında ise hesapların sürpriz yapmadığı sağlam bir simülasyon demektir.

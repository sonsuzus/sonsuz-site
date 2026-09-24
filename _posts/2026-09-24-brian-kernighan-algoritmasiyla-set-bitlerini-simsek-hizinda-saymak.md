---
layout: post
title: "Brian Kernighan Algoritmasıyla Set Bitlerini Şimşek Hızında Saymak"
math: true
categories: 
  - Bilgi
tags: 
  - bit-maskeleme
  - brian-kernighan
  - algoritma
  - popcount
  - düşük-seviye-programlama
toc: true
image: /img/brian-kernighan-algoritmasiyla-11.png
---

Bir tam sayının ikili gösteriminde kaç tane `1` bulunduğunu saymak ilk bakışta sıradan bir döngü problemi gibi görünür. Ancak düşük seviyeli programlamanın büyüsü, bazen bütün bitleri tek tek dolaşmak yerine yalnızca ilgilendiğimiz bitlere dokunabilmemizdir. Brian Kernighan algoritması, her turda sağdaki bir adet set bitini temizleyerek gereksiz döngüleri ortadan kaldıran zarif bir bit maskeleme hilesidir.
``
## Önce problemi ikili düşünelim

Bir bitin değeri `1` ise o bit **set edilmiş**, `0` ise temizlenmiş kabul edilir. Örneğin $n=52$ sayısının ikili gösterimi şöyledir:

$$52 = (110100)_2$$

Bu gösterimde üç tane `1` bulunduğundan sonuç 3'tür. Klasik yaklaşım, sayının en sağındaki biti `n & 1` ile kontrol eder ve ardından sayıyı sağa kaydırır. Sayı $b$ bit uzunluğundaysa bu yöntem yaklaşık $b$ tur çalışır.

| Yaklaşım | Her turdaki işlem | Döngü sayısı | Karmaşıklık |
|---|---|---:|---:|
| Sağa kaydırma | Her biti kontrol eder | Bit uzunluğu kadar | $O(b)$ |
| Brian Kernighan | Yalnızca bir set bitini siler | Set bit sayısı kadar | $O(k)$ |
| Donanımsal `popcount` | İşlemci komutu kullanır | Mimariye bağlı | Genellikle sabit |

![brian-kernighan-algoritmasiyla-11](/img/brian-kernighan-algoritmasiyla-11.svg)


Burada $k$, sayının içindeki `1` bitlerinin sayısıdır. Seyrek bitli sayılarda $k \ll b$ olduğundan fark oldukça belirgin olabilir.

## Hilenin kalbi: `n & (n - 1)`

Algoritmanın temel ifadesi şudur:

```text
n = n & (n - 1)
```

Bir sayıdan 1 çıkarıldığında, en sağdaki set bit `0` olur; onun sağındaki bütün `0` bitleri ise `1` olur. Ardından eski sayı ile yeni sayı arasında AND işlemi yapıldığında bu değişen alt bitler temizlenir. Sonuç olarak sayının en sağındaki tek bir `1` yok edilir.

Örneğin $52$ üzerinden ilerleyelim:

| Tur | `n` değeri | İkili gösterim | Temizlenen bit sonrası |
|---:|---:|---|---|
| 1 | 52 | `110100` | `110000` |
| 2 | 48 | `110000` | `100000` |
| 3 | 32 | `100000` | `000000` |

Sayı sıfıra üç turda ulaştığı için set bit sayısı da 3'tür. Algoritma, aradaki sıfırlarla hiç vakit kaybetmez.

## C ile uygulama

Aşağıdaki fonksiyon, işaretsiz bir tam sayıdaki set bitlerini sayar:

```c
unsigned int count_set_bits(unsigned int n) {
    unsigned int count = 0;

    while (n != 0) {
        n &= (n - 1);  // En sağdaki set bitini temizler.
        count++;
    }

    return count;
}
```

`unsigned int` kullanılması önemlidir. İşaretli negatif sayıların gösterimi ve taşma davranışları dile göre kafa karıştırabilir. İşaretsiz tür, işlemin sabit genişlikte bir bit deseni üzerinde gerçekleştiğini daha açık biçimde ifade eder.

Python'da aynı fikir neredeyse birebir yazılabilir:

```python
def count_set_bits(n: int) -> int:
    if n < 0:
        raise ValueError("n negatif olmamalıdır")

    count = 0
    while n:
        n &= n - 1
        count += 1
    return count
```

## Ne zaman tercih edilmeli?

Bu yöntem; bit bayraklarını analiz ederken, izin sistemlerinde etkin seçenekleri sayarken, grafik algoritmalarındaki bit kümelerinde ve gömülü sistemlerde oldukça kullanışlıdır. Yine de modern dillerin `bit_count`, `popcount` veya benzeri yerleşik fonksiyonları işlemcinin özel komutlarından yararlanabilir. Python'da örneğin `n.bit_count()` çoğunlukla elle yazılan döngüden daha hızlıdır.

Brian Kernighan yaklaşımının asıl değeri yalnızca performans değildir. `n & (n - 1)` ifadesi, bitlerin matematiksel yapısını kullanarak problemi dönüştürür: bütün bitleri aramak yerine bulunan her `1` doğrudan silinir. Kısacası algoritma samanlıkta iğne aramaz; iğneleri sırayla ortadan kaldırır.

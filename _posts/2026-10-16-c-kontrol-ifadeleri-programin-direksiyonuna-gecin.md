---
layout: post
title: "C Kontrol İfadeleri: Programın Direksiyonuna Geçin"
math: true
categories: 
  - Bilgi
tags: 
  - c
  - programlama
  - kontrol ifadeleri
  - if else
  - switch case
  - döngüler
toc: true
image: /img/c-kontrol-ifadeleri-20.png
---

Bir C programı, yalnızca yukarıdan aşağıya çalışan komutlardan oluşsaydı hesap makinesinden pek farklı olmazdı. Kullanıcı kararlarına tepki vermek, bazı işlemleri tekrarlamak ve farklı durumlarda farklı yollar izlemek için kontrol ifadelerine ihtiyaç duyarız. `if-else`, `switch-case` ve döngüler, programın direksiyonunu elimize veren temel araçlardır.

``

## Kontrol akışının teorik temeli

Kontrol ifadeleri, bir koşulun doğruluk değerine göre program sayacının hangi komuta ilerleyeceğini belirler. C dilinde **0 yanlış**, sıfır dışındaki değerler ise **doğru** kabul edilir. Örneğin `5 > 2` ifadesinin sonucu `1`, `5 == 2` ifadesinin sonucu `0` olur.

Mantıksal ifadeler matematiksel olarak şöyle düşünülebilir:

$$
sonuc = (A \land B) \lor \neg C
$$

C dilindeki karşılığı ise `(A && B) || !C` biçimindedir. Burada `&&` VE, `||` VEYA, `!` ise DEĞİL operatörüdür.

| Yapı | Kullanım amacı | Uygun olduğu durum |
|---|---|---|
| `if-else` | Koşula göre karar vermek | Aralıklar ve karmaşık mantıksal ifadeler |
| `switch-case` | Bir değeri sabit seçeneklerle karşılaştırmak | Menü ve durum kodları |
| `for` | Belirli sayıda tekrar yapmak | Sayaç kontrollü işlemler |
| `while` | Koşul doğru olduğu sürece çalışmak | Tekrar sayısı önceden bilinmeyen işlemler |
| `do-while` | İşlemi en az bir kez çalıştırmak | Menü ve kullanıcı girdisi doğrulama |

## `if-else` ile yol ayrımları

`if-else`, programın “Bu doğruysa ne yapmalıyım?” sorusuna verdiği cevaptır. Bir öğrencinin notunu sınıflandıran örnek şöyledir:

```c
int not = 76;

if (not >= 85) {
    printf("Pekiyi\n");
} else if (not >= 70) {
    printf("İyi\n");
} else if (not >= 50) {
    printf("Geçer\n");
} else {
    printf("Başarısız\n");
}
```

Koşullar yukarıdan aşağıya sınanır ve ilk doğru dal çalıştırılır. Bu nedenle daha geniş bir koşulu başa yazmak mantık hatası oluşturabilir. Örneğin `not >= 50` ilk sırada olsaydı 90 alan öğrenci bile yalnızca “Geçer” sonucunu görürdü.

## `switch-case` ile düzenli seçimler

Tek bir değişkenin belirli sabit değerlerini kontrol ederken uzun bir `if-else` zinciri yerine `switch-case` daha okunaklıdır:

```c
int secim = 2;

switch (secim) {
    case 1:
        printf("Yeni oyun başlatıldı.\n");
        break;
    case 2:
        printf("Ayarlar açıldı.\n");
        break;
    case 3:
        printf("Program kapatılıyor.\n");
        break;
    default:
        printf("Geçersiz seçim!\n");
}
```

`break`, eşleşen bölüm tamamlandıktan sonra `switch` yapısından çıkılmasını sağlar. Yazılmazsa program sonraki `case` bloklarına da düşer; buna **fall-through** denir. Bazen bilinçli kullanılsa da çoğunlukla küçük ve sinsi bir böcektir.

## Döngüler: Bilgisayarın yorulmayan tarafı

Bir işlemi tekrar tekrar yazmak yerine döngü kullanırız. İlk beş pozitif sayının toplamını hesaplayalım:

```c
int toplam = 0;

for (int i = 1; i <= 5; i++) {
    toplam += i;
}

printf("Toplam: %d\n", toplam);
```

Bu işlemin matematiksel karşılığı şöyledir:

$$
\sum_{i=1}^{5} i = \frac{5(5+1)}{2} = 15
$$

`for` döngüsünde başlangıç, devam koşulu ve güncelleme aynı satırda bulunur. `while` önce koşulu denetlediği için hiç çalışmayabilir. `do-while` ise koşulu sonda denetler ve gövdeyi en az bir kez yürütür.

```c
int sayi;

do {
    printf("Pozitif bir sayı girin: ");
    scanf("%d", &sayi);
} while (sayi <= 0);
```

Döngülerde koşulun bir noktada yanlış olmasına dikkat edilmelidir; aksi hâlde sonsuz döngü oluşur. `break` döngüyü tamamen bitirirken `continue` yalnızca mevcut turu atlar. Kısacası doğru kontrol yapısını seçmek, hem okunabilir hem güvenilir C programları yazmanın temelidir.

![c-kontrol-ifadeleri-20](/img/c-kontrol-ifadeleri-20.svg)


---
layout: post
title: "Manacher Algoritması: En Uzun Palindromik Alt Dizeyi O(n) Zamanda Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - manacher algoritması
  - palindrom
  - algoritmalar
toc: true
---

Bir metindeki en uzun palindromu bulmak, ilk bakışta her merkezden sağa ve sola yürümeyi gerektiren yorucu bir iş gibi görünür. Manacher algoritması ise daha önce incelenmiş palindromların simetrisinden yararlanarak aynı karakterleri tekrar tekrar karşılaştırmaz ve problemi doğrusal zamanda çözer. Küçük bir terminoloji notu: Algoritma, karakterlerin bitişik olduğu en uzun palindromik **alt dizeyi** bulur; palindromik alt dizi problemi farklıdır.

``

## Temel problem ve klasik yaklaşımlar

Palindrom, tersten okunduğunda değişmeyen metindir. Örneğin `kabak`, `ada` ve `abba` birer palindromdur. Uzunluğu $n$ olan bir metinde bütün alt dizeleri üretmek $O(n^2)$ aday oluşturur; her adayı kontrol etmek toplam maliyeti $O(n^3)$ seviyesine çıkarabilir.

Her karakteri olası merkez kabul edip iki yöne genişlemek daha iyidir. Ancak `aaaaaaa` gibi metinlerde aynı bölgeler defalarca incelendiğinden karmaşıklık hâlâ $O(n^2)$ olur. Manacher’ın hedefi bu tekrarları ortadan kaldırmaktır.

| Yaklaşım | Zaman | Ek alan | Temel fikir |
|---|---:|---:|---|
| Tüm alt dizeleri deneme | $O(n^3)$ | $O(1)$ | Her aralığı ayrı kontrol eder |
| Merkezden genişleme | $O(n^2)$ | $O(1)$ | Her merkezi bağımsız işler |
| Dinamik programlama | $O(n^2)$ | $O(n^2)$ | Alt problemlerin sonuçlarını saklar |
| Manacher | $O(n)$ | $O(n)$ | Bilinen palindromların simetrisini kullanır |

## Tek ve çift uzunlukları birleştirmek

Tek uzunluklu `kabak` palindromunun merkezi bir karakterdir; çift uzunluklu `abba` palindromunun merkeziyse iki karakterin arasındadır. İki durumu ayrı yönetmemek için metni dönüştürürüz:

```text
abba → ^#a#b#b#a#$
```

`#` işaretleri bütün palindromları tek tip, yani tek uzunluklu hâle getirir. `^` ve `$` sınır nöbetçileridir; genişleme sırasında dizi sınırlarını ayrıca kontrol etme ihtiyacını azaltırlar.

Dönüştürülmüş metindeki her $i$ konumu için $P[i]$, merkezden eşleşen karakter sayısını tutar. Böylece en büyük değer doğrudan orijinal metindeki palindrom uzunluğunu verir:

$$L = \max_i P[i]$$

## Simetri numarası

Algoritma, şimdiye kadar sağa en çok uzanan palindromun merkezini $C$, sağ sınırını ise $R$ olarak saklar. Eğer yeni konum $i<R$ ise onun ayna konumu

$$i' = 2C-i$$

olur. Ayna merkezindeki bilgi güvenli sınırı aşmadığı sürece kopyalanabilir:

$$P[i] = \min(R-i, P[i'])$$

Ardından yalnızca henüz bilinmeyen bölge karşılaştırılır. Palindrom $R$ sınırını geçerse $C$ ve $R$ güncellenir. İşte doğrusal performansın sırrı budur: sağ sınır toplamda en fazla dönüştürülmüş metnin uzunluğu kadar ilerler.

## Python uygulaması

```python
def en_uzun_palindrom(metin):
    if not metin:
        return ""

    t = "^#" + "#".join(metin) + "#$"
    p = [0] * len(t)
    merkez = sag = 0

    for i in range(1, len(t) - 1):
        ayna = 2 * merkez - i

        if i < sag:
            p[i] = min(sag - i, p[ayna])

        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1

        if i + p[i] > sag:
            merkez = i
            sag = i + p[i]

    uzunluk, merkez_indisi = max(
        (deger, indis) for indis, deger in enumerate(p)
    )
    baslangic = (merkez_indisi - uzunluk) // 2
    return metin[baslangic:baslangic + uzunluk]

print(en_uzun_palindrom("muzkabaklimon"))  # kabak
```

Dönüşümde eklenen ayraçlar nedeniyle orijinal başlangıç konumu $(merkez\_indisi-uzunluk)/2$ formülüyle hesaplanır. Kod hem tek hem çift uzunluklu palindromları aynı akışta işler.

## Neden gerçekten doğrusal?

İç içe bir `while` döngüsü görmek şüphe uyandırabilir. Fakat başarısız veya yeni karşılaştırmalar sağ sınırı ileri taşır; önceden bilinen bölümler simetriden alınır. Bu nedenle toplam çalışma süresi $O(n)$, yarıçap dizisi ve dönüştürülmüş metin nedeniyle alan maliyeti $O(n)$ olur. Özellikle DNA dizileri, log analizi ve büyük metinlerde palindrom arama gibi senaryolarda Manacher, algoritmik simetrinin ne kadar güçlü olabileceğini gösteren zarif bir çözümdür.

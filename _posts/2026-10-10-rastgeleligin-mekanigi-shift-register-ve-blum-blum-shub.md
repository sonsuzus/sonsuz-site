---
layout: post
title: "Rastgeleliğin Mekaniği: Shift-Register ve Blum Blum Shub"
math: true
categories: 
  - Bilgi
tags: 
  - rastgele-sayılar
  - kriptografi
  - lfsr
  - blum-blum-shub
  - algoritmalar
toc: true
image: /img/rastgeleligin-mekanigi-shift-95.png
---

![rastgeleligin-mekanigi-shift-95](/img/rastgeleligin-mekanigi-shift-95.svg)


Bilgisayarlar zar atamaz, kahve falına bakamaz ve içlerinden geldiği gibi sayı seçemez. Deterministik makineler oldukları için aynı başlangıç koşullarında aynı sonucu üretirler. Buna rağmen oyunlardan simülasyonlara, testlerden kriptografiye kadar rastgele görünen sayılara ihtiyaç duyarız. İşte sözde rastgele sayı üreteçleri, kısa bir başlangıç değerini uzun ve karmaşık görünen bir diziye dönüştürerek bu ihtiyacı karşılar.
``

## Gerçek rastgelelik ile sözde rastgelelik

Gerçek rastgele sayı üreteçleri termal gürültü, radyoaktif bozunma veya atmosferik parazit gibi fiziksel olaylardan yararlanır. Sözde rastgele sayı üreteçleri ise bir **tohum** (seed) ve matematiksel durum geçişi kullanır. Tohum biliniyorsa dizi yeniden üretilebilir.

| Özellik | Gerçek rastgelelik | Sözde rastgelelik |
|---|---|---|
| Kaynak | Fiziksel olay | Deterministik algoritma |
| Tekrarlanabilirlik | Genellikle hayır | Evet |
| Hız | Görece düşük | Çok yüksek |
| Kullanım | Anahtar üretimi | Simülasyon, oyun, test |

Bir üretecin kalitesi yalnızca sayıların dağınık görünmesine bağlı değildir. Periyot uzunluğu, istatistiksel dağılım, tahmin edilebilirlik ve iç durumun ele geçirilmesine karşı dayanıklılık da önemlidir.

## Shift-register: Bitleri kaydır, geri besle

En bilinen shift-register yaklaşımı **Linear Feedback Shift Register**, yani LFSR'dir. LFSR, belirli uzunluktaki bit dizisini her adımda kaydırır. Yeni bit, seçilmiş bitlerin XOR işleminden elde edilir. XOR işlemi ikili alanda toplama anlamına gelir:

$$b_{yeni} = b_i \oplus b_j \oplus \cdots$$

$n$ bitlik uygun bir LFSR'nin ulaşabileceği en yüksek periyot:

$$T = 2^n - 1$$

Sıfırlardan oluşan durum dışarıda kalır; çünkü XOR sonucunda sürekli sıfır üretir. Geri besleme noktaları doğru seçilirse sayaç gibi görünmeyen, uzun bir bit dizisi elde edilir.

```python
def lfsr(seed, taps, count):
    state = seed.copy()
    output = []

    for _ in range(count):
        output.append(state[-1])
        feedback = 0
        for index in taps:
            feedback ^= state[index]
        state = [feedback] + state[:-1]

    return output

print(lfsr([1, 0, 0, 1], [0, 3], 20))
```

Bu kod, kayıtçının son bitini çıktı olarak alır; seçilen konumlardaki bitleri XOR'layıp başa ekler. LFSR hızlıdır ve donanımda birkaç mantık kapısıyla uygulanabilir. Ancak doğrusal yapısı nedeniyle yeterli çıktı gözlemlendiğinde iç durumu hesaplanabilir. Dolayısıyla tek başına kriptografik olarak güvenli değildir.

## Blum Blum Shub: Modüler aritmetiğin ağır topu

Blum Blum Shub, güvenliğini büyük sayıların çarpanlara ayrılmasının zorluğuna dayandırır. Önce $p$ ve $q$ biçiminde, her ikisi de $3$ mod $4$ değerine eşit iki büyük asal seçilir. Ardından:

$$M = p q$$

Tohum $x_0$, $M$ ile aralarında asal olacak şekilde belirlenir. Her adımda durum şu formülle güncellenir:

$$x_{n+1} = x_n^2 \bmod M$$

Çıktı olarak çoğunlukla $x_n$ değerinin en düşük anlamlı biti kullanılır.

```python
def blum_blum_shub(seed, p, q, count):
    modulus = p * q
    state = seed
    bits = []

    for _ in range(count):
        state = pow(state, 2, modulus)
        bits.append(state & 1)

    return bits

print(blum_blum_shub(5, 499, 547, 20))
```

Buradaki `pow(state, 2, modulus)` ifadesi modüler karesini verimli biçimde hesaplar. Örnekteki asallar öğretim amacıyla küçüktür; gerçek güvenlik için çok daha büyük değerler gerekir. Tohumun gizli ve uygun seçilmesi de zorunludur.

## İki yöntemin karşılaşması

| Ölçüt | LFSR | Blum Blum Shub |
|---|---|---|
| Temel işlem | Kaydırma ve XOR | Modüler karesini alma |
| Hız | Çok yüksek | Düşük |
| Donanım uygulaması | Çok kolay | Daha maliyetli |
| Güvenlik | Tek başına zayıf | Uygun parametrelerle güçlü |
| Tipik kullanım | Haberleşme, test, donanım | Kriptografik bit üretimi |

LFSR bir yarış motosikleti gibidir: hızlı ve hafif, fakat korumasızdır. Blum Blum Shub ise zırhlı araçtır; daha güvenli ilerler ama performans bedeli ödetir. Bu nedenle algoritma seçerken yalnızca çıktının rastgele görünmesine değil, saldırganın tohumu veya iç durumu tahmin edip edemeyeceğine bakılmalıdır. Simülasyonda hız öne çıkarken, anahtar ve güvenlik belirteci üretiminde kriptografik güvenlik vazgeçilmezdir.

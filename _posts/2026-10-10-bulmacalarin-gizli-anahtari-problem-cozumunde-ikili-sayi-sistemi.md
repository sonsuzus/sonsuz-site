---
layout: post
title: "Bulmacaların Gizli Anahtarı: Problem Çözümünde İkili Sayı Sistemi"
math: true
categories: 
  - Bilgi
tags: 
  - ikili sistem
  - algoritma
  - problem çözme
  - matematik
  - bulmaca
  - python
toc: true
image: /img/bulmacalarin-gizli-anahtari-13.png
---

![bulmacalarin-gizli-anahtari-13](/img/bulmacalarin-gizli-anahtari-13.svg)


Bilgisayarların yalnızca sıfır ve birlerle çalışması ilk bakışta teknolojik bir sınırlama gibi görünebilir. Oysa ikili sayı sistemi, klasik mantık bulmacalarında bilgiyi düzenlemek, olasılıkları kodlamak ve en az sayıda işlemle sonuca ulaşmak için kullanılan son derece güçlü bir araçtır. Zehirli şişelerden ağırlık tartma sorularına kadar pek çok problem, doğru açıdan bakıldığında aslında gizlenmiş birer ikili kodlama egzersizidir.

``

## İkili sistem neden bu kadar kullanışlı?

Onluk sistemde her basamak 0 ile 9 arasında değer alırken ikili sistemde yalnızca iki durum bulunur: **0** ve **1**. Bunlar hayır–evet, kapalı–açık, başarısız–başarılı veya hafif–ağır gibi iki seçenekli durumları temsil edebilir.

Bir ikili sayının değeri şöyle hesaplanır:

$$
N = b_0 2^0 + b_1 2^1 + b_2 2^2 + ... + b_k 2^k
$$

Burada her $b_i$ yalnızca 0 veya 1 olabilir. Örneğin $1011_2$ sayısı:

$$
1 × 2^3 + 0 × 2^2 + 1 × 2^1 + 1 × 2^0 = 11
$$

Bu gösterimin problem çözmedeki asıl avantajı, $k$ adet iki durumlu gözlemle $2^k$ farklı olasılığı ayırt edebilmesidir.

| Gözlem sayısı | Kodlanabilen olasılık | Örnek kodlar |
|---:|---:|---|
| 1 | $2^1 = 2$ | 0, 1 |
| 2 | $2^2 = 4$ | 00, 01, 10, 11 |
| 3 | $2^3 = 8$ | 000–111 |
| 10 | $2^{10} = 1024$ | 0000000000–1111111111 |

## Zehirli şişe bulmacası

Klasik soruyu düşünelim: **1000 şişeden biri zehirli ve yalnızca 10 test şeridimiz var. Tek turda zehirli şişeyi nasıl buluruz?** Her şişeyi ayrı ayrı test etmek mümkün değildir. Fakat $2^{10}=1024$ olduğu için 10 şerit, 1024 farklı sonucu kodlayabilir.

Şişeleri 0 ile 999 arasında numaralandırır ve numaraları 10 bitlik ikili biçimde yazarız. Bir şişenin ikili gösterimindeki hangi bitler 1 ise o şişeden ilgili test şeritlerine örnek damlatırız. Örneğin 13 numaralı şişenin kodu `0000001101` olur; dolayısıyla 1 değerine sahip bitlerin karşılık geldiği şeritlere eklenir.

Bekleme sonunda pozitif çıkan şeritler 1, negatif çıkanlar 0 kabul edilir. Ortaya çıkan ikili sayı doğrudan zehirli şişenin numarasıdır. Buradaki sihir aslında sihir değil, her şişeye benzersiz bir **bit deseni** vermektir.

## Ağırlıklarla ölçme bulmacası

Elimizde 1, 2, 4 ve 8 kilogramlık ağırlıklar varsa 1 ile 15 kilogram arasındaki her tam değeri ölçebiliriz. Çünkü bu ağırlıklar ikinin kuvvetleridir:

$$
1 + 2 + 4 + 8 = 15
$$

Örneğin 13 kilogram, $1101_2$ biçimindedir. Bu nedenle 8, 4 ve 1 kilogramlık ağırlıklar kullanılır; 2 kilogramlık ağırlık kullanılmaz.

| İkili basamak | Ağırlık | 13 kg için durum |
|---|---:|---|
| $2^3$ | 8 kg | Kullan |
| $2^2$ | 4 kg | Kullan |
| $2^1$ | 2 kg | Kullanma |
| $2^0$ | 1 kg | Kullan |

## Aynı fikri Python ile görmek

Aşağıdaki kod, bir sayıyı oluşturmak için hangi ikinin kuvvetlerinin seçilmesi gerektiğini bulur:

```python
def secilen_agirliklar(hedef):
    agirliklar = []
    bit = 0

    while hedef > 0:
        if hedef & 1:
            agirliklar.append(2 ** bit)
        hedef >>= 1
        bit += 1

    return agirliklar

print(secilen_agirliklar(13))  # [1, 4, 8]
```

`hedef & 1` işlemi en sağdaki bitin 1 olup olmadığını denetler. `hedef >>= 1` ise sayıyı bir bit sağa kaydırarak sıradaki basamağa geçer. Böylece algoritma, sayının ikili gösterimini doğrudan seçilecek ağırlıklara dönüştürür.

## Bulmacalarda ikili düşünme yöntemi

Bir soruda çok sayıda aday ve yalnızca iki sonuç üreten testler varsa şu adımlar uygulanabilir:

1. Olasılık sayısını $n$ olarak belirle.
2. $2^k ≥ n$ koşulunu sağlayan en küçük $k$ değerini bul.
3. Her adaya benzersiz bir $k$ bitlik kod ata.
4. Her testi kodun bir basamağıyla ilişkilendir.
5. Sonuç bitlerini birleştirerek doğru adayı belirle.

Kısacası ikili sistem yalnızca bilgisayarların dili değildir; sınırlı gözlemlerden maksimum bilgi çıkarma yöntemidir. Bir bulmacada “açık veya kapalı”, “doğru veya yanlış” gibi iki durumlu sonuçlar görüyorsanız, çözümün bir köşesinde büyük olasılıkla ikinin kuvvetleri gülümsüyordur.

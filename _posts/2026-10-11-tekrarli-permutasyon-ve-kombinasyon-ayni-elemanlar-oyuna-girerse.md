---
layout: post
title: "Tekrarlı Permütasyon ve Kombinasyon: Aynı Elemanlar Oyuna Girerse"
math: true
categories: 
  - Bilgi
tags: 
  - matematik
  - permütasyon
  - kombinasyon
  - algoritma
  - python
toc: true
image: /img/tekrarli-permutasyon-ve-37.png
---

![tekrarli-permutasyon-ve-37](/img/tekrarli-permutasyon-ve-37.svg)


Bir çekmecede birbirinden ayırt edilemeyen çoraplar, bir şifrede tekrar kullanılabilen rakamlar veya dağıtılmayı bekleyen özdeş şekerler varsa klasik sayma formülleri tek başına yeterli olmayabilir. Çünkü tekrar eden elemanlar bazı düzenlemeleri aynı hâle getirirken, tekrar seçimine izin verilmesi yeni olasılıklar doğurur. İsimleri benzese de **tekrarlı permütasyon** ile **tekrarlı kombinasyon** farklı problemlere cevap verir.
``
## Önce klasik durumu hatırlayalım

Birbirinden farklı $n$ elemanın tamamı sıralanıyorsa klasik permütasyon formülü şöyledir:

$$P(n)=n!$$

Örneğin A, B ve C harfleri $3!=6$ farklı şekilde sıralanabilir. Sıra önemli değilse ve bu elemanlardan $r$ tanesi seçilecekse kombinasyon kullanılır:

$$\binom{n}{r}=\frac{n!}{r!(n-r)!}$$

Buradaki gizli kahraman, elemanların **ayırt edilebilir** olmasıdır. Elemanlar aynı görünmeye veya seçim sırasında yeniden kullanılmaya başladığında hikâye değişir.

## Tekrarlı permütasyon: Aynı elemanlar yer değiştirirse

$ n $ elemanlı bir dizide bazı elemanlar özdeşse, bunların kendi aralarındaki yer değişimleri yeni bir düzen üretmez. Birinci türden $n_1$, ikinci türden $n_2$ ve devamında $n_k$ adet aynı eleman bulunduğunda:

$$\frac{n!}{n_1!n_2!\cdots n_k!}$$

Örneğin **KAKAO** kelimesinde 5 harf vardır; K ve A ikişer kez, O ise bir kez geçer. Bütün harfleri farklı saysaydık $5!$ düzen bulurduk. Ancak iki K'nin ve iki A'nın yer değiştirmesi sonucu değiştirmez:

$$\frac{5!}{2!2!}=30$$

Paydadaki faktöriyeller, yanlışlıkla birden fazla saydığımız özdeş düzenlemeleri temizleyen birer matematik süpürgesi gibidir.

> Dikkat: Şifre oluştururken aynı karakterin yeniden kullanılabilmesi farklı bir durumdur. $n$ seçenekle $r$ basamaklı ve sıralı bir kod oluşturuluyorsa sonuç $n^r$ olur. Bu da bazen “tekrarlı permütasyon” diye adlandırılır; fakat özdeş elemanların dizilmesinden kavramsal olarak ayrılır.

## Tekrarlı kombinasyon: Seç, istersen yine seç

Sıranın önemsiz olduğu ve aynı türün birden fazla seçilebildiği problemlerde tekrarlı kombinasyon kullanılır. $n$ farklı türden toplam $r$ seçim yapmanın sayısı:

$$\binom{n+r-1}{r}=\binom{n+r-1}{n-1}$$

Örneğin çikolata, vanilya ve çilek olmak üzere 3 dondurma çeşidinden 4 top seçelim. Dört topun tamamı çikolata olabilir; tekrar serbesttir. Sonuç:

$$\binom{3+4-1}{4}=\binom{6}{4}=15$$

Bu formülün arkasında **yıldız ve çubuklar** yöntemi bulunur. Dört topu yıldızlarla, üç çeşidi ayıran iki sınırı çubuklarla gösteririz: `**|*|*`. Toplam altı konumdan iki çubuğun yerlerini seçmek, dağılımı belirlemeye yeterlidir.

| Problem türü | Sıra önemli mi? | Tekrar var mı? | Formül |
|---|---:|---:|---:|
| Klasik permütasyon | Evet | Hayır | $n!$ |
| Özdeş elemanlı permütasyon | Evet | Elemanlar zaten tekrar eder | $\frac{n!}{n_1!\cdots n_k!}$ |
| Klasik kombinasyon | Hayır | Hayır | $\binom{n}{r}$ |
| Tekrarlı kombinasyon | Hayır | Evet | $\binom{n+r-1}{r}$ |
| Tekrarlı sıralı seçim | Evet | Evet | $n^r$ |

## Python ile hesaplama

Aşağıdaki fonksiyonlar özdeş elemanlı permütasyonu ve tekrarlı kombinasyonu doğrudan hesaplar:

```python
from math import factorial, comb

def ozdes_perm(*adetler):
    toplam = sum(adetler)
    sonuc = factorial(toplam)
    for adet in adetler:
        sonuc //= factorial(adet)
    return sonuc

def tekrarli_kombinasyon(tur_sayisi, secim_sayisi):
    return comb(tur_sayisi + secim_sayisi - 1, secim_sayisi)

print(ozdes_perm(2, 2, 1))          # KAKAO: 30
print(tekrarli_kombinasyon(3, 4))   # Dondurma seçimi: 15
```

İlk fonksiyon toplam eleman sayısının faktöriyelini hesaplayıp her özdeş grubun faktöriyeline böler. İkinci fonksiyon ise Python'ın `comb` aracılığıyla yıldız ve çubuklar formülünü uygular.

Bir soruda formüle atlamadan önce üç soru sorun: **Sıra önemli mi, elemanlar ayırt edilebilir mi, tekrar seçimine izin var mı?** Bu küçük kontrol listesi, benzer görünen sayma problemlerini birbirinden ayırır ve faktöriyeller arasında kaybolmanızı önler.

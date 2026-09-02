---
layout: post
title: "Çin Kalan Teoremiyle Olimpiyat Şifrelerini Kırmak"
math: true
categories: 
  - Bilgi
tags: 
  - çin kalan teoremi
  - modüler aritmetik
  - matematik olimpiyatları
toc: true
---

Bir kasanın şifresi doğrudan verilmek yerine “3 ile bölündüğünde 2, 5 ile bölündüğünde 3, 7 ile bölündüğünde 2 kalanını bırakıyor” şeklinde saklansaydı ne yapardınız? Matematik olimpiyatlarında sıkça karşımıza çıkan bu tür şifrelerin anahtarı, farklı modüler bilgilerden tek bir ortak sayı üreten **Çin Kalan Teoremi**dir.
``
## Teoremin temel fikri

Bir $x$ sayısı için aşağıdaki sistem verilsin:

$$
x \equiv a_1 \pmod{m_1},\qquad
x \equiv a_2 \pmod{m_2},\qquad
\ldots
$$

Modüller $m_1,m_2,\ldots,m_k$ ikişer ikişer aralarında asal ise sistemin

$$M=m_1m_2\cdots m_k$$

modülünde **tek bir çözüm sınıfı** vardır. Buradaki tekillik, yalnızca bir tam sayı bulunduğu anlamına gelmez. Eğer $x_0$ çözümse bütün çözümler

$$x=x_0+tM,\qquad t\in\mathbb Z$$

biçimindedir. Yani $0\leq x<M$ aralığında tam olarak bir çözüm bulunur.

| Durum | Sonuç | Olimpiyat yorumu |
|---|---|---|
| Modüller ikişer ikişer aralarında asal | Çözüm her zaman vardır ve modulo $M$ tektir | Klasik Çin Kalan Teoremi |
| Modüller aralarında asal değil | Çözüm olmayabilir | Tutarlılık kontrolü gerekir |
| Ortak bölen kalan farkını bölüyor | Çözüm vardır ve modulo EKOK’ta tektir | Genelleştirilmiş teorem |
| Ortak bölen kalan farkını bölmüyor | Çözüm yoktur | Verilen şifre geçersizdir |

İki denklem için geçerlilik koşulu özellikle kullanışlıdır:

$$x\equiv a\pmod m,\qquad x\equiv b\pmod n$$

sisteminin çözülebilmesi için ve ancak

$$a\equiv b\pmod{\gcd(m,n)}$$

olmalıdır.

## Örnek şifreyi adım adım kıralım

Şifremiz şu koşulları sağlasın:

$$x\equiv2\pmod3,
\quad x\equiv3\pmod5,
\quad x\equiv2\pmod7.$$

Modüller aralarında asaldır ve $M=3\cdot5\cdot7=105$ olur. Yapıcı yöntemde $M_i=M/m_i$ değerlerini hesaplarız:

| $m_i$ | $a_i$ | $M_i$ | $M_i^{-1}\pmod{m_i}$ |
|---:|---:|---:|---:|
| 3 | 2 | 35 | 2 |
| 5 | 3 | 21 | 1 |
| 7 | 2 | 15 | 1 |

Örneğin $35\equiv2\pmod3$ ve $2\cdot2\equiv1\pmod3$ olduğundan ilk ters 2’dir. Formülümüz:

$$x\equiv\sum_{i=1}^{k}a_iM_iM_i^{-1}\pmod M.$$

Değerleri yerleştirirsek

$$x\equiv2\cdot35\cdot2+3\cdot21\cdot1+2\cdot15\cdot1=233\equiv23\pmod{105}.$$

Dolayısıyla en küçük pozitif şifre **23**’tür. Kontrol etmek önemlidir: $23$ sayısı sırasıyla 3, 5 ve 7 ile bölündüğünde 2, 3 ve 2 kalanlarını verir.

## Kodla doğrulama

Aşağıdaki Python fonksiyonu, ikişer ikişer aralarında asal modüller için yapıcı formülü uygular. `pow(Mi, -1, mi)` ifadesi modüler tersi hesaplar.

```python
def cin_kalan(kalanlar, moduller):
    M = 1
    for m in moduller:
        M *= m

    sonuc = 0
    for ai, mi in zip(kalanlar, moduller):
        Mi = M // mi
        ters = pow(Mi, -1, mi)
        sonuc += ai * Mi * ters

    return sonuc % M

print(cin_kalan([2, 3, 2], [3, 5, 7]))  # 23
```

## Olimpiyatlarda nasıl görünür?

Sorular teoremin adını çoğu zaman söylemez. Bir sayının farklı bölenlerle kalanları, periyodik olayların ilk ortak zamanı veya basamakları gizlenmiş bir sayı verilebilir. Bazen de “en küçük pozitif çözüm” yerine belirli bir aralıktaki çözüm sorulur. Önce $x_0$ temel çözümü bulunur, ardından $x=x_0+tM$ ailesinden uygun $t$ seçilir.

En güvenilir strateji üç adımdır: modüllerin uyumluluğunu kontrol et, ortak çözümü kur ve sonucu bütün denklemlerde doğrula. Böylece Çin Kalan Teoremi, ezberlenen bir formülden çıkıp olimpiyat kasalarını açan sağlam bir maymuncuğa dönüşür.

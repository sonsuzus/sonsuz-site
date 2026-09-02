---
layout: post
title: "LCG’nin Perde Arkası: Basit Denklem, Sahte Rastgelelik ve Kriptografik Tehlike"
math: true
categories: 
  - Bilgi
tags: 
  - lcg
  - rastgele sayı üretimi
  - kriptografi
toc: true
---

Bilgisayarların zar atması sandığımız kadar gizemli değildir. Çoğu zaman makine, önceki bir sayıyı belirli sabitlerle işleyerek yeni bir sayı üretir. Lineer Kongrüansiyel Üreteç, yani LCG, bu yaklaşımın en eski ve anlaşılır örneklerinden biridir. Hızlı ve öğretici olmasına rağmen güvenlik söz konusu olduğunda bıraktığı matematiksel izler, onu dijital dünyanın fazlasıyla tahmin edilebilir falcısına dönüştürür.
``

## LCG nasıl çalışır?

Bir LCG, sayı dizisini şu denklemle üretir:

$$
X_{n+1} = (aX_n + c) \bmod m
$$

Buradaki değişkenler şunlardır:

- $X_n$: Mevcut durum veya üretilmiş son sayı
- $a$: Çarpan
- $c$: Artış miktarı
- $m$: Modül
- $X_0$: Diziyi başlatan tohum, yani seed

`mod` işlemi sonucu $0$ ile $m-1$ arasında tutar. Örneğin $a=5$, $c=3$, $m=16$ ve $X_0=7$ seçelim:

$$
X_1=(5\cdot7+3)\bmod16=6
$$

Sonraki değer ise $X_2=(5\cdot6+3)\bmod16=1$ olur. Aynı parametreler ve aynı tohum kullanıldığında dizi daima aynıdır. Bu nedenle LCG gerçek rastgele değil, **sözde rastgele** sayı üretir.

## Periyot neden önemlidir?

Durum uzayı yalnızca $m$ farklı değer içerdiği için dizi eninde sonunda önceki bir değere döner ve tekrar etmeye başlar. En iyi durumda periyot $m$ olabilir. Tam periyot elde etmek için Hull–Dobell koşulları kullanılır:

1. $c$ ile $m$ aralarında asal olmalıdır.
2. $a-1$, $m$ değerinin bütün asal çarpanlarına bölünmelidir.
3. $m$, 4'ün katıysa $a-1$ de 4'ün katı olmalıdır.

Bu koşullar uzun bir döngü sağlar; ancak uzun periyot, kriptografik güvenlik anlamına gelmez. Bir saatin yıllarca çalışması, mekanizmasının tahmin edilemez olduğu anlamına gelmediği gibi!

## Python ile küçük bir LCG

Aşağıdaki sınıf, her çağrıda denklemi uygulayarak yeni bir değer üretir:

```python
class LCG:
    def __init__(self, seed, a=1664525, c=1013904223, m=2**32):
        self.state = seed
        self.a = a
        self.c = c
        self.m = m

    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

rng = LCG(seed=42)
for _ in range(5):
    print(rng.next())
```

Kod simülasyon, oyun prototipi veya algoritma eğitimi için kullanılabilir. Fakat parola sıfırlama anahtarı, oturum kimliği ya da şifreleme anahtarı üretmek için uygun değildir.

## LCG neden kriptografik olarak güvensizdir?

LCG'nin temel sorunu çıktılar arasındaki doğrusal ilişkidir. Saldırgan $a$, $c$ ve $m$ değerlerini biliyorsa tek bir iç durumdan bütün gelecek değerleri hesaplayabilir. Parametreler bilinmese bile art arda alınan yeterli sayıda tam çıktı, modüler denklemler çözülerek parametrelerin bulunmasına yardımcı olur.

Üç ardışık çıktı için şu ilişkiler yazılabilir:

$$
X_2-X_1 \equiv a(X_1-X_0) \pmod m
$$

Uygun modüler ters mevcutsa buradan $a$, ardından $c$ hesaplanabilir. Ayrıca düşük anlamlı bitler çoğu LCG'de kısa ve düzenli döngüler sergiler. Çıktıyı kırpmak saldırıyı zorlaştırabilir, fakat tasarımı otomatik olarak güvenli yapmaz.

| Özellik | LCG | Kriptografik güvenli üreteç |
|---|---|---|
| Hız | Çok yüksek | Genellikle yüksek |
| Tekrarlanabilirlik | Kolay | Kontrollü olabilir |
| Gelecek çıktıyı tahmin | Çoğu durumda kolay | Hesaplama açısından zor |
| Durum ele geçirilince geçmiş | Korunmaz | Tasarıma göre korunabilir |
| Uygun kullanım | Simülasyon, eğitim | Anahtar, token, nonce |

## Ne kullanmalıyız?

Güvenlik gereken Python uygulamalarında işletim sisteminin güvenli rastgelelik kaynağını kullanan `secrets` modülü tercih edilmelidir:

```python
import secrets

# Tahmin edilmesi zor, URL kullanımına uygun bir oturum anahtarı üretir.
token = secrets.token_urlsafe(32)
```

Özetle LCG, modüler aritmetiği ve sözde rastgelelik fikrini öğrenmek için harika bir laboratuvardır. Ancak denklem ne kadar hızlı çalışırsa çalışsın, saldırganın çözebileceği kadar düzenliyse kriptografide yeri yoktur.

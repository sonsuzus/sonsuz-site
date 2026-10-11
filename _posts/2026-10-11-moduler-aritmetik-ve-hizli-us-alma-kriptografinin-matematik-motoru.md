---
layout: post
title: "Modüler Aritmetik ve Hızlı Üs Alma: Kriptografinin Matematik Motoru"
math: true
categories: 
  - Bilgi
tags: 
  - modüler aritmetik
  - hızlı üs alma
  - kriptografi
  - algoritma
  - python
  - matematik
toc: true
image: /img/moduler-aritmetik-ve-31.png
---

![moduler-aritmetik-ve-31](/img/moduler-aritmetik-ve-31.svg)


Günlük matematikte sayılar büyüdükçe hesaplar zorlaşır; kriptografide ise sayılar yalnızca büyümez, adeta gökdelen olur. Binlerce bitlik anahtarlarla çalışırken sıradan üs alma yöntemleri bilgisayarı terletebilir. Modüler aritmetik ve hızlı üs alma, bu devasa işlemleri yönetilebilir parçalara ayırarak RSA ve Diffie–Hellman gibi sistemlerin çalışmasını sağlayan temel araçlardır.

``

## Modüler aritmetik: Sayıların saat düzeni

Modüler aritmetiği anlamanın en kolay yolu bir saat düşünmektir. Saat 10 iken beş saat ilerlerseniz 15 değil, 3 sonucuna ulaşırsınız. Çünkü saat üzerindeki değerler 12'ye göre döngüseldir:

$$10 + 5 ≡ 3 \pmod{12}$$

Genel olarak iki sayı, bir $m$ modülüne bölündüklerinde aynı kalanı veriyorsa eşdeğerdir:

$$a ≡ b \pmod{m}$$

Bu yaklaşımın önemli avantajı, ara sonuçların sürekli küçültülebilmesidir. Örneğin çarpma için şu özellik geçerlidir:

$$(a \cdot b) \bmod m = ((a \bmod m)(b \bmod m)) \bmod m$$

Dolayısıyla dev sayıları sonuna kadar taşımak yerine her adımda mod alabiliriz.

| Normal işlem | Modüler karşılığı | Faydası |
|---|---|---|
| $a+b$ | $(a \bmod m+b \bmod m)\bmod m$ | Toplamı küçük tutar |
| $a\cdot b$ | $((a\bmod m)(b\bmod m))\bmod m$ | Büyük çarpımları sınırlar |
| $a^n$ | Tekrarlı kare alma | Üs hesabını hızlandırır |
| Bölme | Modüler ters ile çarpma | Alan yapısında bölmeyi mümkün kılar |

## Neden doğrudan üs almıyoruz?

$7^{13} \bmod 11$ gibi küçük bir işlem doğrudan hesaplanabilir. Ancak kriptografide üsler yüzlerce veya binlerce bitten oluşabilir. Önce $a^n$ değerini üretip sonra mod almak, bellekte gereksiz büyüklükte bir sayı oluşturur.

Ayrıca üssü kadar çarpma yapan basit yöntem $O(n)$ zaman karmaşıklığına sahiptir. Hızlı üs alma, üssün ikili gösteriminden yararlanarak bu maliyeti $O(\log n)$ seviyesine indirir. Aradaki fark, bisikletle kıtalar arası yolculuk yapmak ile hızlı trene binmek gibidir.

## Hızlı üs alma nasıl çalışır?

Temel fikir, üssü sürekli ikiye bölmek ve tabanı karelemektir. Örneğin:

$$a^{13}=a^{8}a^{4}a^{1}$$

Çünkü $13$ sayısının ikili gösterimi $1101_2$ biçimindedir. İkili gösterimdeki her `1`, sonuca hangi kuvvetin katılacağını belirtir. Her aşamada mod alındığı için ara değerler kontrol altında kalır.

```python
def moduler_us(taban, us, modul):
    sonuc = 1
    taban %= modul

    while us > 0:
        # Üs tekse mevcut tabanı sonuca dahil et.
        if us % 2 == 1:
            sonuc = (sonuc * taban) % modul

        # Sonraki ikili basamak için tabanı karele.
        taban = (taban * taban) % modul
        us //= 2

    return sonuc

print(moduler_us(7, 13, 11))  # 2
```

Bu fonksiyon yalnızca birkaç çarpma yapar. Python aynı işlemi yerleşik `pow(7, 13, 11)` çağrısıyla da gerçekleştirebilir.

## Kriptografideki rolü

RSA'da şifreleme kabaca şu denklemle ifade edilir:

$$c = m^e \bmod n$$

Burada $m$ mesajı, $e$ açık üssü, $n$ modülü ve $c$ şifreli metni temsil eder. Şifre çözme ise özel üs $d$ kullanılarak yapılır:

$$m = c^d \bmod n$$

Güvenlik, modüler üs alma işleminin kolay; uygun gizli bilgiler olmadan işlemi tersine çevirmenin ise zor olmasına dayanır. Diffie–Hellman anahtar değişimi ve ElGamal gibi yöntemler de benzer matematiksel yapılardan yararlanır.

## Uygulamadaki önemli ayrıntılar

Matematiksel doğruluk tek başına güvenlik anlamına gelmez. Koşullu dallanmalar ve işlem süreleri, yan kanal saldırılarına bilgi sızdırabilir. Gerçek kriptografik uygulamalarda sabit zamanlı algoritmalar, güvenilir kütüphaneler ve yeterince büyük parametreler kullanılmalıdır. Kendi algoritmanızı yazmak öğrenmek için harikadır; üretimde kullanmak ise paraşütü evde dikmeye biraz benzer.

Özetle modüler aritmetik sayıları döngüsel bir alana hapseder, hızlı üs alma da bu alandaki dev kuvvetleri az sayıda adımla hesaplar. İkisi birleştiğinde modern açık anahtarlı kriptografinin sessiz ama son derece güçlü matematik motoru ortaya çıkar.

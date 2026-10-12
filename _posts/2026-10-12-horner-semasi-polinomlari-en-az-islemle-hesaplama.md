---
layout: post
title: "Horner Şeması: Polinomları En Az İşlemle Hesaplama"
math: true
categories: 
  - Bilgi
tags: 
  - horner şeması
  - polinom
  - algoritma
  - matematik
  - python
  - sayısal hesaplama
toc: true
image: /img/horner-semasi-polinomlari-20.png
---

![horner-semasi-polinomlari-20](/img/horner-semasi-polinomlari-20.svg)


Bir polinomun belirli bir noktadaki değerini hesaplamak ilk bakışta yalnızca üsleri, çarpımları ve toplamları sırayla uygulamak gibi görünür. Ancak derece büyüdükçe klasik yöntem gereksiz işlem kalabalığına dönüşür. Horner şeması, polinomu akıllıca parantezleyerek aynı sonucu daha az çarpma işlemiyle bulur. Üstelik yöntem hem kâğıt üzerinde hem de bilgisayar programlarında son derece kullanışlıdır.

``

## Temel fikir: Polinomu iç içe geçirmek

Derecesi $n$ olan genel bir polinomu şöyle yazabiliriz:

$$P(x)=a_nx^n+a_{n-1}x^{n-1}+\cdots+a_1x+a_0$$

Doğrudan hesaplamada $x^2$, $x^3$ ve diğer kuvvetler ayrı ayrı üretilebilir. Horner şeması ise ortak $x$ çarpanlarını dışarı alarak polinomu şu biçime dönüştürür:

$$P(x)=(((a_nx+a_{n-1})x+a_{n-2})x+\cdots)x+a_0$$

Bu ifade biraz matruşka bebeğine benzer: Her parantezin içinden başka bir çarpma ve toplama çıkar. İşleme en yüksek dereceli katsayıdan başlanır; mevcut sonuç $x$ ile çarpılır ve sıradaki katsayı eklenir.

Örneğin

$$P(x)=2x^3-6x^2+2x-1$$

polinomunu Horner biçiminde yazalım:

$$P(x)=((2x-6)x+2)x-1$$

$x=3$ için adımlar şöyledir:

1. İlk katsayıyla başla: $2$
2. $2\cdot3-6=0$
3. $0\cdot3+2=2$
4. $2\cdot3-1=5$

Dolayısıyla $P(3)=5$ bulunur. Küp veya kareyi ayrıca hesaplamaya hiç gerek kalmaz.

## İşlem sayısı neden azalır?

Standart yaklaşımda her terimin kuvveti bağımsız hesaplanırsa çok sayıda çarpma yapılabilir. Horner yönteminde derece $n$ olan bir polinom için tam olarak $n$ çarpma ve $n$ toplama yeterlidir. Bu nedenle zaman karmaşıklığı $O(n)$ olur.

| Özellik | Doğrudan hesaplama | Horner şeması |
|---|---:|---:|
| Çarpma sayısı | Uygulamaya göre $O(n^2)$ olabilir | $n$ |
| Toplama sayısı | Yaklaşık $n$ | $n$ |
| Ek kuvvet hesabı | Gerekebilir | Gerekmez |
| Kod yapısı | Daha dağınık | Tek döngü |
| Sayısal davranış | Daha fazla ara işlem | Genellikle daha kararlı |

Kuvvetlerin önceden verimli biçimde hesaplanması doğrudan yöntemi iyileştirebilir. Yine de Horner şeması sade yapısı ve düşük sabit maliyeti sayesinde çoğu durumda daha avantajlıdır.

## Python ile uygulama

Katsayıları en yüksek dereceden sabit terime doğru saklayabiliriz. Aşağıdaki fonksiyon, birikmiş sonucu her adımda $x$ ile çarpıp yeni katsayıyı ekler:

```python
def horner(katsayilar, x):
    sonuc = 0

    for katsayi in katsayilar:
        sonuc = sonuc * x + katsayi

    return sonuc

katsayilar = [2, -6, 2, -1]
print(horner(katsayilar, 3))  # 5
```

Buradaki `sonuc`, işlenmiş katsayıların oluşturduğu ara polinomun değeridir. Döngü değişmezi olarak düşünüldüğünde algoritmanın doğruluğu daha net görülür: Her tur sonunda bir derece daha polinoma dâhil edilir.

Ara değerleri görmek istersek fonksiyonu biraz genişletebiliriz:

```python
def horner_adimlari(katsayilar, x):
    sonuc = katsayilar[0]
    print(sonuc)

    for katsayi in katsayilar[1:]:
        sonuc = sonuc * x + katsayi
        print(sonuc)

    return sonuc
```

Bu sürüm eğitim ve hata ayıklama için yararlıdır; ekrana sırasıyla $2$, $0$, $2$ ve $5$ yazdırır.

## Sadece değer hesaplamakla kalmaz

Horner şeması polinom bölmede de kullanılabilir. $P(x)$ polinomunu $(x-r)$ ifadesine sentetik bölme ile böldüğümüzde oluşan son değer $P(r)$, yani kalandır. Bu ilişki kalan teoreminden gelir:

$$P(x)=(x-r)Q(x)+P(r)$$

Sonuç sıfırsa $r$ polinomun köküdür. Böylece aynı kısa algoritma; değer hesaplama, kök denetleme ve sentetik bölme gibi farklı görevlerde kullanılabilir. Horner şeması, iyi bir algoritmanın yalnızca hızlı değil, aynı zamanda fikren zarif olabileceğini gösteren klasik örneklerden biridir.

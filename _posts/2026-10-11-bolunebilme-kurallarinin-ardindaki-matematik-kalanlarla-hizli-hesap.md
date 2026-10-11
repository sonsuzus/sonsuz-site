---
layout: post
title: "Bölünebilme Kurallarının Ardındaki Matematik: Kalanlarla Hızlı Hesap"
math: true
categories: 
  - Bilgi
tags: 
  - matematik
  - bölünebilme
  - modüler aritmetik
  - algoritma
  - python
toc: true
image: /img/bolunebilme-kurallarinin-ardindaki-13.png
---

Uzun bir sayının 3’e, 7’ye veya 11’e tam bölünüp bölünmediğini anlamak için hemen hesap makinesine uzanmanız gerekmez. Bölünebilme kuralları sihirli kestirmeler gibi görünse de aslında basamak değerleri ve kalanlar üzerine kuruludur. Gelin, ezberlenen kuralların matematik motorunun kapağını açalım.


![bolunebilme-kurallarinin-ardindaki-13](/img/bolunebilme-kurallarinin-ardindaki-13.svg)

``

## Bölünebilmek ne demektir?

Bir $N$ tam sayısı, $d$ sayısına bölündüğünde kalan sıfırsa $d$ ile tam bölünür. Modüler aritmetik dilinde bunu şöyle yazarız:

$$N ≡ 0 \pmod d$$

Örneğin $42 ≡ 0 \pmod 7$ olduğundan 42, 7’ye tam bölünür. Bir sayının ondalık gösterimi ise basamak değerleri kullanılarak açılabilir:

$$N = a_0 + 10a_1 + 10^2a_2 + \cdots + 10^ka_k$$

Bölünebilme kuralları, buradaki $10$, $100$ ve diğer kuvvetlerin ilgili bölen karşısındaki kalanlarını kullanır. Yani mesele rakamları rastgele toplamak değil, onluk sistemin davranışını değerlendirmektir.

## Yaygın kurallar ve nedenleri

| Bölen | Hızlı kontrol | Matematiksel fikir |
|---:|---|---|
| 2 | Son rakam çifttir. | $10 ≡ 0 \pmod 2$ |
| 3 | Rakamlar toplamı 3’ün katıdır. | $10 ≡ 1 \pmod 3$ |
| 4 | Son iki basamak 4’ün katıdır. | $100 ≡ 0 \pmod 4$ |
| 5 | Son rakam 0 veya 5’tir. | Onun katlarının son basamağı belirleyicidir. |
| 6 | Sayı hem 2’ye hem 3’e bölünür. | $6 = 2 \times 3$ ve bölenler aralarında asaldır. |
| 8 | Son üç basamak 8’in katıdır. | $1000 ≡ 0 \pmod 8$ |
| 9 | Rakamlar toplamı 9’un katıdır. | $10 ≡ 1 \pmod 9$ |
| 10 | Son rakam 0’dır. | $10 ≡ 0 \pmod {10}$ |
| 11 | Tek ve çift sıralı rakam toplamlarının farkı 11’in katıdır. | $10 ≡ -1 \pmod {11}$ |

### Neden rakamları topluyoruz?

$5832$ sayısını ele alalım. Çünkü $10 ≡ 1 \pmod 3$ olduğundan, 10’un bütün pozitif kuvvetleri de 3’e göre 1 kalanını verir:

$$5832 ≡ 5 + 8 + 3 + 2 = 18 ≡ 0 \pmod 3$$

Dolayısıyla sayı 3’e bölünür. Aynı mantık 9 için de geçerlidir. Bu nedenle rakamlar toplamı yöntemi yalnızca pratik bir numara değil, basamak açılımının doğrudan sonucudur.

## 11 kuralındaki işaret değiştirme

$10 ≡ -1 \pmod {11}$ olduğu için kuvvetler sırayla $1, -1, 1, -1$ biçiminde ilerler. Örneğin 2728 için dönüşümlü toplamı hesaplayalım:

$$8 - 2 + 7 - 2 = 11$$

Sonuç 11’in katı olduğu için 2728 de 11’e tam bölünür. Bir bakıma rakamlar matematiksel bir tahterevalliye oturur; denge 11’in katında kurulursa test başarıyla tamamlanır.

## Peki ya 7?

7 kuralı biraz daha afacan görünür: Son rakamın iki katını, kalan sayıdan çıkarın. Elde edilen sonuç 7’nin katıysa başlangıçtaki sayı da 7’nin katıdır. Örneğin 203 için:

$$20 - 2 \times 3 = 14$$

14, 7’ye bölündüğünden 203 de bölünür. Bu işlem gerekirse sonuç küçülene kadar tekrarlanabilir.

## Kuralları kodlamak

Aşağıdaki Python fonksiyonu, seçilen bölen için anlaşılır kontroller uygular. Böylece kuralların bir algoritmaya nasıl dönüştüğünü görebiliriz:

```python
def bolunur_mu(sayi, bolen):
    rakamlar = [int(rakam) for rakam in str(abs(sayi))]

    if bolen in (3, 9):
        return sum(rakamlar) % bolen == 0
    if bolen == 4:
        return abs(sayi) % 100 % 4 == 0
    if bolen == 8:
        return abs(sayi) % 1000 % 8 == 0
    if bolen == 11:
        fark = sum(rakamlar[::2]) - sum(rakamlar[1::2])
        return fark % 11 == 0

    return sayi % bolen == 0

print(bolunur_mu(2728, 11))  # True
```

Kod, 3 ve 9 için rakamları toplar; 4 ve 8 için yalnızca gerekli son basamakları inceler. Genel durumda ise doğrudan kalan operatörünü kullanır.

Bölünebilme kuralları, zihinden hesaplamayı hızlandırmanın ötesinde modüler aritmetiği somutlaştırır. Kuralları ezberlemek işe yarar; fakat neden çalıştıklarını bilmek, yeni bölenler için kendi yöntemlerinizi geliştirmenizi sağlar.

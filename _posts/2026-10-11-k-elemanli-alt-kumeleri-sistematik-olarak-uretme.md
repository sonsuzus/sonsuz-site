---
layout: post
title: "K-Elemanlı Alt Kümeleri Sistematik Olarak Üretme"
math: true
categories: 
  - Program
tags: 
  - algoritma
  - kombinasyon
  - python
  - bitmask
  - özyineleme
toc: true
image: /img/k-elemanli-alt-29.png
---

Bir kümeden tam olarak $k$ eleman seçmenin kaç farklı yolu olduğunu bilmek kolaydır; asıl eğlence, bu seçimlerin tamamını eksiksiz, tekrarsız ve belirli bir sırada üretmekle başlar. Kombinasyon üretimi; arama algoritmalarından test verisi hazırlamaya, takım oluşturmadan özellik seçimine kadar pek çok alanda karşımıza çıkar. Bu yazıda k-elemanlı alt kümeleri üretmenin üç sistematik yöntemini inceleyeceğiz.

``

## Önce matematik: Kaç sonuç bekliyoruz?

$n$ elemanlı bir kümenin $k$ elemanlı alt kümelerinin sayısı binom katsayısıyla hesaplanır:

$$
{n \choose k}=\frac{n!}{k!(n-k)!}
$$

Örneğin $A=\{a,b,c,d\}$ ve $k=2$ için toplam sonuç sayısı

$$
{4 \choose 2}=6
$$

olur. Üretilecek alt kümeler şunlardır: $\{a,b\}$, $\{a,c\}$, $\{a,d\}$, $\{b,c\}$, $\{b,d\}$ ve $\{c,d\}$.

Bir algoritmanın doğru olduğunu sınarken bu formül iyi bir kontrol mekanizmasıdır. Algoritma tam olarak ${n \choose k}$ sonuç vermeli ve hiçbir sonucu iki kez üretmemelidir.

## 1. Özyinelemeli geri izleme

En anlaşılır yaklaşım, her adımda bir elemanı seçip seçmemeye karar vermektir. Ancak yalnızca seçme dalını açıkça dolaşarak gereksiz adımları azaltabiliriz.

```python
def kombinasyonlar(elemanlar, k):
    sonuc = []

    def ara(baslangic, secilenler):
        # İstenen büyüklüğe ulaştığımızda kopyayı kaydet.
        if len(secilenler) == k:
            sonuc.append(secilenler.copy())
            return

        gereken = k - len(secilenler)
        son_indeks = len(elemanlar) - gereken

        for i in range(baslangic, son_indeks + 1):
            secilenler.append(elemanlar[i])
            ara(i + 1, secilenler)
            secilenler.pop()  # Geri dön ve başka adayı dene.

    ara(0, [])
    return sonuc

print(kombinasyonlar(["a", "b", "c", "d"], 2))
```

`baslangic` değeri, daha önce kullanılan elemanlara geri dönülmesini engeller. Böylece hem tekrar oluşmaz hem de kombinasyonlar sözlük sırasına benzer bir düzende üretilir. `son_indeks` hesabı ise geride yeterli eleman kalmadığı bilinen dalları budar.

## 2. İndeksleri sözlük sırasıyla ilerletmek

Bir kombinasyonu elemanların kendisi yerine indeks dizisiyle temsil edebiliriz. Örneğin `[0, 1, 3]`, kümenin birinci, ikinci ve dördüncü elemanlarını seçer. Her turda sağdan başlayarak artırılabilecek ilk indeks bulunur.

```python
def sirali_k_alt_kumeler(veri, k):
    n = len(veri)
    if k < 0 or k > n:
        return

    indeksler = list(range(k))

    while True:
        yield [veri[i] for i in indeksler]

        i = k - 1
        while i >= 0 and indeksler[i] == i + n - k:
            i -= 1

        if i < 0:
            return

        indeksler[i] += 1
        for j in range(i + 1, k):
            indeksler[j] = indeksler[j - 1] + 1
```

Bu sürüm `yield` kullandığı için tüm sonuçları bellekte tutmaz. Büyük veri kümelerinde yalnızca sıradaki kombinasyona ihtiyaç duyulduğunda oldukça kullanışlıdır.

## 3. Bit maskesi yaklaşımı

Her elemanı bir bit ile temsil edebiliriz: `1` seçildiğini, `0` seçilmediğini gösterir. Örneğin `10110` maskesi üç eleman seçer. Dolayısıyla yalnızca içinde tam $k$ tane `1` bulunan maskeler kabul edilir.

```python
def bitmask_kombinasyonlari(veri, k):
    n = len(veri)
    for maske in range(1 << n):
        if maske.bit_count() == k:
            yield [veri[i] for i in range(n) if maske & (1 << i)]
```

Kod son derece kısa olsa da $0$ ile $2^n-1$ arasındaki bütün maskeleri inceler. Bu nedenle özellikle $k$, $n$ değerine göre küçükken çok sayıda gereksiz maske kontrol edilir.

## Yöntemlerin karşılaştırması

| Yöntem | Üretim maliyeti | Ek bellek | Güçlü yönü |
|---|---:|---:|---|
| Geri izleme | $O(k{n \choose k})$ | $O(k)$ | Kolay uyarlanır ve budanabilir |
| İndeks ilerletme | $O(k{n \choose k})$ | $O(k)$ | Tembel ve sıralı üretim sağlar |
| Bit maskesi | $O(n2^n)$ | $O(k)$ | Basit, düşük seviyeli işlemlere uygun |

![k-elemanli-alt-29](/img/k-elemanli-alt-29.svg)


Pratikte genel amaçlı kullanım için indeks ilerletme yöntemi iyi bir dengedir. Seçimlere özel kurallar eklenecekse geri izleme daha esnektir. Bit maskesi ise küçük kümelerde, bit düzeyindeki temsiller zaten problemin parçasıysa parlamaya başlar. Hangi yolu seçerseniz seçin, sonuç sayısını ${n \choose k}$ ile doğrulamak algoritmik pusulanız olacaktır.

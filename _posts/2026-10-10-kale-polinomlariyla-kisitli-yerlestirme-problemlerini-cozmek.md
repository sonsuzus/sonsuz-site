---
layout: post
title: "Kale Polinomlarıyla Kısıtlı Yerleştirme Problemlerini Çözmek"
math: true
categories: 
  - Bilgi
tags: 
  - kale polinomları
  - kombinatorik
  - satranç
  - yerleştirme problemleri
  - python
  - matematik
toc: true
image: /img/kale-polinomlariyla-kisitli-25.png
---

Bir satranç tahtasına birbirini tehdit etmeyen kaleler yerleştirmek kolay görünebilir. Ancak bazı kareler yasaklandığında işin rengi değişir: Artık yalnızca kaleleri değil, kısıtlamaları da saymamız gerekir. **Kale polinomları**, bu tür yerleştirme problemlerini tek bir cebirsel yapı içinde özetleyerek karmaşık sayımları düzenli ve hesaplanabilir hâle getirir.


![kale-polinomlariyla-kisitli-25](/img/kale-polinomlariyla-kisitli-25.svg)

``

## Temel fikir: Kaleler neden önemli?

Bir kale bulunduğu satır ve sütun boyunca hareket eder. Dolayısıyla iki kalenin birbirini tehdit etmemesi için farklı satırlarda ve farklı sütunlarda bulunmaları gerekir. Bu özellik, satırlarla sütunlar arasında eşleştirme yapılan birçok probleme doğrudan karşılık gelir.

Örneğin dört çalışanın dört göreve atanacağını düşünelim. Bir çalışanın yapamayacağı görevleri yasak karelerle gösterirsek, geçerli atamalar tahtaya birbirini tehdit etmeyen kaleler yerleştirmekle modellenebilir.

Bir $B$ tahtası için $r_k(B)$, izin verilen karelere birbirini tehdit etmeyecek biçimde yerleştirilebilen $k$ kalenin sayısı olsun. Tahtanın **kale polinomu** şöyledir:

$$R_B(x)=\sum_{k=0}^{n} r_k(B)x^k$$

Burada $r_0(B)=1$ kabul edilir; çünkü hiç kale yerleştirmemenin tam olarak bir yolu vardır. Sabit terimin gizemli biçimde hep 1 çıkmasının nedeni budur.

| Kavram | Satranç tahtasındaki anlamı | Atama problemindeki anlamı |
|---|---|---|
| Satır | Kalenin bulunduğu yatay çizgi | Çalışan veya kişi |
| Sütun | Kalenin bulunduğu dikey çizgi | Görev veya seçenek |
| Yasak kare | Kale konulamaz | Atama yapılamaz |
| $r_k$ | $k$ uyumsuz kale yerleşimi | $k$ bağımsız eşleştirme |
| Kale polinomu | Tüm yerleşimlerin özeti | Kısmi atamaların özeti |

## Küçük bir örnek

$2\times2$ tam bir tahtada bir kale yerleştirmek için 4 seçenek vardır. İki kaleyi tehdit oluşturmayacak şekilde yerleştirmenin ise 2 yolu bulunur: ana köşegen veya diğer köşegen. Böylece

$$R_B(x)=1+4x+2x^2$$

elde edilir. Eğer bir kare yasaklanırsa katsayılar değişir. Kale polinomu yalnızca tahta boyutunu değil, izin verilen karelerin geometrisini de yakalar.

## Yasak konumlardan geçerli permütasyonlara

$n$ kişi ile $n$ görevin bulunduğu eksiksiz bir atama probleminde toplam $n!$ permütasyon vardır. Ancak yasak atamalar içeren bir $B$ tahtası verildiğinde, hiçbir yasak kareyi kullanmayan permütasyonların sayısı içerme-dışlama ilkesiyle bulunabilir:

$$N=\sum_{k=0}^{n}(-1)^k r_k(B)(n-k)!$$

Burada kaleleri **yasak karelere** yerleştiririz. $r_k(B)$, aynı satır veya sütunu paylaşmayan $k$ yasağın birlikte gerçekleşebileceği durumları sayar. $(-1)^k$ işareti fazla sayılan durumları sırayla çıkarıp geri ekler. Yani formül, içerme-dışlamanın satranç kostümü giymiş hâlidir.

## Python ile katsayıları hesaplamak

Aşağıdaki kod, izin verilen karelerin koordinatlarını kullanarak geri izleme yöntemiyle $r_k$ değerlerini hesaplar:

```python
def rook_numbers(rows, cols, allowed):
    counts = [0] * (min(rows, cols) + 1)

    def search(index, used_rows, used_cols, placed):
        if index == len(allowed):
            counts[placed] += 1
            return

        row, col = allowed[index]

        # Bu kareyi kullanmadan sonraki kareye geç.
        search(index + 1, used_rows, used_cols, placed)

        # Satır ve sütun boşsa buraya bir kale yerleştir.
        if row not in used_rows and col not in used_cols:
            search(
                index + 1,
                used_rows | {row},
                used_cols | {col},
                placed + 1
            )

    search(0, set(), set(), 0)
    return counts

board = [(0, 0), (0, 1), (1, 0), (1, 1)]
print(rook_numbers(2, 2, board))  # [1, 4, 2]
```

Algoritma her kare için “kullan” ve “kullanma” dallarını araştırır. Satır ve sütun kümeleri, kalelerin birbirini tehdit etmesini engeller. Büyük tahtalarda bu yaklaşım pahalı olabilir; dinamik programlama, bit maskeleri veya tahtayı bağımsız parçalara ayırma daha verimlidir.

Özellikle iki tahta bağımsız satır ve sütun kümelerine sahipse birleşimin kale polinomu çarpım yoluyla bulunur: $R_{B_1\cup B_2}(x)=R_{B_1}(x)R_{B_2}(x)$. Böylece büyük bir problem, küçük polinomların çarpımına dönüşür. Kale polinomlarının asıl gücü de burada yatar: Görsel kısıtları cebire, cebiri ise sistematik sayımlara çevirir.

---
layout: post
title: "B-Ağaçları: Veritabanlarının Diskteki Hız Sırrı"
math: true
categories: 
  - Bilgi
tags: 
  - b-ağacı
  - veritabanı
  - veri yapıları
  - algoritma
  - indeksleme
  - disk erişimi
toc: true
image: /img/b-agaclari-veritabanlarinin-26.png
---

Bir veritabanında milyonlarca kayıt bulunmasına rağmen sorguların birkaç milisaniyede sonuçlanması sihir değildir. Bu başarının arkasında, verileri disk üzerinde akıllıca düzenleyen indeksler ve özellikle B-ağaçları vardır. Dengeli, geniş ve kısa bir yapıya sahip olan B-ağaçları, pahalı disk erişimlerinin sayısını azaltarak aradığımız kayda mümkün olduğunca az adımda ulaşmamızı sağlar.
``

## Asıl sorun: Disk erişimi pahalıdır

RAM üzerindeki verilere erişmek son derece hızlıdır; ancak kalıcı veriler SSD veya sabit diskte tutulur. Diskten tek bir bayt yerine genellikle **sayfa** ya da **blok** adı verilen sabit boyutlu veri parçaları okunur. Bir sayfanın boyutu örneğin 4 KB, 8 KB veya 16 KB olabilir.

Bu nedenle disk tabanlı bir veri yapısında temel maliyet, yapılan karşılaştırmalar değil, okunan sayfa sayısıdır. Bir milyon kayıt arasında ikili arama teorik olarak

$$
\log_2(1.000.000) \approx 20
$$

adım gerektirir. Fakat her düğüm ayrı bir disk sayfasındaysa yaklaşık 20 disk erişimi oldukça pahalı olabilir. B-ağaçları ise bir düğümde çok sayıda anahtar saklayarak ağacın dallanma katsayısını büyütür.

## B-ağacının temel mantığı

İkili arama ağacındaki her düğüm en fazla iki çocuğa sahiptir. B-ağacında ise bir düğüm onlarca, hatta yüzlerce çocuk barındırabilir. Düğüm boyutu genellikle bir disk sayfasını dolduracak şekilde seçilir.

Bir B-ağacının dallanma katsayısı $m$ ise yaklaşık yüksekliği şöyledir:

$$
h \approx \log_m(n)
$$

Örneğin bir düğüm 100 çocuk gösterebiliyorsa bir milyon kayıt için:

$$
\log_{100}(1.000.000) = 3
$$

Yani teorik olarak yalnızca üç sayfa okumasıyla hedef bölgeye ulaşılabilir. Üst düğümlerin önbellekte tutulması durumunda gerçek disk erişimi daha da azalır.

| Yapı | Düğüm başına çocuk | Yaklaşık yükseklik | Disk kullanımı |
|---|---:|---:|---|
| İkili arama ağacı | 2 | Yüksek | Çok sayıda rastgele erişim |
| B-ağacı | Çok sayıda | Düşük | Sayfa odaklı ve verimli |
| B+ ağacı | Çok sayıda | Düşük | Sıralı taramalar için çok uygun |
| Hash indeks | Kovaya bağlı | Genellikle sabit | Eşitlik sorgularında güçlü |

## Arama nasıl gerçekleştirilir?

Her düğümde anahtarlar sıralı tutulur. Aranan değer düğümdeki anahtarlarla karşılaştırılır ve uygun çocuk sayfasına geçilir. Aşağıdaki sadeleştirilmiş Python kodu, bellekteki bir B-ağacı düğümünde bu yönlendirmeyi gösterir:

```python
class BTreeNode:
    def __init__(self, keys, children=None, leaf=False):
        self.keys = keys
        self.children = children or []
        self.leaf = leaf

    def search(self, target):
        index = 0

        while index < len(self.keys) and target > self.keys[index]:
            index += 1

        if index < len(self.keys) and target == self.keys[index]:
            return self.keys[index]

        if self.leaf:
            return None

        return self.children[index].search(target)
```

Kod, önce hedefin hangi anahtar aralığında bulunduğunu belirler. Düğüm yaprak değilse yalnızca ilgili çocuğa ilerler. Gerçek veritabanlarında `children` listesindeki öğeler çoğunlukla nesne değil, disk sayfalarının adresleridir. Ayrıca düğüm içindeki arama doğrusal tarama yerine ikili aramayla yapılabilir.

## Ekleme ve bölünme

Bir düğüm dolduğunda yeni kayıt gelişigüzel başka bir yere konmaz. Düğüm iki parçaya bölünür ve ortadaki anahtar üst düğüme taşınır. Üst düğüm de dolarsa bölünme köke kadar ilerleyebilir. Kök bölündüğünde ağacın yüksekliği yalnızca bir artar.

Bu kurallar bütün yaprakların aynı seviyede kalmasını sağlar. Böylece kötü sıralanmış eklemeler bile ağacı uzun bir zincire dönüştüremez. Arama, ekleme ve silme işlemlerinin maliyeti genel olarak $O(\log_m n)$ seviyesindedir.

## B+ ağaçları neden daha yaygın?

Modern veritabanları çoğunlukla B-ağacının bir türevi olan **B+ ağacını** kullanır. İç düğümler yalnızca yönlendirme anahtarlarını içerirken gerçek kayıtlar yapraklarda saklanır. Yapraklar birbirine bağlı olduğundan `WHERE yas BETWEEN 20 AND 30` gibi aralık sorguları, ilk kayıt bulunduktan sonra sayfalar üzerinde sıralı biçimde ilerleyebilir.

Kısacası B-ağaçlarının gücü yalnızca hızlı arama yapmalarından gelmez. Disk sayfalarıyla uyumlu çalışmaları, dengelerini korumaları ve yüksek dallanma katsayıları sayesinde milyonlarca kaydı birkaç disk erişimine indirgemeleri onları veritabanı indekslerinin vazgeçilmez kahramanı yapar.

![b-agaclari-veritabanlarinin-26](/img/b-agaclari-veritabanlarinin-26.svg)


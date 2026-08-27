---
layout: post
title: "AVL ve Kırmızı-Siyah Ağaçlar: Dengenin Kodla Dansı"
math: true
categories: 
  - Bilgi
tags: 
  - veri yapıları
  - algoritmalar
  - ikili arama ağacı
toc: true
image: /img/avl-ve-kirmizi-27.png
---

İkili arama ağaçları (BST), küçük anahtarları solunda, büyük anahtarları sağında tutarak aramayı hızlandırır. Ancak anahtarlar sıralı gelirse ağaç, bir ağacın heybetinden çok bağlı listeye benzeyen eğik bir yapıya dönüşür. Bu durumda arama, ekleme ve silme maliyeti $O(n)$ olur. AVL ve Kırmızı-Siyah ağaçları, her güncellemeden sonra küçük yapısal müdahaleler yaparak yüksekliği $O(\log n)$ sınırında tutan iki ünlü çözümdür.
``

Dengeli olmanın temel hedefi, kökten en derin yaprağa giden yolun makul kalmasıdır. İdeal olarak yüksekliği yaklaşık $\log_2 n$ olan bir ağaçta arama hızlıdır. Kendini dengeleme; **rotasyon**, düğüm renkleri veya yükseklik bilgisi gibi ek metaverilerle gerçekleştirilir. Rotasyonlar düğümlerin sırasını bozmaz; yalnızca ebeveyn-çocuk ilişkilerini yeniden düzenler. Yani BST kuralı korunurken ağacın ağırlık merkezi toparlanır.

| Özellik | AVL Ağacı | Kırmızı-Siyah Ağacı |
|---|---|---|
| Denge ölçütü | Alt ağaç yükseklik farkı | Renk kuralları ve siyah yükseklik |
| Arama | Genellikle daha hızlı | Çok iyi, fakat biraz daha gevşek |
| Güncelleme | Daha fazla rotasyon gerekebilir | Güncellemelerde pratikte esnek |
| Yaygın kullanım | Okuma ağırlıklı indeksler | `map`, `set` benzeri kütüphaneler |

![avl-ve-kirmizi-27](/img/avl-ve-kirmizi-27.svg)


## AVL: Yükseklik Farkına Sıkı Denetim

AVL düğümünün denge faktörü şöyle tanımlanır:

$$BF(v)=h(v_{sol})-h(v_{sağ})$$

Her düğüm için $BF \in \{-1,0,1\}$ olmalıdır. Ekleme sonrasında bir düğümün faktörü $2$ ya da $-2$ olursa dengesizlik oluşur. Sorunun yönüne göre dört klasik senaryo vardır: Sol-Sol (LL), Sağ-Sağ (RR), Sol-Sağ (LR) ve Sağ-Sol (RL). LL için sağa, RR için sola tek rotasyon yeterlidir; LR ve RL ise önce çocuk üzerinde, sonra kök üzerinde iki rotasyon ister.

Aşağıdaki sade Python örneği, sola rotasyonun özünü gösterir. Bu işlem, sağ tarafa yığılmış bir alt ağacı yukarı taşır:

```python
def sola_dondur(x):
    y = x.sag
    orta = y.sol

    y.sol = x
    x.sag = orta

    x.yukseklik = 1 + max(yukseklik(x.sol), yukseklik(x.sag))
    y.yukseklik = 1 + max(yukseklik(y.sol), yukseklik(y.sag))
    return y
```

Silme AVL için daha heyecanlıdır: Bir düğüm kaldırıldığında yükseklik köke kadar azalabilir. Bu nedenle eklemedeki tek sorunlu atanın aksine, silme sonrası birden fazla atada yeniden dengeleme gerekebilir. İki çocuklu düğüm silinirse genellikle sağ alt ağacın en küçük düğümüyle, yani ardılıyla yer değiştirilir; ardından oluşan yükseklik kaybı rotasyonlarla düzeltilir.

## Kırmızı-Siyah: Daha Gevşek, Daha Çevik

Kırmızı-Siyah ağaçlarda her düğüm kırmızı veya siyahtır. Kök siyahtır, boş yapraklar siyah kabul edilir, kırmızı düğümün kırmızı çocuğu olamaz ve her düğümden torun boş yapraklara giden yollardaki siyah düğüm sayısı eşittir. Bu son sayı **siyah yükseklik** olarak düşünülür. Kurallar, en uzun yolun en kısa yolun iki katını aşmamasını sağlar; dolayısıyla yükseklik yine $O(\log n)$ kalır.

Ekleme sırasında yeni düğüm kırmızı eklenir. Ebeveyni siyahsa iş biter. Ebeveyn ve amca kırmızıysa ikisi siyaha, büyükbaba kırmızıya boyanır; düzeltme yukarı taşınabilir. Amca siyahsa uygun tek veya çift rotasyon uygulanır ve renkler değiştirilir. Silme daha zordur çünkü siyah bir düğümün kaybı siyah yüksekliği eksiltir. Algoritma bu durumu bazen “çifte siyah” gibi ele alır; kardeşin rengine ve çocuklarının renklerine göre yeniden boyama ya da rotasyon yapar.

| İşlem | AVL yaklaşımı | Kırmızı-Siyah yaklaşımı |
|---|---|---|
| Ekleme | Yükseklik güncelle, $ \vert BF \vert >1$ ise döndür | Renk ihlalini boya/döndür |
| Silme | Her atada denge faktörünü izle | Siyah yükseklik eksilmesini onar |
| Garanti | Çok sıkı yükseklik | En uzun yol $\leq 2$ kat kısa yol |

Özetle AVL, arama gecikmesini mümkün olduğunca düşürmek isteyen sistemler için disiplinli bir bekçidir. Kırmızı-Siyah ağaç ise daha az katı denge karşılığında ekleme ve silmede pratik bir ritim sunar. Her ikisinin de sihri rotasyonlarda değil, rotasyonun **hangi durumda** ve **hangi invarianta** hizmet ederek uygulandığını anlamaktadır.

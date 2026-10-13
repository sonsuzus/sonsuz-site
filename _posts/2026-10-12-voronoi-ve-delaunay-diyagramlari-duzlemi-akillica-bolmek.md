---
layout: post
title: "Voronoi ve Delaunay Diyagramları: Düzlemi Akıllıca Bölmek"
math: true
categories: 
  - Bilgi
tags: 
  - voronoi
  - delaunay
  - hesaplamalı geometri
  - coğrafi bilgi sistemleri
  - python
  - algoritma
toc: true
image: /img/voronoi-ve-delaunay-46.png
---

Bir haritada size en yakın hastaneyi bulmak, baz istasyonlarının kapsama alanlarını tahmin etmek veya dağınık ölçüm noktalarından düzgün bir arazi modeli üretmek aynı geometrik soruya dayanabilir: Düzlemdeki noktalar arasında komşuluk ve yakınlık nasıl tanımlanır? Voronoi diyagramları ile Delaunay üçgenlemeleri, bu soruya birbirini tamamlayan iki zarif cevap verir. Biri düzlemi bölgelere ayırırken diğeri noktaları anlamlı kenarlarla birleştirir.


![voronoi-ve-delaunay-46](/img/voronoi-ve-delaunay-46.svg)

``

## Voronoi diyagramının temel fikri

Düzlemde $P = \{p_1,p_2,\ldots,p_n\}$ biçiminde bir nokta kümesi bulunduğunu düşünelim. Bu noktalar hastane, market, meteoroloji istasyonu veya oyun haritasındaki üsler olabilir. Bir $p_i$ noktasına ait Voronoi hücresi, düzlemde o noktaya diğer bütün noktalardan daha yakın olan konumları içerir:

$$V(p_i)=\{x \mid d(x,p_i) \leq d(x,p_j),\; j \neq i\}$$

Buradaki $d$, çoğunlukla Öklid uzaklığıdır:

$$d(a,b)=\sqrt{(a_x-b_x)^2+(a_y-b_y)^2}$$

İki hücrenin sınırı, ilgili iki noktaya eşit uzaklıktaki konumlardan oluşur. Yani sınırlar, nokta çiftlerini birleştiren doğru parçalarının orta dikmelerinden türetilir. Üç veya daha fazla hücrenin buluştuğu köşeler ise birkaç noktaya aynı uzaklıktadır.

Örneğin şehirdeki itfaiye merkezlerini üretici noktalar olarak kullanırsak her Voronoi hücresi, teorik olarak ilgili merkezin en yakın olduğu hizmet alanını gösterir. Elbette gerçek dünyada yollar, trafik ve nehirler Öklid geometrisine pek kulak asmayabilir; geometri bazen “kuş uçuşu” kadar iyimserdir.

## Delaunay üçgenlemesi: Voronoi'nin geometrik ikizi

Delaunay üçgenlemesi, Voronoi diyagramının dual grafıdır. Voronoi hücreleri ortak bir kenar paylaşan iki üretici nokta, Delaunay diyagramında bir kenarla bağlanır. Oluşan üçgenlerin önemli özelliği, her üçgenin çevrel çemberinin içinde başka bir giriş noktasının bulunmamasıdır.

| Özellik | Voronoi | Delaunay |
|---|---|---|
| Ana yapı | Çokgensel bölgeler | Üçgen ağı |
| Temel soru | Hangi nokta en yakın? | Hangi noktalar komşu? |
| Elemanlar | Hücre, kenar, köşe | Nokta, kenar, üçgen |
| Kullanım | Kapsama ve etki alanı | Ağ üretimi ve enterpolasyon |
| Dual ilişki | Hücre komşuluğu verir | Komşu hücre merkezlerini bağlar |

Delaunay üçgenlemesi, mümkün olan üçgenlemeler arasında en küçük açıları büyütme eğilimindedir. Böylece uzun, ince ve sayısal hesaplamalarda sorun çıkarabilecek “iğne üçgenlerin” sayısı azalır. Bu özellik sonlu elemanlar yöntemi, arazi modelleme ve yüzey oluşturma açısından değerlidir.

## Python ile hızlı bir deney

Aşağıdaki kod rastgele noktalar üretir, SciPy ile iki yapıyı hesaplar ve Matplotlib üzerinde gösterir:

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d, Delaunay

# Aynı sonucu yeniden üretebilmek için sabit tohum kullanıyoruz.
rng = np.random.default_rng(42)
points = rng.random((15, 2))

vor = Voronoi(points)
tri = Delaunay(points)

fig, axes = plt.subplots(1, 2, figsize=(11, 5))
voronoi_plot_2d(vor, ax=axes[0], show_vertices=True)
axes[0].set_title("Voronoi Bölgeleri")

axes[1].triplot(points[:, 0], points[:, 1], tri.simplices)
axes[1].scatter(points[:, 0], points[:, 1], color="red")
axes[1].set_title("Delaunay Üçgenlemesi")
plt.show()
```

`Voronoi` sınıfı bölgesel sınırları hesaplar. `Delaunay` ise hangi üç noktanın bir üçgen oluşturacağını `simplices` dizisinde saklar. Aynı nokta kümesinin solda alanlara, sağda bağlantılara dönüştüğünü görmek dualiteyi sezgisel hâle getirir.

## Nerelerde karşımıza çıkar?

Coğrafi bilgi sistemlerinde Voronoi bölgeleri okul, hastane ve mağaza erişilebilirliğinin ilk yaklaşımını sağlar. Ekolojide ağaçların rekabet alanları, telekomünikasyonda vericilerin kapsama bölgeleri ve robotikte en yakın engel ilişkileri modellenebilir. Delaunay üçgenleri ise düzensiz üçgen ağlarıyla arazi yüksekliği enterpolasyonu, 3B modelleme, fizik simülasyonu ve sensör ağlarının komşuluk analizi için kullanılır.

Standart düzlem algoritmaları bu yapıları genellikle $O(n\log n)$ zamanda üretebilir. Ancak eş konumlu noktalar, aynı çember üzerindeki çok sayıda nokta ve kayan nokta hassasiyeti özel dikkat ister. Sonuç olarak Voronoi “alan kime ait?” sorusunu, Delaunay ise “kim kimin komşusu?” sorusunu yanıtlar; birlikte kullanıldıklarında düzlemdeki dağınık veriyi anlaşılır bir geometrik hikâyeye dönüştürürler.

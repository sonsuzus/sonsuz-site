---
layout: post
title: "Yıldızlara Bakarak Yön Bulmak: Yıldız Haritalama ve Gök Cismi Tanıma Algoritmaları"
math: true
categories: 
  - Bilgi
tags: 
  - yıldız haritalama
  - görüntü işleme
  - uzay teknolojileri
  - bilgisayarlı görü
  - algoritma
  - python
toc: true
image: /img/yildizlara-bakarak-yon-64.png
---

Okyanusta kaybolan denizciler yüzyıllarca yıldızlardan yararlandı; modern uzay araçları da benzer bir yöntem kullanıyor, ancak ellerinde pusula yerine kamera, yıldız kataloğu ve bolca matris hesabı var. **Yıldız izleyici** adı verilen sistemler, gökyüzü görüntüsündeki ışık noktalarını tanıyarak aracın uzaydaki yönelimini son derece hassas biçimde hesaplıyor.

![yildizlara-bakarak-yon-64](/img/yildizlara-bakarak-yon-64.svg)

``
## Önce önemli bir ayrım: Konum mu, yönelim mi?

Yıldızlar çok uzak olduğu için farklı noktalardan bakıldığında doğrultuları neredeyse değişmez. Bu nedenle tek bir yıldız görüntüsü çoğunlukla aracın doğrudan konumunu değil, **yönelimini** (attitude) verir. Yönelim; aracın hangi tarafa baktığını, yani üç eksen çevresindeki dönüşünü ifade eder.

Mutlak konum belirlemek için yıldız ölçümleri; yörünge modeli, GPS, radyo sinyalleri, Güneş sensörleri veya gezegen görüntüleriyle birleştirilir. Yakın gök cisimlerinde görülen paralaks da kullanılabilir:

$$p \approx \frac{b}{d}$$

Burada $p$ paralaks açısı, $b$ gözlem noktaları arasındaki taban mesafesi, $d$ ise hedefin uzaklığıdır. Uzak yıldızlarda $d$ devasa olduğundan paralaks küçücük kalır.

## Kamera görüntüsünden yıldız listesine

Ham görüntüde yıldızların yanında sensör gürültüsü, kozmik ışın izleri ve sıcak pikseller bulunabilir. Algoritma önce arka plan parlaklığını tahmin eder, görüntüyü filtreler ve belirli bir eşiğin üzerindeki pikselleri gruplar. Her grubun ağırlıklı merkezi hesaplanarak yıldızın alt piksel hassasiyetindeki konumu bulunur:

$$x_c = \frac{\sum I_i x_i}{\sum I_i}, \qquad y_c = \frac{\sum I_i y_i}{\sum I_i}$$

$I_i$ piksel parlaklığıdır. Parlak pikseller merkeze daha fazla katkı verdiği için bu yöntem yalnızca en parlak pikseli seçmekten daha hassastır.

| Aşama | Girdi | Çıktı | Temel sorun |
|---|---|---|---|
| Ön işleme | Ham kamera karesi | Temiz görüntü | Gürültü ve sıcak pikseller |
| Merkez bulma | Parlak piksel kümeleri | $(x,y)$ noktaları | Optik bulanıklık |
| Eşleştirme | Nokta geometrisi | Yıldız kimlikleri | Yanlış veya eksik yıldızlar |
| Yönelim çözümü | Bilinen doğrultular | Dönüş matrisi/kuaterniyon | Ölçüm hataları |

## Bu yıldız hangisi?

Sistemin belleğinde yıldızların parlaklıklarını ve göksel koordinatlarını içeren bir katalog bulunur. Ancak yalnızca parlaklığa güvenmek risklidir; kamera pozlaması ve yıldız değişkenliği ölçümü etkiler. Bunun yerine yıldız çiftleri arasındaki açılar veya üç yıldızın oluşturduğu üçgenler karşılaştırılır.

**Lost-in-space** yaklaşımında araç başlangıç yönelimini hiç bilmiyormuş gibi davranır. Görüntüdeki üçgenin kenar açıları katalogdaki önceden indekslenmiş üçgenlerle aranır. Aday eşleşme, diğer yıldızlarla doğrulanır. Kabaca çalışan aşağıdaki Python örneği, üç nokta arasındaki piksel uzaklıklarını değişmez bir imzaya dönüştürür:

```python
from itertools import combinations
from math import hypot

def triangle_signature(points):
    # Üçgen kenarlarını hesaplayıp en uzun kenara göre normalize eder.
    distances = [
        hypot(a[0] - b[0], a[1] - b[1])
        for a, b in combinations(points, 2)
    ]
    distances.sort()
    longest = distances[-1]
    return tuple(round(d / longest, 4) for d in distances)

observed = [(120.4, 80.2), (244.1, 91.8), (175.6, 210.3)]
print(triangle_signature(observed))
```

Normalizasyon, görüntünün ölçeği değişse bile benzer üçgenlerin karşılaştırılmasını kolaylaştırır. Gerçek sistemler piksel uzaklığı yerine kamera modeliyle hesaplanan açısal mesafeleri ve hızlı arama tablolarını kullanır.

## Yönelim nasıl çıkarılıyor?

Eşleştirmeden sonra katalogdaki yıldız doğrultuları $\mathbf{r}_i$ ile kamerada ölçülen doğrultular $\mathbf{b}_i$ bilinir. Amaç, bu vektörleri en iyi hizalayan $R$ dönüşünü bulmaktır:

$$\min_R \sum_i w_i \\vert \mathbf{b}_i - R\mathbf{r}_i\\vert ^2$$

Bu problem **Wahba problemi** olarak bilinir; QUEST, Davenport q-yöntemi veya SVD ile çözülebilir. Sonuç genellikle sayısal açıdan kararlı bir kuaterniyon olarak tutulur.

Bir yıldız izleyici böylece birkaç ışık noktasını kozmik bir QR kod gibi okuyabilir. Jiroskop kısa süreli hızlı hareketleri takip ederken yıldız ölçümleri zamanla biriken sürüklenmeyi düzeltir. Sonuç: Uzay aracı, milyarlarca kilometre ötede bile başını hangi yöne çevirdiğini bilir.

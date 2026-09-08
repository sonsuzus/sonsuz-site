---
layout: post
title: "Oyun Motorlarında Uzamsal Bölme: Quadtree ve Octree ile Görünmeyeni İşlememek"
math: true
categories: 
  - Bilgi
tags: 
  - oyun motoru
  - quadtree
  - octree
toc: true
---

Bir oyun sahnesinde binlerce nesne bulunabilir; fakat kameranın aynı anda bunların yalnızca küçük bir bölümünü görmesi muhtemeldir. Her karede bütün nesneleri çizim testinden geçirmek, görünmeyen ejderhalara bile işlemci zamanı ayırmak demektir. Quadtree ve octree gibi uzamsal bölme yapıları, dünyayı hiyerarşik bölgelere ayırarak ilgili nesneleri hızla bulmamızı ve gereksiz kontrolleri azaltmamızı sağlar.
``

## Uzamsal bölmenin temel fikri

En basit yaklaşımda sahnedeki $n$ nesnenin tamamı kamera görüş hacmiyle karşılaştırılır. Bu işlemin maliyeti yaklaşık $O(n)$ olur. Uzamsal bölmede ise önce büyük bölgeler test edilir. Bir bölge görünmüyorsa içindeki yüzlerce nesne tek hamlede elenir.

İdeal ve dengeli bir ağaçta arama maliyeti kabaca $O(\log n + k)$ biçiminde düşünülebilir. Buradaki $k$, gerçekten bulunan veya işlenmesi gereken nesne sayısıdır. Elbette oyun dünyaları matematik kitaplarındaki kadar düzenli değildir; dağılım dengesizse performans da değişir.

| Yapı | Bölünme biçimi | Uygun kullanım | Çocuk sayısı |
|---|---|---|---:|
| Quadtree | X-Z düzlemi dört parçaya ayrılır | Arazi, strateji oyunu, harita | 4 |
| Octree | X-Y-Z uzayı sekiz parçaya ayrılır | Uçuş, uzay ve iç mekân sahneleri | 8 |
| Düzenli grid | Eşit boyutlu hücreler kullanılır | Benzer boyutlu, hareketli nesneler | Sabit komşuluk |

## Quadtree ve octree nasıl büyür?

Kök düğüm tüm oyun alanını temsil eder. Bir düğümdeki nesne sayısı belirlenen kapasiteyi aşarsa düğüm bölünür. Quadtree dört, octree sekiz çocuk üretir. Bu işlem maksimum derinliğe ulaşılana veya düğümler yeterince seyrekleşene kadar sürer.

Bir nesne tamamen tek bir alt bölgeye sığıyorsa o çocuğa taşınabilir. Birden fazla bölgeye yayılan büyük nesneler ise üst düğümde tutulabilir. Aynı nesneyi birçok çocuğa kopyalamak sorguları hızlandırabilse de bellek tüketimini ve yinelenen sonuç riskini artırır.

Bölge boyutu her seviyede yarıya düştüğünden, üç boyutlu bir düğümün hacmi için şu ilişki kurulabilir:

$$V_d = \frac{V_0}{8^d}$$

Burada $V_0$ kök hacmi, $d$ ise derinliktir. Çok büyük derinlik daha hassas seçim sağlarken düğüm ve dolaşım maliyetini yükseltir.

## Görüş hacmi eleme

Kamera görüşü genellikle altı düzlemle çevrili bir frustum olarak modellenir. Ağaç dolaşılırken her düğümün sınır kutusu bu hacimle karşılaştırılır:

- Bölge tamamen dışarıdaysa alt dallar ziyaret edilmez.
- Bölge tamamen içerideyse içindeki nesneler topluca kabul edilebilir.
- Bölge sınırı kesiyorsa çocuklar ayrı ayrı incelenir.

Bu süreç, uzamsal bölme ile **frustum culling** tekniğinin birlikte çalışmasıdır. Ağaç tek başına görünürlüğü belirlemez; yalnızca görünürlük testlerinin aday kümesini küçültür.

```csharp
void QueryVisible(Node node, Frustum camera, List<GameObject> result)
{
    // Bölgenin tamamı görünmüyorsa bütün alt ağacı eler.
    if (!camera.Intersects(node.Bounds))
        return;

    foreach (GameObject obj in node.Objects)
    {
        // Üst bölge kesişse bile nesne dışarıda olabilir.
        if (camera.Intersects(obj.Bounds))
            result.Add(obj);
    }

    if (!node.IsLeaf)
    {
        foreach (Node child in node.Children)
            QueryVisible(child, camera, result);
    }
}
```

Bu örnek, düğümleri özyinelemeli biçimde dolaşır. Gerçek bir motorda sonuç listesi çizim kuyruğuna aktarılabilir; ayrıca mesafe tabanlı LOD, gölge seçimi ve çarpışma sorguları için de kullanılabilir.

## Her sahneye octree mi?

Hayır; optimizasyon dünyasının altın kuralı ölçmektir. Sürekli hareket eden nesneler ağaçtan çıkarılıp yeniden yerleştirileceği için güncelleme maliyeti doğurur. Statik geometri octree içinde tutulurken hareketli karakterlerin ayrı bir yapı veya gevşek octree ile yönetilmesi yaygın bir çözümdür.

| Durum | Tercih |
|---|---|
| Yüksekliği önemsiz geniş arazi | Quadtree |
| Her yönde dağılan üç boyutlu dünya | Octree |
| Çok dinamik ve eş boyutlu nesneler | Grid veya spatial hash |

Doğru yapı seçildiğinde motor, “Her şeyi kontrol et” yaklaşımından “Yalnızca ilgili bölgelere bak” yaklaşımına geçer. Böylece CPU çizim hazırlığı azalır, kare süreleri dengelenir ve görünmeyen ejderhalar sonunda hak ettikleri şekilde görmezden gelinir.

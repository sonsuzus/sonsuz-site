---
layout: post
title: "Geometrik Kesilen Çizgiler: Voronoi Diyagramları ve Delaunay Nirengisi"
math: true
categories: 
  - Bilgi
tags: 
  - voronoi
  - delaunay
  - hesaplamalı-geometri
  - algoritma
  - python
  - üçgenleme
toc: true
image: /img/geometrik-kesilen-cizgiler-93.png
---

Bir şehre yeni itfaiye istasyonları yerleştirdiğimizi düşünelim. Her mahalle hangi istasyona daha yakın? İstasyonları birleştirerek düzgün ve çakışmayan bir iletişim ağı nasıl kurabiliriz? İlk sorunun cevabı **Voronoi diyagramı**, ikincisinin güçlü adaylarından biri ise onun geometrik ikizi olan **Delaunay nirengisi**dir. Bu iki yapı; haritacılıktan oyun geliştirmeye, robot rotalarından kablosuz ağlara kadar şaşırtıcı ölçüde geniş bir kullanım alanına sahiptir.
``
## Noktaların etki alanı: Voronoi diyagramı

Düzlemde $P=\{p_1,p_2,\ldots,p_n\}$ biçiminde bir nokta kümesi bulunsun. $p_i$ noktasına ait Voronoi hücresi, düzlemde bu noktaya diğer bütün noktalardan daha yakın olan konumların kümesidir:

$$
V(p_i)=\{x\mid d(x,p_i)\leq d(x,p_j),\; \forall j\neq i\}
$$

Burada Öklid uzaklığı genellikle

$$
d(a,b)=\sqrt{(a_x-b_x)^2+(a_y-b_y)^2}
$$

olarak hesaplanır. İki hücre arasındaki sınır, ilgili iki noktanın oluşturduğu doğru parçasının **dik orta doğrusundan** gelir. Birden fazla sınırın kesiştiği Voronoi köşesi ise çoğunlukla üç kaynak noktasına eşit uzaklıktadır. Başka bir deyişle noktalar görünmez mıknatıslar, hücreler de onların hakimiyet bölgeleridir.

## Geometrik ikiz: Delaunay nirengisi

Voronoi diyagramında ortak kenarı bulunan iki hücrenin kaynak noktalarını birleştirirsek Delaunay grafiğini elde ederiz. Genel konumdaki noktalar için bu grafik, düzlemi çakışmayan üçgenlere böler.

Delaunay nirengisinin temel koşulu **boş çember özelliğidir**: Her Delaunay üçgeninin çevrel çemberinin içinde başka bir kaynak noktası bulunmamalıdır. $a$, $b$ ve $c$ noktalarından geçen çember için herhangi bir $p$ noktası çemberin içindeyse mevcut köşegen geçersiz olabilir ve bir **kenar çevirme** işlemi gerekebilir.

| Özellik | Voronoi | Delaunay |
|---|---|---|
| Temel öğe | Etki hücreleri | Üçgenler ve kenarlar |
| Yakınlık yorumu | En yakın kaynağı gösterir | Yakın kaynakları bağlar |
| Ana geometrik test | Dik orta doğrular | Boş çevrel çember |
| Tipik kullanım | Kapsama ve bölgeleme | Ağ, yüzey ve arazi modeli |
| Birbirleriyle ilişkisi | Kenarlar Delaunay kenarlarını keser | Voronoi hücre komşularını bağlar |

Üstelik ikili yapıdaki karşılık gelen Voronoi ve Delaunay kenarları birbirine diktir. Geometri burada adeta iki farklı gözlükle aynı yakınlık bilgisini gösterir.

## Bowyer–Watson ile algoritmik yaklaşım

Delaunay nirengisi üretmenin anlaşılır yöntemlerinden biri **Bowyer–Watson** algoritmasıdır. Önce bütün noktaları kapsayan dev bir süper üçgen oluşturulur. Noktalar sırayla eklenir; yeni noktayı çevrel çemberinde barındıran üçgenler silinir ve oluşan çokgensel boşluk yeni üçgenlerle doldurulur.

```python
def bowyer_watson(points, super_triangle, in_circle):
    triangles = [super_triangle]

    for point in points:
        bad = [t for t in triangles if in_circle(point, t)]
        edge_count = {}

        for triangle in bad:
            for edge in triangle.edges():
                edge = tuple(sorted(edge))
                edge_count[edge] = edge_count.get(edge, 0) + 1

        boundary = [e for e, count in edge_count.items() if count == 1]
        triangles = [t for t in triangles if t not in bad]

        for edge in boundary:
            triangles.append(Triangle(edge[0], edge[1], point))

    return [t for t in triangles if not t.touches(super_triangle)]
```

Kodda iki kez görülen iç kenarlar elenir; yalnızca bir kez görülen kenarlar boşluğun sınırını oluşturur. `in_circle` testi sayısal hassasiyet açısından kritik olduğundan gerçek projelerde sağlam geometrik belirleyiciler kullanılmalıdır.

Naif uygulama yaklaşık $O(n^2)$ sürebilir. Noktasal konumlandırma ve uygun veri yapılarıyla beklenen süre $O(n\log n)$ düzeyine indirilebilir. Eşdoğrusal noktalar veya aynı çember üzerindeki dört nokta gibi özel durumlar da ayrıca ele alınmalıdır.

## Nerede karşımıza çıkar?

Voronoi; en yakın hastaneyi bulma, yağış istasyonlarının bölgelerini çıkarma ve oyun haritalarında doğal görünümlü biyomlar üretme işlerinde kullanılır. Delaunay ise arazi yüzeyi modelleme, sonlu elemanlar analizi ve robotların seyrek fakat kullanışlı bağlantı grafikleri kurmasında öne çıkar. Kısacası biri düzleme “Kime aitsin?” diye sorarken diğeri noktalara “Kiminle komşusun?” der.

![geometrik-kesilen-cizgiler-93](/img/geometrik-kesilen-cizgiler-93.svg)


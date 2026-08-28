---
layout: post
title: "Hesaplamalı Geometri Temelleri: Doğru Parçası Kesişimi ve Nokta-Çokgen Testleri"
math: true
categories: 
  - Bilgi
tags: 
  - hesaplamalı geometri
  - algoritmalar
  - python
---

Bilgisayarın çizgileri ve şekilleri anlaması, ekranda birkaç piksel boyamaktan çok daha derin bir iştir. Bir oyundaki merminin duvara çarpması, harita uygulamasında konumunuzun bir bölgeye ait olması veya CAD yazılımında iki kenarın çakışması; aynı geometrik sorulara dayanır: İki doğru parçası kesişiyor mu? Bir nokta çokgenin içinde mi?

``

Bu problemlerde kritik ayrım, **doğru** ile **doğru parçası** arasındadır. Sonsuza uzanan iki doğru bir noktada kesişebilir; fakat bu kesişim, çizilmiş iki parçanın uç sınırları dışında kalıyorsa gerçek bir temas yoktur. Bu nedenle yalnızca eğim hesaplamak yeterli değildir. Dikey doğrular, paralel çizgiler ve kayan noktalı sayı hataları da eğim tabanlı yaklaşımı kırılgan yapar.

## Yönelim testi: Geometrinin pusulası

Üç noktanın saat yönünde mi, saat yönünün tersinde mi, yoksa aynı doğru üzerinde mi bulunduğunu **çapraz çarpım** ile anlayabiliriz. $A(x_1,y_1)$, $B(x_2,y_2)$ ve $C(x_3,y_3)$ için:

$$
orient(A,B,C)=(x_2-x_1)(y_3-y_1)-(y_2-y_1)(x_3-x_1)
$$

Sonucun işareti yönelimi söyler: pozitif değer sola dönüşü, negatif değer sağa dönüşü, sıfır ise kolinerliği belirtir. İki parça $AB$ ve $CD$ genel durumda, $C$ ile $D$ noktaları $AB$'nin farklı taraflarındaysa ve aynı durum $A$, $B$ için de geçerliyse kesişir. Sınırdaki temasları kaçırmamak için ayrıca bir noktanın diğer parçanın eksen hizalı sınır kutusunda olup olmadığı kontrol edilir.

| Durum | Yönelim sonucu | Kesişim yorumu |
|---|---:|---|
| Genel kesişim | İşaretler karşıt | Parçalar iç bölgede kesişir |
| Paralel | Yönelimler tutarlı | Kesişim yoktur |
| Koliner temas | Sonuçlardan biri 0 | Sınır kutusu kontrolü gerekir |
| Ortak uç | Sonuçlardan biri 0 | Genellikle kesişim kabul edilir |

Aşağıdaki Python kodu, hem klasik kesişimleri hem de uç uca veya üst üste gelme durumlarını ele alır:

```python
def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def on_segment(a, b, p):
    return (min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and
            min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))

def segments_intersect(a, b, c, d):
    o1, o2 = orient(a, b, c), orient(a, b, d)
    o3, o4 = orient(c, d, a), orient(c, d, b)

    if o1 * o2 < 0 and o3 * o4 < 0:
        return True

    return ((o1 == 0 and on_segment(a, b, c)) or
            (o2 == 0 and on_segment(a, b, d)) or
            (o3 == 0 and on_segment(c, d, a)) or
            (o4 == 0 and on_segment(c, d, b)))
```

## Nokta çokgenin içinde mi?

Bu soruda popüler yöntem **ışın dökümü**dür (ray casting). Test noktasından sağa doğru hayali bir ışın gönderilir. Işının çokgen kenarlarını kesme sayısı tekse nokta içeridedir; çiftse dışarıdadır. Mantık basittir: Her sınır geçişi, içerisi ve dışarısı durumunu değiştirir.

| Yöntem | Ana fikir | Karmaşıklık | Güçlü yanı |
|---|---|---:|---|
| Işın dökümü | Kesişim sayısının tekliği | $O(n)$ | Uygulaması kolay |
| Sarma sayısı | Nokta etrafındaki açısal dönüş | $O(n)$ | Karmaşık çokgenlerde açıklayıcı |
| Üçgenleme | Çokgeni üçgenlere ayırma | Ön işlem gerekir | Çoklu sorguda avantajlı |

```python
def point_in_polygon(p, polygon):
    x, y = p
    inside = False

    for i in range(len(polygon)):
        a = polygon[i]
        b = polygon[(i + 1) % len(polygon)]
        if (a[1] > y) != (b[1] > y):
            x_hit = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x < x_hit:
                inside = not inside
    return inside
```

Kod, her kenarın test noktasının yatay seviyesini aşıp aşmadığını inceler; aşıyorsa ışının kesişim konumunu hesaplar ve `inside` değerini tersine çevirir. Üretim ortamında noktanın doğrudan bir kenar üzerinde olmasını ayrı bir politika olarak tanımlayın: Bu durum çoğu harita ve çarpışma sisteminde `içeride` kabul edilir. Ayrıca ondalıklı koordinatlarda $0$ yerine küçük bir $\varepsilon$ toleransı kullanmak, sayısal sürprizleri azaltır.

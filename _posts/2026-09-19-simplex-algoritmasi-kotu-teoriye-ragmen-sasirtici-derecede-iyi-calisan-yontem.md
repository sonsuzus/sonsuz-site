---
layout: post
title: "Simplex Algoritması: Kötü Teoriye Rağmen Şaşırtıcı Derecede İyi Çalışan Yöntem"
math: true
categories: 
  - Bilgi
tags: 
  - simplex
  - doğrusal programlama
  - optimizasyon
  - algoritma
  - python
  - matematik
toc: true
---

Simplex algoritması, doğrusal optimizasyon problemlerini çözmek için 1947 yılında George Dantzig tarafından geliştirildi. İlginç olan şu: Algoritmanın en kötü durumdaki çalışma süresi üstel olabilir, fakat gerçek hayattaki problemlerde çoğunlukla son derece hızlıdır. Kısacası Simplex, teorik karnesi biraz problemli olsa da iş hayatında sürekli terfi alan o gizemli çalışan gibidir.

``

## Doğrusal optimizasyon nedir?

Doğrusal optimizasyonda amaç, doğrusal bir hedef fonksiyonunu yine doğrusal kısıtlar altında en iyi hâle getirmektir. Standart bir maksimizasyon problemi şöyle yazılabilir:

$$
\max\; c^T x
$$

$$
Ax \le b, \qquad x \ge 0
$$

Burada $x$ karar değişkenlerini, $c$ değişkenlerin hedefe katkısını, $A$ kısıt katsayılarını ve $b$ mevcut kaynakları temsil eder. Örneğin bir fabrikanın masa ve sandalye üreterek kârını artırması, fakat ahşap ve işçilik sınırlarını aşmaması bu yapıya uyar.

İki değişkenli bir problem geometrik olarak düşünüldüğünde kısıtlar, uygun çözümlerden oluşan dışbükey bir çokgen meydana getirir. Doğrusal hedef fonksiyonunun optimum değeri, uygun bölge boş veya sınırsız değilse bu çokgenin köşe noktalarından en az birinde bulunur. Simplex’in temel fikri tam olarak budur: Bütün alanı taramak yerine köşeler arasında daha iyi hedef değerine doğru yürümek.

## Simplex nasıl ilerler?

Algoritma önce bir temel uygun çözüm seçer. Eşitsizlikleri eşitliğe dönüştürmek için gevşeklik değişkenleri eklenir:

$$
2x_1+x_2 \le 10 \quad \Rightarrow \quad 2x_1+x_2+s_1=10
$$

Ardından hedef değerini iyileştirecek bir **giren değişken** ve uygunluğu koruyacak bir **çıkan değişken** belirlenir. Pivot işlemiyle yeni bir köşeye geçilir. Hedef satırında iyileştirme sağlayabilecek katsayı kalmadığında optimum çözüme ulaşılmıştır.

| Yaklaşım | İzlenen yol | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| Köşeleri tek tek denemek | Tüm adayları inceler | Mantığı basittir | Köşe sayısı çok büyüyebilir |
| Simplex | Komşu ve umut verici köşelere geçer | Pratikte çok hızlıdır | En kötü durumda üstel sürebilir |
| İç nokta yöntemi | Bölgenin içinden ilerler | Güçlü teorik sınırları vardır | Hassas ayar ve lineer cebir maliyeti doğurur |

## Küçük bir Python uygulaması

Aşağıdaki eğitim amaçlı kod, $Ax \le b$ ve $x \ge 0$ biçimindeki basit maksimizasyon problemlerini tablo yöntemiyle çözer. Son sütun sağ taraf değerlerini, son satır ise hedef fonksiyonunu taşır.

```python
import numpy as np

def simplex(c, A, b):
    m, n = A.shape
    tablo = np.zeros((m + 1, n + m + 1))
    tablo[:m, :n] = A
    tablo[:m, n:n + m] = np.eye(m)
    tablo[:m, -1] = b
    tablo[-1, :n] = -c

    while np.min(tablo[-1, :-1]) < 0:
        giren = np.argmin(tablo[-1, :-1])
        sutun = tablo[:m, giren]

        if np.all(sutun <= 0):
            raise ValueError('Problem sınırsızdır')

        oranlar = np.where(sutun > 0, tablo[:m, -1] / sutun, np.inf)
        cikan = np.argmin(oranlar)

        tablo[cikan] /= tablo[cikan, giren]
        for satir in range(m + 1):
            if satir != cikan:
                tablo[satir] -= tablo[satir, giren] * tablo[cikan]

    return tablo[-1, -1], tablo

c = np.array([3, 2])
A = np.array([[2, 1], [1, 2]])
b = np.array([10, 8])

optimum, son_tablo = simplex(c, A, b)
print('En yüksek hedef değeri:', optimum)
```

Kod, en negatif hedef katsayısını giren değişken olarak seçer. Minimum oran testi çıkan değişkeni belirler; böylece yeni çözüm kısıtları ihlal etmez. Gerçek üretim sistemlerinde ise sayısal toleranslar, dejenerasyon, eşitlik kısıtları ve yapay değişkenler de ele alınmalıdır.

## Peki neden pratikte bu kadar başarılı?

Simplex için özel olarak tasarlanmış bazı problemlerde köşe sayısının üstel bir bölümünü dolaşmak mümkündür. Örneğin Klee–Minty küpü, belirli pivot kurallarını kasıtlı olarak kötü davranmaya zorlar. Ancak gerçek veriler genellikle bu kadar düşmanca düzenlenmez. Ayrıca modern çözücüler güçlü pivot kuralları, ön işleme, ölçekleme ve yeniden optimizasyon teknikleri kullanır.

Sonuç olarak Simplex, en kötü durum analizi ile pratik performansın her zaman aynı hikâyeyi anlatmadığını gösteren harika bir örnektir. Matematiksel garantiler önemlidir; fakat veri yapısı, mühendislik kararları ve iyi sezgiler de bir algoritmanın gerçek dünyadaki kaderini belirler.

---
layout: post
title: "Lineer Programlama ve Simpleks Yöntemiyle En İyi Kararı Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - lineer programlama
  - simpleks
  - optimizasyon
  - yöneylem araştırması
  - python
toc: true
image: /img/lineer-programlama-ve-10.png
---

Bir fabrikanın sınırlı ham maddelerle hangi üründen kaç tane üretmesi gerektiğini düşünün. Kârı artırmak istiyoruz; ancak işçilik, bütçe ve makine süresi sonsuz değil. Lineer programlama, bu tür kararları matematiksel bir modele dönüştürür. Simpleks yöntemi ise uygun çözümler arasında gezinerek en iyi noktayı bulur. Kısacası, kaynaklar az ama beklentiler yüksekse sahne simpleksindir!


![lineer-programlama-ve-10](/img/lineer-programlama-ve-10.svg)

``

## Lineer programlamanın temel modeli

Bir lineer programlama problemi; **karar değişkenleri**, **amaç fonksiyonu**, **kısıtlar** ve **işaret koşullarından** oluşur. Genel bir maksimizasyon modeli şöyle yazılabilir:

$$
\max Z = c_1x_1 + c_2x_2 + \dots + c_nx_n
$$

Kısıtlar ise aşağıdaki biçimdedir:

$$
a_{i1}x_1 + a_{i2}x_2 + \dots + a_{in}x_n \leq b_i
$$

Burada $x_j$ karar değişkenlerini, $c_j$ birim katkıları, $a_{ij}$ kaynak kullanım miktarlarını ve $b_i$ mevcut kaynak kapasitesini gösterir. Genellikle $x_j \geq 0$ koşulu eklenir; çünkü eksi üç masa üretmek ticari açıdan biraz yaratıcı kaçacaktır.

| Model öğesi | Sorduğu soru | Örnek |
|---|---|---|
| Karar değişkeni | Neyi belirliyoruz? | Ürün adetleri |
| Amaç fonksiyonu | Neyi iyileştiriyoruz? | Toplam kâr |
| Kısıt | Bizi ne sınırlıyor? | İşçilik süresi |
| İşaret koşulu | Hangi değerler geçerli? | $x_1,x_2 \geq 0$ |

## Simpleks neden köşeleri gezer?

Lineer kısıtların oluşturduğu bölgeye **uygun çözüm bölgesi** denir. Bu bölge geometrik olarak dışbükey bir çokgendir veya daha yüksek boyutlarda bir çokyüzlüdür. Lineer bir amaç fonksiyonunun sonlu optimumu varsa, en az bir optimum çözüm bu bölgenin köşe noktalarından birindedir.

Grafik yöntemi iki değişkende işe yarar; fakat yüzlerce değişken olduğunda çizim tahtası pes eder. Simpleks, bir köşeden komşu ve daha iyi bir köşeye geçerek ilerler. Amaç değeri artık iyileştirilemiyorsa optimuma ulaşılmıştır.

| Yöntem | Güçlü yanı | Sınırlaması |
|---|---|---|
| Grafik yöntem | Görsel ve öğreticidir | Genellikle iki değişkenlidir |
| Simpleks | Büyük modellerde etkilidir | En kötü durumda çok adım atabilir |
| İç nokta | Dev problemlerde güçlüdür | Köşe mantığı daha az sezgiseldir |

## Küçük bir üretim örneği

Bir işletme masa ve sandalye üretsin. Bir masanın kârı 40, sandalyenin kârı 30 birim olsun:

$$
\max Z = 40x_1 + 30x_2
$$

Kaynak kısıtları şöyle verilsin:

$$
2x_1+x_2\leq100
$$

$$
x_1+2x_2\leq80
$$

Eşitsizlikleri denkleme çevirmek için kullanılmayan kapasiteyi temsil eden **gevşeklik değişkenleri** eklenir:

$$
2x_1+x_2+s_1=100
$$

$$
x_1+2x_2+s_2=80
$$

Başlangıçta $x_1=x_2=0$ alınır; dolayısıyla $s_1=100$ ve $s_2=80$ olur. Simpleks tablosunda amaç fonksiyonunu en hızlı iyileştirecek değişken baza girer. Oran testiyle hangi temel değişkenin bazdan çıkacağı seçilir. **Pivot işlemi**, seçilen sütun ve satır üzerinden tabloyu yeni köşeye taşır.

Süreç üç adımda özetlenebilir:

1. Baza girecek değişkeni seç.
2. Pozitif katsayılar üzerinde oran testi yap.
3. Pivot uygula ve optimumluk koşulunu yeniden denetle.

## Python ile çözüm

SciPy içindeki `linprog` minimizasyon yaptığı için kâr katsayılarını negatif veririz:

```python
from scipy.optimize import linprog

# Maksimizasyon: 40*x1 + 30*x2
c = [-40, -30]
A = [[2, 1], [1, 2]]
b = [100, 80]

sonuc = linprog(c, A_ub=A, b_ub=b,
                bounds=[(0, None), (0, None)],
                method="highs")

print("Üretim planı:", sonuc.x)
print("Maksimum kâr:", -sonuc.fun)
```

Çözüm $x_1=40$, $x_2=20$ ve $Z=2200$ değerlerini verir. Her iki kaynak da tamamen kullanılır. Gerçek projelerde model kurulurken katsayıların doğruluğu, çözümün kendisi kadar önemlidir: Simpleks yanlış modele kusursuz cevap verebilir. Bu nedenle sonuçlar duyarlılık analiziyle incelenmeli; kaynak miktarı veya kâr katsayıları değiştiğinde optimum planın nasıl etkilendiği mutlaka sorgulanmalıdır.

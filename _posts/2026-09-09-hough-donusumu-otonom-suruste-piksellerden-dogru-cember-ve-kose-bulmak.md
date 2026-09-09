---
layout: post
title: "Hough Dönüşümü: Otonom Sürüşte Piksellerden Doğru, Çember ve Köşe Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - görüntü işleme
  - hough dönüşümü
  - otonom sürüş
toc: true
---

Otonom bir araç kameraya baktığında şerit, trafik levhası veya yol köşesi görmez; yalnızca renk ve parlaklık değerlerinden oluşan bir piksel matrisi görür. Hough dönüşümü, bu dağınık pikselleri geometrik şekillere dönüştüren güçlü bir oylama yöntemidir. Ancak işin sırrı yalnızca Hough algoritmasında değil, görüntü türevleriyle bulunan kenarların doğru yorumlanmasındadır.
``

## Önce kenarlar: Türevler neden gerekli?

Bir görüntü, iki değişkenli bir yoğunluk fonksiyonu olarak düşünülebilir: $I(x,y)$. Piksel parlaklığının hızla değiştiği yerler nesne veya şerit sınırlarına karşılık gelir. Bu değişim, görüntünün gradyanı ile ölçülür:

$$
\nabla I = \left(\frac{\partial I}{\partial x},\frac{\partial I}{\partial y}\right)
$$

Gradyan büyüklüğü $\vert \nabla I\vert $, kenarın ne kadar güçlü olduğunu; yönü ise kenarın hangi tarafa baktığını gösterir. Sobel ve Canny gibi algoritmalar bu kısmi türevleri yaklaşık olarak hesaplar. Burada doğrudan bir diferansiyel denklem çözülmez; diferansiyel hesap, geometrik adayları üretmek için kullanılır.

| Yöntem | Matematiksel fikir | Otonom sürüşte kullanım |
|---|---|---|
| Canny | Gradyan ve maksimum bastırma | Şerit ve levha sınırları |
| Doğru Hough | $(\rho,\theta)$ uzayında oylama | Yol şeritleri |
| Çember Hough | $(a,b,r)$ uzayında oylama | Yuvarlak trafik levhaları |
| Harris köşe | Gradyanların iki yöndeki değişimi | Kavşak ve karakteristik noktalar |

## Doğruların parametre uzayındaki yolculuğu

Bir doğruyu $y=mx+b$ biçiminde göstermek dikey doğrularda sorun çıkarır. Hough dönüşümü bunun yerine normal formu kullanır:

$$
\rho=x\cos\theta+y\sin\theta
$$

Burada $\rho$, doğrunun orijine uzaklığı; $\theta$ ise normal vektörünün açısıdır. Her kenar pikseli, olası doğrular için $(\rho,\theta)$ tablosundaki hücrelere oy verir. Çok oy alan hücreler, görüntüde gerçekten bulunması muhtemel doğruları temsil eder. Böylece kesintili veya kısmen kapanmış şeritler bile yakalanabilir.

## Çemberler ve artan hesaplama maliyeti

Merkezi $(a,b)$ ve yarıçapı $r$ olan çemberin denklemi şöyledir:

$$
(x-a)^2+(y-b)^2=r^2
$$

Her kenar pikseli olası merkez ve yarıçaplara oy verdiği için parametre uzayı üç boyutludur. Bu nedenle çember Hough, doğru Hough’a göre daha pahalıdır. Bilinen levha boyutlarına göre yarıçap aralığını sınırlamak, hem yanlış tespitleri hem de işlem süresini azaltır.

## Peki keskin köşeler?

Klasik Hough dönüşümü doğrudan köşe bulmak için tasarlanmamıştır. Köşeler genellikle Harris veya Shi-Tomasi ile tespit edilir. Harris yönteminde yerel gradyanlardan yapı tensörü oluşturulur:

$$
M=\sum w(x,y)\begin{bmatrix}I_x^2&I_xI_y\\I_xI_y&I_y^2\end{bmatrix}
$$

Matrisin iki özdeğeri de büyükse yoğunluk iki yönde değişiyor demektir; yani orada güçlü bir köşe vardır. Alternatif olarak Hough ile bulunan doğruların kesişimleri de kavşak veya şerit birleşimi adayı sayılabilir.

## OpenCV ile küçük bir şerit dedektörü

```python
import cv2
import numpy as np

image = cv2.imread("road.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Gürültüyü azaltıp türev tabanlı Canny kenarlarını çıkarır.
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur, 50, 150)

# Kesintili şeritleri doğru parçaları olarak bulur.
lines = cv2.HoughLinesP(
    edges, 1, np.pi / 180,
    threshold=60,
    minLineLength=40,
    maxLineGap=25
)

if lines is not None:
    for x1, y1, x2, y2 in lines[:, 0]:
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
```

Gerçek bir otonom sürüş sisteminde görüntünün yalnızca yol bölgesi işlenir, perspektif dönüşümü uygulanır ve zamansal filtrelerle titreşim azaltılır. Kısacası türevler anlamlı kenarları ortaya çıkarır, Hough bu kenarları geometrik modellere dönüştürür, köşe algoritmaları ise yön değişimlerini yakalar. Pikseller böylece aracın karar verebileceği bir yol haritasına dönüşür.

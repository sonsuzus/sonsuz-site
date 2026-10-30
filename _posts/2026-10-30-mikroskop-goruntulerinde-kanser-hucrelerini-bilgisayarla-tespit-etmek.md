---
layout: post
title: "Mikroskop Görüntülerinde Kanser Hücrelerini Bilgisayarla Tespit Etmek"
math: true
categories: 
  - Proje
tags: 
  - yapay zeka
  - görüntü işleme
  - kanser araştırmaları
  - makine öğrenmesi
  - opencv
  - mikroskopi
toc: true
image: /img/mikroskop-goruntulerinde-kanser-62.png
---

Mikroskop altında yüzlerce hücreyi tek tek incelemek, samanlıkta iğne aramaya benzeyebilir. Bilgisayarlı görüntü analizi ise şüpheli hücreleri otomatik biçimde işaretleyerek araştırmacılara ve patologlara yardımcı olur. Gelin, bir mikroskop görüntüsünün piksellerden hücre adaylarına, oradan da sınıflandırma sonucuna uzanan yolculuğunu inceleyelim.

![mikroskop-goruntulerinde-kanser-62](/img/mikroskop-goruntulerinde-kanser-62.svg)

``

## Problem aslında nedir?

Kanser hücreleri sağlıklı hücrelerden çekirdek büyüklüğü, şekil düzensizliği, kromatin yoğunluğu ve hücre bölünme hızı gibi özelliklerle ayrılabilir. Ancak boyama yöntemi, mikroskop ışığı ve doku türü değiştikçe görüntünün görünümü de değişir. Dolayısıyla bilgisayar yalnızca “koyu renkli olan kanserdir” gibi basit bir kuralla güvenilir sonuç üretemez.

Tipik bir sistem dört aşamadan oluşur:

1. Görüntünün renk ve gürültü bakımından düzeltilmesi
2. Hücre veya çekirdeklerin bölütlenmesi
3. Her hücreden açıklayıcı özelliklerin çıkarılması
4. Hücrenin normal ya da anormal olarak sınıflandırılması

| Aşama | Amaç | Örnek yöntem |
|---|---|---|
| Ön işleme | Görüntü farklılıklarını azaltmak | Gaussian filtre, renk normalizasyonu |
| Bölütleme | Hücre sınırlarını bulmak | Otsu eşikleme, watershed, U-Net |
| Özellik çıkarımı | Hücreyi sayılarla tanımlamak | Alan, çevre, doku, yuvarlaklık |
| Sınıflandırma | Anormallik olasılığı üretmek | SVM, rastgele orman, CNN |

## Hücreyi matematikle anlatmak

Bir hücrenin alanı $A$, çevresi $P$ ile gösterilsin. Şeklin ne kadar dairesel olduğunu ölçmek için şu değer kullanılabilir:

$$C = \frac{4\pi A}{P^2}$$

Kusursuz bir dairede $C$ değeri 1'e yaklaşır. Girintili çıkıntılı hücrelerde ise küçülür. Bunun yanında çekirdeğin ortalama parlaklığı, renk dağılımı ve komşularına göre büyüklüğü de modele verilebilir.

Sınıflandırıcı çoğu zaman $p(y=1\mid x)$, yani özellikleri $x$ olan hücrenin anormal olma olasılığını hesaplar. Olasılık belirlenen eşiği aşarsa hücre şüpheli kabul edilir. Eşiği düşürmek daha fazla şüpheli hücre yakalar; fakat yanlış alarm sayısını da artırır.

## Basit bir prototip

Aşağıdaki Python örneği, gri tonlamalı görüntüde koyu çekirdekleri ayırır, küçük gürültüleri temizler ve büyük hücre adaylarını işaretler. Bu kod klinik tanı sistemi değil, temel görüntü işleme mantığını gösteren bir başlangıçtır.

```python
import cv2

image = cv2.imread("hucreler.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Gürültüyü azaltarak eşikleme sonucunu daha kararlı yapar.
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Otsu yöntemi uygun eşik değerini görüntüden otomatik hesaplar.
_, mask = cv2.threshold(
    blurred, 0, 255,
    cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
)

contours, _ = cv2.findContours(
    mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

for contour in contours:
    area = cv2.contourArea(contour)
    if area > 250:  # Örnek amaçlı şüpheli büyüklük sınırı
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imwrite("isaretli_hucreler.png", image)
```

Gerçek dokularda hücreler üst üste binebilir. Böyle durumlarda watershed algoritması veya piksel düzeyinde öğrenen U-Net gibi derin öğrenme modelleri daha başarılıdır. Yine de derin modeller daha fazla etiketli veri, güçlü donanım ve dikkatli doğrulama gerektirir.

## Başarıyı doğru ölçmek

Kanser taramasında yalnızca doğruluk değerine bakmak yanıltıcıdır. Bin hücrenin yalnızca onu anormalse, her hücreye “normal” diyen model yüzde 99 doğruluk elde eder ama hiçbir vakayı bulamaz.

| Metrik | Yanıtladığı soru |
|---|---|
| Duyarlılık | Anormal hücrelerin kaçını yakaladık? |
| Özgüllük | Normal hücrelerin kaçını doğru eledik? |
| Kesinlik | İşaretlenen hücrelerin kaçı gerçekten anormal? |
| F1 skoru | Duyarlılık ve kesinlik dengeli mi? |

Veriler hasta bazında ayrılmalıdır; aynı hastaya ait benzer görüntülerin hem eğitim hem test kümesine girmesi veri sızıntısına yol açar. Ayrıca farklı laboratuvarlardan alınan örneklerle harici doğrulama yapılmalıdır.

Sonuç olarak bilgisayar, patoloğun yerini alan sihirli bir doktor değil; yorucu tarama işini hızlandıran dikkatli bir asistandır. Güvenilir bir sistem için kaliteli etiketler, açıklanabilir sonuçlar, mahremiyet koruması ve uzman denetimi vazgeçilmezdir.

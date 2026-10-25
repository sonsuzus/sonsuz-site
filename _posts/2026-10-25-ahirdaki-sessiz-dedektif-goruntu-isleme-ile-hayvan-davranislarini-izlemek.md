---
layout: post
title: "Ahırdaki Sessiz Dedektif: Görüntü İşleme ile Hayvan Davranışlarını İzlemek"
math: true
categories: 
  - Bilgi
tags: 
  - görüntü işleme
  - yapay zeka
  - hayvancılık
  - davranış analizi
  - bilgisayarlı görü
  - python
toc: true
image: /img/ahirdaki-sessiz-dedektif-27.png
---

Bir ineğin daha az yürümesi, sürüden uzaklaşması veya normalden uzun süre yatması çoğu zaman sağlık sorununun ilk işaretidir. Ancak yüzlerce hayvanın bulunduğu bir işletmede bu küçük değişimleri insan gözüyle sürekli takip etmek oldukça zordur. Kameralar ve görüntü işleme algoritmaları, hayvanları rahatsız etmeden gözlemleyerek hareketleri ölçülebilir verilere dönüştüren sessiz birer dedektif gibi çalışır.
``

## Kameradan davranış verisine giden yol

Sistem yalnızca video kaydetmez; her kareyi analiz ederek önce hayvanları bulur, ardından aynı hayvanı kareler boyunca takip eder. Genel işlem hattı şu adımlardan oluşur:

1. Kamera görüntüsünün alınması ve zaman damgasıyla kaydedilmesi
2. Gürültü azaltma, parlaklık düzeltme ve perspektif dönüşümü
3. Hayvanların nesne tespit modeliyle belirlenmesi
4. Her hayvana geçici veya kalıcı bir kimlik atanması
5. Konum, hız, yatma süresi ve yemlik ziyareti gibi özelliklerin çıkarılması
6. Olağan dışı davranışlar için uyarı üretilmesi

Nesne tespiti, görüntüdeki her hayvanı bir sınırlayıcı kutuyla gösterir. Takip algoritması ise bu kutunun sonraki karede hangi kutuyla eşleştiğini belirler. Böylece sistem “karede üç inek var” demekle kalmaz; “17 numaralı inek son iki saatte yalnızca 40 metre yürüdü” diyebilir.

## Hareket nasıl sayıya dönüşür?

Bir hayvanın görüntü üzerindeki merkezi $(x_t, y_t)$ ve bir sonraki karedeki merkezi $(x_{t+1}, y_{t+1})$ olsun. Piksel cinsinden yer değiştirme Öklid uzaklığıyla hesaplanabilir:

$$d_t = \sqrt{(x_{t+1}-x_t)^2 + (y_{t+1}-y_t)^2}$$

Kamera kalibrasyonu sayesinde piksel-metre dönüşümü yapılırsa ortalama hız yaklaşık olarak $v=d/\Delta t$ ile bulunur. Fakat tek bir düşük hız değeri hastalık anlamına gelmez. Yaş, sıcaklık, sağım zamanı ve sürünün günlük düzeni de hesaba katılmalıdır. Bu nedenle güvenilir sistemler tek kare yerine zaman serilerini değerlendirir.

| Ölçülen özellik | Olası yorum | Dikkat edilmesi gereken |
|---|---|---|
| Uzun yatma süresi | Ağrı, yorgunluk veya topallık | Geviş getirme dönemiyle karışabilir |
| Azalan yemlik ziyareti | İştahsızlık veya hastalık | Yem dağıtım saati sonucu etkiler |
| Sık ve düzensiz hareket | Stres veya kızgınlık | Sürü içi etkileşim incelenmelidir |
| Sürüden uzak durma | Rahatsızlık veya sosyal baskı | Alanın fiziksel düzeni önemlidir |
| Tekrarlanan baş hareketi | Kaşıntı ya da stres | Sinek yoğunluğu kontrol edilmelidir |

![ahirdaki-sessiz-dedektif-27](/img/ahirdaki-sessiz-dedektif-27.svg)


## Basit bir hareket ölçümü

Aşağıdaki Python örneği, takip modelinden geldiği varsayılan merkez noktaları arasındaki toplam piksel mesafesini hesaplar:

```python
from math import hypot

def toplam_hareket(konumlar, metre_per_piksel=0.02):
    toplam_piksel = 0.0

    for onceki, simdiki in zip(konumlar, konumlar[1:]):
        dx = simdiki[0] - onceki[0]
        dy = simdiki[1] - onceki[1]
        toplam_piksel += hypot(dx, dy)

    return toplam_piksel * metre_per_piksel

iz = [(120, 80), (124, 83), (130, 85), (131, 90)]
print(f"Tahmini hareket: {toplam_hareket(iz):.2f} metre")
```

Bu kod tespiti kendisi yapmaz; YOLO gibi bir model ve ByteTrack benzeri bir takipçi tarafından üretilen koordinatları anlamlı bir mesafeye çevirir. Gerçek uygulamada kamera açısının yol açtığı perspektif hatası kalibrasyonla düzeltilmelidir.

## Sağlık uyarısı nasıl oluşturulur?

Her hayvan için geçmiş davranışlardan bir normal aralık öğrenilebilir. Günlük hareket miktarı $X$, geçmiş ortalama $\mu$ ve standart sapma $\sigma$ kullanılarak standartlaştırılır:

$$z = \frac{X-\mu}{\sigma}$$

Örneğin $z<-2$ olması, hareketin alışılmış seviyenin belirgin biçimde altına düştüğünü gösterebilir. Yine de bu sonuç doğrudan teşhis değildir; veteriner incelemesini tetikleyen bir erken uyarıdır. Yanlış alarmları azaltmak için hareket, yem tüketimi, vücut sıcaklığı ve sağım verisi birlikte değerlendirilebilir.

## Sahadaki gerçek zorluklar

Toz, gece karanlığı, hayvanların birbirini kapatması ve kirlenen kamera lensleri model başarısını düşürür. Kızılötesi kamera, uygun aydınlatma ve farklı açılardan çekim bu sorunları azaltabilir. Ayrıca verilerin güvenli saklanması, çalışan mahremiyeti ve algoritmanın farklı ırklar üzerinde doğrulanması unutulmamalıdır.

Sonuç olarak görüntü işleme, yetiştiricinin deneyiminin yerini almak yerine dikkatini doğru hayvana yönlendirir. Doğru kurulan bir sistem; hastalıkları daha erken fark etmeye, refahı artırmaya ve işletme kaynaklarını daha bilinçli kullanmaya yardımcı olur.

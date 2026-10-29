---
layout: post
title: "Otonom Traktörler Tarlada Yolunu Nasıl Buluyor?"
math: true
categories: 
  - Bilgi
tags: 
  - otonom traktör
  - gps
  - sensör füzyonu
  - robotik
  - navigasyon
  - tarım teknolojileri
toc: true
image: /img/otonom-traktorler-tarlada-91.png
---

![otonom-traktorler-tarlada-91](/img/otonom-traktorler-tarlada-91.svg)


Direksiyonda kimse olmadan dümdüz ilerleyen bir traktör, bilim kurgu filminden kaçmış gibi görünebilir. Oysa bu araç; GPS konumlarını, sensör ölçümlerini ve rota planlama algoritmalarını sürekli bir araya getiren hareketli bir bilgisayardır. Üstelik yalnızca nereye gideceğini değil, engellerden nasıl kaçacağını ve dönüşleri ne zaman yapacağını da hesaplar.

``

## Önce Tarlanın Dijital Haritası Çıkarılır

Otonom sürüş başlamadan önce tarlanın sınırları belirlenir. Operatör, harita üzerinden köşe noktalarını işaretleyebilir veya traktör sınır boyunca sürülerek GPS koordinatları kaydedilebilir. Böylece sistem, çalışılabilir alanı temsil eden bir çokgen elde eder.

Tarla daha sonra traktörün ekipman genişliğine göre paralel şeritlere ayrılır. Örneğin ilaçlama bomunun genişliği $w=12$ metre ise iki rota arasındaki teorik uzaklık yaklaşık 12 metre seçilir. Küçük bir örtüşme gerekiyorsa şerit aralığı şöyle hesaplanabilir:

$$d = w(1-r)$$

Burada $r$, örtüşme oranıdır. Yüzde 5 örtüşme için $d=12(1-0.05)=11.4$ metre olur. Bu yaklaşım, sürülmemiş alan bırakmadan gereksiz tekrarları azaltır.

## GPS Tek Başına Yeterli mi?

Standart GPS ölçümleri birkaç metre hata yapabilir. Hassas ekim gibi işlemlerde bu sapma kabul edilemez. Bu nedenle çoğu tarım robotu, sabit bir referans istasyonundan düzeltme verisi alan RTK-GPS kullanır. RTK ile hata santimetre düzeyine indirilebilir.

Ancak ağaç, tepe veya bağlantı sorunu GPS sinyalini bozabilir. Traktör bu noktada IMU, tekerlek enkoderi, kamera ve LiDAR gibi sensörlerden yardım alır.

| Sensör | Sağladığı bilgi | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| RTK-GPS | Küresel konum | Santimetre hassasiyeti | Sinyal kesilebilir |
| IMU | İvme ve yönelim | Çok hızlı ölçüm | Zamanla sürüklenir |
| Enkoder | Tekerlek dönüşü | Basit ve ekonomiktir | Patinajdan etkilenir |
| LiDAR | Çevre mesafeleri | Engelleri hassas algılar | Maliyetli olabilir |
| Kamera | Görsel çevre | Bitki ve insan tanıyabilir | Işıktan etkilenir |

## Sensör Füzyonu: Ölçümlerin Takım Oyunu

Sensör verileri genellikle Kalman filtresi veya genişletilmiş Kalman filtresiyle birleştirilir. Temel fikir, önce aracın yeni konumunu hareket modelinden tahmin etmek, ardından sensör ölçümüyle bu tahmini düzeltmektir.

$$\hat{x}_k = A\hat{x}_{k-1} + Bu_k$$

Buradaki $\hat{x}_k$ tahmini durum, $A$ hareket modeli, $u_k$ ise direksiyon ve hız gibi kontrol girdileridir. GPS kaybolduğunda IMU kısa süreli konum tahmini yapar; GPS geri geldiğinde biriken hata düzeltilir. Kısacası sensörler birbirlerinin açığını kapatır.

## Rota Planlama ve Takip

Tarlayı en az dönüşle kaplamak için çoğunlukla ileri-geri tarama, yani boustrophedon deseni kullanılır. İsmi karmaşık olsa da mantığı çim biçmeye benzer: bir şeridi tamamla, U dönüşü yap ve yan şeritten geri gel.

A* veya Dijkstra algoritması engellerin bulunduğu karmaşık alanlarda güvenli yol oluşturabilir. Üretilen rotayı izlemek için Pure Pursuit gibi bir takip algoritması kullanılabilir. Bu yöntem, rotanın üzerinde traktörün biraz ilerisinde bir hedef noktası seçer ve direksiyon açısını o noktaya göre hesaplar.

Aşağıdaki sade Python örneği, traktörün hedef noktaya yönelmesi için gereken açı hatasını bulur:

```python
import math

def yon_hatasi(x, y, heading, hedef_x, hedef_y):
    hedef_acisi = math.atan2(hedef_y - y, hedef_x - x)
    hata = hedef_acisi - heading
    return math.atan2(math.sin(hata), math.cos(hata))

hata = yon_hatasi(10, 5, 0.2, 18, 9)
print(f'Direksiyon için açı hatası: {hata:.3f} radyan')
```

Fonksiyon, açıyı $[-\pi,\pi]$ aralığına sıkıştırarak traktörün gereksiz yere uzun yönden dönmesini önler. Gerçek sistemde bu hata, PID denetleyiciye aktarılıp direksiyon komutuna çevrilir.

## Güvenlik Her Şeyden Önce Gelir

Otonom traktör yalnızca rotayı takip etmemeli; insan, hayvan, kaya veya başka bir araç algıladığında yavaşlamalı ya da durmalıdır. Acil durdurma düğmesi, uzaktan kontrol, hız sınırı ve sensör tutarlılık denetimi bu yüzden zorunludur. Başarılı navigasyon; hassas konumlama, akıllı rota planlama ve güvenli kontrol katmanlarının birlikte çalışmasıyla ortaya çıkar. Sonuçta traktörün amacı macera yaşamak değil, tarlayı verimli ve güvenilir biçimde işlemektir.

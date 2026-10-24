---
layout: post
title: "Cerrahî Navigasyon Sistemleri: Vücudun İçinde GPS Gibi Yol Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - cerrahi navigasyon
  - medikal teknoloji
  - bilgisayarlı görü
  - görüntü işleme
  - robotik
  - yapay zekâ
toc: true
image: /img/cerrahi-navigasyon-sistemleri-95.png
---

Bir cerrahın milimetrelerle ölçülen bir hedefe ulaşması gerektiğini düşünün: Beyindeki küçük bir tümör, omurgaya yerleştirilecek vida veya eklem içindeki hassas bir bölge… Cerrahî navigasyon sistemleri; tıbbi görüntüleri, konum sensörlerini ve matematiksel dönüşümleri birleştirerek cerraha aletinin vücut içindeki yerini gerçek zamanlı gösterir. Kısacası sistem, otomobillerdeki GPS’in ameliyathaneye uyarlanmış, çok daha hassas kuzenidir.

``

## Temel fikir: Harita, konum ve hedef

Navigasyon için üç şey gerekir: Önceden hazırlanmış bir **harita**, harita üzerinde belirlenmiş bir **hedef** ve hareket eden nesnenin güncel **konumu**. Cerrahî sistemlerde harita genellikle BT, MR veya ultrason görüntülerinden oluşturulur. Hareket eden nesne ise cerrahın kullandığı prob, matkap ya da iğnedir.

| Navigasyon kavramı | Otomobilde | Cerrahî sistemde |
|---|---|---|
| Harita | Yol ağı | BT, MR veya 3B anatomi modeli |
| Konum ölçümü | GPS uyduları | Optik ya da elektromanyetik sensörler |
| Hedef | Adres | Tümör, kemik veya giriş noktası |
| Rota | Yol tarifi | Güvenli cerrahî yaklaşım |
| Hata riski | Yanlış sokağa girmek | Sağlıklı dokuya yaklaşmak |

![cerrahî-navigasyon-sistemleri-95](/img/cerrahi-navigasyon-sistemleri-95.svg)


Buradaki önemli fark hassasiyettir. Otomobil navigasyonunda birkaç metrelik sapma kabul edilebilirken beyin veya omurga cerrahisinde birkaç milimetre bile kritik olabilir.

## Kayıt: İki dünyayı üst üste getirmek

Bilgisayardaki görüntü koordinatları ile hastanın ameliyat masasındaki fiziksel koordinatları başlangıçta aynı değildir. **Kayıt** veya *registration* adı verilen işlem, bu iki koordinat sistemini eşleştirir. Cerrah hastanın üzerinde bilinen bazı anatomik noktaları işaretleyebilir ya da sistem yüzeyi tarayabilir.

Bir noktanın görüntü uzayından hasta uzayına dönüşümü basitleştirilmiş biçimde şöyle yazılır:

$$
\mathbf{p}_{hasta} = \mathbf{R}\mathbf{p}_{görüntü} + \mathbf{t}
$$

Burada $\mathbf{R}$ dönüşü temsil eden döndürme matrisi, $\mathbf{t}$ öteleme vektörü, $\mathbf{p}$ ise üç boyutlu noktadır. Sistem, eşleştirilen referans noktaları arasındaki toplam hatayı en aza indirecek $\mathbf{R}$ ve $\mathbf{t}$ değerlerini hesaplar.

## Cerrahî alet nasıl takip edilir?

Optik sistemlerde ameliyathanedeki kızılötesi kameralar, aletlere ve hastaya bağlanan yansıtıcı işaretçileri izler. Elektromanyetik sistemlerde ise küçük sensörler oluşturulan manyetik alan içindeki konumlarını bildirir.

| Yöntem | Avantaj | Sınırlama |
|---|---|---|
| Optik takip | Yüksek doğruluk ve hızlı ölçüm | Kamera ile işaretçi arasında görüş gerekir |
| Elektromanyetik takip | Görüş hattına ihtiyaç duymaz | Metal araçlar alanı bozabilir |
| Robotik kodlayıcılar | Eklem konumlarını doğrudan ölçer | Robot mekanizmasına bağımlıdır |

Ölçülen alet ucu, kayıt dönüşümü kullanılarak görüntü üzerinde çizilir. Aşağıdaki Python örneği, homojen koordinatlarla basit bir dönüşümü gösterir:

```python
import numpy as np

# Alet ucunun takip sistemi tarafından ölçülen konumu
alet_ucu = np.array([12.0, 35.0, 80.0, 1.0])

# Döndürme ve ötelemeyi içeren 4x4 kayıt matrisi
kayit_matrisi = np.array([
    [1, 0, 0,  2],
    [0, 1, 0, -1],
    [0, 0, 1,  3],
    [0, 0, 0,  1]
])

goruntu_konumu = kayit_matrisi @ alet_ucu
print(goruntu_konumu[:3])
```

Gerçek sistemlerde matrisler sürekli güncellenir; filtreleme, kamera kalibrasyonu ve gecikme telafisi gibi ek işlemler uygulanır.

## Hata nereden gelir?

Navigasyon ekranı mutlak gerçek değildir. Görüntüleme çözünürlüğü, yanlış işaretlenen referans noktaları, sensör gürültüsü ve hastanın hareketi hata oluşturabilir. Beyin cerrahisinde dokunun operasyon sırasında yer değiştirmesi, **brain shift** adı verilen önemli bir problemdir. Başlangıçta çekilen MR artık güncel anatomiyi tam yansıtmayabilir. Ameliyat içi ultrason veya yeni görüntüleme yöntemleri haritayı güncellemek için kullanılır.

Toplam hedef hatası kabaca bağımsız hata bileşenleriyle modellenebilir:

$$
E_{toplam} \approx \sqrt{E_{kayıt}^2 + E_{takip}^2 + E_{kalibrasyon}^2}
$$

Bu nedenle sistemler ameliyat öncesinde doğrulanır ve cerrah, ekrandaki bilgiyi anatomik gözlemleriyle birlikte değerlendirir.

Cerrahî navigasyon cerrahın yerine karar veren bir otomatik pilot değildir; ona konum farkındalığı sağlayan gelişmiş bir yardımcıdır. Artırılmış gerçeklik, yapay zekâ ve ameliyat sırasında güncellenen 3B modeller geliştikçe bu dijital pusula daha da hassaslaşacaktır. Ancak son karar ve sorumluluk daima eğitimli sağlık ekibinde kalır.

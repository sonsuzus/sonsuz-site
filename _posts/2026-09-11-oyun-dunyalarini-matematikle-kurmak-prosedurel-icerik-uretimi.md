---
layout: post
title: "Oyun Dünyalarını Matematikle Kurmak: Prosedürel İçerik Üretimi"
math: true
categories: 
  - Bilgi
tags: 
  - pcg
  - oyun geliştirme
  - prosedürel üretim
toc: true
---

Bir oyun dünyasındaki her dağı, mağarayı ve ağacı elle yerleştirmek mümkün; fakat harita milyonlarca hücreden oluşuyorsa tasarım ekibi muhtemelen emekliliğini beklerken hâlâ çalı çiziyor olacaktır. Prosedürel İçerik Üretimi, yani PCG, bu işi matematiksel kurallar, tohumlar ve gürültü fonksiyonlarıyla işlemciye devreder. Böylece büyük dünyalar gerektiği anda üretilebilir, tekrar oluşturulabilir ve oyuncuya keşfedilecek benzersiz alanlar sunabilir.

``

## PCG rastgelelikten fazlasıdır

PCG çoğu zaman “rastgele harita üretmek” şeklinde açıklansa da tamamen kontrolsüz rastgelelik genellikle kötü sonuç verir. Rastgele yerleştirilen bir nehir dağın tepesinde bitebilir veya oyuncu çıkışı olmayan bir mağarada doğabilir. Başarılı bir sistem, rastgeleliği tasarım kurallarıyla sınırlar.

Üretimin başlangıç noktası **tohum**, yani `seed` değeridir. Sözde rastgele sayı üreteci aynı tohumla çalıştırıldığında aynı sayı dizisini verir:

$$D = G(s, x, y, p)$$

Burada $s$ tohum, $(x,y)$ dünya koordinatı, $p$ üretim parametreleri ve $D$ ortaya çıkan içeriktir. Bu deterministik yapı sayesinde geliştirici, oyuncunun bulduğu ilginç bir dünyayı yalnızca tohumu saklayarak yeniden oluşturabilir.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Elle tasarım | Güçlü sanatsal kontrol | Yavaş ve maliyetli |
| Saf rastgelelik | Çok hızlı çeşitlilik | Tutarsız sonuçlar |
| Kurallı PCG | Ölçeklenebilir ve tekrar üretilebilir | Ayarlaması karmaşıktır |

## Gürültü fonksiyonları ne yapar?

Her koordinata bağımsız rastgele bir yükseklik verilirse arazi televizyon paraziti gibi görünür. Perlin, Simplex veya OpenSimplex gürültüsü ise yakın koordinatlarda benzer değerler üreterek yumuşak geçişler sağlar. Basit bir yükseklik modeli şöyle kurulabilir:

$$h(x,y) = A \cdot N(fx,fy)$$

$N$ gürültü fonksiyonu, $A$ yükseklik genliği, $f$ ise frekanstır. Düşük frekans geniş tepeler oluştururken yüksek frekans küçük kayalık ayrıntılar üretir. Birden fazla katmanın toplanmasına **oktavlama** denir:

$$h(x,y)=\sum_{i=0}^{k-1} A r^i N(2^i f x,2^i f y)$$

Bu yöntem, büyük kıtalarla küçük arazi pürüzlerini aynı yüzeyde birleştirir.

## Küçük bir yükseklik haritası

Aşağıdaki Python örneği, aynı tohum kullanıldığında aynı arazi matrisini üretir. Gerçek projelerde rastgele değerlerin yerine sürekli bir gürültü kütüphanesi tercih edilmelidir.

```python
import random

SIZE = 8
SEED = 2026
random.seed(SEED)

height_map = []
for y in range(SIZE):
    row = []
    for x in range(SIZE):
        base = random.random()
        height = round(base * 100)
        row.append(height)
    height_map.append(row)

for row in height_map:
    print(row)
```

Kod, `random.seed` ile üretimi deterministik hâle getirir ve değerleri 0–100 arasındaki yüksekliklere dönüştürür. Ancak koordinatların sırayla üretilmesine bağımlıdır. Parça tabanlı açık dünyalarda bunun yerine `hash(seed, chunk_x, chunk_y)` benzeri bir yaklaşım kullanılır. Böylece oyuncunun ziyaret ettiği her **chunk** bağımsız biçimde hesaplanabilir.

## Biyomlar ve tasarım kuralları

Tek bir gürültü haritası yalnızca yükseklik sağlayabilir. İnandırıcı bir dünya için sıcaklık ve nem gibi ek haritalar üretilebilir. Örneğin yüksek sıcaklık ve düşük nem çölü; düşük sıcaklık ise kar biyomunu seçebilir.

| Sıcaklık | Nem | Biyom |
|---|---|---|
| Yüksek | Düşük | Çöl |
| Yüksek | Yüksek | Yağmur ormanı |
| Orta | Orta | Çayır |
| Düşük | Fark etmez | Tundra |

Son aşamada oynanabilirlik kuralları devreye girer: Başlangıç bölgesi güvenli olmalı, yollar hedeflere ulaşmalı ve kaynaklar erişilebilir mesafelerde bulunmalıdır. Bu kontroller; kısıt çözümleme, hücresel otomatlar, grafik algoritmaları veya Wave Function Collapse ile uygulanabilir.

PCG, tasarımcıyı ortadan kaldırmaz; ona fırça yerine dünya üreten bir makine verir. Matematik çeşitliliği oluştururken tasarımcı kuralları, atmosferi ve oyuncu deneyimini belirler. En iyi prosedürel dünya yalnızca büyük olan değil, rastlantılarının bile bilinçli tasarlanmış gibi hissettirdiği dünyadır.

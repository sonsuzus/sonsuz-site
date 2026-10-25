---
layout: post
title: "Sıkışma Algoritmalarıyla Doku Optimizasyonu: VRAM’i Kurtarma Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - doku sıkıştırma
  - oyun geliştirme
  - grafik programlama
  - vram
  - gpu
  - optimizasyon
toc: true
image: /img/sikisma-algoritmalariyla-doku-54.png
---

Modern oyunlardaki kayalar, karakter kostümleri ve çamurlu yollar milyonlarca pikselden oluşur. Ancak bu görsel şölen bedava değildir: Sıkıştırılmamış yüksek çözünürlüklü dokular ekran kartı belleğini hızla tüketir. Doku sıkıştırma algoritmaları, görüntüyü kabul edilebilir kalite kaybıyla küçülterek hem VRAM kullanımını hem de bellek bant genişliği ihtiyacını azaltır.


![sikisma-algoritmalariyla-doku-54](/img/sikisma-algoritmalariyla-doku-54.svg)

``

## Bir doku bellekte ne kadar yer kaplar?

RGBA biçimindeki bir piksel; kırmızı, yeşil, mavi ve alfa kanalları için genellikle dörder adet 8 bitlik değer taşır. Böylece piksel başına toplam maliyet 32 bit, yani 4 bayt olur. Sıkıştırılmamış bir dokunun yaklaşık bellek maliyeti şu formülle hesaplanabilir:

$$
B = W \times H \times C
$$

Burada $W$ genişliği, $H$ yüksekliği, $C$ ise piksel başına bayt miktarını temsil eder. Örneğin 4096 × 4096 boyutunda bir RGBA doku:

$$
4096 \times 4096 \times 4 = 67.108.864\ \text{bayt} \approx 64\ \text{MiB}
$$

Tek bir kaplama için 64 MiB kulağa yönetilebilir gelebilir. Fakat renk, normal, pürüzlülük, metalik ve yükseklik haritaları eklendiğinde yalnızca bir materyal yüzlerce MiB isteyebilir. Ayrıca mipmap zinciri bellek maliyetini yaklaşık üçte bir oranında artırır:

$$
B_{mipmap} \approx B \times \frac{4}{3}
$$

## Blok tabanlı sıkıştırma nasıl çalışır?

GPU dostu yöntemler JPEG veya PNG gibi tüm görüntüyü değişken uzunlukta kodlamak yerine dokuyu küçük bloklara ayırır. BC ailesinde çoğunlukla 4 × 4 piksellik bloklar kullanılır. Algoritma, bloktaki her pikseli ayrı ayrı saklamak yerine birkaç referans renk ve bu renklere ulaşan indeksler kaydeder.

Bu sabit boyutlu yapı önemlidir. GPU, görüntünün tamamını açmadan ihtiyaç duyduğu bloğun adresini hesaplayabilir ve örnekleme sırasında donanım üzerinde çözebilir. Böylece doku, VRAM’de sıkıştırılmış durumda kalır.

| Biçim | Yaklaşık maliyet | Uygun kullanım | Önemli özellik |
|---|---:|---|---|
| BC1 | 4 bit/piksel | Alfa gerektirmeyen renk dokuları | Çok düşük bellek maliyeti |
| BC3 | 8 bit/piksel | Alfa kanallı dokular | Ayrı alfa kodlaması |
| BC5 | 8 bit/piksel | Normal haritaları | İki kanalda yüksek kalite |
| BC7 | 8 bit/piksel | Yüksek kaliteli RGBA | Daha iyi renk doğruluğu |
| ASTC | Değişken | Mobil ve modern platformlar | Ayarlanabilir blok boyutu |
| ETC2 | 4–8 bit/piksel | Mobil cihazlar | Geniş donanım desteği |

Örneğin BC7 kullanan 4096 × 4096 bir doku, piksel başına 8 bit harcar. Ana seviye yaklaşık 16 MiB tutar; yani sıkıştırılmamış sürümün dörtte biri kadar yer kaplar.

## Kalite neden bozulur?

Her blok sınırlı sayıda renk ile temsil edildiğinden ince renk geçişlerinde bantlaşma, keskin sınırlarda lekelenme ve normal haritalarında yön hataları oluşabilir. Bu nedenle “en güçlü sıkıştırıcıyı her yerde kullan” yaklaşımı doğru değildir. Veri türüne uygun biçim seçilmelidir.

| Doku türü | Önerilen yaklaşım | Kaçınılması gereken hata |
|---|---|---|
| Albedo | BC7 veya ASTC | Gereksiz alfa kanalı tutmak |
| Normal | BC5 | Normal verisini sıradan renk gibi sıkıştırmak |
| Maske | Kanal paketleme | Her maskeyi ayrı dosyada saklamak |
| Arayüz | Yüksek kaliteli biçim | Yazıları agresif sıkıştırmak |

Kanal paketleme de etkili bir numaradır. Pürüzlülük, metalik ve ortam tıkanıklığı gibi gri tonlu üç harita, tek RGB dokusunun kanallarına yerleştirilebilir. Böylece üç ayrı örnekleme ve dosya yerine tek bir kaynak kullanılabilir.

## Basit bir bellek hesaplayıcısı

Aşağıdaki Python kodu, blok sıkıştırmalı bir dokunun mipmap dâhil yaklaşık maliyetini hesaplar:

```python
def texture_size(width, height, bits_per_pixel, mipmaps=True):
    base_bytes = width * height * bits_per_pixel / 8
    total_bytes = base_bytes * (4 / 3 if mipmaps else 1)
    return total_bytes / (1024 ** 2)

print(f"BC7 maliyeti: {texture_size(4096, 4096, 8):.2f} MiB")
print(f"BC1 maliyeti: {texture_size(4096, 4096, 4):.2f} MiB")
```

Bu hesap yaklaşık sonuç verir; küçük mip seviyeleri ve motor hizalamaları gerçek değeri biraz değiştirebilir.

## Dengeli optimizasyon stratejisi

İyi optimizasyon yalnızca dosyayı küçültmek değildir. Hedef platformun desteklediği biçimler belirlenmeli, kamera mesafesine uygun çözünürlük seçilmeli ve dokular gerçek sahnelerde karşılaştırılmalıdır. Oyuncunun iki metre uzaktan göremeyeceği ayrıntı için 8K doku kullanmak, dijital bir halıya mikroskopla desen çizmek gibidir.

Sonuç olarak doğru sıkıştırma; daha kısa yükleme süreleri, daha az VRAM tüketimi ve daha kararlı kare hızları sağlar. En iyi biçim ise en küçük olan değil, görsel kalite ile donanım maliyeti arasında oyunun ihtiyaçlarına uygun dengeyi kurandır.

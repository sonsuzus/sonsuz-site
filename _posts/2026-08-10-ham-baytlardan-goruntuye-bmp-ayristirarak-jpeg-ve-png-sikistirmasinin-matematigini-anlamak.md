---
layout: post
title: "Ham Baytlardan Görüntüye: BMP Ayrıştırarak JPEG ve PNG Sıkıştırmasının Matematiğini Anlamak"
math: true
categories: 
  - Proje
tags: 
  - görüntü işleme
  - bmp
  - png
  - jpeg
  - python
image: /img/ham-baytlardan-goruntuye-46.png
---

Bir görüntü dosyası, ekranda gördüğümüz renkli karelerden çok daha fazlasıdır: başlıklar, piksel dizileri, satır hizalama kuralları ve bazen karmaşık sıkıştırma akışları içerir. JPEG ya da PNG kod çözücüsünü çağırmadan bir dosyayı ham baytlarına ayırıp yeniden kurmak, bu katmanları görünür hâle getirir. Başlangıç için BMP idealdir; çoğu BMP dosyası pikselleri neredeyse doğrudan saklar. Ardından aynı bakış açısını PNG filtreleri ve JPEG dönüşümlerine taşıyabiliriz.

``

## Neden BMP ile başlamak gerekir?

24 bitlik sıkıştırmasız BMP, teoriyi pratiğe bağlayan dürüst bir formattır. Dosya başlığı, görüntü bilgisi ve piksel verisi ayrı bölümlerdedir. Her piksel üç bayttır; fakat yaygın RGB beklentisinin aksine sıralama çoğunlukla **BGR** şeklindedir. Ayrıca satırlar dört baytın katına tamamlanır. Bu küçük ayrıntı, yanlış hesaplandığında görüntünün neden “televizyon paraziti”ne döndüğünü açıklar.

| Kavram | BMP | PNG | JPEG |
|---|---|---|---|
| Temel temsil | Ham veya az sıkıştırılmış piksel | Filtrelenmiş, DEFLATE akışı | Dönüştürülmüş frekans katsayıları |
| Kayıp durumu | Genellikle kayıpsız | Kayıpsız | Kayıplı |
| Şeffaflık | Sınırlı / biçime bağlı | Doğal alfa desteği | Yerleşik alfa yok |
| Öğrenme zorluğu | Düşük | Orta | Yüksek |

![ham-baytlardan-goruntuye-46](/img/ham-baytlardan-goruntuye-46.svg)


BMP satır genişliği $w$ ve bayt/piksel değeri $b$ ise satırdaki gerçek veri $w \cdot b$ olur. Dört bayt hizalama sonrası saklanan satır uzunluğu ise şöyledir:

$$stride = 4 \cdot \left\lceil \frac{w \cdot b}{4} \right\rceil$$

Dolgu miktarı $stride - w \cdot b$ kadardır. Bu baytlar piksel değildir; yeniden dosya üretirken onları hesaba katmak zorunludur.

## Baytları elle okumak

Aşağıdaki Python örneği, 24 bit BMP’nin temel alanlarını çözer. `struct`, makinenin bayt düzeninden bağımsız olarak little-endian tamsayılar okumamızı sağlar. Bu bir görüntü kütüphanesi değildir; dosyanın sözleşmesini kendimiz yorumlarız.

```python
import struct

with open("ornek.bmp", "rb") as f:
    raw = f.read()

if raw[:2] != b"BM":
    raise ValueError("Bu örnek yalnızca BMP bekliyor")

offset = struct.unpack_from("<I", raw, 10)[0]
width, height = struct.unpack_from("<ii", raw, 18)
bpp = struct.unpack_from("<H", raw, 28)[0]

if bpp != 24:
    raise ValueError("24 bit BMP kullanın")

row_bytes = width * 3
stride = (row_bytes + 3) & ~3
pixels = []

for y in range(abs(height)):
    start = offset + y * stride
    row = raw[start:start + row_bytes]
    pixels.append([tuple(row[x:x+3]) for x in range(0, row_bytes, 3)])

print(width, height, pixels[0][0])  # İlk piksel: (B, G, R)
```

Negatif yükseklik “üstten alta” satır düzenini belirtirken, pozitif yükseklik klasik BMP’de verinin alttan başlamasına yol açar. Yeniden oluştururken başlıkları koruyup yalnızca piksel alanını değiştirebilir veya yeni bir başlık yazabilirsiniz. En güvenli deney: kırmızı ve mavi kanalları değiştirin, satır dolgularını aynen bırakın, sonra `raw[:offset] + yeni_piksel_verisi` ile dosyayı kaydedin.

## PNG ve JPEG’de matematik nerede saklanır?

PNG ham RGB saklamaz. Her satıra bir filtre uygulanır; örneğin soldaki pikseli tahmin eden Sub filtresinin fikri $R_i = X_i - X_{i-bpp} \pmod{256}$ biçimindedir. Komşu pikseller benzer olduğundan kalan değerler küçülür; DEFLATE bu tekrarları daha iyi kodlar. PNG’yi kütüphanesiz çözmek için önce imza, `IHDR` ve `IDAT` parçalarını ayrıştırmak, sonra zlib/DEFLATE ve filtre tersleme aşamalarını yazmak gerekir.

JPEG ise 8×8 blokları frekans uzayına taşır. DCT’nin özeti $F(u,v)=\sum_x\sum_y f(x,y)\cos(\cdots)\cos(\cdots)$ şeklindedir. Katsayılar kuantizasyon tablosuna bölünüp yuvarlanır; kayıp tam burada doğar. Sıfıra yaklaşan yüksek frekanslar run-length ve Huffman kodlamasıyla ucuzlar.

Bu nedenle BMP projesi yalnızca dosya biçimi egzersizi değildir: piksel düzenini, tahmini, dönüşümü ve entropi kodlamasını ayırmayı öğretir. Önce bir BMP’yi bayt bayt bozup onarın; sonra aynı disiplinle PNG parça yapısını ve JPEG işaretçilerini inceleyin. Görüntü sıkıştırmasının sihri, aslında iyi tanımlanmış bayt kuralları ve akıllı matematikten ibarettir.

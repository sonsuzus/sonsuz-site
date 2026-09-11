---
layout: post
title: "Bit Rot’a Karşı Dijital Arşivleme: Bitler Sessizce Değiştiğinde"
math: true
categories: 
  - Bilgi
tags: 
  - dijital arşivleme
  - bit rot
  - hata düzeltme kodları
toc: true
---

Bir fotoğrafı diske kaydettiğimizde onun yıllarca aynı kalacağını düşünürüz. Ne var ki fiziksel depolama kusursuz değildir: manyetik alanlar zayıflayabilir, flash hücreleri yıpranabilir ve yüksek enerjili parçacıklar geçici bit değişimlerine yol açabilir. Sonuçta bir zamanlar `0` olan bit `1` olabilir. **Bit rot** adı verilen bu sessiz bozulma, özellikle uzun süre saklanan ve nadiren okunan arşivlerde sinsice ilerler.

``

## Bit gerçekten nasıl “çürür”?

Bit rot tek bir arıza türü değil, verinin zaman içinde değişmesini anlatan genel bir kavramdır. Manyetik disklerde kaplamanın yaşlanması veya okuma kafası sorunları; SSD’lerde hücrelerin elektrik yükü kaybetmesi ve programlama-silme döngüleri başlıca nedenlerdir. Kozmik ışınların oluşturduğu parçacıklar ise daha çok RAM gibi çalışan elektronik devrelerde **soft error** meydana getirir. Ancak önbellek, denetleyici veya aktarım sırasında oluşan böyle bir hata, diske yanlış veri yazılmasına da neden olabilir.

Depolama ortamlarının davranışları aynı değildir:

| Ortam | Başlıca risk | Koruma yaklaşımı |
|---|---|---|
| HDD | Manyetik zayıflama, mekanik aşınma | ECC, SMART, düzenli tarama |
| SSD | Hücre yorgunluğu, yük kaybı | LDPC/BCH kodları, wear leveling |
| RAM | Parçacık kaynaklı bit flip | ECC RAM, bellek scrubbing |
| Optik disk | Katman bozulması, çizilme | Çoklu kopya, doğrulama |
| Manyetik teyp | Ortam yaşlanması, gerilme | Periyodik yeniden yazma |

## Hata düzeltme kodlarının mantığı

Hata düzeltme kodları, asıl veriye fazladan kontrol bitleri ekler. Böylece sistem yalnızca “bir şey değişmiş” demez; belirli sınırlar içinde bozulan bitin yerini bulup onu otomatik olarak düzeltebilir.

Basit bir Hamming kodunda gerekli kontrol biti sayısı $r$, veri biti sayısı $m$ olmak üzere şu koşulu sağlamalıdır:

$$2^r \geq m + r + 1$$

Örneğin dört veri biti için üç kontrol biti yeterlidir. Kod sözcükleri arasındaki en küçük farklı bit sayısına **Hamming mesafesi** denir. En küçük mesafe $d$ ise algılanabilecek hata sayısı en fazla $d-1$, düzeltilebilecek hata sayısı ise:

$$t = \left\lfloor \frac{d-1}{2} \right\rfloor$$

olur. Modern SSD’lerde daha güçlü BCH ve LDPC kodları kullanılır. Disk denetleyicisi veriyi okurken kontrol bilgisini inceler, hata sınır içindeyse doğru bitleri yeniden oluşturur. Kullanıcı çoğu zaman bu küçük kurtarma operasyonunu hiç fark etmez.

## Sağlam arşiv için checksum ve scrubbing

ECC fiziksel blokları korurken SHA-256 gibi özetler dosyanın tamamının beklenen içerikle aynı olup olmadığını doğrular. Dosyaları düzenli aralıklarla okuyup özetlerini karşılaştırma işlemine **data scrubbing** denir. Aşağıdaki Python kodu basit bir doğrulama aracı oluşturur:

```python
from pathlib import Path
import hashlib

def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as file:
        for block in iter(lambda: file.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()

archive = Path('arsiv.zip')
expected = Path('arsiv.zip.sha256').read_text().strip()
current = sha256(archive)

if current == expected:
    print('Arşiv sağlam.')
else:
    print('Bozulma algılandı; sağlam kopyadan geri yükleyin!')
```

Kod dosyayı parça parça okuyarak belleği gereksiz yere doldurmaz. Ancak checksum hatayı yalnızca **algılar**; onarabilmek için başka bir kopya, eşlik verisi veya hata düzeltmeli dosya sistemi gerekir.

## RAID, yedekleme değildir

ZFS ve Btrfs gibi dosya sistemleri blok checksum’ları tutabilir. Aynalanmış veya eşlikli depolamada bozuk blok bulunduğunda sağlam kopya okunup hasarlı kısım yeniden yazılır. Buna rağmen RAID; yanlışlıkla silme, fidye yazılımı, yangın veya denetleyici hatasına karşı tek başına yeterli değildir.

Uzun ömürlü arşiv için **3-2-1 kuralı** iyi bir başlangıçtır: verinin üç kopyasını, iki farklı ortamda ve bir kopyası uzak konumda saklamak. Buna düzenli checksum kontrolü, scrubbing, disk sağlık takibi ve eski ortamdan yenisine planlı veri göçü eklenmelidir. Dijital sonsuzluk, “kaydet ve unut” değil; “kaydet, doğrula, çoğalt ve yenile” disiplinidir.

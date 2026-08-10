---
layout: post
title: "Genetik Algoritma ile Yürümeyi Öğrenen Robot Motoru"
math: true
categories: 
  - Proje
tags: 
  - genetik algoritma
  - robotik
  - python
---

Bir robotun yürümeyi öğrenmesi, ona tek tek “sol bacağını kaldır, şimdi sağa bas” komutları vermekten çok daha eğlenceli bir problemdir. Bunun yerine robotun hareket kontrolcülerini bir DNA dizisi gibi düşünebilir, yüzlerce farklı davranışı sanal ortamda yarıştırabiliriz. Başarılı hareket edenler hayatta kalır, başarılı özellikler çaprazlanır ve küçük rastlantısal mutasyonlar yeni çözümler üretir. İşte genetik algoritma motorunun temel fikri budur.

``

Genetik algoritma (GA), kesin çözüm üretmekten ziyade geniş ve karmaşık arama uzaylarında iyi çözümler bulmayı hedefleyen evrimsel bir optimizasyon yöntemidir. Robot yürüyüşünde arama uzayı; eklem açıları, hareket frekansı, faz kaymaları, kuvvet limitleri ve denge düzeltmelerinden oluşur. Bir bireyin kromozomu örneğin altı eklem için bu parametreleri taşıyan bir vektördür: $x = [a_1, f_1, p_1, \dots, a_n, f_n, p_n]$.

Robotun her eklemine doğrudan açı göndermek yerine periyodik bir kontrol sinyali kullanmak işleri sadeleştirir:

$$\theta_i(t) = a_i \sin(2\pi f_i t + p_i) + o_i$$

Burada $a_i$ genlik, $f_i$ frekans, $p_i$ faz ve $o_i$ eklem ofsetidir. Faz farkları özellikle kritiktir: İki bacağın aynı anda ileri savrulması komik ama çoğunlukla dengesiz bir sıçrama doğurur. Yaklaşık $\pi$ radyanlık fark ise dönüşümlü adım üretmeye yakındır.

Bir bireyin ne kadar iyi olduğunu uygunluk fonksiyonu belirler. Sadece alınan mesafeyi ödüllendirmek robotun yerde yuvarlanarak “hile yapmasına” neden olabilir. Bu nedenle ileri mesafe, gövde yüksekliği, enerji tüketimi ve devrilme cezalarını birlikte değerlendirmek gerekir:

$$F = 10d_x + 2h - 0.05E - 20C$$

| Terim | Anlamı | Neden gereklidir? |
|---|---|---|
| $d_x$ | İleri yönlü mesafe | Robotun hedefe ilerlemesini ödüllendirir. |
| $h$ | Ortalama gövde yüksekliği | Sürünme ve yuvarlanmayı azaltır. |
| $E$ | Harcanan tork/enerji | Gereksiz sert hareketleri cezalandırır. |
| $C$ | Düşme veya temas cezası | Dengesiz adayları eler. |

Motorun evrim döngüsü basittir: Rastgele popülasyon oluştur, simülasyonda değerlendir, en iyileri seç, çaprazla, mutasyona uğrat ve tekrar et. Elitizm uygulanırsa en iyi birkaç birey sonraki nesle değişmeden taşınır; böylece iyi bulunan yürüyüş yanlışlıkla kaybolmaz.

```python
import random

GEN_SAYISI = 12  # 4 eklem x [genlik, frekans, faz]

def birey_olustur():
    return [random.uniform(-1.0, 1.0) for _ in range(GEN_SAYISI)]

def caprazla(anne, baba):
    nokta = random.randint(1, GEN_SAYISI - 1)
    return anne[:nokta] + baba[nokta:]

def mutasyon(genler, oran=0.12, siddet=0.18):
    yeni = genler[:]
    for i in range(len(yeni)):
        if random.random() < oran:
            yeni[i] += random.gauss(0, siddet)
            yeni[i] = max(-1.0, min(1.0, yeni[i]))
    return yeni

def turnuva_sec(populasyon, skorlar, k=3):
    adaylar = random.sample(list(zip(populasyon, skorlar)), k)
    return max(adaylar, key=lambda x: x[1])[0]
```

Bu kod, genleri üretir; iki ebeveynden tek noktalı çaprazlama ile çocuk çıkarır; ardından Gauss dağılımlı mutasyonla küçük keşifler yapar. `turnuva_sec` ise tüm popülasyonu seçmek yerine rastgele küçük bir gruptaki en başarılı bireyi ebeveyn yapar. Böylece güçlü adaylar avantaj kazanırken çeşitlilik tamamen yok olmaz.

| Yaklaşım | Güçlü yanı | Riski |
|---|---|---|
| Yüksek mutasyon | Yeni yürüyüşleri hızla keşfeder | İyi çözümleri bozabilir |
| Düşük mutasyon | Kararlı iyileşme sağlar | Yerel optimumda takılabilir |
| Büyük popülasyon | Daha çeşitli davranışlar üretir | Simülasyon maliyeti yükselir |
| Elitizm | En iyi çözümü korur | Aşırı kullanılırsa çeşitlilik azalır |

Gerçek projede `fitness` hesabını PyBullet, MuJoCo veya Webots gibi fizik motorlarına bağlayın. Her aday için robotu örneğin 10 saniye simüle edin, başlangıç ve bitiş konumlarını ölçün, düşme algılanınca testi erken bitirin. Önce iki bacaklı basit bir modelle başlayın; sonra sensör geri bildirimi, eğimli zemin ve enerji limiti ekleyin. Robotun ilk nesillerde takla atması başarısızlık değil, evrimin “bu da olmadı” diye tuttuğu deney günlüğüdür.

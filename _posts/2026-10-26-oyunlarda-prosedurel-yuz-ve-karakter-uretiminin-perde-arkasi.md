---
layout: post
title: "Oyunlarda Prosedürel Yüz ve Karakter Üretiminin Perde Arkası"
math: true
categories: 
  - Bilgi
tags: 
  - prosedürel üretim
  - oyun geliştirme
  - karakter tasarımı
  - algoritma
  - yapay zekâ
  - grafik programlama
toc: true
image: /img/oyunlarda-prosedurel-yuz-38.png
---

Bir oyunda aynı şehirde dolaşan on bin karakterin birbirine benzememesi, her birinin elle tasarlandığı anlamına gelmez. Geliştiriciler; yüz şekli, vücut oranları, saç, kıyafet ve davranış gibi özellikleri kurallara bağlı biçimde birleştirerek özgün karakterler üretir. Buna **prosedürel karakter üretimi** denir. Kısacası bilgisayar, dijital bir oyuncak kutusundan parçalar seçer; fakat burnu alnına takmamak için tasarım kurallarına uyar.

![oyunlarda-prosedurel-yuz-38](/img/oyunlarda-prosedurel-yuz-38.svg)

``

## Rastgelelik tek başına yeterli mi?

Prosedürel üretimin temelinde sözde rastgele sayı üreteçleri bulunur. Bir **seed** değeri verildiğinde algoritma daima aynı sayı dizisini, dolayısıyla aynı karakteri oluşturur. Böylece geliştirici `84721` seed'ine sahip karakteri daha sonra yeniden üretebilir.

Bir karakteri parametre vektörüyle ifade edebiliriz:

$$
C = [h, w, a, e, n, s, o]
$$

Burada $h$ boyu, $w$ vücut genişliğini, $a$ yaşı, $e$ göz boyutunu, $n$ burun uzunluğunu, $s$ ten tonunu ve $o$ kıyafet seçimini temsil eder. Her parametre kendi aralığında üretilir. Örneğin boy hesabı şöyle modellenebilir:

$$
h = h_{min} + r(h_{max} - h_{min}), \quad 0 \leq r \leq 1
$$

Ancak bütün değerleri bağımsız seçmek garip sonuçlar doğurabilir. Bu nedenle sistemler **kısıtlar**, ağırlıklı olasılıklar ve korelasyonlar kullanır.

| Yaklaşım | Avantajı | Olası sorun |
|---|---|---|
| Tam rastgele seçim | Hızlı ve çeşitlidir | Tutarsız karakterler üretir |
| Kural tabanlı seçim | Sanat yönetimini korur | Sonuçlar tekrar edebilir |
| İstatistiksel model | Doğal dağılımlar sağlar | Kaliteli veri gerektirir |
| Üretken yapay zekâ | Çok yüksek görsel çeşitlilik sunar | Kontrol ve performans zordur |

## Yüzler nasıl biçim değiştiriyor?

Modern oyunlarda temel yüz modeli çoğunlukla **blend shape** adı verilen hedef biçimlerle değiştirilir. Gülümseme, çene genişliği veya kaş yüksekliği için ayrı modeller hazırlanır. Son yüz, bu biçimlerin ağırlıklı birleşimidir:

$$
V = V_0 + \sum_{i=1}^{n} w_i(V_i - V_0)
$$

$V_0$ temel yüzü, $V_i$ hedef biçimi ve $w_i$ etkinin gücünü gösterir. Ağırlıklar dikkatli sınırlandırılmazsa karakter, kahramandan çok eriyen balmumu heykeline benzeyebilir.

Aşağıdaki Python örneği seed kullanarak basit bir karakter profili üretir:

```python
import random

def karakter_uret(seed):
    rng = random.Random(seed)

    yas = rng.randint(18, 75)
    boy = round(rng.gauss(172, 9), 1)
    return {
        "yas": yas,
        "boy_cm": max(145, min(205, boy)),
        "yuz": rng.choice(["oval", "köşeli", "yuvarlak"]),
        "sac": rng.choice(["kısa", "uzun", "kıvırcık", "kel"]),
        "aksesuar": rng.choices(
            ["yok", "gözlük", "şapka"],
            weights=[6, 2, 1]
        )[0]
    }

print(karakter_uret(84721))
```

Burada normal dağılım, karakterlerin çoğunu ortalama boya yakın tutar; aşırı kısa veya uzun sonuçları ise seyrekleştirir. `weights` parametresi de her karakterin şapkalı çıkmasını engeller. Aynı seed her çalıştırmada aynı profili verir.

## Çeşitlilik yalnızca görünüş değildir

İnandırıcı bir kalabalık için ses tonu, yürüme animasyonu, meslek, kişilik ve günlük rutin de üretilebilir. Fakat özellikler arasında mantıksal bağ kurulmalıdır. Ağır zırhlı bir savaşçının bale yürüyüşü komik olabilir; oyun özellikle komedi hedeflemiyorsa bu eşleşme filtrelenir.

| Katman | Örnek parametreler | Kullanılan teknik |
|---|---|---|
| Yüz | Çene, göz, burun | Blend shape |
| Vücut | Boy, kas, kilo | İskelet ölçekleme |
| Görünüm | Saç, kıyafet, renk | Modüler parçalar |
| Davranış | Rutin, hız, tepki | Durum makineleri |
| Kimlik | İsim, meslek, geçmiş | Şablon ve dil modeli |

Sonuç olarak iyi prosedürel üretim, rastgele düğmesine basmaktan çok **kontrollü çeşitlilik mühendisliğidir**. Sanatçılar parçaları ve estetik sınırları belirler; programcılar olasılıkları, bağımlılıkları ve performansı yönetir. Böylece oyun, bellekte binlerce hazır model saklamak yerine birkaç temel varlıktan kalabalık ve kişisel görünen bir dünya kurabilir.

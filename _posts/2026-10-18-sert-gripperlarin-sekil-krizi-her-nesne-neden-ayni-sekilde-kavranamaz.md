---
layout: post
title: "Sert Gripper’ların Şekil Krizi: Her Nesne Neden Aynı Şekilde Kavranamaz?"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - gripper
  - robotik-kavrama
  - mekatronik
  - yumuşak-robotik
  - otomasyon
toc: true
image: /img/sert-gripperlarin-sekil-29.png
---

Endüstriyel robotların ucundaki esnek olmayan, yani rijit gripper’lar; düzenli kutuları taşırken son derece başarılıdır. Ancak karşılarına yumurta, tornavida, muz veya eğimli bir makine parçası çıktığında işler değişir. Sabit geometrili parmaklar nesnenin yüzeyine uyum sağlayamaz ve robotun güçlü kolu, bir anda nesneyi düşüren ya da ezen pahalı bir sakara dönüşebilir.

``

## Rijit gripper nasıl çalışır?

Klasik iki parmaklı gripper, nesneyi karşılıklı iki temas noktası arasında sıkıştırır. Parmakların hareket doğrultusu ve yüzey geometrisi genellikle sabittir. Güvenli kavrama için uygulanan normal kuvvetin oluşturduğu sürtünme, nesnenin ağırlığını yenmelidir:

$$2 μ N ≥ mg$$

Burada $μ$ sürtünme katsayısını, $N$ her parmağın uyguladığı normal kuvveti, $m$ nesnenin kütlesini ve $g$ yer çekimi ivmesini ifade eder. Denklem basit görünse de gerçek dünyada $μ$ sabit değildir. Islak, tozlu veya pürüzsüz bir yüzey sürtünmeyi azaltabilir. Nesnenin ağırlık merkezi temas noktalarının dışında kaldığında ayrıca döndürücü bir moment oluşur:

$$τ = r F$$

$r$ mesafesi büyüdükçe nesnenin gripper içinde dönme ihtimali artar. Robot daha fazla kuvvet uygulayarak bunu engellemeye çalışabilir; fakat bu kez hassas nesne zarar görebilir.

## Şekil değişince neden sorun çıkıyor?

Rijit parmaklar belirli bir geometriye göre tasarlanır. Düz yüzeyli bir kutuda geniş temas alanı oluşurken küresel bir nesnede temas, küçük noktalara sıkışabilir. Düzensiz nesnelerde parmaklardan biri yüzeye ulaşırken diğeri boşlukta kalabilir. Sonuç; kararsız kavrama, kayma ve konum hatasıdır.

| Özellik | Rijit gripper | Uyumlu veya yumuşak gripper |
|---|---|---|
| Parmak geometrisi | Sabit | Nesneye göre şekil değiştirebilir |
| Temas alanı | Genellikle sınırlı | Daha geniş ve dağıtılmış |
| Hassas nesneler | Ezilme riski yüksek | Kuvvet daha dengeli yayılır |
| Farklı şekillere uyum | Düşük | Yüksek |
| Kontrol gereksinimi | Görece basit | Sensör ve modelleme gerekebilir |
| Üretim ortamı | Tek tip parçalar | Değişken ürünler |

Bir gripper yalnızca nesneyi tutmamalı; nesnenin şekli, sertliği ve ağırlık merkezi hakkında oluşan belirsizliği de yönetmelidir. Rijit tasarımda bu görev çoğunlukla kamera kalibrasyonuna ve kusursuz konumlandırmaya bırakılır. Birkaç milimetrelik algılama hatası bile temas noktalarını bozabilir.

## Basit bir kavrama kontrolü

Aşağıdaki Python kodu, tahmini sürtünme ve güvenlik katsayısına göre her parmağın uygulaması gereken minimum kuvveti hesaplar:

```python
def gerekli_parmak_kuvveti(kutle, surtunme, guvenlik=1.5):
    if surtunme <= 0:
        raise ValueError("Sürtünme katsayısı pozitif olmalı")

    yer_cekimi = 9.81
    agirlik = kutle * yer_cekimi
    minimum_kuvvet = agirlik / (2 * surtunme)
    return minimum_kuvvet * guvenlik

nesneler = {
    "plastik_kutu": (0.8, 0.4),
    "cam_sise": (0.5, 0.2),
    "metal_parca": (1.4, 0.3)
}

for ad, (kutle, surtunme) in nesneler.items():
    kuvvet = gerekli_parmak_kuvveti(kutle, surtunme)
    print(f"{ad}: parmak başına {kuvvet:.2f} N")
```

Bu hesaplama başlangıç noktasıdır; yüzey eğriliğini, ivmelenmeyi ve ağırlık merkezi kaymasını içermez. Robot hızlandığında etkin kuvvet $F = ma$ nedeniyle artar. Dolayısıyla statik durumda başarılı görünen kavrama, hareket sırasında başarısız olabilir.

## Daha iyi tasarım seçenekleri

Uyumlu mekanizmalar, yaylı eklemler, tendonla çalışan parmaklar ve silikon tabanlı yumuşak gripper’lar farklı şekillere pasif biçimde uyabilir. Dokunsal sensörler temas kuvvetini ölçerken kuvvet geri beslemeli kontrol, nesne kaymaya başladığında sıkma miktarını ayarlayabilir. Değiştirilebilir parmak uçları da tamamen yeni bir gripper üretmeden farklı görevleri destekler.

Rijit gripper’lar kötü değildir; hızlı, dayanıklı ve tekrarlanabilir oldukları için standart üretimde mükemmeldir. Sorun, her nesnenin standart olduğunu varsaymaktır. Robotların gerçek dünyada daha becerikli olabilmesi için çözüm yalnızca daha güçlü motorlar değil; geometriye uyum sağlayan mekanik tasarım, doğru sensörler ve akıllı kuvvet kontrolünün birlikte kullanılmasıdır.

![sert-gripperlarin-sekil-29](/img/sert-gripperlarin-sekil-29.svg)


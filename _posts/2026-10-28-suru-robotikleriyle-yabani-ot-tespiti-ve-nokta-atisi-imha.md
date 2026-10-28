---
layout: post
title: "Sürü Robotikleriyle Yabani Ot Tespiti ve Nokta Atışı İmha"
math: true
categories: 
  - Proje
tags: 
  - sürü robotikleri
  - yapay zeka
  - bilgisayarlı görü
  - tarım teknolojileri
  - otonom robotlar
  - hassas tarım
toc: true
image: /img/suru-robotikleriyle-yabani-83.png
---

Bir tarlayı tek ve pahalı bir dev makineyle ilaçlamak yerine, avuç içi kadar dikkatli robotlardan oluşan bir ekip kullandığınızı düşünün. Bu robotlar bitkileri kameralarıyla inceliyor, yabani otları ürünlerden ayırıyor ve yalnızca gerekli noktaya müdahale ediyor. Sürü robotikleri, hassas tarımı adeta çok oyunculu bir strateji oyununa dönüştürüyor!


![suru-robotikleriyle-yabani-83](/img/suru-robotikleriyle-yabani-83.svg)

``

## Neden robot sürüsü?

Sürü robotikleri; karınca, arı ve balık sürülerindeki merkezi olmayan iş birliğinden ilham alır. Her robot sınırlı algılama ve hesaplama kapasitesine sahip olsa da filo, görev paylaşımı sayesinde geniş bir alanı verimli biçimde tarayabilir. Bir robot arızalandığında operasyon tamamen durmaz; diğer üyeler boşta kalan bölgeyi devralabilir.

| Yaklaşım | Güçlü yönü | Zayıf yönü |
|---|---|---|
| Büyük tarım makinesi | Yüksek işlem kapasitesi | Toprağı sıkıştırır, pahalıdır |
| Tek otonom robot | Kolay yönetim | Arıza, görevi durdurabilir |
| Küçük robot sürüsü | Ölçeklenebilir ve dayanıklı | Koordinasyon gerektirir |

Basit bir modelde, tarlanın alanı $A$, robot sayısı $N$ ve tek robotun tarama hızı $v$ olsun. İdeal koşullarda görev süresi yaklaşık olarak

$$T \approx \frac{A}{N \cdot v}$$

şeklinde azalır. Gerçekte dönüşler, batarya değişimi, iletişim gecikmesi ve çakışan rotalar nedeniyle bir verim katsayısı kullanılır:

$$T_{gerçek} = \frac{A}{N \cdot v \cdot \eta}, \qquad 0 < \eta \leq 1$$

Buradaki $\eta$, sürünün ne kadar uyumlu çalıştığını gösterir.

## Robot yabani otu nasıl tanır?

Robotun kamerasından gelen görüntü önce renk düzeltme ve gürültü azaltma işlemlerinden geçirilir. Ardından YOLO gibi bir nesne algılama modeli veya U-Net benzeri bir segmentasyon ağı, her pikselin ürün mü, toprak mı yoksa yabani ot mu olduğunu tahmin eder.

| Yöntem | Ürettiği sonuç | Uygun kullanım |
|---|---|---|
| Sınıflandırma | Görüntüde ot var veya yok | Hızlı ön eleme |
| Nesne algılama | Otun çevresinde kutu | Hedef koordinatı bulma |
| Segmentasyon | Piksel düzeyinde maske | Hassas püskürtme veya lazer |

Modelin güven skoru düşükse robot hemen saldırıya geçmez. Yeni görüntü alabilir, farklı açıdan yaklaşabilir veya örneği insan operatöre gönderebilir. Böylece değerli ürünlerin yanlışlıkla yok edilme riski azaltılır.

## Filo koordinasyonu

Tarla hücrelere bölünerek her robota bir bölge atanabilir. Robotlar konum, batarya ve görev durumlarını komşularıyla paylaşır. Aşağıdaki sade Python örneği, iş yükü ve mesafeye göre görev seçimini gösterir:

```python
def gorev_maliyeti(robot, hedef):
    mesafe = robot.konum.uzaklik(hedef.konum)
    batarya_cezasi = 100 if robot.batarya < 20 else 0
    return mesafe + robot.is_yuku * 2 + batarya_cezasi


def robot_sec(robotlar, hedef):
    uygunlar = [r for r in robotlar if r.aktif]
    return min(uygunlar, key=lambda r: gorev_maliyeti(r, hedef))
```

Bu kod en yakın robotu körü körüne seçmek yerine mevcut iş yükünü ve düşük batarya riskini de hesaba katar. Daha gelişmiş sistemlerde açık artırma algoritmaları kullanılır: Robotlar görev için maliyet teklifi verir ve en uygun teklif kazanır.

## İmha seçenekleri

Tespit edilen yabani ot; mikro doz herbisit, mekanik bıçak, elektrik darbesi veya kontrollü lazerle hedeflenebilir. Kimyasal yöntem hızlıdır, ancak çevresel yük oluşturabilir. Mekanik yöntem kalıntı bırakmaz fakat sert zeminde zorlanabilir. Lazer oldukça hassastır; buna karşılık enerji tüketimi ve yangın güvenliği dikkatle yönetilmelidir.

Robot, müdahaleden sonra aynı noktayı yeniden görüntüleyerek sonucu doğrulamalıdır. Başarı oranı

$$Başarı = \frac{doğru\ imha\ edilen\ ot}{hedeflenen\ toplam\ ot}$$

ile izlenebilir. Yanlış pozitifler ayrıca kaydedilerek modelin sonraki eğitiminde kullanılır.

Sonuçta başarılı bir sürü sistemi yalnızca iyi bir yapay zekâ modelinden ibaret değildir. Sağlam mekanik tasarım, güvenli imha düzeneği, RTK-GPS konumlandırma, batarya planlaması ve güvenilir haberleşme birlikte çalışmalıdır. Minik robotların gerçek gücü tek tek ne kadar akıllı olduklarında değil, bilgiyi paylaşıp tarlayı birlikte yönetebilmelerinde saklıdır.

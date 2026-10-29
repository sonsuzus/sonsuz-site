---
layout: post
title: "Akıllı Priz Verisiyle Elektrik Faturasını Küçültme Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - akıllı priz
  - enerji optimizasyonu
  - veri analizi
  - python
  - iot
  - elektrik tüketimi
toc: true
image: /img/akilli-priz-verisiyle-23.png
---

![akilli-priz-verisiyle-23](/img/akilli-priz-verisiyle-23.svg)


Elektrik faturası bazen evde görünmez bir canavar dolaşıyormuş hissi verir: Buzdolabı sessizce çalışır, televizyon bekleme modunda enerji tüketir, elektrikli ısıtıcı ise bütçeyi adeta közler. Akıllı prizler bu canavarı görünür hâle getirir. Cihaz bazında güç ve enerji ölçümü yaparak hangi cihazın ne zaman, ne kadar tükettiğini anlamamızı; tahminlere değil, verilere dayalı tasarruf kararları almamızı sağlar.

``

## Akıllı priz hangi verileri toplar?

Tipik bir akıllı priz belirli aralıklarla gerilim, akım ve aktif güç değerlerini kaydeder. Bazı modeller güç faktörü, frekans ve toplam enerji tüketimi de sunar. Temel elektrik ilişkisi şöyledir:

$$P = V \times I \times \cos(\varphi)$$

Burada $P$ aktif gücü (W), $V$ gerilimi, $I$ akımı ve $\cos(\varphi)$ güç faktörünü gösterir. Bir cihazın tükettiği enerji ise gücün zaman boyunca birikimidir:

$$E = \sum_{i=1}^{n} \frac{P_i \times \Delta t_i}{1000}$$

$P_i$ watt, $\Delta t_i$ saat cinsindeyse sonuç kilovatsaat, yani kWh olur. Faturanın enerji kısmını yaklaşık hesaplamak için $E$ değeri birim fiyatla çarpılır.

| Veri | Birim | Bize ne anlatır? |
|---|---:|---|
| Gerilim | V | Şebeke seviyesini ve dalgalanmaları |
| Aktif güç | W | Cihazın o andaki tüketimini |
| Enerji | kWh | Zaman içinde biriken tüketimi |
| Güç faktörü | 0–1 | Elektriğin ne kadar verimli kullanıldığını |
| Zaman damgası | Tarih/saat | Kullanım alışkanlıklarını ve pik saatleri |

## Ham veriden anlamlı sonuca

Akıllı priz kayıtları önce temizlenmelidir. Eksik ölçümler, tekrarlanan satırlar ve gerçek dışı sıçramalar analizi yanıltabilir. Örneğin normalde 100 W çeken bir televizyonun bir saniyeliğine 30.000 W görünmesi büyük olasılıkla ölçüm veya iletişim hatasıdır.

Temiz veride şu göstergeler özellikle değerlidir:

- **Baz yük:** Cihaz kapalı sanılırken devam eden tüketim.
- **Pik güç:** Cihazın ulaştığı en yüksek güç seviyesi.
- **Çalışma süresi:** Gücün belirlenen eşiğin üzerinde kaldığı süre.
- **Günlük enerji:** Gün boyunca biriken kWh miktarı.
- **Kullanım deseni:** Cihazın hangi saatlerde ve ne sıklıkta çalıştığı.

Aşağıdaki Python örneği, CSV dosyasındaki ölçümlerden günlük enerji ve maliyet üretir:

```python
import pandas as pd

BIRIM_FIYAT = 2.60  # Örnek TL/kWh

veri = pd.read_csv("priz_verisi.csv", parse_dates=["zaman"])
veri = veri.sort_values("zaman").drop_duplicates("zaman")

# Ölçümler arasındaki süreyi saate çevirir.
veri["sure_saat"] = veri["zaman"].diff().dt.total_seconds() / 3600
veri["sure_saat"] = veri["sure_saat"].clip(lower=0, upper=1)

# Watt-saat hesabını kWh değerine dönüştürür.
veri["enerji_kwh"] = veri["guc_watt"] * veri["sure_saat"] / 1000
veri["gun"] = veri["zaman"].dt.date

ozet = veri.groupby("gun")["enerji_kwh"].sum().to_frame()
ozet["maliyet_tl"] = ozet["enerji_kwh"] * BIRIM_FIYAT
print(ozet)
```

Kod, ardışık kayıtlar arasındaki süreyi hesaplar ve ölçülen güçle çarpar. Bir saatten uzun veri boşluklarını sınırlamak, eksik kayıtların tüketimi yapay biçimde büyütmesini engeller.

## Tasarruf fırsatlarını sınıflandırmak

Her yüksek tüketim gereksiz değildir. Buzdolabının sürekli çalışması normal olabilir; fakat eski bir modelin yeni modele göre iki kat enerji harcaması değişim kararını destekleyebilir.

| Gözlem | Olası neden | Uygulanabilecek işlem |
|---|---|---|
| Gece boyunca sabit tüketim | Bekleme modu | Zamanlayıcıyla elektriği kesmek |
| Uzun ve sık çalışma döngüsü | Bakım ihtiyacı | Filtre, conta veya termostat kontrolü |
| Pik saatlerde yoğun kullanım | Kullanım alışkanlığı | Çalışmayı uygun saatlere taşımak |
| Benzer cihazdan yüksek tüketim | Düşük verimlilik | Verimli modelle değiştirmeyi değerlendirmek |

Bir önlemin aylık kazancı yaklaşık olarak

$$Tasarruf = Azaltılan\ kWh \times Birim\ Fiyat$$

formülüyle bulunabilir. Yeni cihaz alınacaksa geri ödeme süresi de $Yatırım\ Maliyeti / Aylık\ Tasarruf$ şeklinde hesaplanır.

Sonuç olarak akıllı priz, tek başına faturayı düşüren sihirli bir düğme değildir; doğru soruları sormayı sağlayan küçük bir veri laboratuvarıdır. En etkili yaklaşım, birkaç hafta ölçüm yapmak, baz tüketimi ve çalışma döngülerini karşılaştırmak, ardından zamanlama, bakım veya cihaz değişimi gibi müdahalelerin sonucunu yeniden ölçmektir. Ölç, değiştir, tekrar ölç: Enerji optimizasyonunun en kısa ve en güvenilir döngüsü budur.

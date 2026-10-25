---
layout: post
title: "Akıllı Sayaçlarla Enerji Şebekesi Optimizasyonu"
math: true
categories: 
  - Bilgi
tags: 
  - akıllı sayaç
  - enerji optimizasyonu
  - akıllı şebeke
  - veri analizi
  - makine öğrenmesi
  - python
toc: true
image: /img/akilli-sayaclarla-enerji-71.png
---

Bir şehir aynı anda uyanıp kahve makinelerini, klimaları ve fabrikaları çalıştırdığında elektrik şebekesi ciddi bir denge sınavına girer. Geleneksel sayaçlar yalnızca dönemsel tüketimi gösterirken akıllı sayaçlar, tüketimi kısa aralıklarla ölçerek şebekenin adeta nabzını tutar. Böylece enerji üretimi, depolama sistemleri ve tüketici talepleri gerçek zamanlı verilere göre yönetilebilir.

``

## Akıllı sayaç verisi nedir?

Akıllı sayaçlar elektrik tüketimini genellikle 1, 5, 15 veya 30 dakikalık aralıklarla kaydeder. Her ölçüm; zaman damgası, tüketilen enerji, gerilim, akım ve bazı sistemlerde güç faktörü gibi alanlar içerebilir. Veriler güvenli iletişim ağları üzerinden merkezi bir yönetim platformuna gönderilir.

Bir sayacın belirli bir aralıktaki ortalama gücü basitçe şöyle hesaplanabilir:

$$P = E / t$$

Burada $E$ tüketilen enerji, $t$ ölçüm süresi ve $P$ ortalama güçtür. Şehir genelindeki toplam talep ise $N$ sayacın katkısıyla bulunur:

$$P_{toplam}(t) = \sum_{i=1}^{N} P_i(t)$$

Bu toplam, santrallerin ve bataryaların karşılaması gereken anlık yükü temsil eder. Üretim ile tüketim dengelenemezse frekans sapmaları, kesintiler veya ekipman hasarları ortaya çıkabilir.

## Geleneksel ve akıllı yaklaşım

| Özellik | Geleneksel sayaç | Akıllı sayaç |
|---|---|---|
| Ölçüm sıklığı | Aylık | Dakikalık veya saatlik |
| Veri aktarımı | Görevli tarafından | Otomatik ve uzaktan |
| Arıza tespiti | Gecikmeli | Gerçek zamana yakın |
| Talep tahmini | Sınırlı | Ayrıntılı ve dinamik |
| Fiyatlandırma | Genellikle sabit | Zamana bağlı olabilir |

Akıllı sistem, yalnızca daha fazla veri toplamaz; şehrin davranış kalıplarını görünür hâle getirir. Örneğin sıcaklık yükseldiğinde klima tüketiminin ne kadar artacağı veya bir futbol maçı bittiğinde talebin nasıl sıçrayacağı tahmin edilebilir.

## Veriden dengelemeye giden yol

İlk aşama veri temizliğidir. Eksik ölçümler enterpolasyonla tamamlanabilir, fiziksel olarak imkânsız değerler aykırı veri olarak işaretlenebilir. Ardından hava durumu, takvim, resmi tatiller ve geçmiş tüketim gibi değişkenlerle talep tahmini yapılır.

Basitleştirilmiş bir Python örneği, hareketli ortalama kullanarak kısa vadeli yük tahmini üretir:

```python
import pandas as pd

veri = pd.read_csv("sayac_verisi.csv", parse_dates=["zaman"])
veri = veri.sort_values("zaman")

# Son dört ölçümün ortalaması kısa vadeli tahmin olarak kullanılır.
veri["tahmin_kw"] = veri["tuketim_kw"].rolling(4).mean()

# Gerçek tüketim ile tahmin arasındaki fark hesaplanır.
veri["denge_ihtiyaci_kw"] = (
    veri["tuketim_kw"] - veri["tahmin_kw"]
)

print(veri.tail())
```

Bu yöntem öğretici olsa da gerçek sistemlerde ARIMA, gradyan artırma, LSTM veya Transformer tabanlı modeller kullanılabilir. Tahmin edilen talep üretim planına aktarılır. Beklenmedik bir artış varsa bataryalar devreye alınabilir; düşüş varsa üretim azaltılabilir ya da fazla enerji depolanabilir.

## Talep tarafı yönetimi

Optimizasyon yalnızca daha fazla elektrik üretmek anlamına gelmez. Yoğun saatlerde elektrikli araç şarjını ertelemek, ticari binaların klimalarını küçük ölçüde ayarlamak veya tüketicilere indirim sunmak da denge sağlar. Amaç maliyeti ifade eden $C$, emisyonu ifade eden $M$ ve kesinti riskini ifade eden $R$ değerlerini birlikte küçültmektir:

$$minimize\quad \alpha C + \beta M + \gamma R$$

Katsayılar şehrin önceliklerini temsil eder. Çevreci bir yönetim $\beta$ değerini, kesintiye karşı hassas bir hastane bölgesi ise $\gamma$ değerini yükseltebilir.

## Güvenlik ve mahremiyet

Ayrıntılı tüketim verisi, insanların evde olup olmadığına dair ipuçları verebilir. Bu nedenle veriler şifrelenmeli, mümkün olduğunda anonimleştirilmeli ve yalnızca gerekli süre boyunca saklanmalıdır. Ayrıca sayaç yazılımları güncel tutulmalı ve sahte ölçümlere karşı doğrulama mekanizmaları kullanılmalıdır.

Sonuç olarak akıllı sayaçlar, elektrik faturasını dijitalleştiren cihazlardan çok daha fazlasıdır. Doğru veri mühendisliği ve optimizasyon yöntemleriyle şehirler daha az kayıp yaşayan, yenilenebilir kaynakları daha iyi kullanan ve talep sıçramalarına daha çevik tepki veren enerji sistemleri kurabilir.

![akilli-sayaclarla-enerji-71](/img/akilli-sayaclarla-enerji-71.svg)


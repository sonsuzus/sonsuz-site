---
layout: post
title: "Prophet, ARIMA ve LSTM: Trend ile Mevsimsellik Avında Hangisi Daha Güçlü?"
math: true
categories: 
  - Bilgi
tags: 
  - zaman serisi
  - makine öğrenmesi
  - prophet
  - arıma
  - lstm
toc: true
---

Zaman serisi tahmini, yalnızca geçmiş değerleri geleceğe uzatmak değildir; verinin içindeki yön değişimlerini, tekrar eden döngüleri ve beklenmedik dalgalanmaları okumaktır. Bir e-ticaret sitesinin günlük satışları, elektrik tüketimi ya da web trafiği bu açıdan klasik örneklerdir. Prophet, ARIMA ve LSTM aynı hedefe koşsa da trend ve mevsimselliği ele alış biçimleri oldukça farklıdır.

``

Bir zaman serisini sezgisel olarak şu bileşenlere ayırabiliriz:

$$y_t = T_t + S_t + R_t$$

Burada $T_t$ trendi, $S_t$ mevsimselliği, $R_t$ ise modelin açıklayamadığı rastgele kalıntıyı temsil eder. Bazı serilerde etkiler toplamsal değil çarpımsaldır: satış miktarı büyüdükçe sezon etkisi de büyür. Bu durumda $y_t = T_t \times S_t \times R_t$ yaklaşımı daha uygun olabilir.

## ARIMA: İstatistiksel ve Disiplinli Klasik

ARIMA, adını **AutoRegressive Integrated Moving Average** bileşenlerinden alır ve $ARIMA(p,d,q)$ ile ifade edilir. $p$ geçmiş gözlemlerin, $d$ durağanlık için alınan farkların, $q$ ise geçmiş hata terimlerinin etkisini anlatır. Modelin temel fikri, serinin geçmiş davranışından doğrusal bir gelecek üretmektir.

Mevsimsellik gerekiyorsa ARIMA genellikle SARIMA biçimine genişletilir: $SARIMA(p,d,q)(P,D,Q)_s$. Buradaki $s$, örneğin aylık veride 12 olan mevsim periyodudur. ARIMA trendi doğrudan “görmez”; fark alma işlemiyle trendi kaldırır, sonra tahminleri bu dönüşüm üzerinden üretir. Bu nedenle düzenli, durağanlaştırılabilir serilerde çok başarılıdır; ani yapısal kırılmalar ise canını sıkabilir.

## Prophet: Takvimle Barışık Tahminci

Meta tarafından geliştirilen Prophet, trendi parçalı doğrusal veya lojistik büyüme eğrileriyle, mevsimselliği ise Fourier serileriyle modeller. Mevsimsel etki kabaca şöyle yazılabilir:

$$S(t) = \sum_{n=1}^{N}\left(a_n\cos\left(\frac{2\pi nt}{P}\right)+b_n\sin\left(\frac{2\pi nt}{P}\right)\right)$$

Bu yapı, haftalık ve yıllık döngüleri esnek biçimde yakalar. Tatiller, kampanyalar ve özel günler de modele ek değişken olarak katılabilir. Prophet'in süper gücü, eksik gözlemler ve trend kırılmaları bulunan iş verilerinde hızlı, anlaşılır sonuçlar vermesidir. Buna karşılık çok karmaşık kısa dönem bağımlılıkları LSTM kadar iyi öğrenmeyebilir.

## LSTM: Hafızası Güçlü Derin Öğrenme Modeli

LSTM, tekrarlayan sinir ağlarının uzun vadeli bağımlılık sorununu kapılar yardımıyla çözen bir türüdür. Unutma, giriş ve çıkış kapıları; hangi bilginin saklanacağına karar verir. Örneğin bir ürünün satışındaki “maaş günü etkisi”, yeterli veri varsa LSTM tarafından öğrenilebilir.

Ancak LSTM mevsimselliği kendiliğinden etiketlemez; onu örneklerden çıkarır. Bu yüzden çok veri, iyi ölçekleme ve dikkatli pencereleme ister. Az veride güçlü görünen ağ, eğitim setini ezberleyen pahalı bir papağana dönüşebilir.

| Özellik | ARIMA / SARIMA | Prophet | LSTM |
|---|---|---|---|
| Trend yakalama | Fark alma ile dolaylı | Parçalı trend ile güçlü | Veriden öğrenir |
| Mevsimsellik | Parametreyle açıkça tanımlanır | Fourier bileşenleriyle esnek | Yeterli veriyle öğrenilir |
| Veri ihtiyacı | Düşük-orta | Orta | Yüksek |
| Açıklanabilirlik | Yüksek | Çok yüksek | Düşük-orta |
| Tatil/kampanya etkisi | Dış değişkenle eklenir | Doğal olarak destekler | Özellik mühendisliği ister |

Aşağıdaki örnek, Prophet ile haftalık mevsimsellik ve özel kampanya günlerini tanımlamanın temel halidir:

```python
from prophet import Prophet
import pandas as pd

# df kolonları: ds (tarih), y (hedef değer)
kampanyalar = pd.DataFrame({
    "holiday": "kampanya",
    "ds": pd.to_datetime(["2026-11-27", "2026-11-28"]),
    "lower_window": 0,
    "upper_window": 1
})

model = Prophet(weekly_seasonality=True,
                yearly_seasonality=True,
                holidays=kampanyalar)
model.fit(df)
gelecek = model.make_future_dataframe(periods=30)
tahmin = model.predict(gelecek)
```

Bu kod, geçmiş satışlardan trendi ve döngüleri öğrenir; kampanya günlerinin olağan dışı etkisini ayrı bir sinyal olarak değerlendirir. Model seçerken “en modern” olana değil, veri hacmine ve iş problemine bakın: temiz ve düzenli seri için SARIMA, takvim etkili iş verisi için Prophet, bol veriyle karmaşık örüntüler için LSTM mantıklı başlangıç noktalarıdır. Son kararı ise mutlaka zaman tabanlı doğrulama ve MAE, RMSE gibi hata metrikleri vermelidir.

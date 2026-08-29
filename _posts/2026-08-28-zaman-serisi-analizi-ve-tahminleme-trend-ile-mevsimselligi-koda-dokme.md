---
layout: post
title: "Zaman Serisi Analizi ve Tahminleme: Trend ile Mevsimselliği Koda Dökme"
math: true
categories: 
  - Bilgi
tags: 
  - zaman serisi
  - python
  - tahminleme
  - veri analizi
  - sarıma
---

Zaman serileri, gözlemlerin yalnızca değerinden değil, **ne zaman** oluştuğundan da anlam çıkaran veri yapılarıdır. Bir mağazanın aylık satışları, elektrik tüketimi veya web sitesi trafiği buna örnektir. Geleceği tahmin etmenin sihirli bir kristal küre olmadığını baştan kabul edelim: Ama geçmişte tekrar eden desenleri yakalayarak oldukça makul tahminler üretebiliriz. Bu desenlerin en önemli ikilisi trend ve mevsimselliktir.
``

Bir zaman serisini çoğunlukla üç parçaya ayırırız: uzun vadeli yönü ifade eden **trend**, belirli aralıklarla tekrarlanan **mevsimsellik** ve modelin açıklayamadığı **artık/hata** bileşeni. Toplamsal model şu şekildedir:

$$y_t = T_t + S_t + e_t$$

Burada $y_t$ gözlenen değer, $T_t$ trend, $S_t$ mevsimsel etki ve $e_t$ rastgele hatadır. Değişkenlik seri seviyesi büyüdükçe artıyorsa çarpımsal yaklaşım daha uygundur:

$$y_t = T_t \times S_t \times e_t$$

Örneğin dondurma satışları yıllar içinde artıyorsa trend pozitiftir; her yaz tepe yapıyorsa bu tekrar eden hareket mevsimselliktir. Sadece son üç ayın ortalamasını almak, temmuzdaki satışları ocak verisiyle aynı kefeye koymak demektir. İstatistik de buna hafifçe kaşlarını kaldırır.

| Bileşen | Ne anlatır? | Örnek | Tahmine katkısı |
|---|---|---|---|
| Trend | Uzun dönem yön | Satışların yıllık artması | Temel seviyeyi belirler |
| Mevsimsellik | Sabit periyotlu tekrar | Hafta sonu trafik artışı | Dönemsel düzeltme yapar |
| Artık | Açıklanamayan bölüm | Beklenmedik kampanya etkisi | Belirsizliği gösterir |

İlk pratik adım veriyi doğru zaman indeksine oturtmak, sıralamak ve eksikleri incelemektir. Ardından seriyi eğitim ve test olarak **zamana göre** bölmeliyiz. Rastgele `train_test_split` kullanmak gelecek bilgisini geçmişe sızdırabilir; zaman serilerinde bu, sınavın cevap anahtarını modele vermeye benzer.

Aşağıdaki örnek, aylık satış verisini ayrıştırır ve mevsimsel ARIMA ailesinden `SARIMAX` ile 12 aylık tahmin üretir. `period=12`, aylık veride yıllık döngüyü temsil eder.

```python
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX

# CSV: tarih,satis sütunlarını içeriyor
df = pd.read_csv("satislar.csv", parse_dates=["tarih"])
seri = df.set_index("tarih")["satis"].asfreq("MS")
seri = seri.interpolate()  # Eksik aylara kontrollü yaklaşım

# Trend ve mevsimselliği görünür hale getirir
ayrisim = seasonal_decompose(seri, model="additive", period=12)
print(ayrisim.trend.tail())
print(ayrisim.seasonal.head(12))

# Son 12 ay test, önceki gözlemler eğitim kümesidir
egitim, test = seri.iloc[:-12], seri.iloc[-12:]
model = SARIMAX(egitim, order=(1, 1, 1),
                seasonal_order=(1, 1, 1, 12),
                enforce_stationarity=False)
sonuc = model.fit(disp=False)
tahmin = sonuc.forecast(steps=len(test))

mae = (test - tahmin).abs().mean()
print(f"Ortalama mutlak hata: {mae:.2f}")
```

`order=(p,d,q)` kısa vadeli otokorelasyonu ve fark alma miktarını, `seasonal_order=(P,D,Q,s)` ise bunun mevsimsel karşılığını tanımlar. Özellikle $d=1$, seviyedeki trendi azaltmak için ardışık farkı kullanır:

$$\Delta y_t = y_t - y_{t-1}$$

Model seçerken yalnızca düşük eğitim hatasına bakmayın. Tahmin kalitesini test döneminde MAE, RMSE veya MAPE ile değerlendirin. MAE kolay yorumlanır; RMSE büyük hataları daha sert cezalandırır; MAPE ise değerler sıfıra yakınsa yanıltıcı olabilir.

| Metrik | Formül özeti | Güçlü yanı | Dikkat edilmesi gereken |
|---|---|---|---|
| MAE | $\frac{1}{n}\sum\vert y-\hat{y}\vert $ | Birim cinsinden anlaşılır | Büyük hatalara duyarlılığı sınırlı |
| RMSE | $\sqrt{\frac{1}{n}\sum(y-\hat{y})^2}$ | Büyük sapmaları öne çıkarır | Aykırı değerlerden etkilenir |
| MAPE | Ortalama yüzde hata | Ölçekten bağımsızdır | Sıfıra yakın değerlerde sorunlu |

Son olarak, trendin kırılabileceğini ve mevsimselliğin kampanya, tatil ya da ekonomik koşullarla değişebileceğini unutmayın. Tahmin modeli yaşayan bir sistemdir: Yeni veri geldikçe yeniden değerlendirilmesi, artıkların kontrol edilmesi ve farklı dönemlerde geriye dönük test edilmesi gerekir. İyi tahmin, geçmişi ezberlemek değil; geçmişteki ritmi anlayıp geleceğe temkinli biçimde taşımaktır.

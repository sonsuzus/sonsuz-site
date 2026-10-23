---
layout: post
title: "Python ile Hisse Senedi Analizi: Fiyat, Hacim ve Volatilite"
math: true
categories: 
  - Program
tags: 
  - python
  - hisse senedi
  - veri analizi
  - finans
  - pandas
  - volatilite
  - yfinance
toc: true
image: /img/python-ile-hisse-62.png
---

Bir hisse senedinin grafiğine bakıp “Buradan kesin yükselir!” demek kolaydır; zor olan, bu fikri verilerle sınamaktır. Python sayesinde fiyat hareketlerini, işlem hacmini ve riskin önemli göstergelerinden volatiliteyi birkaç araçla inceleyebiliriz. Bu yazıda `yfinance`, `pandas` ve `matplotlib` kullanarak tekrar çalıştırılabilir küçük bir analiz hazırlayacağız. Amacımız geleceği sihirli biçimde tahmin etmek değil, piyasa davranışını ölçülebilir değişkenlere dönüştürmektir.
``
## Üç temel değişken ne anlatır?

Fiyat, alıcılarla satıcıların ulaştığı son uzlaşmayı gösterir. Hacim, belirli bir dönemde kaç adet hissenin el değiştirdiğini ifade eder. Volatilite ise getirilerin ne kadar dalgalandığını ölçer. Fiyat yönü anlatırken volatilite yön belirtmez; sert yükseliş de sert düşüş de volatiliteyi artırabilir.

| Değişken | Temel soru | Yüksek değer ne söyleyebilir? |
|---|---|---|
| Fiyat | Hisse hangi seviyede? | Tek başına yeterli değildir |
| Hacim | Hareket ne kadar katılımla oluştu? | İlgi veya güçlü işlem aktivitesi |
| Volatilite | Getiriler ne kadar oynak? | Daha yüksek belirsizlik ve risk |

![python-ile-hisse-62](/img/python-ile-hisse-62.svg)


Finansal analizde doğrudan fiyat farkı yerine çoğunlukla günlük yüzde getiri kullanılır:

$$r_t = \frac{P_t}{P_{t-1}} - 1$$

Burada $P_t$ bugünkü, $P_{t-1}$ önceki işlem gününün kapanış fiyatıdır. Günlük getirilerin standart sapması oynaklığın temel ölçüsüdür. Yaklaşık 252 işlem günü bulunduğu varsayımıyla yıllıklandırılmış volatilite şöyle hesaplanır:

$$\sigma_{yıllık} = \sigma_{günlük}\sqrt{252}$$

Karekök çarpanı önemlidir; günlük volatiliteyi doğrudan 252 ile çarpmak finans dünyasının klasik muz kabuklarından biridir.

## Veriyi indirme ve hazırlama

Önce gerekli paketleri kurabiliriz:

```bash
pip install yfinance pandas matplotlib
```

Aşağıdaki kod Apple hissesinin iki yıllık günlük verisini indirir. Farklı bir şirket için `AAPL` sembolünü değiştirmek yeterlidir.

```python
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

symbol = "AAPL"
data = yf.download(
    symbol,
    period="2y",
    interval="1d",
    auto_adjust=True,
    progress=False
)

data = data.dropna()
data["Return"] = data["Close"].pct_change()
data["MA20"] = data["Close"].rolling(20).mean()
data["Volatility20"] = data["Return"].rolling(20).std() * (252 ** 0.5)
```

`auto_adjust=True`, bölünme ve temettü gibi etkiler için düzeltilmiş fiyatlarla çalışmayı kolaylaştırır. `MA20`, son 20 günün ortalama fiyatını; `Volatility20` ise kayan penceredeki yıllıklandırılmış oynaklığı üretir. İlk satırlardaki bazı değerlerin `NaN` olması normaldir çünkü 20 günlük hesaplama için yeterli geçmiş henüz oluşmamıştır.

## Hacimde sıra dışı günleri bulmak

Hacmi yalnızca ham sayı olarak değerlendirmek yanıltıcı olabilir. Apple için normal sayılan hacim, daha küçük bir şirket için olağanüstü olabilir. Bu yüzden hacmi kendi yakın geçmişiyle karşılaştırabiliriz:

```python
data["VolumeAvg20"] = data["Volume"].rolling(20).mean()
data["VolumeRatio"] = data["Volume"] / data["VolumeAvg20"]

unusual = data[data["VolumeRatio"] > 2]
print(unusual[["Close", "Volume", "VolumeRatio"]].tail())
```

`VolumeRatio` değerinin 2 olması, günlük hacmin 20 günlük ortalamanın iki katına ulaştığını belirtir. Bu durum haber, bilanço açıklaması veya güçlü piyasa ilgisiyle ilişkili olabilir; ancak tek başına alış ya da satış sinyali değildir.

## Sonuçları görselleştirme

```python
fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

data[["Close", "MA20"]].plot(ax=axes[0], title=f"{symbol} Fiyat ve 20 Günlük Ortalama")
data["Volume"].plot(ax=axes[1], kind="bar", title="İşlem Hacmi", color="steelblue")
data["Volatility20"].plot(ax=axes[2], title="20 Günlük Yıllıklandırılmış Volatilite", color="darkorange")

plt.tight_layout()
plt.show()
```

Grafikleri birlikte okumak en faydalı yaklaşımdır. Fiyat hareketine yükselen hacim eşlik ediyorsa katılım güçlenmiş olabilir. Aynı sırada volatilite sıçrıyorsa piyasanın sakin bir yürüyüşten çok hız trenine geçtiği anlaşılır. Yine de korelasyon nedensellik değildir ve geçmiş veriler geleceği garanti etmez. Komisyon, likidite, haber akışı ve piyasa rejimi gibi etkenler ayrıca değerlendirilmelidir. Bu çalışma yatırım tavsiyesi değil, daha disiplinli analiz için başlangıç noktasıdır.

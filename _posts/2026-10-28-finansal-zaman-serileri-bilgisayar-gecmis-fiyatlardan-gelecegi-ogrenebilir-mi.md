---
layout: post
title: "Finansal Zaman Serileri: Bilgisayar Geçmiş Fiyatlardan Geleceği Öğrenebilir mi?"
math: true
categories: 
  - Bilgi
tags: 
  - finans
  - zaman-serileri
  - makine-öğrenmesi
  - python
  - veri-bilimi
  - tahminleme
toc: true
image: /img/finansal-zaman-serileri-26.png
---

Borsa grafiklerine bakıp “Bu çizgi birazdan kesin yükselir!” demek kolaydır; bunu tutarlı biçimde kanıtlamak ise oldukça zordur. Bilgisayarlar geçmiş fiyatları insanlardan çok daha hızlı inceleyebilir, ancak geleceği gösteren sihirli bir küreye sahip değildir. Finansal zaman serisi analizi, fiyatların içindeki tekrar eden örüntüleri, riskleri ve olasılıkları matematiksel yöntemlerle araştırır.


![finansal-zaman-serileri-26](/img/finansal-zaman-serileri-26.svg)

``

## Finansal zaman serisi nedir?

Bir varlığın belirli zamanlarda ölçülen fiyatları bir zaman serisi oluşturur:

$$P_1, P_2, P_3, \ldots, P_t$$

Burada $P_t$, varlığın $t$ anındaki fiyatıdır. Fakat doğrudan fiyatları modellemek çoğu zaman yanıltıcıdır. Fiyat serileri genellikle durağan değildir; ortalamaları ve oynaklıkları zamanla değişebilir. Bu nedenle analistler çoğunlukla **getiri** kullanır:

$$r_t = \frac{P_t-P_{t-1}}{P_{t-1}}$$

Logaritmik getiri ise farklı dönemleri toplamayı kolaylaştırır:

$$r_t = \ln\left(\frac{P_t}{P_{t-1}}\right)$$

Örneğin fiyat 100’den 103’e çıkarsa basit getiri yaklaşık yüzde 3’tür. Bilgisayar açısından asıl soru şudur: Önceki getiriler, sıradaki getiri hakkında anlamlı bilgi taşıyor mu?

## Bilgisayar hangi sinyalleri arar?

Algoritmalar trend, momentum, mevsimsellik, işlem hacmi ve oynaklık gibi özellikleri araştırabilir. Ancak bulunan her ilişki gerçek bir ekonomik mekanizma değildir. Bazen model, verideki rastlantısal gürültüyü öğrenir; buna **aşırı öğrenme** denir.

| Kavram | Ne anlatır? | Yaygın risk |
|---|---|---|
| Trend | Uzun dönemli yön | Yönün aniden değişmesi |
| Momentum | Hareketin kısa süre devam etmesi | Geç sinyal üretmesi |
| Ortalama dönüş | Fiyatın tipik seviyeye yaklaşması | “Tipik” seviyenin değişmesi |
| Oynaklık | Hareketlerin büyüklüğü | Krizlerde hızla sıçraması |
| Hacim | Piyasa katılımı | Tek başına yön göstermemesi |

Basit bir hareketli ortalama, son $n$ fiyatın ortalamasıdır:

$$MA_t = \frac{1}{n}\sum_{i=0}^{n-1}P_{t-i}$$

Kısa dönemli ortalama uzun dönemli ortalamayı geçtiğinde yükseliş sinyali üretilebilir. Ne var ki bu, geleceğin kesin yükseleceği anlamına gelmez; yalnızca geçmiş hareketin belirli bir özetidir.

## Python ile küçük bir deney

Aşağıdaki kod fiyatlardan getiri üretir, beş günlük hareketli ortalamayı hesaplar ve bir sonraki günün yönünü tahmin etmek için lojistik regresyon kullanır:

```python
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# CSV dosyasında Date ve Close sütunları bulunduğunu varsayıyoruz.
df = pd.read_csv("prices.csv", parse_dates=["Date"])
df = df.sort_values("Date")

df["return"] = df["Close"].pct_change()
df["ma5"] = df["Close"].rolling(5).mean()
df["distance"] = df["Close"] / df["ma5"] - 1
df["target"] = (df["return"].shift(-1) > 0).astype(int)
df = df.dropna()

split = int(len(df) * 0.8)
train, test = df.iloc[:split], df.iloc[split:]

features = ["return", "distance"]
model = LogisticRegression()
model.fit(train[features], train["target"])

prediction = model.predict(test[features])
print("Doğruluk:", accuracy_score(test["target"], prediction))
```

Buradaki kronolojik ayırma kritik önemdedir. Veriyi rastgele karıştırmak, gelecekteki bilgilerin eğitim kümesine sızmasına yol açabilir. Bu durum modelin gerçekte sahip olamayacağı bir avantaj kazanmasıdır.

## Tahmin başarısı nasıl değerlendirilir?

Yüzde 52 doğruluk ilk bakışta etkileyici görünmeyebilir; ancak işlem maliyetleri düşükse değerli olabilir. Tersine, yüzde 60 doğruluk yüksek komisyonlar ve büyük kayıplar nedeniyle zararla sonuçlanabilir. Bu yüzden doğruluğun yanında getiri, maksimum düşüş, Sharpe oranı ve işlem maliyetleri incelenmelidir.

Bilgisayar geçmişten olasılıksal ilişkiler öğrenebilir; fakat savaşlar, düzenlemeler, şirket haberleri ve yatırımcı psikolojisindeki kırılmalar geçmişte bulunmayabilir. En iyi yaklaşım, modeli bir kâhin değil, belirsizlik altında karar vermeye yardımcı olan ölçüm aracı olarak görmektir. Finansal tahminin asıl başarısı geleceği kusursuz bilmekten değil, yanlış çıkıldığında riski yönetebilmekten gelir.

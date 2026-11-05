---
layout: post
title: "Akıllı Şebekelerde Talep Tahmini: Elektriğin Yarınını Verilerle Okumak"
math: true
categories: 
  - Bilgi
tags: 
  - akıllı şebekeler
  - talep tahmini
  - zaman serileri
  - makine öğrenmesi
  - python
  - enerji
toc: true
image: /img/akilli-sebekelerde-talep-56.png
---

Bir bölgenin yarın ne kadar elektrik tüketeceğini bilmek, enerji sisteminin kristal küresine sahip olmak gibidir. Ancak burada sihir yerine geçmiş ölçümler, hava durumu ve algoritmalar çalışır. Başarılı talep tahmini; üretimi planlamayı, depolamayı yönetmeyi ve şebekedeki pahalı sürprizleri azaltmayı sağlar. Peki elektrik tüketiminin geleceği geçmişten nasıl çıkarılır?

``

## Tüketim neden tahmin edilebilir?

Elektrik tüketimi tamamen rastgele değildir. Sabah çalışan fabrikalar, akşam açılan televizyonlar ve sıcak günlerde devreye giren klimalar tekrar eden örüntüler oluşturur. Saatlik tüketimi kabaca şöyle düşünebiliriz:

$$y_t = T_t + S_t + W_t + \varepsilon_t$$

Burada $T_t$ uzun dönemli eğilimi, $S_t$ günlük ve haftalık mevsimselliği, $W_t$ hava koşullarının etkisini, $\varepsilon_t$ ise açıklanamayan değişimleri temsil eder. Bu ayrışım kavramsal bir başlangıçtır; gerçek ilişkiler her zaman toplamsal değildir.

Tahmin ufku da önemlidir. Bir saat sonrası için yakın geçmiş güçlü bir ipucuyken, ertesi günün tamamında hava tahmini ve takvim daha belirleyici olabilir. Yıllık planlamadaysa nüfus, sanayi ve elektrikli araç kullanımı sahneye çıkar.

## Hangi algoritma ne zaman işe yarar?

| Yaklaşım | Güçlü tarafı | Dikkat edilmesi gereken |
|---|---|---|
| Mevsimsel naif | Basit ve güçlü karşılaştırma noktası | Ani değişimleri yakalayamaz |
| SARIMA | Düzenli mevsimselliği modeller | Karmaşık doğrusal olmayan etkilerde sınırlıdır |
| Gradyan artırmalı ağaçlar | Takvim ve hava etkileşimlerini öğrenir | Özellik hazırlığı ister |
| LSTM / Transformer | Uzun ve karmaşık örüntüleri öğrenebilir | Daha fazla veri ve ayarlama gerektirir |

![akilli-sebekelerde-talep-56](/img/akilli-sebekelerde-talep-56.svg)


En karmaşık model otomatik olarak en iyisi değildir. Dün aynı saatin tüketimini kullanan basit bir yöntem, kötü hazırlanmış bir derin öğrenme modelini rahatlıkla geçebilir. Önce çıtayı ölçün, sonra yükseltin!

## Veriyi hazırlamak: Asıl iş burada

Saatlik bölgesel tüketim, zaman damgası, tatil bilgisi ve mümkünse meteorolojik veriler toplanır. Burada hedefimiz saatlik enerji tüketimidir; birimi MWh'dir. Anlık güç ölçümleriyle enerji toplamlarını karıştırmamak gerekir.

Zaman damgaları ortak saat dilimine dönüştürülmeli, tercihen UTC üzerinden işlenmelidir. Eksik saatler, sayaç arızaları ve olağandışı sıçramalar incelenmelidir. Ancak gerçek tüketim zirvelerini sırf sıra dışı oldukları için silmek, modelin tam ihtiyaç duyulan anlarda başarısız olmasına yol açabilir.

En kritik kural: Geleceğin bilgisini geçmişe sızdırmayın. Hava değişkeni ekleniyorsa, hedef saatin gerçekleşmiş sıcaklığı değil, tahmin anında erişilebilen meteorolojik öngörü kullanılmalıdır.

## Python ile bir saat ileri tahmin

Aşağıdaki örnek, birkaç aylık saatlik veri bulunduğunu varsayar. CSV dosyası `zaman` ve `tuketim_mwh` sütunlarını içerir. Gecikmeler geçmiş tüketimi, döngüsel saat özellikleri ise gün içindeki ritmi temsil eder. Basitlik için hava değişkenlerini dışarıda bırakıyoruz.

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

df = pd.read_csv('tuketim.csv', parse_dates=['zaman'])
df = df.set_index('zaman').sort_index().asfreq('h')

for lag in [1, 24, 168]:
    df[f'lag_{lag}'] = df['tuketim_mwh'].shift(lag)

df['ortalama_24'] = (
    df['tuketim_mwh'].shift(1).rolling(24).mean()
)
df['saat_sin'] = np.sin(2 * np.pi * df.index.hour / 24)
df['saat_cos'] = np.cos(2 * np.pi * df.index.hour / 24)
df['hafta_gunu'] = df.index.dayofweek

data = df.dropna()
X = data.drop(columns='tuketim_mwh')
y = data['tuketim_mwh']
cut = int(len(data) * 0.8)

model = HistGradientBoostingRegressor(
    max_iter=200, learning_rate=0.05, random_state=42
)
model.fit(X.iloc[:cut], y.iloc[:cut])
pred = model.predict(X.iloc[cut:])
baseline = X.iloc[cut:]['lag_24']

print('Model MAE:', mean_absolute_error(y.iloc[cut:], pred))
print('Naif MAE:', mean_absolute_error(y.iloc[cut:], baseline))
```

`shift(1)` sayesinde hareketli ortalama hedef saatin tüketimini içermez. Veriyi rastgele karıştırmak yerine kronolojik bölüyoruz. Test özelliklerinde önceki saatlerin gerçek ölçümleri bulunduğundan bu değerlendirme, her saat yeni ölçüm geldikçe yapılan bir saat ileri tahminleri temsil eder; bütün test dönemini tek seferde öngörmez.

## Başarıyı ve belirsizliği ölçmek

Ortalama mutlak hata şu şekilde hesaplanır:

$$\mathrm{MAE}=\frac{1}{n}\sum_{i=1}^{n}\vert y_i-\hat{y}_i\vert $$

MAE, hatayı hedefle aynı birimde gösterir. Bunun yanında zirve saatlerinin hatası ayrıca izlenmelidir: Sessiz gecelerde başarılı olmak, yoğun akşamları kurtarmaya yetmez. Modeli kayan zaman pencereleriyle değerlendirmek de farklı mevsimlerdeki dayanıklılığını ortaya çıkarır.

Üretimde yalnızca tek sayı değil, tahmin aralığı sunmak değerlidir. Böylece işletmeci olası yüksek tüketim için rezerv ayırabilir. Yeni ölçümler geldikçe hata dağılımı takip edilmeli; tüketim alışkanlıkları değiştiğinde model yeniden eğitilmelidir. Akıllı şebekenin zekâsı, yalnızca tahmin yapmakta değil, ne zaman yanıldığını fark etmekte de saklıdır.

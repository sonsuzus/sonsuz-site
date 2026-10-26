---
layout: post
title: "Tarladan Algoritmaya: Tarımsal Verilerle Pazar Fiyatı Tahmini"
math: true
categories: 
  - Bilgi
tags: 
  - tarım
  - makine öğrenmesi
  - fiyat tahmini
  - zaman serisi
  - veri bilimi
  - python
toc: true
image: /img/tarladan-algoritmaya-tarimsal-17.png
---

![tarladan-algoritmaya-tarimsal-17](/img/tarladan-algoritmaya-tarimsal-17.svg)


Domatesin gelecek ay kaç liraya satılacağını bilmek, yalnızca pazarcıların değil; çiftçilerin, kooperatiflerin ve gıda şirketlerinin de hayalidir. Kesin bir cevap vermek mümkün olmasa da geçmiş hasat miktarı, talep, hava koşulları ve fiyat hareketleri kullanılarak geleceğe yönelik güçlü tahminler üretilebilir. Üstelik bu iş için kristal küre yerine veri bilimi yeterlidir.
``

## Fiyatı hangi değişkenler belirler?

Tarımsal ürün fiyatı, arz ve talebin kesiştiği noktada oluşur. Basitleştirilmiş biçimde arz artıp talep sabit kaldığında fiyat düşer; talep artıp arz sabit kaldığında ise fiyat yükselir. Ancak gerçek dünyada mazot maliyeti, döviz kuru, depolama kapasitesi, ithalat kararları ve mevsim etkisi de oyuna katılır.

Bir ürünün $t+1$ dönemindeki fiyatını şu fonksiyonla düşünebiliriz:

$$P_{t+1}=f(P_t,H_t,D_t,W_t,C_t,S_t)+e$$

Burada $P_t$ geçmiş fiyatı, $H_t$ hasat miktarını, $D_t$ talebi, $W_t$ hava koşullarını, $C_t$ üretim maliyetini ve $S_t$ mevsim bilgisini temsil eder. $e$ ise modelin açıklayamadığı beklenmedik olaylardır. Ani ihracat yasakları veya don felaketi gibi sürprizler bu terime saklanabilir.

| Veri | Fiyata olası etkisi | Örnek özellik |
|---|---|---|
| Hasat miktarı | Yüksek arz fiyatı düşürebilir | Aylık üretim tonu |
| Talep | Artış fiyatı yükseltebilir | Satış veya sipariş miktarı |
| Hava durumu | Verimi ve lojistiği etkiler | Yağış, sıcaklık, don günü |
| Maliyet | Taban fiyatı yukarı itebilir | Gübre, yakıt, işçilik |
| Mevsim | Düzenli dalgalanmaları açıklar | Ay, hafta, hasat dönemi |

## Geçmiş veri nasıl hazırlanır?

Ham kayıtları doğrudan modele vermek genellikle iyi sonuç üretmez. Eksik değerler tamamlanmalı, farklı kaynaklardaki tarihler eşleştirilmeli ve aşırı uçlar incelenmelidir. Örneğin kilogram ve ton değerlerinin aynı sütunda karışması, algoritmaya küçük çaplı bir matematik şakası yaptırır; fakat kimse gülmez.

Zaman serilerinde gecikmeli özellikler özellikle değerlidir. Geçen ayın fiyatı $P_{t-1}$, üç aylık ortalama ve geçen yılın aynı ayındaki fiyat modele eklenebilir. Ayrıca arz-talep oranı gibi türetilmiş bir değişken oluşturulabilir:

$$R_t=H_t/D_t$$

$R_t$ yükseldikçe piyasada ürün bolluğu bulunduğu düşünülebilir. Bununla birlikte bu ilişkinin her ürün için doğrusal olması beklenmemelidir.

## Hangi algoritma seçilmeli?

| Algoritma | Güçlü yanı | Sınırlaması |
|---|---|---|
| Doğrusal regresyon | Açıklanabilir ve hızlıdır | Karmaşık ilişkileri kaçırabilir |
| ARIMA | Zaman bağımlılığını modeller | Dış değişkenleri yönetmek zorlaşabilir |
| Random Forest | Doğrusal olmayan ilişkileri öğrenir | Zaman sırasını kendiliğinden anlamaz |
| XGBoost | Tablosal veride yüksek başarı sağlar | Ayar ve özellik mühendisliği ister |
| LSTM | Uzun dönem örüntülerini öğrenebilir | Çok veri ve hesaplama gücü gerektirir |

Başlangıç için doğrusal regresyon iyi bir referans modelidir. Ardından Random Forest veya XGBoost ile performans karşılaştırılabilir. Aşağıdaki Python örneği, gecikmeli fiyatlarla birlikte hasat ve talep verisini kullanır:

```python
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

veri = pd.read_csv('tarim_fiyatlari.csv', parse_dates=['tarih'])
veri = veri.sort_values('tarih')

# Geçmiş fiyatlardan tahmin edici özellikler oluşturur.
veri['fiyat_1_ay'] = veri['fiyat'].shift(1)
veri['fiyat_3_ay_ortalama'] = veri['fiyat'].shift(1).rolling(3).mean()
veri['arz_talep_orani'] = veri['hasat'] / veri['talep']
veri = veri.dropna()

ozellikler = ['hasat', 'talep', 'fiyat_1_ay',
              'fiyat_3_ay_ortalama', 'arz_talep_orani']

# Zaman sırasını koruyarak geçmişi eğitim, son dönemi test yapar.
sinir = int(len(veri) * 0.8)
egitim, test = veri.iloc[:sinir], veri.iloc[sinir:]

model = RandomForestRegressor(n_estimators=300, random_state=42)
model.fit(egitim[ozellikler], egitim['fiyat'])
tahmin = model.predict(test[ozellikler])

print('MAE:', mean_absolute_error(test['fiyat'], tahmin))
```

## Başarı nasıl ölçülür?

Ortalama mutlak hata, tahminlerin gerçek fiyattan ortalama sapmasını gösterir:

$$MAE=(1/n)\sum_{i=1}^{n}\vert y_i-p_i\vert $$

Zaman serilerinde veriyi rastgele karıştırmak geleceğin bilgisini geçmişe sızdırabilir. Bu nedenle test kümesi daima daha yeni tarihlerden seçilmelidir. Model yalnızca tek sayı üretmek yerine güven aralığı da sunmalıdır. Sonuçta fiyat tahmini kesin kehanet değil, belirsizlik altında karar desteğidir. Doğru kurulan bir sistem çiftçiye ekim planı, depolama zamanı ve satış stratejisi konusunda önemli bir pusula sağlayabilir.

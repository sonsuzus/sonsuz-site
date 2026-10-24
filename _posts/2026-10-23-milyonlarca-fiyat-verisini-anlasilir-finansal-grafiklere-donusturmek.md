---
layout: post
title: "Milyonlarca Fiyat Verisini Anlaşılır Finansal Grafiklere Dönüştürmek"
math: true
categories: 
  - Bilgi
tags: 
  - finansal veri
  - veri görselleştirme
  - python
  - zaman serisi
  - ohlc
  - performans
toc: true
image: /img/milyonlarca-fiyat-verisini-11.png
---

Finansal piyasalarda veri kıtlığı değil, veri bolluğu problemdir. Saniyede binlerce işlem gerçekleşirken birkaç aylık fiyat geçmişi bile milyonlarca satıra ulaşabilir. Bu verilerin tamamını tek bir grafiğe göndermek ise hem tarayıcıyı yorar hem de ortaya finansal analizden çok rengârenk bir ip yumağı çıkarır. İyi bir görselleştirme sistemi, veriyi yalnızca çizmez; zaman ölçeğine göre özetler, önemli hareketleri korur ve kullanıcıya doğru hikâyeyi anlatır.
``

## Önce verinin yapısını anlayalım

Finansal fiyat verileri çoğunlukla zaman serisi biçimindedir. Her kayıt bir zaman damgası, fiyat ve işlem hacmi içerir:

| Alan | Anlamı | Örnek |
|---|---|---|
| `timestamp` | İşlemin gerçekleştiği an | 10:31:05.120 |
| `price` | Gerçekleşen işlem fiyatı | 42,75 TL |
| `volume` | İşlem miktarı | 1.250 |

Ham işlemler, yani *tick* verileri, en ayrıntılı seviyedir. Fakat ekranda 1.500 piksel genişliğinde bir alan varken 10 milyon noktayı ayrı ayrı göstermek anlamsızdır. Bir piksele binlerce veri noktası düşer. Dolayısıyla temel hedefimiz şu olmalıdır:

$$gösterilen\_nokta\_sayısı \leq ekran\_genişliği \times k$$

Buradaki $k$, yakınlaştırma ve görsel kalite için seçilen küçük bir katsayıdır. Genellikle 1 ile 3 arasındaki değerler yeterlidir.

## OHLC ile finansal özeti korumak

Tick verilerini belirli zaman aralıklarında gruplayarak OHLC mumlarına dönüştürebiliriz. Her zaman kovası için dört değer hesaplanır:

- **Open:** İlk fiyat
- **High:** En yüksek fiyat
- **Low:** En düşük fiyat
- **Close:** Son fiyat

Bu yaklaşım yalnızca ortalama almaktan daha güvenlidir. Örneğin bir dakikadaki fiyatların ortalaması 100 TL olabilir; ancak fiyat aynı dakika içinde 90 TL'ye düşüp 110 TL'ye çıkmışsa ortalama bu oynaklığı gizler. OHLC ise hareketin menzilini korur:

$$Aralık = High - Low$$

| Yöntem | Avantaj | Dezavantaj | Uygun kullanım |
|---|---|---|---|
| Ham tick | En yüksek ayrıntı | Çok ağır ve karmaşık | Yakın inceleme |
| Ortalama | Basit ve hızlı | Ani hareketleri gizler | Genel eğilim |
| OHLC | Fiyat aralığını korur | Daha fazla alan ister | Mum grafikleri |
| LTTB | Görsel şekli korur | Finansal anlam taşımaz | Çizgi grafikleri |

## Python ile milyonları binlere indirmek

Pandas kullanarak işlemleri dakikalık mumlara dönüştürebiliriz:

```python
import pandas as pd

# Yalnızca gerekli sütunları okuyarak bellek tüketimini azaltırız.
df = pd.read_parquet(
    "prices.parquet",
    columns=["timestamp", "price", "volume"]
)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp").sort_index()

# Her dakika için fiyat özeti ve toplam işlem hacmi oluşturulur.
ohlc = df["price"].resample("1min").ohlc()
ohlc["volume"] = df["volume"].resample("1min").sum()
ohlc = ohlc.dropna()

print(ohlc.head())
```

Bu kod, milyonlarca işlemi birkaç bin anlamlı zaman kovasına indirir. Parquet biçimi sütun bazlı çalıştığı için CSV'ye göre daha hızlı okunur ve daha az disk alanı kullanır. `sort_index()` ise zaman sırası bozuk kayıtların yanlış mumlar üretmesini engeller.

## Her yakınlaştırma seviyesine ayrı veri

Profesyonel grafiklerde tek bir veri çözünürlüğü kullanılmaz. Kullanıcı yıllık görünümdeyken günlük mumlar, haftalık görünümde saatlik mumlar, yakınlaştığında ise dakikalık veya tick verileri sunulur. Bu yapıya çok çözünürlüklü veri piramidi denebilir.

Sunucu tarafında `1min`, `5min`, `1h` ve `1d` tabloları önceden hazırlanabilir. İstemci yalnızca görünür tarih aralığını ister. Böylece ağ üzerinden gereksiz veri taşınmaz. Veritabanında zaman damgası ve sembol üzerinde indeks bulunması da sorguları ciddi biçimde hızlandırır.

## Okunabilirlik performans kadar önemlidir

Grafikte eksen etiketlerini seyrekleştirmek, hacmi ayrı panelde göstermek ve yükseliş-düşüş renklerini tutarlı kullanmak gerekir. Logaritmik eksen, uzun dönemli karşılaştırmalarda özellikle yararlıdır; çünkü 10'dan 20'ye yükseliş ile 100'den 200'e yükselişi eşit, yani yüzde 100 değişim olarak gösterir.

Sonuçta başarılı finansal görselleştirme, bütün veriyi ekrana boca etmek değildir. Doğru çözünürlüğü seçmek, uç hareketleri korumak ve kullanıcı etkileşimine göre ayrıntı sunmaktır. Grafik sustuğunda değil, milyonlarca kaydın içinden önemli olanı konuştuğunda değerlidir.

![milyonlarca-fiyat-verisini-11](/img/milyonlarca-fiyat-verisini-11.svg)


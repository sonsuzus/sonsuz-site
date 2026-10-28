---
layout: post
title: "Algorithmic Trading: Algoritmalar Finansal Piyasalarda Nasıl İşlem Yapar?"
math: true
categories: 
  - Bilgi
tags: 
  - algorithmic trading
  - algoritma
  - finans
  - python
  - borsa
  - nicel analiz
toc: true
image: /img/algorithmic-trading-algoritmalar-14.png
---

Finansal piyasalarda fiyatlar saniyeler içinde değişirken insan gözü grafiklere, haberlere ve kahve fincanına aynı anda yetişemez. Algorithmic trading, yani algoritmik işlem, önceden tanımlanmış kuralları kullanarak piyasa verilerini analiz eden ve otomatik biçimde emir gönderen sistemlerin genel adıdır. Buradaki amaç geleceği sihirli şekilde bilmek değil; ölçülebilir bir fikri hızlı, tutarlı ve test edilebilir bir sürece dönüştürmektir.

``

## Temel çalışma mantığı

Bir işlem algoritması genellikle dört aşamadan oluşur: veri toplama, sinyal üretme, risk kontrolü ve emir yürütme. Sistem önce fiyat, işlem hacmi, emir defteri veya ekonomik gösterge gibi verileri alır. Ardından bu verilerden alım ya da satım sinyali çıkarır. Risk motoru pozisyon büyüklüğünü sınırlar; yürütme katmanı ise emri borsaya iletir.

Basit bir hareketli ortalama stratejisinde kısa dönem ortalaması uzun dönem ortalamasını geçtiğinde alım sinyali üretilebilir:

$$SMA_n(t)=\frac{1}{n}\sum_{i=0}^{n-1}P_{t-i}$$

Burada $P_t$ ilgili zamandaki fiyatı, $n$ ise incelenen dönem sayısını gösterir. Örneğin $SMA_{10} > SMA_{50}$ olduğunda algoritma yükseliş eğilimi varsayabilir. Ancak bu yalnızca bir hipotezdir; kesin kazanç garantisi değildir.

| Yaklaşım | Temel fikir | Güçlü yanı | Başlıca riski |
|---|---|---|---|
| Trend takibi | Mevcut yönün süreceğini varsayar | Güçlü trendlerde etkilidir | Yatay piyasada sık hata |
| Ortalama dönüş | Fiyatın ortalamaya yaklaşmasını bekler | Aşırı hareketleri değerlendirebilir | Yeni trendi yanlış yorumlayabilir |
| Arbitraj | Benzer varlıkların fiyat farkını kullanır | Piyasa yönüne daha az bağımlıdır | Fark çok hızlı kapanabilir |
| Piyasa yapıcılık | Alış ve satış fiyatı sunar | Fiyat farkından gelir hedefler | Envanter ve ani hareket riski |

## Sinyalden gerçek emre

Doğru sinyal üretmek tek başına yeterli değildir. Algoritma piyasa emri verdiğinde hızlı gerçekleşme elde eder, fakat beklenenden kötü bir fiyatla karşılaşabilir. Limit emri fiyatı kontrol eder, ancak hiç gerçekleşmeyebilir. Büyük emirler de piyasayı hareket ettirebilir. Bu nedenle bazı sistemler emri küçük parçalara ayırarak zamana yayar.

Gerçekleşme fiyatı ile karar anındaki beklenen fiyat arasındaki fark **kayma** olarak adlandırılır. Yaklaşık işlem sonucu şöyle modellenebilir:

$$Net\ Getiri = Brüt\ Getiri - Komisyon - Kayma - Vergiler$$

Kâğıt üzerinde başarılı görünen pek çok strateji, bu maliyetler eklendiğinde cazibesini kaybeder.

## Küçük bir Python örneği

Aşağıdaki kod, kısa ve uzun hareketli ortalamaları karşılaştırarak örnek sinyal üretir. Gerçek para ile emir göndermez; yalnızca stratejinin karar katmanını gösterir.

```python
import pandas as pd

def sinyal_uret(fiyatlar: pd.Series) -> pd.DataFrame:
    sonuc = pd.DataFrame({"fiyat": fiyatlar})
    sonuc["kisa_ortalama"] = fiyatlar.rolling(10).mean()
    sonuc["uzun_ortalama"] = fiyatlar.rolling(50).mean()

    sonuc["sinyal"] = 0
    sonuc.loc[
        sonuc["kisa_ortalama"] > sonuc["uzun_ortalama"], "sinyal"
    ] = 1
    sonuc.loc[
        sonuc["kisa_ortalama"] < sonuc["uzun_ortalama"], "sinyal"
    ] = -1

    return sonuc
```

Burada `1` alım yönünü, `-1` satış yönünü, `0` ise kararsız durumu temsil eder. Üretim ortamında veri eksikliği, bağlantı kopması, tekrar gönderilen emirler ve borsa reddi gibi durumlar ayrıca yönetilmelidir.

## Backtest neden yeterli değildir?

Backtest, stratejiyi geçmiş veriler üzerinde çalıştırır. Fakat geçmişte iyi görünen sonuçlar aşırı uyumdan kaynaklanabilir. Algoritma piyasa davranışını değil, veri setindeki tesadüfleri ezberlemiş olabilir.

| Test türü | Amaç |
|---|---|
| Eğitim dönemi | Kuralları ve parametreleri geliştirmek |
| Doğrulama dönemi | Parametre seçimini kontrol etmek |
| Test dönemi | Görülmemiş veride performansı ölçmek |
| Paper trading | Canlı piyasada sanal emirlerle denemek |

Risk yönetiminde maksimum pozisyon, günlük zarar limiti ve acil durdurma mekanizması bulunmalıdır. Sharpe oranı gibi ölçüler de getiri ile oynaklığı birlikte değerlendirir:

$$Sharpe=\frac{R_p-R_f}{\sigma_p}$$

Sonuç olarak algoritmik işlem; finans, istatistik, yazılım mühendisliği ve operasyon disiplininin birleşimidir. En iyi algoritma en karmaşık olan değil, varsayımları anlaşılır, maliyetleri gerçekçi ve risk sınırları açık olandır. Kod hızlı olabilir; fakat kontrolsüz risk ondan da hızlıdır. Bu içerik yatırım tavsiyesi değil, teknolojik sürecin eğitim amaçlı açıklamasıdır.

![algorithmic-trading-algoritmalar-14](/img/algorithmic-trading-algoritmalar-14.svg)


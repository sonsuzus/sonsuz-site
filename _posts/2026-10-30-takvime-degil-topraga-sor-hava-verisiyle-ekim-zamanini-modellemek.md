---
layout: post
title: "Takvime Değil Toprağa Sor: Hava Verisiyle Ekim Zamanını Modellemek"
math: true
categories: 
  - Proje
tags: 
  - tarım
  - iklim
  - python
  - veri bilimi
  - zaman serileri
  - karar destek
toc: true
image: /img/takvime-degil-topraga-31.png
---

Ekim tarihini yalnızca takvimden seçmek, pikniğe hava durumuna bakmadan çıkmaya benzer: Bazen şanslısınızdır, bazen bütün planınız çamura saplanır. Sıcaklık, yağış ve toprak nemini birlikte değerlendiren bir model, belirli bir bölge ve ürün için uygun ekim pencerelerini sıralayabilir. Üstelik başlangıç için devasa bir yapay zekâ sistemi gerekmez.
``

## Önce biyoloji, sonra algoritma

Tohumun çimlenmesi için yeterli sıcaklık, su ve oksijen gerekir. Soğuk toprak gelişimi yavaşlatırken aşırı ıslaklık havalanmayı azaltabilir. Don ise yeni çıkan bitkileri tehdit eder. Dolayısıyla amaç, yalnızca sıcak bir gün bulmak değil; ekimden sonraki hassas dönemi de değerlendirmektir.

Mısır üzerinden düşünelim. Örnekte üç günlük ortalama toprak sıcaklığının en az 10 °C olmasını isteyeceğiz. Bu değer evrensel bir reçete değildir: Çeşit, ekim derinliği, toprak yapısı ve yerel agronomik öneriler eşikleri değiştirebilir. Hava sıcaklığı da toprak sıcaklığının birebir karşılığı değildir; mümkünse ekim derinliğindeki ölçümler kullanılmalıdır.

Modelimiz iki aşamalıdır: Önce uygun olmayan tarihleri eler, ardından kalanları puanlar.

$$S(d)=0.50T(d)+0.30M(d)+0.20R(d)$$

Burada $T$ sıcaklık uygunluğunu, $M$ nem uygunluğunu, $R$ ise aşırı yağıştan kaçınma puanını temsil eder. Bütün puanlar 0–1 aralığındadır. Ağırlıklar şimdilik tasarım tercihidir; saha sonuçlarıyla kalibre edilmelidir. En yüksek puan, yalnızca değerlendirilen adaylar içindeki tercihimizdir.

## Hangi veriler gerekli?

Günlük toprak sıcaklığı, minimum hava sıcaklığı, yağış ve toprak nemini aynı tarih ekseninde birleştirin. Meteoroloji istasyonları, tarla sensörleri ve uygun grid verileri birlikte kullanılabilir. Ancak kilometrelerce uzaktaki bir istasyonun ölçümü, tarladaki mikroiklimi kusursuz temsil etmez.

Eksik günleri görünür tutun; yağış boşluklarını otomatik olarak sıfırla doldurmayın. Birimleri, saat dilimini ve günlük toplama yöntemini tutarlılaştırın. Ayrıca gözlem ile tahmini ayrı işaretleyin: Gelecek ekim günlerini değerlendirirken henüz bilinmeyen hava koşulları yerine tahminler kullanılmalıdır.

| Yaklaşım | Güçlü tarafı | Temel sınırlaması |
|---|---|---|
| Sabit tarih | Çok kolay uygulanır | Yıllar arasındaki farkı kaçırır |
| Eşik ve puanlama | Açıklanabilir, az veri ister | Yerel kalibrasyon gerektirir |
| Öğrenen model | Karmaşık ilişkileri yakalayabilir | Etiketli veri ve dikkatli doğrulama ister |

## Python ile aday tarihleri sıralamak

Aşağıdaki fonksiyon, günlük veriden üç günlük sıcaklık ve beş günlük yağış özetleri çıkarır. Ekim günü dahil yedi günlük don kontrolü yapar. `moisture`, hacimsel su içeriği değil, yerel olarak 0–1 aralığına normalleştirilmiş nem göstergesidir. Bütün eşikler yalnızca örnek amaçlıdır.

```python
import pandas as pd

def ekim_adaylari(df, adaylar):
    df = df.sort_index().asfreq('D').copy()
    df['soil3'] = df['soil_temp'].rolling(3).mean()
    df['rain5'] = df['rain'].rolling(5).sum()
    sonuclar = []

    for d in df.index.intersection(pd.DatetimeIndex(adaylar)):
        x = df.loc[d]
        don = df.loc[d:d + pd.Timedelta(days=6), 'air_min']
        if x[['soil3', 'rain5', 'moisture']].isna().any():
            continue
        if len(don) != 7 or don.isna().any():
            continue
        if x['soil3'] < 10 or don.min() <= 0:
            continue
        if not 0.35 <= x['moisture'] <= 0.75:
            continue

        T = min(1.0, (x['soil3'] - 10) / 4)
        M = max(0.0, 1 - abs(x['moisture'] - 0.55) / 0.25)
        R = max(0.0, 1 - x['rain5'] / 25)
        puan = 0.50 * T + 0.30 * M + 0.20 * R
        sonuclar.append((d, puan))

    return pd.DataFrame(
        sonuclar, columns=['tarih', 'puan']
    ).sort_values('puan', ascending=False)
```

Verinin indeksi günlük `DatetimeIndex` olmalıdır; yağış milimetre cinsindedir. Fonksiyon eksik pencereleri atlar. Sonuç boşsa sistem tarih uydurmaz: Mevcut bilgilerle uygun aday bulunmadığını bildirir. Yağış puanı basit bir aşırılık cezasıdır; drenajı veya su birikmesini doğrudan modellemez.

## Model gerçekten işe yarıyor mu?

Geçmiş yılları kronolojik olarak eğitim, kalibrasyon ve test dönemlerine ayırın. Rastgele satır bölmek, komşu günlerdeki benzerlik nedeniyle başarıyı olduğundan yüksek gösterebilir. Tarih önerilerini çıkış oranı, çıkış süresi ve mümkünse verim kayıtlarıyla değerlendirin; çiftçinin alışılmış ekim takvimini de karşılaştırma noktası yapın.

Geçmişte gerçekleşen geleceğin havasını kullanmak, operasyonel başarı için iyimser sonuç verir. Gerçekçi testte, karar anında yayımlanmış arşiv tahminleri tercih edilmelidir. Aynı tarlada farklı ekim tarihlerini karşılaştıran denemeler, önerinin etkisini anlamayı kolaylaştırır.

## Tek gün yerine karar penceresi

Tahminler belirsizdir. Farklı hava senaryolarında modeli tekrar çalıştırıp hangi tarihlerin sürekli üst sıralarda kaldığını inceleyin. Böylece tek bir “sihirli salı” yerine birkaç günlük dayanıklı bir pencere elde edersiniz. Son karar; tarla erişimi, iş gücü, makine durumu ve yerel uzman görüşüyle birleştirilmelidir. Model çiftçinin yerine geçmez; takvim sohbetine veriyle katılır.

![takvime-degil-topraga-31](/img/takvime-degil-topraga-31.svg)


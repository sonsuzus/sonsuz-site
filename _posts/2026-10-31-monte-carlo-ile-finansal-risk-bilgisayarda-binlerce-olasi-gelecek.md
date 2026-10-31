---
layout: post
title: "Monte Carlo ile Finansal Risk: Bilgisayarda Binlerce Olası Gelecek"
math: true
categories: 
  - Bilgi
tags: 
  - monte carlo
  - finansal risk
  - python
  - simülasyon
  - var
  - olasılık
toc: true
image: /img/monte-carlo-ile-24.png
---

Yarın piyasa yükselir mi, düşer mi? Tek bir tahmin üretmek yerine yüz bin farklı yarın hayal ettiğinizi düşünün. Monte Carlo simülasyonu tam olarak bunu yapar: Belirsizliği rastgele örneklerle temsil eder, olası sonuçları hesaplar ve riskin dağılımını görünür kılar. Elimizde kristal küre yoktur; fakat oldukça çalışkan bir bilgisayar vardır.

![monte-carlo-ile-24](/img/monte-carlo-ile-24.svg)

``

## Rastgelelik neden işe yarıyor?

Monte Carlo’nun temel fikri, hesaplanması zor bir dağılımı çok sayıda örnekle yaklaşık olarak keşfetmektir. Her senaryo, seçtiğimiz modelin ürettiği olası bir gelecektir. Senaryoların sonunda portföy değerlerini sıralayarak kayıpların ne kadar büyük olabileceğini inceleriz.

Buradaki kritik ayrım şudur: **Rastgele sayı üretmek, doğru piyasa modeli kurmakla aynı şey değildir.** Yanlış varsayımlardan üretilen milyonlarca senaryo, yalnızca yanlışlığı daha hassas hesaplar.

Basit bir başlangıç modeli geometrik Brown hareketidir. Bu modelde gelecekteki fiyat şöyle yazılır:

$$S_T=S_0 e^{(\mu-\sigma^2/2)T+\sigma\sqrt{T}Z},\qquad Z\sim\mathcal{N}(0,1).$$

Burada $S_0$ başlangıç fiyatı, $\mu$ yıllık beklenen getiri parametresi, $\sigma$ yıllık volatilite, $T$ ise yıl cinsinden süredir. Normal dağılımlı değişken fiyatın kendisini değil, logaritmik getirisini etkiler; böylece fiyatlar pozitif kalır.

Bu yaklaşım anlaşılırdır, ancak sabit volatilite ve normal logaritmik getiriler gibi güçlü varsayımlar taşır. Gerçek piyasalardaki sıçramaları ve kalın kuyrukları eksik temsil edebilir.

## İki varlıkla küçük bir risk laboratuvarı

Bir milyon liralık portföyün yüzde 60’ını birinci, yüzde 40’ını ikinci varlığa ayıralım. Ufkumuz on işlem günü olsun. İki varlık tamamen bağımsız hareket etmediği için korelasyonu da modele eklemeliyiz.

Aşağıdaki NumPy kodu, Cholesky ayrıştırmasıyla ilişkili normal örnekler üretir. Ardından her senaryoda dönem sonu portföy değerini ve kaybı hesaplar:

```python
import numpy as np

rng = np.random.default_rng(42)
n = 100_000
T = 10 / 252
initial = 1_000_000
weights = np.array([0.60, 0.40])
mu = np.array([0.08, 0.10])
sigma = np.array([0.20, 0.30])
corr = np.array([[1.0, 0.4], [0.4, 1.0]])

chol = np.linalg.cholesky(corr)
z = rng.standard_normal((n, 2)) @ chol.T

multipliers = np.exp(
    (mu - 0.5 * sigma**2) * T
    + sigma * np.sqrt(T) * z
)
terminal_values = initial * (multipliers @ weights)
losses = initial - terminal_values

var99 = np.quantile(losses, 0.99)
es99 = losses[losses >= var99].mean()

print(f"%99 VaR: {var99:,.0f} TL")
print(f"%99 ES: {es99:,.0f} TL")
```

Sabit tohum, sonuçların tekrar üretilebilmesini sağlar. Cholesky dönüşümü, bağımsız çekilişleri hedef korelasyona sahip şoklara dönüştürür. Kullanılan korelasyon matrisinin pozitif tanımlı olması gerekir.

Kod, başlangıçta alınan varlıkların elde tutulduğunu varsayar; günlük yeniden dengeleme yapmaz. Ayrıca bütün fiyat yollarını değil, doğrudan dönem sonunu örnekler. Bu model altında dönem sonu riski için yeterlidir; bariyer opsiyonları veya dönem içindeki maksimum kayıp gibi yola bağlı ölçüler için zaman adımları gerekir. Parametreler örnektir; yatırım önerisi değildir.

## VaR ve ES bize ne söylüyor?

Kaybı $L=V_0-V_T$ olarak tanımlıyoruz. Pozitif değer zarar, negatif değer kazanç demektir. Yüzde 99 VaR, kayıp dağılımının yüzde 99’luk kantilidir:

$$\operatorname{VaR}_{0.99}(L)=q_{0.99}(L).$$

Örneğin VaR 80 bin lira çıkarsa, modeldeki on günlük kayıpların yaklaşık yüzde 99’u bu eşiği aşmaz. Bu, kalan yüzde 1’de ne olacağını söylemez ve gerçek dünyaya verilmiş bir garanti değildir.

| Ölçü | Yanıtladığı soru | Sınırı |
|---|---|---|
| VaR | Kayıp eşiği nerede? | Eşiğin ötesini özetlemez |
| ES | En kötü yüzde 1’de ortalama kayıp ne? | Kuyruk modeline duyarlıdır |
| Standart sapma | Sonuçlar ne kadar dağınık? | Kazanç ve kaybı birlikte ölçer |

Kodda ES, eşik üzerindeki kayıpların ortalamasıdır. Bu sürekli dağılım örneğinde, felaket mahallesinin ortalama faturasını gösterir.

## Simülasyonu gerçekçilikle terbiye etmek

Volatiliteyi geçmiş verilerden tahmin ederken veri sıklığını ve yıllıklaştırmayı tutarlı seçin. Buradaki $\mu$, gerçek dünya risk analizi içindir; opsiyon fiyatlamasındaki risksiz faiz parametresiyle otomatik olarak değiştirilmemelidir.

Korelasyonların krizlerde yükselebileceğini ayrıca sınayın. Volatiliteyi ikiye katlayıp korelasyonu 0.95 yaparak sonuçları karşılaştırmak, modelin hassasiyetini gösteren basit bir stres denemesidir; krizi eksiksiz temsil etmez.

Senaryo sayısını artırmak örnekleme hatasını azaltır. Düzenli koşullarda standart hatalar kabaca $1/\sqrt{N}$ ölçeğinde küçülür; fakat model hatası ortadan kalkmaz. Farklı tohumlarla tekrarlama, kuyruk örnek sayısını kontrol etme ve geçmiş gerçekleşmelerle geriye dönük sınama bu yüzden önemlidir.

Monte Carlo geleceği bilmez. Daha faydalı bir iş yapar: Varsayımlarınızın hangi geleceklerde canınızı yakabileceğini gösterir. Risk yönetimi de tam burada, güzel görünen ortalamaların arkasındaki tatsız sürprizleri sorgulayarak başlar.

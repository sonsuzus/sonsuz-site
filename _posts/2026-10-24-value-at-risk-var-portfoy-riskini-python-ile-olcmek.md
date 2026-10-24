---
layout: post
title: "Value at Risk (VaR): Portföy Riskini Python ile Ölçmek"
math: true
categories: 
  - Program
tags: 
  - var
  - python
  - finans
  - risk yönetimi
  - portföy
  - numpy
toc: true
image: /img/value-at-risk-30.png
---

Bir yatırım portföyü bugün sakin görünebilir; ancak yarın piyasalar küçük bir korku filmi çekmeye karar verebilir. Value at Risk, yani VaR, belirli bir zaman aralığında ve güven düzeyinde portföyün karşılaşabileceği kaybı tek bir sayıyla özetler. Bu yazıda VaR’ın mantığını kuracak, yöntemleri karşılaştıracak ve Python ile hesaplama yapacağız.

![value-at-risk-30](/img/value-at-risk-30.svg)

``

## VaR tam olarak ne söyler?

VaR üç bileşene dayanır: portföy değeri, zaman ufku ve güven düzeyi. Örneğin günlük %95 güven düzeyinde VaR değeri 20.000 TL ise ifade şu anlama gelir:

> Normal piyasa koşulları altında, portföyün bir günlük kaybının %95 olasılıkla 20.000 TL’yi aşmaması beklenir.

Bunun tersinden söylenmesi daha öğreticidir: Günlerin yaklaşık %5’inde kayıp 20.000 TL’den büyük olabilir. VaR, oluşabilecek en yüksek kaybı söylemez. Kuyruğun başladığı eşiği gösterir; kuyruğun ne kadar korkutucu olduğunu ise tek başına açıklamaz.

Getiri $R$ ve güven düzeyi $c$ olmak üzere VaR, getiri dağılımının sol kuyruğundaki kantil üzerinden tanımlanabilir:

$$VaR_c = -V_0 Q_{1-c}(R)$$

Burada $V_0$ portföyün bugünkü değeri, $Q_{1-c}$ ise getirilerin $(1-c)$ kantilidir. Eksi işareti, negatif getiriyi pozitif bir kayıp tutarı olarak sunar.

## Başlıca hesaplama yöntemleri

| Yöntem | Temel varsayım | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| Tarihsel VaR | Geçmiş geleceği temsil eder | Basit ve dağılımdan bağımsızdır | Geçmişte görülmeyen şoku yakalayamaz |
| Parametrik VaR | Getiriler genellikle normal dağılır | Hızlı ve hesaplaması kolaydır | Kalın kuyrukları küçümseyebilir |
| Monte Carlo VaR | Seçilen modele göre senaryo üretilir | Karmaşık portföylere uygulanabilir | Model ve işlem maliyeti yüksektir |

Parametrik yöntemde ortalama getiri $\mu$, standart sapma $\sigma$ ve standart normal dağılımın kritik değeri $z_{1-c}$ kullanılır:

$$VaR_c = -V_0(\mu + z_{1-c}\sigma)$$

%95 güven düzeyinde sol kuyruk değeri yaklaşık $z_{0.05}=-1.645$ olur. Volatilite yükseldikçe VaR da büyür; başka bir deyişle portföyün kalp atışları hızlandıkça risk göstergesi kırmızıya yaklaşır.

## Python ile tarihsel ve parametrik VaR

Aşağıdaki örnek, günlük portföy getirilerinden iki farklı VaR tahmini üretir. Gerçek bir uygulamada `returns` dizisi, portföy bileşenlerinin ağırlıklı getirilerinden veya portföy değer serisinden hesaplanmalıdır.

```python
import numpy as np
from scipy.stats import norm

# Örnek günlük portföy getirileri
returns = np.array([
    0.004, -0.012, 0.006, -0.021, 0.003,
    -0.008, 0.011, -0.017, 0.002, -0.005
])

portfolio_value = 1_000_000
confidence = 0.95

# Sol kuyruktaki %5 kantilini bulur.
historical_quantile = np.quantile(returns, 1 - confidence)
historical_var = -portfolio_value * historical_quantile

# Ortalama ve volatiliteyle normal dağılım yaklaşımı kurar.
mu = returns.mean()
sigma = returns.std(ddof=1)
z_score = norm.ppf(1 - confidence)
parametric_var = -portfolio_value * (mu + z_score * sigma)

print(f"Tarihsel VaR: {historical_var:,.2f} TL")
print(f"Parametrik VaR: {parametric_var:,.2f} TL")
```

Tarihsel yöntemde `np.quantile`, gözlemlerin en kötü %5’lik bölümünün başladığı noktayı belirler. Parametrik yöntemde ise `norm.ppf`, seçilen güven düzeyine karşılık gelen kritik değeri verir. Veri sayısı az olduğunda her iki sonuç da oynak olabilir; yüzlerce veya binlerce günlük gözlem daha anlamlıdır.

## Zaman ufku ve VaR’ın sınırları

Bağımsız ve benzer dağılan getiriler varsayılırsa günlük VaR, karekök-zaman kuralıyla yaklaşık olarak ölçeklenebilir:

$$VaR_T \approx VaR_1\sqrt{T}$$

Örneğin 10 günlük VaR yaklaşık olarak günlük VaR’ın $\sqrt{10}$ katıdır. Fakat kriz dönemlerinde getiriler bağımsız davranmayabilir ve volatilite kümelenebilir. Bu nedenle formül mekanik biçimde kullanılmamalıdır.

VaR ayrıca eşik sonrasındaki kaybı açıklamadığı için Expected Shortfall ile desteklenmelidir. Expected Shortfall, VaR aşıldığında ortalama kaybı ölçer. Sağlam bir risk sistemi; geriye dönük testler, stres senaryoları ve farklı güven düzeyleriyle sonuçları sınamalıdır. VaR kullanışlı bir pusuladır, fakat finansal fırtınalarda haritanın tamamı değildir.

---
layout: post
title: "Markowitz Modeliyle Portföy Optimizasyonu: Risk ve Getiriyi Kodla Dengelemek"
math: true
categories: 
  - Program
tags: 
  - portföy optimizasyonu
  - markowitz modeli
  - python
  - finans
  - risk yönetimi
  - scipy
toc: true
image: /img/markowitz-modeliyle-portfoy-49.png
---

Yatırım dünyasında herkes yüksek getiri ister; fakat kimse geceleri portföyünün eridiğini düşünerek uyanmak istemez. Markowitz modeli, bu iki isteği matematiksel bir çerçevede buluşturur. Modelin temel sorusu şudur: Belirli bir getiri düzeyine ulaşırken riski nasıl en aza indirebiliriz? Gelin modern portföy teorisinin kalbine inip bu problemi Python ile çözelim.

``

## Markowitz modelinin temel fikri

Harry Markowitz tarafından geliştirilen modern portföy teorisi, yatırım araçlarını yalnızca tek tek değerlendirmez. Varlıkların birbirleriyle nasıl hareket ettiğini de hesaba katar. Çünkü iki riskli varlık, fiyatları farklı yönlerde hareket ediyorsa birlikte daha dengeli bir portföy oluşturabilir.

Bir portföyde $n$ adet varlık bulunduğunu düşünelim. Her varlığa ayrılan oranı $w_i$ ile gösterirsek ağırlıkların toplamı genellikle şöyle sınırlandırılır:

$$
\sum_{i=1}^{n} w_i = 1
$$

Açığa satışa izin verilmiyorsa ayrıca $w_i \geq 0$ koşulu uygulanır. Portföyün beklenen getirisi:

$$
E(R_p) = \mathbf{w}^T\boldsymbol{\mu}
$$

Portföy riski, yani varyansı ise kovaryans matrisi kullanılarak hesaplanır:

$$
\sigma_p^2 = \mathbf{w}^T\Sigma\mathbf{w}
$$

Burada $\boldsymbol{\mu}$ beklenen getiriler vektörü, $\Sigma$ kovaryans matrisi ve $\mathbf{w}$ portföy ağırlıklarıdır. Standart sapma için varyansın karekökü alınır.

| Kavram | Ne anlatır? | Portföydeki etkisi |
|---|---|---|
| Beklenen getiri | Geçmiş veya tahmini ortalama kazanç | Yükseldikçe kazanç potansiyeli artar |
| Varyans | Getirilerin ortalamadan sapması | Yüksekse belirsizlik büyür |
| Kovaryans | İki varlığın birlikte hareketi | Düşük veya negatifse çeşitlendirme sağlar |
| Ağırlık | Varlığa ayrılan sermaye oranı | Risk-getiri profilini belirler |

## Python ile minimum varyanslı portföy

Aşağıdaki örnekte yıllık beklenen getirileri ve kovaryans matrisini doğrudan tanımlıyoruz. Gerçek projelerde bunlar günlük fiyat verilerinden hesaplanabilir.

```python
import numpy as np
from scipy.optimize import minimize

returns = np.array([0.12, 0.18, 0.10, 0.15])

covariance = np.array([
    [0.040, 0.010, 0.008, 0.012],
    [0.010, 0.090, 0.006, 0.020],
    [0.008, 0.006, 0.025, 0.009],
    [0.012, 0.020, 0.009, 0.060]
])

asset_count = len(returns)
initial_weights = np.ones(asset_count) / asset_count

def portfolio_variance(weights):
    return weights.T @ covariance @ weights

constraints = [
    {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
]

bounds = [(0, 1)] * asset_count

result = minimize(
    portfolio_variance,
    initial_weights,
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

weights = result.x
portfolio_return = weights @ returns
portfolio_risk = np.sqrt(portfolio_variance(weights))

print('Ağırlıklar:', np.round(weights, 3))
print('Beklenen getiri:', round(portfolio_return, 3))
print('Risk:', round(portfolio_risk, 3))
```

`portfolio_variance` fonksiyonu optimizasyonun küçültmeye çalıştığı hedefi temsil eder. `constraints`, sermayenin tamamının kullanılmasını; `bounds` ise hiçbir varlığın negatif ağırlık almamasını sağlar. SLSQP algoritması, eşitlik ve sınır koşulları içeren bu tür problemlerde oldukça kullanışlıdır.

## Hedef getiri ve etkin sınır

Minimum varyanslı portföy güvenlidir; ancak beklenen getirisi yatırımcı için yetersiz kalabilir. Örneğin en az %14 getiri istiyorsak ikinci bir koşul ekleyebiliriz:

```python
target_return = 0.14
constraints.append({
    'type': 'eq',
    'fun': lambda w: w @ returns - target_return
})

result = minimize(
    portfolio_variance,
    initial_weights,
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)
```

Farklı hedef getiriler için optimizasyonu tekrarladığımızda **etkin sınır** ortaya çıkar. Bu eğri üzerindeki her portföy, aynı getiri seviyesindeki alternatiflerden daha düşük riske sahiptir.

| Yaklaşım | Amaç | Uygun yatırımcı profili |
|---|---|---|
| Minimum varyans | Riski mümkün olduğunca azaltmak | Temkinli |
| Hedef getirili optimizasyon | Belirli getiride en düşük riski bulmak | Dengeli |
| Maksimum Sharpe oranı | Risk başına getiriyi artırmak | Performans odaklı |

Markowitz modeli güçlüdür ama kusursuz değildir: geçmiş getirilerin geleceği temsil ettiği, korelasyonların sabit kaldığı ve işlem maliyetlerinin önemsiz olduğu varsayılır. Bu nedenle sonuçları kesin reçete değil, karar destek aracı olarak görmek gerekir. Sağlam veri, periyodik yeniden dengeleme ve ağırlık sınırları eklendiğinde model, portföyünüz için matematik bilen bir yardımcı pilota dönüşebilir.

![markowitz-modeliyle-portfoy-49](/img/markowitz-modeliyle-portfoy-49.svg)


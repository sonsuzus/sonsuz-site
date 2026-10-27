---
layout: post
title: "Robo-Advisor Algoritmaları: Portföyünüzü Yazılıma Emanet Eder misiniz?"
math: true
categories: 
  - Bilgi
tags: 
  - robo-advisor
  - algoritma
  - yatırım
  - portföy yönetimi
  - finansal teknoloji
  - python
toc: true
image: /img/robo-advisor-algoritmalari-59.png
---

Bir yatırım portföyünü yönetmek; varlık seçimi, risk analizi, düzenli dengeleme ve duyguları kontrol altında tutma gibi zor görevler içerir. Robo-advisor sistemleri bütün bunları takım elbiseli bir portföy yöneticisi yerine algoritmalarla gerçekleştirmeyi amaçlar. Peki yazılım piyasadaki fırtınalarda soğukkanlı kalabilir mi, yoksa yalnızca daha hızlı hata yapan bir hesap makinesi midir?

``

## Robo-advisor tam olarak nedir?

Robo-advisor, yatırımcının hedeflerini ve risk toleransını öğrenerek otomatik biçimde portföy oluşturan dijital yatırım hizmetidir. Kullanıcı genellikle yaşı, geliri, yatırım süresi, kayıp karşısındaki tutumu ve finansal hedefleri hakkında bir anket doldurur. Algoritma bu cevapları sayısal bir risk profiline dönüştürür.

Sistem daha sonra hisse senedi, tahvil, emtia veya para piyasası fonları gibi varlık sınıfları arasında dağılım yapar. Pek çok servis, düşük maliyetli ve çeşitlendirilmiş ETF’leri tercih eder. Buradaki amaç “gelecek ay uçacak hisseyi” bulmak değil, belirli bir risk düzeyinde tutarlı bir portföy kurmaktır.

## Matematik motor kaputunun altında

Robo-advisor algoritmalarının klasik temeli, Harry Markowitz’in modern portföy teorisidir. Bir portföyün beklenen getirisi, varlıkların beklenen getirilerinin ağırlıklı toplamıdır:

$$E(R_p) = \sum_{i=1}^{n} w_i E(R_i)$$

Burada $w_i$, ilgili varlığın portföydeki oranıdır. Ancak getiri tek başına yeterli değildir; varlıkların birlikte nasıl hareket ettiği de önemlidir. Portföy riski kovaryans matrisiyle hesaplanabilir:

$$\sigma_p^2 = \mathbf{w}^T \Sigma \mathbf{w}$$

İki varlık her zaman aynı yönde hareket etmiyorsa çeşitlendirme toplam riski azaltabilir. Algoritma, ağırlıkların toplamı $1$ olacak şekilde beklenen getiri ile risk arasında uygun dengeyi arar. Bazı sistemler ortalama-varyans optimizasyonu yerine Black-Litterman, risk parity veya Monte Carlo simülasyonu kullanır.

| Yaklaşım | Güçlü tarafı | Zayıf tarafı |
|---|---|---|
| Ortalama-varyans | Anlaşılır ve ölçülebilir | Geçmiş verilere hassastır |
| Risk parity | Riski daha dengeli dağıtır | Getiri beklentisini geri plana atabilir |
| Black-Litterman | Piyasa ile yatırımcı görüşünü birleştirir | Model kurulumu daha karmaşıktır |
| Monte Carlo | Çok sayıda gelecek senaryosu üretir | Varsayımlar yanlışsa sonuç yanıltıcıdır |

![robo-advisor-algoritmalari-59](/img/robo-advisor-algoritmalari-59.svg)


## Basit bir optimizasyon örneği

Aşağıdaki Python kodu, üç varlık arasında hedef getiriye yaklaşırken portföy riskini küçültür:

```python
import numpy as np
from scipy.optimize import minimize

returns = np.array([0.10, 0.06, 0.03])
covariance = np.array([
    [0.040, 0.006, 0.002],
    [0.006, 0.015, 0.003],
    [0.002, 0.003, 0.005]
])

def portfolio_risk(weights):
    return weights @ covariance @ weights

constraints = [
    {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
    {'type': 'eq', 'fun': lambda w: w @ returns - 0.07}
]

result = minimize(
    portfolio_risk,
    x0=np.array([1/3, 1/3, 1/3]),
    bounds=[(0, 1)] * 3,
    constraints=constraints
)

print(result.x)
```

İlk kısıt, sermayenin tamamının dağıtılmasını sağlar. İkinci kısıt ise beklenen getiriyi yüzde 7’ye sabitler. `minimize` fonksiyonu bu koşullar altında en düşük teorik riski veren ağırlıkları arar. Gerçek sistemlerde vergi, işlem maliyeti, likidite ve düzenleyici sınırlar da modele eklenir.

## Algoritma insanı yenebilir mi?

| Robo-advisor | İnsan danışman |
|---|---|
| Düşük maliyetle sürekli çalışır | Karmaşık ihtiyaçları yorumlayabilir |
| Panikle satış yapmaz | Kriz anında psikolojik destek verebilir |
| Kuralları tutarlı uygular | Olağan dışı koşullara esnek yaklaşabilir |
| Verideki hataları sorgulamayabilir | Önyargılı ve duygusal davranabilir |

Robo-advisor sistemlerinin en yararlı özelliklerinden biri otomatik yeniden dengelemedir. Örneğin hedef dağılım yüzde 60 hisse ve yüzde 40 tahvilken hisseler yükselip oran yüzde 70’e ulaştığında algoritma bir miktar hisse satıp tahvil alabilir. Böylece yatırımcı, yükseleni sonsuza kadar kovalamak yerine başlangıçtaki risk planına döner.

## Son karar

Yazılım, standart hedeflere sahip ve uzun vadeli yatırım yapan kişiler için portföyü başarıyla yönetebilir. Fakat algoritma geleceği bilmez; yalnızca veri, varsayım ve kurallar üzerinden karar verir. Miras planlaması, değişken gelir, büyük vergi yükümlülükleri veya panik davranışı gibi karmaşık durumlarda insan uzman hâlâ değerlidir. En güçlü model, otomasyonun disipliniyle insan muhakemesini birleştiren hibrit yaklaşımdır. Kısacası robot direksiyonu tutabilir, ancak rotanın gerçekten size ait olduğundan emin olmak hâlâ sizin görevinizdir.

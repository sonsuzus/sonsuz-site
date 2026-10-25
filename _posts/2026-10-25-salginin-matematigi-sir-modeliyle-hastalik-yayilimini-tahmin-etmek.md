---
layout: post
title: "Salgının Matematiği: SIR Modeliyle Hastalık Yayılımını Tahmin Etmek"
math: true
categories: 
  - Bilgi
tags: 
  - sir modeli
  - matematiksel modelleme
  - epidemiyoloji
  - python
  - simülasyon
  - veri bilimi
toc: true
image: /img/salginin-matematigi-sir-16.png
---

Bir salgının geleceğini tahmin etmek, kristal küreye bakmaktan çok daha sistematik bir iştir. Matematiksel modeller; bulaşma hızı, iyileşme süresi ve duyarlı nüfus gibi değişkenleri kullanarak vaka sayılarının zaman içinde nasıl değişebileceğini gösterir. Bu modellerin en tanınmış örneklerinden biri olan SIR, karmaşık bir toplumsal olayı üç temel nüfus grubuyla açıklamaya çalışır.

``

## SIR modeli nedir?

SIR adı, modeldeki üç grubun İngilizce adlarının baş harflerinden gelir:

- **S — Susceptible:** Hastalığa yakalanabilecek duyarlı kişiler.
- **I — Infectious:** Hastalığı taşıyan ve başkalarına bulaştırabilen kişiler.
- **R — Recovered:** İyileşen, bağışıklık kazanan veya bulaştırıcılığı sona eren kişiler.

Kapalı bir toplumda toplam nüfusun sabit olduğu varsayılır:

$$N = S(t) + I(t) + R(t)$$

Buradaki $t$ zamanı, $N$ ise toplam nüfusu temsil eder. Model; doğum, göç ve doğal ölüm gibi değişimleri genellikle hesaba katmaz. Başka bir deyişle matematik, işe önce masayı sadeleştirerek başlar.

| Grup | Sisteme giriş nedeni | Sistemden çıkış nedeni |
|---|---|---|
| Duyarlı $S$ | Başlangıç nüfusu | Enfekte olmak |
| Enfekte $I$ | Bulaşıcı kişiyle temas | İyileşmek veya bulaştırıcılığı kaybetmek |
| İyileşen $R$ | Hastalığı atlatmak | Temel SIR modelinde çıkış yoktur |

## Modelin matematiksel motoru

SIR modeli üç diferansiyel denklemle çalışır:

$$dS/dt = -βSI/N$$

$$dI/dt = βSI/N - γI$$

$$dR/dt = γI$$

Burada $β$, hastalığın etkili temas yoluyla bulaşma hızını; $γ$ ise iyileşme hızını ifade eder. Ortalama bulaşıcı kalma süresi $D$ günse yaklaşık olarak $γ = 1/D$ kabul edilir.

İlk denklem, duyarlı kişilerin enfekte oldukça azaldığını söyler. İkinci denklemde enfekte grubuna yeni vakalar eklenirken iyileşenler çıkarılır. Son denklem ise iyileşen grubunun hangi hızla büyüdüğünü gösterir. Böylece model, nüfusu bölmeler arasında akan bir sıvı gibi ele alır.

Salgının büyüyüp büyümeyeceğini anlamak için temel üreme sayısı kullanılır:

$$R_0 = β/γ$$

| $R_0$ değeri | Beklenen davranış |
|---|---|
| $R_0 < 1$ | Salgın zamanla küçülür |
| $R_0 = 1$ | Vaka sayısı yaklaşık sabit kalır |
| $R_0 > 1$ | Salgın başlangıçta büyür |

Örneğin $β = 0.30$ ve $γ = 0.10$ ise $R_0 = 3$ olur. Bu, tamamen duyarlı bir toplumda her enfekte kişinin ortalama üç yeni enfeksiyon oluşturabileceği anlamına gelir. Ancak duyarlı nüfus azaldıkça etkili üreme sayısı da düşer:

$$R_t = R_0 S(t)/N$$

## Python ile basit bir simülasyon

Aşağıdaki kod, denklemleri küçük zaman adımlarıyla yaklaşık olarak çözer. Euler yöntemi kullanılan bu yaklaşım eğitim için yeterlidir; ciddi epidemiyolojik analizlerde daha gelişmiş çözücüler tercih edilir.

```python
import numpy as np
import matplotlib.pyplot as plt

N = 100_000
beta = 0.30
gamma = 0.10
days = 160

S, I, R = np.zeros(days), np.zeros(days), np.zeros(days)
S[0], I[0], R[0] = N - 10, 10, 0

for t in range(days - 1):
    new_infections = beta * S[t] * I[t] / N
    new_recoveries = gamma * I[t]

    S[t + 1] = S[t] - new_infections
    I[t + 1] = I[t] + new_infections - new_recoveries
    R[t + 1] = R[t] + new_recoveries

plt.plot(S, label='Duyarlı')
plt.plot(I, label='Enfekte')
plt.plot(R, label='İyileşen')
plt.xlabel('Gün')
plt.ylabel('Kişi sayısı')
plt.legend()
plt.show()
```

Grafikte enfekte kişi sayısı önce yükselir, bir zirveye ulaşır ve ardından düşer. Zirvenin zamanı ve yüksekliği, sağlık sisteminin ihtiyaç duyabileceği yatak veya personel kapasitesini tahmin etmeye yardımcı olur.

## Güçlü ama kusursuz değil

Temel SIR modeli herkesin eşit sıklıkta temas ettiğini, bağışıklığın kaybolmadığını ve bulaşma hızının sabit kaldığını varsayar. Oysa yaş, konum, davranış değişiklikleri, aşılar ve yeni varyantlar sonucu etkiler. Bu nedenle model bir kehanet makinesi değil, farklı senaryoları karşılaştıran matematiksel bir laboratuvardır. Doğru verilerle güncellendiğinde salgının yönünü anlamayı ve müdahalelerin olası etkisini ölçmeyi sağlayan güçlü bir pusulaya dönüşür.

![salginin-matematigi-sir-16](/img/salginin-matematigi-sir-16.svg)


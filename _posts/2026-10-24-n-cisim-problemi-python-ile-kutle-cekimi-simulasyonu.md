---
layout: post
title: "N-Cisim Problemi: Python ile Kütle Çekimi Simülasyonu"
math: true
categories: 
  - Proje
tags: 
  - n-cisim
  - python
  - fizik
  - simülasyon
  - kütle-çekimi
  - sayısal-analiz
toc: true
image: /img/n-cisim-problemi-71.png
---

![n-cisim-problemi-71](/img/n-cisim-problemi-71.svg)


Gökyüzündeki hareketler ilk bakışta kusursuz bir saat mekanizması gibi görünür. Ancak sisteme üçüncü bir gök cismi eklendiğinde işler hızla kozmik bir bilardo masasına dönüşür! N-cisim problemi; yıldızların, gezegenlerin veya galaksilerin karşılıklı kütle çekimi altında nasıl hareket ettiğini bulmayı amaçlar. Genel bir analitik çözümü bulunmadığından bilgisayarlarla küçük zaman adımları hâlinde yaklaşık sonuçlar hesaplarız.

``

## Newton’dan simülasyona

İki cismin arasındaki çekim kuvveti Newton yasasıyla hesaplanır:

$$F = G\frac{m_1m_2}{r^2}$$

Burada $G$ kütle çekim sabiti, $m_1$ ve $m_2$ kütleler, $r$ ise cisimler arasındaki uzaklıktır. Fakat yönü de hesaba katmak için vektörel ifadeye ihtiyacımız vardır. $i$ cisminin $j$ nedeniyle kazandığı ivme şöyledir:

$$\vec{a}_{ij}=Gm_j\frac{\vec{r}_j-\vec{r}_i}{(\vert \vec{r}_j-\vec{r}_i\vert ^2+\epsilon^2)^{3/2}}$$

Toplam ivme, diğer bütün cisimlerin katkılarının toplamıdır:

$$\vec{a}_i=\sum_{j\ne i}\vec{a}_{ij}$$

Formüldeki $\epsilon$, iki cisim aşırı yaklaştığında ivmenin sonsuza gitmesini engelleyen **yumuşatma parametresidir**. Bu değer fiziksel bir yasa değil, sayısal simülasyonu kararlı tutan küçük bir emniyet yastığıdır.

| Kavram | Fiziksel anlamı | Simülasyondaki görevi |
|---|---|---|
| Konum | Cismin uzaydaki yeri | Uzaklık ve yön hesabı |
| Hız | Konumun değişim oranı | Yeni konumu belirleme |
| İvme | Hızın değişim oranı | Kütle çekimini uygulama |
| Zaman adımı | İki hesap arasındaki süre | Hassasiyet ve performans dengesi |
| Yumuşatma | Yakın geçiş düzeltmesi | Sayısal patlamayı önleme |

## Neden adım adım hesaplıyoruz?

İvme sürekli değiştiği için gelecekteki konumu tek hamlede bulamayız. Zamanı $\Delta t$ büyüklüğünde dilimlere ayırır, her dilimde ivme, hız ve konumu güncelleriz. Basit Euler yöntemi kolaydır fakat uzun simülasyonlarda enerji hatası biriktirir. **Leapfrog** yöntemi ise hız ve konumu birbirinin arasına yerleştirerek daha kararlı sonuç verir.

| Yöntem | Kolaylık | Kararlılık | Tipik kullanım |
|---|---:|---:|---|
| Euler | Yüksek | Düşük | Eğitim ve hızlı prototip |
| Leapfrog | Orta | Yüksek | Yörünge simülasyonları |
| Runge-Kutta 4 | Orta | Yüksek | Hassas kısa süreli hesaplar |

## Python ile temel uygulama

Aşağıdaki kod, iki boyutlu bir sistemde bütün cisimlerin ivmelerini hesaplar ve Leapfrog adımı uygular:

```python
import numpy as np

G = 1.0
EPS = 0.01
DT = 0.001

def accelerations(pos, mass):
    n = len(mass)
    acc = np.zeros_like(pos)

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            delta = pos[j] - pos[i]
            distance2 = np.dot(delta, delta) + EPS**2
            acc[i] += G * mass[j] * delta / distance2**1.5

    return acc

def leapfrog_step(pos, vel, mass):
    # Hızı yarım adım ilerlet.
    acc = accelerations(pos, mass)
    vel += 0.5 * DT * acc

    # Yeni hızla konumu tam adım ilerlet.
    pos += DT * vel

    # Yeni konumdaki ivmeyle hız adımını tamamla.
    acc = accelerations(pos, mass)
    vel += 0.5 * DT * acc
    return pos, vel

mass = np.array([1000.0, 1.0, 0.5])
pos = np.array([[0.0, 0.0], [1.0, 0.0], [-1.5, 0.0]])
vel = np.array([[0.0, 0.0], [0.0, 31.6], [0.0, -25.8]])

for _ in range(10000):
    pos, vel = leapfrog_step(pos, vel, mass)
```

İç içe döngüler nedeniyle hesaplama maliyeti $O(N^2)$ olur: cisim sayısı iki katına çıktığında etkileşim sayısı yaklaşık dört kat artar. Binlerce cisim için Barnes–Hut algoritması, uzaktaki cisimleri gruplandırarak maliyeti yaklaşık $O(N\log N)$ seviyesine indirebilir.

Sonuçları değerlendirirken yalnızca güzel yörüngelere bakmak yeterli değildir. Toplam enerji ve momentum yaklaşık korunmalıdır. Enerji sürekli artıyor veya azalıyorsa zaman adımı fazla büyük olabilir. İşte N-cisim simülasyonunun temel sırrı budur: doğru fizik kadar, hatayı kontrol eden doğru sayısal yöntem de gerekir.

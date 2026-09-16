---
layout: post
title: "Robotik Kolda Yörünge Planlama: Pürüzsüz Hareketin Matematiği"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - yörünge planlama
  - kinematik
  - python
  - otomasyon
toc: true
---

Bir robot kolun kahveyi dökmeden fincanı taşıması, yalnızca başlangıç ve bitiş noktalarını bilmesiyle mümkün değildir. Motorların ne zaman hızlanacağı, nerede yavaşlayacağı ve eklemlerin birbiriyle nasıl uyum sağlayacağı da hesaplanmalıdır. İşte yörünge planlama, robotun A noktasından B noktasına giderken izleyeceği hareketi zamana bağlı ve pürüzsüz biçimde tasarlar.

``

## Yol ve yörünge aynı şey mi?

Robotikte **yol**, geometrik olarak hangi noktalardan geçileceğini söyler. **Yörünge** ise bu noktalara zaman bilgisini ekler. Başka bir ifadeyle yol, “Nereden?”; yörünge ise “Nereden, ne zaman ve hangi hızla?” sorularını yanıtlar.

| Kavram | Tanım | Örnek |
|---|---|---|
| Konum | Eklemin belirli andaki açısı | $q=45^\circ$ |
| Hız | Konumun zamana göre değişimi | $\dot q(t)$ |
| İvme | Hızın zamana göre değişimi | $\ddot q(t)$ |
| Sarsıntı | İvmenin değişim hızı | $\dddot q(t)$ |

Pürüzsüz bir harekette yalnızca konumun sürekli olması yetmez. Hızdaki ani sıçramalar motorlara yük bindirir; ivmedeki ani değişimler ise titreşime, mekanik aşınmaya ve taşınan nesnenin düşmesine yol açabilir. Kısacası robot kolun “nazik” davranması için türevleri de düşünmeliyiz.

## Eklem uzayında planlama

En yaygın yaklaşım, her eklem için başlangıç açısı $q_0$ ile hedef açısı $q_f$ arasında bir fonksiyon üretmektir. Basit doğrusal interpolasyon şöyle yazılır:

$$q(t)=q_0+(q_f-q_0)\frac{t}{T}$$

Burada $T$, toplam hareket süresidir. Bu denklem kolaydır ancak hareket başlarken hızın bir anda sıfırdan sabit değere çıkmasına neden olur. Gerçek motorlar bu matematiksel “ışınlanmayı” pek sevmez.

Daha iyi bir çözüm, kübik polinom kullanmaktır:

$$q(t)=a_0+a_1t+a_2t^2+a_3t^3$$

Başlangıç ve bitiş konumlarıyla birlikte hızları da belirtirsek dört katsayıyı bulabiliriz:

$$q(0)=q_0,\quad q(T)=q_f,\quad \dot q(0)=0,\quad \dot q(T)=0$$

Böylece robot harekete yumuşakça başlar ve hedefte yumuşakça durur. İvmenin de başlangıç ve bitişte sıfır olması isteniyorsa beşinci dereceden, yani **quintic**, polinom tercih edilir.

| Yöntem | Süreklilik | Avantaj | Dezavantaj |
|---|---|---|---|
| Doğrusal | Konum | Çok basit | Ani hız değişimi |
| Kübik | Konum ve hız | Yumuşak kalkış/duruş | İvme sınırları sınırlı |
| Quintic | Konum, hız ve ivme | Çok pürüzsüz | Daha fazla hesaplama |
| S-eğrisi | İvme ve sarsıntı kontrollü | Mekanik açıdan güvenli | Parametre ayarı daha zor |

## Python ile quintic yörünge

Aşağıdaki kod, sıfır başlangıç ve bitiş hızı ile ivmesine sahip normalize edilmiş bir quintic profil üretir. `s` değeri, toplam hareketin ne kadarının tamamlandığını gösterir.

```python
import numpy as np

def quintic_trajectory(q0, qf, duration, samples=100):
    t = np.linspace(0, duration, samples)
    tau = t / duration

    # Pürüzsüz ölçekleme: s(0)=0 ve s(1)=1
    s = 10 * tau**3 - 15 * tau**4 + 6 * tau**5
    position = q0 + (qf - q0) * s

    velocity = np.gradient(position, t)
    acceleration = np.gradient(velocity, t)
    return t, position, velocity, acceleration

t, q, dq, ddq = quintic_trajectory(0.0, np.pi / 2, 2.0)
```

Bu profil, bir eklemi iki saniyede $0$ radyandan $\pi/2$ radyana taşır. Çok eklemli bir robotta aynı işlem her ekleme uygulanır; ancak tüm eklemler aynı anda bitirmelidir. Bu nedenle en yavaş eklemin gerektirdiği süre ortak $T$ olarak seçilebilir.

## Gerçek dünyadaki sınırlar

İyi bir planlayıcı motorların maksimum hızını, ivmesini ve torkunu aşmamalıdır. Ayrıca ters kinematik çözümleri, eklem limitleri ve çarpışmalar kontrol edilmelidir. Kartezyen uzayda dümdüz görünen bir hareket, eklem uzayında bazı motorların aşırı hızlanmasına neden olabilir.

Sonuç olarak pürüzsüzlük, yalnızca güzel görünen bir animasyon değildir; güvenlik, hassasiyet ve mekanik ömür demektir. Konumdan hıza, ivmeden sarsıntıya kadar her katmanı planladığınızda robot kolunuz panikleyen bir vinç gibi değil, deneyimli bir cerrah gibi hareket eder.

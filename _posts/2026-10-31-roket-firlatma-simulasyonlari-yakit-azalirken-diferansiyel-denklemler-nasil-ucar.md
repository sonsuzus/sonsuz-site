---
layout: post
title: "Roket Fırlatma Simülasyonları: Yakıt Azalırken Diferansiyel Denklemler Nasıl Uçar?"
math: true
categories: 
  - Proje
tags: 
  - sayısal entegrasyon
  - roket simülasyonu
  - diferansiyel denklemler
  - python
  - scipy
  - fizik
toc: true
image: /img/roket-firlatma-simulasyonlari-10.png
---

Bir roketi simüle etmek, ekrandaki bir nesnenin yüksekliğini sürekli artırmaktan çok daha heyecanlıdır. Yakıt tükendikçe kütle azalır, atmosfer inceldikçe sürükleme değişir ve motor sustuğunda yerçekimi sahneyi devralır. Bu değişkenlerin birlikte nasıl hareket ettiğini anlamak için diferansiyel denklemler kuracak, ardından Python ile sayısal olarak çözeceğiz. Emniyet kemerlerinizi matematiksel olarak bağlayın!

``

## Önce modelin sınırlarını çizelim

Dikey uçan, rüzgârdan etkilenmeyen ve yön değiştirmeyen bir roket düşünelim. Durum değişkenlerimiz yükseklik $h$, dikey hız $v$ ve toplam kütle $m$ olsun. Pozitif yön yukarıdır; başlangıçta roket yerde ve hareketsizdir. Yakıt dışında kütle kaybı olmadığını varsayıyoruz. Bu basitleştirmeler gerçek uçuşun bütün ayrıntılarını kapsamaz, ancak temel fiziği görünür kılar.

## Yakıt, itki ve hareket denklemleri

Motorun saniyede tükettiği yakıt miktarına $q$, etkin egzoz hızına $v_e$ diyelim. Motor çalışırken:

$$\frac{dm}{dt}=-q,\qquad T=qv_e$$

Buradaki $v_e$, egzozun rokete göre hızını ve seçilen modeldeki basınç katkısını temsil eden etkin değerdir. Sabit $q$ ve $v_e$ altında itki sabittir; fakat roket hafiflediği için aynı itkinin ürettiği ivme büyür. Gaz pedalını sabit tutup aracın yükünü azaltmak gibi!

Hareket denklemleri ise şöyledir:

$$\frac{dh}{dt}=v,\qquad \frac{dv}{dt}=\frac{T-\frac12\rho(h)C_DA\,v\vert v\vert }{m}-g(h)$$

$v\vert v\vert $ ifadesi önemlidir: Sürükleme yükselirken aşağı, düşerken yukarı yönelir. Değişken kütleli sistemde egzozun momentum etkisi zaten itkinin içindedir; ayrıca bir $v\,dm/dt$ terimi eklemek bu etkiyi yanlış biçimde tekrar sayar.

Atmosfer ve yerçekimi için basit ama kullanışlı iki yaklaşım seçebiliriz:

$$\rho(h)=\rho_0e^{-h/H},\qquad g(h)=g_0\left(\frac{R}{R+h}\right)^2$$

Burada $H$ atmosferin ölçek yüksekliği, $R$ Dünya yarıçapıdır. $C_D$ sürükleme katsayısı, $A$ ise referans kesit alanıdır. Gerçekte $C_D$ hızla değişebilir; şimdilik sabit kabul ediyoruz.

| Özellik | Motor çalışırken | Yakıt bittikten sonra |
|---|---|---|
| Kütle değişimi | $-q$ | Sıfır |
| İtki | $qv_e$ | Sıfır |
| Sürükleme | Harekete karşı | Harekete karşı |
| Yerçekimi | Aşağı yönlü | Aşağı yönlü |

## Neden sayısal entegrasyon?

Bu denklemler birbirine bağlıdır: Yükseklik yoğunluğu, yoğunluk sürüklemeyi, sürükleme de hızı değiştirir. Genel durumda tek bir kapalı formül aramak yerine zaman boyunca küçük ilerlemeler hesaplarız. Ancak küçük adım seçmek tek başına doğruluk garantisi değildir; yöntemin mertebesi ve hata kontrolü de belirleyicidir.

| Yöntem | Güçlü tarafı | Dikkat edilmesi gereken |
|---|---|---|
| İleri Euler | Kolay anlaşılır | Büyük adımlarda ciddi hata |
| RK4 | Düzgün problemlerde yüksek doğruluk | Genellikle sabit adım |
| Uyarlamalı RK45 | Yerel hataya göre adım seçer | Toleranslar doğru belirlenmeli |

## Python ile iki aşamalı uçuş

Aşağıdaki örnek önce yanmayı, sonra motorsuz uçuşu çözer. Sabit tüketimde yanma süresi $(m_0-m_d)/q$ olduğundan aşamaları tam bu noktada ayırırız. Böylece motor kapanışındaki süreksizliği çözücüye açıkça bildiririz.

```python
import numpy as np
from scipy.integrate import solve_ivp

m0, md = 500.0, 300.0  # kg: toplam ve kuru kütle
q, ve = 4.0, 2200.0    # kg/s ve m/s
Cd, A = 0.4, 0.3
rho0, H = 1.225, 8500.0
R, g0 = 6.371e6, 9.81
burn_time = (m0 - md) / q

def dynamics(t, y, burning):
    h, v, m = y
    rho = rho0 * np.exp(-h / H)
    gravity = g0 * (R / (R + h)) ** 2
    drag = 0.5 * rho * Cd * A * v * abs(v)
    thrust = q * ve if burning else 0.0
    dm = -q if burning else 0.0
    return [v, (thrust - drag) / m - gravity, dm]

def ground(t, y):
    return y[0]

ground.terminal = True
ground.direction = -1
options = dict(rtol=1e-7, atol=[1e-3, 1e-4, 1e-6],
               max_step=1.0)

powered = solve_ivp(
    lambda t, y: dynamics(t, y, True),
    (0, burn_time), [0.0, 0.0, m0], **options
)
if not powered.success:
    raise RuntimeError(powered.message)

state = powered.y[:, -1].copy()
state[2] = md  # Yuvarlama farkını gider.
coast = solve_ivp(
    lambda t, y: dynamics(t, y, False),
    (burn_time, 600.0), state, events=ground, **options
)
if not coast.success:
    raise RuntimeError(coast.message)
if coast.t_events[0].size:
    print('Yere dönüş zamanı:', coast.t_events[0][0])
else:
    print('600 saniye içinde yere dönüş gerçekleşmedi.')
```

`ground` olayı, yüksekliğin azalarak sıfırı geçmesini yakalar ve çözümü durdurur. Bileşenlere ayrı mutlak toleranslar vermemizin nedeni yükseklik, hız ve kütlenin farklı birimlere sahip olmasıdır. Seçilen başlangıç itkisinin ağırlıktan büyük olması da kalkışı mümkün kılar.

## Sonuçlara güvenmeden önce

Sürükleme ve yerçekimini kaldırarak çözümü roket denklemiyle karşılaştırın:

$$\Delta v=v_e\ln\left(\frac{m_0}{m_d}\right)$$

Ardından toleransları sıkılaştırıp sonuçların yakınsadığını kontrol edin. Kütlenin kuru kütlenin altına inmediğini doğrulayın. Bu model eğitim içindir; gerçek uçuş analizinde atmosfer verileri, değişken itki, yönelim ve yapısal sınırlar da gerekir. Roket bilimi zor olabilir, ama ilk sağlam adım doğru denklemdir!

![roket-firlatma-simulasyonlari-10](/img/roket-firlatma-simulasyonlari-10.svg)


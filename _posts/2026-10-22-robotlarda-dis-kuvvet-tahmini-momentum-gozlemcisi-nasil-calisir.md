---
layout: post
title: "Robotlarda Dış Kuvvet Tahmini: Momentum Gözlemcisi Nasıl Çalışır?"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - momentum gözlemcisi
  - dış kuvvet tahmini
  - kontrol
  - dinamik model
  - python
toc: true
image: /img/robotlarda-dis-kuvvet-66.png
---

Bir robot kolu insana, duvara veya çalışma masasındaki beklenmedik bir nesneye temas ettiğinde bunu nasıl fark eder? Her ekleme pahalı kuvvet-tork sensörleri yerleştirmek mümkün olsa da robotun dinamik modelinden yararlanmak daha ekonomik bir seçenektir. Momentum gözlemcisi, ölçülen eklem konumları ve uygulanan torklar arasındaki tutarsızlığı izleyerek dış kuvvetleri tahmin eder. Kısacası robot, “Hesaplarıma göre böyle hareket etmemeliydim!” dediği anda temastan şüphelenir.


![robotlarda-dis-kuvvet-66](/img/robotlarda-dis-kuvvet-66.svg)

``

## Dinamik modelden momentuma

$n$ serbestlik dereceli bir robotun eklem uzayındaki dinamiği şu şekilde yazılır:

$$M(q)\ddot{q}+C(q,\dot{q})\dot{q}+g(q)+\tau_f=\tau_m+\tau_{ext}$$

Burada $q$ eklem konumlarını, $M(q)$ eylemsizlik matrisini, $C(q,\dot q)$ Coriolis ve merkezkaç etkilerini, $g(q)$ yerçekimini ve $\tau_f$ sürtünmeyi temsil eder. Motorların ürettiği tork $\tau_m$, dış temasların eklemlerde oluşturduğu tork ise $\tau_{ext}$ ile gösterilir.

Doğrudan $\ddot q$ hesaplamak teoride kolay, pratikte gürültülüdür. Konum sinyalini iki kez türevlemek, ölçüm gürültüsüne adeta mikrofon uzatır. Momentum gözlemcisinin başrol oyuncusu bu yüzden genelleştirilmiş momentumdur:

$$p=M(q)\dot q$$

Dinamik denklemler uygun biçimde düzenlendiğinde momentumun değişimi üzerinden dış tork bulunabilir. Gözlemci, modelin beklediği momentum ile ölçümlerden elde edilen momentum arasındaki farkı bir artık, yani residual sinyali olarak üretir.

## Gözlemci mantığı

Yaygın bir momentum gözlemcisinde residual yaklaşık olarak şöyle tanımlanır:

$$r=K_I\left[p-p(0)-\int_0^t(\tau_m+\beta-r)\,dt\right]$$

Buradaki $K_I$ pozitif kazanç matrisi, $\beta$ ise yerçekimi ve robot dinamiğinden gelen bilinen terimlerin birleşimidir. İdeal model ve yeterince büyük gözlemci bant genişliği altında:

$$r\approx\tau_{ext}$$

Yani residual, dış eklem torkunun tahmini olur. Ancak kazancı sonsuza götürmek çözüm değildir; yüksek kazanç hızlı tepki sağlarken sensör gürültüsünü de büyütür.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Kuvvet-tork sensörü | Doğrudan ve hassas ölçüm | Maliyet, montaj ve kalibrasyon |
| İvme tabanlı tahmin | Basit dinamik yorum | İkinci türev nedeniyle yüksek gürültü |
| Momentum gözlemcisi | İvme ölçmeden tahmin | Model hatalarına ve sürtünmeye duyarlılık |
| Akım tabanlı algılama | Ek donanım gerektirmeyebilir | Motor sabiti ve transmisyon hataları |

## Kartezyen kuvvete geçiş

Gözlemci önce eklem torkunu tahmin eder. Temas noktası veya ilgili Jacobian $J(q)$ biliniyorsa dış kuvvet ile eklem torku arasındaki ilişki şöyledir:

$$\tau_{ext}=J(q)^T F_{ext}$$

Uygun boyut ve rank koşullarında kuvvet tahmini sözde ters kullanılarak hesaplanabilir:

$$\hat F_{ext}=(J^T)^\dagger\hat\tau_{ext}$$

Temas noktası bilinmiyorsa aynı eklem torkunu oluşturabilecek birden fazla kuvvet bulunabilir. Dolayısıyla gözlemci “bir dış etki var” konusunda güçlü, “tam olarak şurada oldu” konusunda ise ek bilgiye muhtaçtır.

## Basitleştirilmiş uygulama

Aşağıdaki Python kodu ayrık zamanda residual güncellemesinin temel fikrini gösterir:

```python
import numpy as np

class MomentumObserver:
    def __init__(self, gain, dt, dof):
        self.K = np.eye(dof) * gain
        self.dt = dt
        self.integral = np.zeros(dof)
        self.p0 = None

    def update(self, momentum, motor_torque, beta):
        if self.p0 is None:
            self.p0 = momentum.copy()

        residual = self.K @ (
            momentum - self.p0 - self.integral
        )

        # Model girdileri ve residual geri beslemesi entegre edilir.
        self.integral += (
            motor_torque + beta - residual
        ) * self.dt

        return residual
```

Gerçek sistemde momentum $M(q)\dot q$ ile hesaplanır; tork, hız ve model sinyalleri zaman açısından eşleştirilir. Residual doğrudan temas ilan etmek yerine alçak geçiren filtreden geçirilebilir ve belirli bir eşiğin üzerinde kaldığında çarpışma kararı verilebilir.

## Pratikte dikkat edilmesi gerekenler

Kötü modellenmiş sürtünme, redüktör boşluğu, motor tork sabiti hatası ve yanlış yük parametreleri sahte dış kuvvet üretir. Bu nedenle robotun kütle, kütle merkezi ve eylemsizlik parametreleri iyi tanımlanmalıdır. Eşikler de poz ve hıza göre uyarlanabilir; çünkü robot dururken normal görünen residual, yüksek ivmeli harekette fazla iyimser kalabilir.

Doğru ayarlanmış bir momentum gözlemcisi; çarpışma algılama, güvenli insan-robot etkileşimi, elle yönlendirme ve temas kontrollü montaj gibi uygulamalarda güçlü bir “sanal kuvvet sensörü” görevi görür.

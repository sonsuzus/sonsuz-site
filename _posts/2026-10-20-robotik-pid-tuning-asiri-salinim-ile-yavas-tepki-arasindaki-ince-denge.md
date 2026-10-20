---
layout: post
title: "Robotik PID Tuning: Aşırı Salınım ile Yavaş Tepki Arasındaki İnce Denge"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - pid
  - kontrol-sistemleri
  - tuning
  - otomasyon
  - python
toc: true
image: /img/robotik-pid-tuning-34.png
---

Bir robot kolunun hedef konuma yıldırım gibi ulaşıp birkaç kez ileri geri sallanması mı, yoksa ağır çekimde ilerleyerek hedefi şaşmadan bulması mı daha iyidir? PID kontrolcü ayarlarken karşılaşılan temel ikilem tam olarak budur: hızlı tepki ile düşük aşım arasında dengeli bir nokta bulmak.

``

PID kontrolcü, ölçülen durum ile hedef arasındaki hatayı kullanarak eyleyiciye uygulanacak komutu hesaplar. Temel denklem şöyledir:

$$u(t)=K_p e(t)+K_i ∫_0^t e(τ)dτ+K_d\frac{de(t)}{dt}$$

Burada $e(t)$ hedef ile ölçüm arasındaki farktır. $K_p$ anlık hataya, $K_i$ geçmişte biriken hataya, $K_d$ ise hatanın değişim hızına tepki verir. Üç kazanç birlikte çalışır; fakat her biri robotun davranışını farklı yönde iter.

| Kazanç | Artırıldığında genel etki | Olası yan etki |
|---|---|---|
| $K_p$ | Yükselme süresi kısalır | Aşım ve salınım artabilir |
| $K_i$ | Kalıcı durum hatası azalır | Aşım, integral yığılması ve oturma süresi artabilir |
| $K_d$ | Salınım sönümlenir | Sensör gürültüsü büyütülebilir |

![robotik-pid-tuning-34](/img/robotik-pid-tuning-34.svg)


## Aşırı salınım neden oluşur?

Yüksek $K_p$, robota “Hata büyük, daha sert hareket et!” der. Ancak motor ve mekanik sistem atalet taşır. Robot hedefe ulaştığında hareket enerjisi henüz kaybolmamıştır; bu nedenle hedefi geçer. Kontrolcü ters yönde komut verir ve süreç salınıma dönüşebilir. $K_i$ de geçmiş hataları toplamaya devam ederse hedefe varılmış olsa bile güçlü komut üretebilir. Buna **integral windup**, yani integral yığılması denir.

Yüzde aşım yaklaşık olarak şu şekilde ölçülür:

$$M_p=\frac{y_{max}-y_{hedef}}{y_{hedef}}\times 100$$

Örneğin hedef açı $90°$, görülen tepe değer $99°$ ise aşım yüzde 10'dur. Hassas bir kavrayıcı için bu oran tehlikeliyken, hızlı hareket eden basit bir mobil robot için kabul edilebilir olabilir.

## Yavaş tepki neden her zaman güvenli değildir?

Kazançları fazla düşük tutmak aşımı azaltabilir; ancak robot komutlara geç yanıt verir. Denge robotunda bu gecikme düşmeye, çizgi izleyen robotta parkurdan çıkmaya yol açabilir. Dolayısıyla yalnızca aşımı küçültmek yeterli değildir. Yükselme süresi, oturma süresi, kalıcı hata ve kontrol sinyalinin büyüklüğü birlikte değerlendirilmelidir.

| Öncelik | Tercih edilen davranış | Tipik yaklaşım |
|---|---|---|
| Hassas konumlama | Düşük aşım | Orta $K_p$, sınırlı $K_i$, yeterli $K_d$ |
| Hızlı takip | Kısa yükselme süresi | Daha yüksek $K_p$, kontrollü sönümleme |
| Gürültülü sensör | Kararlı kontrol sinyali | Filtrelenmiş veya düşük $K_d$ |
| Sürekli yük hatası | Sıfıra yakın kalıcı hata | Anti-windup ile $K_i$ kullanımı |

## Pratik tuning sırası

Önce $K_i$ ve $K_d$ sıfırlanır, ardından $K_p$ robot hızlı tepki verip salınım sınırına yaklaşana kadar artırılır. Sonra $K_d$ eklenerek hareket sönümlenir. En son küçük bir $K_i$, sürtünme veya yük nedeniyle kalan sabit hatayı temizlemek için kullanılır. Her değişiklikten sonra aynı hedef, yük ve başlangıç koşullarıyla test yapmak önemlidir.

Aşağıdaki Python kodu, ölçüm kayıtlarından aşım ve yaklaşık oturma süresini hesaplar:

```python
import numpy as np

def response_metrics(time, output, target, tolerance=0.02):
    output = np.asarray(output)
    error = np.abs(output - target)

    overshoot = max(0.0, (output.max() - target) / abs(target) * 100)
    limit = tolerance * abs(target)
    settling_time = None

    for i in range(len(output)):
        if np.all(error[i:] <= limit):
            settling_time = time[i]
            break

    return {'overshoot_percent': overshoot,
            'settling_time': settling_time}
```

Kod, tepe değeri kullanarak yüzde aşımı bulur ve çıktının yüzde 2 tolerans bandında kalmaya başladığı zamanı oturma süresi kabul eder. Böylece tuning, “gözüme iyi göründü” yaklaşımından ölçülebilir bir optimizasyona dönüşür.

Sonuç olarak ideal PID ayarı evrensel değildir. Robotun kütlesi, motor gücü, sensör gürültüsü ve görevi denge noktasını belirler. İyi tuning, en hızlı veya en sakin hareketi değil; görevin izin verdiği aşım sınırında yeterince hızlı, kararlı ve güvenli tepkiyi hedefler.

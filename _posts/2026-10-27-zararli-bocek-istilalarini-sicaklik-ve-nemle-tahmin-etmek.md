---
layout: post
title: "Zararlı Böcek İstilalarını Sıcaklık ve Nemle Tahmin Etmek"
math: true
categories: 
  - Bilgi
tags: 
  - tarım teknolojileri
  - matematiksel modelleme
  - veri bilimi
  - python
  - makine öğrenmesi
  - entomoloji
toc: true
image: /img/zararli-bocek-istilalarini-28.png
---

Tarladaki böcekler takvim kullanmaz; fakat sıcaklık ve nem değişimlerine şaşırtıcı derecede düzenli tepkiler verir. Hava ısındığında gelişimleri hızlanabilir, uygun nem seviyelerinde yumurtadan çıkma ve hayatta kalma oranları artabilir. Bu biyolojik ilişkileri matematiksel modellere dönüştürerek bir zararlı popülasyonunun ne zaman tehlikeli seviyeye ulaşacağını önceden tahmin etmek mümkündür.

``

## Böcek gelişiminin termal saati

Böcekler değişken vücut sıcaklığına sahip canlılardır. Bu nedenle gelişme hızları çevre sıcaklığıyla yakından ilişkilidir. En yaygın yaklaşım, **derece-gün** adı verilen birikimli sıcaklık ölçüsüdür. Bir günün derece-gün değeri basitçe şöyle hesaplanabilir:

$$DG = \max\left(0, \frac{T_{max}+T_{min}}{2}-T_{eşik}\right)$$

Burada $T_{eşik}$, zararlının gelişiminin durduğu taban sıcaklığıdır. Örneğin eşik $10^\circ C$, günlük ortalama sıcaklık ise $18^\circ C$ olduğunda o gün $8$ derece-gün birikir. Bir türün yumurtadan erginliğe geçmesi için 240 derece-güne ihtiyacı varsa uygun koşullarda gelişim yaklaşık 30 gün sürebilir.

Ancak sıcaklık tek oyuncu değildir. Nem; yumurtaların kurumasını, larvaların yaşama oranını ve mantar kaynaklı doğal ölümleri etkileyebilir. Bu yüzden modele bir nem uygunluk katsayısı eklenebilir:

$$H(RH)=\exp\left(-\frac{(RH-RH_{opt})^2}{2\sigma^2}\right)$$

$RH$ bağıl nemi, $RH_{opt}$ türün tercih ettiği nemi, $\sigma$ ise tolerans genişliğini gösterir. Nem ideal değerden uzaklaştıkça $H(RH)$ sıfıra yaklaşır.

## Popülasyon nasıl modellenir?

Basit üstel büyüme modeli $N_{t+1}=N_t e^r$ biçimindedir. Gerçek tarlalarda kaynaklar sınırlı olduğu için lojistik büyüme daha gerçekçidir:

$$N_{t+1}=N_t+r_tN_t\left(1-\frac{N_t}{K}\right)-M_t$$

Burada $N_t$ popülasyon, $K$ çevrenin taşıma kapasitesi, $M_t$ doğal ölüm veya mücadele etkisi, $r_t$ ise hava koşullarına bağlı büyüme oranıdır. Örneğin $r_t=r_0 f(T_t)H(RH_t)$ seçilebilir. Böylece çok sıcak, çok soğuk veya aşırı kuru günler büyümeyi frenler.

| Yaklaşım | Güçlü yanı | Sınırlaması |
|---|---|---|
| Derece-gün | Kolay hesaplanır, biyolojik yorumu nettir | Nem ve aşırı sıcaklık etkisini zayıf temsil eder |
| Lojistik model | Kaynak sınırını hesaba katar | Parametre kalibrasyonu gerekir |
| Makine öğrenmesi | Karmaşık ilişkileri öğrenebilir | Çok ve kaliteli veriye ihtiyaç duyar |
| Hibrit model | Biyoloji ile veriyi birleştirir | Kurulumu ve doğrulaması daha zordur |

![zararli-bocek-istilalarini-28](/img/zararli-bocek-istilalarini-28.svg)


## Python ile basit risk skoru

Aşağıdaki örnek, günlük sıcaklık ve nemden sıfır ile bir arasında bir istilâ riski üretir. Bu bir üretim modeli değil, mekanizmayı görünür kılan küçük bir prototiptir.

```python
import math

def istila_riski(t_min, t_max, nem, taban=10,
                  ideal_nem=70, nem_toleransi=15):
    ortalama = (t_min + t_max) / 2
    derece_gun = max(0, ortalama - taban)

    # Nem ideal değerden uzaklaştıkça uygunluk azalır.
    nem_uygunlugu = math.exp(
        -((nem - ideal_nem) ** 2) / (2 * nem_toleransi ** 2)
    )

    # 20 derece-gün günlük üst referans kabul edilmiştir.
    sicaklik_uygunlugu = min(derece_gun / 20, 1)
    return sicaklik_uygunlugu * nem_uygunlugu

print(istila_riski(18, 28, 72))
```

Gerçek bir sistemde bu skor; geçmiş tuzak sayımları, yağış, rüzgâr, bitki gelişim dönemi ve ilaçlama kayıtlarıyla kalibre edilmelidir. Model çıktısı ayrıca düşük, orta ve yüksek risk eşiklerine çevrilebilir.

## Tahmin neden doğrulanmalıdır?

Yüksek risk, kesin istilâ anlamına gelmez. Mikroiklim, doğal düşmanlar ve veri sensörlerindeki hatalar sonucu değiştirebilir. Bu nedenle veri eğitim ve test dönemlerine ayrılmalı; tahminler MAE, RMSE veya sınıflandırma metrikleriyle ölçülmelidir. En güvenli yaklaşım, modeli otomatik ilaçlama düğmesi olarak değil, saha gözlemini doğru zamana yönlendiren bir erken uyarı sistemi olarak kullanmaktır.

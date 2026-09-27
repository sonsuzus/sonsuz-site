---
layout: post
title: "Direksiyon Başındaki Görünmeyeni Bulmak: Sürücü Davranışı Analizinde HMM"
math: true
categories: 
  - Bilgi
tags: 
  - hidden markov modeli
  - hmm
  - sürücü analizi
  - makine öğrenmesi
  - sensör verisi
  - python
toc: true
image: /img/direksiyon-basindaki-gorunmeyeni-86.png
---

![direksiyon-basindaki-gorunmeyeni-86](/img/direksiyon-basindaki-gorunmeyeni-86.svg)


Bir otomobil sürücünün zihnini okuyamaz; ancak direksiyon hareketlerini, hız değişimlerini ve frenleme biçimini dikkatle dinleyebilir. Hidden Markov Modeli (HMM), doğrudan göremediğimiz **uykulu**, **agresif** veya **normal** sürüş durumlarını sensörlerden gelen ölçümler yardımıyla tahmin eder. Kısacası HMM, aracın küçük ipuçlarından sürücünün perde arkasındaki durumunu anlamaya çalışan istatistiksel bir dedektiftir.

``

## Gizli olan ne, gözlenen ne?

HMM'de sistemin gerçek durumu doğrudan gözlemlenemez. Sürücünün agresif olduğunu kesin biçimde ölçen bir sensör yoktur. Bunun yerine gaz pedalı konumu, direksiyon açısı, şerit sapması ve ivme gibi dolaylı belirtiler izlenir.

| HMM bileşeni | Sürücü analizi karşılığı | Örnek |
|---|---|---|
| Gizli durum | Sürücünün gerçek davranışı | Uykulu, normal, agresif |
| Gözlem | Sensörlerden ölçülen değer | Hız, ivme, direksiyon açısı |
| Geçiş olasılığı | Durumlar arasındaki değişim | Normalden uykuluya geçiş |
| Yayılım olasılığı | Durumun belirli ölçümü üretmesi | Agresifken yüksek ivme görülmesi |
| Başlangıç olasılığı | Yolculuk başındaki durum | Yüzde 80 normal sürüş |

Bir HMM, gizli durum dizisini $S_1,S_2,...,S_T$ ve gözlem dizisini $O_1,O_2,...,O_T$ olarak ele alır. Model üç temel olasılık kümesiyle tanımlanır:

- Başlangıç dağılımı: $P(S_1)$
- Geçiş olasılığı: $P(S_t \mid S_{t-1})$
- Gözlem olasılığı: $P(O_t \mid S_t)$

Ortak olasılık genel olarak şöyle yazılır:

$$P(S,O)=P(S_1)P(O_1 \mid S_1)\prod_{t=2}^{T}P(S_t \mid S_{t-1})P(O_t \mid S_t)$$

Buradaki kritik varsayım, mevcut durumun yalnızca önceki duruma bağlı olmasıdır. Başka bir deyişle model, sürücünün bütün hayat hikâyesini değil yakın geçmişini hatırlar. Bu sadeleştirme hesaplamayı mümkün kılar.

## Sensör verisi nasıl hazırlanır?

Ham sensör akışı doğrudan modele verilirse çukurlar, GPS hataları veya ani trafik olayları yanlış alarm üretebilir. Bu nedenle veriler kısa zaman pencerelerine ayrılır. Her pencere için ortalama hız, ivme varyansı, sert fren sayısı ve şerit sapmasının standart sapması gibi özellikler hesaplanır.

| Davranış | Muhtemel sensör örüntüsü | Karıştırılabileceği durum |
|---|---|---|
| Uykulu | Yavaş direksiyon düzeltmeleri, artan şerit sapması | Bozuk yol |
| Agresif | Sert hızlanma, ani fren, keskin dönüş | Acil manevra |
| Normal | Dengeli hız ve düşük değişkenlik | Yoğun trafik |

Gözlemler sürekli değerliyse her gizli durum için Gauss dağılımı kullanılabilir. Çok sayıda özelliğin birlikte değerlendirilmesi gerekiyorsa çok değişkenli Gauss dağılımı tercih edilir.

## Python ile küçük bir model

Aşağıdaki örnek, hız, boylamsal ivme ve şerit sapması özelliklerinden üç davranış durumu öğrenir:

```python
import numpy as np
from hmmlearn.hmm import GaussianHMM

# Her satır: [hız, ivme, şerit_sapması]
X = np.array([
    [82, 0.1, 0.08], [80, 0.0, 0.10],
    [110, 2.4, 0.25], [105, -3.1, 0.30],
    [68, 0.1, 0.65], [66, -0.1, 0.72]
])

model = GaussianHMM(
    n_components=3,
    covariance_type="full",
    n_iter=100,
    random_state=42
)
model.fit(X)

hidden_states = model.predict(X)
print(hidden_states)
```

`fit`, geçiş ve gözlem dağılımlarını veriden öğrenir. `predict` ise Viterbi algoritmasını kullanarak en olası gizli durum dizisini çıkarır. Ancak dönen `0`, `1` ve `2` etiketleri otomatik olarak “uykulu” anlamına gelmez; durumların sensör ortalamaları incelenerek uzmanlar tarafından adlandırılması gerekir.

## Gerçek hayatta dikkat edilmesi gerekenler

HMM zamansal bağımlılığı hesaba kattığı için tek ölçümlük eşik sistemlerinden daha kararlıdır. Yine de hava koşulları, araç tipi ve sürücünün kişisel alışkanlıkları modeli etkiler. Eğitim verisi farklı sürücülerden ve yol koşullarından toplanmalı; sonuçlar precision, recall ve karışıklık matrisiyle değerlendirilmelidir.

Üstelik “agresif” etiketi güvenlik, sigorta ve mahremiyet sonuçları doğurabilir. Bu yüzden tahminler kesin hüküm değil, sürücü destek sistemine sunulan olasılıksal uyarılar olarak ele alınmalıdır. HMM sihirli bir zihin okuyucu değildir; fakat sensörlerin fısıltısını anlamlı bir davranış hikâyesine dönüştürmekte oldukça yeteneklidir.

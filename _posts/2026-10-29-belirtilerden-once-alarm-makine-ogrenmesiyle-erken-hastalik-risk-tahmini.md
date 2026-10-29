---
layout: post
title: "Belirtilerden Önce Alarm: Makine Öğrenmesiyle Erken Hastalık Risk Tahmini"
math: true
categories: 
  - Bilgi
tags: 
  - makine öğrenmesi
  - erken teşhis
  - sağlık teknolojileri
  - yapay zeka
  - risk tahmini
  - veri bilimi
toc: true
image: /img/belirtilerden-once-alarm-54.png
---

Bir hastalığı belirtiler ortaya çıkmadan tahmin etmek bilim kurgu gibi gelebilir. Oysa elektronik sağlık kayıtları, laboratuvar sonuçları, tıbbi görüntüler, genetik veriler ve akıllı saat ölçümleri bir araya geldiğinde makine öğrenmesi önemli risk sinyallerini yakalayabilir. Ancak burada kritik bir ayrım vardır: Model çoğunlukla hastalığa kesin tanı koymaz; belirli bir zaman aralığında hastalığın gelişme olasılığını hesaplar.

``

## Risk tahmini nasıl çalışır?

Makine öğrenmesi, geçmişte sonucu bilinen hasta verilerindeki örüntüleri öğrenir. Örneğin diyabet riskini tahmin eden bir sistem; yaş, vücut kitle indeksi, açlık glukozu, aile öyküsü ve fiziksel aktivite gibi değişkenleri kullanabilir.

Bir hastanın özelliklerini $x$ ile gösterirsek modelin temel amacı şu olasılığı kestirmektir:

$$P(Y=1 \mid X=x)$$

Burada $Y=1$, belirlenen süre içinde hastalığın geliştiği anlamına gelir. Lojistik regresyon gibi açıklanabilir bir model bu olasılığı şöyle hesaplayabilir:

$$P(Y=1)=\frac{1}{1+e^{-(\beta_0+\beta_1x_1+\cdots+\beta_nx_n)}}$$

Katsayılar, her değişkenin risk üzerindeki etkisini temsil eder. Derin öğrenme modelleriyse çok daha karmaşık ilişkileri öğrenebilir; fakat kararlarını açıklamak genellikle daha zordur.

## Hangi veriler erken sinyal taşıyabilir?

| Veri türü | Yakalanabilecek sinyal | Örnek kullanım |
|---|---|---|
| Kan testleri | Küçük biyobelirteç değişimleri | Diyabet veya böbrek hastalığı riski |
| Tıbbi görüntüler | İnsan gözünün zor seçtiği dokusal örüntüler | Kanser taraması |
| Elektronik kayıtlar | Tanı, ilaç ve başvuru geçmişi | Kalp yetmezliği riski |
| Giyilebilir cihazlar | Nabız, uyku ve hareket sapmaları | Ritim bozukluğu uyarısı |
| Genetik veriler | Kalıtsal yatkınlık | Bazı kanser türleri |

![belirtilerden-once-alarm-54](/img/belirtilerden-once-alarm-54.svg)


Tek bir ölçüm yerine zaman içindeki değişim çoğu zaman daha değerlidir. Örneğin nabzın 80 olması tek başına anlamlı olmayabilir; kişinin aylar boyunca 60 civarında seyreden nabzının sürekli 80'e çıkması dikkat çekici olabilir.

## Basit bir risk modeli

Aşağıdaki örnek, hasta özelliklerinden ikili risk tahmini yapan sade bir Python iş akışıdır:

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

model = make_pipeline(
    StandardScaler(),
    LogisticRegression(class_weight="balanced")
)

model.fit(X_train, y_train)
risk_scores = model.predict_proba(X_test)[:, 1]
print("ROC-AUC:", roc_auc_score(y_test, risk_scores))
```

`StandardScaler`, değişkenleri benzer ölçeklere getirir. `class_weight="balanced"` ise hasta sayısının sağlıklı bireylerden çok az olduğu dengesiz veri kümelerinde modele yardımcı olur. `predict_proba`, kesin bir etiket yerine risk skoru üretir.

## Başarı yalnızca doğruluk değildir

Nadir hastalıklarda herkese “sağlıklı” diyen bir model yüksek doğruluk gösterebilir. Bu nedenle farklı ölçütler birlikte değerlendirilmelidir:

| Ölçüt | Yanıtladığı soru |
|---|---|
| Duyarlılık | Gerçek hastaların ne kadarı yakalandı? |
| Özgüllük | Sağlıklı kişilerin ne kadarı doğru elendi? |
| Kesinlik | Riskli denilenlerin ne kadarı gerçekten hastalandı? |
| ROC-AUC | Model riskli ve risksiz kişileri ne kadar ayırabiliyor? |
| Kalibrasyon | Yüzde 20 risk verilen grubun gerçekten yaklaşık yüzde 20'si hastalanıyor mu? |

Tarama sistemlerinde yanlış negatifler tehlikelidir; ancak çok fazla yanlış pozitif de gereksiz testlere, maliyete ve kaygıya yol açabilir. Bu yüzden karar eşiği klinik bağlama göre belirlenmelidir.

## Peki gerçekten mümkün mü?

Evet, bazı hastalıklar için belirtilerden önce anlamlı risk tahmini yapılabilir. Fakat veri kalitesi, farklı topluluklarda doğrulama, mahremiyet, algoritmik önyargı ve klinik denetim vazgeçilmezdir. Bir hastanede başarılı olan model, başka bir bölgede aynı sonucu vermeyebilir.

En sağlıklı yaklaşım, makine öğrenmesini doktorun yerine geçen dijital bir kâhin olarak değil, dikkat edilmesi gereken hastaları önceliklendiren bir erken uyarı sistemi olarak görmektir. Nihai tanı; hekim değerlendirmesi, doğrulayıcı testler ve hastanın klinik öyküsüyle konmalıdır.

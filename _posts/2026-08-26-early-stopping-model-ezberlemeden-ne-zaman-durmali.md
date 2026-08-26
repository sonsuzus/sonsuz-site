---
layout: post
title: "Early Stopping: Model Ezberlemeden Ne Zaman Durmalı?"
math: true
categories: 
  - Bilgi
tags: 
  - yapay zeka
  - makine öğrenmesi
  - early stopping
---

Bir yapay zeka modelini eğitmek, sınava çalışan bir öğrenciyi izlemeye benzer: İlk günlerde temel kavramları öğrenir, sonra soruları daha iyi çözmeye başlar. Ancak öğrencinin yalnızca deneme sorularının cevaplarını ezberlemesi gerçek sınavda başarısızlığa yol açar. Makine öğrenmesindeki karşılığı **overfitting** ya da aşırı öğrenmedir. Early Stopping (erken durdurma), model henüz genelleme yeteneğini kaybetmeden eğitimi bitirerek bu tuzağa karşı kullanılan pratik ve güçlü bir stratejidir.
``

Temel fikir, eğitim başarısını tek başına yeterli kabul etmemektir. Veri genellikle eğitim, doğrulama ve test kümelerine ayrılır. Modelin parametreleri eğitim kümesinde güncellenir; doğrulama kümesi ise daha önce görülmemiş örneklerdeki performansı ölçen bir kontrol noktasıdır. Test kümesi, yalnızca süreç sonunda tarafsız raporlama için saklanmalıdır.

Bir eğitim turuna **epoch** denir. Epoch sayısı arttıkça eğitim kaybı çoğunlukla düşer. Fakat doğrulama kaybı belli bir noktadan sonra yükselmeye başlayabilir. Bu, modelin veri içindeki genel örüntüleri değil, eğitim örneklerine özgü gürültüleri öğrenmeye başladığının sinyalidir. Amaç kabaca aşağıdaki dengeyi yakalamaktır:

$$
\theta^* = \arg\min_{\theta,\; t} L_{val}(\theta_t)
$$

Burada $\theta_t$, $t$ anındaki model parametrelerini; $L_{val}$ ise doğrulama kaybını temsil eder. Early Stopping, en son epoch'u değil, doğrulama metriğinin en iyi olduğu epoch'taki ağırlıkları kullanır.

| Kavram | Eğitim Kaybı | Doğrulama Kaybı | Yorum |
|---|---:|---:|---|
| Yetersiz öğrenme | Yüksek | Yüksek | Model henüz örüntüyü kavrayamadı. |
| Sağlıklı öğrenme | Düşüyor | Düşüyor | Genelleme gücü artıyor. |
| Aşırı öğrenme | Çok düşük | Yükseliyor | Model detayları ezberliyor. |

Erken durdurmanın en önemli ayarı **patience** değeridir. Bu değer, metrik iyileşmediğinde kaç epoch daha bekleneceğini belirler. Örneğin patience=5 ise doğrulama kaybı beş tur boyunca yeni bir en düşük değere ulaşmazsa eğitim durur. Küçük bir değer, geçici dalgalanmalarda eğitimi gereğinden erken kesebilir; büyük bir değer ise hem zamanı uzatır hem de ezberleme riskini artırır.

Aşağıdaki Keras örneğinde izlenen metrik `val_loss` değeridir. `restore_best_weights=True` seçeneği kritik bir ayrıntıdır: Eğitim durduğunda son ağırlıklar yerine en iyi doğrulama sonucunu veren ağırlıklar geri yüklenir.

```python
from tensorflow.keras.callbacks import EarlyStopping

early_stop = EarlyStopping(
    monitor="val_loss",
    mode="min",
    patience=5,
    min_delta=0.001,
    restore_best_weights=True,
    verbose=1
)

history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=100,
    batch_size=32,
    callbacks=[early_stop]
)
```

`min_delta=0.001`, çok küçük iyileşmeleri anlamlı kabul etmemeyi sağlar. Sınıflandırma probleminde kayıp yerine `val_accuracy` izlenebilir; bu durumda yön `mode="max"` olmalıdır. Çünkü doğruluk artması beklenen bir metriktir.

| Ayar | Ne yapar? | Tipik tercih |
|---|---|---|
| `monitor` | İzlenecek doğrulama metriğini seçer | `val_loss` |
| `patience` | İyileşme için bekleme turu | 3-10 epoch |
| `min_delta` | Anlamlı iyileşme eşiği | 0.0001-0.01 |
| `restore_best_weights` | En iyi ağırlıkları geri getirir | `True` |

Early Stopping tek başına sihirli değnek değildir. Küçük veya temsil gücü zayıf bir doğrulama kümesi yanlış sinyaller üretebilir. Bu nedenle veri bölme işlemi dikkatle yapılmalı; dengesiz sınıflarda stratified split, zaman serilerinde ise zamansal sıralama korunmalıdır. Dropout, veri artırma, L2 düzenlileştirme ve uygun model kapasitesiyle birlikte kullanıldığında Early Stopping hem eğitim maliyetini düşürür hem de modelin gerçek dünyada daha güvenilir davranmasına yardımcı olur. Kısacası iyi model, en uzun süre eğitilen değil; doğru anda durdurulan modeldir.

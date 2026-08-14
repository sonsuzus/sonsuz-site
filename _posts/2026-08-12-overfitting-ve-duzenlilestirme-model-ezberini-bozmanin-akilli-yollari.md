---
layout: post
title: "Overfitting ve Düzenlileştirme: Model Ezberini Bozmanın Akıllı Yolları"
math: true
categories: 
  - Bilgi
tags: 
  - makine öğrenmesi
  - deep learning
  - regularization
---

Bir öğrencinin sadece geçen yılın sınav sorularını ezberlediğini düşünün: Aynı sorularda kusursuzdur, fakat soru biçimi biraz değişince bocalar. Makine öğrenmesindeki **aşırı öğrenme (overfitting)** tam olarak budur. Model, eğitim verisindeki gerçek örüntüleri öğrenmek yerine gürültüyü, istisnaları ve tesadüfi ayrıntıları da belleğine kaydeder. Sonuçta eğitim başarımı yüksek, gerçek hayattaki yeni verilerdeki başarımı ise şaşırtıcı derecede düşük olur.
``

Bir modelin temel amacı eğitim kümesindeki hatayı sıfırlamak değil, hiç görmediği örneklerde de iyi tahmin yapmaktır. Bu yeteneğe **genelleme** denir. Eğitim kaybı $L_{train}$ azalırken doğrulama kaybı $L_{val}$ artmaya başlıyorsa alarm zilleri çalmalıdır. Modelin kapasitesi veri miktarına göre fazla olduğunda, örneğin gereğinden çok katman veya parametre kullanıldığında, overfitting ihtimali artar.

## Kayıp Fonksiyonuna Fren: L1 ve L2

Düzenlileştirme, modele “iyi öğren ama gereksiz karmaşıklaşma” diyen matematiksel bir frendir. Standart kayıp fonksiyonuna parametre büyüklüğünü cezalandıran bir terim eklenir:

$$L_{toplam} = L_{veri} + \lambda R(w)$$

Burada $\lambda$, cezanın şiddetini belirleyen hiperparametredir; $R(w)$ ise ağırlıklar için seçilen ceza fonksiyonudur. $\lambda$ çok küçükse model hâlâ ezberleyebilir, çok büyükse bu kez anlamlı örüntüleri bile öğrenemeyerek **underfitting** yaşayabilir.

| Teknik | Ceza | Temel etkisi | Ne zaman öne çıkar? |
|---|---:|---|---|
| L1 (Lasso) | $\lambda \sum_i  \vert w_i \vert $ | Bazı ağırlıkları tam sıfıra iter | Özellik seçimi önemliyse |
| L2 (Ridge / weight decay) | $\lambda \sum_i w_i^2$ | Büyük ağırlıkları yumuşakça küçültür | Sinir ağlarında genel amaçlı kullanımda |
| Dropout | Rastgele nöron kapatma | Nöronların birbirine bağımlılığını azaltır | Derin ağlarda |
| Early stopping | Eğitim zamanını sınırlama | Doğrulama performansını korur | Hızlı ve etkili koruma gerektiğinde |

L1, seyrek bir model üretme eğilimindedir: Önemsiz girdilerin ağırlıkları sıfırlanabilir. L2 ise ağırlıkları tamamen silmekten ziyade dengeler; tek bir özelliğin aşırı baskın hale gelmesini zorlaştırır. Pratikte L2, özellikle derin öğrenme projelerinde sık kullanılan güvenli bir başlangıçtır.

## Dropout: Ekibi Sürekli Değiştirerek Öğretmek

Dropout eğitim sırasında nöronların belirli bir oranını rastgele devre dışı bırakır. Örneğin $p=0.3$ ise her eğitim adımında nöronların yaklaşık %30'u geçici olarak “izinli” sayılır. Böylece model, “bu nöron mutlaka var” varsayımıyla çalışamaz; farklı nöron kombinasyonlarıyla sağlam temsiller öğrenmek zorunda kalır.

```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation="relu", input_shape=(20,)),
    tf.keras.layers.Dropout(0.30),  # Eğitimde nöronların %30'unu kapatır
    tf.keras.layers.Dense(1, activation="sigmoid")
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
```

Dropout yalnızca eğitim aşamasında aktiftir. Tahmin sırasında tüm nöronlar kullanılır; framework, eğitimdeki ölçekleme farkını otomatik yönetir. Çok yüksek dropout oranı ise modelin öğrenmesini gereksiz zorlaştırabilir. Genellikle $0.1$ ile $0.5$ aralığı denenir.

## Early Stopping: En İyi Anda Durmayı Bilmek

Eğitim süresi arttıkça eğitim kaybının düşmesi normaldir; fakat doğrulama metriği bir noktadan sonra kötüleşebilir. Early stopping, doğrulama kaybını takip eder ve belirlenen sayıda epoch boyunca iyileşme görülmezse eğitimi durdurur. En iyi ağırlıkları geri yüklemek kritik bir ayrıntıdır.

```python
callback = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

model.fit(X_train, y_train,
          validation_data=(X_val, y_val),
          epochs=100,
          callbacks=[callback])
```

Buradaki `patience=5`, küçük dalgalanmalar yüzünden eğitimin hemen kesilmesini engeller. En sağlam yaklaşım çoğu zaman tek bir teknik seçmek değil; makul bir L2 cezasını dropout ve early stopping ile birlikte, doğrulama kümesi sonuçlarına bakarak kullanmaktır. Ama unutmayın: Düzenlileştirmenin en iyi dostu hâlâ kaliteli ve çeşitli veridir.

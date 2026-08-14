---
layout: post
title: "Makine Öğrenmesi Paradigmaları: Veriden Öğrenmenin Üç Farklı Yolu"
math: true
categories: 
  - Bilgi
tags: 
  - makine öğrenmesi
  - yapay zeka
  - gözetimli öğrenme
  - gözetimsiz öğrenme
  - pekiştirmeli öğrenme
---

Makine öğrenmesi, bilgisayara her kuralı tek tek yazdırmak yerine örnekler, örüntüler ve geri bildirimler aracılığıyla davranış öğretme sanatıdır. Aynı mutfakta farklı tariflerin bulunması gibi, öğrenme probleminin elindeki veri ve hedefe göre üç temel paradigma öne çıkar: gözetimli, gözetimsiz ve pekiştirmeli öğrenme.
``

## Temel fikir: Veri, hedef ve geri bildirim

Klasik programlamada geliştirici kuralları yazar, sistem bu kuralları girdiye uygular ve çıktı üretir. Makine öğrenmesinde ise çoğu zaman **girdi ve beklenen çıktı örnekleri** verilir; algoritma aradaki kuralları yaklaşık olarak kendisi keşfeder.

Bir modelin genel amacı, eğitim verisinde başarılı olmanın ötesine geçerek daha önce görmediği örneklerde de iyi sonuç vermektir. Bu beceriye **genelleme** denir. Örneğin bir ev fiyatı modelinin yalnızca ezberlediği ilanlarda değil, yeni ilanlarda da makul tahmin yapması beklenir.

| Paradigma | Elimizde ne var? | Ana amaç | Tipik örnek |
|---|---|---|---|
| Gözetimli öğrenme | Girdi + doğru etiket | Tahmin yapmak | Spam tespiti |
| Gözetimsiz öğrenme | Yalnızca girdi verisi | Yapı/örüntü bulmak | Müşteri segmentasyonu |
| Pekiştirmeli öğrenme | Ortam ve ödül sinyali | Uzun vadeli karar vermek | Oyun oynayan ajan |

## Gözetimli öğrenme: Öğretmenli sınıf modeli

Gözetimli öğrenmede veri kümesinde her örneğin bir doğru cevabı, yani **etiketi** vardır. Bir e-posta için “spam” veya “değil”, bir fotoğraf için “kedi” ya da “köpek” etiketi verilebilir. Model, giriş $x$ ile hedef $y$ arasındaki ilişkiyi öğrenerek $\hat{y} = f(x)$ tahminini üretir.

Eğitim sürecinde tahmin ile gerçek değer arasındaki fark bir kayıp fonksiyonuyla ölçülür. Regresyonda yaygın bir seçenek ortalama karesel hatadır:

$$MSE = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$

Bu yaklaşım iki ana probleme ayrılır: **sınıflandırma** (ayrık sınıflar) ve **regresyon** (sürekli değerler). Etiket kalitesi burada kritik bir ayrıntıdır: yanlış etiketlenmiş binlerce örnek, modele yanlış öğretmenlik yapar.

```python
from sklearn.linear_model import LinearRegression

# Metrekare ve oda sayısından ev fiyatı tahmin etme
X = [[80, 2], [120, 3], [150, 4]]
y = [3_000_000, 4_800_000, 6_200_000]

model = LinearRegression().fit(X, y)
tahmin = model.predict([[100, 3]])
print(tahmin)
```

Bu kod, etiketli ev verisinden fiyat ilişkisini öğrenen basit bir regresyon modeli kurar.

## Gözetimsiz öğrenme: Etiketsiz veride dedektiflik

Gözetimsiz öğrenmede doğru cevap anahtarı yoktur. Algoritma, verinin iç yapısını keşfetmeye çalışır: Benzer müşteriler hangi kümelerde toplanıyor? Hangi işlemler alışılmadık davranıyor? Hangi özellikler birlikte değişiyor?

Kümeleme için kullanılan K-Means algoritması, noktaları $k$ kümeye ayırırken küme içi uzaklığı küçültmeyi hedefler:

$$\min \sum_{j=1}^{k}\sum_{x_i \in C_j}  \vert  \vert x_i - \mu_j \vert  \vert ^2$$

Burada $\mu_j$, ilgili kümenin merkezidir. Ancak “kaç küme olmalı?” sorusu çoğu zaman algoritmadan çok iş bilgisi gerektirir. Gözetimsiz öğrenme kesin cevap üretmekten ziyade, analiste keşfedilecek bir harita sunar.

## Pekiştirmeli öğrenme: Deneyerek öğrenen ajan

Pekiştirmeli öğrenmede bir **ajan**, bir **ortamda** eylem seçer ve bunun karşılığında ödül veya ceza alır. Satranç oynayan programın her hamle sonrası oyunun durumunu değiştirmesi buna güzel örnektir. Amaç anlık ödülü değil, gelecekteki toplam ödülü büyütmektir:

$$G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$$

$\gamma$ indirim katsayısıdır; gelecekteki ödüllere ne kadar önem verileceğini belirler. Ajanın temel ikilemi **keşif** ve **sömürü** arasındadır: Yeni bir hamleyi denemeli mi, yoksa bildiği iyi hamleyi mi oynamalı?

| Kriter | Gözetimli | Gözetimsiz | Pekiştirmeli |
|---|---|---|---|
| Geri bildirim | Doğru etiket | Doğrudan yok | Ödül/ceza |
| Öğrenme biçimi | Örnekten tahmin | Örüntü keşfi | Etkileşim ve deneme |
| Zorluk | Etiket toplama maliyeti | Sonucu yorumlama | Çok sayıda deney gereksinimi |

Doğru paradigma seçimi, “hangi algoritma popüler?” sorusundan önce gelir. Etiketli tarihsel sonuçlarınız varsa gözetimli öğrenme; bilinmeyen grupları anlamak istiyorsanız gözetimsiz öğrenme; kararların geleceği etkilediği dinamik bir ortamınız varsa pekiştirmeli öğrenme güçlü bir başlangıç noktasıdır.

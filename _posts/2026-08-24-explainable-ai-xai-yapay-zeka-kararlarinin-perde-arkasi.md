---
layout: post
title: "Explainable AI (XAI): Yapay Zeka Kararlarının Perde Arkası"
math: true
categories: 
  - Bilgi
tags: 
  - Yapay Zeka
  - Explainable AI
  - Makine Öğrenmesi
  - Python
---

Bir kredi başvurusunun neden reddedildiğini, bir görüntünün neden “kedi” olarak sınıflandırıldığını veya bir tıbbi modelin neden yüksek risk uyarısı verdiğini bilmek isteriz. Klasik makine öğrenmesi modelleri çoğu zaman yüksek doğruluk sunarken karar süreçlerini gizleyen birer “kara kutu” gibi davranır. Explainable AI (XAI), yani Açıklanabilir Yapay Zeka, bu kutunun kapağını aralayarak modelin hangi verilere, hangi yönde ve ne kadar ağırlık vererek karar aldığını anlaşılır hale getiren yöntemler bütünüdür.
``

XAI'ın temel amacı sadece “model ne tahmin etti?” sorusunu değil, “neden bu tahmini yaptı?” sorusunu da yanıtlamaktır. Bu ihtiyaç özellikle sağlık, finans, hukuk ve insan hayatını etkileyen otomasyon sistemlerinde kritiktir. Açıklama; veri bilimci için hata ayıklama aracı, alan uzmanı için doğrulama mekanizması, son kullanıcı içinse güven inşa eden bir iletişim katmanıdır.

Teorik olarak bir modelin tahmini $f(x)$ ile gösterilsin. Burada $x$ giriş özellikleri, $f$ ise öğrenilmiş fonksiyondur. XAI yöntemleri genellikle tahminin çevresinde daha basit bir açıklama modeli $g(x)$ kurmaya çalışır. Amaç, $g(x)$ modelinin hem asıl modele yakın olması hem de insan tarafından yorumlanabilmesidir. Bu denge kabaca şöyle ifade edilir:

$$
\min_g \; L(f, g, \pi_x) + \Omega(g)
$$

Burada $L$, açıklamanın asıl modele ne kadar sadık olduğunu; $\pi_x$, incelenen örneğin yakın çevresini; $\Omega(g)$ ise açıklamanın karmaşıklığını temsil eder. Çok karmaşık bir açıklama doğru olsa bile pratikte faydasız olabilir.

XAI yaklaşımları iki temel eksende sınıflanır:

| Boyut | Seçenekler | Örnek |
|---|---|---|
| Kapsam | Global / Yerel | Modelin genel davranışı / Tek kredi başvurusu |
| Model bağımlılığı | Modele özgü / Modelden bağımsız | Ağaç önemleri / SHAP, LIME |
| Açıklama biçimi | Sayısal / Görsel | Özellik katkısı / Isı haritası |

**Global açıklamalar**, modelin tüm veri kümesindeki genel davranışını anlatır. Karar ağaçları bu konuda doğal olarak yorumlanabilirdir: “Gelir 50.000 TL üzerindeyse ve gecikme yoksa onayla” gibi kurallar üretir. Doğrusal regresyonda ise katsayılar doğrudan ipucu verir. Örneğin $y = 2x_1 - 0.5x_2$ formülünde, $x_1$ arttıkça tahmin yükselme eğilimindedir.

**Yerel açıklamalar** ise tek bir kararın izini sürer. LIME, seçilen örneğin çevresinde sentetik örnekler üretir ve karmaşık modele yakın basit, çoğunlukla doğrusal bir model uydurur. SHAP ise oyun teorisindeki Shapley değerlerinden yararlanır. Her özelliğin katkısını, tüm olası özellik kombinasyonlarındaki marjinal etkisinin ortalaması olarak hesaplar:

$$
\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F|-|S|-1)!}{|F|!}[f(S \cup \{i\}) - f(S)]
$$

SHAP değerlerinde pozitif katkı tahmini yukarı, negatif katkı aşağı iter. Örneğin kredi riskini artıran “gecikmiş ödeme sayısı” kırmızı, riski azaltan “düzenli gelir” mavi bir grafikle gösterilebilir.

| Yöntem | Güçlü yanı | Sınırlaması |
|---|---|---|
| Özellik önemi | Hızlı genel bakış sağlar | Nedensellik kanıtlamaz |
| LIME | Tekil kararları sezgisel açıklar | Örneklemeye duyarlı olabilir |
| SHAP | Tutarlı, katkı bazlı analiz sunar | Büyük veride maliyetli olabilir |
| Grad-CAM | Görüntüde etkili alanları gösterir | Isı haritası yanıltıcı yorumlanabilir |

Python ile bir ağaç modelinin özellik önemlerini incelemek oldukça kolaydır:

```python
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

importance = pd.Series(model.feature_importances_, index=X_train.columns)
print(importance.sort_values(ascending=False))
```

Bu kod, rastgele orman modelinin kararlarında hangi sütunların göreli olarak daha etkili olduğunu listeler. Ancak önemli bir uyarı: özellik önemi, “bu özellik sonucu tek başına oluşturdu” anlamına gelmez. Korelasyon, veri sızıntısı ve önyargılı eğitim verisi açıklamaları da yanıltabilir.

İyi bir XAI uygulaması; açıklamayı hedef kitleye göre sunar, model doğruluğunu açıklanabilirlik uğruna körü körüne feda etmez ve açıklamaların kararlı olup olmadığını test eder. Kısacası XAI, yapay zekaya sadece konuşma yeteneği kazandırmaz; verdiği kararlar için hesap verme disiplini de kazandırır.

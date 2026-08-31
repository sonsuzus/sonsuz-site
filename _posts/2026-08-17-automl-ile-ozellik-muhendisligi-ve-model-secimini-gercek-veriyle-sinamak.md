---
layout: post
title: "AutoML ile Özellik Mühendisliği ve Model Seçimini Gerçek Veriyle Sınamak"
math: true
categories: 
  - Program
tags: 
  - automl
  - makine öğrenmesi
  - özellik mühendisliği
image: /img/automl-ile-ozellik-96.png
---

AutoML araçları, makine öğrenmesini “veriyi ver, sihri izle” düzeyine indirgeyen kutular değildir; iyi kullanıldıklarında veri hazırlama, özellik dönüşümü ve model arama süreçlerini sistematik biçimde hızlandırırlar. Ancak bir aracın gerçekten başarılı olup olmadığını anlamanın tek yolu, onu belirli bir veri setinde şeffaf ve tekrarlanabilir bir deneyle test etmektir. Buradaki amaç yalnızca en yüksek skoru bulmak değil, aracın hangi özellikleri faydalı gördüğünü ve hangi model ailesini neden seçtiğini değerlendirmektir.

![automl-ile-ozellik-96](/img/automl-ile-ozellik-96.svg)

``

Başlamadan önce problemi doğru tanımlayın. Örneğin UCI Adult Income veri setinde hedef değişken, kişinin gelirinin belirli bir eşiğin üzerinde olup olmadığıdır. Bu bir ikili sınıflandırma problemidir. Başarıyı yalnızca doğrulukla ölçmek yanıltıcı olabilir; sınıflar dengesizse model çoğunluk sınıfını tahmin ederek rahatça “başarılı” görünebilir. Bu nedenle F1 skoru ve ROC-AUC gibi metrikler daha dengeli bir bakış sunar.

$$F1 = 2 \cdot \frac{Precision \cdot Recall}{Precision + Recall}$$

AutoML sürecini adil test etmek için veriyi eğitim, doğrulama ve test olarak ayırmak gerekir. Test kümesi, araçların kararlarını gördükten sonra yeniden düzenlediğiniz bir alan değil; final sınavıdır. Eğitim verisinin içine test bilgisinin sızması, yani *data leakage*, parlak görünen ama üretimde dağılan modellerin klasik sebebidir.

| Aşama | Manuel yaklaşım | AutoML yaklaşımı |
|---|---|---|
| Eksik değerler | Ayrı imputation stratejisi seçilir | Sayısal ve kategorik sütunlara otomatik işlem uygulanır |
| Kategorik veri | One-hot veya target encoding kararı verilir | Uygun kodlama aranır ya da yerleşik destek kullanılır |
| Özellik seçimi | Korelasyon, önem ve alan bilgisi incelenir | Seçim, dönüşüm veya düzenlileştirme denenir |
| Model seçimi | Uzmanın belirlediği birkaç model çalışır | Birden çok algoritma ve hiperparametre taranır |

Python tarafında AutoGluon, H2O AutoML, PyCaret ve FLAML sık kullanılan seçeneklerdir. Aşağıdaki örnek, AutoGluon ile eğitim verisini kullanarak zaman sınırı içinde farklı modelleri yarıştırır. `time_limit`, deneyin bilgisayar kaynaklarını kontrol altında tutar; aksi halde AutoML, özellikle ansambl modellerde iştahlı bir CPU misafirine dönüşebilir.

```python
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, roc_auc_score
from autogluon.tabular import TabularPredictor

train_df, test_df = train_test_split(
    df, test_size=0.20, stratify=df["income"], random_state=42
)

predictor = TabularPredictor(
    label="income", eval_metric="f1", path="autogluon_income"
).fit(train_df, time_limit=600, presets="medium_quality")

predictions = predictor.predict(test_df.drop(columns="income"))
probabilities = predictor.predict_proba(test_df.drop(columns="income")).iloc[:, 1]

print("F1:", f1_score(test_df["income"], predictions))
print("ROC-AUC:", roc_auc_score(test_df["income"], probabilities))
print(predictor.leaderboard(test_df, silent=True))
```

Liderlik tablosu model seçiminin kalbidir. Örneğin LightGBM, CatBoost ve neural network adaylarının skorlarını, tahmin sürelerini ve ansambl içindeki rollerini karşılaştırabilirsiniz. Birinci olan model her zaman en mantıklı model değildir: milisaniye düzeyinde gecikme gereken bir API için biraz daha düşük skorlu ama hızlı bir model tercih edilebilir.

| İnceleme sorusu | Başarılı bir AutoML çıktısında beklenen işaret |
|---|---|
| Özellikler anlamlı mı? | Yaş, eğitim, çalışma saati gibi alanla ilişkili sütunlar öne çıkar |
| Sonuç kararlı mı? | Farklı rastgele bölmelerde skor dramatik biçimde düşmez |
| Model maliyeti uygun mu? | Eğitim ve çıkarım süreleri kullanım senaryosunu karşılar |
| Sızıntı var mı? | Hedefi doğrudan ya da dolaylı taşıyan sütunlar elenir |

Son olarak AutoML sonucunu basit bir baseline ile kıyaslayın. Lojistik regresyon veya tek bir karar ağacı, “otomasyon gerçekten değer kattı mı?” sorusuna dürüst bir referans sağlar. AutoML’ın başarısı yalnızca $\max(\text{skor})$ değildir; anlaşılabilir, tekrarlanabilir ve maliyeti yönetilebilir bir çözüm üretmesidir. En iyi deney, skor tablosunu özellik önemleri, hata örnekleri ve iş gereksinimleriyle birlikte okuyan deneydir.

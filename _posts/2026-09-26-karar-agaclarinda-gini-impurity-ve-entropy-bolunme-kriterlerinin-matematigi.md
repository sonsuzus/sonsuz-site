---
layout: post
title: "Karar Ağaçlarında Gini Impurity ve Entropy: Bölünme Kriterlerinin Matematiği"
math: true
categories: 
  - Bilgi
tags: 
  - makine öğrenmesi
  - karar ağaçları
  - gini impurity
  - entropy
  - python
  - veri bilimi
toc: true
image: /img/karar-agaclarinda-gini-71.png
---

Bir karar ağacı, verileri dallara ayırırken sürekli aynı soruyu sorar: “Hangi bölünme, sınıfları birbirinden en iyi şekilde ayırır?” Bu soruyu yalnızca sezgilerle cevaplamak yerine düğümlerin ne kadar karışık olduğunu ölçeriz. Sınıflandırma ağaçlarında bu amaçla en sık kullanılan iki ölçüt **Gini Impurity** ve **Entropy**’dir. İkisi de aynı hedefe koşar; ancak hedefe giderken kullandıkları matematiksel rota biraz farklıdır.

``

## Saflık ve belirsizlik ne anlama gelir?

Bir düğümdeki örneklerin tamamı aynı sınıfa aitse düğüm saftır. Örneğin kutuda yalnızca elmalar bulunuyorsa belirsizlik yoktur. Kutuda eşit sayıda elma ve armut varsa hangi meyveyi çekeceğimizi tahmin etmek daha zordur.

İki sınıflı bir problemde pozitif sınıfın oranı $p$, negatif sınıfın oranı $1-p$ olsun. Hem Gini hem de Entropy, $p=0$ veya $p=1$ olduğunda sıfır değerini alır. En yüksek belirsizlik ise sınıflar dengeliyken, yani $p=0.5$ civarında ortaya çıkar.

## Gini Impurity matematiği

Gini Impurity, rastgele seçilen bir örneğin düğümdeki sınıf dağılımına göre rastgele etiketlenmesi durumunda yanlış sınıflandırılma olasılığını temsil eder:

$$
Gini = 1 - \sum_{i=1}^{K} p_i^2
$$

Burada $K$ sınıf sayısını, $p_i$ ise $i$ sınıfının düğümdeki oranını gösterir. Yüzde 50 kedi ve yüzde 50 köpek bulunan bir düğüm için:

$$
Gini = 1-(0.5^2+0.5^2)=0.5
$$

Dağılım yüzde 90 kedi ve yüzde 10 köpek olduğunda sonuç $0.18$ olur. Değerin küçülmesi, düğümün daha saf hâle geldiğini gösterir.

## Entropy ve bilgi teorisi

Entropy, bilgi teorisinden gelir ve bir dağılımdaki şaşkınlığı ya da belirsizliği ölçer:

$$
Entropy = -\sum_{i=1}^{K} p_i\log_2(p_i)
$$

Eşit dağılımlı iki sınıfta Entropy değeri $1$’dir. Tek bir sınıftan oluşan düğümde ise $0$ olur. Hesaplama sırasında $0\log_2(0)$ ifadesi limit yaklaşımıyla sıfır kabul edilir.

Entropy ile bölünme değerlendirilirken çoğunlukla **Information Gain** kullanılır:

$$
IG = H(parent)-\sum_j \frac{n_j}{n}H(child_j)
$$

Yani çocuk düğümlerin ağırlıklı belirsizliği, ebeveynin belirsizliğinden çıkarılır. En yüksek bilgi kazancını sağlayan bölünme seçilir.

| Özellik | Gini Impurity | Entropy |
|---|---|---|
| Formül yapısı | Kare alma | Logaritma |
| İkili sınıfta maksimum | $0.5$ | $1$ |
| Hesaplama maliyeti | Genellikle daha düşük | Biraz daha yüksek |
| Hassasiyet | Baskın sınıfa odaklanabilir | Nadir sınıflara biraz daha duyarlıdır |
| Yaygın kullanım | CART, scikit-learn varsayılanı | ID3, C4.5 ve bilgi kazancı |

![karar-agaclarinda-gini-71](/img/karar-agaclarinda-gini-71.svg)


## Bölünme nasıl puanlanır?

Bir aday bölünmenin kalitesi, çocuk düğümlerin ağırlıklı impurity değeriyle hesaplanır:

$$
I_{split}=\frac{n_L}{n}I_L+\frac{n_R}{n}I_R
$$

Amaç bu değeri küçültmek veya ebeveyn düğüme göre impurity azalmasını büyütmektir. Çok saf fakat yalnızca iki örnek içeren bir dalın ağacı yanıltmaması için örnek sayılarıyla ağırlıklandırma kritik öneme sahiptir.

```python
from sklearn.tree import DecisionTreeClassifier

# Aynı veri üzerinde iki farklı saflık ölçütü kullanan modeller
models = {
    'gini': DecisionTreeClassifier(criterion='gini', random_state=42),
    'entropy': DecisionTreeClassifier(criterion='entropy', random_state=42)
}

for name, model in models.items():
    model.fit(X_train, y_train)
    print(name, model.score(X_test, y_test))
```

Bu kod iki ağacı aynı eğitim verisiyle kurar ve test doğruluklarını karşılaştırır. Sağlıklı bir deneyde yalnızca doğruluğa değil; eğitim süresine, ağaç derinliğine, çapraz doğrulama skorlarına ve dengesiz veri varsa F1 ya da ROC-AUC değerlerine de bakılmalıdır.

## Hangisini seçmeliyiz?

Pratikte iki kriter çoğu zaman benzer bölünmeler ve tahmin performansı üretir. Gini, logaritma hesaplamadığı için teorik olarak daha hızlıdır; Entropy ise olasılıklardaki değişimleri bilgi miktarı olarak yorumlamayı sağlar. Küçük hız farkları modern uygulamalarda genellikle belirleyici değildir.

En doğru yaklaşım, kriteri bir hiperparametre gibi değerlendirmektir. Çapraz doğrulamayla ikisini de deneyin; genelleme performansı, model karmaşıklığı ve çalışma süresi açısından daha uygun olanı seçin. Kısacası Gini hızlı bir saflık dedektörü, Entropy ise bilgi teorisi gözlüğü takmış meraklı bir matematikçidir.

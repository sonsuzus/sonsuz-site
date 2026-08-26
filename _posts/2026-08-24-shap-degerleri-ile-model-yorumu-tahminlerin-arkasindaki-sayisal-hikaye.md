---
layout: post
title: "SHAP Değerleri ile Model Yorumu: Tahminlerin Arkasındaki Sayısal Hikâye"
math: true
categories: 
  - Bilgi
tags: 
  - shap
  - makine öğrenmesi
  - model açıklanabilirliği
toc: true
---

Bir makine öğrenmesi modeli yüksek doğruluk verdiğinde ilk soru genellikle “Ne kadar başarılı?” olur; ikinci ve çoğu zaman daha kritik soru ise “Bu karara neden vardı?”dır. SHAP (SHapley Additive exPlanations), bir tahmini özelliklerin katkılarına bölerek bu soruya sayısal bir yanıt verir. Böylece kredi reddi, müşteri terk tahmini veya fiyat tahmini gibi sonuçlarda modelin hangi sinyalleri ne yönde kullandığını görünür kılar.
``
## SHAP’ın teorik temeli: kooperatif oyun teorisi

SHAP, kooperatif oyun teorisindeki **Shapley değerlerinden** gelir. Burada model tahmini “oyunun kazancı”, özellikler ise bu kazancı birlikte oluşturan oyunculardır. Her özelliğin katkısı, mümkün olan tüm özellik birleşimlerinde modele eklediği ortalama marjinal fayda hesaplanarak bulunur.

Bir özellik için Shapley değeri genel olarak şöyledir:

$$\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F|-|S|-1)!}{|F|!}\left[f(S \cup \{i\}) - f(S)\right]$$

Burada $F$ tüm özellik kümesini, $S$ ise $i$ özelliği eklenmeden önce kullanılan özellik alt kümesini temsil eder. Formül göz korkutucu görünse de ana fikir basittir: Bir özelliğin katkısı, tek bir senaryoda değil, katılabileceği tüm ekip kombinasyonlarında adil biçimde ölçülür.

SHAP açıklaması toplamsal bir yapı kurar:

$$f(x) = E[f(X)] + \sum_{i=1}^{M}\phi_i$$

Yani tahmin; modelin ortalama çıktısı ile her özelliğin pozitif veya negatif katkısının toplamıdır. Bu eşitlik, açıklamanın yalnızca görsel bir yorum değil, tahminle matematiksel olarak tutarlı bir ayrıştırma olduğunu gösterir.

## Yerel ve küresel yorum arasındaki fark

SHAP hem tek bir müşterinin tahminini hem de modelin genel davranışını inceleyebilir. Bu iki bakış açısını birbirine karıştırmamak önemlidir.

| Yaklaşım | Sorduğu soru | Tipik SHAP çıktısı | Kullanım örneği |
|---|---|---|---|
| Yerel açıklama | “Bu kayıt neden yüksek risk aldı?” | Waterfall/force plot | Tek kredi başvurusunu inceleme |
| Küresel açıklama | “Model genel olarak en çok neye bakıyor?” | Summary plot, ortalama $|SHAP|$ | Özellik önceliği analizi |
| Etkileşim analizi | “İki özellik birlikte nasıl davranıyor?” | Dependence plot | Yaş ve gelir ilişkisini inceleme |

Örneğin bir müşterinin terk olasılığı %72 çıktıysa, uzun süre destek kaydı açmış olması tahmini yukarı çekebilir; yıllık abonelik kullanması ise aşağı indirebilir. Bu, o müşteri için yerel açıklamadır. Tüm müşterilerde “destek kaydı sayısı”nın ortalama mutlak SHAP değerinin yüksek olması ise bu değişkenin küresel önemini gösterir.

## Python ile pratik uygulama

Ağaç tabanlı modellerde `TreeExplainer` genellikle hızlı ve etkilidir. Aşağıdaki örnek, eğitilmiş bir `RandomForestClassifier` için test verisini açıklar:

```python
import shap
from sklearn.ensemble import RandomForestClassifier

# X_train, X_test ve y_train daha önce hazırlanmış kabul edilir.
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# İkili sınıflandırmada pozitif sınıfın katkılarını görselleştirir.
shap.summary_plot(shap_values[1], X_test)
```

Bu kodda `explainer`, modelin karar mantığını SHAP katkılarına dönüştürür. `summary_plot` ise her satırı bir gözlem, her noktayı bir özellik değeri olarak gösterir. Sağa giden SHAP değerleri pozitif sınıf olasılığını artırırken, sola gidenler azaltır. Renk çoğunlukla ham özellik değerini belirtir: kırmızı yüksek, mavi düşük değer demektir.

## Dikkat edilmesi gerekenler

| Durum | Neden önemlidir? | Sağlıklı yaklaşım |
|---|---|---|
| Korelasyonlu özellikler | Katkı birbirine benzeyen değişkenler arasında paylaşılabilir | Özellikleri alan bilgisiyle birlikte yorumlayın |
| Nedensellik varsayımı | SHAP ilişkiyi açıklar, sebep-sonucu kanıtlamaz | Deneysel veya nedensel analiz yapın |
| Arka plan verisi | Beklenen değer açıklamanın başlangıç noktasını etkiler | Temsil gücü yüksek bir örneklem seçin |
| Çok büyük veri | Hesaplama maliyeti artabilir | Örneklem kullanın veya modele uygun açıklayıcı seçin |

SHAP, “model hangi değişkenleri kullandı?” sorusunu “bu tahminde her değişken kaç birim etkiledi?” seviyesine taşır. Ancak onu bir nedensellik makinesi gibi değil, karar mekanizmasını denetlenebilir kılan güçlü bir açıklama aracı olarak kullanmak gerekir. En iyi sonuç, SHAP grafikleri, veri kalitesi kontrolleri ve alan uzmanlığının birlikte değerlendirilmesiyle elde edilir.

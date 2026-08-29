---
layout: post
title: "SVM’de Kernel Trick: Doğrusal Olmayan Sınırları Akıllıca Çizmek"
math: true
categories: 
  - Bilgi
tags: 
  - makine öğrenmesi
  - svm
  - kernel trick
---

Destek Vektör Makineleri (SVM), sınıflandırma dünyasının cetvelli öğrencisi gibidir: sınıfları ayıran en güvenli doğruyu bulmak ister. Ancak gerçek veriler nadiren iki kümeye ayrılmış, uslu uslu duran noktalar içerir. İç içe halkalar, kıvrımlı karar bölgeleri ve karmaşık örüntüler ortaya çıktığında doğrusal bir hiper düzlem yetersiz kalır. İşte kernel trick, veriyi görünmez biçimde daha yüksek boyutlu bir uzaya taşıyarak SVM’nin doğrusal araçlarla doğrusal olmayan sınırlar kurmasını sağlar.

``

SVM’nin temel hedefi, sınıflar arasındaki **marjı** en büyük yapan karar düzlemini bulmaktır. Doğrusal durumda karar fonksiyonu aşağıdaki gibidir:

$$f(x)=w^T x+b$$

Bir örnek için sınıf etiketi $y_i \in \{-1,1\}$ ise ideal ayrım koşulu $y_i(w^T x_i+b)\geq1$ biçimindedir. Pratikte veriler kusursuz ayrılmayabilir; bu nedenle `C` parametresi marj genişliği ile eğitim hatası arasındaki dengeyi belirler. Büyük `C`, hataları daha sert cezalandırır; küçük `C` ise daha toleranslı, genellikle daha genellenebilir bir sınır oluşturur.

Asıl sihir, SVM’nin ikili (dual) formunda yalnızca örnekler arasındaki iç çarpıma ihtiyaç duymasıdır. Bir dönüşüm fonksiyonu $\phi(x)$ düşünelim. Açıkça dönüşüm hesaplamak yerine şu eşitliği kullanırız:

$$K(x_i,x_j)=\phi(x_i)^T\phi(x_j)$$

Böylece milyonlarca yeni özellik üretmeden, yüksek hatta sonsuz boyutlu uzaydaki benzerliği hesaplarız. Bu yaklaşım **kernel trick** olarak adlandırılır. Karar fonksiyonu da destek vektörleri üzerinden çalışır:

$$f(x)=\sum_i \alpha_i y_i K(x_i,x)+b$$

Buradaki yalnızca kritik gözlemler, yani destek vektörleri, sınırın biçimini doğrudan etkiler.

| Kernel | Formül | Güçlü olduğu veri yapısı | Dikkat edilmesi gereken |
|---|---|---|---|
| Linear | $K(x,z)=x^Tz$ | Çok boyutlu, yaklaşık doğrusal metin verisi | Karmaşık eğrileri yakalayamaz |
| Polynomial | $K(x,z)=(\gamma x^Tz+r)^d$ | Özellik etkileşimleri | Derece büyürse aşırı uyum |
| RBF | $K(x,z)=e^{-\gamma\\vert x-z\\vert ^2}$ | Genel amaçlı kıvrımlı sınırlar | `gamma` seçimine hassas |
| Sigmoid | $K(x,z)=\tanh(\gamma x^Tz+r)$ | Sinir ağı benzeri deneyler | Her parametrede kararlı değildir |

Deneysel bir karşılaştırmada önce özellikleri ölçeklemek kritik önemdedir. Özellikle RBF, uzaklık kullandığı için büyük değer aralığına sahip bir sütun tüm kararı ele geçirebilir. Aşağıdaki kod, sentetik “iki ay” verisinde lineer, polinom ve RBF kernel’lerini çapraz doğrulama ile kıyaslar:

```python
from sklearn.datasets import make_moons
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

X, y = make_moons(n_samples=600, noise=0.22, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)

pipe = Pipeline([
    ("scale", StandardScaler()),
    ("svm", SVC())
])

params = [
    {"svm__kernel": ["linear"], "svm__C": [0.1, 1, 10]},
    {"svm__kernel": ["poly"], "svm__C": [0.1, 1, 10],
     "svm__degree": [2, 3], "svm__gamma": ["scale"]},
    {"svm__kernel": ["rbf"], "svm__C": [0.1, 1, 10],
     "svm__gamma": [0.1, 1, 10]}
]

search = GridSearchCV(pipe, params, cv=5, scoring="accuracy")
search.fit(X_train, y_train)
print(search.best_params_)
print(search.score(X_test, y_test))
```

Bu veri kümesinde lineer kernel çoğunlukla iki hilali tek çizgiyle ayıramaz. Polinom kernel uygun derecede başarılı olabilir; fakat derece arttıkça sınır gereksiz kıvrılabilir. RBF ise yerel benzerlikleri modellediğinden genellikle en iyi adaydır. `gamma` küçükken her noktanın etkisi genişler ve sınır sadeleşir; büyükken etki alanı daralır, model eğitim örneklerini ezberlemeye yaklaşır.

| Belirti | Muhtemel ayar | Pratik çözüm |
|---|---|---|
| Eğitim ve test başarısı düşük | Model fazla basit | `C` veya kernel esnekliğini artırın |
| Eğitim yüksek, test düşük | Aşırı uyum | `C`/`gamma` değerini azaltın |
| Sonuçlar tutarsız | Ölçekleme yok | `StandardScaler` kullanın |

Özetle kernel trick, “daha fazla özellik üret” demeden daha zengin bir geometri sunar. En iyi kernel evrensel değildir: veri yapısı, hesaplama bütçesi ve çapraz doğrulama sonuçları birlikte karar vermelidir.

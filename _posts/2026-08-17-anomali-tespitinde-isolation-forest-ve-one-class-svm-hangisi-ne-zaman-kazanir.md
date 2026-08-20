---
layout: post
title: "Anomali Tespitinde Isolation Forest ve One-Class SVM: Hangisi Ne Zaman Kazanır?"
math: true
categories: 
  - Bilgi
tags: 
  - anomali tespiti
  - makine öğrenmesi
  - ısolation forest
  - one-class svm
---

Bir kredi kartı işlemi, sunucu metriği veya üretim hattındaki sensör verisi normal davranıştan uzaklaştığında alarm vermek isteriz. Ancak etiketli “sahte” ya da “arıza” örnekleri çoğu zaman azdır. İşte bu noktada denetimsiz ve yarı denetimli anomali tespiti yöntemleri devreye girer. Isolation Forest (IF) ve One-Class SVM (OCSVM), aynı hedefe ulaşırken dünyayı oldukça farklı yorumlayan iki güçlü araçtır.
``

## Temel fikir: Normal olanı mı öğreniyoruz, aykırıyı mı ayırıyoruz?

**Isolation Forest**, anomalilerin seyrek ve diğer gözlemlerden farklı olduğu varsayımından hareket eder. Rastgele özellikler ve bölünme eşikleri seçerek karar ağaçları oluşturur. Uzakta duran sıra dışı bir nokta, genellikle birkaç bölmeyle tek başına kalır; yani kısa bir yol uzunluğuna sahiptir.

Bir gözlemin ortalama izolasyon yolu $E[h(x)]$ ise, IF anomali skorunu kabaca şöyle normalize eder:

$$s(x)=2^{-\frac{E[h(x)]}{c(n)}}$$

Burada $c(n)$, veri kümesi boyutuna bağlı normalleştirme terimidir. Skor 1’e yaklaştıkça gözlem daha şüphelidir. Güzel tarafı: Model, “normal dağılım mutlaka çan eğrisidir” diye diretmez.

**One-Class SVM** ise normal veriyi özellik uzayında çevreleyen bir sınır öğrenir. Çekirdek (kernel) hilesi sayesinde doğrusal olmayan yapıları da yakalayabilir. RBF çekirdeği sık kullanılır:

$$K(x_i,x_j)=\exp(-\gamma\lVert x_i-x_j\rVert^2)$$

Modelin amacı, verilerin çoğunu sınırın bir tarafında tutarken orijinden mümkün olduğunca uzak bir karar yüzeyi kurmaktır. Yeni bir örnek bu yüzeyin dışına taşarsa anomali kabul edilir.

| Kriter | Isolation Forest | One-Class SVM |
|---|---|---|
| Ana yaklaşım | Noktaları rastgele bölerek izole eder | Normal bölgeyi karar sınırıyla sarar |
| Doğrusal olmayan yapı | Ağaç bölmeleriyle yakalar | Kernel ile güçlü biçimde yakalar |
| Ölçeklendirme ihtiyacı | Genellikle düşük | Çok yüksek; standardizasyon şart |
| Büyük veri performansı | Genellikle çok iyi | Eğitimde zorlanabilir |
| Yüksek boyut | Çoğu pratik senaryoda dayanıklı | Boyut arttıkça hassaslaşabilir |

## Hangi senaryoda hangisi önde?

Milyonlarca log kaydı, çok sayıda sayısal özellik ve hızlı model yenileme ihtiyacı varsa **Isolation Forest** genellikle ilk tercihtir. Paralelleşebilir, `n_estimators` ile kararlılığı artırılabilir ve `contamination` parametresiyle beklenen anomali oranı belirtilebilir. Özellikle “uçlarda duran” işlemler ve kaba davranış sapmaları için başarılıdır.

Normal sınıfın karmaşık, kıvrımlı ve yoğun kümeler oluşturduğu; veri setinin ise orta ölçekli olduğu durumda **One-Class SVM** etkileyici sonuç verebilir. Örneğin kontrollü bir üretim sürecinde normal titreşim imzaları çok karakteristikse, RBF kernel hassas sınırlar çizebilir. Buna karşılık yanlış `gamma` seçimi modeli ya aşırı genel ya da aşırı ezberci yapar.

| Durum | Daha uygun seçim | Neden |
|---|---|---|
| Çok büyük tablo verisi | Isolation Forest | Daha iyi ölçeklenir |
| Karmaşık normal sınır | One-Class SVM | Kernel esnekliği sağlar |
| Özellikler farklı birimlerde | Isolation Forest veya ölçeklenmiş OCSVM | OCSVM ölçeğe duyarlıdır |
| Anomali oranı belirsiz | IF ile eşik analizi | Skorları incelemek pratiktir |
| Çok az ama temiz normal veri | One-Class SVM | Normal bölgeyi ayrıntılı öğrenebilir |

## Python ile hızlı karşılaştırma

Aşağıdaki kod, iki modeli aynı standartlaştırılmış veri üzerinde kurar. IF için ölçekleme zorunlu olmasa da adil bir deney düzeni için ortak dönüşüm kullanılmıştır.

```python
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM

X_scaled = StandardScaler().fit_transform(X_train)

iso = IsolationForest(
    n_estimators=300,
    contamination=0.02,
    random_state=42
)
ocsvm = OneClassSVM(kernel="rbf", nu=0.02, gamma="scale")

iso.fit(X_scaled)
ocsvm.fit(X_scaled)

# scikit-learn: -1 anomali, 1 normal anlamına gelir
iso_labels = iso.predict(X_scaled)
svm_labels = ocsvm.predict(X_scaled)
```

`contamination` ve `nu`, kabaca anomali oranına dair beklentiyi temsil eder; bunları körlemesine seçmek yerine geçmiş olaylar, uzman görüşü ve doğrulama setiyle ayarlayın. Son karar yalnızca model etiketiyle verilmemeli: skor dağılımını inceleyin, maliyeti yüksek yanlış alarmları ölçün ve zaman içindeki veri kaymasını takip edin. Kısacası hız ve ölçek için Isolation Forest, hassas geometrik sınırlar için One-Class SVM; gerçek şampiyon ise veriniz üzerinde yapılan ölçülü deneydir.

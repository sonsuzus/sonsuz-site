---
layout: post
title: "Derin Öğrenme: Katman Katman Özellik Keşfi"
math: true
categories: 
  - Bilgi
tags: 
  - derin öğrenme
  - yapay sinir ağları
  - makine öğrenmesi
toc: true
---

Derin öğrenme, yapay zekânın veriye “hangi özelliğe bakması gerektiğini” tek tek öğretmek yerine bunu katmanlar aracılığıyla öğrenmesini sağlayan yaklaşımdır. Temel fikir basittir: Geleneksel sinir ağlarına çok sayıda gizli katman eklenir; böylece model, ham ve yüksek boyutlu verilerden giderek daha soyut temsiller çıkarabilir. Bir görüntüde önce kenarları, sonra şekilleri, en sonunda da “bu bir kedi” fikrini yakalaması tam olarak bu katmanlı maceradır.
``

## Neden “derin” denir?

Klasik bir yapay sinir ağı genellikle giriş, bir veya birkaç gizli katman ve çıkış katmanından oluşur. Derin öğrenmede ise gizli katman sayısı belirgin biçimde artar. Ancak derinlik sadece “daha çok katman” demek değildir; her katman, önceki katmanın ürettiği temsili dönüştürerek daha anlamlı bir soyutlama seviyesi oluşturur.

Bir nöronun temel hesabı şu şekilde ifade edilebilir:

$$z = \sum_{i=1}^{n} w_i x_i + b$$

Burada $x_i$ girişleri, $w_i$ ağırlıkları ve $b$ bias (sapma) değerini temsil eder. Ardından doğrusal olmayan bir aktivasyon uygulanır:

$$a = f(z)$$

Aktivasyon fonksiyonu kritik bir oyuncudur. Eğer tüm katmanlar yalnızca doğrusal işlem yapsaydı, yüz katmanlı bir ağ bile tek bir doğrusal dönüşüme indirgenebilirdi. ReLU, sigmoid veya tanh gibi fonksiyonlar modele karmaşık örüntüleri öğrenme gücü verir.

| Yaklaşım | Özellik çıkarımı | Veri ihtiyacı | Tipik kullanım |
|---|---|---:|---|
| Geleneksel makine öğrenmesi | Uzman tarafından elle tasarlanır | Görece az | Tablo verileri, basit sınıflandırma |
| Sığ sinir ağı | Sınırlı otomatik öğrenme | Orta | Basit tahmin problemleri |
| Derin öğrenme | Katmanlar tarafından otomatik öğrenilir | Genellikle yüksek | Görüntü, ses, metin, video |

## Katmanların öğrenme hiyerarşisi

Bir evcil hayvan fotoğrafını sınıflandıran evrişimsel sinir ağını düşünelim. İlk katmanlar kontrast, çizgi ve kenar gibi düşük seviyeli sinyalleri algılar. Orta katmanlar kulak, göz, kürk deseni veya pati gibi parçaları birleştirir. Son katmanlar ise bu parçaların ilişkisini değerlendirerek “kedi” ya da “köpek” kararına ulaşır. Bu nedenle derin öğrenme, özellikle ham verinin çok karmaşık olduğu alanlarda parlaktır.

Eğitim sürecinde modelin tahmini ile gerçek etiket arasındaki fark bir kayıp fonksiyonuyla ölçülür. Örneğin sınıflandırmada çapraz entropi kaybı yaygındır. Ardından geri yayılım (backpropagation), hatanın her ağırlığa ne kadar bağlı olduğunu hesaplar. Gradyan inişi de ağırlıkları hata azalacak yönde günceller:

$$w \leftarrow w - \eta \frac{\partial L}{\partial w}$$

Burada $L$ kayıp fonksiyonu, $\eta$ ise öğrenme oranıdır. Öğrenme oranı fazla büyükse model hedefi ıskalayarak zıplayabilir; çok küçükse eğitim bir kaplumbağa hızına düşebilir.

## Küçük bir ağ örneği

Aşağıdaki Keras kodu, el yazısı rakamları için basit ama derin sayılabilecek bir sınıflandırıcı kurar. `Dense` katmanları tam bağlı katmanlardır; `Dropout` ise ezberlemeyi azaltmak için eğitim sırasında bazı bağlantıları geçici olarak kapatır.

```python
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout

model = Sequential([
    Dense(256, activation="relu", input_shape=(784,)),
    Dropout(0.2),
    Dense(128, activation="relu"),
    Dense(10, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(x_train, y_train, epochs=10, validation_split=0.1)
```

Son katmandaki `softmax`, 10 rakam sınıfı için olasılık dağılımı üretir. En yüksek olasılık modelin tahmini olur.

| Kavram | Avantajı | Dikkat edilmesi gereken |
|---|---|---|
| Çok gizli katman | Karmaşık temsiller öğrenir | Aşırı öğrenme riski |
| ReLU | Hızlı ve yaygın | Ölü nöron problemi |
| Dropout | Genellemeyi iyileştirir | Eğitim süresini uzatabilir |
| GPU kullanımı | Büyük hesapları hızlandırır | Donanım ve maliyet gerektirir |

Derin öğrenmenin sihri, veriyi yalnızca sayılar yığını olarak görmemesinde yatar: Katmanlar, bu sayıların içindeki anlam hiyerarşisini keşfetmeye çalışır. Doğru veri, uygun mimari ve dikkatli eğitim birleştiğinde bu yaklaşım; görüntü tanımadan dil modellerine kadar şaşırtıcı derecede güçlü sonuçlar üretir.

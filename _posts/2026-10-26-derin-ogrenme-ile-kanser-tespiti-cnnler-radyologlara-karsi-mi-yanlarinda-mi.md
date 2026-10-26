---
layout: post
title: "Derin Öğrenme ile Kanser Tespiti: CNN’ler Radyologlara Karşı mı, Yanlarında mı?"
math: true
categories: 
  - Bilgi
tags: 
  - derin öğrenme
  - yapay zeka
  - kanser tespiti
  - cnn
  - radyoloji
  - tıbbi görüntüleme
toc: true
image: /img/derin-ogrenme-ile-38.png
---

Bir akciğer tomografisindeki birkaç milimetrelik nodülü veya mamografideki belirsiz bir dokuyu fark etmek, radyologlar için dikkat ve deneyim gerektiren bir süreçtir. Derin öğrenme modelleri ise binlerce görüntüden örüntü öğrenerek bu sürece ikinci bir göz olarak katılabilir. Peki evrişimli sinir ağları gerçekten insan uzmanlardan daha başarılı mı, yoksa mesele insan-makine iş birliği mi?


![derin-ogrenme-ile-38](/img/derin-ogrenme-ile-38.svg)

``

## Evrişimli sinir ağı neyi öğrenir?

Evrişimli sinir ağları, yani **CNN’ler**, görüntülerdeki uzamsal ilişkileri öğrenmek için geliştirilmiştir. İlk katmanlar kenar, köşe ve doku gibi basit özellikleri yakalarken daha derin katmanlar kitle biçimi, düzensiz sınır veya doku yoğunluğu gibi karmaşık örüntülere odaklanır.

Bir evrişim işlemi kabaca şöyle ifade edilir:

$$
y_{i,j} = \sum_m \sum_n x_{i+m,j+n} w_{m,n} + b
$$

Burada $x$ giriş görüntüsünü, $w$ öğrenilebilir filtreyi, $b$ sapma değerini ve $y$ üretilen özellik haritasını temsil eder. Filtre görüntü üzerinde dolaşır; önemli bölgelerde yüksek aktivasyonlar oluşturur. Model, eğitim sırasında hatasını azaltacak filtreleri kendisi öğrenir.

Kanser tespitinde süreç genellikle görüntü sınıflandırma, tümör konumlandırma veya piksel düzeyinde segmentasyon biçiminde tasarlanır. Örneğin bir model yalnızca “şüpheli” sonucunu verebilirken başka bir model kitlenin sınırlarını da işaretleyebilir.

## İnsan ve CNN karşılaştırması

Bir sistemi yalnızca doğruluk oranıyla değerlendirmek yanıltıcıdır. Tıbbi taramalarda **duyarlılık** ve **özgüllük** özellikle önemlidir:

$$
\text{Duyarlılık} = \frac{TP}{TP + FN}
$$

$$
\text{Özgüllük} = \frac{TN}{TN + FP}
$$

Duyarlılığın düşük olması gerçek kanserlerin kaçırılması, özgüllüğün düşük olması ise çok sayıda sağlıklı hastanın gereksiz incelemeye yönlendirilmesi anlamına gelebilir.

| Özellik | CNN modeli | İnsan uzman |
|---|---|---|
| Hız | Binlerce görüntüyü hızlı tarayabilir | İnceleme süresi vakaya bağlıdır |
| Tutarlılık | Aynı girdiye genellikle aynı sonucu verir | Yorgunluk ve dikkat etkili olabilir |
| Bağlam | Klinik geçmişi sınırlı yorumlar | Belirti, öykü ve diğer testleri birleştirir |
| Açıklanabilirlik | Karar süreci çoğu zaman opaktır | Gerekçesini tıbbi dille açıklayabilir |
| Nadir vakalar | Eğitim verisi azsa zorlanabilir | Deneyim ve literatürden yararlanabilir |

Araştırmalarda bazı CNN’ler belirli veri kümelerinde uzmanlarla benzer, hatta daha yüksek sonuçlar elde edebilir. Ancak bu, modelin her hastanede aynı başarıyı göstereceği anlamına gelmez. Cihaz markası, çekim protokolü, hasta popülasyonu ve görüntü kalitesi değiştiğinde **veri dağılımı kayması** ortaya çıkabilir.

## Basitleştirilmiş bir CNN örneği

Aşağıdaki TensorFlow modeli, görüntüleri iki sınıfa ayırabilecek temel bir mimari gösterir:

```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(224, 224, 3)),
    tf.keras.layers.Conv2D(32, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)
```

Evrişim katmanları görüntü özelliklerini çıkarır, havuzlama katmanları boyutu küçültür, sigmoid çıkışı ise görüntünün şüpheli sınıfa ait olma olasılığını üretir. Gerçek bir klinik sistemde veri artırma, hasta bazlı veri ayrımı, harici doğrulama ve kalibrasyon gibi ek adımlar zorunludur.

## Rakip değil, ekip arkadaşı

CNN’lerin en güçlü kullanım biçimi radyologların yerini almak değil, önceliklendirme ve karar desteği sağlamaktır. Model şüpheli görüntüleri sıranın başına taşıyabilir, gözden kaçabilecek bölgeleri işaretleyebilir ve ikinci okuma sunabilir. Buna karşılık nihai karar; biyopsi, hasta geçmişi ve diğer klinik bulgularla birlikte uzman tarafından verilmelidir.

Ayrıca eğitim verilerindeki demografik dengesizlikler adaletsiz sonuçlara yol açabilir. Bu nedenle başarı ölçümleri yaş, cinsiyet, cihaz ve merkez gibi alt gruplarda ayrı ayrı incelenmelidir. Güvenli gelecek, “yapay zekâ mı insan mı?” sorusundan çok, **ikisini nasıl denetimli ve şeffaf biçimde birleştiririz?** sorusuna bağlıdır.

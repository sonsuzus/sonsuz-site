---
layout: post
title: "Akıllı Protezler: Düşünceden Harekete Uzanan Biyonik Köprü"
math: true
categories: 
  - Bilgi
tags: 
  - akıllı protezler
  - biyonik
  - sinirbilim
  - yapay zeka
  - biyomedikal
  - makine öğrenmesi
toc: true
image: /img/akilli-protezler-dusunceden-75.png
---

Bir bardağı tutmayı yalnızca düşünerek gerçekleştirdiğinizi hayal edin. Akıllı protezler, kaslarda ve sinirlerde oluşan elektriksel sinyalleri yorumlayarak bu düşünceyi mekanik harekete dönüştürür. Bilim kurgu filmlerindeki robot kolları hatırlatsa da bu teknoloji bugün laboratuvarlardan çıkıp gerçek kullanıcıların günlük yaşamına girmeye başlamış durumda.

``

## Sinir sistemi protezle nasıl konuşur?

Beyin bir hareket başlatmak istediğinde omurilik ve çevresel sinirler üzerinden kaslara elektriksel komutlar gönderir. Bir uzuv kaybedilmiş olsa bile geride kalan sinirler çoğu zaman bu komutları üretmeye devam eder. Elektromiyografi adı verilen yöntem, kasların üzerindeki elektrotlarla bu elektriksel etkinliği ölçer.

Ölçülen ham sinyal genellikle gürültülüdür. Kalp atışı, elektrotun kayması ve çevredeki elektronik cihazlar ölçümü etkileyebilir. Bu nedenle sinyal önce filtrelenir, ardından küçük zaman pencerelerine bölünür. Her pencereden ortalama mutlak değer, varyans veya frekans enerjisi gibi özellikler çıkarılır.

Bir sinyalin basitleştirilmiş enerji ölçümü şöyle ifade edilebilir:

$$E = \sum_{i=1}^{N} x_i^2$$

Burada $x_i$ ölçülen sinyal örneğini, $N$ ise pencere içindeki örnek sayısını gösterir. Kas daha güçlü kasıldığında enerji çoğunlukla yükselir. Ancak farklı hareketleri ayırmak için yalnızca enerji yetmez; sinyalin zamansal ve frekans özellikleri birlikte değerlendirilir.

## Komuttan mekanik harekete

Sistemin işleyişi dört temel aşamaya ayrılır:

1. Elektrotlar sinir veya kas sinyalini toplar.
2. Filtreleme işlemi paraziti azaltır.
3. Bir makine öğrenmesi modeli hareket niyetini sınıflandırır.
4. Denetleyici, protezin motorlarına uygun komutları yollar.

Örneğin model, sinyali “eli aç”, “yumruk yap” veya “bileği döndür” sınıflarından birine yerleştirebilir. Motor komutu için basit bir oransal denetim kullanılabilir:

$$u = K(e)$$

Burada $e$, hedef konum ile mevcut konum arasındaki fark; $K$ ise tepki kuvvetini belirleyen katsayıdır. Büyük hata daha güçlü motor komutu üretir.

| Yaklaşım | Avantajı | Sınırlaması |
|---|---|---|
| Yüzey EMG | Ameliyat gerektirmez | Elektrot kaymasından etkilenir |
| İmplante elektrot | Daha temiz sinyal sağlar | Cerrahi işlem gerektirir |
| Kural tabanlı kontrol | Basit ve hızlıdır | Karmaşık hareketlerde yetersizdir |
| Makine öğrenmesi | Kullanıcıya uyarlanabilir | Eğitim verisine ihtiyaç duyar |

## Küçük bir hareket sınıflandırıcısı

Aşağıdaki Python örneği, önceden çıkarılmış sinyal özelliklerinden hareket türünü öğrenen basit bir modeli gösterir:

```python
from sklearn.ensemble import RandomForestClassifier

# Her satır: enerji, ortalama genlik ve frekans özelliği
X = [[0.2, 0.1, 15], [0.8, 0.7, 32],
     [0.3, 0.2, 18], [0.9, 0.8, 35]]
y = ["ac", "kapat", "ac", "kapat"]

model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X, y)

yeni_sinyal = [[0.75, 0.68, 30]]
print(model.predict(yeni_sinyal)[0])
```

Bu kod doğrudan bir protezi yönetmez; sinyal çözümleme mantığının sadeleştirilmiş bir örneğidir. Gerçek sistemlerde binlerce örnek, gerçek zamanlı veri akışı ve güvenlik kontrolleri bulunur. Yanlış bir tahminin bardağı kırabileceği düşünülürse düşük gecikme kadar güvenilirlik de önemlidir.

## Dokunmayı geri getirmek mümkün mü?

Akıllı protezlerin en heyecan verici yönü çift yönlü iletişimdir. Basınç sensörleri, parmak ucundaki kuvveti ölçerek sinirlere kontrollü elektrik darbeleri gönderebilir. Böylece kullanıcı yalnızca protezi hareket ettirmez; tuttuğu nesnenin sertliği veya kaymak üzere olduğu hakkında geri bildirim de alabilir.

Gelecekte daha küçük elektrotlar, enerji verimli motorlar ve kullanıcıyla birlikte öğrenen algoritmalar göreceğiz. Bununla birlikte mahremiyet, bakım maliyeti, siber güvenlik ve erişilebilirlik unutulmamalıdır. Çünkü sinir sinyali yalnızca teknik veri değil, insan bedenine ait son derece kişisel bir bilgidir. Başarılı bir akıllı protez, metal ve koddan fazlasıdır: İnsan niyetiyle makine hareketi arasında güvenilir, sezgisel ve güvenli bir köprüdür.

![akilli-protezler-dusunceden-75](/img/akilli-protezler-dusunceden-75.svg)


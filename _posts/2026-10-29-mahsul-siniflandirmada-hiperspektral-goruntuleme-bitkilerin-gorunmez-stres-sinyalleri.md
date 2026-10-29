---
layout: post
title: "Mahsul Sınıflandırmada Hiperspektral Görüntüleme: Bitkilerin Görünmez Stres Sinyalleri"
math: true
categories: 
  - Bilgi
tags: 
  - hiperspektral görüntüleme
  - tarım teknolojileri
  - makine öğrenmesi
  - görüntü işleme
  - uzaktan algılama
  - bitki stresi
toc: true
image: /img/mahsul-siniflandirmada-hiperspektral-22.png
---

Bir yaprak insan gözüne capcanlı yeşil görünürken susuzluk, mineral eksikliği veya hastalık nedeniyle çoktan alarm vermeye başlamış olabilir. Normal kameralar bu erken sinyalleri çoğu zaman kaçırır; hiperspektral kameralar ise görünür ışığın ötesindeki dalga boylarını inceleyerek bitkinin adeta biyokimyasal parmak izini çıkarır. Böylece tarla tamamen sararmadan önce hangi mahsulün sağlıklı, stresli veya hastalıklı olduğu belirlenebilir.

``

## Pikselden Spektral İmza Çıkarmak

Standart bir RGB kamera her pikseli kırmızı, yeşil ve mavi olmak üzere üç değerle temsil eder. Hiperspektral görüntüleme ise elektromanyetik spektrumu onlarca, hatta yüzlerce dar banda ayırır. Sonuç, iki uzamsal ve bir spektral boyuta sahip bir **veri küpüdür**:

$$I(x,y,\lambda)$$

Burada $x$ ve $y$ pikselin konumunu, $\lambda$ ise ölçülen dalga boyunu gösterir. Örneğin bir sistem 400–1000 nm aralığında 200 bant kaydedebilir. Her piksel için elde edilen yansıma eğrisi, o noktadaki bitkinin su, pigment ve hücre yapısı hakkında bilgi taşır.

| Özellik | RGB kamera | Hiperspektral kamera |
|---|---|---|
| Bant sayısı | 3 | Onlarca veya yüzlerce |
| Algılanan bölge | Genellikle görünür ışık | Görünür ve yakın kızılötesi |
| Veri boyutu | Düşük | Çok yüksek |
| Erken stres tespiti | Sınırlı | Güçlü |
| Temel kullanım | Renk ve şekil | Kimyasal ve fizyolojik farklılık |

![mahsul-siniflandirmada-hiperspektral-22](/img/mahsul-siniflandirmada-hiperspektral-22.svg)


## Bitki Stresi Neden Görünmezken Yakalanabilir?

Sağlıklı yaprak klorofili, mavi ve kırmızı ışığı güçlü biçimde soğururken yeşil ışığı daha fazla yansıtır. Bu nedenle yaprakları yeşil görürüz. Yakın kızılötesi bölgede ise yansımayı yaprağın hücresel yapısı belirler. Susuzluk, mantar enfeksiyonu veya azot eksikliği başladığında klorofil yoğunluğu, su içeriği ve hücre düzeni değişir. İnsan gözü henüz fark görmese bile spektral eğri kaymaya başlar.

Bitki analizinde sık kullanılan göstergelerden biri NDVI değeridir:

$$NDVI = \frac{NIR-Red}{NIR+Red}$$

Yüksek NDVI genellikle yoğun ve sağlıklı bitki örtüsüne işaret eder. Ancak hiperspektral sistemlerin asıl avantajı, yalnızca iki bandı değil bütün spektral profili kullanabilmesidir. Böylece su stresi ile besin eksikliği gibi görsel açıdan benzer durumlar birbirinden ayrılabilir.

## Sınıflandırma Süreci

Tipik bir projede önce görüntüler sensör gürültüsünden ve aydınlatma farklarından arındırılır. Karanlık ve beyaz referans ölçümleriyle yansıma değeri yaklaşık olarak şöyle hesaplanır:

$$R = \frac{I-D}{W-D}$$

Burada $I$ ham görüntü, $D$ karanlık referans, $W$ ise beyaz referanstır. Ardından PCA gibi boyut indirgeme yöntemleri uygulanabilir. Son aşamada Destek Vektör Makineleri, Random Forest veya sinir ağlarıyla sağlıklı, susuz, hastalıklı ve besin eksikliği bulunan örnekler sınıflandırılır.

Aşağıdaki Python örneği, spektral ölçümler üzerinde Random Forest modeli kurar:

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# X: örneklerin spektral bantları, y: stres sınıfları
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)

model = RandomForestClassifier(
    n_estimators=200, max_depth=12, random_state=42
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print(classification_report(y_test, predictions))
```

Bu kod, her bitki örneğinin bant değerlerini özellik olarak kullanır ve karar ağaçlarından oluşan bir toplulukla stres türünü tahmin eder. `stratify` parametresi sınıf oranlarını korurken rapor; kesinlik, duyarlılık ve F1 skorlarını gösterir.

## Tarladan Geleceğe

Hiperspektral kameralar drone, uydu veya traktör üzerine yerleştirilebilir. Üretici böylece yalnızca sorunlu bölgelere su, gübre ya da ilaç uygulayabilir. Bununla birlikte yüksek cihaz maliyeti, büyük veri hacmi ve değişken güneş ışığı önemli zorluklardır. Yine de daha ucuz sensörler ve güçlü yapay zekâ modelleri sayesinde teknoloji hızla erişilebilir hâle geliyor. Kısacası geleceğin tarlasında bitkiler konuşmayacak; fakat spektrumları onların yerine oldukça ayrıntılı konuşacak.

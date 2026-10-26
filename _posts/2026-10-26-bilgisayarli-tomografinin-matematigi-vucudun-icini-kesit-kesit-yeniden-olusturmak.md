---
layout: post
title: "Bilgisayarlı Tomografinin Matematiği: Vücudun İçini Kesit Kesit Yeniden Oluşturmak"
math: true
categories: 
  - Bilgi
tags: 
  - bilgisayarlı tomografi
  - matematik
  - radon dönüşümü
  - görüntü işleme
  - python
  - tıbbi görüntüleme
toc: true
image: /img/bilgisayarli-tomografinin-matematigi-82.png
---

Bir bilgisayarlı tomografi cihazı, vücudun içine yerleştirilmiş görünmez bir fotoğraf makinesi değildir. Aslında farklı açılardan çok sayıda X-ışını ölçümü yapar ve bu ölçümlerin arkasındaki matematiksel bulmacayı çözerek kesit görüntüleri üretir. Başka bir deyişle cihaz, doğrudan görüntü çekmek yerine gölgelerden üç boyutlu bir hikâye yazar.

``

## X-ışınları bize ne söyler?

X-ışını demeti vücuttan geçerken kemik, kas, yağ ve hava tarafından farklı oranlarda soğurulur. Bu davranış yaklaşık olarak Beer–Lambert yasasıyla açıklanır:

$$I = I_0 e^{-\int_L \mu(x,y)\,ds}$$

Burada $I_0$ başlangıçtaki, $I$ dedektöre ulaşan ışın şiddetidir. $\mu(x,y)$ ise dokunun X-ışınını ne kadar zayıflattığını gösteren doğrusal soğurma katsayısıdır. İntegral, ışının izlediği $L$ yolu boyunca karşılaştığı bütün dokuların etkisini toplar.

Denklemin logaritmasını aldığımızda daha kullanışlı bir ölçüm elde ederiz:

$$p = -\ln\left(\frac{I}{I_0}\right)=\int_L \mu(x,y)\,ds$$

Yani dedektör, ışının geçtiği çizgi üzerindeki piksel değerlerinin toplamına benzer bir bilgi sağlar. Ancak tek bir toplamla hangi dokunun nerede olduğunu bilemeyiz. Bir alışveriş fişinin yalnızca toplam tutarını görüp sepetteki ürünleri tahmin etmeye çalışmak gibi!

## Radon dönüşümü: Gölgelerin kataloğu

Cihaz, X-ışını tüpünü hastanın çevresinde döndürerek farklı açılardan ölçümler toplar. Bir nesnenin belirli açılardaki çizgisel integrallerini hesaplayan matematiksel işleme **Radon dönüşümü** denir:

$$R(\theta,s)=\int\!\!\int \mu(x,y)\,\delta(s-x\cos\theta-y\sin\theta)\,dx\,dy$$

Burada $\theta$ tarama açısını, $s$ ise ışının merkezden uzaklığını belirtir. Bütün açılardan gelen ölçümler yan yana dizildiğinde **sinogram** adı verilen dalgalı bir görüntü oluşur. Noktasal bir nesne sinogramda sinüs eğrisi çizdiği için bu isim oldukça yerindedir.

| Kavram | Girdi | Çıktı | Benzetme |
|---|---|---|---|
| Radon dönüşümü | Kesit görüntüsü | Projeksiyonlar | Nesneden gölge üretmek |
| Ters Radon dönüşümü | Projeksiyonlar | Kesit görüntüsü | Gölgelerden nesneyi bulmak |
| Sinogram | Tüm açısal ölçümler | Ham veri haritası | Gölgelerin kataloğu |

![bilgisayarli-tomografinin-matematigi-82](/img/bilgisayarli-tomografinin-matematigi-82.svg)


## Geri projeksiyon neden tek başına yetmez?

Basit geri projeksiyonda her ölçüm, geldiği doğrultu boyunca görüntüye geri yayılır. Çok sayıda açı birleştirildiğinde nesne ortaya çıkar; fakat sonuç bulanıktır. Çünkü tek bir ölçüm, ait olduğu çizginin tamamına eşit biçimde dağıtılmıştır.

**Filtrelenmiş geri projeksiyon** bu sorunu azaltır. Önce projeksiyonlara yüksek frekansları güçlendiren bir rampa filtresi uygulanır, ardından veriler görüntü düzlemine geri taşınır:

$$\mu(x,y)=\int_0^\pi \widetilde{p}_\theta(x\cos\theta+y\sin\theta)\,d\theta$$

Buradaki $\widetilde{p}_\theta$, filtrelenmiş projeksiyondur. Filtre keskinliği artırırken gürültüyü de büyütebilir; dolayısıyla görüntü kalitesi ile radyasyon dozu arasında dikkatli bir denge kurulur.

## Küçük bir Python deneyi

Aşağıdaki örnek, yapay bir kesitin projeksiyonlarını üretir ve filtrelenmiş geri projeksiyonla görüntüyü yeniden oluşturur:

```python
from skimage.data import shepp_logan_phantom
from skimage.transform import radon, iradon, resize
import numpy as np

# İnsan başına benzeyen standart test kesiti
kesit = resize(shepp_logan_phantom(), (256, 256))

# Cihazın çevrede dolaştığı açıları temsil eder
acilar = np.linspace(0, 180, 256, endpoint=False)
sinogram = radon(kesit, theta=acilar)

# Ölçümlerden kesiti yeniden oluşturur
sonuc = iradon(sinogram, theta=acilar, filter_name="ramp")
```

Bu kodda `radon` ileri ölçüm sürecini, `iradon` ise rekonstrüksiyonu taklit eder. Açı sayısını azaltmak görüntüde çizgisel artefaktlar oluşturur; gerçek cihazlarda da yetersiz veri benzer sorunlara yol açar.

## Piksel değerlerinden doku bilgisine

Rekonstrüksiyon sonunda elde edilen soğurma katsayıları genellikle Hounsfield birimine dönüştürülür:

$$HU = 1000\frac{\mu-\mu_{su}}{\mu_{su}}$$

Su yaklaşık $0$ HU, hava $-1000$ HU, yoğun kemik ise yüzlerce veya binlerce HU değerine sahiptir. Böylece matematiksel bir yoğunluk haritası, doktorun yorumlayabileceği anatomik bir kesite dönüşür. Modern sistemler ayrıca iteratif yöntemler ve yapay zekâ kullanarak ölçüm ile tahmin arasındaki hatayı tekrar tekrar azaltır. Sonuçta tomografi, dönen bir X-ışını kaynağıyla başlayan ve ters problem çözümüyle tamamlanan etkileyici bir matematik mühendisliğidir.

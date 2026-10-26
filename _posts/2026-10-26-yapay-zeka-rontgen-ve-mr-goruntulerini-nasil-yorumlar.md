---
layout: post
title: "Yapay Zekâ Röntgen ve MR Görüntülerini Nasıl Yorumlar?"
math: true
categories: 
  - Bilgi
tags: 
  - yapay zekâ
  - tıbbi görüntüleme
  - derin öğrenme
  - röntgen
  - manyetik rezonans
  - bilgisayarlı görü
toc: true
image: /img/yapay-zeka-rontgen-97.png
---

![yapay-zeka-rontgen-97](/img/yapay-zeka-rontgen-97.svg)


Bir radyolog röntgene baktığında kenarları, yoğunluk farklılıklarını ve anatomik ilişkileri değerlendirir. Bilgisayar ise görüntüyü önce sayılardan oluşan dev bir tablo olarak görür. Yapay zekânın başarısı, bu sayısal desenlerle kırık, tümör veya doku bozukluğu gibi klinik bulgular arasındaki ilişkiyi öğrenmesinden gelir. Yine de bu teknoloji “dijital doktor” değil; hekimin kararını destekleyen güçlü bir araçtır.
``

## Görüntü bilgisayar için ne anlama gelir?

Gri tonlu bir tıbbi görüntü, her hücresinde parlaklık değeri bulunan bir matristir. Basitleştirilmiş biçimde görüntüyü $I(x,y)$ ile gösterebiliriz. Buradaki $x$ ve $y$ pikselin konumunu, $I$ ise yoğunluğunu ifade eder.

Röntgende yoğun dokular ışını daha fazla soğurduğu için kemikler genellikle parlak görünür. MR ise hidrojen çekirdeklerinin manyetik alandaki davranışını ölçer. Bu nedenle aynı anatomik bölge, kullanılan MR sekansına göre farklı görünebilir.

| Özellik | Röntgen | MR |
|---|---|---|
| Temel fizik | X-ışını soğurulması | Manyetik alan ve radyo dalgaları |
| Güçlü olduğu alan | Kemik, akciğer, hızlı tarama | Beyin, kas, bağ ve yumuşak doku |
| Görüntü yapısı | Çoğunlukla 2B | Genellikle çok kesitli 3B hacim |
| Yapay zekâ görevi | Sınıflandırma, kırık bulma | Segmentasyon, hacim ve lezyon analizi |

## Model nasıl öğrenir?

Önce uzmanlar tarafından etiketlenmiş çok sayıda görüntü hazırlanır. “Normal”, “zatürre şüphesi” veya lezyon sınırları gibi etiketler, modelin öğrenme hedefidir. Evrişimli sinir ağları (CNN), küçük filtreleri görüntü üzerinde gezdirerek kenar, doku ve şekil gibi özellikleri çıkarır.

Bir evrişim işlemi kabaca şöyle yazılır:

$$F(i,j)=\sum_m\sum_n I(i+m,j+n)K(m,n)$$

Burada $K$, belirli bir görsel deseni arayan filtredir. İlk katmanlar çizgileri öğrenirken daha derin katmanlar nodül veya anatomik yapı gibi karmaşık örüntülere duyarlı hâle gelir. Vision Transformer modelleri ise görüntüyü küçük parçalara ayırıp uzak bölgeler arasındaki ilişkileri “dikkat” mekanizmasıyla inceler.

Eğitim sırasında tahmin ile gerçek etiket arasındaki hata hesaplanır. İkili sınıflandırmada sık kullanılan kayıp fonksiyonu şöyledir:

$$L=-[y\log(p)+(1-y)\log(1-p)]$$

Model, bu değeri küçültecek şekilde milyonlarca parametresini günceller.

## Tipik analiz hattı

Aşağıdaki örnek, eğitilmiş bir modelle görüntü sınıflandırma sürecinin sadeleştirilmiş hâlidir:

```python
from PIL import Image
from torchvision import transforms

pipeline = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    transforms.Normalize([0.5] * 3, [0.5] * 3)
])

image = Image.open("rontgen.png")
tensor = pipeline(image).unsqueeze(0)
probability = model(tensor).sigmoid().item()
print(f"Şüpheli bulgu olasılığı: {probability:.2%}")
```

Kod görüntüyü standart boyuta getirir, sayısal tensöre dönüştürür ve modele verir. Çıkan olasılık kesin tanı değildir; yalnızca modelin öğrendiği verilere göre ürettiği bir skordur.

## Sınıflandırmadan segmentasyona

Sınıflandırma, görüntünün tamamına bir etiket verir. Nesne tespiti şüpheli bölgeyi kutuyla işaretler. Segmentasyon ise her pikseli ayrı ayrı değerlendirerek tümörün sınırlarını çizebilir. MR analizinde U-Net gibi mimariler bu yüzden oldukça popülerdir.

| Görev | Çıktı | Örnek kullanım |
|---|---|---|
| Sınıflandırma | Etiket veya olasılık | Normal/anormal ayrımı |
| Tespit | Sınırlayıcı kutu | Akciğer nodülü bulma |
| Segmentasyon | Piksel maskesi | Beyin tümörü hacmini ölçme |

## Neden insan denetimi şart?

Farklı hastanelerin cihazları, çekim protokolleri ve hasta grupları değişebilir. Model yalnızca belirli cihazlarda eğitildiyse başka bir merkezde başarısı düşebilir. Ayrıca veri dengesizliği, yanlış etiketler ve açıklanabilirlik sorunları hatalı sonuçlara yol açabilir.

Bu nedenle modeller bağımsız veri kümelerinde test edilir; duyarlılık, özgüllük ve ROC-AUC gibi ölçütlerle değerlendirilir. Isı haritaları modelin hangi bölgelere baktığını gösterebilse de klinik gerekçe yerine geçmez. En güvenli yaklaşım, yapay zekânın yorulmadan tarama yaptığı, radyoloğun ise bağlamı, hasta öyküsünü ve belirsizliği yönettiği insan-makine iş birliğidir.

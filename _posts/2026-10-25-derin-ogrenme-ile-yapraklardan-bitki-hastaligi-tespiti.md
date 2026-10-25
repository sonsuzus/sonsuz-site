---
layout: post
title: "Derin Öğrenme ile Yapraklardan Bitki Hastalığı Tespiti"
math: true
categories: 
  - Proje
tags: 
  - derin öğrenme
  - evrişimli sinir ağları
  - görüntü işleme
  - python
  - pytorch
  - tarım teknolojileri
toc: true
image: /img/derin-ogrenme-ile-50.png
---

Bir yaprağın üzerindeki küçük kahverengi lekeler çiftçi için ciddi bir uyarı, evrişimli sinir ağı içinse sınıflandırılmayı bekleyen görsel örüntülerdir. Derin öğrenme sayesinde yaprak fotoğraflarını analiz ederek bitkinin sağlıklı olup olmadığını ve olası hastalık türünü otomatik biçimde tahmin edebiliriz. Böyle bir sistem, uzmanların yerini almak yerine erken tarama yapan dijital bir tarım asistanı gibi çalışır.

``

## Evrişimli sinir ağı neyi öğrenir?

Klasik makine öğrenmesinde renk, kenar veya doku gibi özellikleri elle çıkarmamız gerekir. Evrişimli sinir ağları, yani CNN'ler, uygun özellikleri eğitim verisinden kendileri öğrenir. İlk katmanlar yaprak kenarlarını ve renk geçişlerini; daha derin katmanlar ise pas lekesi, küf dokusu veya damar bozulması gibi karmaşık yapıları yakalayabilir.

Bir evrişim filtresinin görüntü üzerindeki temel işlemi şöyle gösterilebilir:

$$
Y(i,j)=\sum_m\sum_n X(i+m,j+n)K(m,n)+b
$$

Burada $X$ giriş görüntüsünü, $K$ öğrenilen filtreyi, $b$ sapmayı ve $Y$ özellik haritasını temsil eder. Modelin son katmanındaki **softmax**, her hastalık için olasılık üretir:

$$
P(y=k)=\frac{e^{z_k}}{\sum_{j=1}^{C}e^{z_j}}
$$

| Yaklaşım | Özellik çıkarımı | Veri ihtiyacı | Esneklik |
|---|---|---:|---|
| Geleneksel makine öğrenmesi | Elle tasarlanır | Orta | Sınırlı |
| Sıfırdan CNN eğitimi | Otomatik | Yüksek | Yüksek |
| Transfer öğrenme | Önceden öğrenilmiş | Daha düşük | Çok yüksek |

Küçük ve orta ölçekli tarım veri kümelerinde transfer öğrenme genellikle en pratik seçenektir. ImageNet üzerinde eğitilmiş ResNet veya EfficientNet gibi bir model, görsel dünyaya ilişkin temel bilgisini yapraklara aktarabilir.

## Veri hazırlığı: Modelin gerçek besini

Fotoğraflar hastalık sınıflarına göre klasörlenebilir. Veri; eğitim, doğrulama ve test kümelerine ayrılmalıdır. Aynı yaprağın farklı çekimlerinin iki ayrı kümeye düşmesi **veri sızıntısına** yol açar ve gerçekte başarısız olan modeli kâğıt üzerinde dâhi gibi gösterebilir.

Döndürme, kırpma, parlaklık değiştirme ve yatay çevirme gibi veri artırma işlemleri modeli farklı çekim koşullarına hazırlar. Ancak yaprağın doğal görünümünü bozacak aşırı renk dönüşümleri kullanılmamalıdır. Ayrıca sınıflar dengesizse ağırlıklı kayıp fonksiyonu veya örnekleme yöntemleri düşünülmelidir.

## PyTorch ile transfer öğrenme

Aşağıdaki örnek, önceden eğitilmiş ResNet18 modelinin son katmanını hastalık sınıflarına uyarlayarak tek bir eğitim adımı gerçekleştirir:

```python
import torch
from torch import nn
from torchvision.models import resnet18, ResNet18_Weights

sinif_sayisi = 5
model = resnet18(weights=ResNet18_Weights.DEFAULT)
model.fc = nn.Linear(model.fc.in_features, sinif_sayisi)

kayip_fonksiyonu = nn.CrossEntropyLoss()
optimizasyon = torch.optim.Adam(model.parameters(), lr=1e-4)

model.train()
gorseller, etiketler = next(iter(egitim_yukleyici))
optimizasyon.zero_grad()
tahminler = model(gorseller)
kayip = kayip_fonksiyonu(tahminler, etiketler)
kayip.backward()
optimizasyon.step()
```

`CrossEntropyLoss`, doğru sınıfın olasılığını yükseltmesi için modeli cezalandırır; `backward()` gradyanları hesaplar, `step()` ise ağırlıkları günceller. Görsellerin modelin beklediği boyuta ve normalizasyon değerlerine dönüştürülmesi gerektiği unutulmamalıdır.

## Başarıyı doğru ölçmek

Yalnızca doğruluk değerine bakmak yanıltıcı olabilir. Özellikle nadir hastalıklarda precision, recall, F1 skoru ve karmaşıklık matrisi birlikte incelenmelidir. Yanlış negatif sonuç, hasta bitkinin sağlıklı ilan edilmesi anlamına geldiğinden tarımsal kullanımda çoğu zaman daha kritiktir.

Model farklı telefonlar, ışık koşulları, arka planlar ve bitki çeşitleri üzerinde de sınanmalıdır. Grad-CAM gibi açıklanabilirlik teknikleri, ağın gerçekten lekeye mi yoksa arka plandaki saksıya mı baktığını gösterir. Böylece proje yalnızca yüksek puan alan bir deney olmaktan çıkar, tarlada güvenilebilecek kullanışlı bir yardımcıya dönüşür.

![derin-ogrenme-ile-50](/img/derin-ogrenme-ile-50.svg)


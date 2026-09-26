---
layout: post
title: "Transfer Öğrenme ile Küçük Veriden Büyük Sonuçlar Çıkarmak"
math: true
categories: 
  - Bilgi
tags: 
  - transfer öğrenme
  - makine öğrenmesi
  - derin öğrenme
  - yapay zeka
  - python
  - pytorch
toc: true
image: /img/transfer-ogrenme-ile-22.png
---

Bir görüntü sınıflandırma modeli geliştirmek istiyorsunuz ancak elinizde yalnızca birkaç yüz örnek var. Sıfırdan eğitilen dev bir sinir ağı bu veriyi ezberleyip gerçek dünyada tökezleyebilir. Neyse ki teknoloji devlerinin milyonlarca örnekle eğittiği modellerin öğrendiği zihinsel haritaları ödünç alabiliriz. **Transfer öğrenme**, küçük veri setlerinin süper gücü tam olarak budur.
``

## Transfer öğrenme nedir?

Derin sinir ağlarının ilk katmanları kenar, renk ve doku gibi genel örüntüleri; ilerleyen katmanları ise nesne parçaları ve sınıfa özgü yapıları öğrenir. Bir kediyi tanımak için öğrenilen kenar dedektörleri, otomobil veya yaprak sınıflandırırken de işe yarar. Böylece modelin bütün bilgisini çöpe atmak yerine yalnızca probleminize özgü bölümünü değiştirirsiniz.

Kaynak görevde öğrenilen parametreleri $w_s$, hedef görev için aradığımız parametreleri $w_t$ ile gösterelim. Transfer öğrenmenin temel fikri şudur:

$$w_t^{(0)} = w_s$$

Yani hedef model rastgele başlamaz; eğitim maratonuna başlangıç çizgisinden değil, parkurun büyük bölümünü tamamlamış halde girer. Ardından hedef veri üzerindeki kayıp fonksiyonu küçültülür:

$$w_t^* = \arg\min_w \frac{1}{N}\sum_{i=1}^{N} L(f(x_i;w), y_i)$$

$N$ küçük olduğunda iyi bir başlangıç noktası, aşırı öğrenme riskini ciddi biçimde azaltabilir.

## İki temel strateji

| Strateji | Katmanların durumu | Veri ihtiyacı | Ne zaman kullanılmalı? |
|---|---|---:|---|
| Özellik çıkarımı | Omurga dondurulur | Çok düşük | Veri az ve kaynak görev benzerse |
| İnce ayar | Bazı katmanlar açılır | Orta | Veri daha fazla veya alan farklıysa |
| Sıfırdan eğitim | Tüm ağırlıklar rastgele | Çok yüksek | Büyük ve özgün bir veri seti varsa |

**Özellik çıkarımında** önceden eğitilmiş ağ sabit bir dönüştürücü gibi davranır. Sadece son sınıflandırma katmanı eğitilir. **İnce ayarda** ise üst katmanlardan bazıları düşük öğrenme oranıyla güncellenir. Bu, modele “Bildiklerini unutma ama bizim lehçemizi de öğren” demektir.

## PyTorch ile uygulama

Aşağıdaki örnek, ImageNet üzerinde eğitilmiş ResNet18 modelini üç sınıflı bir problem için hazırlar:

```python
import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights

model = resnet18(weights=ResNet18_Weights.DEFAULT)

# Önceden öğrenilmiş özellikleri koru.
for parameter in model.parameters():
    parameter.requires_grad = False

# Eski 1000 sınıflı çıkışı kendi problemimize uyarla.
input_features = model.fc.in_features
model.fc = nn.Linear(input_features, 3)
```

Burada omurganın parametreleri dondurulur, ancak yeni `model.fc` katmanı varsayılan olarak eğitilebilir durumdadır. Optimize ediciye yalnızca güncellenecek parametreleri vermek gereksiz hesaplamayı önler:

```python
import torch.optim as optim

optimizer = optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=1e-3
)
criterion = nn.CrossEntropyLoss()
```

İlk eğitimden sonra doğrulama başarımı tıkanırsa son katman grubunu açarak ince ayar yapabiliriz:

```python
for parameter in model.layer4.parameters():
    parameter.requires_grad = True

optimizer = optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=1e-5
)
```

Düşük öğrenme oranı önemlidir; büyük adımlar, önceden öğrenilmiş yararlı temsilleri bozarak **felaket unutmaya** yol açabilir.

## Küçük veriyi daha da verimli kullanmak

Veri artırma sırasında döndürme, kırpma, renk değişimi ve yatay çevirme gibi işlemler uygulanabilir. Ancak tıbbi görüntüler veya yönün anlam taşıdığı veriler için her dönüşüm mantıklı değildir. Dikey çevrilmiş bir trafik levhası modele yaratıcılık değil, kafa karışıklığı kazandırabilir.

Eğitim ve doğrulama kümelerini dikkatle ayırmak, sınıf dengesini izlemek ve erken durdurma kullanmak da önemlidir. Başarıyı yalnızca doğrulukla ölçmeyin; dengesiz veri setlerinde precision, recall ve F1 skoru daha açıklayıcıdır.

Transfer öğrenme sihirli değnek değildir: Kaynak ve hedef alanlar çok farklıysa **negatif transfer** oluşabilir. Yine de doğru model, kontrollü ince ayar ve gerçekçi doğrulama ile birkaç yüz örnekten şaşırtıcı derecede güçlü sistemler üretmek mümkündür. Kısacası devlerin omzuna çıkın; fakat direksiyonu kendi probleminize göre çevirmeyi unutmayın.

![transfer-ogrenme-ile-22](/img/transfer-ogrenme-ile-22.svg)


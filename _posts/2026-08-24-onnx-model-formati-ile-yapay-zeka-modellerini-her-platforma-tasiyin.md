---
layout: post
title: "ONNX Model Formatı ile Yapay Zeka Modellerini Her Platforma Taşıyın"
math: true
categories: 
  - Bilgi
tags: 
  - ONNX
  - Makine Öğrenmesi
  - Model Dağıtımı
---

Bir yapay zeka modelini eğitmek çoğu zaman işin heyecanlı kısmıdır; asıl macera ise modeli üretime taşırken başlar. PyTorch ile eğitilmiş bir modeli Java tabanlı bir serviste, C# masaüstü uygulamasında veya edge cihazda çalıştırmak istediğinizde framework bağımlılıkları hız kesebilir. ONNX (Open Neural Network Exchange), modeller için ortak bir dil sunarak bu taşınabilirlik problemini çözmeyi hedefleyen açık standarttır.
``

## ONNX Nedir ve Neden Gereklidir?

ONNX, bir modelin hesaplama grafiğini, katmanlarını, ağırlıklarını ve giriş-çıkış tanımlarını standart biçimde saklayan bir dosya formatıdır. Dosyalar genellikle `.onnx` uzantısına sahiptir. Amaç, eğitim framework'ü ile çıkarım (inference) ortamını birbirinden ayırmaktır.

Bir sinir ağını matematiksel olarak ardışık fonksiyonların bileşimi gibi düşünebiliriz:

$$
\hat{y} = f_n(f_{n-1}(\dots f_1(x)))
$$

ONNX, bu $f_i$ fonksiyonlarını düğümler; verinin dolaşımını ise kenarlar olarak tanımlayan bir hesaplama grafiği taşır. Örneğin `MatMul`, `Add`, `Relu` ve `Softmax` işlemleri grafik düğümleridir. Model parametreleri de bu grafiğe başlangıç değerleri olarak eklenir. Böylece aynı hesaplama mantığı, farklı çalışma zamanlarında yeniden yorumlanabilir.

| Kavram | Eğitim Framework'ü | ONNX Yaklaşımı |
|---|---|---|
| Ana amaç | Eğitim ve araştırma | Taşınabilir çıkarım |
| API bağımlılığı | Genellikle yüksek | Düşük |
| Dosya içeriği | Koda ve framework'e bağlı olabilir | Grafik + ağırlık + metadata |
| Hedef ortam | Çoğunlukla Python | Python, .NET, Java, C++, mobil ve edge |

## Opset: Modelin Sözlüğü

ONNX dosyasındaki en önemli ayrıntılardan biri *opset* sürümüdür. Opset, operatörlerin davranışını tanımlayan sürümlenmiş sözlüktür. Aynı `Resize` işlemi farklı opset sürümlerinde küçük ama kritik davranış farkları gösterebilir. Bu nedenle modeli dışa aktarırken hedef runtime'ın desteklediği opset sürümü seçilmelidir.

Uyumluluğu kabaca şu koşulla düşünebiliriz:

$$
\text{Uyumlu} \iff \text{Model Opset} \leq \text{Runtime'ın Desteklediği Opset}
$$

Bu eşitsizlik tek başına yeterli değildir; kullanılan operatörlerin ve dinamik şekillerin de runtime tarafından desteklenmesi gerekir. Yine de sorun giderme yolculuğunda opset kontrolü ilk duraktır.

## PyTorch Modelini ONNX'e Aktarmak

Aşağıdaki örnek, eğitilmiş bir PyTorch modelini ONNX biçimine dışa aktarır. `dummy_input`, modelin gerçek üretim girdisiyle aynı şekil ve veri türünde olmalıdır.

```python
import torch

model.eval()
dummy_input = torch.randn(1, 3, 224, 224)

torch.onnx.export(
    model,
    dummy_input,
    "siniflandirici.onnx",
    input_names=["image"],
    output_names=["logits"],
    dynamic_axes={"image": {0: "batch"}, "logits": {0: "batch"}},
    opset_version=17
)
```

Burada `model.eval()` dropout ve batch normalization gibi katmanların çıkarım modunda davranmasını sağlar. `dynamic_axes` ise sabit `1` yerine farklı batch boyutlarıyla tahmin yapılabilmesine olanak tanır. Ancak dinamik boyutları gereksiz yere açmak, bazı donanım hızlandırıcılarında optimizasyonu zorlaştırabilir.

## ONNX Runtime ile Tahmin Alma

ONNX Runtime, ONNX grafiğini CPU, CUDA, TensorRT veya farklı sağlayıcılarda çalıştırabilen yüksek performanslı bir motordur. Python tarafında temel kullanım şöyledir:

```python
import onnxruntime as ort
import numpy as np

session = ort.InferenceSession("siniflandirici.onnx")
image = np.random.randn(1, 3, 224, 224).astype(np.float32)

sonuc = session.run(["logits"], {"image": image})
print(sonuc[0].shape)
```

`session.run` çağrısındaki giriş adları, dışa aktarma sırasında verdiğiniz isimlerle birebir eşleşmelidir. Ayrıca PyTorch tensörleri çoğu zaman `float32` iken, NumPy girdisinin yanlışlıkla `float64` olması sık görülen bir hata kaynağıdır.

| Senaryo | ONNX'in Kazancı | Dikkat Edilecek Nokta |
|---|---|---|
| Python'dan .NET'e geçiş | Framework kurmadan çıkarım | Girdi ön işlemesini aynı tutmak |
| GPU sunucu dağıtımı | TensorRT gibi sağlayıcılar | Sağlayıcı ve CUDA uyumu |
| Mobil/edge cihaz | Daha hafif çalışma zamanı | Model boyutu ve operatör desteği |
| Çoklu dil desteği | Ortak model artefaktı | Opset sürümü |

Son olarak, ONNX dönüşümünü bir "kaydet ve unut" işlemi saymayın. Kaynak model ile ONNX çıktılarının sayısal olarak yakın olduğunu test edin. Örneğin ortalama mutlak hata için $MAE = \frac{1}{n}\sum_{i=1}^{n}|y_i-\hat{y}_i|$ ölçülebilir. Doğru doğrulama, ONNX'i sadece taşınabilir değil, güvenilir bir üretim köprüsü hâline getirir.

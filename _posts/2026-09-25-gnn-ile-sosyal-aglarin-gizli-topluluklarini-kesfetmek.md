---
layout: post
title: "GNN ile Sosyal Ağların Gizli Topluluklarını Keşfetmek"
math: true
categories: 
  - Bilgi
tags: 
  - gnn
  - graf sinir ağları
  - sosyal ağ analizi
  - topluluk tespiti
  - python
  - pytorch geometric
toc: true
image: /img/gnn-ile-sosyal-78.png
---

Bir sosyal ağı yalnızca “kim kimi takip ediyor?” sorusuyla incelemek, kalabalık bir partide sadece tokalaşmaları saymaya benzer. Oysa arkadaş grupları, ilgi toplulukları ve etkileşim çevreleri bağlantıların oluşturduğu daha büyük desenlerde saklıdır. Graph Neural Networks (GNN), düğüm özellikleriyle ağ yapısını birlikte öğrenerek bu gizli toplulukları ortaya çıkarabilir.

``

## Sosyal ağı graf olarak düşünmek

Bir sosyal ağ $G=(V,E)$ grafıyla temsil edilir. $V$ kullanıcıları, $E$ ise arkadaşlık, takip veya mesajlaşma gibi ilişkileri gösterir. Her düğümün yaş, ilgi alanı ya da paylaşım sıklığı gibi bir özellik vektörü $x_v$ bulunabilir. Kenarlar da ilişkinin gücü veya türü gibi bilgiler taşıyabilir.

Klasik makine öğrenmesi kullanıcıları çoğunlukla bağımsız örnekler kabul eder. GNN ise “arkadaşının davranışı seni de anlatabilir” fikrinden hareket eder. Her düğüm, komşularından bilgi toplar ve kendi temsiliyle birleştirir. Bu işleme **mesaj geçişi** denir:

$$
h_v^{(l+1)} = \sigma\left(W_1h_v^{(l)} + W_2\sum_{u \in N(v)}h_u^{(l)}\right)
$$

Burada $h_v^{(l)}$, $v$ düğümünün $l$. katmandaki temsilidir. $N(v)$ komşuları, $W_1$ ve $W_2$ öğrenilen ağırlıklar, $\sigma$ ise doğrusal olmayan aktivasyon fonksiyonudur. Birkaç katman sonunda düğüm yalnızca doğrudan arkadaşlarını değil, arkadaşlarının arkadaşlarını da özetleyen bir gömme (**embedding**) kazanır.

## Geleneksel yöntem mi, GNN mi?

| Yaklaşım | Kullandığı bilgi | Güçlü yanı | Sınırlaması |
|---|---|---|---|
| Louvain | Ağ bağlantıları | Hızlı ve etiketsiz çalışır | Düğüm özelliklerini doğrudan kullanmaz |
| Spectral clustering | Komşuluk matrisi | Matematiksel olarak güçlüdür | Büyük ağlarda maliyetlidir |
| GNN | Bağlantılar ve özellikler | Karmaşık örüntüleri öğrenir | Eğitim ve hiperparametre ayarı ister |

![gnn-ile-sosyal-78](/img/gnn-ile-sosyal-78.svg)


GNN doğrudan “topluluk numarası” üretmek zorunda değildir. Önce benzer düğümleri vektör uzayında yakınlaştırır, ardından K-Means gibi bir kümeleme algoritması bu temsilleri gruplandırabilir. Denetimli senaryoda ise bilinen birkaç topluluk etiketiyle düğüm sınıflandırması yapılabilir.

## Küçük bir GCN uygulaması

Aşağıdaki model, PyTorch Geometric kullanarak düğümler için sekiz boyutlu temsiller üretir:

```python
import torch
from torch_geometric.nn import GCNConv

class CommunityGCN(torch.nn.Module):
    def __init__(self, feature_count):
        super().__init__()
        self.conv1 = GCNConv(feature_count, 32)
        self.conv2 = GCNConv(32, 8)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = torch.nn.functional.dropout(
            x, p=0.3, training=self.training
        )
        return self.conv2(x, edge_index)

model = CommunityGCN(feature_count=16)
embeddings = model(data.x, data.edge_index)
```

`data.x`, kullanıcı özelliklerini içeren matrisi; `data.edge_index` ise bağlantıları gösterir. İlk GCN katmanı komşuluk bilgisini 32 boyutta işler. İkinci katman, kümelemeye verilebilecek sekiz boyutlu gömmeler oluşturur. Dropout, modelin belirli bağlantılara aşırı güvenmesini azaltır.

Etiketsiz eğitimde bağlantılı düğümlerin gömmelerini yakın, rastgele seçilen bağlantısız düğümleri uzak tutan bir kayıp kullanılabilir. Örneğin iki gömme arasındaki benzerlik $s(u,v)=z_u^Tz_v$ olarak tanımlanabilir. Model, gerçek kenarlarda yüksek; negatif örneklerde düşük skor üretmeyi öğrenir.

## Başarıyı nasıl ölçeriz?

Gerçek topluluk etiketleri varsa NMI, ARI veya F1 skoru kullanılabilir. Etiket yoksa **modülerlik**, aynı topluluktaki bağlantı yoğunluğunu rastlantısal bir ağla karşılaştırır. Yüksek modülerlik iyi bir işaret olsa da tek başına kusursuzluk garantisi değildir; sosyal gruplar örtüşebilir ve kullanıcılar birden fazla topluluğa ait olabilir.

Son olarak gizlilik ve önyargı unutulmamalıdır. GNN, verideki ayrımcı desenleri de öğrenebilir. Bu yüzden anonimleştirme, adalet testleri ve açıklanabilirlik araçları teknik sürecin parçası olmalıdır. Doğru kullanıldığında GNN, bağlantı karmaşasını anlamlı sosyal haritalara dönüştüren oldukça güçlü bir pusuladır.

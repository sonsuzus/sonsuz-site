---
layout: post
title: "GNN Düellosu: GraphSAGE, GCN ve GAT ile Düğüm Sınıflandırma ve Bağlantı Tahmini"
math: true
categories: 
  - Bilgi
tags: 
  - GNN
  - GraphSAGE
  - GCN
  - GAT
  - Makine Öğrenmesi
---

Graf sinir ağları (GNN), kullanıcılar, ürünler, makaleler veya moleküller gibi ilişkili nesneleri öğrenmek için düğüm özelliklerini bağlantı yapısıyla birleştirir. Düğüm sınıflandırmada amaç her düğüme bir etiket vermek; bağlantı tahmininde ise iki düğüm arasında yeni ya da eksik bir kenar olup olmadığını kestirmektir. GCN, GraphSAGE ve GAT aynı sahnede oynasa da bilgiyi komşulardan toplama biçimleri oldukça farklıdır.
``

Bir grafı $G=(V,E,X)$ ile gösterelim. Burada $V$ düğüm kümesi, $E$ kenarlar ve $X$ düğüm öznitelik matrisidir. Her katman, bir düğümün $k$-inci katmandaki gösterimini $h_v^{(k)}$ olarak günceller. Temel fikir şudur: Bir kullanıcının ilgi alanını yalnızca profilinden değil, arkadaşlarının davranışlarından da öğrenmek isteriz. Ancak çok katman eklemek, uzak komşulardan bilgi getirirken düğümlerin birbirine aşırı benzemesine, yani **over-smoothing** sorununa yol açabilir.

## GCN: Normalize edilmiş komşu ortalaması

GCN (Graph Convolutional Network), komşu mesajlarını derece bilgisiyle normalize ederek toplar. Yaygın güncelleme formülü şöyledir:

$$H^{(k+1)}=\sigma(\tilde{D}^{-1/2}\tilde{A}\tilde{D}^{-1/2}H^{(k)}W^{(k)})$$

Burada $\tilde{A}=A+I$, yani düğüm kendi bilgisini de korur; $\tilde{D}$ derece matrisi, $W^{(k)}$ öğrenilen ağırlıklar ve $\sigma$ aktivasyon fonksiyonudur. GCN, aynı tipte düğüm ve kenar içeren, nispeten sabit graf yapılarında güçlü ve hızlı bir başlangıç modelidir. Fakat tüm komşulara yapısal olarak benzer önem verdiği için gürültülü bağlantılarda zorlanabilir.

## GraphSAGE: Örnekle, topla, genelleştir

GraphSAGE, özellikle devasa veya zamanla büyüyen grafikler için tasarlanmıştır. Her düğümün tüm komşularını kullanmak yerine bir alt küme örnekler. Genel fikri:

$$h_v^{(k+1)}=\sigma\left(W^{(k)}[h_v^{(k)}\,\Vert\,\text{AGG}({h_u^{(k)}:u\in\mathcal{N}(v)})]\right)$$

Buradaki $\Vert$ birleştirme, `AGG` ise ortalama, maksimum havuzlama veya LSTM tabanlı bir toplayıcı olabilir. En önemli avantajı **indüktif** çalışmasıdır: Eğitimde hiç görülmemiş yeni bir düğüm, öznitelikleri ve komşuları geldikten sonra yeniden tüm modeli eğitmeden temsil edilebilir. Bu yönüyle sosyal ağlar ve öneri sistemleri için oldukça pratiktir.

## GAT: Komşular eşit değildir

GAT (Graph Attention Network), her komşuya aynı ağırlığı vermek yerine dikkat katsayıları öğrenir. Bir düğümün $u$ komşusuna verdiği önem kabaca şöyle hesaplanır:

$$\alpha_{vu}=\text{softmax}_u\big(\text{LeakyReLU}(a^T[Wh_v\Vert Wh_u])\big)$$

Ardından yeni gösterim $h_v'=\sigma(\sum_{u\in\mathcal{N}(v)}\alpha_{vu}Wh_u)$ olur. Çok başlıklı dikkat (multi-head attention), farklı ilişki örüntülerini paralel öğrenir. GAT, alakasız komşuların bulunduğu grafiklerde etkileyicidir; bunun karşılığında dikkat hesapları bellek ve süre maliyetini artırır.

| Özellik | GCN | GraphSAGE | GAT |
|---|---|---|---|
| Komşu ağırlığı | Normalize, sabit | Seçilen toplayıcıya bağlı | Öğrenilen dikkat ağırlığı |
| Ölçeklenebilirlik | Orta | Yüksek, örnekleme sayesinde | Orta, dikkat maliyetli |
| Yeni düğümler | Genellikle yeniden eğitim ister | Doğal olarak destekler | Uygun kurulumla desteklenir |
| Güçlü senaryo | Temiz, homofilik graflar | Büyük ve dinamik graflar | Gürültülü, heterojen komşuluklar |

Düğüm sınıflandırmada son katman her düğüm için sınıf olasılığı üretir: $\hat{y}_v=\text{softmax}(h_v^{(L)})$. Bağlantı tahmininde ise iki gömme vektörü bir skorlayıcıya verilir. En basit seçenek iç çarpımdır: $s(u,v)=z_u^Tz_v$. Eğitimde gerçek kenarlar pozitif, rastgele seçilmiş kenarsız çiftler negatif örnek olur.

```python
# z: GNN'den gelen düğüm gömmeleri, edge_index: aday kenarlar
src, dst = edge_index
scores = (z[src] * z[dst]).sum(dim=-1)
probs = scores.sigmoid()  # Kenar var olma olasılığı
loss = torch.nn.functional.binary_cross_entropy(probs, labels.float())
```

Bu kod, encoder olarak GCN, GraphSAGE veya GAT kullanıldıktan sonra ortak bir bağlantı tahmini decoder'ı kurar. Hızlı bir temel için GCN, üretimde yeni düğümler için GraphSAGE, komşu kalitesinin değişken olduğu durumlarda ise GAT mantıklı seçimlerdir. En iyi modeli belirleyen şey yalnızca doğruluk değil; grafın ölçeği, yeni düğüm akışı ve hesaplama bütçesidir.

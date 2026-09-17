---
layout: post
title: "Embedding Geometrisi: Kelimeler Vektör Uzayında Neden Yakınlaşır?"
math: true
categories: 
  - Bilgi
tags: 
  - embedding
  - vektörler
  - doğal dil işleme
  - makine öğrenmesi
  - yapay zeka
  - nlp
toc: true
---

Bir dil modeli için “kedi”, tüylü bir canlıdan önce yüzlerce sayıdan oluşan bir listedir. Buna rağmen “kedi” ile “köpek” birbirine yakın, “kedi” ile “matkap” ise genellikle uzaktır. Bu durum sihir değil; kelimelerin kullanıldıkları bağlamlardan öğrenilen geometrik bir düzendir. Gelin, kelimelerin anlamlarını koordinatlara nasıl dönüştürdüğünü inceleyelim.

``

## Kelimeden vektöre: Anlamın koordinatları

Bir **embedding**, bir kelimeyi $d$ boyutlu gerçek sayı uzayındaki bir vektörle temsil eder:

$$
\text{kedi} \longrightarrow \mathbf{v}_{kedi} \in \mathbb{R}^{d}
$$

Örneğin üç boyutlu, tamamen hayali bir gösterim şöyle olabilir:

$$
\mathbf{v}_{kedi} = [0.8, -0.2, 0.6]
$$

Gerçek sistemlerde boyut sayısı yüzlerce veya binlerce olabilir. Buradaki her koordinatı “tüylülük” ya da “evcil olma” gibi tek bir özellikle eşleştiremeyiz. Anlam, çoğunlukla birçok boyuta **dağıtılmıştır**. Bir kelimenin konumu, diğer kelimelerle kurduğu ilişkiler üzerinden değer kazanır.

Bu yaklaşımın temelinde dağılımsal hipotez bulunur: **Benzer bağlamlarda kullanılan kelimeler, benzer anlamlara sahip olma eğilimindedir.** “Kedi mama yedi” ve “Köpek mama yedi” cümlelerinde kedi ile köpek aynı çevrelerde göründüğü için eğitim sırasında vektörleri yakınlaşır.

| Temsil yöntemi | Benzerliği yakalar mı? | Boyut sayısı | Temel özellik |
|---|---:|---:|---|
| One-hot | Hayır | Kelime sayısı kadar | Her kelime bağımsızdır |
| Word2Vec | Evet | Genellikle 100–300 | Yerel bağlamı öğrenir |
| Bağlamsal embedding | Evet | Yüzlerce–binlerce | Anlamı cümleye göre değiştirir |

## “Yakınlık” tam olarak nedir?

Vektörlerin yakınlığını ölçmek için Öklid uzaklığı kullanılabilir:

$$
d(\mathbf{x},\mathbf{y}) = \sqrt{\sum_{i=1}^{d}(x_i-y_i)^2}
$$

Ancak embedding dünyasında çoğu zaman **kosinüs benzerliği** tercih edilir. Bu ölçü, vektörlerin uzunluğundan çok aralarındaki açıya bakar:

$$
\cos(\theta)=\frac{\mathbf{x}\cdot\mathbf{y}}{\\vert \mathbf{x}\\vert \\vert \mathbf{y}\\vert }
$$

Sonuç $1$ değerine yaklaştıkça yönler benzer, $0$ civarında ilişki zayıf, $-1$ civarında ise yönler karşıttır. Başka bir deyişle iki kelime, koordinatlarının büyüklükleri farklı olsa bile aynı anlamsal yöne bakabilir.

| Ölçü | Neye odaklanır? | Ne zaman kullanışlıdır? |
|---|---|---|
| Öklid uzaklığı | Noktalar arasındaki fiziksel mesafe | Vektör ölçekleri anlamlıysa |
| Kosinüs benzerliği | Vektörler arasındaki açı | Metin ve anlam karşılaştırmalarında |
| Noktasal çarpım | Yön ve büyüklük | Model eğitimi ve dikkat mekanizmalarında |

## Geometri nasıl öğreniliyor?

Word2Vec gibi yöntemlerde model, hedef kelimeden çevresindeki kelimeleri veya çevredeki kelimelerden hedefi tahmin eder. Doğru tahminlerin skoru artırılırken yanlış eşleşmelerin skoru azaltılır. Basitleştirilmiş hedef şöyledir:

$$
P(c\mid w) \propto \exp(\mathbf{v}_w \cdot \mathbf{v}_c)
$$

Burada $w$ hedef kelimeyi, $c$ bağlam kelimesini gösterir. Sıkça birlikte görülen çiftlerin noktasal çarpımı büyür; böylece vektörleri uyumlu yönlere döner. Model, dev bir kelime galaksisinde benzer kullanım örüntülerini aynı mahalleye taşır.

Aşağıdaki kod iki embedding arasındaki kosinüs benzerliğini hesaplar:

```python
import numpy as np

def cosine_similarity(a, b):
    # İki vektörün yön bakımından benzerliğini ölçer.
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

kedi = np.array([0.8, -0.2, 0.6])
kopek = np.array([0.7, -0.1, 0.65])
matkap = np.array([-0.3, 0.9, 0.1])

print(cosine_similarity(kedi, kopek))
print(cosine_similarity(kedi, matkap))
```

İlk sonucun daha yüksek olması beklenir. Elbette gerçek embedding’ler birkaç elle seçilmiş sayı yerine büyük metin koleksiyonlarından öğrenilir.

## Kusursuz bir anlam haritası mı?

Hayır. Embedding’ler eğitim verisindeki toplumsal önyargıları da geometrilerine taşıyabilir. Ayrıca klasik Word2Vec, “yüz” kelimesinin sayı ve surat anlamlarını tek vektörde sıkıştırır. Transformer tabanlı bağlamsal modeller ise kelimenin vektörünü bulunduğu cümleye göre üretir.

Sonuç olarak kelimeler, sözlük tanımları aynı olduğu için değil, **benzer dilsel görevlerde kullanıldıkları için** yakın durur. Embedding uzayı anlamın kendisi değil; kullanım örüntülerinden çizilmiş, güçlü fakat kusurlu bir geometrik haritadır.

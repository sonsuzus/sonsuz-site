---
layout: post
title: "Embedding Kavramı: Metinler Sayısal Uzayda Nasıl Anlama Dönüşür?"
math: true
categories: 
  - Bilgi
tags: 
  - embedding
  - doğal dil işleme
  - makine öğrenmesi
toc: true
---

Bilgisayarlar için “kedi” ile “köpek” kelimeleri, ilk bakışta yalnızca farklı karakter dizileridir. Oysa insan zihni ikisinin de hayvan olduğunu, “kedi” ile “miyav” arasında güçlü bir ilişki bulunduğunu sezebilir. **Embedding** (gömme), metin, kelime, cümle ya da belge gibi verileri; bu anlamsal ilişkileri korumaya çalışan sayısal vektörlere dönüştürme yöntemidir. Böylece arama motorları, öneri sistemleri ve yapay zekâ uygulamaları metnin yalnızca yazılışını değil, yaklaşık anlamını da karşılaştırabilir.
``

## Sayısal temsil neden gereklidir?

Makine öğrenmesi algoritmaları metinle doğrudan çalışmaz; giriş olarak sayılar bekler. En basit dönüşüm yöntemi **one-hot encoding** yaklaşımıdır. Sözlükte 10.000 kelime varsa, her kelime 10.000 boyutlu bir vektörde yalnızca bir konumun `1`, diğerlerinin `0` olmasıyla temsil edilir. Ancak bu yöntem kelimeler arasındaki anlam bağını kaybeder: “kedi” ve “köpek” vektörleri matematiksel olarak tamamen eşit uzaklıktadır.

Embedding ise her öğeyi daha küçük boyutlu, yoğun bir vektöre taşır. Örneğin `kedi` kelimesi `[0.12, -0.47, 0.81, ...]` gibi 384 veya 768 bileşenli bir dizi olabilir. Eğitim sürecinde benzer bağlamlarda geçen kelimelerin vektörleri uzayda birbirine yaklaşır. Bu yüzden geometrik yakınlık, anlamsal yakınlığın pratik bir vekili hâline gelir.

| Temsil yöntemi | Boyut | Anlamsal benzerlik | Bellek verimliliği |
|---|---:|---|---|
| One-hot encoding | Sözlük büyüklüğü kadar | Yok | Düşük |
| Bag of Words | Sözlük büyüklüğü kadar | Sınırlı | Orta |
| Embedding | Genellikle 128-1536 | Yüksek | Yüksek |

## Benzerlik uzayda nasıl ölçülür?

Vektörlerin yönü, çoğu senaryoda uzunluğundan daha anlamlıdır. Bu nedenle en sık kullanılan ölçü **kosinüs benzerliği**dir:

$$\cos(\theta) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|\|\mathbf{v}\|}$$

Sonuç `1` değerine yaklaştıkça vektörler aynı yöne, yani benzer anlama sahiptir. `0` civarı ilişkisizliği; negatif değerler ise zıt yönleri ifade eder. Örneğin “yazılım geliştirme” sorgusu, “Python ile uygulama programlama” belgesine; anahtar kelimeleri birebir aynı olmasa bile yüksek benzerlik verebilir.

Embedding modelleri bu uzayı büyük metin koleksiyonlarından öğrenir. Word2Vec gibi erken dönem modeller kelime komşuluklarını kullanırken, güncel transformer tabanlı modeller bir kelimenin cümledeki bağlamını dikkate alır. Böylece “yüz” kelimesinin insan yüzü mü, sayı yüz mü olduğu çevresindeki sözcüklere göre farklı vektörlerle temsil edilebilir.

| Seviye | Temsil edilen veri | Tipik kullanım |
|---|---|---|
| Kelime embedding’i | Tek kelime | Benzer kelime bulma |
| Cümle embedding’i | Bir ifade veya soru | Semantik arama |
| Belge embedding’i | Paragraf veya doküman | RAG, doküman eşleştirme |

## Küçük bir semantik arama örneği

Aşağıdaki Python örneği, `sentence-transformers` ile cümleleri vektörleştirir ve bir sorguya en yakın metni bulur. Model indirilirken ilk çalıştırma biraz sabır isteyebilir; vektörler ise sabrın ödülüdür.

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

belgeler = [
    "Python ile web API geliştirme rehberi",
    "Evde sağlıklı ekmek yapımı",
    "Makine öğrenmesi modellerini dağıtma"
]
sorgu = "Python kullanarak servis oluşturmak istiyorum"

belge_vektorleri = model.encode(belgeler)
sorgu_vektoru = model.encode([sorgu])

skorlar = cosine_similarity(sorgu_vektoru, belge_vektorleri)[0]
en_iyi_indeks = skorlar.argmax()

print(belgeler[en_iyi_indeks], skorlar[en_iyi_indeks])
```

Burada `encode`, metni sayısal uzaya yerleştirir; `cosine_similarity` ise sorgunun hangi belgeye anlamsal olarak en yakın olduğunu hesaplar. Gerçek projelerde bu vektörler FAISS, Chroma veya Pinecone gibi vektör veritabanlarında saklanır.

Embedding kusursuz bir “anlama motoru” değildir: eğitim verisindeki önyargıları taşıyabilir, alan dışı terimlerde zorlanabilir ve çok uzun metinleri parçalara ayırmayı gerektirebilir. Yine de doğru model, doğru parçalara bölme stratejisi ve iyi bir benzerlik eşiğiyle, metni aranabilir ve karşılaştırılabilir bir matematiksel haritaya dönüştürür.

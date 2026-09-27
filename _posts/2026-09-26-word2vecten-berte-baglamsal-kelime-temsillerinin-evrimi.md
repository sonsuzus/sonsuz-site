---
layout: post
title: "Word2Vec’ten BERT’e: Bağlamsal Kelime Temsillerinin Evrimi"
math: true
categories: 
  - Bilgi
tags: 
  - word2vec
  - bert
  - nlp
  - yapay zeka
  - transformer
  - kelime gömme
toc: true
image: /img/word2vecten-berte-baglamsal-81.png
---

Bilgisayarlar kelimeleri doğrudan anlayamaz; onları sayılara dönüştürmemiz gerekir. Ancak bu dönüşüm göründüğünden daha çetrefillidir. Örneğin banka kelimesi, para çektiğimiz bir kurumu da nehir kenarını da anlatabilir. Doğal dil işlemenin yolculuğu, kelimelere tek bir kimlik kartı veren sabit temsillerden, cümleyi okuyup anlama göre yeni kimlik üreten bağlamsal modellere doğru ilerledi.

``

## Kelimeleri vektörlere dönüştürmek

Eski yöntemlerde kelimeler çoğunlukla one-hot vektörlerle gösteriliyordu. Sözlükte $N$ kelime varsa her kelime, yalnızca bir bileşeni 1 olan $N$ boyutlu bir vektör alıyordu. Bu yaklaşım, kedi ile köpek arasındaki ilişkinin kedi ile buzdolabı arasındaki ilişkiden daha güçlü olduğunu söyleyemezdi.

Word2Vec bu sorunu dağılımsal hipotezle ele aldı: Benzer bağlamlarda kullanılan kelimeler benzer anlamlara sahiptir. Modelin temel amacı kabaca şu olasılığı yükseltmektir:

$$P(w_{context} \vert  w_{target})$$

CBOW, çevredeki kelimelerden merkez kelimeyi tahmin ederken Skip-gram merkez kelimeden çevresindekileri tahmin eder. Eğitim sonunda anlamsal yakınlık taşıyan kelimeler vektör uzayında birbirine yaklaşır. İki vektör arasındaki benzerlik çoğunlukla kosinüs benzerliğiyle ölçülür:

$$cos(a,b) = (a \cdot b) / (\vert a\Vert b\vert )$$

Bu yapı sayesinde kral - erkek + kadın ≈ kraliçe gibi eğlenceli vektör işlemleri yapılabilir. Yine de önemli bir sorun vardır: Bir kelime, kullanıldığı bütün cümlelerde aynı vektöre sahiptir.

| Yaklaşım | Kelime temsili | Bağlam duyarlılığı | Temel sınırlama |
|---|---|---:|---|
| One-hot | Seyrek ve yüksek boyutlu | Yok | Anlamsal ilişki kuramaz |
| Word2Vec | Yoğun ve sabit | Sınırlı | Çok anlamlılığı ayıramaz |
| ELMo | Dinamik | Var | Çift yönlülüğü katmanlarla kurar |
| BERT | Dinamik ve derin | Çok güçlü | Hesaplama maliyeti yüksektir |

## Sabit anlam neden yetmedi?

Word2Vec için yüz kelimesinin insan yüzü, yüz sayısı veya yüzmek fiilinin emri olarak kullanılması fark etmez; sözlükteki öğe aynı vektörü alır. Anlamların eğitim verisindeki ortalaması tek bir temsile sıkıştırılır. Bu durum kelime benzerliğinde işe yarasa da duygu analizi, soru yanıtlama ve anlam ayrıştırma gibi görevlerde sorun çıkarır.

ELMo, kelime temsilini cümlenin tamamına bakarak üretip önemli bir geçiş sağladı. Çift yönlü LSTM katmanları sayesinde aynı kelime, sağındaki ve solundaki sözcüklere göre farklı vektörler alabildi. Böylece temsil artık sözlükten hazır alınan bir etiket değil, kullanım anında hesaplanan bir sonuç oldu.

## BERT ve Transformer sıçraması

BERT, yinelemeli ağlar yerine Transformer mimarisinin self-attention mekanizmasını kullanır. Her kelime, cümledeki diğer kelimelerin kendisi için ne kadar önemli olduğunu öğrenir. Attention işleminin özeti şöyledir:

$$Attention(Q,K,V) = softmax(QK^T / sqrt(d_k))V$$

BERT, Masked Language Modeling sırasında bazı kelimeleri gizleyip onları iki taraftaki bağlamdan tahmin eder. Örneğin Çocuk nehir kıyısındaki bankada oturdu cümlesindeki banka temsiliyle Bankada yeni hesap açtı cümlesindeki temsil aynı değildir.

Aşağıdaki örnek, aynı kelimenin iki bağlamdaki BERT vektörlerini çıkarır:

```python
import torch
from transformers import AutoTokenizer, AutoModel

model_name = "dbmdz/bert-base-turkish-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

sentences = [
    "Nehir kıyısındaki bankada oturdu.",
    "Bankada yeni bir hesap açtı."
]

inputs = tokenizer(sentences, return_tensors="pt", padding=True)
with torch.no_grad():
    outputs = model(**inputs)

vectors = outputs.last_hidden_state
print(vectors.shape)
```

`last_hidden_state`, her cümledeki her token için bağlama özel bir vektör içerir. Gerçek bir karşılaştırmada banka tokenının konumu bulunup iki vektörün kosinüs benzerliği hesaplanabilir.

## Değişen şey yalnızca teknoloji değil

Word2Vec kelimenin genel olarak neye benzediğini öğrenirken BERT, kelimenin bu cümlede ne ifade ettiğini öğrenir. Başka bir deyişle temsil, statik bir sözlük maddesinden dinamik bir anlam hesabına dönüşmüştür. Günümüzde büyük dil modellerinin başarısının temelinde de bu fikir bulunur: Anlam kelimenin içinde tek başına durmaz; diğer kelimelerle kurduğu ilişkiden doğar.

![word2vecten-berte-baglamsal-81](/img/word2vecten-berte-baglamsal-81.svg)


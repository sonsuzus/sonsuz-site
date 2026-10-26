---
layout: post
title: "Doğal Dil İşleme ile Klinik Notlardan Yapılandırılmış Tıbbi Veri Çıkarma"
math: true
categories: 
  - Bilgi
tags: 
  - doğal dil işleme
  - klinik nlp
  - yapay zeka
  - sağlık bilişimi
  - bilgi çıkarımı
  - python
toc: true
image: /img/dogal-dil-isleme-37.png
---

Doktor notları klinik açıdan son derece değerlidir; ancak “üç gündür artan göğüs ağrısı, diyabet öyküsü var, ateş yok” gibi serbest metinler bilgisayarların doğrudan analiz edebileceği satır ve sütunlara benzemez. Klinik Doğal Dil İşleme, bu dağınık anlatımı tanılar, belirtiler, ilaçlar, ölçümler ve zaman bilgileri gibi yapılandırılmış verilere dönüştürür. Böylece araştırma, karar desteği ve hastane operasyonlarında kullanılabilecek güvenilir veri üretilir.

![dogal-dil-isleme-37](/img/dogal-dil-isleme-37.svg)

``
## Klinik notları anlamak neden zordur?

Gündelik NLP uygulamalarında bir kelimenin olumlu veya olumsuz duygu taşıması önemli olabilir. Klinik alandaysa tek bir olumsuzluk eki hastanın durumunu tamamen değiştirir: “pnömoni var” ile “pnömoni saptanmadı” aynı kavramı içerir ama zıt sonuçlar bildirir.

Notlarda kısaltmalar, yazım hataları, özel terminoloji ve bağlama bağlı ifadeler de bulunur. “MI” miyokart enfarktüsü anlamına gelebilirken farklı bir bölümde başka bir kısaltmayı temsil edebilir. Türkçenin eklemeli yapısı da “hipertansiyonu”, “hipertansiyondan” ve “hipertansiyonsuz” biçimlerinin aynı kökle ilişkilendirilmesini gerektirir.

| Görev | Girdi örneği | Yapılandırılmış sonuç |
|---|---|---|
| Varlık tanıma | “Metformin 500 mg kullanıyor” | İlaç: Metformin, doz: 500 mg |
| Olumsuzluk analizi | “Ateş gözlenmedi” | Ateş: yok |
| Zaman çıkarımı | “İki yıl önce ameliyat oldu” | İşlem zamanı: geçmiş |
| Kavram eşleme | “Yüksek tansiyon” | SNOMED CT: hipertansiyon |
| İlişki çıkarımı | “Baş ağrısı için parasetamol” | İlaç-belirti ilişkisi |

## Tipik bilgi çıkarım hattı

Sistem önce metni cümlelere ve sözcüklere ayırır. Ardından normalizasyon yaparak yazım çeşitlerini azaltır. Adlandırılmış Varlık Tanıma modeli hastalık, ilaç, anatomik bölge ve laboratuvar değeri gibi ifadeleri etiketler. Sonraki aşamada olumsuzluk, belirsizlik, deneyimleyen kişi ve zaman belirlenir.

Örneğin “Hastanın annesinde meme kanseri vardı” cümlesinde hastalık gerçektir; fakat deneyimleyen kişi hasta değildir. Bu ayrım yapılmazsa hastaya yanlış tanı atanabilir. Son aşamada bulunan ifadeler ICD-10, LOINC veya SNOMED CT gibi kontrollü terminolojilerle eşleştirilir.

Modern sistemler BERT benzeri dönüştürücü modeller kullanır. Bir ifadenin bağlamsal gösterimi kabaca şöyle düşünülebilir:

$$h_i = \operatorname{Transformer}(x_1, x_2, \ldots, x_n)_i$$

Burada $x_i$ sözcük veya alt sözcük birimini, $h_i$ ise çevresindeki kelimeleri dikkate alan bağlamsal temsili gösterir. Sınıflandırıcı bu temsilden “ilaç”, “belirti” veya “varlık değil” gibi bir etiket üretir.

## Basitleştirilmiş Python örneği

Aşağıdaki örnek, eğitilmiş bir spaCy modelinin klinik varlıkları nasıl çıkarabileceğini gösterir. Gerçek kullanımda genel amaçlı model yerine kuruma ve dile uygun klinik veriyle eğitilmiş bir model gerekir.

```python
import spacy

nlp = spacy.load("tr_clinical_ner_model")
text = "Hasta metformin 500 mg kullanıyor, ateş gözlenmedi."
doc = nlp(text)

records = []
for entity in doc.ents:
    records.append({
        "text": entity.text,
        "type": entity.label_,
        "start": entity.start_char,
        "end": entity.end_char
    })

print(records)
```

Kod, metni modele gönderir ve tespit edilen ifadeleri türleriyle birlikte sözlük listesine dönüştürür. Ancak “gözlenmedi” bilgisinin ateşi olumsuzladığını anlamak için ayrıca kural tabanlı veya öğrenilmiş bir olumsuzluk modülü kullanılmalıdır.

## Başarı nasıl ölçülür?

Klinik sistemlerde yalnızca doğruluk oranına bakmak yanıltıcıdır. Kesinlik ve duyarlılık daha açıklayıcıdır:

$$\text{Kesinlik}=\frac{TP}{TP+FP}, \qquad \text{Duyarlılık}=\frac{TP}{TP+FN}$$

Yüksek kesinlik, üretilen kayıtların çoğunun doğru olduğunu; yüksek duyarlılık ise gerçek klinik ifadelerin çok azının kaçırıldığını gösterir. Dengeli değerlendirme için $F_1$ skoru kullanılır.

## Güvenlik ve insan denetimi

Klinik notlar son derece hassas kişisel veriler içerir. Bu nedenle kimliksizleştirme, erişim kontrolü, şifreleme ve ayrıntılı denetim kayıtları zorunludur. Model çıktıları doğrudan tanı yerine geçmemeli; doktor onayına sunulan yardımcı öneriler olarak değerlendirilmelidir. Kısacası başarılı klinik NLP, yalnızca iyi bir model değil, güvenilir veri, tıbbi terminoloji, mahremiyet ve insan denetiminin birlikte çalıştığı bir sistemdir.

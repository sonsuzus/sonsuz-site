---
layout: post
title: "Makine Çevirisinde BLEU Skoru Bizi Kandırıyor mu?"
math: true
categories: 
  - Bilgi
tags: 
  - bleu
  - makine çevirisi
  - doğal dil işleme
  - yapay zeka
  - değerlendirme metrikleri
toc: true
image: /img/makine-cevirisinde-bleu-94.png
---

![makine-cevirisinde-bleu-94](/img/makine-cevirisinde-bleu-94.svg)


Bir çeviri sistemi yüksek BLEU skoru aldığında gerçekten iyi çeviri yapıyor diyebilir miyiz? Kısa cevap: Her zaman değil. BLEU, makine çevirisi dünyasının en meşhur ölçüm araçlarından biri olsa da anlamı, akıcılığı ve bağlamı doğrudan ölçmez. Üstelik bazen kulağa robotik gelen bir çeviriyi ödüllendirirken gayet doğal bir alternatifi cezalandırabilir.

``

## BLEU aslında neyi ölçüyor?

BLEU, yani **Bilingual Evaluation Understudy**, aday çevirideki kelime dizilerini insan tarafından hazırlanmış referans çevirilerle karşılaştırır. Buradaki temel fikir, iki metnin ortak $n$-gram sayısı arttıkça çevirinin daha başarılı kabul edilmesidir.

Bir $n$-gram, art arda gelen $n$ adet parçadan oluşur:

- 1-gram: `yapay`
- 2-gram: `yapay zeka`
- 3-gram: `yapay zeka sistemi`

Basitleştirilmiş $n$-gram kesinliği şöyle gösterilebilir:

$$
p_n = \frac{\text{Eşleşen aday n-gram sayısı}}{\text{Adaydaki toplam n-gram sayısı}}
$$

BLEU, farklı uzunluklardaki $n$-gram kesinliklerinin geometrik ortalamasını alır ve çok kısa çevirileri engellemek için bir uzunluk cezası ekler:

$$
BLEU = BP \cdot \exp\left(\sum_{n=1}^{N} w_n \log p_n\right)
$$

Buradaki $BP$, **brevity penalty** olarak bilinen kısalık cezasıdır. Sistem yalnızca birkaç doğru kelime üretip yüksek puanı kapamasın diye kullanılır.

## Aynı anlam, farklı kelimeler

Kaynak cümlenin “The meeting was called off” olduğunu düşünelim. Referans çeviri “Toplantı iptal edildi” olsun.

| Aday çeviri | Anlamsal kalite | BLEU açısından durum |
|---|---:|---|
| Toplantı iptal edildi | Yüksek | Tam eşleşme |
| Görüşme iptal oldu | Yüksek | Düşük kelime eşleşmesi |
| Toplantı edildi iptal | Düşük | Bazı n-gramlar eşleşebilir |
| Toplantı ertelendi | Yanlış | “Toplantı” nedeniyle kısmi puan alabilir |

İkinci çeviri bağlama göre son derece doğal olabilir. Ancak BLEU, “görüşme” ile “toplantı” arasındaki yakınlığı veya “iptal oldu” ifadesinin aynı mesajı taşıdığını bilmez. Çünkü kelimelerin anlamlarını değil, yüzeydeki parçaların örtüşmesini sayar.

Bu durum özellikle eş anlamlıların bol olduğu dillerde, serbest sözcük diziliminde ve Türkçe gibi eklemeli dillerde belirginleşir. “Evlerimizden” tek bir kelimeyken başka bir dilde birkaç ayrı sözcüğe karşılık gelebilir. Tokenizasyon tercihi bile sonucu değiştirebilir.

## Skoru hızlıca hesaplamak

Python'da `sacrebleu` paketiyle standartlaştırılmış bir BLEU hesabı yapılabilir:

```python
import sacrebleu

referanslar = [['Toplantı iptal edildi']]
adaylar = ['Görüşme iptal oldu']

sonuc = sacrebleu.corpus_bleu(adaylar, referanslar)
print(f'BLEU: {sonuc.score:.2f}')
```

Bu kod aday çeviriyi referansla karşılaştırır. Sonuç düşük çıkarsa adayın mutlaka kötü olduğunu söyleyemeyiz; yalnızca referansın kelime dizilimine yeterince benzemediğini söyleyebiliriz. Ayrıca farklı kütüphanelerin tokenizasyon ve düzeltme yöntemleri farklı sonuçlar üretebildiğinden deneylerde kullanılan BLEU sürümü açıkça belirtilmelidir.

## BLEU ne zaman işe yarar?

BLEU tamamen kullanışsız değildir. Büyük veri kümelerinde, aynı test seti üzerinde eğitilen sistemlerin genel ilerlemesini hızlı ve ucuz biçimde karşılaştırmak için pratiktir. Ancak tek bir cümlenin kalitesini değerlendirmekte güvenilir değildir. Korpus düzeyinde anlamlı olan istatistikler, cümle düzeyinde oynak hale gelir.

| Yöntem | Güçlü yanı | Temel kusuru |
|---|---|---|
| BLEU | Hızlı ve tekrarlanabilir | Anlamı doğrudan ölçmez |
| chrF | Karakter ve ek benzerliğine duyarlı | Bağlam bilgisi sınırlıdır |
| COMET | Anlamsal ilişkileri modelleyebilir | Eğitildiği verilere bağımlıdır |
| İnsan değerlendirmesi | Akıcılık ve doğruluğu birlikte görebilir | Pahalı ve öznel olabilir |

## Tek sayı yerine ölçüm sepeti

Sağlıklı değerlendirme için BLEU; chrF, COMET veya BERTScore gibi metriklerle desteklenmelidir. Kritik uygulamalarda insan değerlendiriciler doğruluk, akıcılık, terminoloji ve kültürel uygunluk başlıklarını ayrı ayrı puanlamalıdır.

Sonuç olarak BLEU bizi bilinçli biçimde kandırmaz; yalnızca kendisine sormadığımız soruları cevaplayamaz. O, “Bu çeviri referansa ne kadar benziyor?” sorusunda iyidir. “Bu çeviri anlamı doğru, doğal ve güvenli biçimde aktarıyor mu?” sorusu içinse tek başına oldukça sessizdir.

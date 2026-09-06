---
layout: post
title: "Model Drift Nedir? Yapay Zeka Modelleri Neden Zamanla Doğruluğunu Kaybeder?"
math: true
categories: 
  - Bilgi
tags: 
  - yapay zeka
  - makine öğrenmesi
  - model drift
toc: true
image: /img/model-drift-nedir-26.png
---

Bir makine öğrenmesi modelini yayına almak, yarışın bitiş çizgisi değil; aslında başlangıç tabancasıdır. Eğitim verisinde %95 doğruluk yakalayan bir dolandırıcılık, öneri ya da tahmin modeli, birkaç ay sonra beklenmedik biçimde hatalı kararlar vermeye başlayabilir. Bu olaya **model drift** denir: Modelin üretim ortamındaki performansının, zaman içinde eğitim dönemindeki performansından anlamlı biçimde uzaklaşmasıdır.


![model-drift-nedir-26](/img/model-drift-nedir-26.svg)

``

Model drift'in temel nedeni basittir: Dünya sabit değildir, ama model çoğunlukla geçmişin fotoğrafıyla eğitilir. Matematiksel olarak modelin eğitim anındaki veri dağılımını $P_{train}(X, Y)$, canlı ortamdaki dağılımı ise $P_{prod}(X, Y)$ ile gösterelim. Bu iki dağılım eşit değilse modelin öğrendiği ilişkiler zayıflayabilir:

$$P_{train}(X, Y) \neq P_{prod}(X, Y)$$

Burada $X$ girdi özelliklerini, $Y$ ise tahmin edilmek istenen etiketi temsil eder. Örneğin bir e-ticaret modelinin eğitim verisinde müşteriler çoğunlukla masaüstünden alışveriş yapmış olabilir. Zamanla mobil kullanım artar, yeni ürün kategorileri eklenir ve kampanya davranışları değişir. Model hâlâ eski müşteri dünyasının kurallarıyla karar verdiği için önerileri isabetsizleşir.

## Drift Türleri: Değişen Şey Tam Olarak Ne?

Her performans düşüşü aynı nedenle yaşanmaz. Drift'i doğru sınıflandırmak, doğru çözümü seçmenin ilk adımıdır.

| Drift türü | Değişen unsur | Örnek | Olası çözüm |
|---|---|---|---|
| Covariate drift | $P(X)$ | Kullanıcıların cihaz dağılımı değişir | Yeni verilerle yeniden eğitim |
| Concept drift | $P(Y \mid X)$ | Aynı davranışın anlamı değişir | Etiketli veriyi hızla güncellemek |
| Label drift | $P(Y)$ | Dolandırıcılık oranı yükselir | Eşik ve örnekleme stratejisini ayarlamak |
| Data quality drift | Veri kalitesi | Bir API alanı boş dönmeye başlar | Veri hattını onarmak |

**Covariate drift**, girdilerin dağılımının değişmesidir. Örneğin hava tahmin modeline ait sıcaklık değerleri, mevsim değişince farklı aralıklarda dolaşabilir. **Concept drift** ise daha sinsi bir problemdir: Girdi benzer görünür ama girdi-hedef ilişkisi değişmiştir. Pandemi döneminde geçmiş satış davranışlarına göre eğitilmiş modellerin zorlanması bunun klasik örneğidir.

## Doğruluk Neden Bir Anda Değil, Sessizce Düşer?

Drift çoğu zaman dramatik bir hata mesajı üretmez. Sistem çalışır, API yanıt verir, grafikler akar; fakat kararların kalitesi yavaşça erir. Üstelik gerçek etiketler hemen gelmiyorsa, örneğin kredi temerrüdü aylar sonra belli oluyorsa, doğruluk metriğini anında ölçmek mümkün değildir.

Bu nedenle yalnızca accuracy izlemek yeterli değildir. Girdi dağılımlarını, eksik veri oranını, tahmin skorlarını ve iş metriklerini birlikte takip etmek gerekir. İki dağılım arasındaki farkı ölçmek için Population Stability Index (PSI) gibi metrikler kullanılabilir. Basitleştirilmiş biçimiyle:

$$PSI = \sum_i (p_i - q_i) \ln\left(\frac{p_i}{q_i}\right)$$

Burada $p_i$ eğitim verisindeki, $q_i$ ise güncel verideki ilgili aralık oranıdır. PSI büyüdükçe dağılım farkı da genellikle büyür. Ancak bu değer tek başına hüküm vermez; alan bilgisi ve iş etkisiyle birlikte yorumlanmalıdır.

## Pratik Bir İzleme Kontrolü

Aşağıdaki Python örneği, bir özelliğin eğitim ve canlı ortamdaki ortalamalarını hızlıca karşılaştırır. Bu, üretim izleme sisteminin küçük ama öğretici bir parçasıdır.

```python
import pandas as pd

train_mean = train_df["sepet_tutari"].mean()
prod_mean = prod_df["sepet_tutari"].mean()
change_ratio = abs(prod_mean - train_mean) / train_mean

if change_ratio > 0.20:
    print("Uyarı: Sepet tutarı dağılımında belirgin değişim var!")
else:
    print("Özellik dağılımı kabul edilebilir aralıkta.")
```

Gerçek sistemlerde buna medyan, standart sapma, kategorik oranlar, null değer oranı ve model skoru dağılımı da eklenir. Uyarı eşiği her proje için farklıdır: Sağlık alanında küçük bir sapma kritik olabilirken, içerik öneri sisteminde daha toleranslı davranılabilir.

Model drift'i tamamen engellemek mümkün değildir; çünkü kullanıcılar, pazarlar ve veri kaynakları değişir. Ama onu erken fark etmek mümkündür. Düzenli veri izleme, geri bildirim döngüsü, yeniden eğitim planı ve sürümleme; “bir kez eğit, sonsuza kadar kullan” düşüncesini güvenilir bir MLOps sürecine dönüştürür.

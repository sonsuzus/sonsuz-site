---
layout: post
title: "Adversarial Analysis: Algoritmayı En Kötü Rakibine Karşı Sınamak"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - adversarial-analysis
  - karmaşıklık
  - python
  - performans
  - test
toc: true
---

Bir algoritma günlük verilerde ışık hızında çalışabilir; fakat karşısına onun zayıf noktalarını bilen kurnaz bir rakip çıktığında bütün karizma dağılabilir. **Adversarial analysis**, girdilerin tesadüfen değil, algoritmayı mümkün olduğunca zorlamak amacıyla seçildiğini varsayar. Böylece “Genellikle hızlı mı?” sorusu yerine daha güvenli bir soru sorarız: “Onu sabote etmeye çalışan biri varken ne kadar iyi?”

``

## Rakip modeli nedir?

Buradaki rakip mutlaka kötü niyetli bir bilgisayar korsanı değildir. Rakip; en kötü girdiyi seçen matematiksel bir model, yoğun trafik oluşturan kullanıcılar veya sistemdeki kararları gözlemleyebilen başka bir süreç olabilir. Analize başlamadan önce rakibin gücünü tanımlamak gerekir:

- Girdinin tamamını önceden seçebiliyor mu?
- Algoritmanın önceki kararlarını görebiliyor mu?
- Rastgele üretilen bitleri biliyor mu?
- Girdiyi çalışma sırasında değiştirebiliyor mu?

Rakibin gücü arttıkça kanıtlanan performans garantisi daha değerli, fakat bu garantiyi elde etmek daha zor olur.

| Analiz yaklaşımı | Girdi varsayımı | Cevapladığı soru |
|---|---|---|
| Ortalama durum | Bilinen bir olasılık dağılımı | Tipik girdide ne olur? |
| En kötü durum | Olası en pahalı girdi | En fazla ne kadar kaynak gerekir? |
| Adversarial analiz | Bilinçli ve uyarlanabilir rakip | Algoritma sömürülürse ne olur? |
| Amortize analiz | İşlem dizisinin toplam maliyeti | Uzun vadede işlem başına maliyet nedir? |

## Matematiksel bakış

Bir algoritmanın $x$ girdisindeki maliyeti $C(A,x)$ olsun. Klasik en kötü durum maliyeti şöyle ifade edilir:

$$W_A(n) = \max_{\vert x\vert =n} C(A,x)$$

Çevrim içi algoritmalarda ise algoritmanın sonucu, bütün geleceği bilen ideal çözümle karşılaştırılır. Rekabet oranı için yaygın hedef şudur:

$$C(A,x) \leq c \cdot C(OPT,x) + b$$

Burada $OPT$, girdinin tamamını önceden bilen kusursuz oyuncudur. $c$ küçüldükçe algoritma rakibe karşı daha dayanıklıdır; $b$ ise küçük girdilerdeki sabit sapmayı karşılar.

## Quicksort’un aşil tendonu

İlk elemanı pivot seçen deterministik Quicksort, sıralı bir diziyle karşılaşınca sürekli dengesiz bölünür. İş miktarı yaklaşık olarak

$$T(n)=T(n-1)+O(n)=O(n^2)$$

olur. Rastgele pivot seçildiğinde rakibin bölünmeleri önceden ayarlaması zorlaşır ve beklenen maliyet $O(n\log n)$ seviyesine iner. Rastgelelik sihirli kalkan değildir; yalnızca rakibin bilgi avantajını azaltır.

Aşağıdaki Python kodu, basit bir sıralama işlevini farklı rakip girdileriyle sınar:

```python
from time import perf_counter
import random

def adversarial_cases(n):
    ascending = list(range(n))
    return {
        "sirali": ascending,
        "ters": ascending[::-1],
        "esit": [7] * n,
        "rastgele": random.sample(range(n), n),
        "organ_pipe": list(range(n // 2)) + list(range(n // 2, 0, -1))
    }

def benchmark(sort_fn, n=10_000):
    for name, values in adversarial_cases(n).items():
        data = values.copy()
        start = perf_counter()
        sort_fn(data)
        elapsed = perf_counter() - start
        assert data == sorted(values)
        print(f"{name:12} {elapsed:.6f} saniye")
```

`adversarial_cases`, sıralı, ters, tekrarlı ve özel desenli diziler üretir. `benchmark` ise hem süreyi ölçer hem de sonucun doğruluğunu denetler. Tek bir ölçüm kesin hüküm değildir; farklı boyutlar, tekrarlar ve bellek tüketimi de incelenmelidir.

## Sağlam bir test stratejisi

Adversarial test yalnızca birkaç “çirkin” örnek yazmaktan ibaret değildir. Önce algoritmanın karar noktaları bulunmalı, ardından bu kararları sürekli en pahalı yola iten girdiler tasarlanmalıdır. Özellikle hash tablolarında çakışmalar, önbelleklerde erişim dizileri, grafik algoritmalarında yoğun veya aşırı seyrek yapılar hedeflenebilir.

| Savunma | Avantaj | Bedel |
|---|---|---|
| Rastgeleleştirme | Girdinin önceden ayarlanmasını zorlaştırır | Tekrarlanabilirlik azalabilir |
| Girdi doğrulama | Zararlı biçimleri erken reddeder | Ek çalışma maliyeti getirir |
| Kaynak sınırı | Çökme ve hizmet kesintisini önler | Geçerli işler yarıda kalabilir |
| Algoritma değiştirme | Teorik garantiyi güçlendirir | Uygulama karmaşıklaşabilir |

Sonuç olarak adversarial analysis, algoritmaya düşman olmak değil, üretime çıkmadan önce onun en dürüst eleştirmeni olmaktır. Algoritmanız kötü niyetli girdiler karşısında ayakta kalıyorsa normal günlerde rahatça kahvesini içebilir.

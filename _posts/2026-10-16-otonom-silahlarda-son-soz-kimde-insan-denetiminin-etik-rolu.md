---
layout: post
title: "Otonom Silahlarda Son Söz Kimde? İnsan Denetiminin Etik Rolü"
math: true
categories: 
  - Bilgi
tags: 
  - robotik etik
  - otonom sistemler
  - yapay zeka etiği
  - insan denetimi
  - sorumlu yapay zeka
  - askeri robotik
toc: true
image: /img/otonom-silahlarda-son-92.png
---

Otonom silah sistemleri; çevresini algılayabilen, seçenekleri değerlendirebilen ve belirli ölçülerde bağımsız karar verebilen teknolojilerdir. Ancak teknik olarak bir kararın üretilebilmesi, o kararın etik veya hukuki açıdan kabul edilebilir olduğu anlamına gelmez. Özellikle insan yaşamını etkileyen durumlarda temel soru şudur: Makine ne kadar yetkin olursa olsun, son söz insanda mı kalmalıdır?

``

## Otonom karar nasıl oluşur?

Bir otonom sistemin karar süreci kabaca algılama, sınıflandırma, risk hesaplama ve eylem seçimi aşamalarından oluşur. Sensörlerden gelen veriler önce bir modele aktarılır. Model, gözlemi daha önce öğrendiği örüntülerle karşılaştırarak tahmin üretir. Ardından yazılım, tanımlanmış hedef fonksiyonuna göre seçenekleri puanlar.

Basitleştirilmiş bir karar skoru şöyle gösterilebilir:

$$S(a) = B(a) - R(a) - E(a)$$

Burada $B(a)$ eylemin beklenen faydasını, $R(a)$ operasyonel riski, $E(a)$ ise etik maliyeti temsil eder. Sorun, etik maliyetin sıcaklık veya mesafe gibi doğrudan ölçülememesidir. Bağlam, niyet, orantılılık ve ayrım gözetme gibi kavramlar yalnızca sayılara indirgenemez.

Üstelik sensör hatası ile yanlış kararın olası zararı birlikte değerlendirilmelidir:

$$Toplam\ Risk = P(hata) \times Zarar$$

Olasılığı düşük görünen bir hata bile sonucu geri döndürülemez olduğunda kabul edilemez olabilir.

## İnsan denetiminin farklı seviyeleri

İnsan denetimi tek bir açma-kapama düğmesi değildir. Tasarıma göre farklı noktalarda uygulanabilir:

| Denetim modeli | İnsanın rolü | Etik avantaj | Temel risk |
|---|---|---|---|
| İnsan döngünün içinde | Her kritik eylemi insan onaylar | Açık sorumluluk ve muhakeme | Zaman baskısı, operatör yorgunluğu |
| İnsan döngünün üzerinde | Sistem çalışır, insan izler ve durdurabilir | Hız ile gözetim arasında denge | Müdahale için sürenin yetersiz kalması |
| İnsan döngünün dışında | Sistem kararı bağımsız uygular | Çok hızlı tepki | Anlamlı denetim ve hesap verebilirlik kaybı |

Etik açıdan en güçlü yaklaşım, **anlamlı insan denetimi** kavramıdır. Buradaki “anlamlı” sözcüğü önemlidir: Operatör yalnızca ekrandaki onay düğmesine basan biri olmamalıdır. Kararın bağlamını anlayabilmeli, yeterli zamana ve bilgiye sahip olmalı, sistemi durdurabilmeli ve verdiği kararın sonuçlarını kavrayabilmelidir.

## Yazılıma etik fren eklemek

Aşağıdaki örnek, gerçek bir silah kontrolü değil; yüksek riskli bir robotik kararın insan onayına yönlendirilmesini gösteren güvenli bir yönetişim taslağıdır:

```python
def karar_yolu(model_guveni, sivil_riski, iletisim_var):
    # Belirsizlik veya yüksek zarar ihtimali varsa otomasyonu durdurur.
    if not iletisim_var:
        return "EYLEMİ DURDUR"

    if model_guveni < 0.95:
        return "İNSAN İNCELEMESİ GEREKLİ"

    if sivil_riski > 0.01:
        return "EYLEMİ REDDET"

    return "YETKİLİ İNSAN ONAYI BEKLENİYOR"

sonuc = karar_yolu(0.91, 0.02, True)
print(sonuc)
```

Bu kodda sistem, güven eşiğini geçse bile kendi başına nihai eyleme karar vermiyor. Ayrıca iletişimin kesilmesi “serbest çalışma” gerekçesi değil, güvenli duruş sebebi oluyor. Buna **fail-safe**, yani hata durumunda güvenli konuma geçme yaklaşımı denir.

## Sorumluluk boşluğu neden tehlikelidir?

Bir hata gerçekleştiğinde sorumluluğun geliştiriciye, komutana, operatöre veya üreticiye sürekli aktarılması “sorumluluk boşluğu” yaratır. Bunu önlemek için karar kayıtları tutulmalı, modeller bağımsız denetlenmeli, yetki zinciri önceden belirlenmeli ve sistemler açıklanabilir olmalıdır. “Algoritma böyle istedi” etik bir savunma değildir; çünkü algoritmalar amaçlarını, sınırlarını ve verilerini insanlardan alır.

Sonuç olarak insan denetimi, otonom silahların üzerine sonradan eklenen dekoratif bir güvenlik katmanı değil, sistem mimarisinin merkezidir. Teknoloji seçenek önerebilir ve karmaşık verileri hızla işleyebilir; fakat yaşamı sona erdirebilecek kararların ahlaki yükünü üstlenemez. Etik hedef, insanı denklemden çıkarmak değil, insan muhakemesini bilinçli, bilgili ve hesap verebilir hâle getirmektir.

![otonom-silahlarda-son-92](/img/otonom-silahlarda-son-92.svg)


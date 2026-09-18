---
layout: post
title: "Sürü Robotiği: Basit Kurallardan Kolektif Zekâya"
math: true
categories: 
  - Bilgi
tags: 
  - sürü robotiği
  - robotik
  - yapay zekâ
  - kolektif davranış
  - python
  - algoritma
toc: true
image: /img/suru-robotigi-basit-44.png
---

Bir karınca tek başına yol planlama konusunda pek etkileyici görünmeyebilir; ancak binlerce karınca birlikte yiyeceğe giden verimli yollar oluşturabilir. Sürü robotiği de benzer bir fikirden beslenir: Çok sayıda görece basit robot, merkezi bir yönetici olmadan etkileşime girerek karmaşık görevleri tamamlar. İşin büyüsü, kolektif zekânın robotlara ayrı ayrı programlanmaması; yerel kuralların etkileşiminden kendiliğinden ortaya çıkmasıdır.

``

## Sürü robotiğinin temel fikri

Geleneksel robot sistemlerinde kararları merkezi bir bilgisayar verebilir. Sürü yaklaşımında ise her robot yalnızca yakın çevresini algılar, komşularıyla sınırlı bilgi paylaşır ve birkaç basit kural uygular. Robotların hiçbiri sistemin tamamını görmek zorunda değildir.

Bu yapıya **beliren davranış** denir. Kuş sürülerinin aynı anda yön değiştirmesi, balıkların avcılardan kaçarken düzenli biçimde dağılması ve karıncaların feromon izleri oluşturması bunun doğal örnekleridir.

| Yaklaşım | Merkezi sistem | Sürü sistemi |
|---|---|---|
| Karar verme | Tek merkezde | Robotlara dağıtılmış |
| Arıza etkisi | Kritik olabilir | Genellikle yereldir |
| Ölçeklenebilirlik | Yönetimi zorlaşabilir | Yeni robot eklemek kolaydır |
| Robot karmaşıklığı | Yüksek olabilir | Görece düşüktür |
| İletişim | Küresel bilgi gerekebilir | Yerel bilgi çoğu zaman yeterlidir |

![suru-robotigi-basit-44](/img/suru-robotigi-basit-44.svg)


## Üç basit kural

Birçok sürü hareketi üç davranışla modellenebilir:

1. **Ayrılma:** Çarpışmayı önlemek için çok yakın komşulardan uzaklaş.
2. **Hizalanma:** Yakındaki robotların ortalama hareket yönüne yaklaş.
3. **Birleşme:** Komşuların oluşturduğu merkeze doğru ilerle.

Bir robotun yeni hız vektörü şöyle ifade edilebilir:

$$
\vec{v}_{yeni} = w_s\vec{S} + w_a\vec{A} + w_c\vec{C}
$$

Burada $\vec{S}$ ayrılma, $\vec{A}$ hizalanma ve $\vec{C}$ birleşme vektörüdür. $w_s$, $w_a$ ve $w_c$ katsayıları ise davranışların önemini belirler. Ayrılma ağırlığı çok düşükse robotlar birbirine girer; çok yüksekse sürü, kalabalık bir asansörde kişisel alan arayan insanlara dönüşür.

## Küçük bir Python modeli

Aşağıdaki fonksiyon, tek bir robot için komşulara göre basitleştirilmiş yön değişimi hesaplar:

```python
import numpy as np

def suru_adimi(konum, hiz, komsu_konumlari, komsu_hizlari):
    if len(komsu_konumlari) == 0:
        return hiz

    merkez = np.mean(komsu_konumlari, axis=0)
    ortalama_hiz = np.mean(komsu_hizlari, axis=0)

    birlesme = merkez - konum
    hizalanma = ortalama_hiz - hiz

    farklar = konum - komsu_konumlari
    mesafeler = np.linalg.norm(farklar, axis=1)
    yakinlar = farklar[mesafeler < 2.0]
    ayrilma = np.sum(yakinlar, axis=0) if len(yakinlar) else np.zeros(2)

    yeni_hiz = hiz + 0.05 * birlesme + 0.1 * hizalanma + 0.3 * ayrilma
    maksimum_hiz = 2.0
    norm = np.linalg.norm(yeni_hiz)

    if norm > maksimum_hiz:
        yeni_hiz = yeni_hiz / norm * maksimum_hiz

    return yeni_hiz
```

Fonksiyon önce komşuların merkezini ve ortalama hızını bulur. İki birimden yakın robotlar için ayrılma kuvveti üretir, ardından üç davranışı farklı ağırlıklarla birleştirir. Son bölüm hızın fiziksel sınırı aşmasını engeller. Gerçek robotlarda buna sensör gürültüsü, gecikme, pil seviyesi ve engel algılama gibi değişkenler de eklenir.

## Neden dayanıklıdır?

Sürüde görev bilgisi dağıtıldığı için tek bir robotun bozulması çoğunlukla tüm operasyonu durdurmaz. Eğer bir robotun çalışma olasılığı $p$ ve sürüdeki robot sayısı $N$ ise beklenen çalışan robot sayısı basitçe $Np$ olur. Sistem görevini yalnızca belirli sayıda robota ihtiyaç duyarak sürdürebiliyorsa doğal bir hata toleransı kazanır.

Bu özellik; afet bölgelerinde arama, tarım alanlarının izlenmesi, depo taşımacılığı, çevresel ölçüm ve uzay keşfi gibi alanlarda değerlidir. Yine de haberleşme çakışmaları, güvenlik açıkları ve beklenmeyen kolektif davranışlar önemli mühendislik sorunlarıdır.

Sürü robotiğinin en çarpıcı dersi şudur: Karmaşık sonuçlar için her zaman karmaşık bireyler gerekmez. Doğru seçilmiş birkaç yerel kural, yüzlerce robotu koordineli ve dayanıklı bir topluluğa dönüştürebilir.

---
layout: post
title: "A/B Testi ve İstatistiksel Anlamlılık: Ürün Kararlarını Şansa Bırakmamak"
math: true
categories: 
  - Bilgi
tags: 
  - a/b testi
  - istatistik
  - ürün analitiği
image: /img/ab-testi-ve-58.png
---

Bir ürün ekibinin en tehlikeli cümlesi bazen şudur: “Yeni buton daha güzel görünüyor, yayınlayalım.” Güzel görünüm değerli olsa da dönüşümü gerçekten artırıp artırmadığını yalnızca kontrollü deney söyleyebilir. A/B testi, kullanıcıları rastgele iki veya daha fazla varyanta ayırarak tek bir değişikliğin davranış üzerindeki etkisini ölçme yöntemidir. Amaç, sezgiyi öldürmek değil; sezgiyi ölçülebilir kanıtla güçlendirmektir.
``
A varyantı mevcut deneyimdir; B varyantı ise test edilen değişikliği içerir. Örneğin kayıt sayfasındaki “Hemen Başla” düğmesini “Ücretsiz Deneyin” olarak değiştirmek isteyelim. Kullanıcıların bir kısmı A’yı, diğer kısmı B’yi görür. Rastgele atama kritik noktadır: Trafik kaynakları, cihazlar ve kullanıcı niyeti iki gruba dengeli dağılmazsa düğme metnini değil, gruplar arasındaki farkı ölçmüş oluruz.

Bir deney başlamadan önce **birincil metriği** seçin. Bu metrik kayıt dönüşüm oranı, satın alma oranı ya da aktifleşme olabilir. Dönüşüm oranı basitçe şöyle hesaplanır:

$$\hat{p} = \frac{\text{dönüşüm sayısı}}{\text{ziyaretçi sayısı}}$$

Örneğin A’da 10.000 ziyaretçiden 800 kişi kayıt olduysa $\hat{p}_A=0{,}08$; B’de 10.000 ziyaretçiden 880 kişi kayıt olduysa $\hat{p}_B=0{,}088$ olur. Gözlenen fark $0{,}8$ yüzde puandır. Ancak bu farkın gerçek bir iyileşme mi, yoksa örnekleme şansı mı olduğunu istatistiksel test yanıtlar.

| Kavram | Ne söyler? | Yaygın hata |
|---|---|---|
| Sıfır hipotezi ($H_0$) | Varyantlar arasında gerçek fark yoktur. | “Kesinlikle aynıdır” diye yorumlamak |
| Alternatif hipotez ($H_1$) | B’nin etkisi A’dan farklıdır. | Etki yönünü önceden tanımlamamak |
| p-değeri | $H_0$ doğruysa, en az bu kadar uç bir sonucu görme olasılığıdır. | “Sonucun doğru olma olasılığı” sanmak |
| Güven aralığı | Etkinin makul değer aralığını gösterir. | Sadece p-değerine bakmak |

İki oran arasındaki fark için yaklaşık test istatistiği şu yapıdadır:

$$z=\frac{\hat{p}_B-\hat{p}_A}{\sqrt{\hat{p}(1-\hat{p})(1/n_A+1/n_B)}}$$

Burada $\hat{p}$ iki grubun birleştirilmiş dönüşüm oranıdır. Çoğu ekip $\alpha=0{,}05$ anlamlılık eşiğini kullanır. p-değeri bu eşikten küçükse sonuç “istatistiksel olarak anlamlı” kabul edilir. Fakat anlamlılık, ürün açısından mutlaka önemli olduğu anlamına gelmez: Milyonlarca kullanıcıda %0,05 artış anlamlı çıkabilir ama geliştirme maliyetini karşılamayabilir.

| Karar boyutu | Sorulacak soru | Örnek |
|---|---|---|
| İstatistiksel anlamlılık | Sonuç şansla açıklanabilir mi? | p-değeri < 0,05 |
| Pratik anlamlılık | Etki iş hedefi için yeterli mi? | Gelir artışı maliyeti aşıyor mu? |
| Güvenlik metrikleri | Başka davranışlar zarar gördü mü? | İade oranı yükseldi mi? |

Örneklem büyüklüğünü testten **önce** belirlemek gerekir. Küçük örneklem gerçek faydayı kaçırabilir; dev örneklem ise önemsiz farkları “zafer” gibi gösterebilir. Hesaplama; mevcut dönüşüm oranı, saptamak istediğiniz minimum etki (MDE), anlamlılık seviyesi ve test gücüne bağlıdır. Genellikle %80 güç tercih edilir: Gerçekten hedeflenen büyüklükte bir etki varsa, testin bunu yakalama olasılığı %80’dir.

Aşağıdaki Python örneği, iki varyantın dönüşüm oranı için z-testi yapar. Kod, gözlenen farkın rastlantısal olup olmadığına hızlı bir ilk bakış sağlar:

```python
from statsmodels.stats.proportion import proportions_ztest

conversions = [800, 880]   # A ve B dönüşümleri
visitors = [10000, 10000]  # A ve B ziyaretçileri

z_score, p_value = proportions_ztest(conversions, visitors)
print(f"z: {z_score:.3f}, p-değeri: {p_value:.4f}")

if p_value < 0.05:
    print("Fark istatistiksel olarak anlamlı.")
else:
    print("Daha fazla veri veya farklı bir fikir gerekli.")
```

Son olarak test sırasında sonucu sürekli kontrol edip p-değeri 0,05’in altına iner inmez durdurmayın; bu davranış yanlış pozitif oranını yükseltir. Önceden belirlenen süreye, örneklem büyüklüğüne ve karar kuralına sadık kalın. Segment analizlerini de dikkatle yapın: Mobilde çalışan sonuç masaüstünde başarısız olabilir; fakat test sonrasında onlarca segment kazımak yanıltıcı “kazançlar” üretebilir. İyi A/B testi, yalnızca kazananı seçmez; ekibe kullanıcı davranışı hakkında güvenilir bir öğrenme döngüsü kurar.

![ab-testi-ve-58](/img/ab-testi-ve-58.svg)


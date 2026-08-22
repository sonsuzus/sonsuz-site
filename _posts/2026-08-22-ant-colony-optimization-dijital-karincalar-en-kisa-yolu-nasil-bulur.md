---
layout: post
title: "Ant Colony Optimization: Dijital Karıncalar En Kısa Yolu Nasıl Bulur?"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - optimizasyon
  - python
---

Bir karınca kolonisinin yiyeceğe giden en kısa rotayı bulması, ilk bakışta basit bir doğa olayı gibi görünür. Ancak binlerce karıncanın bıraktığı ve takip ettiği kimyasal izler, karmaşık optimizasyon problemlerini çözmek için güçlü bir fikir sunar. Ant Colony Optimization (ACO), merkezi bir yöneticiye ihtiyaç duymadan; küçük, basit kuralları izleyen yapay karıncaların kolektif zekâsıyla iyi çözümler üretir. Özellikle rota planlama, çizelgeleme ve ağ yönlendirme problemlerinde oldukça etkilidir.
``

Gerçek karıncalar hareket ederken **feromon** adı verilen kimyasal bir iz bırakır. Kısa rotadan geçen karınca, hedefe daha hızlı dönerek aynı yol üzerinde daha sık feromon bırakır. Böylece kısa yolların kokusu zamanla yoğunlaşır. Uzun rotalardaki feromon ise buharlaşma nedeniyle zayıflar. ACO, bu davranışı sayısal bir modele dönüştürür.

Bir yapay karınca, bulunduğu düğümden sonraki düğümü rastgele seçmez. Seçim olasılığı iki bilgi kaynağıyla hesaplanır: kenardaki mevcut feromon miktarı ve yolun yerel çekiciliği. Gezgin Satıcı Problemi (TSP) için çekicilik genellikle mesafenin tersidir: $\eta_{ij} = 1/d_{ij}$.

$$
P_{ij}^k = \frac{(\tau_{ij})^\alpha (\eta_{ij})^\beta}{\sum_{l \in N_i^k}(\tau_{il})^\alpha (\eta_{il})^\beta}
$$

Burada $P_{ij}^k$, $k$ numaralı karıncanın $i$ şehrinden $j$ şehrine gitme olasılığıdır. $\tau_{ij}$ feromon düzeyini, $N_i^k$ henüz ziyaret edilmemiş şehirleri gösterir. $\alpha$ feromona güveni, $\beta$ ise mesafe gibi sezgisel bilgiye güveni belirler.

| Kavram | Doğadaki karşılığı | Algoritmadaki görevi |
|---|---|---|
| Feromon ($\tau$) | Karıncanın koku izi | Daha önceki başarılı yolları hatırlar |
| Sezgisel bilgi ($\eta$) | Yakın hedefin cazibesi | Yerel olarak mantıklı seçimleri destekler |
| Buharlaşma ($\rho$) | Kokunun zamanla silinmesi | Eski ve kötü çözümlere saplanmayı önler |
| Koloni | Karınca grubu | Aynı turda farklı çözümler araştırır |

Her iterasyon sonunda karıncaların oluşturduğu turlar değerlendirilir. İyi tur bulan karıncalar, kullandıkları kenarlara daha fazla feromon ekler. Güncelleme fikri şu şekilde özetlenebilir:

$$
\tau_{ij} \leftarrow (1-\rho)\tau_{ij} + \sum_k \Delta\tau_{ij}^k
$$

$\rho$ buharlaşma oranıdır. Değeri çok küçükse algoritma geçmiş kararlarına aşırı bağlanabilir; çok büyükse faydalı deneyimler hızla unutulur. Genellikle $0 < \rho < 1$ seçilir. Bir karıncanın katkısı, tur uzunluğu $L_k$ ile ters orantılı verilebilir: $\Delta\tau_{ij}^k = Q/L_k$. Yani kısa tur, daha kuvvetli dijital koku bırakır.

Aşağıdaki sade Python örneği, bir sonraki şehrin olasılıksal seçimini gösterir. Gerçek projede bu fonksiyon her karınca ve her tur için çağrılır.

```python
import random

def sonraki_sehir(secilebilir, feromon, mesafe, mevcut, alpha=1, beta=3):
    agirliklar = []
    for hedef in secilebilir:
        iz = feromon[mevcut][hedef] ** alpha
        gorunurluk = (1 / mesafe[mevcut][hedef]) ** beta
        agirliklar.append(iz * gorunurluk)

    # Ağırlıklara göre rastgele seçim: keşif tamamen kaybolmaz.
    return random.choices(secilebilir, weights=agirliklar, k=1)[0]
```

Bu yaklaşımın önemli gücü, **keşif** ve **sömürü** arasındaki dengedir. Sadece en yoğun feromonu izleyen koloni erken bir çözümde kilitlenebilir. Tamamen rastgele hareket eden koloni ise öğrendiklerini kullanamaz.

| Ayar | Yüksek olduğunda etkisi | Olası risk |
|---|---|---|
| $\alpha$ | Feromon geçmişi baskın olur | Yerel optimuma takılma |
| $\beta$ | Kısa kenarlar tercih edilir | Uzak ama iyi rotaları kaçırma |
| $\rho$ | Eski izler hızla silinir | Kararsız arama |
| Karınca sayısı | Daha geniş çözüm çeşitliliği | Daha yüksek hesaplama maliyeti |

ACO, kesin olarak küresel optimumu garanti etmez; fakat çözüm uzayı büyüdükçe pratik ve esnek bir sezgisel yöntemdir. Teslimat araçlarının rotalanması, üretim görevlerinin sıralanması veya ağ paketlerinin yönlendirilmesi gibi alanlarda, doğanın bu küçük navigatörleri şaşırtıcı derecede büyük problemleri çözmeye yardım eder.

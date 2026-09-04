---
layout: post
title: "Uzman Sistemlerden Derin Öğrenmeye: Tıbbi Teşhiste Algoritmik Evrim"
math: true
categories: 
  - Bilgi
tags: 
  - uzman sistemler
  - tıbbi yapay zeka
  - karar ağaçları
toc: true
---

Bir hastanın ateşi, öksürüğü ve laboratuvar sonuçları bilgisayara girildiğinde makine nasıl teşhis önerir? Tıbbi yapay zekânın ilk yanıtı oldukça insansıydı: Uzman doktorların kullandığı kuralları açıkça yazmak. Günümüzde görüntüleri milyonlarca parametreyle inceleyen derin öğrenme modellerine ulaşmış olsak da kural tabanlı uzman sistemler; açıklanabilirlikleri, denetlenebilirlikleri ve kritik kararları standartlaştırmaları sayesinde hâlâ önemini koruyor.
``

## Uzman sistem nasıl düşünür?

Uzman sistem, belirli bir alandaki insan bilgisini **bilgi tabanı** içinde saklar. Bir çıkarım motoru ise hasta verilerini bu bilgilerle karşılaştırarak sonuç üretir. En yaygın yapı şu tür kurallardan oluşur:

> Eğer ateş yüksekse, öksürük varsa ve akciğer grafisinde infiltrasyon görülüyorsa zatürre olasılığını artır.

Kurallar ileri zincirleme ile bulgulardan teşhise, geri zincirleme ile olası bir teşhisten doğrulanması gereken bulgulara doğru çalıştırılabilir. Karar ağacında aynı mantık dallara ayrılır: Her düğüm bir soru, her dal bir yanıt, yapraklar ise teşhis veya işlem önerisidir.

Bir testin başarısı yalnızca genel doğrulukla ölçülmez. Özellikle tehlikeli hastalıkların atlanmaması için duyarlılık önemlidir:

$$\text{Duyarlılık}=\frac{TP}{TP+FN}$$

Özgüllük ise sağlıklı kişilerin gereksiz yere hasta olarak işaretlenmemesini gösterir:

$$\text{Özgüllük}=\frac{TN}{TN+FP}$$

Burada $TP$ doğru pozitif, $FN$ yanlış negatif, $TN$ doğru negatif ve $FP$ yanlış pozitiftir. Nadir hastalıklarda yüzde 95 doğruluk etkileyici görünebilir; ancak model herkese “sağlıklı” diyorsa klinik açıdan neredeyse işe yaramazdır.

| Yaklaşım | Güçlü yönü | Temel sorunu |
|---|---|---|
| Kural tabanlı sistem | Karar gerekçesi açıkça izlenebilir | Yeni kuralları elle eklemek gerekir |
| Karar ağacı | Görselleştirmesi ve yorumlaması kolaydır | Derinleştiğinde aşırı öğrenebilir |
| İstatistiksel model | Olasılık ve belirsizlik sunabilir | Karmaşık ilişkileri kaçırabilir |
| Derin öğrenme | Görüntü ve sinyal verisinde güçlüdür | Açıklanabilirliği sınırlı olabilir |

## MYCIN’den günümüze algoritmik yolculuk

1970’lerde geliştirilen **MYCIN**, bakteriyel enfeksiyonlar ve antibiyotik seçimi için yüzlerce “eğer–ise” kuralı kullanıyordu. Belirsizliği yönetmek amacıyla kesinlik faktörlerinden yararlanması dönemi için yenilikçiydi. Ancak kuralların uzmanlardan çıkarılması zahmetliydi; sistem hastane altyapısına kolayca bağlanamıyor ve hukuki sorumluluk soruları doğuruyordu.

1990’lardan itibaren elektronik sağlık kayıtlarının yaygınlaşmasıyla karar ağaçları, lojistik regresyon ve Bayes ağları veriden öğrenmeye başladı. 2000’lerde destek vektör makineleri ve topluluk yöntemleri öne çıktı. 2010 sonrasında derin sinir ağları; radyoloji görüntüleri, patoloji slaytları ve kalp sinyalleri gibi yüksek boyutlu verilerde çarpıcı başarılar gösterdi. Günümüzde eğilim, kuralları tamamen terk etmek değil; klinik yönergeleri makine öğrenmesiyle birleştiren **hibrit sistemler** geliştirmektir.

## Basit bir kural motoru

Aşağıdaki Python örneği, bulguları puanlayarak açıklanabilir bir öneri üretir:

```python
def enfeksiyon_degerlendir(ates, crp, oksuruk):
    puan = 0
    nedenler = []

    if ates >= 38:
        puan += 2
        nedenler.append("yüksek ateş")
    if crp > 10:
        puan += 2
        nedenler.append("yüksek CRP")
    if oksuruk:
        puan += 1
        nedenler.append("öksürük")

    risk = "yüksek" if puan >= 4 else "düşük/orta"
    return risk, nedenler
```

Kod teşhis koymaz; yalnızca hangi kuralların tetiklendiğini bildirerek hekimi uyarır. Gerçek bir sistemde eşikler klinik araştırmalarla doğrulanmalı, yaş ve ek hastalıklar hesaba katılmalı, sonuçlar farklı hastanelerde test edilmelidir.

Sonuç olarak uzman sistemlerin en büyük katkısı doktorun yerini almak değil, karar sürecini tutarlı ve görünür hâle getirmektir. Modern yapay zekâ örüntü keşfinde güçlüdür; fakat veri yanlılığı, mahremiyet, açıklanabilirlik ve yanlış güven gibi riskler taşır. En güvenli yaklaşım, algoritmanın öneri sunduğu, hekimin klinik bağlamı değerlendirdiği ve nihai sorumluluğun insanda kaldığı iş birliğidir.

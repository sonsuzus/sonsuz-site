---
layout: post
title: "Director AI: Oyun Zorluğunu Oyuncuya Göre Yöneten Görünmez Yönetmen"
math: true
categories: 
  - Bilgi
tags: 
  - yapay zeka
  - oyun geliştirme
  - director ai
  - dinamik zorluk
  - left 4 dead
  - oyuncu deneyimi
toc: true
image: /img/director-ai-oyun-26.png
---

Bir oyunda tam rahatladığınız anda zombilerin koridordan taşması tesadüf olmayabilir. *Left 4 Dead* gibi yapımlarda kullanılan Director AI, önceden hazırlanmış olayları sırayla oynatmak yerine oyuncuların durumunu izler, gerilim seviyesini tahmin eder ve karşılaşmaları dinamik biçimde düzenler. Kısacası bu sistem, oyun dünyasının görünmez film yönetmenidir.

![director-ai-oyun-26](/img/director-ai-oyun-26.svg)

``

## Director AI tam olarak nedir?

Director AI, tek bir düşmanın nasıl hareket edeceğini belirleyen klasik yapay zekâdan farklıdır. Bireysel düşman AI'ı hedef seçme, siper alma veya yol bulma gibi yerel kararlarla ilgilenirken yönetmen sistemi bütün oyun deneyimini denetler.

| Sistem | İzlediği ölçek | Tipik karar |
|---|---|---|
| Düşman AI | Tek karakter | Kime saldırmalıyım? |
| Director AI | Takım ve bölüm | Ne zaman saldırı başlamalı? |
| Sabit zorluk | Önceden tanımlı kurallar | Düşman ne kadar güçlü? |
| Dinamik zorluk | Anlık oyuncu performansı | Baskı artırılmalı mı? |

Amaç oyuncuyu sürekli cezalandırmak değildir. İyi bir yönetmen; stres, rahatlama ve yeniden yükselişten oluşan dramatik bir ritim üretir. Kesintisiz baskı yorucu, sürekli kolaylık ise sıkıcıdır.

## Oyuncunun stresi nasıl ölçülür?

Sistem doğrudan oyuncunun heyecanını okuyamaz; bunun yerine ölçülebilir sinyaller kullanır. Can miktarı, takım üyeleri arasındaki mesafe, isabet oranı, alınan hasar, cephane ve son saldırıdan beri geçen süre bunlardan bazılarıdır.

Basitleştirilmiş bir stres puanı şöyle hesaplanabilir:

$$
S = 0.35D + 0.25(1-H) + 0.20I + 0.20A
$$

Burada $D$ normalize edilmiş hasarı, $H$ kalan sağlık oranını, $I$ takımın dağılma seviyesini ve $A$ aktif düşman yoğunluğunu temsil eder. Katsayıların toplamının $1$ olması yorumlamayı kolaylaştırır. Örneğin $S$ değeri $1$'e yaklaştıkça oyuncuların baskı altında olduğu varsayılır.

Tek karelik ölçümler yanıltıcı olabileceğinden üstel hareketli ortalama kullanılabilir:

$$
S_t = \alpha x_t + (1-\alpha)S_{t-1}
$$

Küçük bir $\alpha$, sistemin ani değişimlere aşırı tepki vermesini engeller. Böylece tek bir kötü nişan, hemen devasa bir zombi sürüsüyle sonuçlanmaz.

## Gerilim döngüsü

Director AI genellikle deneyimi aşamalara böler:

1. **Hazırlık:** Oyuncular kaynak toplar ve çevreyi inceler.
2. **Yükseliş:** Düşman sayısı veya özel tehdit olasılığı artar.
3. **Zirve:** Yoğun bir saldırı ya da kritik karşılaşma yaşanır.
4. **Rahatlama:** Baskı azaltılır, oyuncuya toparlanma fırsatı verilir.

Bu döngü yalnızca düşman sayısını değiştirmez. Sağlık paketlerinin konumu, müzik, özel düşman türleri ve alternatif yollar da yönetilebilir. Ancak sistem oyuncuya açıkça yardım ederse yapaylık hissi doğar. Bu nedenle ayarlamalar çoğunlukla perde arkasında yapılır.

## Basit bir yönetmen prototipi

Aşağıdaki Python örneği, stres puanına göre yönetmenin hangi aşamaya geçeceğini gösterir:

```python
class Director:
    def __init__(self):
        self.stress = 0.0
        self.phase = "hazirlik"

    def update(self, damage, low_health, isolation, enemies):
        sample = (
            0.35 * damage
            + 0.25 * low_health
            + 0.20 * isolation
            + 0.20 * enemies
        )

        # Ölçümü yumuşatarak ani ve dengesiz kararları önler.
        self.stress = 0.2 * sample + 0.8 * self.stress

        if self.stress < 0.25:
            self.phase = "yukselis"
        elif self.stress > 0.75:
            self.phase = "rahatlama"
        else:
            self.phase = "denge"

        return self.phase
```

Buradaki önemli ayrıntı ters dengedir: stres düşükken tehdit artırılır, yüksekken oyuncuya nefes aldırılır. Gerçek projelerde eşiklerin sürekli aşılmasını önlemek için histerezis, aşamalar için minimum süre ve rastlantısal seçim ağırlıkları da eklenir.

## Adil görünmek, adil olmaktan farklıdır

Dinamik zorluk sisteminin en büyük riski oyuncunun başarılarını değersizleştirmesidir. İyi oynayan kişiye durmadan daha güçlü düşman göndermek, ilerleme hissini yok edebilir. Çözüm; zorluğu yalnızca sayısal güçle değil, karşılaşma çeşitliliği ve tempo üzerinden düzenlemektir.

Başarılı bir Director AI, oyuncunun ne kazanacağını belirlemez; unutulmaz bir mücadele yaşayabileceği koşulları hazırlar. En iyi yönetmen de zaten varlığını hissettirmeden sahneyi yöneten yönetmendir.

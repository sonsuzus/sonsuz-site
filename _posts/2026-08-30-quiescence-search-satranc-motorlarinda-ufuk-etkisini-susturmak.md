---
layout: post
title: "Quiescence Search: Satranç Motorlarında Ufuk Etkisini Susturmak"
math: true
categories: 
  - Bilgi
tags: 
  - satranç motoru
  - yapay zeka
  - algoritmalar
toc: true
---

Satranç motorları yalnızca güçlü hamleler bulmaz; aynı zamanda *ne zaman hesaplamayı bırakacaklarını* da öğrenmek zorundadır. Sabit derinlikli minimax veya alpha-beta araması, taktik açıdan patlayan bir konumun tam ortasında durursa taş kaybını ya da zorunlu matı birkaç hamle sonrasına itebilir. Bu yanılsamaya **ufuk etkisi** denir. Quiescence Search (QS), ana aramanın yaprak düğümlerinde konumu daha sakin, yani ani taktik değişimlerin azaldığı bir noktaya taşıyarak değerlendirmeyi güvenilir hâle getirir.

``

## Ufuk etkisi neden ortaya çıkar?

Bir motorun arama derinliği 4 yarım hamle olsun. Motor, son seviyede vezirinin rakip at tarafından alınacağını görür; fakat bir sonraki hamlede rakibin atını kendi piyonu ile geri alabileceğini göremez. Bu nedenle konumu gereğinden kötü değerlendirir. Tersi durumda motor, rakibin yapacağı yıkıcı bir şah çekişi veya taş alma hamlesini derinlik sınırının arkasına gizleyerek sahte bir avantaj da görebilir.

Klasik minimax yaprakta doğrudan statik değerlendirme çağırır:

$$V(s) \approx E(s)$$

Burada $E(s)$; materyal, şah güvenliği, piyon yapısı ve taş etkinliği gibi özelliklerden hesaplanan değerlendirmedir. Ancak taşların havada olduğu bir konumda $E(s)$, fotoğrafın yalnızca ilk karesidir. Quiescence Search ise bu değeri taktik devamlarla düzeltir:

$$Q(s)=\max\left(E(s), \max_{m \in T(s)} -Q(\operatorname{play}(s,m))\right)$$

$T(s)$ genellikle alma hamleleri, terfiler ve bazen şah çekişlerinden oluşan taktik hamle kümesidir. Negamax biçimindeki eksi işareti, oyuncu değiştiğinde değerlendirmenin bakış açısını tersine çevirir.

| Özellik | Normal arama | Quiescence Search |
|---|---|---|
| Başlangıç noktası | Kök konum | Ana aramanın yaprakları |
| Hamle üretimi | Çoğu yasal hamle | Seçili taktik hamleler |
| Temel amaç | En iyi planı bulmak | Taktik gürültüyü azaltmak |
| Başlıca risk | Ufuk etkisi | Kontrolsüz dallanma |

## Stand-pat: “Hiçbir şey yapmasam ne olur?”

QS'nin kritik fikri **stand-pat** değeridir. Motor önce mevcut konumu statik olarak değerlendirir. Eğer bu değer beta sınırını aşıyorsa, rakibin zaten bu kadar iyi bir sonuca izin vermeyeceği varsayılır ve dal budanır. Bu, alpha-beta budamasının QS içindeki doğal uzantısıdır.

Aşağıdaki sadeleştirilmiş örnek, alma hamleleri üzerinden çalışan bir negamax QS gösterir:

```python
def quiescence(position, alpha, beta):
    stand_pat = evaluate(position)

    if stand_pat >= beta:
        return beta              # beta cut-off
    alpha = max(alpha, stand_pat)

    for move in ordered_captures(position):
        position.push(move)
        score = -quiescence(position, -beta, -alpha)
        position.pop()

        if score >= beta:
            return beta
        alpha = max(alpha, score)

    return alpha
```

`ordered_captures`, örneğin değerli kurbanları ve avantajlı alımları önce deneyerek budamayı güçlendirir. Pratik motorlar ayrıca **delta pruning** kullanır: Bir alma hamlesinin, olası kazanacağı taş değeri hesaba katılsa bile `alpha` değerini geçmesi imkânsızsa hamle hiç aranmaz.

## Her şah çekişini eklemek doğru mu?

İlk bakışta QS'ye bütün şah çekişlerini katmak cazip gelir. Fakat bu hamleler çok sayıda olabilir ve aramayı yeniden neredeyse tam genişlikli bir ağaca dönüştürebilir. Bu yüzden yaygın yaklaşım, alımları ve terfileri varsayılan olarak eklemek; şah çekişlerini ise sınırlı derinlikte, kaçış hamlesi az olan durumlarda veya özel uzatmalarla ele almaktır.

| Tasarım tercihi | Kazanç | Bedel |
|---|---|---|
| Yalnızca alımlar | Hızlı ve kararlı | Bazı zorlayıcı şahları kaçırabilir |
| Alımlar + terfiler | Geçer piyon taktiklerini yakalar | Küçük ek maliyet |
| Alımlar + tüm şahlar | Daha fazla taktik görür | Arama patlaması riski |

Sonuç olarak Quiescence Search, motorun daha derin düşünmesini sağlamaktan çok, **doğru yerde durmasını** sağlar. İyi bir statik değerlendirme motorun sezgisiyse, QS o sezginin taktik gürültü tarafından kandırılmasını engelleyen güvenlik kemeridir.

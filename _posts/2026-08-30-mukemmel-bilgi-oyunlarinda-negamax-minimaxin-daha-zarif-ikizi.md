---
layout: post
title: "Mükemmel Bilgi Oyunlarında Negamax: Minimax’in Daha Zarif İkizi"
math: true
categories: 
  - Bilgi
tags: 
  - negamax
  - minimax
  - oyun teorisi
toc: true
---

Satranç, dama veya tic-tac-toe gibi mükemmel bilgi oyunlarında iki oyuncu da tahtadaki her şeyi görür; gizli kartlar, zar şansı ya da sürpriz kutular yoktur. Bu ortamda bilgisayarın temel sorusu basittir: “Rakibim en iyi hamleyi yaparsa, benim en iyi hamlem ne olur?” Minimax bu sorunun klasik cevabıdır. Negamax ise aynı matematiği, iki ayrı MAX ve MIN rolünü tek bir zarif kuralla birleştirerek uygular.
``
## Minimax neden iki farklı role ihtiyaç duyar?

Klasik minimax ağacında bir oyuncu skoru **maksimize**, diğeri ise **minimize** eder. Değerlendirme fonksiyonu bilgisayarın bakış açısından `+10` veriyorsa, rakip için aynı konum doğal olarak `-10` anlamına gelir. Sıfır toplamlı oyunların sihri tam burada ortaya çıkar:

$$
V(s, oyuncu) = -V(s, rakip)
$$

Bir tarafın kazancı diğer tarafın eşit büyüklükte kaybıdır. Negamax, “minimize etmek” yerine rakibin en iyi sonucunu bulup işaretini ters çevirir. Böylece her rekürsif çağrı aynı işi yapar: mevcut oyuncu için en yüksek skoru ara.

| Özellik | Minimax | Negamax |
|---|---|---|
| Oyuncu rolleri | MAX ve MIN ayrı ele alınır | Tek tip oyuncu mantığı vardır |
| Rekürsif ifade | `max` ve `min` dallanır | Her seviyede `max` kullanılır |
| Skor dönüşümü | Perspektif elle yönetilir | Çağrı sonucunun işareti çevrilir |
| Uygun oyunlar | Genel adversarial oyunlar | İki oyunculu sıfır toplamlı oyunlar |

Minimax’in özeti şöyledir: MAX kendi çocukları arasındaki en büyük değeri seçer, MIN ise en küçüğünü. Negamax’ta bunun yerini şu kompakt eşitlik alır:

$$
N(s) = \max_{c \in Children(s)}(-N(c))
$$

Buradaki eksi işareti süs değildir. Çocuk düğüme geçtiğimizde oynama sırası rakibe geçer. Rakibin iyi gördüğü bir konum, bizim açımızdan kötü olmalıdır. Örneğin rakip için `8` değerindeki bir devam yolu bizim için `-8`’dir.

## Temel Negamax uygulaması

Aşağıdaki Python örneği, oyun kurallarını soyutlayan bir `state` nesnesi kullanır. Nesnenin hamle üretebildiğini, hamle oynayabildiğini ve terminal durumları değerlendirebildiğini varsayıyoruz.

```python
INF = float("inf")

def negamax(state, depth, color):
    if depth == 0 or state.is_terminal():
        # evaluate() her zaman beyaz perspektifinden skor üretir.
        return color * state.evaluate()

    best_score = -INF

    for move in state.legal_moves():
        child = state.play(move)
        # Rakibin perspektifindeki en iyi sonucu ters çeviririz.
        score = -negamax(child, depth - 1, -color)
        best_score = max(best_score, score)

    return best_score
```

`color` parametresi genellikle beyaz için `+1`, siyah için `-1` olur. Değerlendirme fonksiyonu sabit biçimde beyazın avantajını ölçüyorsa, `color * evaluate()` sonucu sıradaki oyuncunun perspektifine taşır. Rekürsif çağrıda hem skorun hem de `color` değerinin işaret değiştirmesi, perspektif değişimini tutarlı hâle getirir.

Bu yaklaşımın önemli avantajı, “şimdi MIN düğümünde miyim?” diye ayrı kod yolları yazmamanızdır. Her düğüm kendi adına en iyi hamleyi arar. Rakibin başarısı ise negatiflenmiş olarak geri gelir. Kod kısalır; daha önemlisi, perspektif hatası yapma olasılığı azalır.

## Derinlik, değerlendirme ve performans

Gerçek oyun ağaçları hızla büyür. Ortalama dallanma sayısı $b$, arama derinliği $d$ ise kaba maliyet $O(b^d)$ olur. Bu nedenle yalnızca saf Negamax çoğu ciddi oyunda yetersiz kalır. En doğal güçlendirme alpha-beta budamadır: Sonucun rakip tarafından zaten reddedileceği dalları incelemeden keser.

| Kavram | Görevi | Negamax içindeki yeri |
|---|---|---|
| Derinlik | Kaç hamle ileri bakılacağını belirler | Terminal kontrolünde azaltılır |
| Değerlendirme | Yaprak konuma sayısal değer verir | `color` ile perspektife çevrilir |
| Hamle sıralama | İyi adayları önce dener | Budamayı ciddi biçimde artırır |
| Alpha-beta | Gereksiz dalları eler | Negamax formuna doğrudan eklenir |

Negamax yalnızca bir kod golf numarası değildir; sıfır toplamlılığın doğrudan algoritmik ifadesidir. Ancak dikkat: Üç veya daha fazla oyunculu oyunlarda, işbirlikçi senaryolarda ya da kazançların birbirinin tam tersi olmadığı sistemlerde bu simetri bozulur. O durumda klasik minimax bile yeterli olmayabilir. Ama iki oyunculu, tam bilgili ve sıfır toplamlı bir tahtada Negamax, matematiğin “eksi işaretiyle gelen sadeliğidir.”

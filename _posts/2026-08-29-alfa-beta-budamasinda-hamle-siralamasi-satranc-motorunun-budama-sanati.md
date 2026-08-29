---
layout: post
title: "Alfa-Beta Budamasında Hamle Sıralaması: Satranç Motorunun Budama Sanatı"
math: true
categories: 
  - Bilgi
tags: 
  - alfa-beta budaması
  - satranç programlama
  - minimax
  - hamle sıralaması
---

Bir satranç motoru için iyi hamleyi bulmak yalnızca güçlü bir değerlendirme fonksiyonu yazmak değildir; aynı zamanda yanlış yolları mümkün olduğunca erken terk etmektir. Alfa-beta budaması bunu sağlar, fakat gerçek performansın gizli kahramanı hamle sıralamasıdır. Şah çeken, değerli taş kazandıran ya da önceki aramalarda başarılı olmuş hamleleri önce denemek, motorun arama ağacını adeta elektrikli testereyle budamasına yardım eder.
``

## Neden sıralama bu kadar önemlidir?

Minimax algoritması, her pozisyonda olası hamleleri inceleyerek en iyi sonucu seçer. Ancak satrançta dallanma faktörü çoğu zaman $b \approx 30-40$ civarındadır. Derinlik $d$ olduğunda kaba maliyet $O(b^d)$ olur; bu, birkaç ek yarım hamlede bile devasa bir hesap yükü demektir.

Alfa-beta, arama sırasında iki sınır tutar: MAX oyuncusunun garantilediği en iyi değer olan $\alpha$ ve MIN oyuncusunun kabul edeceği en düşük sınır olan $\beta$. Bir dalda $\alpha \geq \beta$ oluşursa, o dalın geri kalanı incelenmez. Çünkü taraflardan biri bu varyantı zaten seçmeyecektir.

İdeal sıralamada en iyi hamle her düğümde ilk denenirse alfa-beta'nın maliyeti yaklaşık olarak şu seviyeye yaklaşır:

$$O(b^{d/2})$$

Bu, pratikte arama derinliğini ciddi biçimde artırır. Kötü sıralama ise alfa-beta'yı neredeyse sıradan minimax kadar pahalı hâle getirebilir. Yani budama algoritması bıçaksa, hamle sıralaması bileme taşıdır.

| Sıralama kalitesi | Budama miktarı | Yaklaşık davranış |
|---|---:|---|
| Mükemmel | Çok yüksek | $O(b^{d/2})$ sınırına yaklaşır |
| Orta seviye | Değişken | Çoğu motorda gerçekçi hedef |
| Rastgele | Düşük | Minimax maliyetine yaklaşır |

## Satrançta hangi hamleler önce gelir?

Taktik hamleler, pozisyonun değerini hızlı değiştirebildikleri için öncelik kazanır. Şah çekme hamleleri rakibin cevaplarını kısıtlar; taş yemeler materyal dengesini doğrudan etkiler. Ancak her şah veya taş yeme hamlesi iyi değildir. Vezirle korunan bir piyonu almak, veziri kaybettiriyorsa motor bunu erken denese bile doğru değerlendirme sonunda ortaya çıkar. Sıralamanın amacı hamleyi peşinen doğru ilan etmek değil, umut vaat eden adayları önce incelemektir.

Yaygın bir öncelik sırası şöyledir:

| Öncelik | Hamle türü | Amaç |
|---:|---|---|
| 1 | TT hamlesi | Transposition table'da daha önce en iyi görülen hamle |
| 2 | Şah çekmeler | Rakip yanıtlarını daraltmak |
| 3 | Taş yemeler | Taktik kazançları erken bulmak |
| 4 | Killer hamleler | Aynı derinlikte daha önce kesme yapan sessiz hamleler |
| 5 | History hamleleri | Geçmişte sık kesme üreten hamleler |
| 6 | Diğer hamleler | Normal gelişim ve konumsal adaylar |

Taş yeme hamlelerinde klasik **MVV-LVA** (*Most Valuable Victim - Least Valuable Attacker*) sezgisinden yararlanılır. Yüksek değerli kurbanı düşük değerli taşla almak daha önce denenir. Örneğin piyonun veziri alması, vezirin piyonu almasına göre çok daha heyecan verici bir adaydır.

```python
def score_move(move, position, tt_move, killers, history):
    # Büyük puan, hamlenin daha erken aranacağı anlamına gelir.
    if move == tt_move:
        return 1_000_000

    score = 0
    if position.gives_check(move):
        score += 50_000

    if position.is_capture(move):
        victim = position.captured_piece_value(move)
        attacker = position.moving_piece_value(move)
        score += 10_000 + 16 * victim - attacker  # MVV-LVA

    if move in killers:
        score += 9_000

    score += history.get(move, 0)
    return score
```

Bu fonksiyon hamle üretmez; üretilmiş hamleleri puanlayıp sıralamak için kullanılır. Gerçek motorlarda taş yeme hamleleri için ayrıca `SEE` (*Static Exchange Evaluation*) uygulanabilir. SEE, aynı karedeki olası karşılıklı taş değişimlerini hesaplayarak görünüşte kârlı bir alışın gerçekten kayıp olup olmadığını tahmin eder.

## Iterative deepening ile düzenli öğrenme

Hamle sıralaması tek başına çalışmak zorunda değildir. Motor önce derinlik 1, sonra 2, 3 ve daha derin aramalar yaparsa, önceki turda bulunan en iyi hamle sonraki turun başında denenebilir. Buna iterative deepening denir. İlk bakışta tekrar iş yapmak gibi görünür; oysa daha derin aramada güçlü bir ilk hamle tahmini sunduğu için toplam süreyi çoğu zaman azaltır.

Sonuç olarak, şah çekmeler ve taş yemeler yalnızca satranç tahtasında taktik alarm değildir. Alfa-beta içinde doğru önceliklendirilirse, milyonlarca gereksiz düğümün hiç doğmadan elenmesini sağlayan hesaplama kısayollarına dönüşür.

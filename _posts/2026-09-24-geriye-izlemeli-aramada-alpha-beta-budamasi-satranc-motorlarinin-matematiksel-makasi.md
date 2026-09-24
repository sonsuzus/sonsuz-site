---
layout: post
title: "Geriye İzlemeli Aramada Alpha-Beta Budaması: Satranç Motorlarının Matematiksel Makası"
math: true
categories: 
  - Bilgi
tags: 
  - alpha-beta
  - minimax
  - yapay zeka
  - satranç
  - arama algoritmaları
  - oyun teorisi
toc: true
image: /img/geriye-izlemeli-aramada-93.png
---

Bir satranç motoru geleceği gerçekten görmez; olası hamleleri dallanan dev bir ağaç üzerinde sistematik biçimde dener. Ancak bütün dalları incelemek, daha açılışta hesaplama kaynaklarını tüketir. Alpha-beta budaması, sonuca etki etmeyeceği matematiksel olarak kanıtlanan dalları keserek motorun aynı sürede çok daha derine inmesini sağlayan akıllı makastır.

![geriye-izlemeli-aramada-93](/img/geriye-izlemeli-aramada-93.svg)

``

## Arama ağacının temel problemi

Satranç gibi iki oyunculu, sıfır toplamlı oyunlarda klasik yaklaşım **minimax** algoritmasıdır. MAX oyuncusu skoru büyütmeye, MIN oyuncusu küçültmeye çalışır. Yaprak konumların değerlendirme fonksiyonu $E(s)$ ise bir düğümün değeri dönüşümlü olarak şöyle hesaplanır:

$$V_{MAX}(s)=\max V(c), \qquad V_{MIN}(s)=\min V(c)$$

Burada $c$, mevcut konumdan ulaşılabilen çocuk konumlardır. Ortalama hamle sayısı $b$, incelenen derinlik $d$ olduğunda kaba zaman karmaşıklığı:

$$O(b^d)$$

Satrançta $b$ yaklaşık 35 kabul edilirse yalnızca 6 yarım hamlelik arama bile teorik olarak $35^6$ konum üretir. İşte üstel büyüme canavarı burada uyanır.

| Yaklaşım | İncelenen düğüm | Sonuç doğruluğu | Temel özellik |
|---|---:|---|---|
| Saf minimax | $O(b^d)$ | Kesin | Her dalı gezer |
| Alpha-beta, kötü sıralama | $O(b^d)$ | Kesin | Çok az budama yapar |
| Alpha-beta, ideal sıralama | $O(b^{d/2})$ | Kesin | Derinliği yaklaşık ikiye katlar |

Alpha-beta yaklaşık sonuç üretmez. Minimax ile aynı hamleyi seçer; yalnızca gereksiz hesapları atlar.

## Alpha ve beta neyi temsil eder?

Arama boyunca iki sınır taşınır:

- **Alpha ($\alpha$):** MAX oyuncusunun şimdiye kadar garanti ettiği en yüksek değer.
- **Beta ($\beta$):** MIN oyuncusunun şimdiye kadar garanti ettiği en düşük değer.

Bir noktada $\alpha \ge \beta$ olursa kalan çocukları incelemek anlamsızdır. Çünkü üst seviyedeki oyuncu, bu dala gelmek yerine zaten daha iyi veya eşit bir seçeneğe sahiptir. Buna **beta kesmesi** ya da genel adıyla budama denir.

Örneğin MIN düğümü daha önce 4 değerini bulmuş olsun; yani $\beta=4$. Yeni çocuk dalında MAX, 7 değerini garanti etmişse bu dalın sonucu en az 7 olacaktır. MIN zaten 4’ü seçebildiği için 7 veya daha büyük sonuç veren dalın devamıyla ilgilenmez.

## Geriye izlemeli uygulama

Aşağıdaki Python kodu, hamleyi uygular, alt ağacı araştırır ve ardından geri alır. Bu desen bellek tüketimini azaltır:

```python
def alpha_beta(state, depth, alpha, beta, maximizing):
    if depth == 0 or state.is_terminal():
        return state.evaluate()

    if maximizing:
        value = float('-inf')
        for move in order_moves(state.legal_moves()):
            state.make(move)              # Hamleyi geçici uygula
            score = alpha_beta(state, depth - 1, alpha, beta, False)
            state.unmake(move)            # Önceki konuma geri dön
            value = max(value, score)
            alpha = max(alpha, value)
            if alpha >= beta:
                break                     # Kalan dallar sonucu değiştiremez
        return value

    value = float('inf')
    for move in order_moves(state.legal_moves()):
        state.make(move)
        score = alpha_beta(state, depth - 1, alpha, beta, True)
        state.unmake(move)
        value = min(value, score)
        beta = min(beta, value)
        if alpha >= beta:
            break
    return value
```

`make` ve `unmake`, bütün tahtayı her çağrıda kopyalamak yerine yalnızca değişiklikleri uygular ve geri çevirir. Gerçek motorlarda rok hakları, geçerken alma karesi ve hamle sayacı da eksiksiz saklanmalıdır.

## Budamayı kusursuzlaştıran hamle sıralaması

Alpha-beta’nın gücü, iyi hamlelerin önce denenmesine bağlıdır. Kesin kesmeye yol açacak hamleyi sona bırakırsanız algoritma turist gibi bütün ağacı dolaşır.

| Teknik | Önce incelenen hamleler | Kazanç |
|---|---|---|
| Yakalama sıralaması | Değerli taşı alan ucuz taşlar | Erken taktik kesmeler |
| Killer heuristic | Aynı derinlikte kesme yapan hamleler | Tekrarlanan kalıplar |
| History heuristic | Geçmişte başarılı sessiz hamleler | Konumdan bağımsız öncelik |
| Transposition table | Daha önce bulunan en iyi hamle | Tekrarlı konumları azaltma |

Bunlara **iterative deepening** eklenir: motor önce derinlik 1’i, sonra 2’yi ve giderek daha derin seviyeleri arar. Önceki turun en iyi hamlesi sonraki turda ilk sıraya alınır. Ayrıca yaprakta ani şah çekme veya taş alma varsa **quiescence search** sürdürülerek yanıltıcı, gürültülü değerlendirmeler engellenir.

Sonuç olarak kusursuz alpha-beta yalnızca iki sınırdan ibaret değildir. Doğru geri alma mekanizması, güçlü hamle sıralaması, konum önbelleği ve sakinlik araması birleştiğinde motor, daha fazla düşünmek yerine daha az ama anlamlı dal düşünür. Satranç zekâsının önemli kısmı da tam olarak budur: Her ihtimali hesaplamak değil, hangilerinin hesaplanmaya değmeyeceğini bilmektir.

---
layout: post
title: "Minimax Ağaçlarında Transposition Tables: Aynı Pozisyonu İki Kez Düşünmemek"
math: true
categories: 
  - Bilgi
tags: 
  - minimax
  - transposition table
  - yapay zeka
toc: true
---

Satranç, dama veya Connect Four oynayan bir yapay zekânın en pahalı alışkanlığı aynı pozisyonu tekrar tekrar analiz etmektir. Farklı hamle sıraları, tahtada birebir aynı duruma ulaşabilir; buna **transposition** denir. Transposition table (TT), daha önce hesaplanan bu durumları önbelleğe alır ve minimax aramasının “bu filmi izlemiştim” diyerek pahalı alt ağacı atlamasını sağlar.
``

## Neden aynı düğüm yeniden oluşur?

Arama ağacı çoğu zaman gerçekte ağaç değildir; durumların hamlelerle bağlandığı yönlü bir grafiktir. Örneğin iki bağımsız taşın hareket sırası değişebilir: önce A, sonra B oynamakla önce B, sonra A oynamak aynı tahtayı üretebilir. Saf minimax bu iki yolu ayrı alt ağaçlar sayar. TT ise ikisinin de aynı duruma işaret ettiğini fark eder.

Klasik minimax’ın dallanma faktörü $b$, derinliği $d$ ise kaba maliyeti $O(b^d)$’dir. Her durumda mucize beklemek doğru değildir; yine de tekrar eden konumlar fazlaysa etkin benzersiz durum sayısı dramatik biçimde azalır. Özellikle alpha-beta budamasıyla beraber TT, daha iyi hamle sıralaması sağladığı için aramayı pratikte çok daha derinlere taşır.

| Yaklaşım | Aynı konuma yeniden rastlayınca | Tipik sonuç |
|---|---|---|
| Saf minimax | Alt ağacı baştan arar | Fazla düğüm ziyareti |
| Alpha-beta | Bazı dalları sınırlar ile keser | Hamle sırasına duyarlı hızlanma |
| Alpha-beta + TT | Önceki değeri veya sınırı kullanır | Daha az hesap, daha iyi sıralama |

## Tabloya ne konur?

Bir TT girdisinin anahtarı, pozisyonun hızlı ve yeterince benzersiz temsilidir. Pratikte **Zobrist hashing** kullanılır: her kare-taş kombinasyonuna rastgele bir bit dizisi atanır, tahtadaki ilgili değerler XOR’lanır. Sıra kimde, rok hakkı veya en passant gibi oyun durumları da anahtara dahil edilmelidir. Aksi halde görünüşte aynı, ama kurallarca farklı iki konum yanlışlıkla eşleşir.

Değerin yanında arama derinliği ve sonucun türü tutulur. Çünkü derinliği 3 olan bir değerlendirme, derinliği 8 aramasının yerini güvenle tutamaz. Ayrıca alpha-beta bağlamında saklanan değer her zaman kesin sonuç değildir:

| Bayrak | Anlamı | Yeniden kullanım |
|---|---|---|
| `EXACT` | Gerçek minimax değeri bulundu | Doğrudan döndür |
| `LOWERBOUND` | Değer en az bu kadar | Alpha değerini yükselt |
| `UPPERBOUND` | Değer en fazla bu kadar | Beta değerini düşür |

Bu sınırlar kritik bir ayrıntıdır. Bir düğüm budandığında elde edilen puan, tam değerlendirme olmayabilir. Onu yanlışlıkla `EXACT` diye kaydetmek, motorun güvenle ama yanlış karar vermesine yol açar.

## Alpha-beta ile orta düzey bir TT iskeleti

Aşağıdaki örnek, tablo kaydını aramaya bağlayan temel mantığı gösterir. `hash_position`, bütün kural durumlarını içeren 64 bitlik bir anahtar üretmelidir.

```python
TT = {}  # key -> (depth, score, flag, best_move)

EXACT, LOWER, UPPER = 0, 1, 2

def alphabeta(pos, depth, alpha, beta):
    if depth == 0 or pos.is_terminal():
        return pos.evaluate()

    key = pos.hash_position()
    alpha_original = alpha
    entry = TT.get(key)

    if entry and entry[0] >= depth:
        saved_depth, score, flag, _ = entry
        if flag == EXACT:
            return score
        if flag == LOWER:
            alpha = max(alpha, score)
        elif flag == UPPER:
            beta = min(beta, score)
        if alpha >= beta:
            return score

    best_score, best_move = -float('inf'), None
    moves = pos.ordered_moves(entry[3] if entry else None)
    for move in moves:
        score = -alphabeta(pos.play(move), depth - 1, -beta, -alpha)
        if score > best_score:
            best_score, best_move = score, move
        alpha = max(alpha, score)
        if alpha >= beta:
            break

    flag = UPPER if best_score <= alpha_original else LOWER if best_score >= beta else EXACT
    TT[key] = (depth, best_score, flag, best_move)
    return best_score
```

Kod negamax biçimini kullanır; oyuncu değişince değer işareti ters çevrilir. Tablo ayrıca `best_move` saklar. Bu hamleyi sonraki aramada ilk denemek, alpha-beta kesmelerini artıran küçük ama etkili bir optimizasyondur.

Son olarak, hash çakışmaları teorik olarak mümkündür. 64 bit anahtarlar çoğu hobi projesinde yeterlidir; rekabetçi motorlarda doğrulama bilgisi, yaşlandırma stratejisi ve sınırlı tablo boyutu uygulanır. Özetle TT yalnızca hafıza değil, aramanın geçmiş deneyimidir: motor her yeni varyantta düşünür, ama aynı pozisyona geldiğinde unutmaz.

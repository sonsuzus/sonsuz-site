---
layout: post
title: "Minimax Algoritmasında Tahta Değerlendirme: Satranç Motorlarının Pozisyonel Matematiği"
math: true
categories: 
  - Bilgi
tags: 
  - minimax
  - satranç motoru
  - yapay zeka
---

Bir satranç motoru yalnızca taş saymaz; şah güvenliğini, piyon yapısını, merkez kontrolünü ve taşların gelecekteki hareket alanını da sayısallaştırmaya çalışır. Minimax algoritması hamle ağacında en iyi kararı ararken, ağacın derinliğinin yetmediği yaprak düğümlerde bir **değerlendirme fonksiyonuna** ihtiyaç duyar. Bu fonksiyon, “Bu konum kimin için daha iyi?” sorusunu matematiksel bir skora dönüştürür.
``

Temel yaklaşım, konumu beyaz açısından pozitif ve siyah açısından negatif bir değerle ifade etmektir. En yaygın formül şöyledir:

$$E(s)=M(s)+P(s)+K(s)+A(s)+S(s)+T(s)$$

Burada $s$ tahta durumudur; $M$ materyal, $P$ piyon yapısı, $K$ şah güvenliği, $A$ aktivite, $S$ alan/merkez kontrolü ve $T$ tempo bileşenidir. Pratikte her bileşen ayrıca bir ağırlıkla çarpılır. Böylece motorun karakteri değiştirilebilir: Agresif bir motor şah saldırısına daha büyük ağırlık verirken, konumsal bir motor zayıf kareleri ve piyon çoğunluklarını daha fazla önemser.

## Materyal: Gerekli ama Yetersiz Başlangıç

Klasik taş değerleri piyon için 100 santipiyon (cp) baz alınarak kurulabilir. Santipiyon kullanmak, yarım piyon gibi küçük üstünlükleri belirtmeyi kolaylaştırır.

| Taş | Geleneksel değer | Neden sabit değildir? |
|---|---:|---|
| Piyon | 100 | Geçer piyon olduğunda değeri yükselir. |
| At | 320 | Kapalı merkezlerde genellikle güçlenir. |
| Fil | 330 | Açık pozisyonlarda ve iki fil avantajında değerlidir. |
| Kale | 500 | Açık hatlarda ve yedinci yatayda etkisi artar. |
| Vezir | 900 | Erken oyunda savunmasız kalabilir; taktik yükü yüksektir. |

Salt materyal hesabı, motorun fedaları anlayamamasına yol açar. Örneğin beyaz bir piyon eksik olsa da gelişimini tamamlamış, siyah şahı merkezde kalmış olabilir. Bu nedenle $M(s)$ yalnızca ilk terimdir, kararın tamamı değildir.

## Parça-Kare Tabloları ve Konumsal Bonuslar

Bir taşın değeri bulunduğu kareye göre değişir. Bu davranış **parça-kare tablosu** (Piece-Square Table, PST) ile modellenir:

$$PST(s)=\sum_{p\in White}v_p(q_p)-\sum_{p\in Black}v_p(\operatorname{mirror}(q_p))$$

$q_p$, taşın bulunduğu kareyi; `mirror` ise siyah taşlar için tahtayı dikey olarak ters çevirmeyi temsil eder. Böylece beyaz atın e5 karesindeki bonusu ile siyah atın e4 karesindeki bonusu simetrik ölçülür.

```python
PIECE_VALUE = {"P": 100, "N": 320, "B": 330, "R": 500, "Q": 900, "K": 0}

def evaluate(board):
    score = 0
    for square, piece in board.items():
        sign = 1 if piece.isupper() else -1
        kind = piece.upper()
        # pst[kind][square], ilgili taşın o karedeki konumsal bonusudur.
        score += sign * (PIECE_VALUE[kind] + pst[kind][square])

    score += 18 * count_legal_moves(board, "white")
    score -= 18 * count_legal_moves(board, "black")
    score += pawn_structure_score(board)
    score += king_safety_score(board)
    return score
```

Bu örnekte hareketlilik her yasal hamle için 18 cp ile ödüllendiriliyor. Gerçek motorlarda bu katsayılar elle seçilmek yerine binlerce oyun veya öz-oyun verisi üzerinde ayarlanabilir.

## Piyon Yapısı, Şah Güvenliği ve Aşama Faktörü

Piyonlar geri gidemez; bu yüzden değerlendirme fonksiyonunun uzun vadeli hafızası gibidir. İzole piyon cezası, çift piyon cezası ve geçer piyon bonusu tipik terimlerdir. Ancak geçer piyonun değeri sabit olmamalıdır:

$$B_{passed}=b\cdot r^2$$

Burada $r$, piyonun terfiye yaklaştıkça artan göreli sırasıdır. Kare alınmış bir bonus, yedinci yataydaki geçer piyonun neden dramatik derecede önemli olduğunu güzelce yansıtır.

| Özellik | Açılış | Oyun ortası | Oyun sonu |
|---|---:|---:|---:|
| Şah güvenliği ağırlığı | Orta | Çok yüksek | Düşük |
| Merkez ve gelişim | Çok yüksek | Yüksek | Orta |
| Geçer piyon bonusu | Düşük | Orta | Çok yüksek |
| Şah aktivitesi | Düşük | Düşük | Yüksek |

Bu geçiş, oyun aşaması katsayısı ile yapılır. Örneğin $\lambda\in[0,1]$ oyun sonuna yaklaştıkça büyüsün. Nihai skor:

$$E=(1-\lambda)E_{mid}+\lambda E_{end}$$

Son olarak Minimax taraf işaretini doğru kullanmalıdır: beyaz maksimize eder, siyah minimize eder. Daha ileri motorlarda ise bu doğrusal formül; saldırı haritaları, tehditler, bağlı taşlar ve hatta sinir ağı çıktılarıyla zenginleşir. Yine de sağlam bir materyal + PST + piyon yapısı + şah güvenliği temeli, anlaşılabilir ve geliştirilebilir bir motorun en iyi başlangıç noktasıdır.

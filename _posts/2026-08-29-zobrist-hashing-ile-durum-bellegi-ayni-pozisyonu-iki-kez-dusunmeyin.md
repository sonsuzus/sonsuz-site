---
layout: post
title: "Zobrist Hashing ile Durum Belleği: Aynı Pozisyonu İki Kez Düşünmeyin"
math: true
categories: 
  - Bilgi
tags: 
  - Zobrist Hashing
  - Oyun Yapay Zekası
  - Algoritmalar
---

Bir satranç motoru ya da bir zeka oyunu ajanı, hamle ağacında ilerlerken şaşırtıcı derecede sık biçimde aynı tahtaya yeniden ulaşır. Farklı hamle sıraları aynı konumu üretebilir; ayrıca arama algoritmaları önceki derinliklerde gördüğü dalları tekrar ziyaret edebilir. Her seferinde konumu sıfırdan değerlendirmek, motorun işlemcisini adeta aynı bulmacayı tekrar tekrar çözen sabırsız bir öğrenciye dönüştürür. Zobrist Hashing, oyun durumlarını çok hızlı biçimde parmak iziyle temsil ederek bu tekrarları yakalamayı sağlar.
``

Temel fikir basittir: Tahtadaki anlamlı her özellik için rastgele, genellikle 64 bitlik bir sayı üretilir. Satrançta bu özellikler `taş türü × renk × kare` kombinasyonlarıdır. Örneğin beyaz atın `f3` karesinde durması için önceden atanmış bir sayı bulunur. Mevcut pozisyonun özeti, tahtada bulunan tüm taşların sayılarının XOR işlemiyle birleştirilmesiyle hesaplanır:

$$H = Z(p_1, s_1) \oplus Z(p_2, s_2) \oplus \dots \oplus Z(p_n, s_n)$$

Burada $Z(p_i, s_i)$, $i$. taşın türü ve karesi için rastgele anahtarı; $\oplus$ ise bit düzeyinde XOR işlemini ifade eder. XOR'un sihri, bir değeri iki kez uygularsanız onu geri alabilmenizdir: $a \oplus b \oplus b = a$. Dolayısıyla hamle sonrası bütün tahtayı taramak yerine, yalnızca değişen karelerin anahtarlarını XOR'lamak yeterlidir.

| Yaklaşım | Pozisyon hesaplama maliyeti | Tipik kullanım |
|---|---:|---|
| Tahtayı serialize etmek | $O(n)$ | Hata ayıklama, küçük projeler |
| Her seferinde hash üretmek | $O(n)$ | Basit prototipler |
| Zobrist ile artımlı güncelleme | $O(1)$ | Motorlar ve derin arama |

Zobrist anahtarı yalnızca taşları kapsamak zorunda değildir. Sıra kimdeyse, rok hakları, en passant karesi veya oyuna özgü özel kurallar da hash'e eklenmelidir. Aksi halde taş dizilimi aynı olsa bile kuralları farklı iki pozisyon yanlışlıkla eş kabul edilir. Satrançta bu hata, motorun yasal olmayan bir devam yolunu hatırlamasına yol açabilir.

Aşağıdaki JavaScript örneği, basitleştirilmiş bir tahta için anahtar üretimi ve hamle güncellemesini gösterir. Gerçek projelerde rastgele sayılar için güvenilir bir `uint64` üreticisi veya `BigInt` kullanılmalıdır.

```js
// pieceKeys["white_knight"]["f3"] gibi erişilen önceden üretilmiş 64-bit anahtarlar.
const sideToMoveKey = random64();

function hashPosition(board, whiteToMove) {
  let hash = 0n;
  for (const square of Object.keys(board)) {
    const piece = board[square];
    if (piece) hash ^= pieceKeys[piece][square];
  }
  if (whiteToMove) hash ^= sideToMoveKey;
  return hash;
}

function updateMove(hash, piece, from, to) {
  hash ^= pieceKeys[piece][from]; // Taşı eski kareden kaldır.
  hash ^= pieceKeys[piece][to];   // Taşı yeni kareye ekle.
  hash ^= sideToMoveKey;          // Sırayı değiştir.
  return hash;
}
```

Bu kodda `updateMove`, normal bir hamleyi sabit zamanda işler. Taş alma durumunda rakip taşın hedef kare anahtarı da XOR'lanarak kaldırılır. Terfi, rok ve en passant gibi özel hamleler ise birden fazla özellik güncellemesi gerektirir. Arama sırasında `makeMove` ile hash güncellenir; `unmakeMove` çağrısında aynı XOR'lar ters sırada uygulanarak eski hash zahmetsizce geri getirilir.

Hash tek başına genellikle bir **transposition table** anahtarıdır. Bu tabloda değerlendirme puanı, arama derinliği, sınır türü ve en iyi hamle saklanır. Aynı hash tekrar bulunursa motor, daha önce yaptığı hesabı kullanabilir.

| Saklanan alan | Neden gereklidir? |
|---|---|
| Hash anahtarı | Pozisyonu hızlı bulmak için |
| Derinlik | Eski sonucun yeterince ayrıntılı olup olmadığını anlamak için |
| Skor ve sınır | Alpha-beta budamasını güvenli hızlandırmak için |
| En iyi hamle | Hamle sıralamasını iyileştirmek için |

Elbette iki farklı konumun aynı 64 bit hash'e sahip olma ihtimali vardır; buna çakışma denir. İyi rastgele anahtarlarla olasılık çok düşüktür, fakat sıfır değildir. Kritik uygulamalarda tam anahtar saklamak, 128 bit kullanmak veya ikincil doğrulama eklemek riski azaltır. Sonuç olarak Zobrist Hashing, matematiksel olarak zarif XOR özelliğini kullanıp oyun motorlarına güçlü bir hafıza kazandırır: Daha az tekrar, daha derin arama ve daha akıllı hamleler.

---
layout: post
title: "A* Algoritmasıyla 15-Taş Bulmacasını Çözmek: Manhattan Mesafesi Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - a*
  - yapay zeka
  - python
  - 15-taş
  - algoritmalar
toc: true
---

15-taş bulmacası, 4×4 bir tahtadaki numaralı taşları boş kareyi kullanarak hedef düzene getirmeyi ister. Görünüşte basit olan bu oyun, bilgisayar biliminin klasik durum-uzayı arama problemlerinden biridir: Her tahta dizilimi bir **durum**, boşluğun hareketi bir **eylem**, hedef dizilim ise çözülmek istenen noktadır. Amaç yalnızca bir çözüm bulmak değil, mümkün olan en az hamleli çözümü bulmaktır. İşte A* algoritması, doğru sezgisel fonksiyonla bu işi akıllıca yapar.
``

## Neden körlemesine arama yetmez?

Her durumda boş kare teorik olarak dört yöne hareket edebilir. Tahtanın kenarları ve önceki adıma geri dönme gibi kısıtlar seçenekleri azaltır; yine de durum sayısı devasa boyuttadır. 15-taşın erişilebilir durum uzayı yaklaşık $16!/2 \approx 10^{13}$ farklı konfigürasyon içerir. Genişlik öncelikli arama (BFS), en kısa yolu garanti eder fakat özellikle zor örneklerde bellek tüketimi nedeniyle pratik değildir.

A* bu sorunu, şimdiye kadar ödenen maliyet ile hedefe kalan tahmini maliyeti birleştirerek çözer:

$$f(n) = g(n) + h(n)$$

Burada $g(n)$ başlangıçtan mevcut duruma kadar yapılan hamle sayısıdır. $h(n)$ ise hedefe ulaşmak için gereken hamle sayısının tahminidir. A*, her adımda $f(n)$ değeri en küçük olan durumu genişletir. Böylece hem kısa geçmiş yolları hem de umut verici gelecekleri dikkate alır.

| Kavram | Anlamı | 15-Taştaki karşılığı |
|---|---|---|
| `g(n)` | Kesin maliyet | Yapılmış hamle sayısı |
| `h(n)` | Tahmini kalan maliyet | Taşların hedefe uzaklığı |
| `f(n)` | Öncelik puanı | `g(n) + h(n)` |
| Açık küme | İncelenecek adaylar | Öncelik kuyruğundaki tahtalar |
| Kapalı küme | Görülmüş durumlar | Yeniden işlenmeyecek dizilimler |

## Manhattan mesafesi neden işe yarar?

Bir taşın bulunduğu satır-sütun ile hedef satır-sütunu arasındaki yatay ve dikey farkların toplamına Manhattan mesafesi denir. Örneğin 7 numaralı taş `(0, 1)` konumunda, hedefi `(1, 2)` ise uzaklığı $\vert 0-1\vert  + \vert 1-2\vert  = 2$ olur. Tüm taşların uzaklıkları toplanır; boş kare hesaba katılmaz.

$$h_{Manhattan}(s) = \sum_{tile \ne 0} \left(\vert r-r^*\vert  + \vert c-c^*\vert \right)$$

Bu sezgisel fonksiyon **kabul edilebilir**dir (*admissible*): Gerçek kalan maliyeti asla olduğundan büyük tahmin etmez. Çünkü bir taşı hedefe yaklaştırmak için en az Manhattan uzaklığı kadar hamle gerekir; üstelik taşların birbirini engellemesi gerçek maliyeti artırabilir. Ayrıca **tutarlı**dır (*consistent*): Tek hamleyle sezgisel değer en fazla 1 değişir. Bu iki özellik sayesinde A*, en kısa çözümü garanti eder.

| Sezgisel | Avantaj | Dezavantaj |
|---|---|---|
| Sıfır sezgiseli | Her zaman doğrudur | A*, BFS'e dönüşür |
| Yanlış yerdeki taş sayısı | Çok hızlı hesaplanır | Zayıf yönlendirme sağlar |
| Manhattan mesafesi | Güçlü ve güvenilir | Çakışan taşları ayrı düşünür |
| Manhattan + linear conflict | Daha az düğüm açar | Hesaplaması daha maliyetlidir |

## Python ile sezgisel hesaplama

Aşağıdaki fonksiyon, tahtayı 16 elemanlı bir demet olarak alır. `0`, boş kareyi temsil eder. Demet kullanmak önemlidir: Durumlar `set` içinde saklanabilir ve tekrar ziyaretler kolayca engellenir.

```python
GOAL = tuple(range(1, 16)) + (0,)
GOAL_POS = {tile: divmod(i, 4) for i, tile in enumerate(GOAL)}

def manhattan(board):
    total = 0
    for index, tile in enumerate(board):
        if tile == 0:
            continue
        row, col = divmod(index, 4)
        goal_row, goal_col = GOAL_POS[tile]
        total += abs(row - goal_row) + abs(col - goal_col)
    return total
```

A* uygulamasında öncelik kuyruğuna `(f, g, board)` benzeri kayıtlar eklenir. Bir komşu durum üretildiğinde yeni maliyet hesaplanır: `new_g = g + 1` ve `priority = new_g + manhattan(neighbor)`. Daha önce daha düşük `g` değeriyle görülmüş bir tahta tekrar kuyruğa alınmaz. Bu ayrıntı, boşluğun sağa-sola giderek sonsuz döngü oluşturmasını engeller.

Pratikte Manhattan mesafesini **linear conflict** ile güçlendirmek faydalıdır. Aynı satırda hedef satırlarına ait iki taş ters sıradaysa, en az iki ek hamle gerekir. Bu ceza Manhattan değerine eklenebilir; yine de kabul edilebilirlik korunur. Son olarak, her 15-taş diziliminin çözülebilir olmadığını unutmayın: A* çalıştırmadan önce inversiyon paritesi ve boş karenin satırı ile çözüm kontrolü yapmak, imkânsız bulmacalarda saatlerce arama yapılmasını önler.

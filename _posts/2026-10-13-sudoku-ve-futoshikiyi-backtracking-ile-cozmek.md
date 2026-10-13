---
layout: post
title: "Sudoku ve Futoshiki’yi Backtracking ile Çözmek"
math: true
categories: 
  - Program
tags: 
  - sudoku
  - futoshiki
  - backtracking
  - python
  - algoritma
  - kısıt-programlama
toc: true
image: /img/sudoku-ve-futoshikiyi-95.png
---

Sudoku’daki boş karelere bakıp “Buraya kesin 7 gelir!” demek kolaydır; bilgisayara neden 7 gelmesi gerektiğini anlatmak ise işin algoritmik kısmıdır. Sudoku ve Futoshiki, çözümün belirli kuralları aynı anda sağlaması gereken **kısıt tatmin problemleridir**. Bu yazıda kuralları matematiksel olarak modelleyecek ve Python ile genel amaçlı bir backtracking çözücüsü geliştireceğiz.


![sudoku-ve-futoshikiyi-95](/img/sudoku-ve-futoshikiyi-95.svg)

``

## Kısıt tatmin problemi nedir?

Bir **Kısıt Tatmin Problemi** (Constraint Satisfaction Problem veya CSP) üç temel bileşenden oluşur:

- **Değişkenler:** Doldurulacak hücreler
- **Alanlar:** Hücrelerin alabileceği değerler
- **Kısıtlar:** Hangi değer birleşimlerinin geçerli olduğu

$n \times n$ boyutlu bir bulmacada her hücreyi $X_{r,c}$ ile gösterelim. Hücrelerin değer alanı genellikle şöyledir:

$$X_{r,c} \in \{1,2,\ldots,n\}$$

Sudoku ve Futoshiki aynı aileden gelseler de kısıtları farklıdır:

| Özellik | Sudoku | Futoshiki |
|---|---|---|
| Satır kısıtı | Sayılar tekrarlanamaz | Sayılar tekrarlanamaz |
| Sütun kısıtı | Sayılar tekrarlanamaz | Sayılar tekrarlanamaz |
| Bölge kısıtı | Vardır | Yoktur |
| Eşitsizlik | Yoktur | `<` ve `>` ilişkileri vardır |
| Tipik boyut | $9 \times 9$ | $4 \times 4$ veya $5 \times 5$ |

Bir satırdaki değerlerin farklı olması matematiksel olarak `AllDifferent` kısıtıyla ifade edilir. Futoshiki’de ayrıca komşu hücreler arasında $X_{a}<X_{b}$ gibi ilişkiler bulunur.

## Backtracking nasıl çalışır?

Backtracking, boş bir hücre seçip olası değerleri sırayla dener. Bir değer kısıtları bozarsa o dalı terk eder; çıkmaz sokağa giren bir gezgin gibi geri dönüp diğer yolu seçer.

En kötü durumda çalışma süresi yaklaşık $O(n^m)$ olabilir. Burada $m$ boş hücre sayısıdır. Ancak geçersiz dalları erken budamak, pratikte aramayı ciddi ölçüde küçültür.

```python
def solve(board, is_valid):
    empty = find_empty(board)
    if empty is None:
        return True  # Tüm hücreler geçerli biçimde dolduruldu.

    row, col = empty
    for value in range(1, len(board) + 1):
        if is_valid(board, row, col, value):
            board[row][col] = value

            if solve(board, is_valid):
                return True

            board[row][col] = 0  # Çıkmaz sokak: hamleyi geri al.

    return False


def find_empty(board):
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == 0:
                return row, col
    return None
```

Bu kodun güzel tarafı, arama mekanizmasını bulmacanın kurallarından ayırmasıdır. `is_valid` fonksiyonunu değiştirerek aynı motoru iki bulmacada da kullanabiliriz.

## Sudoku kısıtlarını kodlamak

Sudoku’da aday değer satırda, sütunda veya ilgili bölgede bulunmamalıdır:

```python
def sudoku_valid(board, row, col, value):
    n = len(board)
    box = int(n ** 0.5)

    if value in board[row]:
        return False
    if any(board[r][col] == value for r in range(n)):
        return False

    start_row = (row // box) * box
    start_col = (col // box) * box
    for r in range(start_row, start_row + box):
        for c in range(start_col, start_col + box):
            if board[r][c] == value:
                return False

    return True
```

`row // box` işlemi hücrenin hangi bölgeye ait olduğunu belirler. Örneğin 9×9 Sudoku’da `box` değeri 3’tür.

## Futoshiki eşitsizliklerini eklemek

Futoshiki’de satır ve sütun benzersizliğine ek olarak eşitsizlikleri kontrol ederiz. İlişkileri `(sol_hücre, operatör, sağ_hücre)` biçiminde saklayabiliriz:

```python
def futoshiki_valid(board, row, col, value, constraints):
    n = len(board)
    if value in board[row]:
        return False
    if any(board[r][col] == value for r in range(n)):
        return False

    old = board[row][col]
    board[row][col] = value

    for left, op, right in constraints:
        lr, lc = left
        rr, rc = right
        a, b = board[lr][lc], board[rr][rc]
        if a and b and not (a < b if op == "<" else a > b):
            board[row][col] = old
            return False

    board[row][col] = old
    return True
```

Yalnızca iki hücre de doluysa eşitsizlik sınanır. Böylece henüz bilinmeyen bir değeri yanlışlıkla geçersiz saymayız.

## Daha akıllı arama

İlk boş hücreyi seçmek yerine **en az adaya sahip hücreyi** seçmek, Minimum Remaining Values sezgisidir. Ayrıca adayları önceden hesaplamak ve her atamadan sonra komşuların alanlarını daraltmak, yani ileri kontrol uygulamak mümkündür.

Backtracking’in özü basittir: **dene, kontrol et, ilerle; olmazsa geri dön**. Gücü ise Sudoku’nun bölgeleri veya Futoshiki’nin eşitsizlikleri gibi farklı kuralları aynı CSP modeli altında birleştirebilmesinden gelir. Böylece bilgisayar yalnızca sayı yerleştirmez; sistematik biçimde mantık yürütür.

---
layout: post
title: "Sudoku Üreticilerinde Backtracking: Simetrik, Benzersiz ve Ayarlanabilir Bulmacalar"
math: true
categories: 
  - Proje
tags: 
  - sudoku
  - backtracking
  - algoritmalar
  - python
  - oyun geliştirme
---

Bir Sudoku üreticisi, ekrana rastgele sayılar serpiştirmekten çok daha fazlasıdır: Ortaya çıkan tahtanın geçerli, tek çözümlü, estetik açıdan dengeli ve hedeflenen zorlukta olması gerekir. Bu hedeflerin merkezinde derinlik öncelikli arama (DFS) ile çalışan geri izleme, yani *backtracking*, bulunur. Algoritma yanlış bir seçime girdiğinde panik yapmaz; son kararı geri alır, başka olasılığı dener ve sabırla çözüm uzayını tarar.
``
Sudoku'nun temel kuralı, her satır, sütun ve 3×3 kutuda 1–9 rakamlarının birer kez görünmesidir. Hücreleri değişken, olası rakamları da değerler olarak düşünürsek bu problem bir **Kısıt Tatmin Problemi**dir (CSP). Bir hücreye atanabilecek aday kümesi şu şekilde yazılabilir:

$$A(r,c)=\{1,\ldots,9\}\setminus (R_r \cup C_c \cup B_{r,c})$$

Burada $R_r$ satırdaki, $C_c$ sütundaki ve $B_{r,c}$ ilgili kutudaki kullanılmış rakamlardır. $A(r,c)$ boşsa, mevcut seçimlerden biri hatalıdır; backtracking tam bu noktada bir önceki adıma döner.

## Üretim iki aşamalıdır

Sağlam bir üretici önce tamamen dolu, geçerli bir çözüm tahtası oluşturur. Ardından hücreleri kaldırır ve her kaldırma girişiminden sonra tahtanın hâlâ **tam olarak bir çözümü** olduğunu kontrol eder. Çözüm sayısı 1 değilse kaldırılan değer geri konur. Bu ayrım önemlidir: “çözülebilir” olmak, “benzersiz çözümlü” olmak demek değildir.

| Amaç | Yöntem | Başarı ölçütü |
|---|---|---|
| Tam tahta üretmek | Rastgeleleştirilmiş backtracking | Tüm hücrelerin geçerli dolması |
| İpucu kaldırmak | Simetrik hücre çiftlerini silmek | Çözüm sayısının 1 kalması |
| Zorluğu ayarlamak | Arama maliyetini ve ipucu sayısını izlemek | Hedef aralığa yaklaşmak |

180 derece dönel simetride $(r,c)$ hücresinin eşi $(8-r,8-c)$ olur. Bir hücreyi kaldırırken eşini de kaldırmak, oyuncunun gözüne daha dengeli görünen tahtalar üretir. Merkez hücre kendi eşidir; bu küçük istisna, tek sayıda ipucu hedeflerinde oldukça kullanışlıdır.

## En küçük aday, en büyük hız kazancı

Boş hücreleri soldan sağa seçmek çalışır, fakat çoğu zaman gereksiz dallanma yaratır. Bunun yerine **MRV** (*Minimum Remaining Values*) sezgiseli uygulanır: En az adaya sahip hücre önce seçilir. Arama ağacındaki yaklaşık ham olasılık sayısı $b^d$ ise, aday sayısı küçük hücreleri erkenden seçmek etkin dallanma katsayısını $b$ düşürür. Sonuç: daha az geri dönüş, daha hızlı üretim.

Aşağıdaki Python parçası, çözüm sayısını iki ile sınırlandıran bir kontrol fonksiyonunun çekirdeğidir. İki çözüm bulununca durmak yeterlidir; çünkü amacımız bütün çözümleri listelemek değil, benzersizliği test etmektir.

```python
def count_solutions(board, limit=2):
    cell = choose_mrv_cell(board)
    if cell is None:
        return 1  # Tahta tamamen dolu: bir çözüm bulundu.

    r, c = cell
    total = 0
    for value in candidates(board, r, c):
        board[r][c] = value
        total += count_solutions(board, limit - total)
        board[r][c] = 0  # Geri izleme: seçimi geri al.
        if total >= limit:
            return total
    return total
```

Üretimde `candidates` listesini karıştırmak, her çalıştırmada aynı çözümün çıkmasını engeller. İpucu silme döngüsünde ise bir simetri çifti geçici olarak sıfırlanır, `count_solutions(board)` çağrılır ve sonuç 1 ise silme kalıcı hâle getirilir.

## Zorluk yalnızca boş hücre sayısı değildir

40 ipuçlu bir tahta bazen 28 ipuçlu başka bir tahtadan daha zor olabilir. Çünkü zorluk, insan çözücünün görebildiği çıkarım zincirleriyle ilgilidir. Pratik bir üretici; ipucu sayısı, çözümleyicinin yaptığı geri dönüş sayısı ve kullanılan teknikleri birlikte puanlayabilir.

| Seviye | Yaklaşık ipucu | Çözücü sinyali |
|---|---:|---|
| Kolay | 36–45 | Tek aday ve gizli tekli yeterli |
| Orta | 32–36 | Daha uzun aday elemesi gerekir |
| Zor | 26–32 | Kontrollü tahmin veya gelişmiş desenler |

Sonuç olarak backtracking, Sudoku üreticisinin hem mimarı hem denetçisidir. Rastgelelik çeşitliliği sağlar; kısıtlar doğruluğu korur; çözüm sayacı benzersizliği garantiler; simetri ise bulmacaya profesyonel bir görünüm kazandırır. Bu dört parçayı birleştirdiğinizde, yalnızca çalışan değil, tekrar tekrar çözmek isteyeceğiniz Sudoku tahtaları üretebilirsiniz.

---
layout: post
title: "Kadane Algoritmasını 2B’ye Taşımak: Maksimum Toplamlı Alt Matris"
math: true
categories: 
  - Bilgi
tags: 
  - kadane algoritması
  - dinamik programlama
  - matris algoritmaları
toc: true
---

Bir boyutlu Kadane algoritması, sayı dizisindeki maksimum toplamlı kesintisiz aralığı doğrusal zamanda bulur. Peki sayılar tek sıra yerine bir matrisin hücrelerine dağılmışsa? Bu kez hedefimiz; satırları ve sütunları kesintisiz olan, toplamı mümkün olduğunca büyük bir dikdörtgen seçmektir. Neyse ki Kadane’yi çöpe atmıyoruz: Matrisi akıllıca sıkıştırarak problemi tekrar tek boyuta indiriyoruz.

``

## Önce tek boyutlu Kadane’yi hatırlayalım

Bir $A$ dizisi için her konumda şu kararı veririz: Önceki alt diziyi sürdürmek mi, yoksa mevcut elemanla yeni bir dizi başlatmak mı?

$$
bestEndingHere_i = \max(A_i,\ bestEndingHere_{i-1}+A_i)
$$

Genel cevap ise bütün konumlarda görülen en büyük değerdir:

$$
maximum = \max_i(bestEndingHere_i)
$$

Bu yaklaşımın zaman karmaşıklığı $O(n)$, ek alan ihtiyacı ise $O(1)$’dir. Önemli ayrıntı, bütün elemanlar negatif olduğunda başlangıç değerini sıfır değil ilk eleman olarak seçmektir. Aksi hâlde algoritma, gerçekte seçilemeyen boş bir alt dizi döndürebilir.

## Matris nasıl tek boyuta dönüşür?

$R \times C$ boyutlu bir matris düşünelim. Önce bir sol sütun, ardından ondan önce gelmeyen bir sağ sütun seçeriz. Bu iki sınır arasındaki değerleri her satır için topladığımızda, uzunluğu $R$ olan geçici bir dizi oluşur.

Örneğin sol sınır $L$, sağ sınır $K$ ise:

$$
temp[i] = \sum_{j=L}^{K} M[i][j]
$$

Artık `temp` üzerinde Kadane çalıştırabiliriz. Kadane’nin bulduğu maksimum alt dizi, seçili sütun sınırları arasında hangi satırların kullanılacağını söyler. Böylece üst, alt, sol ve sağ sınırları belirlenmiş bir alt matris elde ederiz.

| Yaklaşım | İncelenen yapı | Zaman karmaşıklığı |
|---|---|---:|
| Tüm dikdörtgenleri doğrudan toplama | Her alanı hücre hücre toplar | $O(R^3C^3)$ |
| Prefix sum ile tüm dikdörtgenler | Her alanı sabit zamanda hesaplar | $O(R^2C^2)$ |
| 2B Kadane | Sütun çiftleri ve sıkıştırılmış satırlar | $O(C^2R)$ |

Matris çok geniş fakat az satırlıysa algoritmayı transpoze etmek avantaj sağlar. Genel hedef, karesi alınan boyutu küçük seçmektir:

$$
O(\min(R,C)^2 \cdot \max(R,C))
$$

## C++ uygulaması

Aşağıdaki kod hem maksimum toplamı hem de dikdörtgenin koordinatlarını döndürür:

```cpp
#include <iostream>
#include <vector>
#include <climits>
using namespace std;

struct Result {
    long long sum;
    int top, left, bottom, right;
};

Result maxSumSubmatrix(const vector<vector<int>>& matrix) {
    int rows = matrix.size();
    int cols = matrix[0].size();
    Result answer{LLONG_MIN, 0, 0, 0, 0};

    for (int left = 0; left < cols; ++left) {
        vector<long long> compressed(rows, 0);

        for (int right = left; right < cols; ++right) {
            for (int row = 0; row < rows; ++row)
                compressed[row] += matrix[row][right];

            long long current = compressed[0];
            long long best = compressed[0];
            int candidateTop = 0, bestTop = 0, bestBottom = 0;

            for (int row = 1; row < rows; ++row) {
                if (current + compressed[row] < compressed[row]) {
                    current = compressed[row];
                    candidateTop = row;
                } else {
                    current += compressed[row];
                }

                if (current > best) {
                    best = current;
                    bestTop = candidateTop;
                    bestBottom = row;
                }
            }

            if (best > answer.sum)
                answer = {best, bestTop, left, bestBottom, right};
        }
    }
    return answer;
}
```

`compressed` dizisi, sağ sınır her ilerlediğinde yeni sütun eklenerek güncellenir. Böylece aynı toplamları tekrar tekrar hesaplamayız. `candidateTop` mevcut Kadane parçasının başlangıcını, `bestTop` ve `bestBottom` ise o turdaki en başarılı satır aralığını saklar.

## Neden gerçekten çalışıyor?

Her olası sol-sağ sütun çifti mutlaka denenir. Sabitlenmiş bir sütun çifti için herhangi bir dikdörtgenin toplamı, `compressed` dizisindeki kesintisiz bir satır aralığının toplamına eşittir. Kadane bu aralıkların en iyisini bulduğuna göre, bütün sütun çiftleri tamamlandığında hiçbir geçerli dikdörtgen gözden kaçmaz.

Kısacası 2B Kadane, yeni ve gizemli bir algoritmadan çok güçlü bir indirgeme tekniğidir: Bir boyutu sınırlarla sabitle, diğer boyutu topla ve bildiğin doğrusal çözümü çalıştır. Algoritmik dünyada bazen en iyi numara, zor problemi tanıdık bir probleme dönüştürmektir.

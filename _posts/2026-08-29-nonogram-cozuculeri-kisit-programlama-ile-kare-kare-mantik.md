---
layout: post
title: "Nonogram Çözücüleri: Kısıt Programlama ile Kare Kare Mantık"
math: true
categories: 
  - Program
tags: 
  - nonogram
  - constraint programming
  - algoritmalar
---

Nonogramlar, satır ve sütun kenarlarındaki sayı ipuçlarından hareketle hangi hücrelerin boyanacağını bulduğumuz görsel mantık bulmacalarıdır. İnsan için keyifli bir dedektiflik oyunu olan bu yapı, bilgisayar için de kısıt programlamanın (Constraint Programming, CP) oldukça temiz bir uygulamasıdır: Her hücre bir karar değişkeni, her ipucu ise çözüm uzayını daraltan bir kuraldır.

``

Bir $R \times C$ Nonogram tahtasını ikili değişkenlerle modelleyelim. Her hücre için $x_{r,c} \in \{0,1\}$ tanımlarız. Burada $1$ boyalı, $0$ boş hücreyi temsil eder. Ancak satırdaki boyalı hücre sayısını toplamak tek başına yeterli değildir. Örneğin `[2, 1]` ipucu, üç boyalı hücre demektir; fakat bu hücreler önce uzunluğu 2 olan, ardından en az bir boşlukla ayrılan uzunluğu 1 olan iki blok oluşturmalıdır.

Bir satırda blok uzunlukları $a_1, a_2, \ldots, a_k$ olsun. Blokların başlangıç konumlarını $s_i$ ile gösterebiliriz. Geçerli bir yerleşimde şu koşullar sağlanır:

$$1 \le s_1, \qquad s_{i+1} \ge s_i + a_i + 1, \qquad s_k + a_k - 1 \le C$$

Her blok kendi aralığındaki hücreleri 1 yapar; blokların dışındaki hücreler 0 olur. Aynı model hem satırlar hem de sütunlar için kurulur. İşin sihri burada başlar: Bir hücre, ait olduğu satırın **ve** sütununun kurallarını eşzamanlı karşılamak zorundadır. Yani satırdan gelen “burayı boya” bilgisi, sütunun olası düzenlerini azaltır; sütundan gelen bilgi de satırı sıkıştırır.

| Yaklaşım | Temel fikir | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| Kaba kuvvet | Tüm hücre kombinasyonlarını dener | Uygulaması basit | $2^{R\cdot C}$ nedeniyle hızla imkânsızlaşır |
| Satır deseni üretimi | Her satır için geçerli bit desenlerini listeler | Nonogram yapısına çok uygundur | Büyük satırlarda desen sayısı artabilir |
| Kısıt programlama | Değişken alanlarını ve kuralları yayar | Geri izlemeyi ciddi azaltır | Modelleme dikkat ister |

Pratik bir çözücüde yaygın teknik, her satır ve sütun için tüm geçerli desenleri önceden üretmektir. Örneğin genişliği 5 olan bir satırın `[2, 1]` ipucuna ait desenlerinden biri `##..#`, diğeri `.##.#` olabilir. Ardından mevcut hücre bilgileriyle çelişen desenler elenir. Kalan tüm satır desenlerinde bir hücre daima boyalıysa o hücre kesinlikle boyanır; daima boşsa kesinlikle boştur. Bu işlem satır-sütun arasında sabit noktaya ulaşana kadar tekrarlanır.

Aşağıdaki Python parçası, bir çizginin aday desenlerinden hücre zorunluluklarını çıkarır:

```python
def zorunlu_hucreler(adaylar):
    # Adaylar, örneğin "##..#" gibi aynı uzunlukta dizgelerdir.
    # Tüm adaylarda ortak olan karakterler kesin bilgidir.
    sonuc = []
    for sutun in zip(*adaylar):
        sonuc.append(sutun[0] if len(set(sutun)) == 1 else "?")
    return "".join(sonuc)

adaylar = ["##..#", "##.#.", ".##.#"]
print(zorunlu_hucreler(adaylar))  # ?#???
```

Bu kod bir CP çözücüsünün küçük ama önemli parçasını temsil eder: **kısıt yayılımı**. Gerçek sistemde `?` hücreleri henüz belirsizdir. Yayılım ilerlemiyorsa çözücü kontrollü bir seçim yapar: En az aday desene sahip satır ya da sütunu seçer, olası bir deseni dener ve çelişki oluşursa geri döner. Bu strateji “en kısıtlı değişken önce” sezgisidir ve arama ağacını küçültür.

| Kavram | Nonogram karşılığı |
|---|---|
| Değişken | Hücre değeri veya satır/sütun deseni |
| Alan (domain) | Hücrenin `{0,1}` değeri ya da aday desen kümesi |
| Kısıt | İpucundaki blok uzunlukları ve zorunlu boşluklar |
| Yayılım | Çelişen adayları silme, kesin hücreleri işaretleme |
| Geri izleme | Belirsiz durumda varsayım yapıp çelişirse dönme |

Sonuç olarak Nonogram çözücüsü yalnızca resim boyamaz; mantıksal bilgiyi satır ve sütunlar arasında dolaştırır. Bu nedenle problem, Sudoku, çizelgeleme ve kaynak atama gibi daha büyük kısıt tatmin problemlerine geçmek için hem görsel hem de son derece öğretici bir başlangıç noktasıdır.

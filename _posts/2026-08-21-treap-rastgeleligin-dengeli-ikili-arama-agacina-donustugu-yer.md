---
layout: post
title: "Treap: Rastgeleliğin Dengeli İkili Arama Ağacına Dönüştüğü Yer"
math: true
categories: 
  - Bilgi
tags: 
  - Veri Yapıları
  - Treap
  - Algoritmalar
---

Bir ikili arama ağacında (BST) hızlı arama, ekleme ve silme isteriz; ancak anahtarlar sıralı gelirse ağaç bir çubuğa dönüşebilir. Treap, bu talihsiz senaryoyu rastgelelik yardımıyla büyük ölçüde engeller. Adı, **tree** ve **heap** kelimelerinin birleşimidir: Anahtarlara göre BST, rastgele önceliklere göre ise heap davranışı sergiler. Böylece AVL veya Kırmızı-Siyah ağaçların katı dengeleme kurallarına alternatif, zarif bir yaklaşım sunar.
``

Her düğüm iki değer taşır: arama için kullanılan `key` ve genellikle rastgele üretilen `priority`. Treap iki değişmezi aynı anda korur:

1. **BST değişmezi:** Sol alt ağaçtaki anahtarlar küçük, sağ alt ağaçtakiler büyüktür.
2. **Min-heap değişmezi:** Bir düğümün önceliği, çocuklarının önceliklerinden küçüktür. (Max-heap seçmek de mümkündür; yalnızca karşılaştırmalar tersine döner.)

Örneğin `key=40, priority=12` olan bir düğümün solunda `key=20`, sağında `key=70` bulunabilir; fakat çocukların öncelikleri 12'den küçük olamaz. Bu ikili kural, ağacın şeklinin anahtarların eklenme sırasından çok rastgele önceliklerden etkilenmesini sağlar.

| Özellik | Sıradan BST | AVL Ağacı | Treap |
|---|---|---|---|
| Denge garantisi | Yok | Kesin | Olasılıksal |
| Beklenen yükseklik | Kötü durumda $O(n)$ | $O(\log n)$ | $O(\log n)$ |
| Uygulama yaklaşımı | Basit | Yükseklik takibi | Öncelik + rotasyon |
| Sıralı girişe direnç | Zayıf | Güçlü | Rastgelelik sayesinde güçlü |

Treap'e ekleme iki aşamalıdır. Önce düğüm, yalnızca `key` kullanılarak sıradan BST eklemesiyle yerleştirilir. Ardından yeni düğümün önceliği ebeveynin önceliğinden küçükse heap kuralı bozulmuştur. Düğüm, uygun yönde rotasyonlarla yukarı çıkarılır. Sol çocuk ebeveyninden daha öncelikliyse sağ rotasyon; sağ çocuk daha öncelikliyse sol rotasyon yapılır. Rotasyonlar anahtarların sıralı gezilmesini bozmaz; yalnızca yerel bağlantıları değiştirir.

```python
import random

class Node:
    def __init__(self, key):
        self.key = key
        self.priority = random.random()
        self.left = self.right = None

def rotate_right(root):
    pivot = root.left
    root.left = pivot.right
    pivot.right = root
    return pivot

def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
        if root.left.priority < root.priority:
            root = rotate_right(root)
    elif key > root.key:
        root.right = insert(root.right, key)
        if root.right.priority < root.priority:
            root = rotate_left(root)  # Simetrik sol rotasyon
    return root
```

Bu örnekte `insert`, önce BST konumunu bulur; dönüş çağrıları sırasında ise heap ihlalini kontrol ederek düğümü yukarı taşır. `rotate_left` fonksiyonu `rotate_right`ın ayna görüntüsüdür. Eşit anahtarlar burada yok sayılmıştır; gerçek uygulamada sayaç tutmak veya değeri güncellemek tercih edilebilir.

Silme işleminde hedef düğüm yaprak hâline gelene kadar aşağı indirilir. İki çocuk varsa, önceliği daha küçük olan çocuk seçilerek hedef üzerinde rotasyon uygulanır. Böylece heap düzeni korunur. Sonunda düğümün en fazla bir çocuğu kalır ve klasik BST silmesiyle kaldırılır.

Treap'in analizi rastgele öncelik varsayımına dayanır. $n$ düğüm için beklenen yükseklik $E[h]=O(\log n)$ olduğundan arama, ekleme ve silmenin beklenen maliyeti de $O(\log n)$ olur. Buna karşılık teorik olarak kötü bir öncelik dizisi $O(n)$ yüksekliğe yol açabilir. Güvenlik veya tekrarlanabilirlik gereken sistemlerde kaliteli bir rastgele üreteç ya da sabit tohum kullanımı bu yüzden önemlidir.

Treap; sıralı küme, sözlük, aralık sorgusu ve özellikle `split`/`merge` işlemlerinin doğal olduğu senaryolarda parlak bir seçimdir. Katı en kötü durum garantisinden çok sade kod ve pratikte güçlü denge arıyorsanız, rastgeleliğin bu küçük numarası oldukça etkileyicidir.

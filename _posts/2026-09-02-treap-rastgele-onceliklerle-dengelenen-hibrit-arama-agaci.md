---
layout: post
title: "Treap: Rastgele Önceliklerle Dengelenen Hibrit Arama Ağacı"
math: true
categories: 
  - Bilgi
tags: 
  - treap
  - veri yapıları
  - algoritmalar
toc: true
---

İkili arama ağaçları hızlıdır; ancak elemanlar sıralı geldiğinde zarif bir ağaç yerine tek yönlü bir zincire dönüşebilir. Treap, bu sorunu ikili arama ağacı ile heap yapısını birleştirerek çözer. Her düğüme anahtarın yanında rastgele bir öncelik verir ve böylece ağacın büyük olasılıkla dengeli kalmasını sağlar.

``

## Treap tam olarak nedir?

Treap adı, **tree** ve **heap** kelimelerinin birleşiminden gelir. Her düğüm iki önemli değer taşır:

- **Anahtar:** İkili arama ağacı düzenini belirler.
- **Öncelik:** Heap düzenini belirleyen, genellikle rastgele üretilen sayıdır.

Bir treap aynı anda şu iki koşulu sağlamalıdır:

1. Sol alt ağaçtaki anahtarlar düğümün anahtarından küçük, sağdakiler büyüktür.
2. Bir düğümün önceliği çocuklarının önceliklerinden üstündür.

Maksimum heap kullandığımızı varsayarsak bir düğüm için:

$$p(v) \geq p(v_{sol}) \quad \text{ve} \quad p(v) \geq p(v_{sağ})$$

Bu iki kural sayesinde anahtarlar arama yapmayı, öncelikler ise ağacın şeklini yönetir. Kısacası anahtarlar “Nereye yerleşmeliyim?”, öncelikler “Kim yukarıda oturmalı?” sorusunu cevaplar.

## Neden rastgelelik işe yarar?

Klasik bir ikili arama ağacına $1,2,3,4,5$ sırasıyla ekleme yapılırsa ağacın yüksekliği $n$ olabilir. Arama maliyeti de:

$$T(n)=O(n)$$

seviyesine çıkar. Treap'te öncelikler rastgele seçildiği için giriş sırası ağacın biçimini doğrudan belirleyemez. Beklenen yükseklik $O(\log n)$, temel işlemlerin beklenen maliyeti de şöyledir:

$$E[T(n)]=O(\log n)$$

Burada önemli bir düzeltme var: Treap, **en kötü durumda kesin olarak dengeli değildir**. Teorik olarak kötü öncelikler seçilip $O(n)$ yüksekliğinde bir yapı oluşabilir. Fakat iyi bir rastgele sayı üreticisiyle bunun olasılığı oldukça düşüktür. Yani garanti yerine güçlü bir olasılıksal denge sunar.

| Yapı | Denge yöntemi | Beklenen arama | En kötü arama |
|---|---|---:|---:|
| Sıradan BST | Yok | $O(\log n)$ | $O(n)$ |
| AVL ağacı | Katı yükseklik kuralları | $O(\log n)$ | $O(\log n)$ |
| Kırmızı-Siyah ağaç | Renk kuralları | $O(\log n)$ | $O(\log n)$ |
| Treap | Rastgele öncelikler | $O(\log n)$ | $O(n)$ |

## Ekleme ve rotasyonlar

Yeni düğüm önce anahtarına göre normal bir BST düğümü gibi eklenir. Ardından önceliği ebeveyninden büyükse heap kuralı bozulur. Bu durumda sağ veya sol rotasyon uygulanarak düğüm yukarı taşınır.

```python
import random

class Node:
    def __init__(self, key):
        self.key = key
        self.priority = random.random()
        self.left = None
        self.right = None

def rotate_right(root):
    new_root = root.left
    root.left = new_root.right
    new_root.right = root
    return new_root

def rotate_left(root):
    new_root = root.right
    root.right = new_root.left
    new_root.left = root
    return new_root

def insert(root, key):
    if root is None:
        return Node(key)

    if key < root.key:
        root.left = insert(root.left, key)
        if root.left.priority > root.priority:
            root = rotate_right(root)
    elif key > root.key:
        root.right = insert(root.right, key)
        if root.right.priority > root.priority:
            root = rotate_left(root)

    return root
```

Kod önce BST düzenine göre özyinelemeli ekleme yapar. Daha sonra öncelikleri karşılaştırır ve gerekirse rotasyon gerçekleştirir. Eşit anahtarlar bu örnekte yok sayılmıştır; gerçek uygulamalarda sayaç tutulabilir veya tekrar politikası belirlenebilir.

## Nerelerde kullanılır?

Treap; dinamik sıralı kümelerde, yarışma programlamada, bellek içi indekslerde ve aralık sorgularında kullanışlıdır. Özellikle **split** ve **merge** işlemlerinin doğal biçimde uygulanabilmesi büyük avantajdır. Bir treap anahtara göre iki ağaca ayrılabilir, uygun koşullardaki iki treap yeniden birleştirilebilir.

AVL gibi yapılara kıyasla kuralları daha az ve kodu daha sadedir. Bunun karşılığında kesin denge garantisinden vazgeçilir. Sonuç olarak treap, “Mükemmel düzen için karmaşık kurallar mı, basitlik için biraz şans mı?” sorusuna rastgele ama oldukça güvenilir bir cevap verir.

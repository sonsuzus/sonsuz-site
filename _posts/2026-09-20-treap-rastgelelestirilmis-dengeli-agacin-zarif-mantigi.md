---
layout: post
title: "Treap: Rastgeleleştirilmiş Dengeli Ağacın Zarif Mantığı"
math: true
categories: 
  - Bilgi
tags: 
  - treap
  - veri yapıları
  - algoritmalar
  - ağaçlar
  - python
  - rastgeleleştirme
toc: true
---

İkili arama ağaçları hızlıdır; tabii ağaç bir bambu dalına dönüşmediği sürece! Sıralı veriler sıradan bir ikili arama ağacına eklendiğinde yapı doğrusal bir liste gibi uzayabilir. Treap, bu sorunu katı dengeleme kuralları yerine rastgelelik kullanarak çözer. İsmi de iki yapının birleşiminden gelir: **tree** ve **heap**. Sonuç, şaşırtıcı derecede basit ama beklenen performansı oldukça güçlü bir veri yapısıdır.

``

## İki kural, tek ağaç

Treap içindeki her düğüm iki değere sahiptir:

- Arama işlemlerinde kullanılan bir **anahtar** (`key`)
- Rastgele üretilen bir **öncelik** (`priority`)

Yapı, anahtarlara göre ikili arama ağacı kuralını korur:

$$
\text{sol.key} < \text{düğüm.key} < \text{sağ.key}
$$

Aynı zamanda önceliklere göre bir maksimum yığın gibi davranır:

$$
\text{ebeveyn.priority} \geq \text{çocuk.priority}
$$

Yani anahtarlar “Nereye yerleşmeliyim?”, öncelikler ise “Ne kadar yukarı çıkmalıyım?” sorusunu cevaplar. Rastgele öncelikler sayesinde ekleme sırası kötü olsa bile ağacın sürekli tek tarafa yatması düşük olasılıklıdır.

| Yapı | Düzenleme ölçütü | Denge yaklaşımı | Beklenen arama |
|---|---|---|---|
| Sıradan BST | Anahtar | Yok | $O(n)$ olabilir |
| AVL ağacı | Anahtar ve yükseklik | Sıkı dengeleme | $O(\log n)$ |
| Kırmızı-siyah ağaç | Anahtar ve renk | Kurallı dengeleme | $O(\log n)$ |
| Treap | Anahtar ve rastgele öncelik | Olasılıksal | $O(\log n)$ |

## Rastgelelik neden denge getiriyor?

Anahtarlar sabitken birbirinden farklı öncelikler seçildiğini düşünelim. En yüksek öncelikli düğüm kök olur; solundaki anahtarlar sol alt ağacı, sağındakiler sağ alt ağacı oluşturur. Aynı mantık alt ağaçlarda tekrar edilir. Bu yapı, anahtarların rastgele sırada sıradan bir BST’ye eklenmesiyle aynı dağılıma sahiptir.

$n$ düğümlü bir treap’in beklenen yüksekliği:

$$
E[h] = O(\log n)
$$

Dolayısıyla arama, ekleme ve silme işlemleri beklenen durumda $O(\log n)$ sürer. Buradaki “beklenen” sözcüğü önemlidir: En kötü durumda hâlâ $O(n)$ mümkündür, ancak kaliteli ve bağımsız önceliklerle bunun gerçekleşme ihtimali oldukça düşüktür.

## Ekleme ve rotasyonlar

Yeni düğüm önce anahtarına göre normal BST eklemesiyle yerleştirilir. Ardından önceliği ebeveyninden büyükse rotasyonlarla yukarı taşınır. Rotasyon, anahtar sırasını bozmadan ağacın yerel şeklini değiştirir.

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

Bu kodda özyinelemeli ekleme BST düzenini kurar; dönüşte yapılan öncelik kontrolleri ise heap düzenini onarır. Eşit anahtarlar özellikle yok sayılmıştır. Gerçek bir uygulamada tekrar sayacı tutulabilir veya eşitlik için ayrı bir politika belirlenebilir.

## Treap ne zaman parlıyor?

Treap; sıralı küme, dinamik sıralama, aralık sorguları ve yarışma programcılığında oldukça kullanışlıdır. Alt ağaç boyutu tutulursa bir dizinin $k$’ıncı elemanı bulunabilir. Anahtara göre **split** ve iki treap’i birleştiren **merge** işlemleri de doğal biçimde uygulanır.

Bununla birlikte gerçek zamanlı sistemlerde kesin en kötü durum garantisi gerekiyorsa AVL veya kırmızı-siyah ağaç daha uygun olabilir. Treap’in güzelliği başka yerdedir: Karmaşık dengeleme durumlarını rastgele önceliklere devreder. Bazen algoritmik zarafet, her şeyi kontrol etmek yerine olasılığın işini yapmasına izin vermektir.

---
layout: post
title: "Splay Tree: Sık Erişilen Veriyi Köküne Taşıyan Akıllı Ağaç"
math: true
categories: 
  - Bilgi
tags: 
  - veri yapıları
  - splay tree
  - ikili arama ağacı
image: /img/splay-tree-sik-28.png
---

Splay Tree, klasik ikili arama ağacının (BST) heyecanlı ve biraz da inatçı kuzenidir: Bir düğüme eriştiğiniz anda onu ağacın köküne kadar taşımaya çalışır. Amaç, yakın geçmişte sık kullanılan verilere gelecekte daha hızlı ulaşmaktır. Dengeli ağaçlar gibi her an kusursuz görünmek zorunda değildir; bunun yerine kullanım alışkanlıklarınızı öğrenir.

``

Bir BST’de temel kural şudur: Her düğüm için sol alt ağaçtaki anahtarlar daha küçük, sağ alt ağaçtaki anahtarlar daha büyüktür. Arama, ekleme ve silme işlemlerinin maliyeti ağacın yüksekliğine bağlıdır. Ağaç kötü biçimde tek tarafa yatarsa yükseklik $h=n$ olabilir ve işlemler $O(n)$ sürer. Splay Tree bu kötü görünümü tek tek işlemlerde garantiyle engellemez; ancak uzun bir işlem serisinde toplam maliyeti kontrol eder.

Sihirli hareketin adı **splaying**’dir. Bir düğüm bulunduğunda ya da aramada ulaşılan son düğüm belirlendiğinde, düğüm köke gelene kadar rotasyon uygulanır. Bu rotasyonlar BST sıralama kuralını bozmaz. Üç temel durum vardır:

| Durum | Yapısal koşul | Uygulanan işlem |
|---|---|---|
| Zig | Düğümün ebeveyni köktür | Tek sağ veya sol rotasyon |
| Zig-Zig | Düğüm ve ebeveyni aynı yöndedir | Aynı yönde iki rotasyon |
| Zig-Zag | Düğüm ve ebeveyni zıt yöndedir | Önce düğüm-ebeveyn, sonra düğüm-büyük ebeveyn rotasyonu |

Örneğin `30` düğümüne eriştiğinizi düşünün. Eğer `30`, `50`nin solunda; `50` de `100`ün solundaysa bu bir **Zig-Zig** durumudur. Önce `100` ile `50`, ardından `50` ile `30` arasında sağ rotasyon yapılır. Böylece `30` yukarı çıkar. Aynı anahtara tekrar erişirseniz artık doğrudan köktedir: maliyet yaklaşık $O(1)$ olur.

Splay Tree’nin teorik gücü, **amortize analiz** ile açıklanır. Tek bir arama bazen uzun sürebilir; hatta ağacın en altındaki düğüm köke taşınırken $O(n)$ iş yapılabilir. Buna rağmen $m$ işlem için toplam maliyet şu sınırla ifade edilir:

$$T(m)=O(m\log n)$$

Dolayısıyla işlem başına amortize maliyet $O(\log n)$ olur. Buradaki fikir, pahalı bir erişimin ağacı gelecekteki erişimler için daha uygun hâle getirmesidir. Buna erişim yerelliği denir: Yakın zamanda kullanılan verilerin yeniden kullanılma ihtimali genellikle yüksektir.

Aşağıdaki Python örneği, arama sonrası bulunan düğümü köke taşıyan sade bir iskelet sunar. Gerçek bir sınıfta silme, ebeveyn bağları ve hata durumları da eklenmelidir.

```python
class Node:
    def __init__(self, key):
        self.key = key
        self.left = self.right = self.parent = None

def rotate_right(x):
    y = x.left
    x.left = y.right
    if y.right:
        y.right.parent = x
    y.parent = x.parent
    if x.parent:
        if x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
    y.right = x
    x.parent = y
    return y

def splay(node):
    while node.parent:
        parent = node.parent
        grand = parent.parent
        if not grand:                 # Zig
            rotate_right(parent) if node == parent.left else None
        elif node == parent.left and parent == grand.left:  # Zig-Zig
            rotate_right(grand)
            rotate_right(parent)
        # Zig-Zag ve sağ yönlü simetrik durumlar burada eklenir.
    return node
```

Bu örnekte `rotate_right`, sol çocuğu yukarı taşıyarak yerel yapıyı dönüştürür. `splay` fonksiyonu ise düğümün ebeveyn ve büyük ebeveyn ilişkisine bakarak uygun rotasyon dizisini seçer. Üretim kodunda hem sol hem sağ rotasyonun simetrik tüm durumları eksiksiz uygulanmalıdır.

| Yapı | En kötü tek işlem | Amortize işlem | Güçlü yanı |
|---|---:|---:|---|
| Sıradan BST | $O(n)$ | $O(n)$ | Basit yapı |
| AVL Tree | $O(\log n)$ | $O(\log n)$ | Sıkı denge garantisi |
| Red-Black Tree | $O(\log n)$ | $O(\log n)$ | Standart kütüphanelerde yaygın |
| Splay Tree | $O(n)$ | $O(\log n)$ | Sık erişilen anahtarlarda çok hızlı |

Özetle Splay Tree, en kötü durum garantisinden biraz feragat ederek davranışa uyum sağlar. Önbellek benzeri erişimler, yakın zamanda kullanılan oturumlar veya tekrar eden sorgular için etkileyici bir seçimdir. Ağacınız biraz dağınık görünse bile endişelenmeyin: Splay Tree, her erişimde kendi masasını yeniden toplar.

![splay-tree-sik-28](/img/splay-tree-sik-28.svg)


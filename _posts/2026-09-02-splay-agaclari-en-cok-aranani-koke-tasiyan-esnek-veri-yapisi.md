---
layout: post
title: "Splay Ağaçları: En Çok Arananı Köke Taşıyan Esnek Veri Yapısı"
math: true
categories: 
  - Bilgi
tags: 
  - splay-tree
  - veri-yapıları
  - algoritmalar
toc: true
---

Bazı anahtarlar diğerlerinden daha sık aranıyorsa, neden hepsine aynı mesafeyi sunalım? Splay ağacı, erişilen düğümü rotasyonlarla köke taşıyarak bu soruya oldukça pratik bir cevap verir. Katı denge kurallarıyla uğraşmaz; bunun yerine kullanım alışkanlıklarını öğreniyormuş gibi davranır ve popüler düğümleri el altında tutar.

``

## Splay Ağacı Nedir?

Splay ağacı, ikili arama ağacı kurallarını koruyan fakat her erişimden sonra **splay** adı verilen yeniden düzenleme işlemini uygulayan kendi kendini ayarlayan bir veri yapısıdır. Bir düğüm arandığında, eklendiğinde veya silme sırasında kullanıldığında çeşitli rotasyonlarla köke çıkarılır.

Normal bir ikili arama ağacında sol alt ağaçtaki anahtarlar düğümden küçük, sağ alt ağaçtakiler büyüktür. Rotasyonlar bu sıralamayı bozmaz; yalnızca düğümlerin yüksekliklerini değiştirir.

| Özellik | Splay Ağacı | AVL Ağacı | Kırmızı-Siyah Ağaç |
|---|---|---|---|
| Açık denge bilgisi | Yok | Yükseklik | Renk biti |
| Tek işlem için en kötü durum | $O(n)$ | $O(\log n)$ | $O(\log n)$ |
| Amortize işlem maliyeti | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ |
| Sık erişilene uyum | Çok iyi | Özel avantaj yok | Özel avantaj yok |
| Uygulama yaklaşımı | Rotasyon odaklı | Daha katı | Orta karmaşıklıkta |

## Rotasyon Senaryoları

Bir düğümün köke yolculuğu üç temel hareketle gerçekleşir:

- **Zig:** Düğümün ebeveyni köktür. Tek rotasyon yeterlidir.
- **Zig-Zig:** Düğüm ve ebeveyni aynı yöndedir; örneğin ikisi de sol çocuktur. Aynı yönde iki rotasyon yapılır.
- **Zig-Zag:** Düğüm ve ebeveyni farklı yönlerdedir. Önce ebeveyn, ardından büyük ebeveyn çevresinde ters yönlü rotasyon uygulanır.

Zig-Zig hareketinin düğümü yalnızca yukarı çekmekten fazlasını yaptığına dikkat etmek gerekir: Erişim yolundaki uzun zinciri de kısaltır. Bu nedenle gelecek işlemler dolaylı biçimde hızlanır.

## Amortize Maliyet Nasıl Çalışır?

Tek bir arama, tamamen eğilmiş bir ağaçta $O(n)$ sürebilir. Ancak amortize analiz, tek işleme değil uzun bir işlem dizisine bakar. $m$ adet işlem için toplam maliyet genel olarak

$$
O(m\log n)
$$

ile sınırlanır. Böylece işlem başına amortize maliyet $O(\log n)$ olur. Buradaki fikir, pahalı bir erişimin ağacı sonraki erişimler için daha kullanışlı hâle getirmesidir. Başka bir deyişle ağaç, bugün ödediği yüksek maliyetle yarının yolunu kısaltır.

## Python ile Temel Uygulama

Aşağıdaki kod, sağ rotasyonu ve bir düğümü köke taşıyan özyinelemeli splay işlemini gösterir:

```python
class Node:
    def __init__(self, key):
        self.key = key
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


def splay(root, key):
    if root is None or root.key == key:
        return root

    if key < root.key:
        if root.left is None:
            return root

        if key < root.left.key:  # Zig-Zig
            root.left.left = splay(root.left.left, key)
            root = rotate_right(root)
        elif key > root.left.key:  # Zig-Zag
            root.left.right = splay(root.left.right, key)
            if root.left.right:
                root.left = rotate_left(root.left)

        return rotate_right(root) if root.left else root

    if root.right is None:
        return root

    if key > root.right.key:  # Zig-Zig
        root.right.right = splay(root.right.right, key)
        root = rotate_left(root)
    elif key < root.right.key:  # Zig-Zag
        root.right.left = splay(root.right.left, key)
        if root.right.left:
            root.right = rotate_right(root.right)

    return rotate_left(root) if root.right else root
```

Aranan anahtar bulunamazsa kod, arama yolunda ulaşılan son uygun düğümü köke yaklaştırır. Bu davranış, yakın anahtarların tekrar aranacağı senaryolarda da avantaj sağlayabilir.

## Ne Zaman Kullanılmalı?

Splay ağaçları önbellekler, metin editörleri, sık tekrarlanan sorgular ve zamansal yerellik gösteren iş yükleri için uygundur. Buna karşılık her işlemin kesin olarak $O(\log n)$ sürmesi gereken gerçek zamanlı sistemlerde AVL veya Kırmızı-Siyah ağaç daha güvenli olabilir. Splay ağacının gücü kusursuz dengede değil, erişim düzenine uyum sağlayan esnekliğindedir.

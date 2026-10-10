---
layout: post
title: "İkili Ağaçlarda Dolaşma: Ön Sıra, Orta Sıra ve Son Sıra"
math: true
categories: 
  - Bilgi
tags: 
  - ağaç yapıları
  - ikili ağaç
  - algoritma
  - veri yapıları
  - python
  - özyineleme
toc: true
image: /img/ikili-agaclarda-dolasma-65.png
---

![ikili-agaclarda-dolasma-65](/img/ikili-agaclarda-dolasma-65.svg)


Ağaçlar; dosya sistemlerinden arama motorlarına, derleyicilerden oyunlardaki karar mekanizmalarına kadar birçok alanda kullanılan hiyerarşik veri yapılarıdır. Ancak düğümleri dallara yerleştirmek tek başına yeterli değildir: Bilgiye ulaşabilmek için ağacı sistemli biçimde dolaşmamız gerekir. İkili ağaçlarda en yaygın derinlik öncelikli yöntemler ön sıra, orta sıra ve son sıra dolaşmadır.

``

## İkili ağaç nedir?

İkili ağaçta her düğümün en fazla iki çocuğu bulunur: **sol çocuk** ve **sağ çocuk**. En üstteki düğüme kök, çocuğu olmayan düğümlere ise yaprak denir.

Örnek olarak aşağıdaki ağacı düşünelim:

```text
        8
       / \
      3   10
     / \    \
    1   6    14
```

Dolaşma yöntemleri arasındaki temel fark, kök düğümün ne zaman ziyaret edildiğidir. Buradaki “ziyaret”, değeri yazdırmak, toplamak, karşılaştırmak veya başka bir işlem gerçekleştirmek anlamına gelebilir.

| Yöntem | Ziyaret sırası | Örnek sonuç | Tipik kullanım |
|---|---|---|---|
| Ön sıra | Kök → Sol → Sağ | 8, 3, 1, 6, 10, 14 | Ağacı kopyalama, serileştirme |
| Orta sıra | Sol → Kök → Sağ | 1, 3, 6, 8, 10, 14 | Sıralı değer üretme |
| Son sıra | Sol → Sağ → Kök | 1, 6, 3, 14, 10, 8 | Silme, bağımlılık çözme |

## Ön sıra dolaşma

Ön sıra dolaşmada kök, çocuklarından önce işlenir. Bu nedenle hiyerarşik yapıyı dışarı aktarmak veya ağacın bir kopyasını oluşturmak için kullanışlıdır. Kökün önce bilinmesi, alt dalların hangi üst düğüme bağlanacağını belirlemeyi kolaylaştırır.

```python
def preorder(node):
    if node is None:
        return

    print(node.value)       # Önce kökü işle
    preorder(node.left)     # Ardından sol alt ağacı dolaş
    preorder(node.right)    # Son olarak sağ alt ağacı dolaş
```

Bir klasör yapısında önce klasör adını, ardından içindeki dosya ve alt klasörleri göstermek bu yaklaşıma benzer.

## Orta sıra dolaşma

Orta sırada kök, sol ve sağ alt ağaçların arasında ziyaret edilir. Bu yöntem özellikle **ikili arama ağaçlarında** önemlidir. İkili arama ağacında sol taraftaki değerler kökten küçük, sağ taraftakiler büyüktür. Dolayısıyla orta sıra dolaşma değerleri küçükten büyüğe üretir.

```python
def inorder(node):
    if node is None:
        return

    inorder(node.left)      # Küçük değerleri gez
    print(node.value)       # Kökü işle
    inorder(node.right)     # Büyük değerleri gez
```

Bu özellik, ayrıca bir sıralama algoritması çalıştırmadan düzenli çıktı alınmasını sağlar. Fakat aynı sonuç sıradan bir ikili ağaç için garanti edilmez; ağacın ikili arama ağacı kurallarına uyması gerekir.

## Son sıra dolaşma

Son sıra dolaşmada kök en son işlenir. Başka bir deyişle, ebeveyn üzerinde işlem yapılmadan önce bütün çocuklar tamamlanır.

```python
def postorder(node):
    if node is None:
        return

    postorder(node.left)    # Sol bağımlılıkları tamamla
    postorder(node.right)   # Sağ bağımlılıkları tamamla
    print(node.value)       # En son kökü işle
```

Bu yöntem ağacı bellekten güvenli biçimde silmek için idealdir. Önce çocuk düğümler kaldırılır, sonra ebeveyn silinir. İfade ağaçlarında hesaplama yapmak da benzer mantıktadır: Operatör uygulanmadan önce iki operandın değeri hesaplanır.

## Zaman ve alan karmaşıklığı

Üç yöntem de her düğümü tam bir kez ziyaret eder. Düğüm sayısı $n$ ise çalışma süresi:

$$T(n)=T(n_L)+T(n_R)+O(1)=O(n)$$

Özyinelemeli çağrıların bellek maliyeti ağacın yüksekliğine, yani $h$ değerine bağlı olarak $O(h)$ olur. Dengeli ağaçta $h \approx \log_2 n$ iken tek tarafa yatmış bir ağaçta $h=n$ olabilir.

Kısacası seçim, “kökü ne zaman işlemeliyim?” sorusuna bağlıdır: Yapıyı yukarıdan aşağı kurmak için ön sıra, sıralı veri almak için orta sıra, çocukları ebeveynden önce tamamlamak için son sıra tercih edilir.

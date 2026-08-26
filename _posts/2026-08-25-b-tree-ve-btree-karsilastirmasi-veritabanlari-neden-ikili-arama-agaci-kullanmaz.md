---
layout: post
title: "B-Tree ve B+Tree Karşılaştırması: Veritabanları Neden İkili Arama Ağacı Kullanmaz?"
math: true
categories: 
  - Bilgi
tags: 
  - veritabanı
  - veri yapıları
  - b-tree
  - b+tree
  - indeksleme
toc: true
---

Bir veritabanında milyonlarca kaydı bulmak, bellekte küçük bir dizide arama yapmaktan oldukça farklıdır. Klasik ikili arama ağaçları (BST), teoride zarif görünür: her düğümün en fazla iki çocuğu vardır ve dengeli bir yapıda arama maliyeti $O(\log_2 N)$ olur. Ancak disk ve SSD üzerinde çalışan veritabanları için asıl pahalı işlem karşılaştırma değil, sayfa okuma yani I/O işlemidir. İşte B-Tree ve B+Tree bu maliyeti dramatik biçimde düşürmek için sahneye çıkar.
``

## Sorun: İkili Ağaç Fazla Uzun

Dengeli bir BST’de her düğüm iki dallıdır. Bir milyar kayıt için ağacın yaklaşık yüksekliği şöyledir:

$$h \approx \log_2(10^9) \approx 30$$

Her düğüm disk üzerinde ayrı bir sayfada bulunuyorsa, tek bir sorgu yaklaşık 30 sayfa erişimi gerektirebilir. Disk önbelleği bunu bazen azaltır; fakat yüksek eşzamanlılık ve büyük veri altında bu hâlâ pahalıdır.

B-Tree ailesinin zekice fikri basittir: Bir düğüme yalnızca bir anahtar koymak yerine, disk sayfasına sığacak kadar çok anahtar koy. Dallanma derecesi $b$ ise yükseklik yaklaşık olarak $\log_b N$ olur. Örneğin bir düğüm 200 çocuk gösterebiliyorsa:

$$h \approx \log_{200}(10^9) \approx 4$$

Yani 30 yerine yaklaşık 4 sayfa erişimi! Veritabanı motorlarının yüzü tam burada güler.

## B-Tree: Anahtarlar Her Seviyede Yaşar

B-Tree’de bir düğüm birden fazla sıralı anahtar ve çocuk işaretçisi tutar. Önemli nokta şudur: Asıl kayıt ya da kayıt işaretçisi hem iç düğümlerde hem de yapraklarda bulunabilir. Arama, kökten başlayarak uygun anahtar aralığını seçer; aranan değer bir iç düğümde bulunursa işlem orada bitebilir.

Bir düğüm kapasitesi $m$ çocuk ise, dengeli B-Tree’de düğümler genellikle belirli bir doluluk oranını korur. Ekleme sırasında taşan düğüm bölünür; silmede aşırı boşalan düğüm komşusundan ödünç alır veya birleşir. Böylece ağaç dengeli kalır ve karmaşıklıklar korunur:

| İşlem | B-Tree maliyeti | I/O açısından anlamı |
|---|---:|---|
| Nokta arama | $O(\log_m N)$ | Az sayıda sayfa okuma |
| Ekleme | $O(\log_m N)$ | Bölünme nadiren ek yazma doğurur |
| Silme | $O(\log_m N)$ | Yeniden dengeleme gerekebilir |
| Aralık taraması | İyi | Yapraklar arasında ilerleme maliyetli olabilir |

## B+Tree: Yapraklar Veri, İç Düğümler Rehber

B+Tree, B-Tree’nin veritabanlarında daha popüler kuzenidir. İç düğümler yalnızca anahtar ve çocuk işaretçileri taşır. Asıl kayıtlar veya kayıt konumları **yalnızca yaprak düğümlerdedir**. Ayrıca yapraklar genellikle bağlı liste gibi birbirine işaret eder.

Bu tasarımın iki büyük ödülü vardır. İlk olarak iç düğümlerde kayıt verisi taşınmadığı için daha fazla anahtar yer alır; yani dallanma katsayısı büyür ve ağaç daha da kısalır. İkinci olarak aralık sorguları çok hızlıdır: İlk anahtar bulunur, ardından bağlı yapraklar sırayla taranır.

| Özellik | B-Tree | B+Tree |
|---|---|---|
| Veri konumu | İç ve yaprak düğümler | Yalnızca yaprak düğümler |
| İç düğüm kapasitesi | Daha düşük | Daha yüksek |
| Nokta arama | İç düğümde bitebilir | Her zaman yaprağa iner |
| Aralık sorgusu | Uygun | Genellikle üstün |
| Yaprak bağlantısı | Zorunlu değil | Tipik olarak vardır |

## Mini Bir B+Tree Araması

Aşağıdaki sözde kod, B+Tree’de bir anahtarın yaprağa kadar nasıl takip edildiğini gösterir. `childIndex`, anahtarın hangi aralığa düştüğünü ikili arama ile belirler.

```python
def find_leaf(node, key):
    # İç düğümler yalnızca doğru çocuğu seçmek için kullanılır.
    while not node.is_leaf:
        index = binary_search_child_index(node.keys, key)
        node = node.children[index]

    # Gerçek kayıt işaretçisi yaprakta aranır.
    index = binary_search(node.keys, key)
    return node.values[index] if index is not None else None
```

Bu yaklaşım, özellikle `WHERE id = ...` sorgularında etkili bir nokta araması sağlar. `WHERE created_at BETWEEN ...` gibi aralık sorgularında ise ilk yaprak bulunduğunda yaprak bağlantıları boyunca yürünür; ağacın köküne tekrar dönmeye gerek kalmaz.

Kısacası klasik BST, RAM odaklı düşünür ve ikili dallanması nedeniyle disk sayfalarını verimsiz kullanır. B-Tree disk dostu, dengeli ve geniştir; B+Tree ise buna sıralı yaprak taramasını ekler. Bu nedenle MySQL/InnoDB, PostgreSQL ve pek çok depolama motorunda indeks denince akla çoğunlukla B+Tree gelir.

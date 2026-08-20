---
layout: post
title: "Persistent Veri Yapılarıyla Zaman Yolculuğu: Immutable Ağaç Tasarımı"
math: true
categories: 
  - Bilgi
tags: 
  - fonksiyonel programlama
  - persistent veri yapıları
  - immutable
  - ağaçlar
  - algoritmalar
toc: true
---

Bir uygulamanın geçmişini saklamak çoğu zaman ya pahalı kopyalama ya da karmaşık geri alma kayıtları anlamına gelir. Persistent veri yapıları bu ikilemi değiştirir: Bir ağacı güncellediğinizde eski sürüm bozulmaz, bunun yerine yeni bir sürüm üretilir. Böylece sürüm 3'teki bir değere bakmak için günlük taramak gerekmez; doğrudan o sürümün köküne ulaşırsınız. Bu yaklaşım, fonksiyonel programlamanın değişmezlik fikrini veri yapılarının kalbine taşır.
``
## Persistent olmak ne demektir?

Bir veri yapısının **persistent** olması, güncelleme işlemlerinden sonra eski hâllerinin kullanılabilir kalmasıdır. Buradaki önemli ayrım, her sürümün ağacın tamamını kopyalaması değildir. Akıllı tasarımın anahtarı **yapısal paylaşım**dır (*structural sharing*).

Örneğin dengeli bir ikili arama ağacında `42` anahtarını eklerseniz, yalnızca kökten `42`'ye giden yol üzerindeki düğümler yeniden oluşturulur. Bu yolun dışındaki alt ağaçlar aynen paylaşılır. Ağacın yüksekliği $h$ ise, yeni sürüm üretmenin maliyeti yaklaşık olarak:

$$T_{update}=O(h)$$

Dengeli bir ağaçta $h=O(\log n)$ olduğundan ekleme, silme ve arama beklenen ya da garantili biçimde logaritmik kalabilir. Önceki sürüme erişim ise bir `roots[version]` dizisi üzerinden sabit zamanda yapılır:

$$T_{version\ access}=O(1)$$

| Özellik | Mutable ağaç | Persistent immutable ağaç |
|---|---:|---:|
| Güncelleme | Düğümleri yerinde değiştirir | Yeni kök/sürüm üretir |
| Eski hâle erişim | Ek mekanizma gerekir | Doğal olarak desteklenir |
| Bellek | Tek anlık durum için düşük | Yol kopyalama kadar ek maliyet |
| Eşzamanlı okuma | Kilit ihtiyacı doğabilir | Daha güvenlidir |
| Hata ayıklama | Geçmişi yeniden kurmak zor | Sürümler doğrudan incelenir |

## Yol kopyalama: Kopya makinesi değil, cerrahi işlem

Yeni bir düğüm oluştururken çocuk referanslarını paylaşırız. Aşağıdaki Python örneği, immutable bir ikili arama ağacına ekleme yapar. `Node` sınıfının `frozen=True` olması, oluşturulduktan sonra alanların değiştirilemeyeceğini anlatır.

```python
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Node:
    key: int
    left: Optional['Node'] = None
    right: Optional['Node'] = None

def insert(root: Optional[Node], key: int) -> Node:
    if root is None:
        return Node(key)

    if key < root.key:
        return Node(root.key, insert(root.left, key), root.right)
    if key > root.key:
        return Node(root.key, root.left, insert(root.right, key))

    return root  # Anahtar zaten varsa aynı sürüm paylaşılır.

versions = [None]
versions.append(insert(versions[0], 10))
versions.append(insert(versions[1], 5))
versions.append(insert(versions[2], 20))
```

Burada `versions[1]` yalnızca `10` düğümünü, `versions[3]` ise `5-10-20` ağacını temsil eder. En güzel detay şudur: Son sürümdeki `20` eklenirken sol taraftaki `5` düğümü yeniden üretilmez; referansı paylaşılır. Yani geçmiş, gereksiz fotokopilerden değil, ortak dallardan oluşur.

## Sürüm yönetimi ve pratik kullanım

Bir sürümü indeksle seçmek kolaydır; fakat hangi sürümden yeni dal üretileceğini de siz belirlersiniz. Örneğin `versions[1]` üzerinden tekrar ekleme yaparak lineer bir geçmiş yerine sürüm ağacı oluşturabilirsiniz. Bu davranış Git dallarına oldukça benzer: Eski commit değişmez, yeni commit eski yapının büyük bölümünü paylaşır.

| Kullanım alanı | Persistent yapının kazancı |
|---|---|
| Undo/redo editörü | Her düzenleme doğal bir sürümdür |
| Yarışma programlama | Geçmiş sorgulara hızlı erişim sağlar |
| Eşzamanlı sistemler | Okuyucular tutarlı, değişmez snapshot görür |
| Konfigürasyon yönetimi | Güvenli karşılaştırma ve geri dönüş sunar |

Dengeli ağaçlarda silme ve rotasyonlar biraz daha dikkat ister: Rotasyon sırasında değişen düğümler de yeniden yaratılmalıdır. Buna rağmen ilke değişmez: **asla mevcut düğümü değiştirme, yalnızca değişen yolu yeniden kur**. Böylece veri yapınız yalnızca değer saklamaz; zaman içindeki güvenilir hikâyesini de saklar.

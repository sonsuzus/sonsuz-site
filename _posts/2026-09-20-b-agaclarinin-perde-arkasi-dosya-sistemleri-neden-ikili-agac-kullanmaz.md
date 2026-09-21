---
layout: post
title: "B-Ağaçlarının Perde Arkası: Dosya Sistemleri Neden İkili Ağaç Kullanmaz?"
math: true
categories: 
  - Bilgi
tags: 
  - b-ağacı
  - dosya-sistemleri
  - veri-yapıları
  - algoritmalar
  - veritabanı
  - disk
toc: true
image: /img/b-agaclarinin-perde-81.png
---

Bir dosyayı açtığınızda işletim sistemi milyonlarca kayıt arasından doğru disk bloğunu şaşırtıcı bir hızla bulur. Bu numaranın arkasında çoğu zaman ikili arama ağacı değil, tek düğümüne adeta küçük bir mahalle sığdırabilen B-ağacı veya onun akrabaları vardır. Çünkü disk dünyasında pahalı olan karşılaştırma yapmak değil, verinin bulunduğu bloğa fiziksel ya da mantıksal olarak ulaşmaktır.


![b-agaclarinin-perde-81](/img/b-agaclarinin-perde-81.svg)

``

## Asıl mesele: Disk erişimi

Dengeli bir ikili arama ağacında her düğüm en fazla iki çocuğa sahiptir. Arama karmaşıklığı teoride $O(\log_2 N)$ olduğu için bu gayet iyi görünür. Ancak her düğüm farklı bir disk bloğundaysa, ağacın her seviyesi yeni bir I/O işlemi doğurabilir.

B-ağacı ise bir düğümde çok sayıda sıralı anahtar ve çocuk işaretçisi saklar. Düğüm boyutu genellikle disk veya dosya sistemi blok boyutuna göre seçilir. Böylece tek blok okumasıyla onlarca, hatta yüzlerce olası dal elenir.

Bir düğümün en fazla $m$ çocuğu varsa yaklaşık yükseklik:

$$h \approx \log_m N$$

Bir milyon kayıt için ikili ağacın yüksekliği yaklaşık $\log_2 10^6 \approx 20$ seviyedir. Dallanma katsayısı 200 olan bir B-ağacıysa yaklaşık $\log_{200} 10^6 \approx 3$ seviyeye ihtiyaç duyar. Yani yaklaşık 20 blok erişimi yerine 3 blok erişimi! İşlemci birkaç karşılaştırmayı göz açıp kapayıncaya kadar yaparken depolama erişimi yanında kahve molasına çıkmış gibi kalır.

| Özellik | Dengeli ikili ağaç | B-ağacı |
|---|---:|---:|
| Düğüm başına çocuk | En fazla 2 | Genellikle onlarca veya yüzlerce |
| Ağaç yüksekliği | Daha fazla | Çok daha az |
| Disk bloğu kullanımı | Verimsiz olabilir | Blok boyutuna uyarlanır |
| Güncelleme dengesi | Rotasyonlarla | Bölme ve birleştirmelerle |
| Tipik kullanım | Bellek içi yapılar | Dosya sistemleri ve veritabanları |

## B-ağacı nasıl dengede kalır?

B-ağacında bütün yapraklar aynı seviyededir. Kök dışındaki düğümler belirli bir minimum doluluk oranını korur. Bir düğüm kapasitesini aşarsa ortadaki anahtar üst düğüme taşınır ve düğüm ikiye bölünür. Silme sırasında fazla boşalan düğümler komşularından anahtar ödünç alabilir veya birleşebilir.

Aşağıdaki sadeleştirilmiş Python kodu, dolu bir çocuğun nasıl bölündüğünü gösterir:

```python
def split_child(parent, index, degree):
    child = parent.children[index]
    sibling = Node(leaf=child.leaf)

    middle_key = child.keys[degree - 1]
    sibling.keys = child.keys[degree:]
    child.keys = child.keys[:degree - 1]

    if not child.leaf:
        sibling.children = child.children[degree:]
        child.children = child.children[:degree]

    parent.keys.insert(index, middle_key)
    parent.children.insert(index + 1, sibling)
```

Buradaki `degree`, düğümlerin taşıyabileceği anahtar sayısını belirler. İşlem, taşan düğümün ortasındaki anahtarı ebeveyne yükseltir; küçük anahtarlar solda, büyükler sağda kalır. Bu sayede arama düzeni bozulmadan ağaç dengeli büyür.

## Dosya sistemlerinde hangi akrabaları görülür?

Pratikte sıkça B+ ağacı kullanılır. B+ ağacında gerçek kayıtlar veya kayıt adresleri yapraklarda tutulur; iç düğümler yalnızca yönlendirme anahtarları içerir. Yaprakların birbirine bağlanması, sıralı dolaşmayı ve aralık sorgularını hızlandırır.

| Yapı | Verinin konumu | Güçlü tarafı |
|---|---|---|
| B-ağacı | İç ve yaprak düğümler | Genel amaçlı arama |
| B+ ağacı | Çoğunlukla yapraklar | Aralık taraması ve sıralı erişim |
| İkili ağaç | Her düğüm | Bellekte basit ve hızlı kullanım |

NTFS, HFS+, XFS ve Btrfs gibi sistemler farklı B-ağacı türevlerinden yararlanır. Bunlarla dosya adları, dizin girdileri, uzantılar ve boş alan bilgileri indekslenebilir. Elbette ikili ağaç kullanmak yasak değildir; yalnızca disk bloklarıyla kötü dans eder. B-ağaçları ise depolamanın ritmini bilir: daha geniş düğümler, daha kısa yol ve çok daha az I/O.

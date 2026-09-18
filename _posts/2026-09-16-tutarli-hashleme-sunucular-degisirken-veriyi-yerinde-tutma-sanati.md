---
layout: post
title: "Tutarlı Hashleme: Sunucular Değişirken Veriyi Yerinde Tutma Sanatı"
math: true
categories: 
  - Bilgi
tags: 
  - tutarlı hashleme
  - dağıtık sistemler
  - önbellek
  - yük dengeleme
  - algoritma
toc: true
image: /img/tutarli-hashleme-sunucular-46.png
---

![tutarli-hashleme-sunucular-46](/img/tutarli-hashleme-sunucular-46.svg)


Dağıtık bir sistemde yeni sunucu eklemek güzel haberdir; ta ki milyonlarca anahtarın başka sunuculara taşınması gerekene kadar! Tutarlı hashleme, yani *consistent hashing*, sunucu sayısı değiştiğinde verilerin yalnızca küçük bir bölümünü yeniden eşleyerek bu karmaşayı yönetir. Özellikle dağıtık önbellekler, veritabanları ve içerik dağıtım ağlarında sistemin büyümesini daha az sancılı hâle getirir.
``
## Klasik hashleme neden sorun çıkarır?

Basit bir dağıtım yaklaşımında bir anahtarın gideceği sunucu şöyle belirlenebilir:

$$
\text{sunucu}(k) = h(k) \bmod N
$$

Burada $h(k)$ anahtarın hash değeri, $N$ ise sunucu sayısıdır. Üç sunucumuz varken `kullanici:42` ikinci sunucuya düşebilir. Dördüncü sunucu eklendiğinde mod değeri değişir ve aynı anahtar bambaşka bir sunucuya gönderilebilir.

Sorun yalnızca tek bir anahtarla sınırlı değildir. $N$ değiştiğinde anahtarların büyük çoğunluğu yeniden eşlenir. Bir önbellek sisteminde bu durum toplu cache miss, veritabanında ise pahalı veri taşıma operasyonları anlamına gelir.

| Özellik | Mod tabanlı hashleme | Tutarlı hashleme |
|---|---|---|
| Sunucu ekleme etkisi | Anahtarların çoğu değişir | Küçük bir bölüm değişir |
| Sunucu çıkarma etkisi | Genel yeniden eşleme oluşur | Komşu aralık etkilenir |
| Uygulama kolaylığı | Çok kolay | Orta düzey |
| Yük dengesi | Genellikle düzgün | Sanal düğüm gerektirebilir |

## Hash halkası mantığı

Tutarlı hashleme, olası hash değerlerini bir halka üzerinde düşünür. Örneğin hash fonksiyonumuz $0$ ile $2^{32}-1$ arasında değer üretiyorsa, son değer tekrar sıfıra bağlanır. Hem sunucular hem de veri anahtarları aynı halkaya hashlenir.

Bir anahtarın sahibi, halka üzerinde saat yönünde ilerlerken karşılaşılan ilk sunucudur. Eğer arama halkanın sonunu aşarsa başa dönülür. Böylece bir sunucu eklendiğinde yalnızca kendisinden önceki sunucu ile arasındaki anahtarları devralır. Bir sunucu çıkarıldığında ise anahtarları sıradaki sunucuya geçer.

$K$ anahtar ve $N$ dengeli sunucu için yeni bir sunucu eklenince taşınması beklenen veri yaklaşık olarak şöyledir:

$$
\text{taşınan oran} \approx \frac{1}{N+1}
$$

Yani yöntem veriyi hiç taşımamak değil, taşınan miktarı sınırlamak üzerine kuruludur.

## Küçük bir Python uygulaması

Aşağıdaki sınıf, sunucuları sıralı bir hash halkasında tutar ve anahtarın sorumlusunu ikili aramayla bulur:

```python
import bisect
import hashlib

class HashRing:
    def __init__(self):
        self.positions = []
        self.nodes = {}

    def hash(self, value):
        digest = hashlib.sha256(value.encode()).hexdigest()
        return int(digest, 16)

    def add_node(self, node):
        position = self.hash(node)
        bisect.insort(self.positions, position)
        self.nodes[position] = node

    def remove_node(self, node):
        position = self.hash(node)
        self.positions.remove(position)
        del self.nodes[position]

    def get_node(self, key):
        if not self.positions:
            raise RuntimeError("Halkada sunucu yok")

        position = self.hash(key)
        index = bisect.bisect_left(self.positions, position)
        index %= len(self.positions)
        return self.nodes[self.positions[index]]
```

`bisect_left`, anahtarın hash değerine eşit veya ondan büyük ilk sunucu konumunu bulur. Mod işlemi ise halkanın sonuna gelindiğinde ilk sunucuya dönülmesini sağlar. Arama maliyeti sıralı yapı sayesinde yaklaşık $O(\log N)$ olur.

## Sanal düğümler neden gereklidir?

Gerçek sunucular halkaya rastgele yerleştiği için bazıları çok geniş, bazıları çok dar aralıklardan sorumlu olabilir. Bu dengesizliği azaltmak amacıyla her fiziksel sunucu halkaya birden fazla kez, örneğin `sunucu-a#1` ve `sunucu-a#2` adlarıyla eklenir. Bunlara sanal düğüm denir.

| Sanal düğüm sayısı | Dağılım | Bellek ve yönetim maliyeti |
|---|---|---|
| Az | Daha dengesiz | Düşük |
| Fazla | Daha dengeli | Daha yüksek |

Tutarlı hashleme sihirli bir değnek değildir; replikasyon, hata algılama ve popüler anahtarların oluşturduğu sıcak noktalar ayrıca yönetilmelidir. Yine de sunucuların sık değiştiği sistemlerde, tüm evi taşımak yerine yalnızca birkaç kolinin yerini değiştiren son derece güçlü bir mimari araçtır.

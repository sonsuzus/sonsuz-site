---
layout: post
title: "Bloom Filter: Az Bellekle Işık Hızında Üyelik Testi"
math: true
categories: 
  - Bilgi
tags: 
  - veri yapıları
  - bloom filter
  - algoritmalar
  - olasılıksal programlama
toc: true
---

Bir web tarayıcısının daha önce ziyaret edilmiş bir URL’yi, bir e-posta sunucusunun şüpheli adresi veya bir veritabanının diskte bulunmayan anahtarı saniyeler değil mikrosaniyeler içinde kontrol etmesi gerekir. Bloom Filter tam bu tür senaryolarda parlayan, olasılıksal bir veri yapısıdır: Bir elemanın kümede **kesinlikle olmadığını** söyler ya da **muhtemelen bulunduğunu** bildirir. Bu küçük belirsizlik, inanılmaz düşük bellek tüketimi ve sabit zamana yakın sorgu performansı karşılığında kabul edilir.

``

## Temel fikir: Bitlerden oluşan akıllı bir iz

Bloom Filter, başlangıçta tamamı `0` olan $m$ bitlik bir dizi ve $k$ farklı hash fonksiyonu kullanır. Bir eleman eklenirken her hash fonksiyonu çalıştırılır; üretilen indekslerdeki bitler `1` yapılır. Sorguda ise aynı indeksler kontrol edilir:

- En az bir bit `0` ise eleman **kesinlikle yoktur**.
- Tüm bitler `1` ise eleman **muhtemelen vardır**.

Yanlış negatif oluşmamasının sebebi budur: Bir kez `1` yapılan bit, standart Bloom Filter’da tekrar `0` olmaz. Ancak farklı elemanların hash sonuçları aynı bitlere denk gelebilir. Bu çakışmalar, kümede olmayan bir öğenin varmış gibi görünmesine yani **false positive** durumuna yol açar.

| Özellik | Bloom Filter | Hash Set |
|---|---|---|
| Üyelik sonucu | Kesin yok / muhtemel var | Kesin var veya yok |
| Bellek kullanımı | Çok düşüktür | Anahtarları sakladığı için yüksektir |
| Sorgu süresi | $O(k)$, pratikte çok hızlı | Ortalama $O(1)$ |
| Eleman silme | Standart sürümde güvenli değil | Desteklenir |
| Yanlış pozitif | Mümkün | Yok |

## Hata oranı nereden gelir?

Filtreye $n$ eleman eklendiğinde yaklaşık yanlış pozitif olasılığı şöyledir:

$$p \approx \left(1-e^{-kn/m}\right)^k$$

Burada $m$ bit dizisinin boyutu, $k$ hash sayısı ve $n$ beklenen eleman sayısıdır. Belirli bir hata oranı için ideal parametreler yaklaşık olarak:

$$m = -\frac{n\ln p}{(\ln 2)^2}, \qquad k = \frac{m}{n}\ln 2$$

Örneğin bir milyon eleman için %1 hata hedeflendiğinde yaklaşık 9,6 milyon bit, yani yalnızca yaklaşık 1,2 MB alan yeterlidir. Aynı anahtarları geleneksel bir `HashSet` içinde tutmak, nesne ve tablo ek yükleri nedeniyle bunun çok üzerinde bellek harcayabilir.

## Basit bir Python uygulaması

Aşağıdaki örnek, kavramı göstermek için `hashlib` ile iki temel hash türetiyor. Gerçek sistemlerde kaliteli ve hızlı hash fonksiyonları veya Redis gibi hazır çözümler tercih edilir.

```python
import hashlib

class BloomFilter:
    def __init__(self, bit_count=10_000, hash_count=5):
        self.m = bit_count
        self.k = hash_count
        self.bits = bytearray((bit_count + 7) // 8)

    def _indexes(self, value):
        raw = str(value).encode("utf-8")
        for seed in range(self.k):
            digest = hashlib.sha256(seed.to_bytes(2, "big") + raw).digest()
            yield int.from_bytes(digest[:8], "big") % self.m

    def _set_bit(self, index):
        self.bits[index // 8] |= 1 << (index % 8)

    def _get_bit(self, index):
        return bool(self.bits[index // 8] & (1 << (index % 8)))

    def add(self, value):
        for index in self._indexes(value):
            self._set_bit(index)

    def might_contain(self, value):
        return all(self._get_bit(i) for i in self._indexes(value))
```

`add` yalnızca bitleri işaretler; `might_contain` ise tüm işaretlerin mevcut olup olmadığını denetler. Fonksiyon adı özellikle önemlidir: Sonuç `True` olduğunda bunu kesin kanıt gibi kullanmamak gerekir.

## Nerede kullanılır, nerede kullanılmaz?

Bloom Filter çoğunlukla pahalı bir işlemin önünde koruyucu katman olarak görev yapar. Örneğin önce filtre kontrol edilir; sonuç olumluysa veritabanına sorgu atılır. Olumsuz sonuçta veritabanına hiç gidilmez. Önbellek sızıntısını azaltma, web tarayıcısı URL geçmişi, kötü amaçlı URL listeleri ve dağıtık depolama sistemleri klasik kullanım alanlarıdır.

Silme gereksiniminiz varsa sayaç tutan **Counting Bloom Filter** kullanılabilir. Buna karşılık finansal bakiye, yetkilendirme veya kesinlik zorunlu kayıtlar için Bloom Filter tek başına uygun değildir. Onu bir karar verici değil, pahalı sorguları eleyen son derece hızlı bir ön kontrol görevlisi olarak düşünün.

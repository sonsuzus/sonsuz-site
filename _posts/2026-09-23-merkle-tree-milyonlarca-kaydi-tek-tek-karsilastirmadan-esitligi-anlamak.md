---
layout: post
title: "Merkle Tree: Milyonlarca Kaydı Tek Tek Karşılaştırmadan Eşitliği Anlamak"
math: true
categories: 
  - Bilgi
tags: 
  - merkle-tree
  - veri-yapıları
  - hash
  - algoritma
  - dağıtık-sistemler
  - python
toc: true
---

Elinizde milyonlarca dosya veya kayıt içeren iki veri kümesi olduğunu düşünün. Bunların aynı olup olmadığını anlamak için her kaydı tek tek karşılaştırmak mümkündür; fakat pek zarif değildir. Merkle Tree, verileri kriptografik özetlerden oluşan bir ağaca dönüştürerek bu işi çok daha verimli yapar. Kök özetler aynıysa veri kümeleri büyük olasılıkla aynıdır; farklıysa ağacın dallarını izleyerek uyuşmazlığın yerini bulabilirsiniz.
``
## Temel fikir: Verinin parmak izini çıkarmak

Merkle Tree, yapraklarında verilerin hash değerlerini taşıyan ikili bir ağaçtır. Hash fonksiyonu, herhangi bir girdiyi sabit uzunlukta bir özete dönüştürür:

$$h_i = H(d_i)$$

Burada $d_i$ veri parçasını, $H$ hash fonksiyonunu, $h_i$ ise oluşan özeti temsil eder. SHA-256 gibi kriptografik fonksiyonlarda girdideki küçücük bir değişiklik, tamamen farklı bir çıktı üretir.

Yaprakların üstündeki her düğüm, iki çocuğunun özetleri birleştirilip yeniden hash edilerek hesaplanır:

$$p_i = H(h_{2i} \Vert h_{2i+1})$$

$\Vert$ sembolü birleştirme işlemini gösterir. Bu süreç tek bir kök kalana kadar devam eder. Kök değerine **Merkle Root** denir ve bütün veri kümesinin parmak izi gibi davranır.

| Yaklaşım | İlk kontrol maliyeti | Farkın yerini bulma | Ek yapı |
|---|---:|---:|---:|
| Kayıtları tek tek karşılaştırma | $O(n)$ | $O(n)$ | Gerekmez |
| Tek dosya hash’i kullanma | $O(1)$ | Farkın konumunu göstermez | Tek hash |
| Merkle Tree kullanma | $O(1)$ kök kontrolü | Yaklaşık $O(\log n)$ dal incelemesi | $O(n)$ hash |

Tablodaki $O(1)$ ifadesi, ağaçların önceden oluşturulduğu ve yalnızca köklerin karşılaştırıldığı durumu anlatır. Ağacı sıfırdan kurmanın maliyeti hâlâ $O(n)$ seviyesindedir. Yani Merkle Tree sihir değil; tekrar eden doğrulamalar için önceden hazırlanmış akıllı bir indeks gibidir.

## Farklı kayıt nasıl bulunur?

İki ağacın kökleri eşitse kontrol biter. Kökler farklıysa onların çocukları karşılaştırılır. Sol çocuklar aynı, sağ çocuklar farklıysa yalnızca sağ dala ilerlenir. Her adımda arama alanı yaklaşık yarıya düşer. Bir milyon yaprak için yaklaşık

$$\log_2(1.000.000) \approx 20$$

seviye yeterlidir. Böylece milyonlarca kaydı ağ üzerinden taşımak yerine birkaç düzine hash karşılaştırılabilir. Dağıtık veritabanları, blokzincirler ve eşler arası dosya sistemleri bu avantajdan yararlanır.

## Python ile küçük bir Merkle Tree

Aşağıdaki kod, metin kayıtlarından Merkle kökü üretir. Yaprak sayısı tek olduğunda son hash kopyalanarak çift oluşturulur:

```python
import hashlib


def digest(value: bytes) -> bytes:
    """Verilen bayt dizisinin SHA-256 özetini üretir."""
    return hashlib.sha256(value).digest()


def merkle_root(records: list[str]) -> str:
    if not records:
        return hashlib.sha256(b"").hexdigest()

    level = [digest(record.encode("utf-8")) for record in records]

    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])

        level = [
            digest(level[i] + level[i + 1])
            for i in range(0, len(level), 2)
        ]

    return level[0].hex()

set_a = ["elma", "armut", "kiraz", "muz"]
set_b = ["elma", "armut", "vişne", "muz"]

print(merkle_root(set_a))
print(merkle_root(set_b))
```

İki çıktı farklı olacaktır; çünkü tek bir kaydın değişmesi köke kadar bütün üst hash değerlerini etkiler. Ancak pratik bir senkronizasyon sisteminde yalnızca kökü hesaplamak yetmez. Ara düğümler de saklanır ve farklı kökün hangi alt ağaçtan kaynaklandığı araştırılır.

## Dikkat edilmesi gerekenler

Merkle Root eşitliği matematiksel olarak verilerin kesinlikle aynı olduğunu kanıtlamaz; teorik olarak hash çakışması mümkündür. Bununla birlikte SHA-256 için rastgele çakışma olasılığı yaklaşık $1/2^{256}$ olduğundan pratikte ihmal edilir.

Ayrıca kayıt sırası, karakter kodlaması ve serileştirme biçimi standartlaştırılmalıdır. `42`, `"42"` ve boşluk içeren `"42 "` farklı bayt dizileridir. Kısacası Merkle Tree karşılaştırmayı hızlandırır, fakat önce “aynı veri” tanımında anlaşmak gerekir. Doğru normalizasyonla birlikte kullanıldığında ise milyonluk veri kümelerinin dedektifliğini birkaç hash’e indiren son derece güçlü bir araçtır.

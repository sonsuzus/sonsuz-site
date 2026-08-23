---
layout: post
title: "Cuckoo Hashing: Çakışmaları Tekmeleyerek Çözen Hızlı Hash Tablosu"
math: true
categories: 
  - Bilgi
tags: 
  - veri yapıları
  - hash tablosu
  - algoritmalar
---

Hash tabloları, anahtarları ortalama $O(1)$ sürede bulma vaadiyle programlamanın görünmez kahramanlarıdır. Ancak iki anahtar aynı konuma düştüğünde ortaya çıkan çakışma, bu vaadi zorlayabilir. Cuckoo Hashing, çakışmayı zincirleme listelerle uzatmak yerine iki farklı olası yuva sunar ve gerekirse mevcut elemanı yerinden “tekmeleyerek” taşır. Adını da yumurtasını başka kuşların yuvasına bırakan guguk kuşundan alır.
``

Klasik bir hash tablosunda tek bir $h(k)$ fonksiyonu kullanıldığını düşünelim. Cuckoo Hashing ise her anahtar için en az iki aday hücre üretir: $h_1(k)$ ve $h_2(k)$. Anahtar yalnızca bu iki hücreden birinde bulunabilir. Arama sırasında en fazla iki konuma bakılması, erişim maliyetini özellikle öngörülebilir kılar:

$$T_{arama}(k) \leq 2 = O(1)$$

Bu sınır, zincirleme yaklaşımında kötü dağılım veya yüksek doluluk altında oluşabilecek uzun listelerin aksine, en kötü durum araması için de geçerlidir. Elbette bu güzelliğin bedeli ekleme operasyonunda ortaya çıkar.

| Yaklaşım | Çakışma çözümü | Arama | Ekleme davranışı |
|---|---|---:|---|
| Zincirleme | Aynı kovada liste tutar | Ortalama $O(1)$ | Listeye ekler |
| Linear Probing | Boş hücreyi sırayla arar | Kümeleşmeden etkilenir | Komşu hücrelere kayar |
| Cuckoo Hashing | İki aday konum kullanır | En kötü durumda $O(1)$ | Elemanları yer değiştirir |

Ekleme mantığı bir tahliye zinciri gibidir. Yeni anahtarı ilk konumuna koymak isteriz. Hücre doluysa oradaki anahtarı çıkarır, yerine yenisini yerleştiririz. Çıkarılan anahtarın da diğer hash fonksiyonuyla hesaplanan alternatif yuvasına taşınması gerekir. Bu süreç boş bir hücre bulunana kadar sürer.

```python
class CuckooTable:
    def __init__(self, size=11):
        self.table = [None] * size
        self.size = size

    def h1(self, key):
        return hash(key) % self.size

    def h2(self, key):
        return (hash(str(key) + "salt") % self.size)

    def insert(self, key, limit=20):
        current = key
        pos = self.h1(current)

        for _ in range(limit):
            if self.table[pos] is None:
                self.table[pos] = current
                return True
            self.table[pos], current = current, self.table[pos]
            alternative = self.h2(current)
            pos = alternative if pos == self.h1(current) else self.h1(current)
        return False  # Döngü olasılığı: yeniden hashleme gerekli
```

Bu örnekte `insert`, dolu bir hücreye geldiğinde içeriği `current` değişkenine alır; yeni anahtar hücreye geçer. Ardından yerinden edilen anahtarın diğer adresi hesaplanır. `limit` ise sonsuz tahliye döngülerine karşı emniyet kemeridir.

Peki döngü neden oluşur? İki hash fonksiyonunun ürettiği ilişkileri bir grafik gibi düşünebiliriz: hücreler düğüm, her anahtar ise iki olası hücreyi bağlayan bir kenardır. Yeni bir kenar eklendiğinde boş bir düğüme ulaşamayan kapalı bir bileşen oluşursa yer değiştirme sonsuza dek sürebilir. Çözüm, tabloyu büyütmek ve yeni hash fonksiyonlarıyla tüm anahtarları yeniden yerleştirmektir.

| Özellik | Güçlü taraf | Dikkat edilmesi gereken |
|---|---|---|
| Arama | En fazla iki bellek erişimi | İki hash hesaplanır |
| Silme | Hücre doğrudan boşaltılır | Özel “silindi” işareti gerekmez |
| Ekleme | Ortalama olarak hızlıdır | Nadir de olsa yeniden hashleme olur |
| Bellek | Zincir düğümü gerektirmez | Doluluk oranı sınırlı tutulmalıdır |

İki fonksiyonlu temel sürümde pratik doluluk hedefi genellikle yaklaşık $\alpha = n/m < 0.5$ civarındadır; burada $n$ eleman sayısı, $m$ hücre sayısıdır. Daha yüksek doluluk istenirse her kovada birden fazla hücre kullanan bucketed cuckoo hashing veya üçten fazla hash fonksiyonu tercih edilebilir.

Sonuç olarak Cuckoo Hashing, ekleme anını biraz hareketli hâle getirip aramayı son derece sakinleştirir. Önbellek, ağ tablosu ve gecikme garantisinin önemli olduğu sistemlerde bu takas oldukça değerlidir: Anahtarınızı bulmak için uzun bir listeyi gezmek yerine, sadece iki kapıyı çalarsınız.

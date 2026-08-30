---
layout: post
title: "Perfect Hashing Nedir? Çakışmasız Hash Tablolarının Teorisi ve Kullanımı"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - veri yapıları
  - hashing
toc: true
---

Hash tabloları, anahtarları hızlıca bulmanın süper kahramanıdır; fakat klasik yaklaşımlarda iki anahtarın aynı kovaya düşmesi, yani **çakışma**, kaçınılmazdır. Perfect hashing ise özellikle anahtar kümesinin önceden bilindiği durumlarda bu dramayı tamamen ortadan kaldırır. Amaç, her anahtarı benzersiz bir hücreye yerleştiren ve sorguları sabit zamanda gerçekleştiren bir hash fonksiyonu tasarlamaktır.
``

## Temel fikir: Bire bir eşleme

Bir anahtar kümesi $S$ ve $n = \vert S\vert $ olsun. Bir hash fonksiyonu $h$, anahtarları $m$ adet tablo hücresine gönderir:

$$h: S \rightarrow \{0,1,\dots,m-1\}$$

Eğer $S$ içindeki farklı her iki anahtar için aşağıdaki koşul sağlanıyorsa fonksiyon **perfect hash function** olarak adlandırılır:

$$x \neq y \Rightarrow h(x) \neq h(y)$$

Başka bir deyişle, $h$ fonksiyonu anahtar kümesi üzerinde enjeksiyondur. Tablo boyutu tam olarak anahtar sayısına eşitse, yani $m=n$ ise buna **minimal perfect hashing** denir. Bu senaryoda tek bir boş hücre bile yoktur: alan kullanımı teorik olarak kusursuza yakındır.

| Yaklaşım | Çakışma | Arama maliyeti | Alan kullanımı | Anahtar kümesi |
|---|---:|---:|---:|---|
| Zincirleme (chaining) | Var | Ortalama $O(1)$ | Ek bağlantılar gerekir | Dinamik |
| Açık adresleme | Var | Ortalama $O(1)$ | Doluluk oranına duyarlı | Dinamik |
| Perfect hashing | Yok | En kötü durumda $O(1)$ | Genellikle kompakt | Statik |
| Minimal perfect hashing | Yok | En kötü durumda $O(1)$ | Yaklaşık $n$ hücre | Statik |

Buradaki kritik kelime **statik**tir. Perfect hash yapısı oluşturulduktan sonra anahtar eklemek veya silmek çoğunlukla tüm yapıyı yeniden inşa etmeyi gerektirir. Bu nedenle kullanıcı oturumları gibi sürekli değişen verilerden çok, derleme zamanında belirlenen anahtarlar için parlar.

## FKS: İki seviyeli zarif çözüm

Fredman, Komlós ve Szemerédi tarafından geliştirilen FKS şeması, teorik bilgisayar bilimlerinin ünlü perfect hashing yöntemlerinden biridir. İlk hash fonksiyonu anahtarları kovalar arasında dağıtır. Bir kovada çakışma oluşursa, yalnızca o kova için ikinci bir tablo ve ikinci bir hash fonksiyonu kurulur.

Kovanın içinde $k_i$ anahtar varsa, ikinci seviye tablo yaklaşık $k_i^2$ boyutunda seçilir. Bu ilk bakışta pahalı görünür; ancak rastgele seçilmiş iyi birinci seviye fonksiyonla toplam alanın beklenen değeri $O(n)$ olur. Sonuç: hem depolama hem de erişim maliyeti verimlidir.

```python
# Eğitim amaçlı basitleştirilmiş iki seviyeli yapı fikri
# Gerçek uygulamada her kova için çakışmasız ikinci fonksiyon aranır.
def first_hash(key, bucket_count):
    return hash(key) % bucket_count

keys = ["GET", "POST", "PUT", "DELETE"]
buckets = [[] for _ in range(len(keys))]

for key in keys:
    buckets[first_hash(key, len(buckets))].append(key)

for index, bucket in enumerate(buckets):
    if bucket:
        print(f"Kova {index}: {bucket}, ikinci tablo boyutu: {len(bucket) ** 2}")
```

Bu kod doğrudan üretim kalitesinde perfect hash üretmez; ilk dağılımı ve FKS'nin neden kare boyutlu alt tablolara başvurduğunu görünür kılar. Uygulamada ikinci hash fonksiyonu, ilgili kovadaki tüm anahtarlar farklı hücrelere yerleşene kadar seçilir veya denenir.

## Nerede kullanılır?

Perfect hashing; programlama dillerindeki anahtar sözcük tanımada, HTTP başlıkları veya metot adlarında, derleyicilerdeki sembol tablolarında, ağ protokollerinde ve salt-okunur sözlüklerde kullanışlıdır. Örneğin bir dilin `while`, `return` ve `class` gibi anahtar sözcükleri sürüm boyunca değişmiyorsa, bunları zincirleme karşılaştırmalar yerine perfect hash ile eşlemek hızlı ve öngörülebilir olur.

| Kullanım senaryosu | Neden uygundur? | Dikkat edilmesi gereken |
|---|---|---|
| Derleyici anahtar sözcükleri | Küme küçük ve sabittir | Dil sürümünde yeniden üretim gerekir |
| Protokol sabitleri | Hızlı ayrıştırma sağlar | Girdi doğrulaması ayrıca yapılmalıdır |
| Salt-okunur sözlükler | Bellek verimliliği yüksektir | Güncelleme maliyetlidir |
| Konfigürasyon anahtarları | Tahmin edilebilir gecikme | Çok sık değişimde uygun değildir |

Özetle perfect hashing, “her şeyi hash tablosuna atalım” yaklaşımından ziyade, anahtarları önceden tanıdığınızda kullanılan planlı bir optimizasyondur. Kurulum maliyetini peşin öder, karşılığında çakışmasız ve en kötü durumda bile $O(1)$ erişim elde edersiniz.

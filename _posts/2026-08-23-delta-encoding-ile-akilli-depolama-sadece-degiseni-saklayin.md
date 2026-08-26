---
layout: post
title: "Delta Encoding ile Akıllı Depolama: Sadece Değişeni Saklayın"
math: true
categories: 
  - Bilgi
tags: 
  - delta encoding
  - veri sıkıştırma
  - depolama
  - python
---

Bir klasördeki günlük yedeklerin neredeyse aynı olduğunu düşünün: Dün 2 GB olan verinin bugün yalnızca birkaç megabaytı değişti. Her sürümün tamamını saklamak, hem disk alanını hem de ağ trafiğini hızla tüketir. Delta Encoding, tam da bu israfı azaltmak için benzer dosyaların ortak kısımlarını tekrar depolamak yerine yalnızca aralarındaki farkı, yani *delta* bilgisini saklar.
``

Temel fikir iki sürüm üzerinden anlaşılır. Elimizde bir **baz dosya** $B$ ve onun değiştirilmiş hâli olan **hedef dosya** $T$ olsun. Geleneksel yaklaşım her ikisini de saklar. Delta yaklaşımı ise $B$ ile birlikte, $B$ dosyasını $T$ dosyasına dönüştürecek dönüşüm bilgisini $\Delta(B,T)$ saklar:

$$T = Apply(B, \Delta(B,T))$$

Depolama açısından kazanç, delta boyutunun hedef dosyadan belirgin biçimde küçük olmasına bağlıdır. Yaklaşık tasarruf oranı şöyle ifade edilebilir:

$$Tasarruf = 1 - \frac{\vert B\vert  + \vert \Delta\vert }{\vert B\vert  + \vert T\vert }$$

Örneğin 100 MB'lık bir dosyanın sonraki sürümünde 2 MB değişmişse, iyi üretilmiş bir delta birkaç MB civarında olabilir. Ancak dosyanın tamamı değiştiyse delta, baz dosya kadar hatta bazı algoritmalarda daha büyük bile olabilir. Yani delta encoding sihir değil; benzerlikten güç alan bir tekniktir.

| Yaklaşım | Saklanan veri | Avantaj | Dezavantaj |
|---|---|---|---|
| Tam kopya | Her sürümün tamamı | Geri yükleme çok basit | Yüksek alan tüketimi |
| Delta encoding | Baz sürüm + farklar | Benzer sürümlerde büyük tasarruf | Geri yükleme için zincir çözülür |
| Blok tabanlı tekilleştirme | Yinelenen bloklar bir kez | Çok sayıda dosyada etkilidir | İndeks ve karma yönetimi gerekir |

Delta üretmenin farklı yolları vardır. Metin dosyalarında satır tabanlı karşılaştırma anlaşılır sonuçlar verir: eklenen, silinen ve değişen satırlar kaydedilir. İkili dosyalarda ise algoritmalar çoğunlukla dosyayı bloklara ayırır, baz dosyada bulunan blokları bulmak için karma değerlerinden yararlanır ve yalnızca yeni bayt dizilerini gönderir. `rsync` algoritmasının ünlü yanı, uzak taraftaki dosyanın blok özetlerini kullanarak ağ üzerinden gereksiz veri taşımamasıdır.

Aşağıdaki Python örneği, eğitim amacıyla iki metin sürümü arasında satır tabanlı bir delta üretir. Bu, üretim ortamındaki ikili delta formatlarının yerini tutmaz; fakat mantığı görünür kılar.

```python
from difflib import ndiff, restore

base = "merhaba\ndelta encoding\ndisk tasarrufu\n"
target = "merhaba\ndelta encoding\nbüyük disk tasarrufu\n"

# '+' eklenen, '-' silinen, ' ' aynı kalan satırları gösterir.
delta = list(ndiff(base.splitlines(True), target.splitlines(True)))
print("".join(delta))

# 2, diff çıktısından hedef sürümü yeniden kur anlamına gelir.
reconstructed = "".join(restore(delta, 2))
assert reconstructed == target
```

Burada `delta`, değişiklikleri taşıyan bir talimat listesi gibidir. Gerçek bir sistemde bu liste sıkıştırılabilir, sürüm kimliği ve bütünlük doğrulaması için hash ile birlikte tutulabilir. Örneğin hedef sürümün SHA-256 özeti kaydedilirse geri yükleme sonrasında üretilen verinin doğru olduğu doğrulanır.

Delta zincirlerinin de bir bedeli vardır. `v1` tam kopya, `v2` ise `v1` farkı, `v3` ise `v2` farkı olarak saklanırsa `v3` için tüm halkaların uygulanması gerekir. Zincir uzadıkça erişim yavaşlar ve aradaki tek bir bozuk delta sonraki sürümleri etkileyebilir. Bu nedenle pratik sistemler belirli aralıklarla yeni bir tam kopya, yani *snapshot* oluşturur.

| Senaryo | Delta Encoding uygun mu? | Neden? |
|---|---|---|
| Kaynak kodu sürümleri | Evet | Değişiklikler genellikle küçük ve metinseldir |
| Günlük veritabanı yedekleri | Genellikle evet | Artımlı değişimler tam yedekten küçüktür |
| Her karede değişen video | Sınırlı | Benzerlik olsa da özel codec gerekir |
| Şifrelenmiş rastgele veri | Çoğunlukla hayır | Küçük değişim bile tüm çıktıyı değiştirebilir |

Özetle delta encoding, depolama maliyetini azaltmak için “dosyayı tekrar saklama, değişikliği sakla” der. Başarılı bir tasarım; doğru baz sürüm seçimi, makul zincir uzunluğu, bütünlük kontrolü ve düzenli snapshot politikasıyla birleştiğinde hem yedekleme hem sürümleme sistemlerinin güçlü araçlarından biri olur.

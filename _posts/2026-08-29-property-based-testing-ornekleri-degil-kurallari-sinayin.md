---
layout: post
title: "Property-Based Testing: Örnekleri Değil Kuralları Sınayın"
math: true
categories: 
  - Bilgi
tags: 
  - property-based testing
  - yazılım testi
  - python
  - hypothesis
---

Geleneksel birim testleri, belirli girdiler için beklenen çıktıları doğrular: `topla(2, 3) == 5` gibi. Bu yaklaşım vazgeçilmezdir; ancak geliştiricinin hiç düşünmediği binlerce uç durum kapının dışında kalabilir. Property-Based Testing (özellik tabanlı test), tek tek örnekler yazmak yerine fonksiyonun her zaman sağlaması gereken genel kuralları tanımlar. Test aracı da çok sayıda girdi üreterek bu kuralları zorlamaya başlar. Kısacası siz dedektifin kural kitabını yazarsınız, araç ise şüpheli vakaları bulur.
``

Bu yaklaşımın merkezinde **property**, yani değişmez davranış kuralı bulunur. Örneğin bir sıralama fonksiyonu için yalnızca `[3, 1, 2]` örneğini test etmek yeterli değildir. Asıl kurallar şunlardır: sonuç sıralı olmalı, girişteki elemanları kaybetmemeli ve aynı girdiyi tekrar sıralamak sonucu değiştirmemelidir. Matematiksel olarak sıralama işlemi için şu özellikleri ifade edebiliriz:

$$
\operatorname{sort}(x) = y \Rightarrow y_i \leq y_{i+1}
$$

Ayrıca sıralama idempotenttir:

$$
\operatorname{sort}(\operatorname{sort}(x)) = \operatorname{sort}(x)
$$

| Yaklaşım | Testin odağı | Güçlü yanı | Yaygın riski |
|---|---|---|---|
| Örnek tabanlı test | Bilinen senaryolar | Okunması ve anlatılması kolaydır | Unutulan uç durumlar |
| Property-Based Testing | Genel davranış kuralları | Çok geniş girdi uzayını tarar | Yanlış veya muğlak property yazmak |
| Entegrasyon testi | Bileşenlerin birlikte çalışması | Gerçek akışları yakalar | Çalıştırması yavaş olabilir |

Property-Based Testing, rastgelelikten ibaret değildir. İyi araçlar, türüne uygun **generator**'lar kullanır: tam sayılar, Unicode metinler, boş koleksiyonlar, çok uzun listeler ve sınır değerler üretir. Bir hata yakalandığında da **shrinking** adı verilen küçültme işlemi devreye girer. Araç, başarısızlığa yol açan karmaşık girdiyi mümkün olan en küçük karşı örneğe indirger. Böylece `[-19, 0, 884, ...]` yerine belki yalnızca `[-1]` ile karşılaşırsınız. Bu, hata ayıklama süresini dramatik biçimde azaltır.

Python dünyasında Hypothesis, bu fikri oldukça erişilebilir kılar. Aşağıdaki test, özel bir sıralama fonksiyonunun hem sıralı sonuç üretmesini hem de eleman korumasını denetler:

```python
from hypothesis import given, strategies as st


def benim_sirala(sayilar):
    return sorted(sayilar)


@given(st.lists(st.integers()))
def test_siralama_kurallari(sayilar):
    sonuc = benim_sirala(sayilar)

    # Sonuç artan sırada olmalı.
    assert all(sonuc[i] <= sonuc[i + 1]
               for i in range(len(sonuc) - 1))

    # Sıralama, elemanların sayısını ve değerlerini korumalı.
    assert sorted(sonuc) == sorted(sayilar)
```

Burada `@given`, test fonksiyonunu farklı listelerle defalarca çağırır. `st.lists(st.integers())` stratejisi ise boş liste, negatif değerler, tekrar eden sayılar ve büyük sayılar gibi çeşitleri otomatik üretir. İkinci assertion ilk bakışta gereksiz görünebilir; fakat kendi sıralama algoritmanızı yazıyorsanız bir elemanı yanlışlıkla düşürme gibi hataları yakalar.

Her fonksiyon için property seçerken şu sorular faydalıdır: İşlem tekrarlandığında sonuç aynı kalır mı? Girdi büyüdükçe çıktıdaki hangi ilişki korunur? Bir işlemin tersi var mı? Örneğin encode/decode çiftinde ideal kural şudur:

$$
\operatorname{decode}(\operatorname{encode}(x)) = x
$$

| Problem tipi | Yararlı property örneği |
|---|---|
| Tarih işlemleri | Tarihe eklenen ve çıkarılan aynı gün sayısı ilk tarihi vermeli |
| Serileştirme | `deserialize(serialize(x)) == x` olmalı |
| Arama | Bulunan indeks geçerliyse o konumdaki değer hedefe eşit olmalı |
| Para hesaplama | Toplam, kalemlerin toplamına eşit olmalı; yuvarlama açıkça tanımlanmalı |

Bu teknik örnek tabanlı testlerin yerine geçmez; onları tamamlar. Kritik iş kuralları ve anlaşılır senaryolar için örnek testler yazın. Ardından sınırları, dönüşümleri ve değişmezleri Property-Based Testing'e devredin. Sonuç: Daha az tahmin, daha çok güven ve üretimde daha az “bu girdi nereden çıktı?” sürprizi.

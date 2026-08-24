---
layout: post
title: "Fuzz Testing ile Yazılımların Gizli Hatalarını Avlayın"
math: true
categories: 
  - Bilgi
tags: 
  - Fuzz Testing
  - Yazılım Testi
  - Siber Güvenlik
---

Bir yazılımın mutlu yolunda çalışması, onun her koşulda güvenli olduğu anlamına gelmez. Kullanıcıların boş metin, devasa dosya, bozuk karakter kodlaması veya beklenmeyen veri türleri gönderebildiği gerçek dünyada asıl sorunlar köşe durumlarda yaşanır. **Fuzz testing** ya da kısa adıyla *fuzzing*, uygulamalara otomatik biçimde sıra dışı, hatalı veya rastgele girdiler göndererek çökmeleri, istisnaları ve güvenlik açıklarını bulma disiplinidir. Bir bakıma yazılımınıza kontrollü kaos yaşatırsınız.
``

## Fuzzing neden gereklidir?

Birim testleri genellikle geliştiricinin tahmin ettiği senaryoları doğrular. Fuzzing ise “Bunu biri gerçekten gönderirse ne olur?” sorusunu sorar. Örneğin bir JSON ayrıştırıcısı geçerli bir sipariş verisini sorunsuz okuyabilir; fakat yarım kalmış JSON, negatif miktar, çok derin iç içe nesneler veya geçersiz Unicode karakterleri geldiğinde hata verebilir.

Fuzzing'in temel fikri, girdi uzayını olabildiğince geniş taramaktır. Bir fonksiyonun kabul ettiği olası girdi kümesini $I$, hataya yol açan girdileri de $F$ ile gösterelim. Amaç, üretilen test girdileri $T$ için şu kesişimi bulmaktır:

$$T \cap F \neq \varnothing$$

Elbette tüm olası girdileri denemek çoğu zaman imkânsızdır. Özellikle uzunluğu $n$ olan ve 256 farklı byte içerebilen bir veri için teorik kombinasyon sayısı $256^n$ olur. Bu nedenle iyi fuzzing araçları rastgelelik, mutasyon ve kod kapsama bilgisini birlikte kullanır.

| Test yaklaşımı | Girdi kaynağı | Güçlü yanı | Sınırlaması |
|---|---|---|---|
| Birim testi | Elle yazılmış örnekler | Beklenen davranışı doğrular | Bilinmeyen köşe durumları kaçabilir |
| Rastgele fuzzing | Tamamen rastgele veri | Hızlı başlangıç sağlar | Anlamlı kod yollarına ulaşmak zor olabilir |
| Mutasyon tabanlı fuzzing | Geçerli örneklerin bozulması | Gerçekçi veri yapısını korur | Başlangıç örneklerine ihtiyaç duyar |
| Kapsama güdümlü fuzzing | Kod geri bildirimi | Yeni yürütme yolları keşfeder | Kurulum ve ölçüm maliyeti vardır |

## Basit bir örnekle başlayalım

Python'da bir metin ayrıştırıcısının yalnızca rakamlardan oluşan, 1-100 arası değerleri kabul ettiğini düşünün. Aşağıdaki mini örnek, beklenmeyen girdilerin yönetilip yönetilmediğini kontrol eder:

```python
import random
import string

def indirim_orani(metin: str) -> int:
    oran = int(metin)
    if not 1 <= oran <= 100:
        raise ValueError("Oran 1 ile 100 arasında olmalı")
    return oran

for _ in range(1000):
    girdi = "".join(random.choice(string.printable)
                    for _ in range(random.randint(0, 20)))
    try:
        indirim_orani(girdi)
    except (ValueError, TypeError):
        pass  # Beklenen, kontrollü hata
    except Exception as hata:
        print("Beklenmeyen hata:", repr(hata), "Girdi:", repr(girdi))
```

Bu kod bir güvenlik tarayıcısı değildir; ancak önemli bir ilkeyi gösterir: Beklenmeyen veri geldiğinde uygulama anlaşılır ve kontrollü biçimde başarısız olmalıdır. `ValueError` beklenen bir doğrulama sonucuyken, örneğin `IndexError` veya uygulamanın çökmesi araştırılması gereken bir bulgudur.

## Etkili bir fuzzing stratejisi

İyi bir kampanya için önce hedefi belirleyin: Dosya ayrıştırıcıları, API uç noktaları, deserializasyon katmanları ve kullanıcı girdisi alan fonksiyonlar önceliklidir. Ardından mümkünse geçerli örnek girdilerden oluşan küçük bir *corpus* hazırlayın. Fuzzer bu örnekleri keser, birleştirir, byte değiştirir ve sınır değerleri dener.

Bulduğunuz her çökme için tekrar üretilebilir bir test vakası saklayın. Ardından hatayı düzeltin ve bu girdiyi regresyon testlerine ekleyin. AFL++, libFuzzer ve Honggfuzz gibi araçlar yerel programlarda; web servislerinde ise şema tabanlı araçlar ve özel test üreticileri faydalı olabilir.

Fuzzing'i yalnızca size ait veya test etme izniniz bulunan sistemlerde çalıştırın. Doğru kapsam, kayıt tutma ve izolasyon ile bu yöntem; rastgele veri savurmaktan çok, yazılımınızın dayanıklılığını ölçen güçlü ve sürekli bir kalite pratiğine dönüşür.

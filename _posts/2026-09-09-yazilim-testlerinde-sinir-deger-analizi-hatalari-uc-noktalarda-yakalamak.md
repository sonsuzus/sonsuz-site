---
layout: post
title: "Yazılım Testlerinde Sınır Değer Analizi: Hataları Uç Noktalarda Yakalamak"
math: true
categories: 
  - Bilgi
tags: 
  - yazılım testi
  - sınır değer analizi
  - test otomasyonu
toc: true
---

Bir kullanıcı formuna 18 yerine 17 yaş girildiğinde ne olur? Peki 18 kabul edilirken 65’in kabul edilmemesi gerekiyorsa sistem 65’e nasıl davranır? Yazılım hataları çoğu zaman veri aralığının ortasında değil, koşulların birbirine değdiği uç noktalarda saklanır. **Sınır Değer Analizi** (Boundary Value Analysis — BVA), her olasılığı denemek yerine hata çıkma ihtimali yüksek değerleri seçerek minimum eforla güçlü bir test kapsamı oluşturur.

``

## Sınırlar neden risklidir?

Programcılar aralıkları genellikle karşılaştırma operatörleriyle tanımlar: `<`, `<=`, `>`, `>=`. Ancak küçücük bir eşittir işareti, sistem davranışını tamamen değiştirebilir. Örneğin geçerli yaş aralığı matematiksel olarak

$$18 \leq x \leq 65$$

şeklinde tanımlansın. Geliştirici yanlışlıkla `x > 18` yazarsa 18 yaşındaki kullanıcı reddedilir. `x < 65` yazarsa benzer sorun üst sınırda ortaya çıkar. Bunlar klasik **off-by-one** hatalarıdır.

Sınır Değer Analizi, geçerli bir $[a,b]$ aralığı için özellikle şu değerlerle ilgilenir:

$$a-1,\ a,\ a+1,\ b-1,\ b,\ b+1$$

Bu değerler; sınırın hemen dışını, kendisini ve hemen içini temsil eder. Aralığın ortasından seçilen bir değer de normal davranışı doğrulamak için eklenebilir.

| Değer türü | Yaş örneği | Beklenen sonuç | Amaç |
|---|---:|---|---|
| Alt sınırın dışı | 17 | Geçersiz | Eksik alt sınır kontrolünü bulmak |
| Alt sınır | 18 | Geçerli | `>` ile `>=` hatasını yakalamak |
| Alt sınırın içi | 19 | Geçerli | Sınır sonrası davranışı doğrulamak |
| Normal değer | 40 | Geçerli | Tipik akışı kontrol etmek |
| Üst sınırın içi | 64 | Geçerli | Sınır öncesi davranışı doğrulamak |
| Üst sınır | 65 | Geçerli | `<` ile `<=` hatasını yakalamak |
| Üst sınırın dışı | 66 | Geçersiz | Taşan değerin reddedildiğini görmek |

## Eşdeğer bölümlendirme ile ilişkisi

BVA tek başına sihirli bir değnek değildir. Çoğunlukla **Eşdeğer Bölümlendirme** ile birlikte kullanılır. Bu yaklaşım, girdileri aynı davranışı göstermesi beklenen sınıflara ayırır.

| Bölüm | Aralık | Temsilci değer |
|---|---|---:|
| Geçersiz düşük | $x < 18$ | 17 |
| Geçerli | $18 \leq x \leq 65$ | 40 |
| Geçersiz yüksek | $x > 65$ | 66 |

Eşdeğer bölümlendirme “hangi bölgeleri test etmeliyim?” sorusunu, sınır analizi ise “bu bölgelerin en riskli noktaları hangileri?” sorusunu yanıtlar. Böylece yüzlerce giriş yerine birkaç stratejik değer kullanılır.

## Orta düzey bir otomasyon örneği

Aşağıdaki Python fonksiyonu yaşın kabul edilip edilmediğini belirler. Parametreli test ise bütün kritik değerleri tek bir test yapısında çalıştırır:

```python
def is_valid_age(age: int) -> bool:
    return 18 <= age <= 65

import pytest

@pytest.mark.parametrize("age, expected", [
    (17, False),
    (18, True),
    (19, True),
    (40, True),
    (64, True),
    (65, True),
    (66, False),
])
def test_age_boundaries(age, expected):
    assert is_valid_age(age) is expected
```

`pytest.mark.parametrize`, aynı test mantığını farklı girdilerle tekrar çalıştırır. Böylece kopyala-yapıştır testler yerine okunabilir ve genişletilebilir bir senaryo tablosu elde edilir.

## Her sınır sayısal değildir

Sınırlar yalnızca yaş veya fiyat gibi sayılarda görülmez. Parola uzunluğu, dosya boyutu, liste kapasitesi, tarih aralığı ve API istek limiti de sınır üretir. Örneğin parola uzunluğu 8–20 karakterse 7, 8, 9, 19, 20 ve 21 karakterlik girdiler denenmelidir. Tarihlerde ay sonları, 29 Şubat ve yıl geçişleri özellikle değerlidir.

Çok değişkenli sistemlerde tüm sınır kombinasyonlarını denemek test sayısını hızla büyütür. Bu nedenle önce bir değişken sınırdayken diğerlerini normal değerlerde tutmak, ardından yalnızca iş açısından kritik kombinasyonları eklemek iyi bir dengedir. Özetle BVA, daha fazla test yazmak değil, **doğru noktalara test yerleştirmek** sanatıdır; çünkü hatalar da uçlarda yaşamayı sever.

---
layout: post
title: "Fuzzing ile Otomatik Zafiyet Keşfi: Yazılımı Rastgele Verilerle Sınamak"
math: true
categories: 
  - Bilgi
tags: 
  - fuzzing
  - siber güvenlik
  - zafiyet analizi
  - otomasyon
  - python
  - güvenli yazılım
toc: true
---

Bir uygulamanın beklenmedik girdiler karşısında nasıl davranacağını elle sınamak, samanlıkta iğne aramaya benzeyebilir. Fuzzing ise samanlığı otomatik olarak karıştırır: programa bozuk, sıra dışı veya rastgele girdiler gönderir; çökme, kilitlenme ve bellek ihlali gibi belirtileri yakalar. Böylece geliştiricilerin aklına gelmeyen uç durumlar, saldırganlardan önce keşfedilebilir.

``

## Fuzzing mantığı nedir?

Bir **fuzzer**, hedef yazılıma tekrar tekrar test girdileri verir ve sonuçları gözlemler. Örneğin resim işleyen bir uygulamaya hatalı başlık alanları, aşırı büyük boyut değerleri veya yarım bırakılmış dosyalar gönderilebilir. Hedef çökerse ilgili girdi kaydedilir ve hata yeniden üretilebilir.

Basitleştirilmiş süreç şöyledir:

1. Başlangıç girdileri hazırlanır.
2. Girdiler değiştirilir veya sıfırdan üretilir.
3. Hedef program çalıştırılır.
4. Çökme, zaman aşımı ve anormal davranışlar izlenir.
5. İlginç girdiler yeni testlerin tohumu yapılır.

Bir fuzzing kampanyasının kaba verimliliğini şu oranla düşünebiliriz:

$$
E = \frac{B}{T}
$$

Burada $B$ benzersiz davranış veya hata sayısını, $T$ ise toplam çalışma süresini temsil eder. Ancak yalnızca saniyedeki test sayısını artırmak yeterli değildir; yeni kod yollarına ulaşmak da önemlidir.

## Fuzzer türleri

| Yaklaşım | Girdi üretimi | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| Rastgele fuzzing | Tamamen rastgele | Kurulumu kolaydır | Geçerli format üretmekte zorlanır |
| Mutasyon tabanlı | Mevcut girdileri değiştirir | Gerçekçi dosyalara yakın kalır | İyi tohumlara ihtiyaç duyar |
| Üretim tabanlı | Format kurallarını kullanır | Karmaşık yapıları geçebilir | Model hazırlamak zahmetlidir |
| Kapsam güdümlü | Kod kapsamına göre yönlenir | Yeni yürütme yolları bulur | Enstrümantasyon gerektirebilir |

AFL++, libFuzzer ve honggfuzz gibi araçlar kapsam güdümlü yaklaşımı kullanır. Fuzzer, yeni bir dal keşfeden girdiyi değerli kabul eder. Teorik olarak amaç, ulaşılan program durumları kümesini büyütmektir:

$$
\max \vert S_{ulaşılan}\vert , \qquad S_{ulaşılan} \subseteq S_{tüm}
$$

## Küçük bir Python örneği

Aşağıdaki eğitim örneği, bir ayrıştırıcıyı farklı bayt dizileriyle çağırır. Gerçek güvenlik testleri yalnızca izin verilen sistemlerde yapılmalıdır.

```python
import os
import random

def parse_packet(data):
    # İlk dört bayt sihirli değer, beşinci bayt uzunluk olsun.
    if len(data) < 5:
        return False
    if data[:4] != b'PKT!':
        return False

    declared_length = data[4]
    payload = data[5:]
    if declared_length != len(payload):
        raise ValueError('Uzunluk alanı hatalı')
    return True

def fuzz(iterations=10_000):
    for test_id in range(iterations):
        size = random.randint(0, 32)
        sample = os.urandom(size)

        try:
            parse_packet(sample)
        except Exception as error:
            print(f'Hata #{test_id}: {sample.hex()} -> {error}')

fuzz()
```

Bu kod rastgele veri üretir, ayrıştırıcıya gönderir ve istisna oluşturan girdileri raporlar. Fakat tamamen rastgele girdilerin `PKT!` kontrolünü geçme olasılığı düşüktür. Dört belirli baytı rastgele tutturma olasılığı yaklaşık olarak

$$
P = \left(\frac{1}{256}\right)^4
$$

olduğundan, akıllı bir fuzzer geçerli örnekleri mutasyona uğratarak daha hızlı ilerler.

## Çökme bulmak neden yeterli değil?

Her çökme güvenlik açığı değildir; bazıları yalnızca zararsız bir hata mesajıdır. Bulunan girdiler küçültülmeli, yinelenen sonuçlar gruplanmalı ve kök neden analiz edilmelidir. AddressSanitizer gibi araçlar taşma ve use-after-free hatalarını görünür hâle getirir. Zaman aşımı takibi ise sonsuz döngüleri yakalayabilir.

Başarılı bir kampanya; kaliteli tohumlar, uygun zaman aşımı, bellek denetleyicileri ve sürekli çalışan otomasyon gerektirir. Fuzzing sihirli bir zafiyet dedektörü değil, sabırlı ve yorulmayan bir test robotudur. CI/CD hattına eklendiğinde her değişiklikten sonra aynı saldırgan merakını tekrar tekrar göstererek güvenli yazılım geliştirme sürecini güçlendirir.

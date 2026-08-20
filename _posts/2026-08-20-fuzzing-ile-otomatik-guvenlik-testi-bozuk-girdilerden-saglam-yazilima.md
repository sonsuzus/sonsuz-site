---
layout: post
title: "Fuzzing ile Otomatik Güvenlik Testi: Bozuk Girdilerden Sağlam Yazılıma"
math: true
categories: 
  - Bilgi
tags: 
  - fuzzing
  - siber güvenlik
  - yazılım testi
toc: true
---

Bir programın yalnızca beklenen kullanıcı davranışlarıyla çalışması, onun güvenli olduğu anlamına gelmez. Fuzzing; uygulamalara rastgele, sınır dışı, eksik veya biçimi bozulmuş girdiler göndererek çökme, beklenmeyen hata ve güvenlik açığı üreten davranışları bulmaya yarayan otomatik test yaklaşımıdır. Özellikle C/C++ gibi bellek yönetiminin geliştirici sorumluluğunda olduğu dillerde, görünmeyen köşe durumlarını yakalamak için son derece etkilidir.
``

## Fuzzing'in temel mantığı

Klasik birim testlerinde geliştirici, giriş ve beklenen çıktıyı çoğunlukla kendisi belirler. Fuzzing ise şu soruyu sorar: “Program, hiç düşünmediğim bir girdiyle karşılaşırsa ne yapacak?” Amaç yalnızca programı kapatmak değildir; çöküşün nedenini, tekrar üretilebilir girdiyi ve etkilenen kod yolunu bulmaktır.

Basit bir modelde toplam test uzayı şöyle düşünülebilir:

$$N = |A|^L$$

Burada $|A|$ kullanılabilecek karakter veya bayt sayısını, $L$ ise girdi uzunluğunu ifade eder. Örneğin 256 farklı bayttan oluşan yalnızca 10 baytlık bir alan için olası kombinasyon sayısı $256^{10}$ olur. Bu devasa uzay, saf rastgeleliğin neden her zaman yeterli olmadığını açıklar. Akıllı fuzzer'lar, yeni kod dallarına ulaşan girdileri saklayıp onların üzerinde değişiklik yaparak aramayı yönlendirir.

| Yaklaşım | Girdi üretimi | Güçlü yanı | Sınırlaması |
|---|---|---|---|
| Rastgele fuzzing | Tamamen rastgele baytlar | Hızlı başlangıç, basit kurulum | Derin mantık yollarına ulaşmak zor olabilir |
| Mutasyon tabanlı fuzzing | Mevcut örnekleri bozar | Dosya ayrıştırıcılarında çok etkilidir | İyi başlangıç örnekleri ister |
| Üretim tabanlı fuzzing | Biçim kurallarına göre üretir | Geçerli ve karmaşık girdiler sağlar | Gramer hazırlama maliyetlidir |
| Kapsama güdümlü fuzzing | Yeni dallara göre seçim yapar | Kod keşfinde verimlidir | Derleme ve araç entegrasyonu gerekebilir |

## Hedef seçimi ve corpus hazırlığı

İyi bir fuzzing kampanyası, küçük ve sınırları açık bir hedef fonksiyonla başlar. Örneğin bir JSON ayrıştırıcısının tüm sunucusunu çalıştırmak yerine, metni alan ve ayrıştıran fonksiyonu test etmek daha hızlı sonuç verir. Başlangıç girdileri kümesine *corpus* denir. Corpus; boş dosya, normal örnek, çok büyük alan, Unicode karakterleri ve biçimsel olarak geçerli farklı örnekler içermelidir.

Aşağıdaki Python örneği, bir metin ayrıştırıcısı için öğretici bir mutasyon döngüsü gösterir. Bu örnek üretim ortamı aracı değildir; temel fikri görünür kılar.

```python
import os
import random

seed = b'{"ad":"Ada","yas":24}'

def mutate(data: bytes) -> bytes:
    buffer = bytearray(data)
    if buffer and random.random() < 0.7:
        index = random.randrange(len(buffer))
        buffer[index] ^= random.randrange(1, 256)
    else:
        buffer.insert(random.randrange(len(buffer) + 1), random.randrange(256))
    return bytes(buffer)

def parse_profile(raw: bytes):
    # Gerçek hedef fonksiyon burada çağrılır.
    return raw.decode("utf-8")

for attempt in range(10_000):
    candidate = mutate(seed)
    try:
        parse_profile(candidate)
    except Exception as error:
        os.makedirs("crashes", exist_ok=True)
        with open(f"crashes/case-{attempt}.bin", "wb") as file:
            file.write(candidate)
        print("İlginç hata:", type(error).__name__)
```

## Çöküşten güvenlik bulgusuna

Her hata güvenlik açığı değildir. Örneğin kontrollü bir `ValueError`, çoğu zaman iyi yapılmış doğrulamanın işaretidir. Buna karşılık bellek taşması, kullanım sonrası bellek erişimi, sonsuz döngü veya kaynak tüketimi ciddi inceleme gerektirir. Dinamik analiz araçları bu noktada fuzzer'ın en iyi arkadaşlarıdır. AddressSanitizer bellek ihlallerini, UndefinedBehaviorSanitizer ise tanımsız davranışları yakalamaya yardımcı olur.

Risk değerlendirmesinde kabaca şu düşünce kullanılabilir:

$$Risk = Etki \times Olasılık$$

Bir çöküşün tekrar üretilebilir olması olasılığı artırır; uzaktan tetiklenebilmesi ve hassas veriye erişim potansiyeli ise etkiyi büyütür. Bulgu kaydında girdi dosyası, sürüm, çalıştırma komutu, hata çıktısı ve mümkünse küçültülmüş test örneği bulunmalıdır.

## Sağlıklı bir çalışma döngüsü

Fuzzing'i tek seferlik bir “hata avı” değil, sürekli entegrasyonun parçası olarak düşünün. Önce hedefi izole edin, corpus oluşturun, kapsama ve sanitizasyon ekleyin, sonra bulguları ayıklayın. Düzeltmeden sonra aynı çöküş girdisini regresyon testine dönüştürün. Böylece rastgele bozulmuş veriler, zamanla uygulamanızın en disiplinli kalite müfettişlerinden birine dönüşür.

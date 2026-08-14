---
layout: post
title: "Rastgele Sayı Üretimi: Bilgisayarlar Zar Atmayı Nasıl Taklit Eder?"
math: true
categories: 
  - Bilgi
tags: 
  - rastgelelik
  - PRNG
  - kriptografi
---

Bilgisayarlar son derece düzenli makinelerdir: aynı girdiye, aynı koşullarda daima aynı çıktıyı verirler. Bu yüzden ekranda “rastgele” görünen bir oyun zarı, şifreleme anahtarı ya da simülasyon sonucu aslında çoğu zaman dikkatle tasarlanmış bir algoritmanın ürünüdür. Bu algoritmalar, tahmin edilmesi zor ve istatistiksel olarak dengeli diziler üretmeye çalışır; fakat geçmişteki durumları bilen biri için sonuçlar teorik olarak yeniden üretilebilir.

``

Bu yaklaşımın adı **sözde rastgele sayı üretimi**dir (Pseudo-Random Number Generation, PRNG). Bir PRNG, küçük bir başlangıç bilgisi olan **tohum**u (*seed*) alır ve uzun bir sayı dizisi oluşturur. Aynı tohum verilirse aynı dizi yeniden elde edilir. Bu özellik, ilk bakışta kusur gibi görünse de hata ayıklama, bilimsel deneyleri tekrar etme ve oyun dünyasında aynı haritayı tekrar üretme açısından büyük avantajdır.

En temel örneklerden biri doğrusal eşlenik üreteçtir (*Linear Congruential Generator*, LCG):

$$X_{n+1} = (aX_n + c) \bmod m$$

Burada $X_n$ mevcut durum, $a$ çarpan, $c$ artış değeri ve $m$ modüldür. Üretilen sayı genellikle $0$ ile $1$ arasına $X_n / m$ ile ölçeklenir. Formül küçük, hızlı ve öğreticidir; ancak modern ihtiyaçlar için güvenli değildir. Parametreleri ve birkaç çıktıyı bilen bir saldırgan, sonraki değerleri tahmin edebilir.

| Özellik | Gerçek rastgelelik | Sözde rastgelelik |
|---|---|---|
| Kaynak | Fiziksel olaylar | Matematiksel algoritma |
| Tekrarlanabilirlik | Genellikle hayır | Aynı tohumla evet |
| Hız | Donanıma bağlıdır | Genellikle çok yüksektir |
| Kullanım alanı | Anahtar üretimi, bilimsel ölçüm | Oyunlar, simülasyonlar, testler |
| Tahmin edilebilirlik | İyi kaynakta çok düşüktür | Algoritmaya göre değişir |

Python’daki `random` modülü, Mersenne Twister adlı kaliteli bir genel amaçlı PRNG kullanır. Simülasyon ve oyun mantığı için oldukça başarılıdır. Aşağıdaki kod, sabit bir tohumla zar atışlarını her çalıştırmada aynı sırayla üretir:

```python
import random

random.seed(42)  # Deneyi tekrarlanabilir yapar
zarlar = [random.randint(1, 6) for _ in range(10)]
print(zarlar)

ortalama = sum(zarlar) / len(zarlar)
print(f"Ortalama: {ortalama:.2f}")
```

Buradaki `seed(42)`, üretecin başlangıç durumunu belirler. Test yazarken bu son derece kullanışlıdır: “Bazen hata veriyor” yerine herkesin aynı rastgele senaryoyu görmesini sağlarsınız. Fakat parola sıfırlama bağlantısı, oturum belirteci veya kripto para cüzdanı anahtarı üretirken bu modül kullanılmamalıdır.

Kriptografik senaryolarda **CSPRNG** (*Cryptographically Secure PRNG*) gerekir. Bu üreteçler, önceki çıktılar bilinse bile sonraki çıktının pratikte hesaplanamaması hedefiyle tasarlanır. Python’da doğru tercih `secrets` modülüdür:

```python
import secrets

# URL içinde güvenle taşınabilecek rastgele belirteç üretir
token = secrets.token_urlsafe(32)
print(token)
```

CSPRNG’ler çoğunlukla işletim sisteminin topladığı entropiden yararlanır: zamanlama farklılıkları, donanım olayları ve uygun sistemlerde fiziksel rastgelelik kaynakları bu havuza katkı sağlar. Burada amaç sadece sayıların “dağınık görünmesi” değil, saldırganın onları öngörememesidir.

Rastgeleliği değerlendirirken yalnızca birkaç farklı sayı görmek yeterli değildir. İyi bir dizide değerlerin dağılımı dengeli olmalı, ardışık değerler arasında anlamlı korelasyon bulunmamalı ve periyot yeterince uzun olmalıdır. Örneğin adil bir altı yüzlü zarda teorik ortalama $3.5$’tir; çok sayıda atış sonrası gözlenen ortalamanın bu değere yaklaşması beklenir. Yani rastgelelik, kaos değil; ölçülebilir istatistiksel özelliklere sahip kontrollü belirsizliktir.

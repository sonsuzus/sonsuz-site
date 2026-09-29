---
layout: post
title: "Kriptografik Rastgelelik: /dev/urandom Neden Hayat Kurtarır?"
math: true
categories: 
  - Bilgi
tags: 
  - kriptografi
  - linux
  - güvenlik
  - rastgelelik
  - dev-urandom
  - csprng
toc: true
image: /img/kriptografik-rastgelelik-devurandom-68.png
---

Bir parola sıfırlama bağlantısı, oturum belirteci veya şifreleme anahtarı üretirken “rastgele görünüyor” demek yeterli değildir. Çıktının, saldırganın bildiği tüm bilgiler ışığında bile tahmin edilememesi gerekir. İşte sıradan rastgele sayı üreteçleriyle kriptografik güvenli üreteçler arasındaki hayat kurtaran fark burada başlar.

``

## Rastgele görünen her şey rastgele değildir

Programlama dillerindeki klasik sözde rastgele sayı üreteçleri, yani PRNG'ler, küçük bir başlangıç değerinden (*seed*) uzun bir sayı dizisi üretir. Aynı algoritmaya aynı seed verilirse aynı dizi yeniden ortaya çıkar. Bu özellik oyunlar, simülasyonlar ve testler için harikadır; ancak güvenlik açısından mayın tarlasıdır.

Bir üretecin iç durumu $S_n$ ve sonraki çıktısı $X_n$ olsun:

$$S_{n+1}=f(S_n), \qquad X_n=g(S_n)$$

Saldırgan $S_n$ durumunu veya seed'i tahmin edebilirse geçmiş ya da gelecek çıktıları hesaplayabilir. Seed olarak yalnızca zaman damgası kullanıldığını düşünün. Saldırgan işlemin yaklaşık saatini biliyorsa milyarlarca ihtimal yerine birkaç bin olasılığı denemesi yeterli olabilir.

| Özellik | Sıradan PRNG | Kriptografik CSPRNG |
|---|---|---|
| Temel amaç | Hız ve istatistiksel dağılım | Tahmin edilemezlik |
| Aynı seed | Aynı sonuç dizisi | Aynı iç durumda yine deterministik |
| Durum tahminine direnç | Genellikle zayıf | Tasarım gereği güçlü |
| Kullanım alanı | Oyun, simülasyon, test | Anahtar, nonce, token, parola |
| Örnek | `Math.random()`, Python `random` | `getrandom()`, `secrets`, `/dev/urandom` |

## /dev/urandom ne yapar?

Linux çekirdeği; disk ve ağ olaylarının zamanlaması, donanım kesmeleri ve uygun sistemlerde işlemci tabanlı rastgelelik kaynakları gibi öngörülmesi zor girdileri toplar. Bu veriler bir entropi havuzunda karıştırılır. Çekirdek daha sonra kriptografik olarak güvenli bir üreteç aracılığıyla uygulamalara bayt sunar.

Buradaki “entropi”, belirsizliğin ölçüsüdür. Eşit olasılıklı $N$ seçenek için:

$$H=\log_2(N)$$

Örneğin ideal biçimde seçilmiş 256 bitlik bir anahtarın arama uzayı $2^{256}$ büyüklüğündedir. Fakat anahtarı zaman damgasından türetirseniz dosyanın uzunluğu 256 bit olsa bile gerçek belirsizlik çok daha düşük kalır. Başka bir deyişle, uzun anahtar otomatik olarak güçlü anahtar değildir.

`/dev/urandom`, çekirdeğin rastgelelik sistemi güvenli biçimde başlatıldıktan sonra pratik kriptografik kullanım için uygundur. Modern Linux uygulamalarında doğrudan dosyayı okumak yerine `getrandom()` sistem çağrısını kullanan yüksek seviyeli kütüphaneler tercih edilir. Böylece sistem henüz yeterince başlatılmamışsa güvenli davranış elde edilir.

## Doğru ve yanlış kullanım

Python'daki `random` modülü güvenlik için tasarlanmamıştır:

```python
import random

# Simülasyon için uygundur, erişim anahtarı için değildir.
token = random.getrandbits(128)
print(token)
```

Güvenli seçenek `secrets` modülüdür. Bu modül işletim sisteminin CSPRNG mekanizmasını kullanır:

```python
import secrets

# URL içinde güvenle taşınabilen, tahmin edilmesi zor bir token üretir.
token = secrets.token_urlsafe(32)
print(token)

# 256 bitlik ham anahtar malzemesi üretir.
key = secrets.token_bytes(32)
```

Benzer şekilde tarayıcı tarafında `Math.random()` yerine Web Crypto API kullanılmalıdır:

```javascript
const bytes = new Uint8Array(32);
crypto.getRandomValues(bytes);
console.log(bytes);
```

## /dev/random daha mı güvenli?

Geçmişte `/dev/random` azalan entropi tahmini nedeniyle bloklanırken `/dev/urandom` veri üretmeye devam ederdi. Bu durum, ikincisinin “daha zayıf” olduğu efsanesini doğurdu. Modern Linux çekirdeklerinde CSPRNG güvenli biçimde başlatıldıktan sonra genel amaçlı kriptografik kullanımda `/dev/urandom` doğru seçimdir; gereksiz bloklanma çoğu uygulamaya ek güvenlik sağlamaz.

Asıl kural basittir: Kendi rastgelelik algoritmanızı, seed düzeninizi veya “çok karmaşık” sayı karıştırıcınızı icat etmeyin. Anahtar ve token üretimini işletim sistemine ve denetlenmiş kriptografi kütüphanelerine bırakın. Çünkü saldırganın tahmin edemediği bir sayı, yalnızca rastgele görünen bir sayıdan çok daha değerlidir.

![kriptografik-rastgelelik-devurandom-68](/img/kriptografik-rastgelelik-devurandom-68.svg)


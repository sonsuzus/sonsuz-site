---
layout: post
title: "Diffie-Hellman Anahtar Değişimi: Açık Kanalda Ortak Sır Üretmek"
math: true
categories: 
  - Bilgi
tags: 
  - diffie-hellman
  - kriptografi
  - siber güvenlik
  - anahtar değişimi
  - python
toc: true
image: /img/diffie-hellman-anahtar-47.png
---

İnternet trafiğinin herkes tarafından dinlenebildiği bir ortamda iki kişinin aynı gizli anahtarı oluşturması ilk bakışta imkânsız görünür. Diffie-Hellman anahtar değişimi, parolayı veya anahtarı doğrudan göndermek yerine iki tarafın matematiksel işlemlerle aynı sırra ulaşmasını sağlar. Böylece pasif bir dinleyici bütün mesajları görse bile ortak anahtarı pratik sürede hesaplayamaz.
``
## Temel fikir: Anahtarı gönderme, birlikte üret

Diffie-Hellman algoritmasında taraflara geleneksel olarak Alice ve Bob adı verilir. Öncelikle açıkça paylaşılabilen iki sayı belirlenir:

- Büyük bir asal sayı: $p$
- Üreteç adı verilen sayı: $g$

Alice yalnızca kendisinin bildiği rastgele bir $a$, Bob ise gizli bir $b$ sayısı seçer. Ardından açık değerlerini hesaplarlar:

$$A = g^a \bmod p$$

$$B = g^b \bmod p$$

Alice, $A$ değerini Bob'a; Bob da $B$ değerini Alice'e gönderir. Bu mesajların dinlenmesi sorun değildir. Taraflar gelen değeri kendi gizli sayılarıyla işleyerek ortak anahtarı bulur:

$$K_A = B^a \bmod p$$

$$K_B = A^b \bmod p$$

İki sonuç eşittir çünkü:

$$B^a = (g^b)^a = g^{ab} = (g^a)^b = A^b \pmod p$$

| Bilgi | Alice | Bob | Dinleyici |
|---|---:|---:|---:|
| $p$ ve $g$ | Görür | Görür | Görür |
| $A$ ve $B$ | Görür | Görür | Görür |
| $a$ | Bilir | Bilmez | Bilmez |
| $b$ | Bilmez | Bilir | Bilmez |
| Ortak anahtar | Hesaplar | Hesaplar | Kolayca hesaplayamaz |

## Küçük sayılarla örnek

Eğitim amacıyla $p=23$ ve $g=5$ seçelim. Alice'in gizli sayısı $a=6$, Bob'unki ise $b=15$ olsun.

Alice şu açık değeri üretir:

$$A = 5^6 \bmod 23 = 8$$

Bob'un açık değeri şöyledir:

$$B = 5^{15} \bmod 23 = 19$$

Alice $19^6 \bmod 23$ işlemini, Bob ise $8^{15} \bmod 23$ işlemini yapar. İkisi de $K=2$ sonucuna ulaşır. Dinleyici 23, 5, 8 ve 19 sayılarını bilir; fakat gizli üsleri çıkarmak için ayrık logaritma problemini çözmek zorundadır.

## Python ile çalışma mantığı

Aşağıdaki kod, süreci küçük sayılarla canlandırır. Python'ın üç parametreli `pow` fonksiyonu modüler üs almayı büyük ara değerler oluşturmadan gerçekleştirir.

```python
from secrets import randbelow

p = 23
g = 5

# Her taraf kendi gizli sayısını seçer.
alice_private = randbelow(p - 2) + 1
bob_private = randbelow(p - 2) + 1

# Bunlar açık kanal üzerinden gönderilebilir.
alice_public = pow(g, alice_private, p)
bob_public = pow(g, bob_private, p)

# Taraflar aynı ortak sırra bağımsız biçimde ulaşır.
alice_secret = pow(bob_public, alice_private, p)
bob_secret = pow(alice_public, bob_private, p)

print(alice_secret, bob_secret)
assert alice_secret == bob_secret
```

Buradaki 23 sayısı gerçek güvenlik sağlamaz; olası gizli değerler kolayca denenebilir. Gerçek sistemlerde standartlaştırılmış çok büyük gruplar veya X25519 gibi eliptik eğri tabanlı modern seçenekler kullanılır. Elde edilen sayı da doğrudan şifreleme anahtarı yapılmaz; genellikle HKDF gibi bir anahtar türetme fonksiyonundan geçirilir.

## Dinleyici neden zorlanır?

$g^a \bmod p$ değerini hesaplamak kolaydır. Ancak yalnızca $g$, $p$ ve sonuç bilinirken $a$ değerini bulmak, uygun parametrelerde hesaplama açısından son derece pahalıdır. Güvenlik “matematiksel olarak asla çözülemez” anlamına gelmez; güncel bilgisayarlar ve doğru anahtar boyutları karşısında pratik olarak çözülemez demektir. Yeterince güçlü kuantum bilgisayarlar, Shor algoritmasıyla klasik Diffie-Hellman'ı tehdit edebilir.

## Kritik açık: Aktif araya girme saldırısı

Diffie-Hellman pasif dinlemeye dayanıklıdır, fakat tarafların kimliğini tek başına doğrulamaz. Mallory adlı saldırgan mesajları değiştirebiliyorsa Alice ve Bob ile ayrı anahtarlar oluşturup trafiği aktarabilir. Bu, ortadaki adam saldırısıdır.

| Tehdit | Saf Diffie-Hellman sonucu | Çözüm |
|---|---|---|
| Pasif trafik dinleme | Dayanıklı | Güçlü parametreler |
| Mesaj değiştirme | Savunmasız | Dijital imza veya sertifika |
| Eski anahtarın çalınması | Oturuma bağlı | Geçici anahtarlar, yani ECDHE |

Bu nedenle TLS, Diffie-Hellman değişimini sertifikalar ve dijital imzalarla doğrular. Özetle taraflar bir parolayı paylaşmaz; açık kanalda, yalnızca kendilerinin hesaplayabildiği ortak bir sır üretir. Diffie-Hellman'ın sihri de tam olarak anahtarı taşımadan anahtar üzerinde anlaşabilmesidir.

![diffie-hellman-anahtar-47](/img/diffie-hellman-anahtar-47.svg)


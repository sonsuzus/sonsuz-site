---
layout: post
title: "Kriptografide ECC: Küçük Anahtarların Büyük Matematiği"
math: true
categories: 
  - Bilgi
tags: 
  - kriptografi
  - eliptik-eğriler
  - siber-güvenlik
toc: true
---

Kriptografi dünyasında “daha büyük anahtar, daha güçlü güvenlik” düşüncesi her zaman geçerli değildir. Eliptik Eğri Kriptografisi (Elliptic Curve Cryptography veya ECC), zekice seçilmiş matematiksel yapılar sayesinde RSA gibi klasik açık anahtarlı yöntemlerle benzer güvenliği çok daha kısa anahtarlarla sunar. Böylece özellikle mobil cihazlarda, akıllı kartlarda ve IoT sistemlerinde daha az bellek, bant genişliği ve enerji tüketimi hedeflenir.
``
## Eliptik eğri nedir?

Adı uzay geometrisini çağrıştırsa da kriptografide kullanılan eliptik eğriler elips değildir. Sonlu bir alan üzerinde genellikle şu denkleme uyan noktalardan oluşurlar:

$$y^2 \equiv x^3 + ax + b \pmod p$$

Burada $p$ büyük bir asal sayı, $a$ ve $b$ ise eğrinin parametreleridir. Eğrinin tekil olmaması için şu koşul sağlanır:

$$4a^3 + 27b^2 \not\equiv 0 \pmod p$$

Eğri üzerindeki noktalar özel bir toplama işlemine sahiptir. Bir $P$ noktası kendisiyle tekrar tekrar toplandığında skaler çarpım elde edilir:

$$Q = kP$$

$P$ ve $k$ biliniyorsa $Q$ noktasını hesaplamak kolaydır. Buna karşılık yalnızca $P$ ve $Q$ bilindiğinde $k$ değerini bulmak pratikte son derece zordur. ECC’nin güvenliği, **Eliptik Eğri Ayrık Logaritma Problemi** adı verilen bu tek yönlü zorluğa dayanır.

## ECC neden kısa anahtar kullanabilir?

RSA’nın güvenliği büyük sayıların çarpanlarına ayrılmasının zorluğuna dayanır. Bu problem için geliştirilen algoritmalar nedeniyle güvenlik arttıkça RSA anahtarları hızla büyür. Eliptik eğri ayrık logaritması için bilinen genel saldırılar daha az verimli olduğundan ECC aynı güvenlik düzeyine daha küçük anahtarlarla ulaşabilir.

| Yaklaşık güvenlik düzeyi | RSA anahtarı | ECC anahtarı |
|---:|---:|---:|
| 80 bit | 1024 bit | 160 bit |
| 112 bit | 2048 bit | 224 bit |
| 128 bit | 3072 bit | 256 bit |
| 256 bit | 15360 bit | 512 bit |

Örneğin 256 bitlik modern bir eliptik eğri, yaklaşık 3072 bitlik RSA anahtarının sunduğu klasik güvenlik seviyesine yakındır. Küçük anahtarlar sertifikaları, imzaları ve ağ üzerinden taşınan verileri de küçültür.

## ECC tek bir algoritma değildir

ECC, farklı amaçlara hizmet eden bir algoritma ailesidir:

| Yöntem | Görev | Tipik kullanım |
|---|---|---|
| ECDH | Ortak sır üretme | TLS anahtar anlaşması |
| ECDSA | Dijital imza | Yazılım ve belge doğrulama |
| EdDSA | Hızlı, modern imza | SSH, uygulama protokolleri |
| ECIES | Hibrit şifreleme | Verinin alıcı anahtarıyla korunması |

ECC çoğunlukla büyük veriyi doğrudan şifrelemez. ECDH veya ECIES ile ortak bir simetrik anahtar oluşturulur; asıl veri AES ya da ChaCha20 gibi hızlı bir algoritmayla şifrelenir.

## Matematiği küçük sayılarla görelim

Aşağıdaki Python kodu, eğitim amacıyla küçük bir sonlu alanda iki eğri noktasını toplar. Gerçek sistemlerde sabit zamanlı ve denetlenmiş kriptografi kütüphaneleri kullanılmalıdır.

```python
P_MOD = 97
A = 2

# Eğri noktaları üzerinde P + Q işlemini hesaplar.
def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and (y1 + y2) % P_MOD == 0:
        return None  # Sonsuzdaki nokta

    if P != Q:
        slope = (y2 - y1) * pow(x2 - x1, -1, P_MOD)
    else:
        slope = (3 * x1 * x1 + A) * pow(2 * y1, -1, P_MOD)

    slope %= P_MOD
    x3 = (slope * slope - x1 - x2) % P_MOD
    y3 = (slope * (x1 - x3) - y1) % P_MOD
    return x3, y3

print(point_add((3, 6), (3, 6)))
```

Kod, modüler ters alma ve nokta ikiye katlama işlemlerini gösterir. Gerçek ECC uygulamalarındaki dev sayılar, yan kanal saldırıları ve nokta doğrulaması gibi ayrıntılar ise işi çok daha hassas hâle getirir.

## Hızlı ama sihirli değil

ECC genellikle anahtar üretimi, bant genişliği ve enerji tüketiminde avantajlıdır; ancak her işlemde RSA’dan mutlak biçimde hızlı olduğu söylenemez. Örneğin küçük açık üs kullanan RSA imza doğrulaması oldukça hızlı olabilir. Ayrıca ECC’nin güvenliği doğru eğri seçimine, güvenli rastgeleliğe ve hatasız uygulamaya bağlıdır.

Kuantum bilgisayarlar yeterince gelişirse Shor algoritması hem RSA’yı hem ECC’yi tehdit edecektir. Bugün içinse doğru standartlarla uygulanan ECC, küçük anahtarlarla güçlü güvenlik sunan ve modern internetin görünmez kahramanlarından biri olan son derece verimli bir araçtır.

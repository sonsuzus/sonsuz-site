---
layout: post
title: "RSA’nın Matematiği: Asal Sayılardan Açık Anahtarlı Şifrelemeye"
math: true
categories: 
  - Bilgi
tags: 
  - rsa
  - kriptografi
  - matematik
  - python
  - asal sayılar
  - bilgi güvenliği
toc: true
image: /img/rsanin-matematigi-asal-57.png
---

İnternette gönderdiğimiz bir mesajın, onu hiç tanımadığımız bir sunucu tarafından güvenle alınabilmesi ilk bakışta sihir gibi görünebilir. RSA, bu sihri modüler aritmetik ve büyük asal sayılarla gerçekleştirir. Adını geliştiricileri Rivest, Shamir ve Adleman’dan alan yöntem, şifreleme anahtarını herkese gösterebildiğimiz hâlde çözme anahtarını gizli tutabilmemizi sağlar.

![rsanin-matematigi-asal-57](/img/rsanin-matematigi-asal-57.svg)

``
## Açık anahtar fikri

Simetrik şifrelemede aynı gizli anahtar hem şifreleme hem çözme için kullanılır. RSA gibi asimetrik sistemlerde ise matematiksel olarak ilişkili iki farklı anahtar vardır:

| Özellik | Açık anahtar | Özel anahtar |
|---|---|---|
| Kim görebilir? | Herkes | Yalnızca sahibi |
| Temel bileşenler | $(n,e)$ | $(n,d)$ |
| Ana işlev | Şifreleme veya imza doğrulama | Çözme veya imzalama |
| Paylaşılması | Güvenlidir | Tehlikelidir |

Bu ayrımın arkasındaki fikir, yapılması kolay fakat tersine çevrilmesi çok zor bir işlem kullanmaktır. İki büyük asal sayıyı çarpmak hızlıdır; ortaya çıkan dev sayıyı asal çarpanlarına ayırmak ise bilinen klasik yöntemlerle oldukça pahalıdır.

## Anahtarlar nasıl üretilir?

Önce birbirinden farklı iki büyük asal sayı seçilir:

$$p \neq q$$

Ardından bu sayılar çarpılarak ortak modül hesaplanır:

$$n=pq$$

Euler’in totient fonksiyonu, $n$ ile aralarında asal olan pozitif tam sayıların miktarını verir. İki asalın çarpımı için sonuç şöyledir:

$$\varphi(n)=(p-1)(q-1)$$

Şimdi $1<e<\varphi(n)$ koşulunu sağlayan ve $\varphi(n)$ ile aralarında asal olan bir $e$ seçilir. Başka bir ifadeyle:

$$gcd(e,\varphi(n))=1$$

Özel üs $d$, $e$ sayısının $\varphi(n)$ modundaki çarpımsal tersidir:

$$ed \equiv 1 \pmod{\varphi(n)}$$

Böylece $(n,e)$ açık, $(n,d)$ ise özel anahtar olur. Gerçek sistemlerde $p$, $q$ ve $\varphi(n)$ değerleri de gizli tutulmalı veya güvenli biçimde yok edilmelidir.

## Şifreleme ve çözme

Mesaj önce $0 \leq m<n$ aralığında bir tam sayıya kodlanır. Şifreli metin $c$ şu işlemle üretilir:

$$c \equiv m^e \pmod n$$

Alıcı, özel anahtarıyla ters işlemi gerçekleştirir:

$$m \equiv c^d \pmod n$$

Bunun çalışmasını sağlayan temel dayanak Euler teoremidir. Uygun koşullarda $m^{\varphi(n)} \equiv 1 \pmod n$ olur. $ed=1+k\varphi(n)$ biçiminde yazılabildiğinden, $m^{ed}$ yeniden $m$ sonucuna ulaşır.

Küçük sayılarla çalışan aşağıdaki Python örneği süreci görünür kılar:

```python
# Öğretim amacıyla küçük asallar kullanıyoruz; bunlar güvenli değildir.
p, q = 61, 53
n = p * q
phi = (p - 1) * (q - 1)
e = 17

# pow(e, -1, phi), modüler çarpımsal tersi hesaplar.
d = pow(e, -1, phi)

message = 65
ciphertext = pow(message, e, n)   # Hızlı modüler üs alma
recovered = pow(ciphertext, d, n)

print("Açık anahtar:", (n, e))
print("Özel üs:", d)
print("Şifreli mesaj:", ciphertext)
print("Çözülen mesaj:", recovered)
```

Buradaki `pow(a, b, n)`, önce devasa $a^b$ değerini üretmek yerine modüler üs alma algoritması kullanır. Böylece işlem hem hızlı hem de bellek açısından verimli olur.

## Güvenlik gerçekten nereden gelir?

Bir saldırgan açık anahtardaki $n$ ve $e$ değerlerini bilir. Eğer $n$ sayısını $p$ ve $q$ çarpanlarına ayırabilirse $\varphi(n)$ değerini, ardından da $d$ özel üssünü hesaplayabilir. Yeterince büyük ve doğru üretilmiş asallar kullanıldığında bu ayrıştırma klasik bilgisayarlar için pratik olmaktan çıkar.

| Yaklaşım | Durum |
|---|---|
| Küçük asal sayılar | Saniyeler içinde kırılabilir |
| 2048 bit RSA | Günümüzde yaygın alt sınırdır |
| Kuantum bilgisayarda Shor algoritması | Yeterli ölçeğe ulaşırsa ciddi tehdittir |
| Hatalı rastgele sayı üretimi | Büyük anahtarı bile zayıflatabilir |

Son olarak, ders kitaplarındaki “çıplak RSA” gerçek uygulamalarda güvenli değildir. Şifreleme için OAEP, dijital imza için PSS gibi dolgulama şemaları kullanılmalıdır. Ayrıca RSA genellikle büyük dosyanın tamamını şifrelemez; rastgele üretilen simetrik oturum anahtarını korur. Kısacası matematik kaleyi kurar, doğru protokoller ise kapıların açık unutulmamasını sağlar.

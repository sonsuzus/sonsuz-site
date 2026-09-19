---
layout: post
title: "Homomorfik Şifreleme: Veriyi Görmeden Hesaplama Sanatı"
math: true
categories: 
  - Bilgi
tags: 
  - homomorfik şifreleme
  - kriptografi
  - veri güvenliği
  - gizlilik
  - bulut bilişim
  - python
toc: true
image: /img/homomorfik-sifreleme-veriyi-91.png
---

Bir bulut sunucusunun verilerinizi hiç görmeden maaş ortalaması hesapladığını, tıbbi kayıtlarınızı okumadan hastalık riski tahmin ettiğini düşünün. Kulağa sihir gibi gelse de homomorfik şifreleme tam olarak bunu hedefler: Veriler şifreli kalırken üzerlerinde matematiksel işlemler yapılabilir. Sunucu yalnızca anlamsız görünen şifreli değerlerle uğraşır; sonucu anlamlı hâle getirebilen tek taraf, gizli anahtarın sahibidir.

![homomorfik-sifreleme-veriyi-91](/img/homomorfik-sifreleme-veriyi-91.svg)

``
## Temel fikir nasıl çalışır?

Geleneksel şifrelemede veriyle işlem yapmak için önce veriyi çözmek gerekir. Bu sırada veri bellekte açık hâlde bulunduğundan saldırılara veya yetkisiz erişime açık olabilir. Homomorfik şifreleme ise hesaplamayı doğrudan şifreli uzaya taşır.

Bir şifreleme fonksiyonunu $E$, çözme fonksiyonunu $D$ ve uygulanacak işlemi $f$ ile gösterelim. İstenen özellik şudur:

$$D(f(E(x), E(y))) = f(x, y)$$

Buradaki eşitlik kavramsaldır; şifreli alanda uygulanan işlem, kullanılan sisteme göre normal toplama veya çarpmadan farklı olabilir. Örneğin toplamsal homomorfik bir sistemde:

$$D(E(x) \otimes E(y)) = x + y$$

Sunucu $x$ ve $y$ değerlerini öğrenmeden toplamı temsil eden yeni bir şifreli metin üretir. Gizli anahtara sahip kullanıcı bu sonucu çözdüğünde $x+y$ değerini elde eder.

| Yaklaşım | Şifreliyken işlem | Esneklik | Tipik kullanım |
|---|---|---:|---|
| Kısmi homomorfik | Yalnızca toplama veya çarpma | Düşük | Oy verme, toplam alma |
| Biraz homomorfik | Sınırlı sayıda farklı işlem | Orta | Basit istatistikler |
| Tam homomorfik | Keyfî toplama ve çarpma devreleri | Yüksek | Makine öğrenmesi, genel hesaplama |

## Neden toplama ve çarpma yeterli olabilir?

Bilgisayar programlarının önemli bir bölümü mantıksal veya aritmetik devreler olarak ifade edilebilir. Toplama ve çarpma işlemleri birlikte kullanıldığında polinomlar hesaplanabilir. Örneğin bir risk modeli şöyle olsun:

$$r(x)=3x^2+2x+5$$

Tam homomorfik şifreleme, $x$ değerini açmadan bu polinomu değerlendirebilir. Karşılaştırma, bölme ve üstel fonksiyonlar daha zordur; çoğu zaman bunların polinom yaklaşımları kullanılır. Yani sistem güçlüdür, fakat “normal kodu şifreli veriye aynen çalıştır” kadar zahmetsiz değildir.

## Oyuncak bir toplamsal örnek

Aşağıdaki Python kodu gerçek güvenlik sağlamaz; yalnızca homomorfik davranışın mantığını görünür kılar. Üretim ortamında Microsoft SEAL, OpenFHE veya TenSEAL gibi denetlenmiş kütüphaneler tercih edilmelidir.

```python
MOD = 10_000
SECRET = 1_337

def encrypt(value):
    # Değeri gizli bir kaydırmayla temsil eder.
    return (value + SECRET) % MOD

def add_encrypted(left, right):
    # İki şifreli değeri, eklenen iki sırrı düzelterek toplar.
    return (left + right - SECRET) % MOD

def decrypt(ciphertext):
    return (ciphertext - SECRET) % MOD

salary_a = encrypt(4000)
salary_b = encrypt(6000)
encrypted_total = add_encrypted(salary_a, salary_b)

print(decrypt(encrypted_total))  # 10000 yerine mod nedeniyle 0
```

Bu örnek yalnızca cebirsel ilişkiyi anlatır. Gerçek şemalarda rastgelelik, büyük asal sayılar, gürültü yönetimi ve karmaşık anahtar mekanizmaları bulunur. Ayrıca örnekteki küçük modül taşmaya yol açar; gerçek parametreler beklenen sayı aralığına göre seçilir.

## Gürültü ve performans meselesi

Modern homomorfik şemalar, güvenlik için şifreli metne kontrollü bir “gürültü” ekler. Her işlem gürültüyü büyütür. Gürültü belirli sınırı aşarsa sonuç doğru çözülemez. Tam homomorfik sistemlerde **bootstrapping** adı verilen işlem, şifreli metni yine şifreli biçimde yenileyerek hesaplamaya devam edilmesini sağlar. Ancak bu süreç zaman ve işlem gücü tüketir.

| Ölçüt | Açık veri hesabı | Homomorfik hesap |
|---|---:|---:|
| Hız | Çok yüksek | Görece düşük |
| Veri gizliliği | İşlem sırasında azalır | İşlem boyunca korunur |
| Bellek ihtiyacı | Düşük | Yüksek |
| Uygulama karmaşıklığı | Standart | Parametre seçimi gerektirir |

Homomorfik şifreleme özellikle sağlık, finans, güvenli oylama ve gizlilik odaklı yapay zekâ için heyecan vericidir. Henüz her sorguya serpilecek ucuz bir kriptografi baharatı değildir; fakat hassas verinin paylaşılmadan işlenmesi gerektiğinde son derece güçlü bir araçtır. Kısacası sunucu hesap makinesini kullanır, fakat ekrandaki sayıları asla göremez.

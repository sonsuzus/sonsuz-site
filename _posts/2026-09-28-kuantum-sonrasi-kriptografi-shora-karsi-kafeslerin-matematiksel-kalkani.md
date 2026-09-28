---
layout: post
title: "Kuantum Sonrası Kriptografi: Shor’a Karşı Kafeslerin Matematiksel Kalkanı"
math: true
categories: 
  - Bilgi
tags: 
  - kuantum
  - kriptografi
  - post-kuantum
  - shor-algoritması
  - kafes-kriptografisi
  - ml-kem
toc: true
image: /img/kuantum-sonrasi-kriptografi-36.png
---

İnternetin güvenliği bugün büyük ölçüde çarpanlara ayırma ve ayrık logaritma gibi klasik bilgisayarlar için zor problemlere dayanıyor. Yeterince güçlü, hata düzeltmeli bir kuantum bilgisayarı ise Shor algoritmasıyla bu temeli sarsabilir. Neyse ki kriptograflar boş durmuyor: kafes tabanlı sistemler, kuantum çağının dijital surları olmaya hazırlanıyor.
``

## RSA neden tehlikede?

RSA’da açık anahtar, iki büyük asalın çarpımı olan $N=pq$ modülünü içerir. Şifreleme basitleştirilmiş biçimde

$$c=m^e \bmod N$$

olarak gösterilir. Gizli anahtarı çıkarmak için $N$ sayısının çarpanlarına ayrılması gerekir. Klasik bilgisayarlarda bilinen en iyi genel yöntemler büyük anahtarlar için son derece pahalıdır.

Shor algoritması doğrudan “asal çarpanları tahmin etmez.” Bunun yerine modüler bir fonksiyonun periyodunu kuantum Fourier dönüşümüyle bulur. Bulunan periyot, çarpanların hesaplanmasını mümkün kılar. Teorik karmaşıklık polinomiktir; dolayısıyla yeterli sayıda güvenilir mantıksal kübite sahip gelecekteki makineler RSA ve eliptik eğri kriptografisini kırabilir. “Saniyeler içinde” ifadesi dramatiktir: günümüzde bunu gerçekleştirecek ölçekli, hata düzeltmeli kuantum bilgisayarları henüz yoktur.

| Sistem | Dayandığı zor problem | Shor’a karşı durum |
|---|---|---|
| RSA | Tam sayı çarpanlarına ayırma | Savunmasız |
| ECC | Eliptik eğride ayrık logaritma | Savunmasız |
| AES-256 | Simetrik anahtar arama | Uygun anahtar boyuyla güçlü |
| Kafes tabanlı KEM | LWE, Module-LWE | Bilinen saldırılara karşı dirençli |

![kuantum-sonrasi-kriptografi-36](/img/kuantum-sonrasi-kriptografi-36.svg)


## Kafes nedir?

Matematiksel kafes, seçilen baz vektörlerinin tam sayı katsayılı birleşimlerinden oluşan düzenli bir nokta kümesidir:

$$L(B)=\{Bz : z \in Z^n\}$$

İki boyutta kareli kâğıt gibi görünür; yüzlerce boyutta ise sezgilerimiz bavulunu toplayıp gider. Kriptografik güvenlik tam da bu yüksek boyutlu geometriden yararlanır. Örneğin En Kısa Vektör Problemi, kafesteki sıfırdan farklı en kısa vektörü bulmayı ister. Boyut büyüdükçe bu problem bilinen klasik ve kuantum yöntemleri için çok zorlaşır.

### LWE: Gürültünün faydalı olduğu an

Learning With Errors, gizli bir $s$ vektörü için şu örnekleri kullanır:

$$b=As+e \bmod q$$

Burada $A$ açık ve rastgele bir matris, $e$ ise küçük bir hata vektörüdür. Gürültü bulunmasaydı doğrusal denklem sistemi çözülerek $s$ kolayca elde edilirdi. Küçük hatalar eklendiğinde saldırgan, yüksek boyutlu kafeste zor bir yakın vektör problemiyle karşılaşır. Yetkili taraf ise anahtar yapısı ve hata sınırları sayesinde doğru ortak sırrı uzlaştırabilir.

| Özellik | RSA | Kafes tabanlı yaklaşım |
|---|---|---|
| Temel matematik | Sayılar teorisi | Yüksek boyutlu geometri |
| Kuantum tehdidi | Shor ile doğrudan | Etkili Shor benzeri çözüm bilinmiyor |
| Anahtar boyutu | Görece küçük | Genellikle daha büyük |
| İşlem yapısı | Büyük üs alma | Matris, polinom ve modüler aritmetik |

## ML-KEM ile ortak sır üretmek

NIST tarafından standartlaştırılan ML-KEM, eski adıyla CRYSTALS-Kyber, Module-LWE ailesine dayanır. Bir KEM doğrudan mesaj şifrelemek yerine iki tarafın ortak bir simetrik anahtar oluşturmasını sağlar. Mesajlar daha sonra AES-GCM gibi hızlı bir algoritmayla korunur.

Aşağıdaki Python benzeri örnek iş akışını gösterir:

```python
public_key, secret_key = ml_kem.keygen()

ciphertext, alice_secret = ml_kem.encapsulate(public_key)
bob_secret = ml_kem.decapsulate(secret_key, ciphertext)

assert alice_secret == bob_secret
```

`encapsulate`, açık anahtarla bir şifreli kapsül ve ortak sır üretir. `decapsulate` ise gizli anahtarı kullanarak aynı sırrı geri kazanır. Gerçek uygulamalarda doğrulanmış kütüphaneler kullanılmalı; kafes matematiğini evde karıştırmak, roket yakıtını mutfakta hazırlamaya benzer.

## Geçiş neden şimdiden başlamalı?

Saldırganlar bugün şifreli trafiği kaydedip gelecekte kuantum bilgisayarıyla çözebilir. Bu risk “şimdi topla, sonra çöz” olarak bilinir. Uzun süre gizli kalması gereken sağlık, devlet veya finans verileri özellikle tehlikededir.

Geçiş yalnızca algoritma değiştirmek değildir. Sertifikalar, protokoller, donanımlar ve anahtar yönetimi güncellenmelidir. Klasik ve post-kuantum algoritmalarını birlikte kullanan hibrit düzenler, geçiş döneminde güvenli bir köprü sunar. Kuantum fırtınası henüz ufukta olabilir; fakat dijital şemsiyeyi yağmur başladıktan sonra açmak pek iyi bir kriptografi stratejisi değildir.

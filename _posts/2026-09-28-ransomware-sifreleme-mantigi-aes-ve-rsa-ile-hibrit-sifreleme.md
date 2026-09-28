---
layout: post
title: "Ransomware Şifreleme Mantığı: AES ve RSA ile Hibrit Şifreleme"
math: true
categories: 
  - Bilgi
tags: 
  - ransomware
  - siber güvenlik
  - aes
  - rsa
  - kriptografi
  - hibrit şifreleme
toc: true
image: /img/ransomware-sifreleme-mantigi-50.png
---

Fidye yazılımlarının en kritik özelliği, kurbanın dosyalarını kısa sürede kullanılamaz hâle getirirken çözme anahtarını saldırgandan başka kimsenin erişemeyeceği biçimde saklamasıdır. Bunu yalnızca RSA veya yalnızca AES kullanarak yapmak yerine, iki algoritmanın güçlü yönlerini birleştiren **hibrit şifreleme** yaklaşımından yararlanırlar. Aynı yöntem HTTPS, e-posta güvenliği ve bulut sistemleri gibi meşru teknolojilerde de kullanılır; kötü niyetli olan matematik değil, kullanım amacıdır.

``

## Neden tek bir algoritma yeterli değil?

**AES**, simetrik bir şifreleme algoritmasıdır: Veriyi şifrelemek ve çözmek için aynı gizli anahtar kullanılır. Büyük dosyalarda son derece hızlıdır. Fakat anahtar dosyaların yanında bırakılırsa şifreleme anlamsızlaşır; anahtar uzaktaki bir sunucuya gönderilmeye çalışılırsa ağ bağlantısı ve operasyonel güvenlik sorunları ortaya çıkar.

**RSA** ise biri açık, diğeri özel olmak üzere bir anahtar çifti kullanır. Açık anahtarla korunan bilgi yalnızca özel anahtarla çözülebilir. Ancak RSA, gigabaytlarca dosyayı doğrudan şifrelemek için hem yavaş hem de uygun değildir. Ayrıca şifrelenebilecek mesaj boyutu anahtar uzunluğu ve dolgu şemasına bağlı olarak sınırlıdır.

| Özellik | AES | RSA |
|---|---|---|
| Tür | Simetrik | Asimetrik |
| Performans | Çok hızlı | Görece yavaş |
| Uygun kullanım | Dosya ve veri şifreleme | Anahtar koruma, imza |
| Anahtar yapısı | Tek gizli anahtar | Açık ve özel anahtar |
| Tipik seçenek | AES-256-GCM | RSA-2048/3072-OAEP |

![ransomware-sifreleme-mantigi-50](/img/ransomware-sifreleme-mantigi-50.svg)


## Hibrit sistemin çalışma zinciri

Genel model, **zarf şifreleme** olarak da bilinir. Önce kriptografik olarak güvenli rastgele bir AES anahtarı $K$ üretilir. Dosya verisi $M$, bu anahtar ve benzersiz bir nonce $N$ kullanılarak şifrelenir:

$$C, T = \operatorname{AES\text{-}GCM\_Enc}(K, N, M)$$

Burada $C$ şifreli veri, $T$ ise verinin değiştirilip değiştirilmediğini doğrulayan kimlik doğrulama etiketidir. Ardından AES anahtarı, saldırganın önceden oluşturduğu RSA açık anahtarı $PK$ ile korunur:

$$E_K = \operatorname{RSA\text{-}OAEP\_Enc}(PK, K)$$

Diskte genellikle şifreli dosya, RSA ile sarılmış anahtar, nonce ve doğrulama etiketi kalır. RSA özel anahtarı $SK$ cihazda bulunmadığından, sistemi inceleyen kişi AES anahtarını kolayca elde edemez. Teorik çözme sırası önce $K = \operatorname{RSA\text{-}OAEP\_Dec}(SK, E_K)$, ardından AES-GCM çözme işlemidir.

Aşağıdaki zararsız örnek, yalnızca bellekteki sabit bir mesaj üzerinde kavramı gösteren sözde koddur; dosya sistemi işlemi içermez:

```python
# Kavramsal gösterim: gerçek bir kripto API'sinin birebir sözdizimi değildir.
message = b"ornek veri"
aes_key = secure_random_bytes(32)       # 256 bit geçici anahtar
nonce = secure_random_bytes(12)         # GCM için benzersiz değer

ciphertext, tag = aes_gcm_encrypt(aes_key, nonce, message)
wrapped_key = rsa_oaep_encrypt(public_key, aes_key)

package = {
    "ciphertext": ciphertext,
    "wrapped_key": wrapped_key,
    "nonce": nonce,
    "tag": tag
}
```

Buradaki püf noktası hız ve anahtar yönetimidir: Ağır işi AES yapar, RSA ise yalnızca 32 baytlık AES anahtarını korur. Böylece performans ile asimetrik güvenlik aynı pakette buluşur.

## Savunma açısından ne ifade eder?

Güçlü ve doğru uygulanmış şifrelemeyi kaba kuvvetle kırmak pratik değildir. AES-256 için anahtar uzayı $2^{256}$ büyüklüğündedir. Bu nedenle savunma, algoritmayı kırmaya değil saldırıyı önlemeye ve etkisini azaltmaya odaklanmalıdır.

- **Çevrimdışı ve değiştirilemez yedekler** tutun; geri yüklemeyi düzenli olarak test edin.
- Uç nokta davranışlarını izleyerek kısa sürede gerçekleşen yoğun dosya değişikliklerini yakalayın.
- Makro, betik ve uygulama çalıştırma politikalarını sınırlandırın.
- Ağ segmentasyonu ve en az ayrıcalık ilkesiyle yayılma alanını daraltın.
- Olay sırasında cihazı ağdan ayırın, kanıtları koruyun ve uzman desteği alın.

Sonuç olarak hibrit şifreleme, kendi başına kötü bir teknoloji değildir. Fidye yazılımları, modern kriptografinin hız ve anahtar güvenliği avantajlarını kötüye kullanır. Mekanizmayı anlamak ise sihir perdesini kaldırır ve savunma planlarının neden yedekleme, erken tespit ve erişim kontrolü etrafında kurulması gerektiğini açıkça gösterir.

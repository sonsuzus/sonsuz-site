---
layout: post
title: "Akıllı Kilitlerde Güvenli Uzaktan Açma: Kimlik Doğrulama ve Şifreleme"
math: true
categories: 
  - Bilgi
tags: 
  - akıllı kilit
  - siber güvenlik
  - kimlik doğrulama
  - şifreleme
  - iot
  - hmac
toc: true
image: /img/akilli-kilitlerde-guvenli-79.png
---

Telefonunuzdaki düğmeye dokunduğunuzda kilometrelerce uzaktaki bir kapının açılması sihir gibi görünebilir. Oysa perde arkasında cihaz kimliği, kriptografik anahtarlar, zaman damgaları ve tek kullanımlık mesajlar birlikte çalışır. Amaç yalnızca doğru komutu kilide ulaştırmak değil; komutun gerçekten yetkili kişiden geldiğini, değiştirilmediğini ve daha önce kullanılmış bir kaydın tekrarı olmadığını kanıtlamaktır.

``

## Uzaktan açma isteği nasıl ilerler?

Tipik bir sistemde telefon doğrudan kilide bağlanmak yerine üreticinin sunucusuyla haberleşir. Kullanıcı önce parola, biyometri veya geçiş anahtarıyla oturum açar. Sunucu kullanıcının ilgili kapıyı açma yetkisini denetler ve kilide imzalanmış bir komut gönderir. Kilit, komutun doğruluğunu kendi içindeki güvenli anahtarla kontrol ettikten sonra motoru çalıştırır.

Bu süreç üç temel soruya cevap vermelidir:

1. **Kim gönderdi?** Kimlik doğrulama bunu belirler.
2. **Mesaj değiştirildi mi?** Bütünlük kontrolü bunu gösterir.
3. **İçeriği başkası okuyabilir mi?** Şifreleme gizliliği sağlar.

Kimlik doğrulama ile yetkilendirme aynı şey değildir. Kimlik doğrulama, “Bu kişi Ayşe mi?” sorusunu; yetkilendirme ise “Ayşe bu kapıyı şu anda açabilir mi?” sorusunu cevaplar. Örneğin temizlik görevlisinin hesabı gerçek olabilir, fakat erişimi yalnızca 09.00–11.00 arasında geçerli olabilir.

## Şifreleme hangi katmanlarda kullanılır?

Telefon, sunucu ve kilit arasındaki ağ trafiği genellikle TLS ile korunur. Böylece ortak Wi-Fi ağındaki saldırgan komutu okuyamaz veya değiştiremez. Ancak yalnızca bağlantı şifrelemesine güvenmek yeterli değildir. Açma komutunun ayrıca dijital imza ya da HMAC ile doğrulanması, aradaki sunucu veya ağ katmanlarına karşı ek güvence sağlar.

| Yöntem | Temel amacı | Akıllı kilitte örnek |
|---|---|---|
| AES | Veriyi gizlemek | Yerel kayıtları şifrelemek |
| HMAC | Kaynak ve bütünlüğü doğrulamak | Açma komutunu onaylamak |
| Dijital imza | Özel anahtar sahibini kanıtlamak | Sunucunun komut imzalaması |
| TLS | İletişim kanalını korumak | Telefon-sunucu bağlantısı |

HMAC kabaca şu şekilde ifade edilir:

$$HMAC(K,m)=H((K'\oplus opad)\parallel H((K'\oplus ipad)\parallel m))$$

Burada $K$ gizli anahtar, $m$ ise mesajdır. Anahtarı bilmeyen saldırgan geçerli doğrulama kodunu pratikte üretemez.

## Tekrar saldırısı neden tehlikelidir?

Bir saldırgan şifreli paketi okuyamasa bile paketi kaydedip daha sonra yeniden gönderebilir. Buna **replay saldırısı** denir. Savunma için her isteğe rastgele bir `nonce`, kısa son kullanma süresi ve benzersiz işlem kimliği eklenir. Kilit daha önce gördüğü nonce değerlerini reddeder.

```python
import hmac, hashlib, time, secrets

key = b"cihaz-icin-gizli-anahtar"
nonce = secrets.token_hex(16)
expires = int(time.time()) + 30
message = f"OPEN|front-door|{nonce}|{expires}".encode()
signature = hmac.new(key, message, hashlib.sha256).hexdigest()
```

Bu örnek, kapı kimliğiyle birlikte rastgele nonce ve 30 saniyelik geçerlilik süresi içeren bir mesaj üretir. HMAC, mesajın değiştirilip değiştirilmediğini denetlemeyi sağlar. Gerçek bir üründe anahtar kaynak koda yazılmaz; secure element, TPM benzeri güvenli donanım veya işletim sisteminin anahtar kasasında tutulur.

256 bitlik ideal bir anahtarı rastgele tahmin etmenin tek denemedeki başarı olasılığı $1/2^{256}$ seviyesindedir. Fakat güçlü matematik, kötü anahtar yönetimini kurtaramaz. Aynı anahtarın bütün kilitlerde kullanılması, güncelleme imzalarının doğrulanmaması veya hata ayıklama portlarının açık bırakılması sistemi savunmasız yapabilir.

## Güvenli tasarımın tamamlayıcı parçaları

Akıllı kilit güvenliği; çok faktörlü kimlik doğrulama, erişim süresi sınırları, başarısız denemelerde hız kısıtlama, imzalı yazılım güncellemeleri ve denetlenebilir olay kayıtlarıyla tamamlanır. İnternet kesildiğinde sistemin nasıl davranacağı da önceden belirlenmelidir. Acil çıkış güvenliği korunurken dışarıdan yetkisiz girişe izin verilmemelidir.

Kısacası güvenli bir akıllı kilit, sadece “şifreli bağlantı kullanan motorlu kapı” değildir. Kimlik, yetki, mesaj bütünlüğü, anahtar saklama ve fiziksel güvenlik birlikte tasarlandığında uzaktan açma işlemi hem kullanışlı hem de güvenilir hale gelir.

![akilli-kilitlerde-guvenli-79](/img/akilli-kilitlerde-guvenli-79.svg)


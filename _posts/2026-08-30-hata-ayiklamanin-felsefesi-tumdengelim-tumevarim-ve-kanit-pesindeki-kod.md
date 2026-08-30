---
layout: post
title: "Hata Ayıklamanın Felsefesi: Tümdengelim, Tümevarım ve Kanıt Peşindeki Kod"
math: true
categories: 
  - Bilgi
tags: 
  - debugging
  - yazılım felsefesi
  - mantık
  - hata ayıklama
---

Hata ayıklama, ekrana birkaç `console.log` serpiştirmekten çok daha fazlasıdır: Belirsizlik altında kanıt toplama sanatıdır. Bir program beklenmedik davrandığında geliştirici aslında küçük bir dedektiflik soruşturması yürütür. Elinde semptomlar, varsayımlar, loglar ve çoğu zaman da “ama benim bilgisayarımda çalışıyor” cümlesinin bıraktığı metafizik sis vardır.

``

Bu sürecin merkezinde klasik mantığın iki güçlü aracı bulunur: **tümdengelim** ve **tümevarım**. Tümdengelim, genel bir kuraldan özel bir sonuca iner. Örneğin “Kimlik doğrulama katmanı geçersiz token’ları reddeder” kuralı doğruysa ve istek 401 dönüyorsa, token ya geçersizdir ya da katman token’ı geçersiz olarak görüyordur. Tümevarım ise tekil gözlemlerden genel bir açıklama üretir: Üç farklı kullanıcıda hata yalnızca Türkçe karakter içeren e-postalarda oluşuyorsa, karakter kodlaması veya doğrulama regex’i şüpheli hale gelir.

| Mantık biçimi | Başlangıç noktası | Debugging’de kullanım | Temel risk |
|---|---|---|---|
| Tümdengelim | Kural veya değişmez | Beklenen davranışı sınamak | Başlangıç kuralı yanlış olabilir |
| Tümevarım | Gözlem ve örnekler | Desen, korelasyon bulmak | Korelasyonu neden sanmak |
| Yanlışlama | Hipotez | Hipotezi çürütecek test tasarlamak | Yetersiz test kapsamı |

Tümdengelimci bir hata ayıklama oturumunda sistemin sözleşmelerini yazarsınız. Bir fonksiyonun girdisi, çıktısı ve yan etkileri nettir. Örneğin toplamın negatif olamayacağı bir sepet modelinde şu değişmez geçerlidir:

$$total = \sum_{i=1}^{n}(price_i \times quantity_i), \qquad total \geq 0$$

Eğer `total` negatifse, matematik bize hatanın hesaplama zincirinde olduğunu söyler; ama hangi halkada olduğunu söylemez. İşte burada tümevarım devreye girer: Farklı sepetler, indirimler ve iade senaryoları denenir. Hata yalnızca iade miktarı stoktan büyük olduğunda görünüyorsa, yeni bir hipotez doğar: miktar doğrulaması işlemden sonra yapılıyordur.

```javascript
function applyRefund(cart, refundAmount) {
  const nextTotal = cart.total - refundAmount;

  if (refundAmount < 0 || refundAmount > cart.total) {
    throw new Error("Geçersiz iade tutarı");
  }

  return { ...cart, total: nextTotal };
}
```

Bu örnekte doğrulama, sonucu üretmeden önce yapılır. Kod basit görünür; ancak felsefi açıdan önemli olan şudur: Fonksiyon, geçersiz dünyanın oluşmasına izin vermez. Hata ayıklamanın ideal hedefi sadece hatayı bulmak değil, hatanın temsil edilemeyeceği tasarımlar kurmaktır.

Yine de gözlem, kanıtla aynı şey değildir. “Bu satırdan sonra uygulama çöktü” ifadesi, o satırın suçlu olduğunu kanıtlamaz; yalnızca soruşturma alanını daraltır. Özellikle asenkron sistemlerde neden-sonuç ilişkisi zaman içinde dağılır. Bu yüzden loglara bağlam eklemek gerekir: istek kimliği, kullanıcı kimliği, zaman damgası ve ilgili durum bilgisi. İyi bir log, “bir şey oldu” demez; “hangi koşulda, hangi veriyle, hangi sırada oldu?” diye cevap verir.

Pratikte en verimli yaklaşım, iki mantık biçimini dönüşümlü kullanmaktır. Önce tümevarımla anomalinin desenini çıkarın: Hata hangi ortamda, hangi girdide, ne sıklıkta oluşuyor? Ardından tümdengelimle değişmezleri kontrol edin: Bu noktaya gelene kadar hangi kurallar mutlaka doğru olmalıydı? Sonra hipotezinizi çürütmeye çalışın. Hipoteziniz çürümüyorsa güven kazanır; çürülüyorsa yeni bir bilgi kazanırsınız. Her iki sonuç da ilerlemedir.

Unutmayın: Debugging’de amaç ilk makul açıklamayı bulmak değildir. Amaç, alternatif açıklamaları sistematik olarak eleyip en iyi kanıtlanan açıklamaya ulaşmaktır. Kodun hatası çoğu zaman mantığın yenilgisi değil; eksik varsayımların görünür hale gelmesidir.

---
layout: post
title: "Üstbilişle Debugging: Kodunuzu Değil, Düşünme Biçiminizi İzleyin"
math: true
categories: 
  - Bilgi
tags: 
  - üstbiliş
  - debugging
  - hata çözümü
toc: true
---

Bir hata ayıklama oturumunda en pahalı kaynak çoğu zaman CPU, IDE ya da kahve değildir: dikkatimizdir. Üstbiliş (metacognition), kendi düşünme sürecimizi gözlemleme ve gerektiğinde yönlendirme becerisidir. Yazılımcı için bu, sadece “bu kod neden çalışmıyor?” sorusunu sormak değil; “Ben bu hatanın sebebi hakkında neden böyle düşünüyorum, hangi varsayımı test ettim ve hangisini kanıt sanıyorum?” diye de sormaktır. Bu ikinci soru, özellikle inatçı mantık hatalarında oyunun kurallarını değiştirir.
``
## Hata çözümünde iki katmanlı düşünme

Normal problem çözme birinci katmandır: değişkenleri inceler, log ekler, test çalıştırır ve hipotez üretiriz. Üstbiliş ise ikinci katmandır: kullandığımız hipotez üretme yöntemini denetleriz. Örneğin “Sorun kesinlikle API'de” cümlesi teknik bir bulgudan çok, henüz sınanmamış bir zihinsel ankordur.

Hata ayıklama süresini kabaca şöyle modelleyebiliriz:

$$T_{çözüm} = T_{arama} + T_{doğrulama} + T_{yanlış\_iz}$$

Üstbiliş, her zaman ilk iki terimi azaltmaz; fakat yanlış izlerde geçirilen $T_{yanlış\_iz}$ süresini dramatik biçimde düşürür. Çünkü geliştirici, bir varsayıma duygusal olarak bağlandığını erken fark eder ve kanıt aramak yerine varsayımı çürütmeye çalışır.

| Alışkanlık | Otomatik yaklaşım | Üstbilişsel yaklaşım |
|---|---|---|
| İlk tahmin | “Muhtemelen null değer.” | “Null hipotezim; bunu destekleyen gözlem ne?” |
| Log okuma | Beklenen hatayı arar. | Beklenmeyen veriyi özellikle arar. |
| Test sonucu | Başarısız testi tekrar çalıştırır. | Testin hangi varsayımı ayırdığını sorar. |
| Çözüm sonrası | “Düzeldi.” der. | “Kök neden neydi, sinyal neydi?” diye not alır. |

## Varsayımı görünür hâle getirin

Mantıksal hatalar çoğu zaman sözdizimi hatalarından daha sinsidir. Kod çalışır, hatta çoğu veriyle doğru sonuç verir; yalnızca sınır durumunda yanlış davranır. Bunun temel nedeni, zihnimizin eksik bilgiyi hızlıca tamamlamasıdır. Bu yüzden düşünceyi dışsallaştırmak gerekir: hipotezinizi, beklenen sonucu ve onu yanlışlayacak veriyi yazın.

Aşağıdaki örnekte geliştirici, indirim oranının yüzde olarak geldiğini varsaymıştır; fakat fonksiyon ondalık oran beklemektedir:

```javascript
function finalPrice(price, discountRate) {
  return price * (1 - discountRate);
}

const total = finalPrice(1000, 20);
console.log(total); // -19000: çalışıyor ama mantıksal olarak yanlış
```

Burada yalnızca `discountRate / 100` eklemek yeterli görünür. Fakat üstbilişsel soru şudur: “Bu parametrenin birimi nerede tanımlandı?” Sorun fonksiyonda değil, belirsiz sözleşmededir. Daha sağlam çözüm, isimlendirme ve doğrulama ile varsayımı kodun içine taşımaktır:

```javascript
function finalPrice(price, discountPercent) {
  if (discountPercent < 0 || discountPercent > 100) {
    throw new RangeError("İndirim 0 ile 100 arasında olmalı");
  }
  return price * (1 - discountPercent / 100);
}
```

Bu kodun yaptığı iş yalnızca hesaplama değildir; gelecekteki zihinsel hatalara karşı bir sınır koymaktır.

## Kısa bir üstbiliş rutini

Bir bug ile karşılaştığınızda şu sırayı deneyin:

1. **Gözlemi ayırın:** Kesin olarak ne oldu? Yorum eklemeyin.
2. **Varsayımı yazın:** Hatanın nedeni olduğuna ne inanıyorsunuz?
3. **Karşı kanıt isteyin:** Bu hipotez yanlışsa hangi çıktı görünürdü?
4. **En küçük testi kurun:** Tek seferde yalnızca bir varsayımı sınayın.
5. **Kararı kaydedin:** Hipotez doğrulandı mı, çürütüldü mü?

Bu yaklaşımın özünde Bayesçi güncelleme fikri vardır. Başlangıç inancınız $P(H)$ olsun; yeni kanıt $E$ geldikçe hipotezin olasılığını güncellersiniz:

$$P(H\vert E) = \frac{P(E\vert H)P(H)}{P(E)}$$

Elbette debug sırasında elle olasılık hesaplamazsınız. Fakat zihinsel model değerlidir: İlk fikriniz hüküm değil, güncellenebilir bir önceliktir. Kısacası iyi yazılımcı hatayı sadece kodda aramaz; hatayı arama biçimini de test eder. Bu refleks, daha az tahmin, daha küçük deney ve daha hızlı kök neden demektir.

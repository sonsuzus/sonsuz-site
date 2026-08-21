---
layout: post
title: "TypeScript ile Tip Güvenli JavaScript: Büyük Projelerde Hataları Azaltma Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - typescript
  - javascript
  - tip güvenliği
toc: true
image: /img/typescript-ile-tip-22.png
---

JavaScript'in esnekliği hızlı prototip üretmek için harikadır; ancak ekip, dosya ve entegrasyon sayısı büyüdükçe bu esneklik pahalı sürprizlere dönüşebilir. TypeScript, JavaScript'in üzerine statik tip katmanı ekleyerek değişkenlerin, fonksiyonların ve veri sözleşmelerinin daha kod çalışmadan doğrulanmasını sağlar. Amaç JavaScript'i “daha katı” yapmak değil; hataları kullanıcıya ulaşmadan, geliştiricinin editöründe yakalamaktır.

``

## Statik tip denetimi neden önemlidir?

JavaScript'te bir fonksiyonun hangi türde değer beklediği çoğu zaman yalnızca isimlendirme, yorumlar veya ekip alışkanlıklarıyla anlaşılır. Örneğin API'den gelen bir kullanıcının `id` alanının sayı mı, metin mi olduğu çalışma anına kadar belirsiz kalabilir. TypeScript bu belirsizliği bir sözleşmeye dönüştürür:

```ts
interface User {
  id: number;
  name: string;
  email?: string;
}

function formatUser(user: User): string {
  return `${user.id} - ${user.name.toUpperCase()}`;
}

formatUser({ id: "42", name: "Ada" }); // Derleme hatası
```

Buradaki hata uygulama tarayıcıda açılmadan yakalanır. Matematiksel olarak, üretime taşınan hata sayısını kabaca şöyle düşünebiliriz:

$$H_{üretim} = H_{potansiyel} \times (1 - K_{tip}) \times (1 - K_{test})$$

Burada $K_{tip}$, tip sisteminin yakalayabildiği hata oranını temsil eder. TypeScript tüm sorunları çözmez; fakat yanlış argüman, eksik alan, hatalı dönüş değeri ve `undefined` erişimi gibi sınıfları erkenden elemekte çok etkilidir.

| Özellik | Sadece JavaScript | TypeScript ile JavaScript |
|---|---|---|
| Veri sözleşmesi | Dokümantasyon ve disipline bağlı | Arayüzler ve tiplerle tanımlı |
| Hata yakalama zamanı | Çalışma zamanı | Yazım/derleme zamanı + çalışma zamanı |
| IDE desteği | Tahmine dayalı | Otomatik tamamlama ve güvenli yeniden adlandırma |
| Büyük refaktör | Riskli, manuel kontrol yoğun | Etkilenen kullanımları derleyici listeler |

## En değerli alan: sınırlar ve sözleşmeler

Büyük web projelerinde hatalar genellikle modüllerin kesiştiği yerlerde ortaya çıkar: API yanıtları, form verileri, Redux/Zustand store'ları veya bileşen `props`ları. TypeScript bu sınırları görünür hâle getirir. Özellikle `strict` modu, potansiyel olarak boş olan değerlere karşı koruma sağlar.

```ts
type ApiResponse = {
  user?: { name: string };
};

function welcome(response: ApiResponse) {
  // response.user.name; // "user" tanımsız olabilir
  return response.user?.name
    ? `Hoş geldin, ${response.user.name}`
    : "Misafir kullanıcı";
}
```

Bu yaklaşım, “ben bu alan hep gelir sanıyordum” türü üretim hatalarını azaltır. Ancak kritik bir ayrım vardır: TypeScript dışarıdan gelen veriyi sihirli biçimde doğrulamaz. Sunucu yanlış JSON gönderirse tipler yalnızca geliştirici varsayımını anlatır. Bu nedenle API sınırlarında Zod gibi çalışma zamanı doğrulama araçlarıyla birleşmek güçlü bir stratejidir.

## Tipler refaktörün emniyet kemeridir

Bir `User` alanını `fullName` olarak değiştirdiğinizi düşünün. JavaScript projesinde eski `name` kullanımlarını aramak gerekir; dinamik erişimler veya gözden kaçan dosyalar risk yaratır. TypeScript ise derleme hatalarıyla etkilenmiş noktaları işaretler. Bu durum geliştirme hızını yavaşlatmaz; ilk anda biraz daha fazla yazmayı gerektirse de hata ayıklama ve kod inceleme maliyetini düşürür.

| Yaygın hata | TypeScript'in katkısı | Ek önlem |
|---|---|---|
| Yanlış fonksiyon argümanı | Parametre tipi denetimi | Birim testi |
| Eksik API alanı | Opsiyonel alan ve `strictNullChecks` | Runtime şema doğrulaması |
| Yanlış refaktör | Kullanım noktalarını derleme hatasıyla bulma | CI derleme adımı |
| Mantıksal iş kuralı hatası | Sınırlı; tip doğru olsa da sonuç yanlış olabilir | E2E ve domain testleri |

## Dengeli kullanım için öneriler

Yeni bir projede `strict: true` ile başlayın; eski projelerde ise modül modül geçiş yapın. `any` kullanmak kısa vadede engelleri kaldırır ama tip güvenliği zincirini koparır. Onun yerine bilinmeyen dış veriler için `unknown`, farklı durumlar için ayrık birleşimler (`union`) ve daraltma kontrolleri kullanın.

TypeScript'i testlerin alternatifi değil, ilk savunma hattı olarak konumlandırın. Tipler kodun şeklinin doğru olduğunu; testler ise davranışın doğru olduğunu doğrular. Bu ikili, büyük ölçekli web projelerinde daha öngörülebilir sürümler, daha güvenli refaktörler ve daha az gece yarısı hata avı anlamına gelir.

![typescript-ile-tip-22](/img/typescript-ile-tip-22.svg)


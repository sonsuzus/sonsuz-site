---
layout: post
title: "Feature Flag Sistemleri: Kod Dağıtmadan Özellik Açıp Kapatmanın Mimarisi"
math: true
categories: 
  - Bilgi
tags: 
  - feature flag
  - yazılım mimarisi
  - devops
toc: true
---

Modern yazılım ekipleri için bir özelliği geliştirmek ile onu kullanıcılara sunmak aynı olay olmak zorunda değildir. Feature flag (özellik bayrağı), uygulamaya dağıtılmış fakat henüz herkese görünür olmayan davranışları çalışma anında kontrol etmeyi sağlar. Böylece büyük sürümler yerine küçük, geri alınabilir ve ölçülebilir değişiklikler yapılır. Bir nevi sahne arkasında dekor hazırdır; perdeyi ne zaman açacağınıza bayrak karar verir.
``

Temel fikir oldukça basittir: Uygulama, belirli bir anahtarın değerini okuyup akışı buna göre seçer. Matematiksel olarak bir kullanıcı için karar fonksiyonunu şöyle düşünebiliriz:

$$E(u, f, t) = R_f \land H(u) \land Z(t)$$

Burada $R_f$ bayrağın açık olup olmadığını, $H(u)$ kullanıcının hedef kitleye dahil edilmesini, $Z(t)$ ise zaman, bölge veya hesap türü gibi ek kuralları temsil eder. Sonuç doğruysa yeni deneyim, yanlışsa mevcut deneyim çalışır. Bu yaklaşım yalnızca `true/false` anahtarından ibaret değildir; kademeli yayılım, A/B testi ve acil kapatma gibi operasyonel yeteneklerin temelidir.

## Dağıtım ile yayınlama arasındaki fark

Kod dağıtımı (deployment), derlenen uygulamanın sunucuya veya istemciye ulaşmasıdır. Yayınlama (release) ise kullanıcının bu davranışı gerçekten görmesidir. Feature flag bu iki süreci ayırır. Yeni ödeme ekranını pazartesi günü dağıtıp yalnızca ekip hesaplarına açabilir, metrikler sağlamsa salı günü kullanıcıların %5'ine, daha sonra tamamına sunabilirsiniz.

| Yaklaşım | Geri alma süresi | Risk seviyesi | Deney kontrolü |
|---|---:|---:|---|
| Klasik sürüm geri alma | Dakikalar-saatler | Yüksek | Sınırlı |
| Feature flag kapatma | Saniyeler-dakikalar | Daha düşük | Ayrıntılı |
| Canary dağıtımı | Dakikalar | Orta | Sunucu/traﬁk odaklı |

Canary dağıtımı ve feature flag rakip değildir. Canary yeni kodun hangi altyapı örneklerinde çalışacağını kontrol ederken, flag hangi kullanıcıların hangi işlevi göreceğini belirleyebilir.

## Basit ama etkili bir uygulama

Aşağıdaki TypeScript örneğinde bayrak, kullanıcının rolü ve yüzde tabanlı bir kural birlikte değerlendirilir. Gerçek projelerde değerler çevresel değişkenden, önbellekten ya da merkezi bir flag servisinden gelir.

```ts
type User = { id: string; role: "admin" | "member" };

function isNewCheckoutEnabled(user: User, enabled: boolean): boolean {
  if (!enabled) return false; // Acil kapatma anahtarı
  if (user.role === "admin") return true; // İç kullanıcılar önce dener

  const bucket = hashToBucket(user.id); // 0-99 arası kararlı değer
  return bucket < 10; // Kullanıcıların yaklaşık %10'u
}

function hashToBucket(value: string): number {
  let hash = 0;
  for (const char of value) hash = (hash * 31 + char.charCodeAt(0)) | 0;
  return Math.abs(hash) % 100;
}
```

Buradaki kritik ayrıntı kararlılıktır: Aynı kullanıcı her istekte aynı grupta kalmalıdır. Rastgele sayı kullanmak, bir sayfa yenilemede eski sepeti, diğerinde yeni sepeti gösterebilir. Bu da hem kullanıcı deneyimini hem de deney sonuçlarını bozar.

## Bayrak türleri ve yaşam döngüsü

| Bayrak türü | Amaç | Önerilen ömür |
|---|---|---|
| Release flag | Bitmemiş özelliği güvenle açmak | Kısa |
| Experiment flag | Varyasyonları ölçmek | Deney sonuna kadar |
| Ops flag | Trafiği veya pahalı işlemi kısmak | Uzun olabilir |
| Permission flag | Paket/rol bazlı yetki vermek | Uzun olabilir |

Bayrakların gizli maliyeti teknik borçtur. Kullanımdan kalkmış bir flag, iki ayrı kod yolunu gereksiz yere yaşatır. Bu nedenle her bayrağın sahibi, oluşturulma tarihi, kapatma planı ve kaldırılma görevi olmalıdır. Örneğin yeni akış kalıcılaştığında `if/else` yapısını temizleyip bayrağı ve yönetim panelindeki kaydını silin.

Son olarak, flag değerlendirmesi hata anında güvenli bir varsayıma sahip olmalıdır. Merkezi servis erişilemezse ödeme gibi kritik bir akışın yeni ve doğrulanmamış sürümünü açmak yerine çoğu zaman eski, güvenilir davranışa dönmek mantıklıdır. İzleme metrikleri, denetim kayıtları ve yetki kontrolleri eklendiğinde feature flag sistemi; sadece aç-kapa düğmesi değil, kontrollü ürün teslimatının güçlü bir mimari aracına dönüşür.

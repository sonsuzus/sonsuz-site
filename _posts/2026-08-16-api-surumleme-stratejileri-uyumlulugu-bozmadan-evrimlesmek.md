---
layout: post
title: "API Sürümleme Stratejileri: Uyumluluğu Bozmadan Evrimleşmek"
math: true
categories: 
  - Bilgi
tags: 
  - apı
  - sürümleme
  - rest
  - geriye dönük uyumluluk
image: /img/api-surumleme-stratejileri-49.png
---

Bir API yayınlamak, taş tabletlere kural kazımak değildir; daha çok şehir içindeki bir metro hattını işletmeye benzer. Yeni duraklar eklemek istersiniz, fakat her gün o hattı kullanan yolcuların işe geç kalmaması gerekir. API sürümleme, istemcilerin mevcut davranışlarını korurken servisinizin veri modelini, uç noktalarını ve iş kurallarını güvenle geliştirme disiplinidir. Başarılı stratejinin merkezi yalnızca `/v2` etiketi değil; değişikliğin etkisini ölçmek, sözleşmeyi korumak ve geçişi yönetmektir.
``

Temel ilke şudur: **ekleyici değişiklikler** genellikle güvenlidir, **çıkarıcı veya anlam değiştirici değişiklikler** ise kırıcıdır. Örneğin bir JSON yanıtına `avatarUrl` alanı eklemek, alanları görmezden gelen istemciler için çoğunlukla sorun yaratmaz. Buna karşılık `name` alanını kaldırmak, türünü metinden nesneye dönüştürmek ya da bir alanın anlamını değiştirmek istemciyi sessizce yanlış çalıştırabilir.

Bunu basit bir uyumluluk modeliyle düşünebiliriz. Bir istemcinin beklediği sözleşme kümesi $C$, sunucunun sunduğu davranış kümesi $S$ olsun. Eski istemcinin çalışmaya devam etmesi için ideal koşul $C_{eski} \subseteq S_{yeni}$ olmalıdır. Yeni sürüm daha fazla özellik sunabilir; ancak eski istemcinin zorunlu kabul ettiği özellikleri kaybetmemelidir.

| Değişiklik | Risk seviyesi | Genellikle uyumlu mu? | Not |
|---|---:|---|---|
| Yeni, isteğe bağlı alan eklemek | Düşük | Evet | İstemci bilinmeyen alanları yok saymalıdır. |
| Alanı zorunlu yapmak | Yüksek | Hayır | Eski istekler doğrulamada başarısız olabilir. |
| Alan adını değiştirmek | Yüksek | Hayır | Bir geçiş dönemi ve iki alan desteği gerekir. |
| Yeni endpoint eklemek | Düşük | Evet | Mevcut akışları etkilemez. |
| HTTP durum kodunu değiştirmek | Orta/Yüksek | Çoğunlukla hayır | İstemciler hata yönetiminde kırılabilir. |

Sürüm numarasını nereye koyacağınız ise mimari ve kullanıcı alışkanlıklarına bağlıdır. URL sürümleme görünür ve anlaşılırdır: `/api/v1/orders`. Header tabanlı yaklaşım kaynak adresini temiz tutar; örneğin `Accept: application/vnd.magaza.v2+json`. Sorgu parametresi ise hızlı prototiplerde pratik olsa da önbellekleme ve dokümantasyon açısından daha zayıf kalabilir.

| Yaklaşım | Örnek | Güçlü yanı | Dikkat edilmesi gereken |
|---|---|---|---|
| URL | `/api/v2/users` | Keşfedilebilir, kolay yönlendirilir | Endpoint çoğalması |
| Header | `Accept: ...v2+json` | Kaynak kimliği sabit kalır | Test ve kullanım daha karmaşık |
| Parametre | `?version=2` | Hızlı uygulanır | Standartlaşması zayıftır |

Pratikte yalnızca büyük kırıcı değişikliklerde yeni ana sürüm açmak iyi bir dengedir. Küçük ve geriye uyumlu geliştirmeler için aynı sürüm içinde ilerleyin. Örneğin sipariş yanıtına yeni alan eklerken v2 üretmek yerine alanı nullable veya isteğe bağlı tasarlayın:

```json
{
  "id": "ord_42",
  "status": "shipped",
  "trackingUrl": null
}
```

Burada `trackingUrl` henüz her kargo firması için mevcut değildir. `null` değerini açıkça tanımlamak, istemcinin alanın yokluğu ile geçici olarak bilinmeyen değer arasındaki farkı yönetmesine yardım eder. Ancak bu sözleşmeyi dokümante etmezseniz `null`, yazılım dünyasının meşhur “bakarız” cevabına dönüşür.

Kırıcı bir değişiklik kaçınılmazsa, **deprecation** süreci uygulayın. Eski endpoint'i çalışır bırakın, yanıt başlıklarıyla kullanımın sonlanacağını duyurun ve ölçüm toplayın:

```http
Deprecation: true
Sunset: Wed, 01 Jul 2027 00:00:00 GMT
Link: </docs/migration-v2>; rel="deprecation"
```

Bu başlıklar tek başına sihir değildir; e-posta duyurusu, sürüm notu, geçiş rehberi ve kullanım analitiğiyle desteklenmelidir. Hangi istemcilerin hâlâ v1 kullandığını bilmeden kapatma tarihi belirlemek, köprüyü geçmeden yakmaya benzer.

Son olarak sözleşme testleri kurun. OpenAPI şeması, consumer-driven contract testleri ve üretim trafiğinin kontrollü gölgelemesi, sürümleme kararlarını tahmin yerine kanıta dayandırır. Sağlam API'ler hiç değişmeyen API'ler değildir; değişirken kullanıcılarını yolda bırakmayan API'lerdir.

![api-surumleme-stratejileri-49](/img/api-surumleme-stratejileri-49.svg)


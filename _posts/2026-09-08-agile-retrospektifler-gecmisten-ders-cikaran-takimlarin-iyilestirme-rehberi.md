---
layout: post
title: "Agile Retrospektifler: Geçmişten Ders Çıkaran Takımların İyileştirme Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - agile
  - retrospektif
  - takım kültürü
toc: true
---

Bir sprint sona erdiğinde yalnızca tamamlanan işlere bakmak yeterli değildir. Takımın nasıl çalıştığını, nerelerde zorlandığını ve bir sonraki sprintte neyi farklı yapabileceğini konuşması gerekir. Agile retrospektif, geçmişi suçlu aramak için değil, geleceği biraz daha akıllıca tasarlamak için inceleyen güvenli bir geri bildirim ortamıdır.
``

## Retrospektifin teorik temeli

Retrospektif, deneysel süreç kontrolü anlayışına dayanır. Agile ekipler kusursuz bir planın peşinden gitmek yerine kısa döngülerle çalışır, sonuçları gözlemler ve yöntemlerini yeni bilgilere göre uyarlar. Bu yaklaşım üç temel sütunla açıklanabilir:

- **Şeffaflık:** Sorunlar ve başarılar görünür hâle gelir.
- **Denetim:** Ekip çalışma biçimini düzenli olarak değerlendirir.
- **Uyarlama:** Değerlendirme sonucunda somut değişiklikler yapılır.

Basitçe ifade edersek süreç iyileştirmesi şu döngüyü izler:

$$Gözlem \rightarrow İçgörü \rightarrow Aksiyon \rightarrow Ölçüm$$

Retrospektif yalnızca toplantı yapmak değildir. Ölçülmeyen ve takip edilmeyen kararlar, dijital bir çekmecede unutulan yapılacaklar listesine dönüşebilir.

## Retrospektif ile durum toplantısı aynı şey değildir

| Özellik | Günlük toplantı | Sprint değerlendirmesi | Retrospektif |
|---|---|---|---|
| Odak | Günlük ilerleme | Ürün çıktısı | Çalışma süreci |
| Ana soru | Bugün ne yapacağız? | Ne ürettik? | Nasıl daha iyi çalışırız? |
| Katılımcılar | Geliştirme ekibi | Ekip ve paydaşlar | Genellikle takım üyeleri |
| Beklenen sonuç | Günlük plan | Ürün geri bildirimi | İyileştirme aksiyonu |

Bu ayrım önemlidir: Retrospektifte kodun kendisinden çok, kodu üretirken yaşanan iletişim, iş akışı, kalite ve iş birliği konuşulur.

## Verimli bir tören nasıl yürütülür?

İyi bir retrospektif genellikle beş aşamada ilerler:

1. **Ortamı hazırla:** Kolaylaştırıcı, görüşmenin amacını ve güven kurallarını açıklar.
2. **Veri topla:** Ekip iyi gidenleri, zorlanılan noktaları ve gözlemlerini paylaşır.
3. **İçgörü üret:** Tekrarlayan örüntüler ve kök nedenler araştırılır.
4. **Aksiyon seç:** Her şeyi düzeltmeye çalışmak yerine bir veya iki etkili adım belirlenir.
5. **Kapanış yap:** Toplantı formatı değerlendirilir ve katılımcılara teşekkür edilir.

Örneğin aksiyonların makine tarafından okunabilir biçimde kaydedilmesi takip sürecini kolaylaştırabilir:

```yaml
aksiyon:
  sorun: Kod incelemeleri uzun sürüyor
  adim: Her iş günü iki inceleme saati belirle
  sorumlu: Gelistirme ekibi
  son_tarih: Sonraki sprint sonu
  metrik: Ortalama inceleme süresi
```

Bu kayıt; sorunu, uygulanacak deneyi, sorumluluğu ve başarı ölçütünü görünür kılar.

## Psikolojik güvenlik neden kritik?

Bir ekip üyesi hata yaptığını söylediğinde cezalandırılacağını düşünüyorsa gerçek sorunlar masaya gelmez. Toplantı sakin görünür, fakat bu sessizlik sağlık göstergesi değildir. Psikolojik güvenlik, insanların küçük düşürülmeden soru sorabilmesi, itiraz edebilmesi ve başarısız deneylerden söz edebilmesidir.

Kolaylaştırıcı, “Kim bozdu?” yerine “Sistem bu sonuca nasıl izin verdi?” sorusunu kullanmalıdır. Kişiliklere değil gözlemlenebilir davranışlara odaklanılmalıdır. “Sen ilgilenmedin” ifadesi savunma yaratırken, “Üç görev iki gün boyunca sahipsiz kaldı” ifadesi araştırılabilir veri sunar.

Takımın iyileştirme hızını kabaca şöyle düşünebiliriz:

$$İyileştirme\ Hızı = Geri\ Bildirim\ Kalitesi \times Uygulama\ Oranı$$

Harika fikirler üretilip hiçbiri uygulanmıyorsa çarpım yine sıfıra yaklaşır.

## Retrospektifi canlı tutmak

Her sprint aynı formatı kullanmak töreni otomatik pilota bağlayabilir. “Başlat, Durdur, Devam Et”, yelkenli analizi veya mutluluk grafiği gibi formatlar dönüşümlü kullanılabilir. Ancak renkli notlar amaç değil, konuşmayı kolaylaştıran araçlardır.

Sonraki retrospektif mutlaka önceki aksiyonların kontrolüyle başlamalıdır. Böylece ekip geri bildirimin gerçekten değişim yarattığını görür. Güven, takip ve küçük deneylerle desteklenen retrospektifler; yalnızca süreçleri değil, takım ruhunu da güçlendiren düzenli bir öğrenme motoruna dönüşür.

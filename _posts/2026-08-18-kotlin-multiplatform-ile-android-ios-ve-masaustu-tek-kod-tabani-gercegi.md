---
layout: post
title: "Kotlin Multiplatform ile Android, iOS ve Masaüstü: Tek Kod Tabanı Gerçeği"
math: true
categories: 
  - Program
tags: 
  - Kotlin Multiplatform
  - Compose Multiplatform
  - Mobil Geliştirme
---

Android, iOS ve masaüstü için ayrı ekipler, ayrı iş listeleri ve aynı hatanın üç farklı yerde düzeltilmesi… Tanıdık bir senaryoysa Kotlin Multiplatform (KMP) güçlü bir çıkış noktasıdır. KMP, uygulamanın iş mantığını tek bir ortak modülde yazıp Android, iOS, Windows, macOS ve Linux hedeflerine derlemenizi sağlar. Amaç “her şeyi sihirli biçimde tek seferde yazmak” değil; tekrar eden mantığı merkezileştirip platforma özgü katmanları kontrollü biçimde ayırmaktır.
``

KMP’nin teorik temeli, **paylaşılan kod** ile **platform entegrasyonu** arasındaki sınırı doğru çizmektir. Ağ istekleri, veri doğrulama, kullanım senaryoları, önbellekleme ve durum yönetimi genellikle ortak alanda yaşar. Kamera erişimi, bildirimler, mağaza dağıtımı veya iOS’e özgü sistem arayüzleri ise hedef platformda kalır. Böylece kod paylaşım oranı yaklaşık olarak şu şekilde düşünülebilir:

$$Paylaşım\ Oranı = \frac{Ortak\ Kod}{Toplam\ Kod} \times 100$$

İyi tasarlanmış bir uygulamada bu oran iş mantığında oldukça yüksek olabilir; ancak arayüz ve cihaz yetenekleri nedeniyle yüzde 100 hedefi her zaman doğru değildir.

| Katman | KMP ile paylaşım durumu | Örnek |
|---|---:|---|
| Domain / iş kuralları | Çok yüksek | Sepet tutarı, giriş doğrulama |
| Veri katmanı | Yüksek | Ktor API istemcisi, SQLDelight |
| Sunum durumu | Yüksek | ViewModel, UI state |
| Kullanıcı arayüzü | Değişken | Compose Multiplatform veya native UI |
| Donanım ve sistem API’leri | Düşük | Kamera, push bildirimleri |

Projede tipik olarak `commonMain`, `androidMain`, `iosMain` ve `desktopMain` kaynak kümeleri bulunur. `commonMain`, tüm hedeflerin anlayacağı Kotlin kodunu içerir. Platforma özel ihtiyaçlarda `expect` ve `actual` mekanizması devreye girer: ortak kod bir yetenek bekler, her platform bu yeteneğin gerçek uygulamasını verir.

```kotlin
// commonMain: Uygulamanın istediği yeteneği tanımlar
expect class PlatformInfo() {
    fun name(): String
}

fun welcomeMessage(): String =
    "Merhaba, ${PlatformInfo().name()} kullanıcısı!"

// androidMain: Android karşılığı
actual class PlatformInfo {
    actual fun name(): String = "Android"
}
```

Bu örnekte ortak katman Android sınıflarını bilmez. Aynı `PlatformInfo` sınıfının iOS ve masaüstü için de `actual` karşılıkları yazılır. Bu yaklaşım, bağımlılık yönünü temiz tutar: iş mantığı platforma değil, soyutlamaya bağlıdır.

Arayüz tarafında iki temel strateji vardır:

| Strateji | Avantajı | Dikkat edilmesi gereken |
|---|---|---|
| Native UI + ortak mantık | Platform hissi ve olgun bileşenler | Android/iOS ekranları ayrı yazılır |
| Compose Multiplatform | Daha fazla UI paylaşımı ve hızlı prototipleme | iOS davranışları, erişilebilirlik ve tasarım testleri gerekir |

Compose Multiplatform, özellikle Android ve masaüstünde oldukça üretkendir; iOS hedefi de hızla olgunlaşmaktadır. Yine de “tek UI” kararını teknik heyecanla değil, ürün ihtiyacıyla verin. Örneğin iOS tasarım kurallarına sıkı uyum gerektiren bir bankacılık ekranında native SwiftUI tercih edilebilir. Buna karşılık yönetim paneli, eğitim uygulaması veya içerik odaklı bir ürün Compose ile ciddi hız kazanabilir.

Ortak bir API istemcisi için Ktor kullanmak, tekrarın azalmasına güzel bir örnektir:

```kotlin
class UserRepository(private val client: HttpClient) {
    suspend fun getUser(id: String): User {
        return client.get("https://api.ornek.com/users/$id")
            .body()
    }
}
```

Buradaki `UserRepository`, Android, iOS ve masaüstünde aynı davranışı üretir. Platform tarafında yalnızca HTTP motoru veya güvenlik yapılandırması gerektiğinde farklılaştırma yapılabilir.

Geliştirme süresini etkileyen kaba bir model de kurulabilir: $$T_{yeni} \approx T_{ortak} + \sum T_{platform\_özel}$$. Üç ayrı uygulamada ise ortak işlerin tekrarından dolayı maliyet çoğu zaman $3 \times T_{ortak}$ seviyesine yaklaşır. KMP, özellikle bakım ve özellik geliştirme döngülerinde bu farkı görünür hâle getirir.

Başarılı bir başlangıç için küçük bir dikey dilim seçin: giriş ekranı, API çağrısı, yerel veri saklama ve bir liste görünümü. Önce ortak domain ve data katmanını kurun; sonra UI paylaşımını ölçerek artırın. KMP bir “her şeyi ortaklaştırma” aracı değil, doğru kodun doğru yerde yaşamasını sağlayan üretken bir mimari yatırımıdır.

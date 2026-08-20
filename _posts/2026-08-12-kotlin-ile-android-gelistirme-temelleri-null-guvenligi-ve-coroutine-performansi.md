---
layout: post
title: "Kotlin ile Android Geliştirme Temelleri: Null Güvenliği ve Coroutine Performansı"
math: true
categories: 
  - Bilgi
tags: 
  - kotlin
  - android
  - coroutine
toc: true
---

Android geliştirmede kullanıcıların sabrı, uygulamanın akıcılığı kadar değerlidir: Bir ekran donarsa, en şık arayüz bile puan kaybeder. Kotlin, Java ekosistemiyle uyumunu korurken null güvenliği ve coroutine gibi modern araçlarla bu soruna iki cepheden yaklaşır. İlki beklenmeyen çöküşleri azaltır; ikincisi ise uzun süren işleri ana iş parçacığını kilitlemeden yürütür. Bu ikiliyi doğru anlamak, yalnızca daha temiz kod değil, daha güvenilir ve hızlı hissedilen uygulamalar üretmenin temelidir.
``

## Null neden bu kadar tehlikeli?

Android'de bir API yanıtı, `Intent` ekstra değeri, veritabanı sorgusu veya görünüm referansı her zaman mevcut olmayabilir. Java'daki `NullPointerException`, çoğu zaman uygulamanın tam da kullanıcının en kritik anda karşısına çıkan klasik kazasıdır. Kotlin, tür sisteminde null olasılığını açıkça belirtir:

```kotlin
val userName: String = "Deniz"
val avatarUrl: String? = null
```

Burada `String`, boş olamayacağını; `String?` ise değerin `null` olabileceğini anlatır. Derleyici, `avatarUrl.length` yazmanıza izin vermez. Bu küçük engel, çalışma zamanındaki çöküşü derleme zamanında yakalayan bir emniyet kemeridir.

| Yaklaşım | Null değerde davranış | Kullanım amacı |
|---|---|---|
| `?.` güvenli çağrı | İşlemi atlar, `null` üretir | Opsiyonel veriyi okumak |
| `?:` Elvis operatörü | Varsayılan değer seçer | Arayüz için yedek değer |
| `!!` zorla açma | Çöküş riski taşır | Sadece kesin kanıt varsa |
| `let` | Değer varsa blok çalışır | Null olmayan değeri işlemek |

Örneğin profil görseli yoksa metin tabanlı bir yer tutucu göstermek hem güvenli hem de kullanıcı dostudur:

```kotlin
val label = user.avatarUrl?.take(20) ?: "Varsayılan avatar"
textView.text = label
```

`!!` operatörü bazen hızlı bir çözüm gibi görünür; fakat aslında Kotlin'in güvenlik alarmını susturmaktır. Tercih edilmesi gereken düşünce şudur: “Bu değer neden boş olabilir ve uygulama bunu nasıl zarifçe karşılamalı?”

## Coroutine: Beklerken arayüzü dondurmamak

Ağ isteği, diskten veri okuma ve ağır görsel işleme zaman alır. Android'in ana iş parçacığı (`Main`) ise dokunmaları, animasyonları ve çizimleri yönetir. Uzun bir işi burada yaparsanız kareler gecikir. Yaklaşık olarak bir kare için zaman bütçesi $16.67\,ms$'dir; çünkü $60\,FPS$ hedefinde $T = 1000/60$ olur. Bu bütçe aşılırsa kullanıcı takılmayı hisseder.

Coroutine, işi farklı bir dispatcher üzerinde askıya alıp sonucu ana iş parçacığına döndürmeyi kolaylaştırır. “Askıya alma”, thread'i boş yere bekletmek yerine başka işlere fırsat tanır.

```kotlin
viewModelScope.launch {
    val products = withContext(Dispatchers.IO) {
        repository.fetchProducts()
    }
    uiState.value = UiState.Success(products)
}
```

Bu örnekte `fetchProducts()` ağ veya veritabanı işi yaptığı için `Dispatchers.IO` üzerinde çalışır. İş bitince coroutine doğal olarak `viewModelScope` bağlamındaki ana akışa döner ve arayüz durumu güncellenir. `viewModelScope`, ViewModel temizlendiğinde görevleri iptal ederek gereksiz iş ve bellek sızıntısı riskini de azaltır.

| Dispatcher | En uygun iş | Yanlış kullanım sonucu |
|---|---|---|
| `Dispatchers.Main` | UI güncelleme | Ağ çağrısında donma |
| `Dispatchers.IO` | Ağ, dosya, veritabanı | UI güncellemede hata |
| `Dispatchers.Default` | CPU yoğun hesaplama | Ana thread'de kare kaybı |

Coroutine performansı yalnızca “arka plana atmak” değildir. Yapılandırılmış eşzamanlılık sayesinde görevlerin yaşam döngüsü sahipleri bellidir. Bir ekran kapanınca ona ait istekleri iptal etmek, artık görünmeyen bir ekrana veri basmayı önler. Ayrıca `async` yalnızca gerçekten paralel iki sonucu birleştirmeniz gerektiğinde kullanılmalıdır; her fonksiyona `async` serpmek hız değil, karmaşıklık üretir.

Sonuçta null güvenliği uygulamanın hata toleransını, coroutine ise tepki hızını güçlendirir. Kotlin'in asıl avantajı bu özellikleri ayrı numaralar olarak değil, okunabilir bir tasarım dili olarak sunmasıdır: Verinin belirsizliğini türlerle anlatın, yavaş işleri doğru bağlamda çalıştırın ve kullanıcıya hiçbir zaman “uygulama düşünürken” donmuş bir ekran bırakmayın.

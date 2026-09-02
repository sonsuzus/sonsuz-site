---
layout: post
title: "SwiftUI ile Deklaratif Arayüzler: Durum Değişsin, Ekran Kendini Toparlasın"
math: true
categories: 
  - Bilgi
tags: 
  - swiftuı
  - swift
  - ios
  - durum yönetimi
  - deklaratif programlama
toc: true
image: /img/swiftui-ile-deklaratif-88.png
---

SwiftUI, Apple platformlarında arayüz yazmayı “hangi pikseli nereye taşıyayım?” sorusundan “mevcut durumda kullanıcı ne görmeli?” sorusuna taşır. Bu yaklaşımın süper gücü, görünüm ile veri arasındaki bağı açıkça kurmasıdır. Bir değer değiştiğinde ekrana yeniden çizim emri yağdırmak yerine SwiftUI yeni durumu değerlendirir, eski görünüm ağacıyla karşılaştırır ve yalnızca gerekli bölümü günceller. Sonuç: daha az tören, daha okunabilir kod ve animasyonlara hazır modern ekranlar.

``

## Deklaratif düşünme: tarif değil sonuç

Emirsel UIKit dünyasında bir etiketi bulup `label.text = ...` demek yaygındır. Deklaratif modelde ise etiketin metni, durumun bir fonksiyonudur. Teorik olarak arayüzü şöyle düşünebiliriz:

$$UI = f(State)$$

Buradaki `State` değiştiğinde `f` yeniden hesaplanır. Bu, SwiftUI'ın her pikseli baştan boyadığı anlamına gelmez. Framework, görünümün `body` tanımından oluşan yeni değeri önceki değerle kıyaslar; farklılaşan alan için en uygun güncellemeyi uygular. `View` tiplerinin çoğunun `struct` olması da bu yüzden önemlidir: görünüm tanımı kısa ömürlü bir değer, kalıcı veri ise ayrı bir durum deposudur.

| Yaklaşım | Emirsel UI | SwiftUI deklaratif UI |
|---|---|---|
| Ana fikir | Bileşeni bul, değiştir | Durumu değiştir, sonucu tanımla |
| Güncelleme | Geliştirici yönetir | Framework türetir |
| Hata riski | Unutulan UI güncellemesi | Hatalı/verimsiz durum sahipliği |
| Güçlü taraf | İnce ayarlı kontrol | Tutarlılık ve hızlı geliştirme |

## Doğru durum kutusunu seçmek

SwiftUI'da önemli mesele “veri nerede yaşamalı?” sorusudur. `@State`, görünümün sahip olduğu basit ve yerel değerler içindir. Bir alt görünüm bu değeri değiştirecekse `@Binding` ile referansı değil, kontrollü bir bağlantıyı alır. Uygulama mantığı daha geniş ve paylaşılabilir olduğunda `ObservableObject` ile `@StateObject` veya `@ObservedObject` devreye girer. iOS 17 ve sonrası için Observation sistemiyle `@Observable` da daha doğal bir alternatif sunar.

| Araç | Sahip kim? | Tipik kullanım |
|---|---|---|
| `@State` | Görünüm | Sayaç, metin alanı, açılır pencere |
| `@Binding` | Üst görünüm | Alt görünümden düzenleme |
| `@StateObject` | Oluşturan görünüm | Ekranın kalıcı view model'i |
| `@ObservedObject` | Başka yer | Dışarıdan verilen model |
| `@Environment` | SwiftUI ortamı | Tema, erişilebilirlik, ortak servis |

Aşağıdaki örnek, yerel durum, binding ve otomatik görünüm yenilenmesini aynı sahnede gösterir:

```swift
import SwiftUI

struct CounterView: View {
    @State private var count = 0
    @State private var isCelebrating = false

    var body: some View {
        VStack(spacing: 20) {
            Text("Skor: \(count)")
                .font(.system(size: 42, weight: .bold))
                .contentTransition(.numericText())

            Stepper("Puanı değiştir", value: $count, in: 0...10)

            Toggle("Konfeti modu", isOn: $isCelebrating)

            if isCelebrating && count >= 5 {
                Label("Harika gidiyorsun!", systemImage: "sparkles")
                    .foregroundStyle(.orange)
            }
        }
        .padding()
        .animation(.spring, value: count)
    }
}
```

Burada `Stepper`, `$count` üzerinden binding alır. Kullanıcı değeri değiştirince `count` güncellenir; `body` tekrar değerlendirilir; metin, koşullu `Label` ve animasyon kararı yeni duruma göre oluşur. Dikkat edilmesi gereken nokta şudur: `body` içinde ağ isteği başlatmak veya rastgele veri üretmek kötü fikirdir. `body`, sıkça çağrılabilen saf bir görünüm tanımı olmalıdır.

## Güncelleme mekanizmasını verimli kullanmak

Durumu mümkün olduğunca küçük tutun ve türetilebilir bilgiyi ayrıca saklamayın. Örneğin `isGoalReached` yerine `count >= 5` kullanmak iki gerçeğin zamanla çelişmesini engeller. Bu prensip basitçe şudur:

$$DerivedState = g(SourceState)$$

Ayrıca kimlik (`id`) kavramını ihmal etmeyin. `ForEach` içindeki kararlı kimlikler, SwiftUI'ın hangi satırın eklendiğini, silindiğini ya da taşındığını anlamasını sağlar. Büyük uygulamalarda ekran durumunu `loading`, `success`, `empty` ve `failure` gibi açık durumlara ayırmak da belirsiz `Bool` ormanlarını azaltır.

SwiftUI sihir yapmaz; iyi modellenmiş durumun mantıklı sonucunu üretir. Verinin tek doğru kaynağını belirleyip sahipliği doğru atadığınızda, Apple ekosisteminde iPhone'dan Mac'e kadar arayüzünüz güncel kalır. En keyifli tarafı ise şudur: kullanıcı bir düğmeye basar, siz yalnızca gerçeği değiştirirsiniz; ekran geri kalan koreografiyi halleder.

![swiftui-ile-deklaratif-88](/img/swiftui-ile-deklaratif-88.svg)


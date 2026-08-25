---
layout: post
title: "Swift ile iOS Uygulama Mimarisi: Optional ve ARC’nin Görünmeyen Gücü"
math: true
categories: 
  - Bilgi
tags: 
  - swift
  - ios
  - optional
  - arc
  - uygulama mimarisi
toc: true
image: /img/swift-ile-ios-29.png
---

iOS uygulamalarında iyi mimari yalnızca ekranları MVVM, MVC veya Clean Architecture klasörlerine ayırmak değildir. Asıl kalite; verinin belirsizliğini doğru modellemek ve nesnelerin yaşam döngüsünü güvenle yönetmekle başlar. Swift’in `Optional` tipi ile Automatic Reference Counting (ARC) sistemi, Apple ekosistemindeki bu iki temel problemi dil seviyesinde ele alır: “Bu değer gerçekten var mı?” ve “Bu nesne artık bellekte kalmalı mı?”


![swift-ile-ios-29](/img/swift-ile-ios-29.svg)

``

## Optional: `nil` ihtimalini tasarımın parçası yapmak

Swift’te `Optional`, bir değerin mevcut olabileceğini veya olmayabileceğini ifade eden türdür. Örneğin ağdan gelen bir kullanıcının profil fotoğrafı URL’si her zaman bulunmayabilir. Bu durumu boş metin (`""`) ya da uydurma bir URL ile temsil etmek yerine `URL?` kullanmak, belirsizliği açıkça anlatır.

Teorik olarak bir optional türü iki olası durum taşır:

$$Optional<T> = .some(T) \cup .none$$

Başka bir deyişle `String?`, ya gerçek bir `String` içerir ya da `nil` olur. Bu küçük görünen fark, özellikle API yanıtları, form alanları, Core Data kayıtları ve UIKit yaşam döngüsünde hataları derleme zamanında yakalamaya yardımcı olur.

| Yaklaşım | Anlamı | Risk |
|---|---|---|
| `String` | Değer kesinlikle vardır | Eksik veri geldiğinde tasarım baskı görür |
| `String?` | Değer olmayabilir | Güvenli açma işlemi gerekir |
| `String!` | Değer var kabul edilir | Beklenmedik anda uygulama çöker |

Optional açmak için en okunabilir yöntemlerden biri `if let` veya `guard let` kullanmaktır. `guard`, özellikle fonksiyonun ana akışını sade tutar:

```swift
func configureProfile(imageURL: String?) {
    guard let imageURL,
          let url = URL(string: imageURL) else {
        print("Varsayılan profil görseli gösteriliyor.")
        return
    }

    print("Görsel şu adresten indirilecek: \(url)")
}
```

Bu kodda iki belirsizlik kontrol edilir: metnin gerçekten gelmesi ve gelen metnin geçerli bir URL’ye dönüşmesi. `!` ile zorla açmak kısa görünse de, üretim uygulamalarında “çalışıyor ama bir gün çökecek” türü borçlar oluşturur.

## ARC: Nesnelerin sahneden ne zaman ineceğine karar vermek

Swift, sınıf tabanlı nesnelerin belleğini ARC ile yönetir. Her güçlü referans, nesnenin referans sayısını artırır. Sayı sıfıra indiğinde ARC nesneyi bellekten temizler. Basit model şöyledir:

$$RC = \sum_{i=1}^{n} strongReference_i$$

Eğer $RC = 0$ ise nesne için `deinit` çalışabilir. Struct ve enum gibi değer tipleri bu referans sayımı modeline dayanmaz; bu nedenle mimaride model katmanını değer tipleriyle kurmak çoğu zaman daha öngörülebilirdir.

| Referans türü | Sahiplik | Kullanım senaryosu |
|---|---|---|
| `strong` | Nesneyi canlı tutar | Varsayılan property ilişkileri |
| `weak` | Nesneyi canlı tutmaz, optional’dır | Delegate, parent-controller ilişkileri |
| `unowned` | Nesneyi canlı tutmaz, optional değildir | Yaşam süresi kesin olarak daha uzun olan sahiplik |

ARC’nin en meşhur tuzağı retain cycle, yani karşılıklı güçlü referans döngüsüdür. Bir `ViewController`, bir view modelini; view model de closure üzerinden view controller’ı güçlü biçimde tutarsa, ekran kapansa bile iki nesne bellekte kalabilir. Closure’larda `self` yakalama listesi bu yüzden mimari bir ayrıntı değil, bellek güvenliği aracıdır:

```swift
final class ProfileViewModel {
    var onProfileLoaded: ((String) -> Void)?

    func loadProfile() {
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            self.onProfileLoaded?("Ayşe")
        }
    }
}

final class ProfileViewController: UIViewController {
    private let viewModel = ProfileViewModel()

    override func viewDidLoad() {
        super.viewDidLoad()

        viewModel.onProfileLoaded = { [weak self] name in
            self?.title = name
        }
    }
}
```

Burada closure, denetleyiciyi `weak` olarak yakalar. `self` bellekten temizlendiyse `self?.title` hiçbir şey yapmaz; uygulama da çökmez. Optional ile ARC’nin ortak mesajı nettir: Belirsizlikleri gizlemeyin, modelleyin. Swift mimarisinde güvenli kod; hem olmayan değeri hem de artık yaşamaması gereken nesneyi hesaba katan koddur.

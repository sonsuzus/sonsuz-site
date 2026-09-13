---
layout: post
title: "Clojure ve Değişmez Veri Yapıları: Eşzamanlılığa Fonksiyonel Bir Çözüm"
math: true
categories: 
  - Bilgi
tags: 
  - clojure
  - eşzamanlılık
  - fonksiyonel programlama
toc: true
---

Birden fazla iş parçacığının aynı veriyi değiştirmeye çalıştığı programlar, kısa sürede kilitler, yarış durumları ve gizemli hatalarla dolu bir labirente dönüşebilir. Clojure bu soruna alışılmışın dışında yaklaşır: Veriyi korumak için her yere kilit koymak yerine, verinin büyük bölümünü değiştirilemez hâle getirir. Böylece “Bu değeri kim değiştirdi?” sorusu büyük ölçüde ortadan kalkar ve eşzamanlı programlama daha öngörülebilir olur.
``

## Değişmezlik gerçekte nedir?

Clojure’daki bir koleksiyona eleman eklediğimizde mevcut koleksiyon değiştirilmez; yeni bir koleksiyon üretilir. Bu davranış, fonksiyonel programlamanın temel ilkelerinden biridir.

```clojure
(def numbers [1 2 3])
(def updated-numbers (conj numbers 4))

(println numbers)         ; [1 2 3]
(println updated-numbers) ; [1 2 3 4]
```

Burada `conj`, `numbers` değişkeninin gösterdiği vektörü bozmaz. Bunun yerine sonuna `4` eklenmiş yeni bir vektör döndürür. Dolayısıyla eski değer başka bir iş parçacığı tarafından güvenle okunmaya devam edebilir.

İlk bakışta her işlemde bütün koleksiyonun kopyalandığı düşünülebilir. Ancak Clojure kalıcı veri yapıları ve **yapısal paylaşım** kullanır. Yeni koleksiyon, eski yapının değişmeyen bölümlerini yeniden kullanır. Ağaç tabanlı bir vektörde erişim maliyeti yaklaşık olarak

$$T(n) = O(\log_{32} n)$$

şeklindedir. Dallanma katsayısı yüksek olduğu için pratikte bu derinlik oldukça küçüktür. Yani değişmezlik, “her seferinde her şeyi kopyala” anlamına gelmez.

## Değişebilir ve değişmez yaklaşım

| Özellik | Değişebilir veri | Clojure değişmez verisi |
|---|---|---|
| Güncelleme | Mevcut nesne değiştirilir | Yeni bir değer oluşturulur |
| İş parçacığı güvenliği | Genellikle kilit gerekir | Okuma doğal olarak güvenlidir |
| Geçmiş değere erişim | Ek kopyalama gerekir | Önceki değer korunur |
| Hata ayıklama | Zamanlamaya bağlı olabilir | Veri akışı daha öngörülebilirdir |
| Performans tekniği | Yerinde güncelleme | Yapısal paylaşım |

Değişmez veriler tüm eşzamanlılık problemlerini sihirli biçimde çözmez. Programın güncel bir durumu temsil etmesi gerektiğinde, değerlerin zaman içinde kontrollü olarak değiştirilmesine ihtiyaç duyulur. Clojure bu noktada kimlik ile değeri birbirinden ayırır.

## Atom ile güvenli durum geçişleri

`atom`, bağımsız bir durumu yönetmek için kullanılan referans türüdür. İçindeki değer değişmezdir; fakat atomun hangi değeri gösterdiği atomik olarak güncellenebilir.

```clojure
(def counter (atom 0))

(defn increase-counter []
  (swap! counter inc))

(dotimes [_ 1000]
  (future (increase-counter)))

(println @counter)
```

`swap!`, mevcut değeri okur, verilen saf fonksiyonu uygular ve sonucu atomik biçimde yerleştirir. Başka bir iş parçacığı araya girerse işlem yeni değer üzerinden tekrar denenebilir. Bu nedenle `swap!` içinde kullanılan fonksiyonun yan etkisiz olması önemlidir; aksi hâlde yeniden deneme, aynı yan etkinin birkaç kez gerçekleşmesine yol açabilir.

Bir sayacın geçişi matematiksel olarak şöyle ifade edilebilir:

$$s_{yeni} = f(s_{eski}) = s_{eski} + 1$$

Burada paylaşılan değişebilir bir sayı yerine, değişmez değerler arasında güvenli geçiş yapan bir kimlik bulunur.

## Birden fazla durumu koordine etmek

Birbiriyle ilişkili birkaç değerin birlikte güncellenmesi gerekiyorsa Clojure’un `ref` ve Yazılımsal İşlemsel Bellek, yani STM sistemi kullanılabilir.

```clojure
(def account-a (ref 500))
(def account-b (ref 200))

(defn transfer [amount]
  (dosync
    (alter account-a - amount)
    (alter account-b + amount)))

(transfer 100)
```

`dosync` içindeki işlemler tek bir mantıksal işlem gibi değerlendirilir. Ya iki hesap da güncellenir ya da hiçbiri güncellenmez. Böylece elle kilit sırası belirleme ve kilitlerin birbirini sonsuza dek beklediği deadlock senaryolarıyla uğraşma ihtiyacı azalır.

Clojure ayrıca bağımsız güncellemeler için `atom`, koordineli işlemler için `ref`, asenkron işler için `agent` ve geçici iş parçacığına özel değişimler için `transient` sunar. Ana fikir ise değişmez: Durumu kontrolsüzce değiştirmek yerine, değişmez değerler arasında açık ve güvenli geçişler kur. Sonuç, eşzamanlılığın ejderhasını tamamen yok etmese de ona yaklaşırken eline sağlam bir kalkan verir.

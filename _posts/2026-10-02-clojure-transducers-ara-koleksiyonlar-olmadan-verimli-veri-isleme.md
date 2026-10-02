---
layout: post
title: "Clojure Transducers: Ara Koleksiyonlar Olmadan Verimli Veri İşleme"
math: true
categories: 
  - Bilgi
tags: 
  - clojure
  - transducers
  - fonksiyonel-programlama
  - performans
  - veri-işleme
toc: true
image: /img/clojure-transducers-ara-66.png
---

Bir milyon sayıyı dönüştürmek, bazılarını elemek ve sonucu toplamak istediğinizi düşünün. Klasik bir `map`–`filter` zinciri gayet okunaklıdır; ancak her adım ara koleksiyonlar üretebilir veya tembel diziler üzerinden ek soyutlama maliyeti getirebilir. Clojure transducers, dönüşümün *nasıl saklandığını* değil, *nasıl uygulandığını* tarif ederek bu zinciri veri kaynağından bağımsız ve şaşırtıcı derecede verimli hâle getirir.

``

## Transducer tam olarak nedir?

Transducer, bir koleksiyon değildir ve veriyi kendi başına dolaşmaz. Bir **reducing function** alan ve onu yeni davranışlarla süsleyen yüksek seviyeli bir fonksiyondur. Başka bir ifadeyle `map`, `filter` ve benzeri işlemlerin koleksiyondan ayrılmış hâlidir.

Normal bir indirgeme şu düşünceyle çalışır:

$$a_{n+1} = f(a_n, x_n)$$

Burada $a_n$ mevcut birikim, $x_n$ sıradaki girdi ve $f$ reducing function’dır. Transducer ise doğrudan girdiyi değil, $f$ fonksiyonunu dönüştürür:

$$T(f) = f'$$

Böylece eşleme, filtreleme veya sınırlandırma mantığı; liste, vektör, kanal ya da akış hakkında hiçbir şey bilmeden çalışabilir. Transducer’ın felsefi güzelliği burada yatar: **dönüşüm ile veri taşıma mekanizması birbirinden ayrılır.**

## Klasik zincir ile karşılaştırma

Aşağıdaki işlem çift sayıları seçer, karelerini hesaplar ve toplar:

```clojure
(reduce +
        (map #(* % %)
             (filter even? (range 1000000))))
```

Kod nettir; Clojure’ın tembel dizileri sayesinde bütün ara sonuçlar aynı anda belleğe yüklenmez. Yine de her aşamada lazy sequence düğümleri, fonksiyon çağrıları ve dolaşım katmanları oluşabilir.

| Özellik | Dizi tabanlı zincir | Transducer |
|---|---|---|
| Ara temsil | Tembel veya somut diziler | Ara dizi yok |
| Veri yapısına bağlılık | Koleksiyon API’sine bağlı | Büyük ölçüde bağımsız |
| Dolaşım | Katmanlı olabilir | Tek indirgeme geçişi |
| Yeniden kullanım | Dizi işlemlerinde | `transduce`, `into`, kanallar ve akışlarda |
| Bellek davranışı | Kaynağa ve zincire göre değişir | Genellikle sabit ek bellek |

![clojure-transducers-ara-66](/img/clojure-transducers-ara-66.svg)


Aynı işlemi transducer ile şöyle kurabiliriz:

```clojure
(def xf
  (comp
    (filter even?)
    (map #(* % %))))

(transduce xf + 0 (range 1000000))
```

`xf`, henüz hiçbir veriyi işlemeyen bir dönüşüm tarifidir. `transduce`, bu tarifi `+` reducing function’ına uygular, başlangıç değerini `0` kabul eder ve kaynağı tek geçişte tüketir.

## `comp` sırası neden şaşırtıcıdır?

Normal fonksiyon bileşiminde `(comp f g)` önce `g`, sonra `f` çalıştırır. Transducer zincirinde ise veri yukarıdaki örnekte önce `filter`, sonra `map` aşamasından geçer. Bunun nedeni, reducing function’ların iç içe sarılmasıdır. Boru hattını okurken kodu yukarıdan aşağıya bir üretim bandı gibi düşünmek işleri kolaylaştırır: güvenlik görevlisi çiftleri içeri alır, sonraki robot da karelerini hesaplar.

## Sonucu farklı kaplara dökmek

Aynı dönüşüm tarifini bir vektör üretmek için `into` ile kullanabiliriz:

```clojure
(into [] xf (range 10))
;; => [0 4 16 36 64]
```

Özel bir indirgeme de yazılabilir:

```clojure
(defn toplam-ve-adet
  ([] {:toplam 0 :adet 0})
  ([sonuc] sonuc)
  ([birikim x]
   (-> birikim
       (update :toplam + x)
       (update :adet inc))))

(transduce xf toplam-ve-adet (range 10))
```

Bu üç ariteli biçim; başlatma, tamamlama ve adım davranışlarını tanımlar. Böylece aynı geçişte hem toplam hem adet hesaplanır.

## Ne zaman tercih edilmeli?

Transducers özellikle büyük veri kümelerinde, tekrar kullanılacak dönüşüm hatlarında, `core.async` kanallarında ve ara koleksiyonların pahalı olduğu süreçlerde parlar. Küçük bir liste için sırf havalı görünmek amacıyla kullanmak ise kodu gereksiz zorlaştırabilir. Önce okunabilirlik, ardından ölçüm gelmelidir; performans sorununu tahmin etmek yerine benchmark yapmak daha sağlıklıdır.

Kısacası transducer, “koleksiyon üzerinde işlem yap” demez; “bir indirgeme sürecine şu dönüşümleri ekle” der. Bu küçük perspektif değişimi, Clojure’da verimli ve birleştirilebilir veri işleme boru hatlarının kapısını açar.

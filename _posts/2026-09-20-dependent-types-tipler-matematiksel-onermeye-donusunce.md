---
layout: post
title: "Dependent Types: Tipler Matematiksel Önermeye Dönüşünce"
math: true
categories: 
  - Bilgi
tags: 
  - dependent-types
  - tip-sistemleri
  - fonksiyonel-programlama
  - matematik
  - idris
  - curry-howard
toc: true
---

Bir fonksiyonun yalnızca `Int` döndürdüğünü değil, **pozitif bir `Int`**, tam olarak üç elemanlı bir liste veya belirli bir denklemi sağlayan sonuç döndürdüğünü tip seviyesinde ifade edebilseydik ne olurdu? Dependent Types, yani bağımlı tipler, tiplerin değerlere bağlı olmasına izin vererek bu fikri gerçeğe dönüştürür. Böylece tip denetleyici, kodun kapısında bekleyen bir güvenlik görevlisinden matematik ödevimizi kontrol eden son derece titiz bir asistana dönüşür.

``

## Tipler değerlere bağımlı olabilir mi?

Geleneksel tip sistemlerinde `List String`, listenin eleman türünü söyler; fakat uzunluğu hakkında bilgi taşımaz. Bağımlı tipli bir dilde ise `Vect 3 String`, üç metinden oluşan bir vektörü temsil eder. Buradaki `3`, çalışma zamanındaki sıradan bir veri olmasının yanında tipin de parçasıdır.

Bunu matematiksel olarak bir tip ailesi şeklinde düşünebiliriz:

$$
Vect : \mathbb{N} \rightarrow Type \rightarrow Type
$$

Yani `Vect`, bir doğal sayı ve eleman tipi alıp yeni bir tip üretir.

| Yaklaşım | İfade | Derleyicinin bildiği |
|---|---|---|
| Geleneksel tip | `List Int` | Elemanlar tam sayıdır |
| Bağımlı tip | `Vect 4 Int` | Elemanlar tam sayıdır ve uzunluk 4'tür |
| Çalışma zamanı kontrolü | `if length xs == 4` | Bilgi ancak program çalışınca doğrulanır |
| Tip seviyesinde kontrol | `xs : Vect 4 Int` | Bilgi derleme sırasında kanıtlanır |

## Curry–Howard: Programlar kanıt, tipler önerme

Dependent Types yaklaşımının kalbinde **Curry–Howard correspondence** bulunur. Bu düşünceye göre matematiksel önermeler tip, önermelerin kanıtları ise o tipin değerleridir.

| Mantık | Programlama |
|---|---|
| Önerme | Tip |
| Kanıt | Değer veya program |
| İmplikasyon $A \Rightarrow B$ | Fonksiyon `A -> B` |
| Birleşim $A \land B$ | Çift `(A, B)` |
| Yanlış önerme | Değeri üretilemeyen boş tip |

Örneğin `A -> B` tipinde bir fonksiyon yazmak, “Elimde $A$ için kanıt varsa $B$ için de kanıt üretebilirim” demektir. Kod derleniyorsa kanıt, kullanılan tip sistemi ve aksiyomlar çerçevesinde kabul edilmiştir.

## Uzunluğu tipte saklamak

Idris ile iki vektörü birleştiren fonksiyon şöyle tanımlanabilir:

```idris
append : Vect n a -> Vect m a -> Vect (n + m) a
append [] ys = ys
append (x :: xs) ys = x :: append xs ys
```

Fonksiyonun dönüş tipi yalnızca “bir vektör döner” demez. Sonucun uzunluğunun kesinlikle $n+m$ olduğunu da belirtir. Uygulamada bir elemanı yanlışlıkla atlarsak derleyici dönüş tipinin beklenen uzunlukla uyuşmadığını fark eder. Böylece bazı testler yazılmadan önce, olası hataların tamamı tip seviyesinde elenir.

Aynı yöntem güvenli bir `head` fonksiyonu sağlar:

```idris
safeHead : Vect (S n) a -> a
safeHead (x :: xs) = x
```

`S n`, sıfırdan büyük bir doğal sayıdır. Fonksiyon boş vektör kabul etmediği için eksik durum yoktur; çalışma zamanında “liste boşmuş!” sürprizi yaşanmaz.

## Eşitlik de bir tiptir

İki ifadenin eşitliği `$x = y$` biçiminde bir tip olarak temsil edilebilir. Idris'teki `Refl`, iki taraf aynı değere indirgenebildiğinde eşitliğin kanıtını oluşturur:

```idris
zeroPlus : (n : Nat) -> 0 + n = n
zeroPlus n = Refl
```

Burada fonksiyon her `n` için $0+n=n$ önermesinin kanıtını üretir. Daha karmaşık eşitliklerde örüntü eşleme ve tümevarım kullanılır. Dolayısıyla fonksiyon yazmak ile teorem kanıtlamak arasındaki çizgi neredeyse tamamen silinir.

## Her şeyi tipe taşımak iyi mi?

Bağımlı tipler güçlüdür; ancak bedelsiz değildir. Karmaşık kanıtlar hata mesajlarını büyütebilir, geliştirme süresini uzatabilir ve okunabilirliği azaltabilir. Ayrıca tip sistemi genellikle programların sonlandığını doğrulamak zorundadır; sonsuz özyineleme, mantıksal tutarlılığı bozabilir.

En iyi yaklaşım, kritik kuralları tipe taşımaktır: protokol durumları, dizi boyutları, yetkilendirme koşulları veya para birimleri buna iyi adaylardır. Dependent Types dünyasında derleyici yalnızca “Bu kod çalışır mı?” diye sormaz; “Bu kod, iddia ettiğin matematiksel sözleşmeyi gerçekten yerine getiriyor mu?” diye de sorar. İşte eğlence—oraya göre hafif bir varoluş krizi—tam burada başlar.

---
layout: post
title: "Ada ile Güvenlik Kritik Sistem Programlama: Uçuşa Hazır Kodun Dili"
math: true
categories: 
  - Bilgi
tags: 
  - ada
  - gömülü sistemler
  - havacılık
  - güvenlik kritik yazılım
---

Bir uçakta yazılımın küçük bir hatası yalnızca uygulamanın çökmesi anlamına gelmez; yanlış sensör verisi, geciken bir kontrol komutu veya öngörülemez bellek davranışı ciddi sonuçlar doğurabilir. Ada, tam bu nedenle tasarlanmış bir programlama dilidir: derleme zamanında hataları yakalamayı, eşzamanlı görevleri disiplinli biçimde yönetmeyi ve yazılımın davranışını denetlenebilir hâle getirmeyi hedefler. Havacılık, uzay, demiryolu ve savunma gibi alanlarda Ada; “önce doğru çalışsın, sonra hızlı olsun” yaklaşımının güçlü bir temsilcisidir.
``

## Neden Ada?

Ada'nın temel felsefesi, hatayı mümkün olduğunca erken aşamada durdurmaktır. C veya C++ gibi dillerde aynı temel türde tutulan iki sayısal değerin anlamları birbirine karışabilir. Örneğin irtifa ile hız, ikisi de `float` olduğunda yanlışlıkla toplanabilir. Ada'da ise anlamı farklı kavramlar için ayrı türler tanımlanır. Bu, **tip güvenliği** sayesinde mantıksal hataların derleme aşamasında görünür olmasını sağlar.

Güvenlik kritik geliştirmede hedef yalnızca “hata sayısını azaltmak” değildir. Amaç, sistemin hata durumundaki davranışını da sınırlamaktır. Basit bir güvenilirlik modeliyle bunu şöyle düşünebiliriz:

$$R_{sistem} = R_{donanım} \times R_{yazılım} \times R_{iletişim}$$

Bileşenlerden birinin güvenilirliği düştüğünde toplam güvenilirlik de düşer. Ada, özellikle yazılım bileşenindeki belirsizliği azaltmak için güçlü tür sistemi, aralık denetimi, sözleşmeler ve kontrollü eşzamanlılık sunar.

| Özellik | Ada | Geleneksel düşük seviye yaklaşım |
|---|---|---|
| Türler | Anlamsal olarak ayrıştırılabilir | Sıklıkla ortak sayısal türler kullanılır |
| Dizi sınırları | Çalışma zamanında denetlenebilir | Taşma riski geliştiricinin sorumluluğundadır |
| Eşzamanlılık | Dilin yerleşik parçasıdır | Kütüphane ve işletim sistemi bağımlıdır |
| Sözleşmeler | Ön/son koşullar desteklenir | Genellikle elle yazılan denetimler gerekir |
| Sertifikasyon | DO-178C ekosistemiyle uyumludur | Süreç ve araç seçimi daha dağınık olabilir |

## Tip Güvenliği: Birim Hatasına Karşı Kalkan

Ada'da tür tanımı yalnızca veri boyutunu değil, verinin anlamını da ifade eder. Aşağıdaki örnekte metre ve kilometre kavramları bilinçli olarak ayrılmıştır:

```ada
type Metre is range 0 .. 20_000;
type Kilometre is range 0 .. 20;

Irtifa : Metre := 12_000;
Menzil : Kilometre := 8;

-- Irtifa := Menzil; -- Derleme hatası: türler uyumsuz
```

Bu kod, metre cinsinden irtifaya yanlışlıkla kilometre değeri atamayı engeller. Dahası, `Metre` türünün aralığı dışına çıkılmaya çalışılırsa Ada bir `Constraint_Error` üretir. Güvenlik kritik tasarımda bu istisna “beklenmedik sürpriz” değil, sistem mimarisinde ele alınması gereken açık bir hata yoludur.

Örneğin fiziksel bir değer için güvenli sınır şudur:

$$0 \leq h \leq 20\,000\text{ m}$$

Bu sınırın tür tanımında bulunması, dokümantasyon ile kod arasındaki mesafeyi azaltır.

## Sözleşmelerle Davranışı Belirtmek

Ada 2012 ile gelen sözleşmeler, bir alt programın ne beklediğini ve ne garanti ettiğini kodun üzerinde ifade eder. Bu yaklaşım, test senaryoları ve gereksinim izlenebilirliği için de çok değerlidir.

```ada
function Guvenli_Tirmanis_Hizi
  (Mevcut_Hiz : Integer;
   Maksimum_Hiz : Integer) return Integer
with
  Pre  => Mevcut_Hiz >= 0 and Maksimum_Hiz > 0,
  Post => Guvenli_Tirmanis_Hizi'Result >= 0
          and Guvenli_Tirmanis_Hizi'Result <= Maksimum_Hiz;
```

Burada `Pre`, fonksiyon çağrılmadan önce sağlanması gereken koşulları; `Post` ise dönüş değerinin garantilerini tanımlar. Gereksinim cümlesi doğrudan yürütülebilir bir ifadeye yaklaşır: “Çıkış hızı negatif olmayacak ve üst limiti geçmeyecek.”

## Görev Güvenliği ve Eşzamanlılık

Uçuş kontrol sistemleri aynı anda sensör okumalı, aktüatörleri güncellemeli ve sağlık kontrolleri yürütmelidir. Ada'nın `task` yapısı bu işleri dil düzeyinde modeller. Rastgele paylaşılan bellek yerine korumalı nesneler (`protected object`) kullanmak, yarış koşullarını azaltır.

| Risk | Ada mekanizması | Kazanım |
|---|---|---|
| Yarış koşulu | Protected object | Kontrollü karşılıklı dışlama |
| Zamanlama karmaşası | Task ve rendezvous | Açık iletişim modeli |
| Geçersiz değer | Range ve subtype | Erken hata yakalama |
| Belirsiz arayüz | Package specification | Net modül sözleşmesi |

Ada tek başına sertifikasyon belgesi değildir; doğru mimari, test, statik analiz ve izlenebilirlik yine zorunludur. Ancak SPARK alt kümesi ve kanıt araçlarıyla birleştiğinde, taşma, null erişim ve sözleşme ihlali gibi pek çok hatanın testten önce matematiksel olarak incelenmesini sağlar. Sonuçta Ada, gömülü yazılımda sadece kod yazmak için değil, yazılımın güvenli davranışını savunabilmek için seçilen bir dildir.

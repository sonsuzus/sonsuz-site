---
layout: post
title: "Görünmez Öğretmen: Oyun Tasarımında Zımni Öğretim"
math: true
categories: 
  - Bilgi
tags: 
  - oyun tasarımı
  - seviye tasarımı
  - zımni öğretim
  - oyuncu deneyimi
  - game design
  - çevresel anlatım
toc: true
image: /img/gorunmez-ogretmen-oyun-29.png
---

Bir oyun size ekrana kocaman bir pencere açıp “Zıplamak için Space tuşuna bas!” demeden zıplamayı öğretebilir mi? Elbette. Hatta iyi tasarlanmış bir oyun, kurallarını açıktan anlatmak yerine merakınızı, çevreyi okuma yeteneğinizi ve deneme isteğinizi kullanır. İşte oyuncunun farkında olmadan öğrendiği bu yaklaşım, **zımni öğretim** veya İngilizce adıyla *implicit tutorial* olarak bilinir.

![gorunmez-ogretmen-oyun-29](/img/gorunmez-ogretmen-oyun-29.svg)

``
## Zımni öğretim nedir?

Zımni öğretim, oyunun mekaniklerini metin kutuları veya uzun açıklamalar yerine **seviye düzeni, görsel ipuçları, güvenli deneyler ve sonuçlar** aracılığıyla öğretmesidir. Tasarımcı oyuncuya doğrudan ne yapacağını söylemez; doğru davranışı keşfedebileceği kontrollü bir durum hazırlar.

Bu yaklaşımın temel döngüsü şöyle modellenebilir:

$$Gözlem \rightarrow Deneme \rightarrow Geri\ Bildirim \rightarrow Öğrenme$$

Örneğin oyuncunun önüne küçük bir çukur yerleştirilir. İlerlemek için zıplaması gerekir; fakat çukur ölümcül değildir. Oyuncu düşse bile kolayca geri çıkabilir. Böylece oyun hem zıplama gereksinimini gösterir hem de hata yapmayı cezalandırmadan denemeye izin verir.

## Açık ve zımni öğretimin farkı

| Özellik | Açık öğretim | Zımni öğretim |
|---|---|---|
| Bilgi aktarımı | Metin, ses veya tuş göstergesi | Seviye ve çevre düzeni |
| Oyuncunun rolü | Talimatı uygulamak | Kuralı keşfetmek |
| Akışa etkisi | Oyunu durdurabilir | Oynanışla bütünleşir |
| Hatırlanabilirlik | Okunan bilgi unutulabilir | Deneyimlenen bilgi daha kalıcıdır |
| Risk | Bilgi bombardımanı | İpucunun anlaşılmaması |

Zımni öğretim her durumda üstün değildir. Karmaşık envanter sistemleri veya erişilebilirlik seçenekleri açık açıklamalar gerektirebilir. İyi tasarım, iki yaklaşımı rakip değil tamamlayıcı araçlar olarak görür.

## Seviye tasarımı nasıl öğretmene dönüşür?

İlk yöntem **odak yönetimidir**. Işık, renk, hareket ve mimari çizgiler oyuncunun bakışını önemli noktaya taşır. Karanlık bir koridordaki tek parlak kapı, üzerinde “Buraya git” yazmasa da oldukça konuşkandır.

İkinci yöntem, yeni mekaniği güvenli bir ortamda tanıtmaktır. Oyuncu patlayan bir varili ilk kez düşmansız bir odada görürse ona ateş ederek sonucunu inceleyebilir. Daha sonra aynı varil düşmanların yanında kullanıldığında oyuncu bağlantıyı kendisi kurar.

Öğrenme başarısını basitçe şu şekilde düşünebiliriz:

$$Öğrenme = İpucuNetliği \times DenemeFırsatı \times GeriBildirimGücü$$

Çarpanlardan biri sıfıra yaklaşırsa öğretim de zayıflar. Parlayan bir nesne dikkat çekebilir; ancak oyuncu onunla etkileşime giremiyorsa anlamlı öğrenme oluşmaz.

## Küçük bir tasarım örneği

Bir platform oyununda duvardan zıplama mekaniğini tanıttığımızı varsayalım. Seviyenin davranışı aşağıdaki sözde kodla ifade edilebilir:

```text
oyuncu öğretim_odasına_girince:
    çıkışı yüksek bir noktaya yerleştir
    iki zıplanabilir duvarı karşılıklı konumlandır
    düşülen zemini güvenli yap

oyuncu duvara temas edince:
    karakteri kısa süre duvara tutundur
    görsel parçacık ve ses geri bildirimi üret

oyuncu çıkışa ulaşınca:
    aynı mekaniği düşük riskli bir engelde tekrar kullan
```

Bu kod gerçek bir oyun motoruna bağlı değildir; tasarımın mantığını gösterir. Yüksek çıkış hedefi belirler, karşılıklı duvarlar çözüm alanını sınırlar, güvenli zemin ise korkmadan denemeyi sağlar. Parçacık ve ses, duvarın özel bir davranış sunduğunu bildirir.

## Tasarımcının görünmez eli

Başarılı bir zımni öğretimde oyuncu “Tasarımcı bana bunu öğretti” demez; “Ben bunu çözdüm!” der. Bu sahiplenme duygusu motivasyonu artırır. Ancak ipuçları fazla belirgin olursa keşif hissi kaybolur, fazla belirsiz olursa oyuncu sıkışır.

Bu nedenle iyi bir seviye önce mekaniği **gösterir**, sonra güvenle **denetir**, ardından farklı bir bağlamda **sınar**. Oyuncu kuralları okumak yerine yaşar. Görünmez öğretmenin en büyük başarısı da ders verdiğini hiç belli etmemesidir.

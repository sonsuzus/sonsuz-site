---
layout: post
title: "Oyunlarda Ahlaki Seçimler: Kahraman mı, Kaos Ajanı mı?"
math: true
categories: 
  - Bilgi
tags: 
  - oyun tasarımı
  - oyuncu psikolojisi
  - ahlaki seçimler
  - karar verme
  - davranış bilimi
  - oyun geliştirme
toc: true
image: /img/oyunlarda-ahlaki-secimler-88.png
---

![oyunlarda-ahlaki-secimler-88](/img/oyunlarda-ahlaki-secimler-88.svg)


Bir oyun size yanan bir köyü kurtarmak ile değerli ganimetin peşinden gitmek arasında seçim sunduğunda, yalnızca ekrandaki karakterin geleceğine karar vermezsiniz. Empati, merak, ödül beklentisi ve kendi değerleriniz aynı anda devreye girer. Ahlaki seçim sistemleri bu nedenle basit bir hikâye süsü değil, oyuncunun kendisiyle pazarlık yapmasını sağlayan güçlü tasarım araçlarıdır.
``

## İyi ve kötü arasında bir sayaç

Klasik ahlak sistemleri, davranışları tek boyutlu bir eksene yerleştirir. Bir sivili kurtarmak puan kazandırırken masum bir karakteri soymak puan kaybettirebilir. Oyuncunun ahlaki durumu matematiksel olarak şöyle modellenebilir:

$$M_{t+1} = \operatorname{clamp}(M_t + w_a \cdot A_t, -100, 100)$$

Burada $M_t$ mevcut ahlak puanını, $A_t$ seçimin yönünü, $w_a$ ise davranışın önemini temsil eder. Örneğin küçük bir yalan $-2$, bir şehri kurtarmak $+40$ değerinde olabilir.

Bu yöntem anlaşılırdır; ancak ahlakı muhasebe tablosuna dönüştürme riski taşır. Oyuncu, “Doğru olan nedir?” yerine “En iyi yeteneği açmak için kaç iyilik puanı gerekiyor?” diye düşünmeye başlayabilir.

| Sistem | Oyuncu düşüncesi | Güçlü yanı | Temel riski |
|---|---|---|---|
| İyi-kötü ölçeği | Hangi seçenek puan kazandırır? | Kolay anlaşılır | Ahlakı mekanikleştirir |
| Çok eksenli sistem | Kime ve hangi ilkeye sadığım? | Daha nüanslıdır | Takibi zorlaşabilir |
| Gizli itibar | Dünya beni nasıl görüyor? | Doğal hissettirir | Sonuçlar belirsiz kalabilir |
| Sonuç odaklı sistem | Bu karar ileride ne doğuracak? | Güçlü dramatik etki yaratır | Oyuncu sonucu öngöremeyebilir |

## Oyuncu neden “iyi” olmayı seçer?

Araştırmalar ve oyuncu davranışları, birçok kişinin ilk oynayışında kendi değerlerine yakın seçimler yaptığını gösterir. Bunun nedenlerinden biri, dijital karakterlerle kurulan empatidir. Sanal bir karakter üzülse bile oyuncunun hissettiği rahatsızlık gerçektir.

Karar verme sürecini basitleştirilmiş bir fayda modeliyle ifade edebiliriz:

$$U = R + E + I - C$$

Bu denklemde $R$ mekanik ödülü, $E$ duygusal tatmini, $I$ oyuncunun kimliğiyle uyumu ve $C$ beklenen maliyeti gösterir. Kötü seçenek daha fazla altın verse bile suçluluk hissi ve karakter kimliğiyle çelişmesi toplam faydayı düşürebilir.

İkinci oynayışta ise işler değişir. Oyuncu artık güvenli hikâyeyi bildiği için merak ağır basar: “Acaba herkese ihanet edersem ne olur?” Böylece oyun, ahlaki laboratuvara dönüşür. Gerçek hayatta denenmeyecek davranışlar düşük riskli bir ortamda keşfedilir.

## Daha inandırıcı bir sistem tasarlamak

Etkili bir ahlak sistemi, seçenekleri açıkça “iyi” ve “kötü” diye etiketlemek yerine çatışan değerler sunmalıdır. Bir kasabayı kurtarmak için tek bir masumu feda etmek, merhamet ile toplumsal faydayı karşı karşıya getirir. Bu durumda seçim değil, gerekçe ilginç hâle gelir.

Aşağıdaki örnek, kararları tek puan yerine merhamet, sadakat ve pragmatizm eksenlerinde değerlendirir:

```python
morality = {
    "merhamet": 0,
    "sadakat": 0,
    "pragmatizm": 0
}

def apply_choice(choice):
    effects = {
        "dusmani_affet": {"merhamet": 3, "pragmatizm": -1},
        "emri_uygula": {"sadakat": 2, "merhamet": -2},
        "kopruyu_yik": {"pragmatizm": 3, "sadakat": -1}
    }

    for trait, value in effects[choice].items():
        morality[trait] += value
```

Bu kod, her kararın birden fazla değeri aynı anda etkileyebilmesini sağlar. Böylece oyuncu “kötü” ilan edilmez; kararlarının oluşturduğu kişilik profiliyle karşılaşır. NPC diyalogları, görevler ve final sahneleri de baskın değerlere göre değiştirilebilir.

## Seçimlerin gerçek ağırlığı

Ahlaki kararların etkili olması için sonuçların yalnızca final videosunda değil, oyun dünyasında görünmesi gerekir. Kurtarılan bir çocuğun saatler sonra yardımcı olarak dönmesi veya terk edilen bir kasabanın harabeye dönüşmesi, oyuncuya kararının hatırlandığını hissettirir.

En başarılı sistemler oyuncuya parlayan bir iyilik rozeti dağıtmaz. Bunun yerine belirsizlik, gecikmiş sonuçlar ve çatışan değerler yaratır. Çünkü unutulmaz soru “Kaç ahlak puanı kazandım?” değil, “Doğru şeyi gerçekten yaptım mı?” sorusudur.

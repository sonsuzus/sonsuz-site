---
layout: post
title: "Teknoloji Determinizmi: Kodlarımız Bizi Ne Kadar Yeniden Yazıyor?"
math: true
categories: 
  - Bilgi
tags: 
  - teknoloji determinizmi
  - algoritmalar
  - yazılım etiği
  - toplum
toc: true
---

Bir sabah telefonunuzun önerdiği videoyu izleyip, navigasyonun çizdiği yoldan gidip, alışveriş uygulamasının hatırlattığı ürünü satın aldığınızda küçük bir soru belirir: Kararları gerçekten siz mi veriyorsunuz? Teknoloji determinizmi, teknolojik araçların yalnızca hayatı kolaylaştırmadığını; toplumun kurumlarını, kültürel normlarını ve bireysel alışkanlıklarını güçlü biçimde şekillendirdiğini savunan yaklaşımdır. Ancak bu yaklaşımın en tartışmalı kelimesi “zorunlu”dur.

``

## Teknoloji nötr bir çekiç değildir

Klasik teknoloji deterministlerine göre matbaa, ulus-devlet fikrinin yayılmasını; televizyon kitlesel kültürü; internet ise ağ toplumunu neredeyse kaçınılmaz biçimde doğurmuştur. Yazılım dünyasında bunun karşılığı, bir platformun teknik tasarımının kullanıcı davranışına sınırlar ve teşvikler koymasıdır. Örneğin sonsuz kaydırma, içeriğin doğal bir bitiş noktası olmamasını sağlar. Bildirim rozetleri ise dikkati tekrar uygulamaya çağırır.

Bir algoritmanın amacı çoğu zaman ölçülebilir bir hedefi eniyilemektir. Basitleştirilmiş biçimiyle:

$$\max_{a \in A} \; U(a) = \alpha \cdot E(a) + \beta \cdot R(a) - \gamma \cdot C(a)$$

Burada $E$ etkileşimi, $R$ geliri, $C$ ise maliyeti temsil edebilir. Sorun şudur: Sistem yalnızca etkileşimi artırmaya ayarlıysa, insanın uzun vadeli iyiliği hedef fonksiyonuna otomatik olarak girmez. Kod, niyet kadar metriklerin de hikâyesidir.

| Tasarım tercihi | Yakın davranışsal etki | Olası kültürel sonuç |
|---|---|---|
| Sonsuz akış | Daha uzun oturum süresi | Sabırsız tüketim alışkanlığı |
| Beğeni sayacı | Sosyal onay arayışı | Görünürlük odaklı iletişim |
| Kişiselleştirilmiş öneri | Tanıdık içeriğe yönelim | Filtre balonları |
| Uçtan uca şifreleme | Daha güvenli iletişim | Yeni mahremiyet beklentileri |

## Zorunluluk mu, karşılıklı şekillenme mi?

Determinist yorum ikna edicidir ama eksiktir. Aynı teknoloji, farklı toplumlarda farklı sonuçlar doğurabilir. Mesajlaşma uygulaması bir ülkede aile koordinasyonu için kullanılırken başka bir yerde politik örgütlenmenin altyapısına dönüşebilir. Bu nedenle daha dengeli yaklaşım, **teknolojinin toplumsal olarak şekillendiğini** söyler: Mühendisler, şirket modelleri, yasalar, kullanıcı pratikleri ve kültürel değerler teknolojinin etkisini birlikte üretir.

| Yaklaşım | Temel iddia | Yazılımcı için sonuç |
|---|---|---|
| Sert determinizm | Teknoloji toplumu belirler | Tasarım kararları çok büyük güç taşır |
| Sosyal şekillenme | Toplum teknolojiyi belirler | Bağlam ve kullanıcı topluluğu önemlidir |
| Karşılıklı etkileşim | İkisi birbirini dönüştürür | Sürekli ölçüm, geri bildirim ve düzeltme gerekir |

Örneğin öneri sistemini yazarken yalnızca tıklanma oranını izlemek kolaydır. Fakat çeşitlilik, tekrar oranı ve kullanıcı kontrolü gibi sinyaller eklenirse sistemin kültürel etkisi değişebilir:

```python
def skorla(icerik, kullanici):
    ilgi = tahmin_edilen_ilgi(icerik, kullanici)
    cesitlilik = konu_cesitliligi(icerik, kullanici.gecmis)
    tekrar_cezasi = benzerlik(icerik, kullanici.son_gordukleri)

    # Yalnızca tıklama değil, keşif ve yorgunluk da hesaba katılır.
    return 0.65 * ilgi + 0.25 * cesitlilik - 0.10 * tekrar_cezasi
```

Bu örnek kusursuz bir etik çözüm değildir; fakat “en yüksek etkileşim” varsayımının teknik bir zorunluluk olmadığını gösterir. Ağırlıklar $0.65$, $0.25$ ve $-0.10$; ürün ekibinin değer yargılarını temsil eder.

## Yazılım geliştiricinin sorumluluğu

Algoritmalar insanları robot gibi yönetmez; ama seçenekleri sıralar, varsayılanları belirler ve bazı davranışların maliyetini düşürür. Bu küçük yönlendirmeler milyonlarca kullanıcıda birikince kültürel evrimin parçası olur. Bu yüzden iyi mühendislik; performans, güvenlik ve ölçeklenebilirliğin yanında “Bu özellik hangi alışkanlığı normalleştiriyor?” sorusunu da sormalıdır.

Teknoloji determinizmi bize önemli bir uyarı verir: Kod yalnızca çalışan talimatlardan ibaret değildir. Fakat kader de değildir. Şeffaf metrikler, kullanıcıya seçim hakkı, bağımsız denetim ve farklı topluluklardan geri bildirim sayesinde yazılımın yönü değiştirilebilir. Kısacası algoritmaları biz yazıyoruz; ama onlar da günlük hayatımızın sonraki sürümünü yazıyor.

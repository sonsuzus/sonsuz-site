---
layout: post
title: "Bitmeyen Proje Sendromu: Bilişim Projelerinde Kapsam Kayması"
math: true
categories: 
  - Bilgi
tags: 
  - kapsam kayması
  - proje yönetimi
  - yazılım geliştirme
toc: true
---

Bir yazılım projesi düşünün: Başlangıçta yalnızca kullanıcıların görev oluşturacağı küçük bir uygulamadır. Sonra bildirimler, raporlar, yapay zekâ, karanlık tema ve hatta akıllı saat desteği istenir. Ekip çalıştığı hâlde bitiş çizgisi sürekli uzaklaşır. İşte bu durum, proje yönetiminin meşhur canavarı **kapsam kaymasıdır**.
``

## Kapsam kayması nedir?

Kapsam, bir projenin hangi ihtiyaçları karşılayacağını ve hangi çıktıları üreteceğini belirleyen sınırdır. **Kapsam kayması (scope creep)** ise onaylanmış bu sınırların; süre, bütçe ve kaynaklar uygun biçimde güncellenmeden genişlemesidir.

Her değişiklik kapsam kayması değildir. Kullanıcı geri bildirimlerine göre planlı değişiklik yapmak sağlıklıdır. Sorun, yeni taleplerin etkisi değerlendirilmeden projeye eklenmesidir. Küçük görünen istekler analiz, tasarım, geliştirme, test, dokümantasyon ve bakım maliyeti doğurur.

| Planlı kapsam değişikliği | Kapsam kayması |
|---|---|
| Etki analizi yapılır | Talep doğrudan geliştirmeye alınır |
| Süre ve bütçe güncellenir | Takvim değişmeden kalır |
| Öncelik açıkça belirlenir | Her özellik acil kabul edilir |
| Paydaş onayı alınır | Karar çoğunlukla sözlüdür |
| Başka işler kapsamdan çıkarılabilir | Kapsam yalnızca büyür |

## Proje neden tamamlanamaz hâle gelir?

Bir projenin temel kısıtları kapsam, zaman, maliyet ve kalitedir. Basitleştirilmiş biçimde iş yükünü şöyle düşünebiliriz:

$$W = \sum_{i=1}^{n}(G_i + T_i + D_i)$$

Burada $G_i$ geliştirme, $T_i$ test ve $D_i$ dokümantasyon eforudur. Yeni özellik sayısı $n$ arttıkça toplam iş yükü $W$ büyür. Üstelik özellikler birbirleriyle etkileştiğinde maliyet doğrusal değil, daha hızlı artabilir.

Ekibin haftalık üretim kapasitesi $V$, her hafta eklenen yeni iş miktarı $A$ olsun. Kalan iş miktarı yaklaşık olarak şu şekilde değişir:

$$R_{t+1} = R_t - V + A$$

Eğer $A \geq V$ ise ekip ne kadar çalışırsa çalışsın kalan işler azalmaz. Yazılım dünyasının koşu bandı tam olarak budur: Çok terlersiniz ama hedefe yaklaşamazsınız.

Kapsam büyüdükçe test senaryoları, bağımlılıklar ve hata ihtimali de artar. Sonuçta teslim tarihi ertelenir, teknik borç yükselir ve ekip motivasyonu düşer. Aceleyle geliştirilen özellikler mevcut mimariyi zorladığında kalite de sessizce feda edilir.

## Tehlikeyi erken gösteren işaretler

- Gereksinimler yazılı değil, toplantılarda sözlü biçimde değişiyorsa,
- Paydaşlar sürekli küçük eklemeler istiyorsa,
- Tamamlanma tanımı net değilse,
- Sprint sırasında işler sık sık değişiyorsa,
- Her talep yüksek öncelikli görünüyorsa,
- Takvim sabitken özellik listesi büyüyorsa kapsam kayması başlamış olabilir.

Basit bir kontrol mekanizması bile görünmez talepleri görünür hâle getirir:

```python
def talebi_degerlendir(efor, deger, kapasite):
    if efor > kapasite:
        return "Sonraki sürüme taşı"
    if deger / efor < 1.5:
        return "Önceliği yeniden değerlendir"
    return "Değişiklik kuruluna sun"
```

Bu örnek, talebin hemen kabul edilmesi yerine efor, değer ve kapasite açısından incelenmesini sağlar. Gerçek projelerde güvenlik, risk ve bağımlılık gibi ölçütler de değerlendirmeye eklenmelidir.

## Kapsam nasıl kontrol altında tutulur?

Öncelikle bir **kapsam bildirimi** hazırlanmalı; teslimatlar kadar kapsam dışındaki maddeler de yazılmalıdır. Ardından gereksinimler kabul kriterleriyle tanımlanmalı ve her değişiklik kayıt altına alınmalıdır.

| Yöntem | Sağladığı fayda |
|---|---|
| MVP belirlemek | En küçük değerli ürüne odaklanmayı sağlar |
| Değişiklik talep formu | İsteğin maliyetini görünür kılar |
| MoSCoW önceliklendirmesi | Zorunlu ve isteğe bağlı işleri ayırır |
| Ürün biriktirme listesi | Talepleri hemen yapmak yerine sıralar |
| Kapsam dondurma tarihi | Teslime yakın değişiklikleri sınırlar |

Yeni bir özellik istendiğinde doğru cevap doğrudan hayır demek değildir. Bunun yerine, **Bu özelliği eklersek neyi çıkarıyoruz veya teslim tarihini ne kadar değiştiriyoruz?** diye sorulmalıdır. Böylece kapsam artışının bedeli görünür olur.

Kapsam kaymasını önlemek yeniliğe direnmek değil, değişimi bilinçli yönetmektir. Başarılı proje her özelliği içeren proje değil; doğru problemi, kabul edilebilir kaliteyle ve öngörülebilir sınırlar içinde çözen projedir.

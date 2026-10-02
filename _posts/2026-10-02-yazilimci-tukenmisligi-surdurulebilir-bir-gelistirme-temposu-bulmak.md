---
layout: post
title: "Yazılımcı Tükenmişliği: Sürdürülebilir Bir Geliştirme Temposu Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - yazılımcı tükenmişliği
  - burnout
  - üretkenlik
  - zaman yönetimi
  - yazılım geliştirme
  - mental sağlık
toc: true
image: /img/yazilimci-tukenmisligi-surdurulebilir-29.png
---

Bir yazılımcının zihni bazen tarayıcıdaki 47 sekmeye benzer: Üçünde dokümantasyon, beşinde hata kaydı, birinde yarım kalmış eğitim ve en az birinde nereden geldiği bilinmeyen müzik çalar. Sürekli öğrenme baskısı, yetişmeyen işler ve gece gelen hata bildirimleri birleştiğinde ortaya yalnızca yorgunluk değil, uzun süreli tükenmişlik çıkabilir. Çözüm daha hızlı koşmak değil; bitiş çizgisi olmayan bu maratonda sürdürülebilir bir tempo geliştirmektir.
``
## Tükenmişlik sadece yorulmak değildir

Normal yorgunluk dinlenince azalır. Tükenmişlikte ise uyku veya hafta sonu izni yeterli olmayabilir. Dünya Sağlık Örgütü yaklaşımıyla iş bağlamındaki tükenmişliğin üç önemli boyutu vardır: enerji kaybı, işe karşı zihinsel uzaklaşma ve mesleki yeterlilik hissinin azalması.

Bunu basitleştirilmiş bir modelle ifade edebiliriz:

$$B = \frac{T \times S \times K}{D + O}$$

Burada $B$ tükenmişlik riski, $T$ iş talebi, $S$ stres süresi, $K$ kontrol kaybı, $D$ dinlenme ve $O$ ise özerkliktir. Bu klinik bir formül değildir; önemli bir gerçeği görselleştirir: Talep ve stres büyürken dinlenme ile kontrol azalırsa risk hızla yükselir.

| Geçici yoğunluk | Sürdürülemez tempo |
|---|---|
| Belirli bir bitiş tarihi vardır | Yoğunluk normal çalışma biçimidir |
| Sonrasında dinlenme planlanır | Dinlenme sürekli ertelenir |
| Öncelikler nettir | Her görev acildir |
| Hatalar öğrenme fırsatıdır | Hatalar kişisel başarısızlık gibi görülür |

## Teknoloji treninin arkasından koşmayın

Her hafta yeni bir framework, yapay zekâ aracı veya JavaScript çalışma zamanı çıkabilir. Fakat sektörün tamamını öğrenmek bir kariyer hedefi değil, matematiksel olarak imkânsız bir yan görevdir. Öğrenilecek konuları üç gruba ayırın:

1. **Şimdi gerekli:** Mevcut projede doğrudan kullanılacak bilgiler.
2. **Yakında değerli:** Kariyer yönünüzle uyumlu, planlanabilir konular.
3. **Sadece ilginç:** Merak uyandıran fakat acil olmayan teknolojiler.

Öğrenme bütçenizi örneğin %70 mevcut uzmanlığa, %20 yakın alanlara ve %10 deneysel konulara ayırabilirsiniz. Böylece merakınızı öldürmeden FOMO etkisini sınırlandırırsınız.

## Bildirimler görev değil, kesintidir

Bir hata bildiriminin görünmesi, ona anında müdahale edilmesi gerektiği anlamına gelmez. Bildirimleri önem seviyesine göre yönlendiren basit bir kural sistemi kullanılabilir:

```python
def route_alert(severity, users_affected, work_hours):
    score = severity * 2 + min(users_affected / 100, 5)

    if score >= 9:
        return 'page-on-call'
    if work_hours and score >= 5:
        return 'team-channel'
    return 'next-business-day'
```

Bu örnek, hatanın teknik önemini ve etkilenen kullanıcı sayısını puanlayarak bildirim kanalını seçer. Amaç insanları robotlaştırmak değil; gerçekten acil olaylarla sabaha kadar bekleyebilecek sorunları ayırmaktır. Ekip içinde “acil” kelimesinin ölçülebilir bir tanımı bulunmalıdır.

## Sınır belirlemek profesyonelliktir

Sınırlar tembellik değil, sistem güvenilirliğinin insan tarafıdır. Çalışma saatlerini görünür kılın, mesai dışı bildirimleri kapatın ve nöbet görevlerini dönüşümlü dağıtın. Kapasite dolduğunda yeni bir görev için şu soruyu sorun: “Bunu eklersek mevcut işlerden hangisini çıkarıyoruz?”

| Zararlı alışkanlık | Sürdürülebilir alternatif |
|---|---|
| Her mesaja anında cevap vermek | İletişim blokları belirlemek |
| Öğle arasında kod yazmak | Ekrandan tamamen uzaklaşmak |
| Sürekli fazla mesai | Kapsam veya teslim tarihi görüşmek |
| İzin gününde sistemi kontrol etmek | Yetki devri ve nöbet planı yapmak |

## Yavaşlamak geride kalmak değildir

Sürdürülebilir tempo, her gün aynı miktarda üretmek anlamına gelmez. Bazı günler karmaşık bir hatayı çözersiniz, bazı günler yalnızca düşünürsünüz. Haftalık olarak enerji düzeyinizi, kesinti sayısını ve mesai süresini kaydedin. Düşük enerji birkaç hafta devam ediyorsa bunu bireysel irade problemi olarak değil, sistem sinyali olarak değerlendirin.

Tükenmişlik belirtileri günlük yaşamı etkiliyorsa yöneticinizle konuşmak, iş yeri desteğine başvurmak veya bir ruh sağlığı uzmanından yardım almak önemlidir. En iyi geliştirici sürekli çalışan değil; dinlenebilen, sınır koyabilen ve uzun vadede üretmeye devam edebilen geliştiricidir.

![yazilimci-tukenmisligi-surdurulebilir-29](/img/yazilimci-tukenmisligi-surdurulebilir-29.svg)


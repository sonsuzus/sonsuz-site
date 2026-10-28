---
layout: post
title: "Akıllı Evlerde Hayalet Komutlar: Sesli Asistanlar Neden Yanlış Tetikleniyor?"
math: true
categories: 
  - Bilgi
tags: 
  - akıllı ev
  - ses tanıma
  - siber güvenlik
  - yapay zeka
  - iot
  - mahremiyet
toc: true
image: /img/akilli-evlerde-hayalet-17.png
---

Televizyondaki bir karakterin söylediği sıradan bir cümle yüzünden ışıkların kapanması komik görünebilir. Ancak aynı yanlış anlaşılma kapının kilidini açıyor, alarmı devre dışı bırakıyor veya özel bir konuşmayı buluta gönderiyorsa mesele artık teknolojik bir şakadan ibaret değildir. Akıllı evlerde sesli komutların yanlış tetiklenmesi, kullanılabilirlik ile güvenlik arasındaki hassas dengeyi doğrudan etkileyen önemli bir tasarım problemidir.

![akilli-evlerde-hayalet-17](/img/akilli-evlerde-hayalet-17.svg)

``

## Sesli asistan gerçekte neyi dinliyor?

Akıllı hoparlörler genellikle konuşmaların tamamını sürekli olarak buluta iletmez. Bunun yerine cihaz üzerinde çalışan düşük güçlü bir model, “Hey Asistan” gibi **uyandırma sözcüğünü** arar. Model yeterince yüksek bir güven skoru üretirse asıl ses kaydı işlenmeye başlanır.

Bu karar basitçe şöyle gösterilebilir:

$$
Karar = \begin{cases}
Tetikle, & p(uyandırma\ sözcüğü \mid ses) \geq \theta \\
Bekle, & p(uyandırma\ sözcüğü \mid ses) < \theta
\end{cases}
$$

Buradaki $\theta$, sistemin karar eşiğidir. Eşik düşürülürse kullanıcı asistanı daha kolay uyandırır; fakat televizyon sesi, benzer kelimeler ve arka plan konuşmaları da komut sanılabilir. Eşik yükseltildiğinde yanlış tetiklenmeler azalırken gerçek komutların kaçırılma ihtimali artar.

| Eşik ayarı | Yanlış tetiklenme | Gerçek komutu kaçırma | Kullanıcı deneyimi |
|---|---:|---:|---|
| Düşük | Yüksek | Düşük | Hızlı fakat huzursuz |
| Dengeli | Orta | Orta | Çoğu ev için uygun |
| Yüksek | Düşük | Yüksek | Güvenli fakat yorucu |

Bu ilişki, istatistikte **yanlış pozitif** ve **yanlış negatif** kavramlarıyla açıklanır. Yanlış pozitif, asistanın söylenmeyen bir komutu var sanmasıdır. Yanlış negatif ise gerçekten verilen komutu algılayamamasıdır.

## Neden yanlış tetiklenir?

Başlıca nedenler arasında fonetik benzerlik, televizyon ve radyo sesleri, yankılı odalar, çocukların tiz konuşmaları, farklı aksanlar ve düşük kaliteli mikrofonlar bulunur. Ayrıca ses tanıma modeli belirli yaş veya dil gruplarını yeterince temsil etmeyen verilerle eğitilmiş olabilir.

Saldırganlar da bu zayıflıklardan yararlanabilir. İnsan kulağında anlamsız veya zor fark edilen seslerin içine komut gizlenmesi, **adversarial audio** saldırısı olarak bilinir. Açık bir pencereden, televizyondaki videodan ya da ele geçirilmiş bir IoT cihazından yayılan ses teorik olarak asistana komut verebilir.

## Güvenlik ve mahremiyet etkileri

Her komut aynı risk düzeyine sahip değildir. Müziğin yanlışlıkla başlaması yalnızca can sıkıcıyken akıllı kilit, garaj kapısı, kamera veya alarm üzerinde işlem yapılması fiziksel güvenlik riski oluşturur. Yanlış tetiklenme sonrasında kaydedilen konuşmanın buluta gönderilmesi de mahremiyet sorununa dönüşebilir.

| İşlem | Olası sonuç | Önerilen doğrulama |
|---|---|---|
| Işığı açma | Düşük risk | Tek sesli komut |
| Alışveriş yapma | Finansal kayıp | PIN veya uygulama onayı |
| Kapı kilidini açma | Fiziksel erişim | Telefon ve biyometri |
| Alarmı kapatma | Kritik güvenlik açığı | Çok faktörlü doğrulama |

## Basit bir risk tabanlı kontrol

Aşağıdaki Python örneği, komutun güven skoru ile işlem riskini birlikte değerlendirir. Kritik işlemlerde yalnızca ses tanımaya güvenmek yerine ikinci doğrulama ister:

```python
def komutu_degerlendir(guven_skoru, risk_seviyesi):
    esikler = {"dusuk": 0.70, "orta": 0.85, "yuksek": 0.95}

    if guven_skoru < esikler[risk_seviyesi]:
        return "Komut reddedildi"

    if risk_seviyesi == "yuksek":
        return "Telefon üzerinden ek onay gerekli"

    return "Komut uygulanabilir"

print(komutu_degerlendir(0.92, "yuksek"))
```

Bu yaklaşım, güvenliği yalnızca model doğruluğuna bırakmaz; işlemin muhtemel zararını da hesaba katar.

## Daha güvenli bir akıllı ev için

Kullanıcılar ses kayıt geçmişini düzenli olarak kontrol etmeli, gereksiz satın alma özelliklerini kapatmalı ve kritik cihazları ayrı bir IoT ağına yerleştirmelidir. Üreticiler ise yerel ses işleme, kişiye özel konuşmacı doğrulama, görünür kayıt göstergeleri ve kolay erişilen fiziksel mikrofon düğmeleri sunmalıdır.

Kusursuz ses tanıma gerçekçi olmayabilir. En sağlam çözüm, sistemin hata yapacağını kabul edip sonuçları sınırlandırmaktır. Başka bir deyişle iyi bir akıllı ev, yalnızca sahibini anlayan değil, emin olmadığında “Bunu gerçekten yapmak istiyor musunuz?” diye sorabilen evdir.

---
layout: post
title: "Prosedürel Anlatı ve Dinamik Hikâye Motorları Nasıl Çalışır?"
math: true
categories: 
  - Bilgi
tags: 
  - prosedürel anlatı
  - oyun geliştirme
  - dinamik hikâye
  - yapay zekâ
  - oyuncu seçimi
  - durum makineleri
toc: true
image: /img/prosedurel-anlati-ve-26.png
---

![prosedurel-anlati-ve-26](/img/prosedurel-anlati-ve-26.svg)


Bir oyunda verdiğiniz masum bir kararın saatler sonra bir krallığın çökmesine yol açtığını düşünün. Bu sonuç önceden yazılmış tek bir senaryodan değil, seçimlerinizi değerlendiren dinamik bir hikâye motorundan doğabilir. Prosedürel anlatı; karakterleri, olayları ve sonuçları belirli kurallar doğrultusunda birleştirerek her oyuncuya farklı bir hikâye deneyimi sunmayı amaçlar.

``

## Prosedürel anlatı nedir?

Geleneksel anlatıda yazar, olayların sırasını büyük ölçüde önceden belirler. Oyuncu bazen farklı yollar seçse de bunlar çoğunlukla elle yazılmış dallardır. Prosedürel anlatıda ise yazar yalnızca olayları değil, **olay üretme kurallarını** da tasarlar.

Bir hikâye motorunun kararını basitçe şöyle modelleyebiliriz:

$$
S_{t+1} = F(S_t, A_t, R)
$$

Burada $S_t$ mevcut dünya durumunu, $A_t$ oyuncunun eylemini, $R$ anlatı kurallarını ve $S_{t+1}$ yeni durumu temsil eder. Örneğin oyuncu bir tüccarı soyarsa para miktarı artabilir; fakat itibar düşer, muhafızların şüphe seviyesi yükselir ve tüccarın ailesi ileride intikam görevi başlatabilir.

| Yaklaşım | Hikâye yapısı | Avantajı | Riski |
|---|---|---|---|
| Doğrusal anlatı | Sabit olay sırası | Güçlü tempo ve dramatik kontrol | Düşük tekrar oynanabilirlik |
| Dallanan anlatı | Önceden yazılmış seçim yolları | Anlamlı ve kontrollü kararlar | Dal sayısı hızla büyür |
| Prosedürel anlatı | Kurallarla üretilen olaylar | Yüksek çeşitlilik | Tutarsız veya anlamsız sonuçlar |
| Hibrit sistem | Yazılmış sahneler ve dinamik kurallar | Kontrol ile özgürlük arasında denge | Tasarımı ve testi zordur |

## Durum değişkenleri ve koşullar

Dinamik hikâye motorlarının hafızası, durum değişkenlerinden oluşur. İtibar, korku, sadakat, kaynak miktarı ve karakter ilişkileri bu değişkenlere örnektir. Motor, uygun olayları seçerken koşulları kontrol eder.

Aşağıdaki Python örneği, dünya durumuna göre yeni bir anlatı olayı seçer:

```python
import random

def uygun_olaylari_bul(durum, olaylar):
    uygunlar = []

    for olay in olaylar:
        kosullar = olay["kosullar"]
        if all(durum.get(anahtar, 0) >= deger
               for anahtar, deger in kosullar.items()):
            uygunlar.append(olay)

    return uygunlar

def olay_sec(durum, olaylar):
    uygunlar = uygun_olaylari_bul(durum, olaylar)
    return random.choice(uygunlar) if uygunlar else None

olaylar = [
    {"ad": "Köylülerin İsyanı", "kosullar": {"korku": 70}},
    {"ad": "Kraliyet Daveti", "kosullar": {"itibar": 60}},
    {"ad": "Gizemli Tüccar", "kosullar": {"altin": 20}}
]
```

`uygun_olaylari_bul` fonksiyonu, koşulları sağlanan olayları filtreler. `olay_sec` ise bunlardan birini rastgele seçer. Gerçek bir motorda rastgelelik genellikle ağırlıklıdır; önemli olayların seçilme ihtimali daha yüksek tutulabilir.

Bir olayın puanı şu şekilde hesaplanabilir:

$$
P(o) = w_rR + w_dD + w_cC - w_tT
$$

Burada $R$ rastgelelik, $D$ dramatik değer, $C$ mevcut durumla uyum ve $T$ yakın zamanda tekrar edilme cezasıdır. $w$ katsayıları tasarımcının hangi özelliğe önem verdiğini belirler.

## Anlamlı seçim nasıl üretilir?

Her seçimin dünyayı değiştirmesi gerekmez; ancak oyuncu, kararının fark edildiğini hissetmelidir. İyi bir sistem üç katmanda tepki verir:

1. **Anlık sonuç:** Karakter hemen kızar veya ödül verir.
2. **Sistemsel sonuç:** İtibar, ekonomi ya da ilişki değeri değişir.
3. **Gecikmiş sonuç:** Eski karar, saatler sonra yeni bir görev veya düşman üretir.

Buradaki en büyük tehlike, sayısız ama yüzeysel seçenek sunmaktır. Beş anlamsız düğme yerine, bedeli açık olmayan iki güçlü seçenek genellikle daha etkilidir. Ayrıca sistemin tamamen kontrolsüz olması komik tutarsızlıklar doğurabilir: Dün ölen kralın bugün oyuncuya mektup göndermesi gibi!

## Tasarımcı hâlâ hikâyenin yazarı mı?

Evet; fakat artık yalnızca sahneleri değil, olasılık uzayını da yazar. Karakterlerin hedeflerini, dünyanın sınırlarını ve hangi olayların birlikte anlamlı olduğunu tanımlar. Böylece motor doğaçlama yaparken temadan kopmaz.

Başarılı bir dinamik hikâye motoru, matematiksel kurallar ile insan yaratıcılığını birleştirir. Amaç sonsuz içerik üretmek değil, oyuncunun seçimlerinin hatırlandığına ve dünyanın gerçekten karşılık verdiğine inanmasını sağlamaktır.

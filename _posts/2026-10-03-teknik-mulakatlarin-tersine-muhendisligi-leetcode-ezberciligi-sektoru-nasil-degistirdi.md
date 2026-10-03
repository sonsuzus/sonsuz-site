---
layout: post
title: "Teknik Mülakatların Tersine Mühendisliği: LeetCode Ezberciliği Sektörü Nasıl Değiştirdi?"
math: true
categories: 
  - Bilgi
tags: 
  - teknik mülakat
  - leetcode
  - algoritma
  - yazılım kariyeri
  - işe alım
  - problem çözme
toc: true
image: /img/teknik-mulakatlarin-tersine-80.png
---

Modern teknik mülakat, adayın günlük işte nasıl yazılım geliştireceğini ölçen bir süreç olmaktan çıkıp kendine özgü kuralları bulunan paralel bir sektöre dönüştü. Artık bir API tasarlayabilmek, hatalı üretim kaydını incelemek veya anlaşılır kod yazmak bazen yeterli değil; adaydan kırk dakikada daha önce görmüş olmasının büyük avantaj sağladığı olimpiyat tarzı bir bulmacayı çözmesi bekleniyor. Böylece mülakatı geçme becerisi ile işi yapma becerisi arasındaki bağ giderek zayıflıyor.


![teknik-mulakatlarin-tersine-80](/img/teknik-mulakatlarin-tersine-80.svg)

``

## Ölçülmek İstenen Şey Neydi?

Algoritma sorularının çıkış noktası bütünüyle mantıksız değildi. Şirketler özgeçmişten bağımsız, standartlaştırılabilir ve hızlı değerlendirilebilir bir yöntem arıyordu. Veri yapıları üzerinden adayın problemi parçalaması, karmaşıklık analizi yapması ve baskı altında iletişim kurması ölçülebilirdi.

Bir algoritmanın maliyeti kabaca

$$T(n) = a \cdot n^2 + b \cdot n + c$$

ise büyük girdilerde baskın terim nedeniyle $T(n) = O(n^2)$ denir. Bu bilgiyi anlamak değerlidir. Sorun, karmaşıklık kavramını bilmekle yüzlerce soru kalıbını ezberlemenin aynı şey sayılmasıdır.

| Değerlendirme yöntemi | Ölçtüğü güçlü taraf | Kaçırabileceği beceri |
|---|---|---|
| LeetCode sorusu | Algoritmik örüntü tanıma | Bakımı kolay kod yazma |
| Eve verilen proje | Uygulama ve araştırma | Zaman baskısında düşünme |
| Sistem tasarımı | Mimari kararlar | Kodlama ayrıntıları |
| Eşli çalışma | İletişim ve hata ayıklama | Bağımsız çalışma biçimi |
| Geçmiş proje incelemesi | Gerçek deneyim | Deneyimsiz adayın potansiyeli |

## Mülakatın Tersine Mühendisliği

Bir ölçüm sistemi yaygınlaştığında insanlar doğal olarak sistemi optimize eder. Adaylar soru bankalarını tarar, şirketlere göre listeler çıkarır ve “sliding window”, “two pointers” ya da “dynamic programming” sinyallerini tanımayı öğrenir. Başarı olasılığını basitleştirerek şöyle düşünebiliriz:

$$P(başarı) \approx f(temel\ bilgi,\ kalıp\ aşinalığı,\ stres\ yönetimi)$$

Kalıp aşinalığının katsayısı gereğinden fazla büyüdüğünde süreç, problem çözme sınavından tanıma testine dönüşür. Örneğin aşağıdaki kod iki toplam problemini verimli çözer:

```python
def iki_toplam(sayilar, hedef):
    gorulen = {}
    for indis, sayi in enumerate(sayilar):
        gereken = hedef - sayi
        if gereken in gorulen:
            return gorulen[gereken], indis
        gorulen[sayi] = indis
    return None
```

Sözlük kullanımı sayesinde çözümün zaman karmaşıklığı ortalama $O(n)$ olur. Bu yaklaşımı neden seçtiğini açıklayan aday güçlü bir sinyal verebilir. Fakat çözümü dün ezberleyen aday ile temel ilkelerden üreten adayı kısa bir görüşmede ayırmak zordur.

## Şirketler İçin Görünmeyen Maliyet

Yanlış negatif, işi başarıyla yapabilecek bir adayın elenmesidir. Yanlış pozitif ise bulmacalarda başarılı olup ekip çalışması, ürün düşüncesi veya kod kalitesi konusunda yetersiz kalan adaydır. Her iki hata da pahalıdır.

Üstelik yoğun hazırlık gereksinimi fırsat eşitsizliği yaratır. Tam zamanlı çalışan, bakım sorumluluğu bulunan ya da aylarca ücretsiz hazırlanamayacak adaylar dezavantajlıdır. Şirket böylece en iyi mühendisi değil, hazırlığa en fazla kaynak ayırabileni seçebilir. Görüşmecilerin soru hazırlama, oturum yürütme ve geri bildirim yazma süresi de toplam işe alım maliyetine eklenir.

## Daha Gerçekçi Bir Sistem Mümkün mü?

Çözüm algoritmaları tamamen çöpe atmak değildir. Rol gerçekten düşük gecikmeli sistemler, derleyiciler veya arama altyapısı içeriyorsa derin algoritma bilgisi anlamlıdır. Ancak değerlendirme işin kendisiyle orantılı olmalıdır.

Daha dengeli bir süreç; kısa bir temel kodlama sorusu, mevcut koddaki hatayı bulma, küçük bir tasarım tartışması ve adayın geçmiş kararlarını inceleme aşamalarını birleştirebilir. Sorular önceden tanımlanmış ölçütlerle puanlanmalı; yalnızca doğru sonuç değil, varsayımlar, testler, iletişim ve okunabilirlik de değerlendirilmelidir.

Teknik mülakatın amacı en hızlı bulmaca çözücüyü bulmak değil, belirsizlik içinde güvenilir yazılım üretecek kişiyi tanımaktır. Sektör ölçtüğü şeyi yeniden düşünmezse adaylar oyunu oynamayı öğrenmeye devam edecek; şirketler ise oyunda iyi olanlarla işte iyi olanları karıştıracaktır.

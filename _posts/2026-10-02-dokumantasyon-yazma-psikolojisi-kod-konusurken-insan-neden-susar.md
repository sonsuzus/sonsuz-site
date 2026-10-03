---
layout: post
title: "Dokümantasyon Yazma Psikolojisi: Kod Konuşurken İnsan Neden Susar?"
math: true
categories: 
  - Bilgi
tags: 
  - dokümantasyon
  - yazılım
  - mühendislik-kültürü
  - teknik-iletişim
  - temiz-kod
  - bilgi-paylaşımı
toc: true
image: /img/dokumantasyon-yazma-psikolojisi-23.png
---

Yeni bir özellik geliştirmek çoğu yazılımcıya heyecan verir: problem çözülür, testler yeşile döner ve ekranda somut bir sonuç belirir. Aynı geliştiriciden özelliği açıklaması istendiğinde ise görünmez bir duvar yükselir. Çünkü kod yazmak makineye kesin talimatlar vermekken dokümantasyon yazmak, başka insanların eksik bilgilerini ve muhtemel yanlış anlamalarını tahmin etmeyi gerektirir.


![dokumantasyon-yazma-psikolojisi-23](/img/dokumantasyon-yazma-psikolojisi-23.svg)

``

## Neden anlatmak kodlamaktan zor gelir?

Programlama sırasında sınırlar bellidir. Derleyici belirsizliği sevmez; sözdizimi yanlışsa hata verir. İnsan dili ise bağlama, deneyime ve beklentiye bağlıdır. `timeout = 30` ifadesi bilgisayar için açıktır, fakat insan için yeni sorular üretir: Otuz saniye mi? Neden otuz? Süre aşımında yeniden deneme yapılır mı?

Bu farkı basitçe şöyle modelleyebiliriz:

$$
D = K_t - K_o
$$

Burada $K_t$, teknik yazarın sahip olduğu bilgi; $K_o$ ise okuyucunun ön bilgisidir. $D$ büyüdükçe açıklama ihtiyacı artar. Ne var ki uzmanlar, uzun süredir bildikleri kavramların başkaları için yeni olduğunu unutabilir. Psikolojide buna **bilginin laneti** denir.

| Kod yazarken | Dokümantasyon yazarken |
|---|---|
| Makinenin kuralları sabittir | Okuyucunun bilgisi değişkendir |
| Sonuç testlerle doğrulanabilir | Anlaşılırlık kullanıcıyla doğrulanır |
| Ne yapılacağı tarif edilir | Neden, nasıl ve ne zaman açıklanır |
| Hata çoğunlukla görünürdür | Yanlış anlama sessizce büyüyebilir |

## “Kod kendini anlatıyor” bahanesi

Temiz kod gerçekten önemlidir. Anlamlı isimler ve küçük fonksiyonlar bilişsel yükü azaltır. Ancak kod çoğunlukla **ne yaptığını** gösterir; **neden öyle yaptığını** her zaman göstermez.

```python
def calculate_price(amount):
    # Ödeme sağlayıcısının alt sınırı nedeniyle ücret 0,50'den az olamaz.
    fee = max(amount * 0.029, 0.50)
    return amount + fee
```

Fonksiyon adı ve değişkenler işlemi okunabilir kılar. Fakat yorum kaldırılırsa `0.50` değeri sihirli bir sayıya dönüşür. Bu sınır yasal zorunluluk mu, iş kararı mı, yoksa geçici çözüm mü? Kod geçmişte alınmış kararın gerekçesini taşımaz.

“Kod kendini anlatıyor” söylemi bazen kalite arzusundan değil, dokümantasyonun bakım maliyetinden kaçma isteğinden doğar. Ayrıca bazı mühendislik kültürlerinde karmaşık anlatım uzmanlık göstergesi sayılır. Oysa gerçek uzmanlık, karmaşıklığı saklamak değil onu doğru katmanlara ayırabilmektir.

## Teknik dili insan diline çevirmek

İyi dokümantasyon, terimleri tamamen ortadan kaldırmaz; onları ihtiyaç anında tanımlar. Okuyucuya önce zihinsel bir harita, ardından ayrıntı verir. Örneğin bir önbelleği yalnızca “düşük gecikmeli veri katmanı” diye tanımlamak yerine, “sık kullanılan veriyi yakında tutan geçici raf” benzetmesiyle başlatmak öğrenmeyi kolaylaştırır.

Etkili bir açıklama şu sırayı izleyebilir:

1. **Amaç:** Bu özellik hangi problemi çözüyor?
2. **Model:** Sistem kabaca nasıl çalışıyor?
3. **Kullanım:** Okuyucu ilk başarılı sonucu nasıl alır?
4. **Sınırlar:** Hangi durumlarda kullanılmamalıdır?
5. **Gerekçe:** Kritik kararlar neden alınmıştır?

Dokümantasyon kapsamını da kabaca $Y = E \times R$ ile düşünebiliriz. Burada $E$ etkilenen kişi sayısını, $R$ ise yanlış kullanım riskini temsil eder. İkisi yükseldikçe daha kapsamlı açıklama gerekir; her yardımcı fonksiyon için roman yazmak gerekmez.

## Yazmayı kültürün parçası yapmak

Dokümantasyonu geliştirme tamamlandıktan sonra ödenen bir vergi gibi görmek yerine, özelliğin teslim kriterine dönüştürmeliyiz. Kod incelemelerinde “çalışıyor mu?” sorusunun yanına “altı ay sonra neden böyle olduğunu anlayacak mıyız?” sorusu eklenebilir. Kısa karar kayıtları, çalıştırılabilir örnekler ve düzenli güncellenen README dosyaları bu alışkanlığı güçlendirir.

En iyi dokümantasyon en uzun metin değildir; doğru kişinin doğru anda doğru kararı vermesini sağlayan metindir. Kod bilgisayarla anlaşmamızı sağlar, dokümantasyon ise geçmişteki ve gelecekteki ekip arkadaşlarımızla. Üstelik gelecekteki ekip arkadaşımız çoğu zaman, ne yaptığını unutmuş olan bizizdir.

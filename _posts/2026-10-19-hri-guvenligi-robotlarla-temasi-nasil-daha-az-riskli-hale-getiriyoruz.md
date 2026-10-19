---
layout: post
title: "HRI Güvenliği: Robotlarla Teması Nasıl Daha Az Riskli Hâle Getiriyoruz?"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - hri
  - iş güvenliği
  - iso standartları
  - cobot
  - risk analizi
toc: true
image: /img/hri-guvenligi-robotlarla-97.png
---

İnsanlarla aynı çalışma alanını paylaşan robotlar artık yalnızca bilim kurgu filmlerinde değil; fabrikalarda, hastanelerde ve laboratuvarlarda karşımıza çıkıyor. Ancak bir robotun nazikçe kahve uzatmasıyla kontrolsüz biçimde kolumuza çarpması arasında ciddi bir güvenlik farkı var. İnsan-robot etkileşimi, yani HRI güvenlik standartları, bu farkı şansa bırakmak yerine temas olasılığını, çarpışma enerjisini ve uygulanabilecek kuvveti sistematik olarak sınırlandırır.
``

## Standartlar neden gereklidir?

Robot güvenliğinde temel yaklaşım, “Çarpışma olursa dururuz” demek değildir. Öncelikle tehlike belirlenir, risk tahmin edilir ve tasarım yoluyla azaltılır. ISO 12100 bu genel risk değerlendirme mantığını sunarken ISO 10218 endüstriyel robot sistemlerine ilişkin güvenlik şartlarını tanımlar. İş birliğine dayalı uygulamalarda kullanılan ISO/TS 15066 ise insan vücudunun farklı bölgeleri için temas, basınç ve kuvvet değerlendirmelerine rehberlik eder.

Standartların izlediği hiyerarşi kabaca şöyledir:

1. Tehlikeyi mümkünse tasarımdan kaldırmak.
2. Hızı, kuvveti ve hareket alanını sınırlandırmak.
3. Sensörler ve güvenlik fonksiyonları kullanmak.
4. Kalan riskleri kullanıcıya bildirmek ve eğitim sağlamak.

Buradaki önemli ayrıntı şudur: Üzerinde “cobot” etiketi bulunan bir robot kendiliğinden güvenli değildir. Robot, uç efektör, taşınan parça, çalışma hızı ve çevredeki yüzeyler birlikte değerlendirilmelidir. Yumuşak robot kolu sivri bir metal parça taşıyorsa güvenlik hikâyesinin kötü karakteri o parça olabilir.

## Dört temel iş birliği yaklaşımı

| Yaklaşım | Çalışma mantığı | Temas riskini azaltma yöntemi |
|---|---|---|
| Güvenlik dereceli izlemeli duruş | İnsan ortak alana girdiğinde robot durur | Hareketli robotla teması önler |
| Elle yönlendirme | Kullanıcı robotu kontrollü biçimde hareket ettirir | Hız ve hareket yetkisini sınırlar |
| Hız ve mesafe izleme | İnsan yaklaştıkça robot yavaşlar | Çarpışmadan önce güvenli duruş sağlar |
| Güç ve kuvvet sınırlama | Temas algılandığında kuvvet sınırlandırılır | Yaralanma şiddetini azaltır |

![hri-guvenligi-robotlarla-97](/img/hri-guvenligi-robotlarla-97.svg)


Hız ve mesafe izleme yaklaşımında robotun yalnızca mevcut konumu değil, durmak için ihtiyaç duyduğu alan da önemlidir. Basitleştirilmiş durma mesafesi şöyle düşünülebilir:

$$S = vT + \frac{v^2}{2a} + C$$

Burada $v$ robot hızı, $T$ algılama ve kontrol gecikmesi, $a$ frenleme ivmesi, $C$ ise sensör belirsizliği ve güvenlik payıdır. Hız iki katına çıktığında frenleme bölümünün dört kat büyümesi, hızlı robotların neden daha geniş güvenlik mesafesine ihtiyaç duyduğunu açıklar.

Çarpışmada taşınan enerji de önemlidir:

$$E_k = \frac{1}{2}mv^2$$

Etkili kütle $m$ aynı kalsa bile hızdaki küçük artışlar temas enerjisini belirgin biçimde yükseltir. Bu nedenle güvenlik sistemleri çoğu zaman insan yaklaştıkça hızı kademeli azaltır.

## Basit bir hız sınırlandırma mantığı

Aşağıdaki örnek, ölçülen insan-robot mesafesine göre hız komutu üretir:

```python
def guvenli_hiz(mesafe, azami_hiz=1.0):
    if mesafe < 0.4:
        return 0.0       # Tehlikeli yakınlık: dur
    if mesafe < 1.0:
        return azami_hiz * (mesafe - 0.4) / 0.6
    return azami_hiz

robot_hizi = guvenli_hiz(sensor_mesafesi)
```

Bu kod öğretici bir modeldir; gerçek bir güvenlik fonksiyonu değildir. Endüstriyel uygulamalarda sıradan kamera, işletim sistemi veya Python betiği tek başına yeterli kabul edilmez. Güvenlik dereceli sensörler, yedekli kontrol kanalları, hata teşhisi ve ISO 13849 gibi standartlara göre doğrulanmış performans seviyeleri gerekir.

## Temasın türü de sonucu değiştirir

Standartlar geçici temas ile sıkışmalı teması ayırır. Robotun çarpıp geri çekildiği geçici temas kısa sürebilir; insanın robot ile duvar arasında sıkıştığı yarı statik temas ise daha tehlikelidir. Ayrıca baş, boyun ve göğüs gibi bölgelerin toleransı kol veya elden farklıdır. Bu nedenle tek bir evrensel kuvvet sınırı kullanmak yerine vücut bölgesi, temas alanı, süre ve basınç birlikte incelenir.

Sonuç olarak HRI güvenliği, robota dev bir acil durdurma düğmesi takmaktan ibaret değildir. Güvenli tasarım; mekanik yapı, sensörler, yazılım, doğrulama testleri ve insan davranışının ortak ürünüdür. İyi uygulanmış standartlar teması tamamen yok etmeyebilir, fakat temasın oluşma ihtimalini ve gerçekleştiğinde vereceği zararı ölçülebilir biçimde azaltır.

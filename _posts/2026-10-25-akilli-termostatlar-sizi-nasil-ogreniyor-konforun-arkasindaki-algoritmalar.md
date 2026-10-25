---
layout: post
title: "Akıllı Termostatlar Sizi Nasıl Öğreniyor? Konforun Arkasındaki Algoritmalar"
math: true
categories: 
  - Bilgi
tags: 
  - akıllı termostat
  - makine öğrenmesi
  - nesnelerin interneti
  - yapay zeka
  - enerji verimliliği
toc: true
image: /img/akilli-termostatlar-sizi-11.png
---

Akıllı bir termostatın sabah siz uyanmadan evi ısıtması sihir gibi görünebilir. Oysa cihazın içinde pelerinli bir büyücü değil; sensörler, geçmiş veriler ve öğrenen algoritmalar bulunur. Termostat, hangi saatlerde evde olduğunuzu, hangi sıcaklıkları tercih ettiğinizi ve evin ne kadar sürede ısındığını gözlemleyerek zamanla kişisel bir ısıtma planı oluşturur.

``

## Termostat hangi verileri toplar?

Öğrenme süreci, düzenli olarak ölçüm yapılmasıyla başlar. Temel veri noktaları oda sıcaklığı, hedef sıcaklık, saat, gün ve kullanıcının yaptığı manuel değişikliklerdir. Daha gelişmiş cihazlar hareket sensörlerinden, telefon konumundan, nem ölçümlerinden ve hava durumu servislerinden de yararlanabilir.

| Veri | Algoritmaya anlattığı şey | Örnek |
|---|---|---|
| Saat ve gün | Günlük veya haftalık rutin | Hafta içi 07.00'de uyanma |
| Manuel ayar | Kullanıcının gerçek tercihi | Akşam sıcaklığı 22°C yapma |
| Hareket sensörü | Evde birinin bulunup bulunmadığı | İki saat hareket algılanmaması |
| Dış sıcaklık | Evin ısınma hızını etkileyen koşul | Dışarısı -3°C |
| Telefon konumu | Eve yaklaşma veya evden ayrılma | Kullanıcı eve 5 km uzakta |

![akilli-termostatlar-sizi-11](/img/akilli-termostatlar-sizi-11.svg)


Burada kritik nokta şudur: Tek bir değişiklik alışkanlık sayılmaz. Kullanıcının sıcaklığı bir akşam yükseltmesi tesadüf olabilir. Algoritma, tekrar eden örüntülere daha fazla güvenmelidir.

## Öğrenmenin temel mantığı

Basit bir sistem, benzer zaman dilimlerindeki tercihlerin hareketli ortalamasını kullanabilir. Son $n$ günde aynı saatte seçilen sıcaklıklar $T_1, T_2, \ldots, T_n$ ise tahmin şöyle hesaplanır:

$$\hat{T}=\frac{1}{n}\sum_{i=1}^{n}T_i$$

Yeni davranışların daha önemli olması istenirse üstel düzeltme uygulanabilir:

$$S_t=\alpha T_t+(1-\alpha)S_{t-1}$$

Buradaki $\alpha$, algoritmanın değişime ne kadar hızlı tepki verdiğini belirler. Büyük bir $\alpha$ yeni tercihlere hızla uyum sağlar; küçük değer ise geçmiş alışkanlıkları daha uzun süre korur.

| Yaklaşım | Güçlü yanı | Zayıf yanı |
|---|---|---|
| Sabit program | Basit ve öngörülebilir | Değişen rutine uymaz |
| Hareketli ortalama | Gürültüyü azaltır | Ani değişiklikleri geç öğrenir |
| Karar ağacı | Saat, hava ve varlığı birlikte işler | Fazla veriyle karmaşıklaşabilir |
| Pekiştirmeli öğrenme | Konfor ve tasarrufu birlikte optimize eder | Güvenli keşif mekanizması gerektirir |

## Küçük bir öğrenme örneği

Aşağıdaki Python kodu, belirli bir saat için son sıcaklık tercihlerine daha yüksek ağırlık verir. Böylece termostat eski alışkanlıkları tamamen unutmadan yeni davranışlara uyum sağlar.

```python
def sicaklik_tahmini(tercihler, alpha=0.35):
    """Geçmiş tercihlerden üstel düzeltilmiş hedef üretir."""
    if not tercihler:
        return 20.0  # Veri yoksa güvenli varsayılan

    tahmin = tercihler[0]
    for sicaklik in tercihler[1:]:
        tahmin = alpha * sicaklik + (1 - alpha) * tahmin

    return round(tahmin, 1)

aksam_tercihleri = [21, 21.5, 22, 22, 22.5]
print(sicaklik_tahmini(aksam_tercihleri))
```

Gerçek bir cihaz yalnızca sıcaklığı tahmin etmez. Evin termal davranışını da öğrenir. Örneğin salonun 19°C'den 22°C'ye ulaşması 30 dakika sürüyorsa sistem, hedef saate kadar beklemek yerine kombiyi önceden çalıştırır.

## Konfor ile tasarruf arasındaki denge

Termostatın amacı evi sürekli sıcak tutmak değildir. Daha mantıklı hedef, konfor kaybı ile enerji tüketimini birlikte azaltmaktır:

$$J=\lambda E+(1-\lambda)C$$

Burada $E$ enerji maliyetini, $C$ hedef sıcaklıktan sapmayı, $\lambda$ ise tasarrufa verilen önemi temsil eder. Kullanıcı üşüyüp ayarı sürekli değiştiriyorsa algoritma konfora daha fazla ağırlık vermeyi öğrenebilir.

Elbette öğrenen cihazlarda mahremiyet önemlidir. Evde bulunma saatleri hassas bilgi sayılmalı; veriler mümkünse cihaz üzerinde işlenmeli, şifrelenmeli ve kullanıcı tarafından silinebilmelidir. Ayrıca donma riski veya aşırı ısınma gibi durumlarda öğrenilmiş kararlar güvenlik sınırlarını aşmamalıdır.

Sonuç olarak akıllı termostat, yalnızca uzaktan kontrol edilen bir düğme değildir. Tekrarlanan davranışları istatistiksel örüntülere dönüştüren, evin fiziksel tepkisini modelleyen ve konfor ile maliyet arasında sürekli pazarlık yapan küçük bir karar sistemidir. Üstelik siz rutininizi değiştirdikçe o da ders programını günceller.

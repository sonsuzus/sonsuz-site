---
layout: post
title: "Zero-Day Açıklarının Ekonomisi: Bir Bug Neden Milyon Dolar Eder?"
math: true
categories: 
  - Bilgi
tags: 
  - zero-day
  - siber güvenlik
  - açık ekonomisi
  - exploit
  - tehdit istihbaratı
  - devlet destekli saldırılar
toc: true
image: /img/zero-day-aciklarinin-97.png
---

![zero-day-aciklarinin-97](/img/zero-day-aciklarinin-97.svg)


Bir yazılım hatasının fiyatı kahve parasından milyonlarca dolara kadar çıkabilir. Bu şaşırtıcı aralığın tepesinde **zero-day**, yani üreticinin henüz bilmediği ve dolayısıyla yama yayımlamadığı güvenlik açıkları bulunur. Ancak alıcı yalnızca birkaç hatalı kod satırı satın almaz; gizlilik, erişim imkânı, operasyon süresi ve stratejik üstünlük satın alır. Kısacası mesele bug değil, bug sayesinde açılabilen kapıdır.
``

## Zero-day tam olarak nedir?

Bir güvenlik açığı üreticiye bildirilmeden veya kamuya açıklanmadan önce saldırılarda kullanılabiliyorsa zero-day niteliğindedir. Üreticinin sorunu düzeltmek için teorik olarak **sıfır günü** bulunduğundan bu adla anılır.

Burada üç kavramı ayırmak önemlidir:

| Kavram | Ne ifade eder? | Piyasa değerine etkisi |
|---|---|---:|
| Güvenlik açığı | Yazılımdaki temel hata | Tek başına sınırlı olabilir |
| Exploit | Hatayı tetikleyen yöntem veya kod | Kullanılabilirliği artırır |
| Exploit zinciri | Birden fazla açığın birlikte kullanılması | Değeri dramatik biçimde yükseltir |

Örneğin tarayıcıdaki bir açık yalnızca uygulama içinde kod çalıştırabilir. İşletim sistemi korumalarını aşan ikinci bir açıkla birleştiğinde ise cihazın ele geçirilmesine uzanan bir zincir oluşabilir. Bu nedenle fiyat etiketleri çoğunlukla tek bir bug’dan ziyade güvenilir bir operasyon paketini yansıtır.

## Fiyat nasıl belirleniyor?

Zero-day değerlemesi klasik arz-talep mantığına uyar, fakat ürün hızla bozulan dijital bir meyve gibidir. Aynı açığı başka bir araştırmacı bulabilir, üretici tesadüfen kapatabilir veya hedef yazılım güncellenebilir.

Basitleştirilmiş bir değer modeli şöyle düşünülebilir:

$$V = I \times R \times S \times E - D$$

Burada $I$ etkinin büyüklüğünü, $R$ güvenilirliği, $S$ gizli kalma olasılığını, $E$ hedef kitlenin yaygınlığını ve $D$ keşfedilme riskinden doğan değer kaybını temsil eder.

| Özellik | Daha düşük değer | Daha yüksek değer |
|---|---|---|
| Etkileşim | Kullanıcının dosya açması gerekir | Etkileşimsiz çalışır |
| Yetki | Kısıtlı uygulama erişimi | Yüksek sistem yetkisi |
| Hedef | Nadir kullanılan sürüm | Güncel ve yaygın platform |
| Güvenilirlik | Sık sık çöker | Tutarlı ve sessiz çalışır |
| Görünürlük | Kolay tespit edilir | İz bırakması zordur |

Bu mantığı saldırı geliştirmeden, yalnızca teorik puanlama amacıyla küçük bir Python modeliyle gösterebiliriz:

```python
def tahmini_deger(etki, guvenilirlik, gizlilik, yayginlik, risk):
    # Tüm girdiler 0 ile 1 arasında normalize edilir.
    taban_deger = 2_000_000
    operasyonel_deger = etki * guvenilirlik * gizlilik * yayginlik
    return max(0, taban_deger * operasyonel_deger * (1 - risk))

print(tahmini_deger(0.95, 0.90, 0.80, 0.85, 0.20))
```

Bu kod gerçek bir piyasa fiyatı üretmez; nitel faktörlerin değeri birlikte ve çarpan etkisiyle oluşturduğunu anlatır. Tek bir zayıf halka toplam fiyatı ciddi biçimde düşürebilir.

## Kimler satın alıyor?

**Hata ödülü programları**, araştırmacılara açığı doğrudan üreticiye bildirmeleri için yasal ve savunmacı bir yol sunar. Açık kapatılır, kullanıcılar korunur ve araştırmacı ödüllendirilir.

Bunun yanında exploit broker’ları, güvenlik şirketleri, kolluk kuvvetleri ve istihbarat kurumları da alıcı olabilir. Devletler açısından zero-day; casusluk, terörle mücadele veya askeri operasyonlarda kullanılabilecek bir **siber kapasite** olarak görülür. Fiziksel mühimmatın aksine aynı kod farklı hedeflerde uygulanabilir; fakat kullanıldığı anda tespit edilip yamalanma ihtimali artar.

## Silah mı, savunma aracı mı?

Temel ikilem stoklamak ile açıklamak arasındadır. Devlet açığı saklarsa kısa vadede istihbarat avantajı kazanabilir; ancak kendi vatandaşları, kurumları ve altyapısı da aynı açıktan etkilenmeye devam eder. Açığı üreticiye bildirirse saldırı kapasitesinden vazgeçer, fakat kolektif güvenliği yükseltir.

Bu yüzden sağlıklı bir yaklaşım; hedefin önemi, açığın başkalarınca keşfedilme ihtimali, savunmasız kullanıcı sayısı ve olası toplumsal zarar gibi ölçütleri birlikte değerlendirmelidir. Zero-day piyasasının milyon dolarlık fiyatları yalnızca teknik ustalığı değil, **geçici ve son derece asimetrik bir bilgi üstünlüğünü** temsil eder. En pahalı bug, en karmaşık olan değil; doğru hedefte, doğru anda ve fark edilmeden sonuç üretebilendir.

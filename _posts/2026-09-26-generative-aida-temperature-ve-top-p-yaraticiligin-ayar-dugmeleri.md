---
layout: post
title: "Generative AI’da Temperature ve Top-P: Yaratıcılığın Ayar Düğmeleri"
math: true
categories: 
  - Bilgi
tags: 
  - generative ai
  - temperature
  - top-p
  - dil modelleri
  - yapay zeka
  - olasılık
toc: true
image: /img/generative-aida-temperature-32.png
---

![generative-aida-temperature-32](/img/generative-aida-temperature-32.svg)


Bir dil modeline “Bana bir hikâye yaz” dediğinizde bazen güvenli ve tahmin edilebilir, bazen de uzayda simit satan melankolik bir robot kadar sıra dışı sonuçlar alabilirsiniz. Bu farkın önemli nedenlerinden ikisi **temperature** ve **top-p** parametreleridir. Bu ayarlar modelin bilgisini değiştirmez; bir sonraki token seçilirken ne kadar temkinli veya maceracı davranacağını belirler.
``
## Model aslında neyi seçiyor?

Dil modelleri metni tek seferde yazmaz. Her adımda mevcut bağlama bakarak olası sonraki token’lara puan verir. Bu puanlar **softmax** fonksiyonu ile olasılığa dönüştürülür:

$$
P(x_i)=\frac{e^{z_i}}{\sum_j e^{z_j}}
$$

Burada $z_i$, ilgili token’ın ham skorudur. Model daha sonra bu dağılımdan seçim yapar. Örneğin “Gökyüzü bugün çok...” ifadesinden sonra dağılım şöyle olabilir:

| Token | Olasılık |
|---|---:|
| güzel | %45 |
| mavi | %30 |
| bulutlu | %20 |
| turşulu | %5 |

En yüksek olasılıklı token’ı sürekli seçmek tutarlı sonuçlar üretir; ancak metin kısa sürede tahmin edilebilir hâle gelebilir. İşte temperature ve top-p bu noktada sahneye çıkar.

## Temperature: Olasılıkların ses mikseri

Temperature, softmax hesabındaki skorları yeniden ölçeklendirir:

$$
P(x_i)=\frac{e^{z_i/T}}{\sum_j e^{z_j/T}}
$$

$T$ temperature değeridir. Düşük değerlerde güçlü adaylar daha baskın hâle gelir. Yüksek değerlerde dağılım düzleşir ve düşük olasılıklı seçeneklerin seçilme şansı artar.

| Temperature | Davranış | Uygun kullanım |
|---:|---|---|
| 0–0.2 | Çok kararlı, tekrarlanabilir | Sınıflandırma, veri çıkarma |
| 0.3–0.7 | Dengeli ve kontrollü | Açıklama, özetleme, kod yardımı |
| 0.8–1.2 | Çeşitli ve yaratıcı | Hikâye, slogan, beyin fırtınası |
| 1.2 üzeri | Sürprizli, hata riski yüksek | Deneysel üretim |

Temperature sıfıra yaklaştığında sistem çoğunlukla en güçlü adayı seçer. Fakat API davranışı sağlayıcıya göre değişebilir; “temperature 0” her platformda matematiksel olarak tamamen deterministik sonuç garantisi değildir.

## Top-P: Davetli listesini daraltmak

**Top-p**, diğer adıyla nucleus sampling, token’ları olasılıklarına göre sıralar ve toplam olasılığı $p$ eşiğine ulaşan en küçük aday kümesini tutar. Örneğin $p=0.90$ ise model, toplam olasılığın en az %90’ını kapsayan seçenekler arasından seçim yapar.

Önceki örnekte top-p değeri 0.75 olursa “güzel” ve “mavi” adayları toplamda %75’e ulaştığı için diğerleri elenir. Böylece “turşulu” gökyüzü şimdilik kuliste bekler.

| Özellik | Temperature | Top-P |
|---|---|---|
| Müdahale biçimi | Dağılımın keskinliğini değiştirir | Aday havuzunu sınırlar |
| Düşük değer etkisi | Güçlü adayları baskınlaştırır | Yalnızca en olası adayları bırakır |
| Yüksek değer etkisi | Rastlantısallığı artırır | Daha geniş aday kümesi sunar |
| Temel risk | Anlamsız seçimler | Fazla dar ve tekdüze metin |

## Python ile küçük bir deney

Aşağıdaki kod, OpenAI uyumlu bir istemcide aynı istemi farklı ayarlarla çalıştırarak sonuçları karşılaştırır:

```python
from openai import OpenAI

client = OpenAI()
prompt = "Yağmuru anlatan tek cümlelik yaratıcı bir slogan yaz."

ayarlar = [
    {"temperature": 0.2, "top_p": 0.9},
    {"temperature": 0.8, "top_p": 0.95},
    {"temperature": 1.2, "top_p": 1.0},
]

for ayar in ayarlar:
    yanit = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        temperature=ayar["temperature"],
        top_p=ayar["top_p"]
    )
    print(ayar, yanit.output_text)
```

Kod aynı görevi üç örnekleme profiliyle çalıştırır. İlk profil güvenli, ikincisi dengeli, üçüncüsü ise daha sürprizli ifadeler üretmeye eğilimlidir. Sonuçların değişkenliğini görmek için her profili birkaç kez çalıştırmak gerekir.

## Hangisini ne zaman ayarlamalıyız?

Fatura bilgisi çıkarma, JSON üretme veya kod düzeltme gibi doğruluğun önemli olduğu görevlerde düşük temperature ve nispeten dar top-p tercih edilebilir. Pazarlama metni, karakter diyaloğu ve fikir üretiminde değerler yükseltilebilir. Yine de iki parametreyi aynı anda aşırı değiştirmek, hangi ayarın sonucu etkilediğini anlamayı zorlaştırır.

Pratik başlangıç noktası olarak temperature için **0.6–0.8**, top-p için **0.9–1.0** denenebilir. Ardından yalnızca bir parametre değiştirilerek kalite, çeşitlilik ve tutarlılık ölçülmelidir. Kısacası temperature modelin ne kadar cesur konuşacağını, top-p ise konuşmadan önce kaç kelime adayını masada tutacağını belirler. İyi ayarlandıklarında yapay zekâ ne toplantı tutanağı kadar sıkıcı ne de rüya günlüğü kadar kontrolsüz olur.

---
layout: post
title: "Şehrin Sinir Sistemi: Akıllı Şehirlerde Sensör Ağları Nasıl Çalışır?"
math: true
categories: 
  - Bilgi
tags: 
  - akıllı şehir
  - sensör ağları
  - iot
  - veri işleme
  - hava kalitesi
  - trafik
toc: true
image: /img/sehrin-sinir-sistemi-82.png
---

Bir şehir konuşabilseydi, sabah trafiğinden yakınır, öğleden sonra hava kalitesini sorar, gece de biraz sessizlik isterdi. Sensör ağları, bu konuşmayı sayılara çevirir. Ancak mesele sokaklara cihaz yerleştirmek değildir: Ölçümlerin güvenilir biçimde toplanması, bağlamıyla değerlendirilmesi ve doğru kararlara dönüşmesi gerekir. Gelin, şehrin görünmez sinir sisteminin nasıl çalıştığını inceleyelim.

``

## Ölçümden karara uzanan yol

Akıllı şehir altyapısında temel zincir **sensör → ağ geçidi → veri platformu → analiz → uygulama** şeklindedir. Sensör fiziksel dünyayı ölçer; ağ geçidi cihazları internete bağlar; platform veriyi saklar ve işler. Son aşamada bir trafik panosu güncellenebilir veya belediyenin inceleme ekibine bildirim gönderilebilir.

Buradaki kritik ayrım, **ölçüm ile yorumun aynı şey olmamasıdır**. Yüksek parçacık ölçümü kirlenmeye işaret edebilir; ancak nem, cihazın konumu ve kalibrasyon durumu değerlendirilmeden kesin sonuca varılamaz.

| Veri türü | Yaygın ölçüm yöntemi | Üretilen bilgi | Başlıca sınırlama |
|---|---|---|---|
| Trafik | Radar, manyetik sensör, kamera | Araç sayısı, hız, doluluk | Yerleşim ve görüş koşulları |
| Hava kalitesi | Optik parçacık, elektrokimyasal gaz sensörü | PM2.5, PM10, NO₂ | Nem ve kalibrasyon sapması |
| Gürültü | Kalibre edilmiş mikrofon | A-ağırlıklı ses seviyesi | Rüzgâr ve mikrofon konumu |

![sehrin-sinir-sistemi-82](/img/sehrin-sinir-sistemi-82.svg)


## Sayıların arkasındaki fizik

Trafik akışı, belirli sürede geçen araç sayısıyla ifade edilebilir: $q=N/\Delta t$. Örneğin beş dakikada 100 araç geçen noktada akış 20 araç/dakikadır. Fakat akış tek başına sıkışıklığı açıklamaz; hız ve yol doluluğu da gerekir. Az araç, bazen sakin yolu değil, ilerleyemeyen kuyruğu gösterir!

Hava sensörlerinde ham sinyal, kalibrasyon modeliyle konsantrasyona dönüştürülür. Basit bir yaklaşım $x_{kalibre}=ax_{ham}+b$ olabilir; gerçek sistemlerde sıcaklık ve nem de modele katılır. Düşük maliyetli cihazlar geniş kapsama sağlar, fakat referans istasyonlarla karşılaştırılmadan resmî ölçümün yerine geçirilmemelidir.

Gürültüde ise desibel logaritmiktir. Eşit süreli, A-ağırlıklı eşdeğer seviye ölçümlerini birleştirirken aritmetik ortalama yerine enerji ortalaması kullanılır:

$$L_{Aeq}=10\log_{10}\left(\frac{1}{n}\sum_{i=1}^{n}10^{L_{A,i}/10}\right)$$

Yani iki gürültü değerini toplayıp ikiye bölmek, fizik açısından her zaman doğru cevap değildir.

## Veriler şehir boyunca nasıl taşınır?

Düşük veri hacimli, pil ile çalışan cihazlarda LoRaWAN; daha yüksek kapasite veya farklı kapsama ihtiyaçlarında hücresel bağlantılar tercih edilebilir. Kameralar ise çoğunlukla daha güçlü bağlantılara ihtiyaç duyar. Uç cihazda araç sayısını hesaplayıp yalnızca sayımı göndermek, görüntü taşımaktan daha ekonomik ve mahremiyet dostudur.

Ağ geçidi, bağlantı kesildiğinde ölçümleri tamponlayabilir. MQTT gibi protokoller mesaj taşımayı kolaylaştırır; ancak mesajın alınması, ölçümün doğru olduğunu garanti etmez. Her kayıtta sensör kimliği, ölçüm zamanı, birim, konum ve kalite bilgisi bulunmalıdır.

Platform, olay zamanına göre pencereler oluşturur. Geç gelen kayıtlar için tolerans tanımlar; tekrar gönderilen mesajları benzersiz kimliklerle ayıklar. Böylece bağlantı kesintisi, araç sayısını yanlışlıkla ikiye katlamaz.

## Python ile dakikalık PM2.5 özeti

Aşağıdaki örnek, şeması önceden doğrulanmış kayıtlarda geçersiz değerleri eler ve her sensör için dakikalık ortalama üretir. `ts`, UTC tabanlı Unix zamanıdır; PM2.5 değerleri aynı birimde olmalıdır.

```python
from collections import defaultdict
from math import isfinite


def minute_pm25(events):
    buckets = defaultdict(list)
    for event in events:
        if event.get('metric') != 'pm25' or event.get('quality') != 'ok':
            continue
        try:
            value = float(event['value'])
            minute = int(float(event['ts']) // 60)
        except (KeyError, TypeError, ValueError, OverflowError):
            continue
        if not isfinite(value) or value < 0:
            continue
        buckets[(event['sensor_id'], minute)].append(value)
    return {key: sum(values) / len(values)
            for key, values in buckets.items()}
```

Sensörleri ayrı gruplamak, farklı mahallelerin ölçümlerini yanlışlıkla karıştırmayı önler. Bu ortalama eşit aralıklı örnekleme varsayar; düzensiz örneklerde zaman ağırlıklı hesaplama gerekir. Ayrıca üretim sisteminde eksik veri oranı ve kalibrasyon bilgisi de sonuca eklenmelidir.

## Güvenilir şehir, güvenilir veri

Veriler zaman serisi depolarında saklanabilir; coğrafi analizlerle mahalle haritalarına dönüştürülebilir. Ancak tek sensör bütün mahalleyi temsil etmeyebilir. Sensör yoğunluğu, yol kenarı etkisi ve yerel koşullar haritanın yorumunu değiştirir. Eksik ölçümleri renkli bir haritada gizlemek yerine belirsizliği göstermek daha dürüsttür.

Cihaz kimlik doğrulaması, şifreli iletişim ve güvenli güncellemeler altyapının temelidir. Gürültü için konuşma kaydetmek yerine cihaz üzerinde seviye hesaplamak tercih edilmelidir. Trafik kameralarında da mümkünse kişisel görüntüler saklanmadan anonim sayımlar üretilmelidir.

Sonuçta akıllı şehir, en fazla sensöre sahip şehir değildir. Verisinin sınırlarını bilen, hataları izleyen ve ölçümleri insanların yaşamını iyileştiren kararlara dönüştüren şehirdir.

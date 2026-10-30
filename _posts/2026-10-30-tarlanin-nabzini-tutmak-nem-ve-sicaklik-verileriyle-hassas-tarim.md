---
layout: post
title: "Tarlanın Nabzını Tutmak: Nem ve Sıcaklık Verileriyle Hassas Tarım"
math: true
categories: 
  - Bilgi
tags: 
  - hassas tarım
  - iot
  - toprak nemi
  - sensörler
  - python
  - veri analizi
toc: true
image: /img/tarlanin-nabzini-tutmak-43.png
---

Bir tarlayı yalnızca takvime bakarak sulamak, kahveyi tadına bakmadan sürekli şekerlendirmeye benzer: İyi niyet vardır, doğru doz garanti değildir. Hassas tarım, toprağın gerçek durumunu sensörlerle izleyerek bu alışkanlığı değiştirir. Toprak nemi ve sıcaklık verileri doğru işlendiğinde, çiftçiye yalnızca grafik değil; nerede, ne zaman ve ne kadar sulama gerektiğini değerlendirebileceği bir karar zemini sunar.

``

## Ölçümden Önce: Toprak Ne Anlatıyor?

Toprak nem sensörlerinin hepsi aynı büyüklüğü ölçmez. Kapasitif sensörler, toprağın dielektrik özelliklerinden su içeriğini tahmin eder; tensiyometreler ise suyun toprak tarafından ne kadar kuvvetle tutulduğunu gösterir. Bu nedenle cihazdan gelen ham değeri doğrudan “nem yüzdesi” diye etiketlemek hatalı olabilir. Sensör, toprak türüne ve üretici yöntemine uygun biçimde kalibre edilmelidir.

Hacimsel su içeriği $\theta = V_{su}/V_{toprak}$ olarak tanımlanır. Örneğin $\theta = 0.22$, ölçülen toprak hacminin yaklaşık yüzde 22’sinin su olduğunu ifade eder. Ancak bunun yeterli olup olmadığı toprağın özelliklerine bağlıdır.

İki önemli referans, fazla suyun süzülmesinden sonraki **tarla kapasitesi** ve bitkinin suyu artık yeterince kullanamadığı **kalıcı solma noktasıdır**. Basitleştirilmiş bağıl tükenme göstergesi şöyledir:

$$D = \frac{\theta_{TK} - \theta}{\theta_{TK} - \theta_{SN}}$$

Tarla kapasitesi 0.34, solma noktası 0.14 ve güncel nem 0.22 ise $D = 0.60$ çıkar. Bu değer, kullanılabilir su aralığının yaklaşık yüzde 60’ının tükendiğini anlatır. Uygulamada gösterge 0–1 aralığına sınırlandırılır; sulama eşiği ürünün gelişim dönemine göre belirlenir.

| Veri | Anlattığı durum | Yönetimdeki karşılığı |
|---|---|---|
| Hacimsel nem | Topraktaki su miktarı | Sulama gereksinimini değerlendirme |
| Toprak sıcaklığı | Kök ortamının termal durumu | Gelişim koşullarını yorumlama |
| Yağış tahmini | Yaklaşan doğal su girdisi | Sulamayı erteleme olasılığı |
| Debi ölçümü | Gerçekte verilen su | Uygulama miktarını doğrulama |

![tarlanin-nabzini-tutmak-43](/img/tarlanin-nabzini-tutmak-43.svg)


## Verinin Tarladan Yazılıma Yolculuğu

Tipik akış **sensör → saha düğümü → ağ geçidi → veri platformu → karar ekranı** şeklindedir. Düğüm, ölçümü zaman damgası, sensör kimliği, konum, derinlik ve birim bilgisiyle paketler. LoRaWAN gibi bağlantılar saha iletişimini sağlayabilir; ağ geçidi veriyi MQTT veya HTTPS üzerinden sunucuya aktarabilir.

Zaman serisi veritabanı geçmişi saklarken, coğrafi bilgi sistemi ölçümleri yönetim bölgeleriyle eşleştirir. Böylece kumlu bölümle killi bölüm aynı sulama reçetesine mahkûm olmaz. Sensörler temsilî noktalara, ilgili kök derinliklerine yerleştirilmelidir; tek noktadan bütün tarlaya hükmetmek, bir lokmadan bütün tencereyi değerlendirmektir.

## Python ile Gürültüyü Azaltıp Öneri Üretmek

Aşağıdaki örnekte her bölgeyi temsil eden tek sensör bulunuyor. Kod, son beş ölçümün ortalamasını alıyor ve farklı başlatma/durdurma eşikleriyle **histerezis** uyguluyor. Böylece eşik çevresindeki küçük dalgalanmalar öneriyi sürekli değiştirmiyor. Sıcaklık sınırı ve nem eşikleri yalnızca örnektir; sahaya göre ayarlanmalıdır.

```python
from collections import defaultdict, deque
from datetime import datetime, timezone
from math import isfinite

history = defaultdict(lambda: deque(maxlen=5))
demand = defaultdict(bool)

def evaluate(reading):
    zone = reading["zone"]
    theta = float(reading["theta"])
    temp = float(reading["temp"])
    measured_at = datetime.fromisoformat(reading["time"])
    age = (datetime.now(timezone.utc) - measured_at).total_seconds()

    valid = (
        all(isfinite(x) for x in (theta, temp))
        and 0 <= theta <= 0.70
        and -20 <= temp <= 70
        and 0 <= age <= 600
    )
    if not valid:
        return {"zone": zone, "status": "incele"}

    history[zone].append(theta)
    if len(history[zone]) < 5:
        return {"zone": zone, "status": "veri bekleniyor"}

    average = sum(history[zone]) / len(history[zone])
    if temp < 5 or average >= 0.28:
        demand[zone] = False
    elif average < 0.22:
        demand[zone] = True

    return {"zone": zone, "irrigate": demand[zone]}
```

Zaman damgası saat dilimi içermelidir. Üretimde eksik alanlar, bozuk tarihler, yinelenen paketler ve sırasız ölçümler ayrıca yönetilir. Bu kod vana açmaz; yalnızca öneri üretir. Bağlantı kesilmesini “toprak kuru” diye yorumlayıp sulamaya başlamak özellikle kaçınılması gereken bir hatadır.

## Öneriyi Tarla Yönetimine Bağlamak

Karar ekranında bölgesel nem eğilimleri, sıcaklık, veri güncelliği ve önerinin gerekçesi birlikte gösterilir. Sulama miktarı için hedef nem, kök derinliği ve uygulama verimi kullanılır. Basit yaklaşımda net su derinliği $I = (\theta_{hedef}-\theta)Z_r$ olur; kök derinliği milimetreyse sonuç da milimetredir. Bu hesap homojen kök bölgesi varsayar.

Otomatik uygulamada yağış beklentisi, pompa kapasitesi, günlük su sınırı ve vana çalışma süresi ek kısıtlardır. Debimetre, planlanan suyun gerçekten verilip verilmediğini doğrular. Güvenli iletişim ve cihaz kimlik doğrulaması da ihmal edilmemelidir.

Başarıyı yalnızca güzel grafiklerle ölçmeyin: Kullanılan suyu, ürün verimini ve sensör arızalarını karşılaştırın. İyi hassas tarım sistemi, çiftçinin deneyimini ortadan kaldırmaz; o deneyime ölçülebilir, güncel ve bölgesel bir hafıza kazandırır.

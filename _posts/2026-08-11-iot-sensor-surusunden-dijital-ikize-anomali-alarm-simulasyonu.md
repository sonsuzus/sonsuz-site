---
layout: post
title: "IoT Sensör Sürüsünden Dijital İkize: Anomali Alarm Simülasyonu"
math: true
categories: 
  - Proje
tags: 
  - IoT
  - Python
  - Anomali Tespiti
  - Dijital İkiz
  - Siber-Fiziksel Sistem
---

Bir fabrikanın, seranın ya da akıllı binanın yüzlerce sensörle konuştuğunu düşünün: sıcaklıklar yükseliyor, titreşimler dalgalanıyor, nem değerleri fısıldıyor. Bu verinin içinden gerçekten tehlikeli olanı seçmek, samanlıkta iğne aramaktan biraz daha zor; çünkü bazen iğne de hareket ediyor. Bu projede sahte IoT verileri üreten, fiziksel ortamın dijital ikizini güncelleyen ve olağandışı durumlarda alarm veren küçük ama genişletilebilir bir siber-fiziksel sistem simülasyonu kuracağız.

``

Siber-fiziksel sistem (CPS), fiziksel dünyadaki cihazların yazılım, ağ ve kontrol mantığıyla birleşmesidir. **Dijital ikiz** ise fiziksel sistemin anlık veya geçmiş verilerle beslenen yazılımsal temsilidir. Sensör verisi ikize akar, ikiz sistem davranışını yorumlar ve gerektiğinde operatöre ya da otomatik kontrol mekanizmasına geri bildirim üretir.

Anomali kavramı yalnızca "eşik aşıldı" demek değildir. Normal sıcaklık $25^\circ C$ iken $70^\circ C$ açıkça şüphelidir; fakat sıcaklığın bir saniye içinde $25$'ten $38$'e çıkması, değer hâlâ kabul edilebilir aralıkta olsa bile fiziksel açıdan anlamlı bir alarm olabilir. Bu nedenle hem mutlak seviye hem de beklenen davranıştan sapma izlenmelidir.

| Yaklaşım | Güçlü yanı | Zayıf yanı | Uygun senaryo |
|---|---|---|---|
| Sabit eşik | Basit ve açıklanabilir | Bağlama duyarsız | Kritik sınırlar |
| Z-skoru | Dağılımdan sapmayı bulur | Ortalama kaymalara duyarlı | Kararlı sensörler |
| Hareketli pencere | Yerel davranışı izler | Pencere boyutu önemlidir | Zaman serileri |
| ML tabanlı model | Karmaşık örüntüleri yakalar | Eğitim verisi ister | Büyük filolar |

Bu örnekte her sensör için sıcaklık, nem ve titreşim üreteceğiz. Normal veriler küçük rastgele gürültü taşırken, belirli olasılıkla sıcaklık sıçraması veya titreşim patlaması enjekte edeceğiz. Z-skoru şu mantıkla hesaplanır:

$$z = \frac{x - \mu}{\sigma}$$

Burada $x$ anlık ölçüm, $\mu$ hareketli pencerenin ortalaması, $\sigma$ ise standart sapmasıdır. Genel kural olarak $|z| > 3$ değerleri nadir kabul edilir. Ancak sıfıra yakın standart sapma durumunda bölme hatasını önlemek için küçük bir $\epsilon$ kullanmak iyi bir mühendislik refleksidir.

```python
import random
from collections import defaultdict, deque
from statistics import mean, pstdev

WINDOW = 20
history = defaultdict(lambda: deque(maxlen=WINDOW))

def produce_reading(sensor_id):
    temperature = random.gauss(24, 0.8)
    humidity = random.gauss(48, 2.5)
    vibration = abs(random.gauss(0.12, 0.03))

    # Kontrollü biçimde sahte fiziksel arıza ekle
    if random.random() < 0.08:
        temperature += random.uniform(8, 18)
        vibration += random.uniform(0.4, 1.0)

    return {
        "sensor_id": sensor_id,
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "vibration": round(vibration, 3)
    }

def is_anomaly(sensor_id, value):
    values = history[sensor_id]
    if len(values) < 8:
        values.append(value)
        return False, 0.0

    sigma = pstdev(values)
    z_score = abs((value - mean(values)) / max(sigma, 0.001))
    values.append(value)
    return z_score > 3, z_score
```

Kodda `history`, her sensörün son ölçümlerini ayrı tutar. Bu ayrım kritiktir: Bir motorun normal titreşimi, başka bir motor için arıza belirtisi olabilir. Simülasyon döngüsünde dijital ikiz durumunu güncelleyip sıcaklık ve titreşim için ayrı denetimler uygulayabiliriz.

```python
for tick in range(60):
    for sensor_id in ["motor-01", "motor-02", "tank-01"]:
        reading = produce_reading(sensor_id)
        bad_temp, score = is_anomaly(sensor_id, reading["temperature"])

        if bad_temp or reading["vibration"] > 0.65:
            print(f"🚨 ALARM | {sensor_id} | veri={reading} | z={score:.2f}")
        else:
            print(f"✅ Normal | {sensor_id} | {reading['temperature']}°C")
```

Gerçek hayatta alarmı doğrudan tek ölçüme bağlamak gürültü nedeniyle yanlış pozitif üretebilir. Daha sağlam bir politika, alarmı iki ardışık anomaliye, birden fazla sensörün ortak sapmasına veya sıcaklık artışı ile titreşim artışının aynı anda görülmesine bağlamaktır. Bu, sensör hatası ile fiziksel arızayı ayırmada güçlüdür.

| Alarm seviyesi | Örnek koşul | Önerilen aksiyon |
|---|---|---|
| Bilgi | Tekil hafif sapma | Logla ve izle |
| Uyarı | Ardışık iki anomali | Operatöre bildirim |
| Kritik | Yüksek titreşim + sıcaklık sıçraması | Ekipmanı güvenli moda al |

Bir sonraki adımda verileri MQTT ile yayınlayabilir, ikiz durumunu SQLite veya InfluxDB'de saklayabilir ve Grafana panosunda görselleştirebilirsiniz. Böylece oyuncak simülasyon, üretim ortamına yaklaşan gözlemlenebilir bir dijital ikize dönüşür.

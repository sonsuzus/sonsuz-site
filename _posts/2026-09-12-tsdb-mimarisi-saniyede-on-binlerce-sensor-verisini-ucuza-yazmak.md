---
layout: post
title: "TSDB Mimarisi: Saniyede On Binlerce Sensör Verisini Ucuza Yazmak"
math: true
categories: 
  - Bilgi
tags: 
  - zaman serisi
  - veritabanı mimarisi
  - ıot
toc: true
---

Bir fabrikanın sensörleri her saniye sıcaklık, basınç ve titreşim ölçümleri gönderiyorsa ortaya küçük görünen fakat hiç durmayan bir veri seli çıkar. Zaman Serisi Veritabanları (TSDB), bu seli klasik ilişkisel veritabanlarından farklı olarak satır satır düzenlemek yerine zaman odaklı, sıralı ve toplu biçimde işleyerek yüksek yazma hızına daha düşük disk maliyetiyle ulaşır.
``
## Zaman serisini farklı yapan nedir?

Bir zaman serisi kaydı çoğunlukla zaman damgası, ölçüm adı, etiketler ve sayısal bir değerden oluşur:

$$x_t = (t, m, L, v)$$

Burada $t$ zaman damgası, $m$ ölçüm adı, $L$ sensör veya konum gibi etiketler, $v$ ise ölçülen değerdir. Sensör verileri genellikle zaman sırasıyla gelir, nadiren güncellenir ve çoğunlukla belirli bir zaman aralığı üzerinden sorgulanır. TSDB mimarisi tam olarak bu davranışları avantaja çevirir.

Saniyede $N$ sensörün her biri $f$ adet kayıt gönderiyorsa yazma yükü şöyledir:

$$W = N \times f$$

Örneğin 20.000 sensör saniyede iki ölçüm ürettiğinde sistemin en az 40.000 kayıt/saniye hızını sürdürebilmesi gerekir. Klasik bir veritabanında her kayıt için indeks güncellemek ve rastgele disk sayfalarına erişmek darboğaz oluşturabilir.

## TSDB yazma hattı

Tipik bir TSDB, gelen kayıtları önce bellekteki tamponlara alır. Kayıtlar tek tek diske gönderilmez; gruplandırılarak büyük ve sıralı bloklar hâlinde yazılır. Böylece çok sayıdaki pahalı rastgele I/O işlemi, daha az sayıdaki ucuz sıralı I/O işlemine dönüşür.

1. **Alım katmanı:** HTTP, MQTT veya özel protokollerle veriyi kabul eder.
2. **WAL:** Write-Ahead Log, çökme durumunda verinin kurtarılabilmesi için kaydı hızlıca eklemeli bir günlüğe yazar.
3. **Bellek tablosu:** Veriler zaman ve seri kimliğine göre RAM üzerinde gruplanır.
4. **Kalıcı bloklar:** Dolan tamponlar değiştirilemez segmentler şeklinde diske aktarılır.
5. **Sıkıştırma:** Eski segmentler birleştirilir, sıkıştırılır ve saklama politikasına göre silinir.

Bu yaklaşım LSM-tree mantığına benzer. Yazma sırasında mevcut disk bloklarını sürekli değiştirmek yerine yeni veri sona eklenir. Maliyeti basitleştirirsek tekil yazmada yaklaşık $N$ disk işlemi gerekirken, $B$ kayıtlık gruplarla işlem sayısı yaklaşık $N/B$ seviyesine iner.

| Özellik | İlişkisel veritabanı | TSDB |
|---|---|---|
| Ana erişim modeli | Satır ve ilişki odaklı | Zaman aralığı ve seri odaklı |
| Yazma biçimi | Dağınık sayfa güncellemeleri | Toplu, sıralı ve eklemeli |
| İndeksleme | Çok sayıda sütun indeksi | Zaman ve etiket indeksleri |
| Güncelleme | Güçlü ve sık | Genellikle nadir |
| Veri ömrü | Manuel arşivleme | Yerleşik saklama politikası |
| Sıkıştırma | Genel amaçlı | Zaman serisine özel |

## Sıkıştırmanın gizli gücü

Zaman damgaları düzenli arttığından her değeri tamamen saklamak gerekmez. İlk fark $\Delta_t=t_i-t_{i-1}$, ardından farkların farkı tutulabilir. Ölçüm değerlerinde ise Gorilla benzeri XOR sıkıştırması kullanılabilir. Ardışık kayan noktalı değerlerin bitleri benzer olduğunda yalnızca değişen bitler kaydedilir.

Etiketler her kayıtta tekrar yazılmak yerine bir seri kimliğine dönüştürülür:

$$seriesId = hash(metric, tags)$$

Ancak yüksek kardinalite tehlikelidir. `device_id` uygun bir etiketken her isteğe özgü `request_id`, milyonlarca seri yaratarak RAM tüketimini patlatabilir.

## Toplu veri gönderme örneği

Aşağıdaki Python kodu ölçümleri tek tek değil, 500 kayıtlık paketler hâlinde gönderir:

```python
import requests

buffer = []

for reading in sensor_stream():
    line = (
        f"temperature,device={reading.device} "
        f"value={reading.value} {reading.timestamp_ns}"
    )
    buffer.append(line)

    if len(buffer) >= 500:
        payload = "\n".join(buffer)
        response = requests.post(
            "http://tsdb:8086/api/v2/write",
            data=payload,
            timeout=5
        )
        response.raise_for_status()
        buffer.clear()
```

Paketleme ağ bağlantısı, HTTP başlığı ve disk senkronizasyonu maliyetlerini yüzlerce kayıt arasında paylaştırır. Üretim ortamında başarısız paketler için yeniden deneme, yerel kuyruk ve idempotent yazma mekanizmaları da eklenmelidir.

Sonuç olarak TSDB’nin hız sırrı daha güçlü donanım değil; veri modelini tanımaktır. Sıralı yazma, WAL, toplu işleme, zaman tabanlı bölümleme, özel sıkıştırma ve otomatik veri yaşam döngüsü birleştiğinde saniyelik on binlerce sensör paketi hem hızlı hem ekonomik biçimde saklanabilir.

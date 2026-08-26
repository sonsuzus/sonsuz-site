---
layout: post
title: "Grafana Panoları Tasarlamak: Teknik Veriyi Anlaşılır Hikâyelere Dönüştürmek"
math: true
categories: 
  - Bilgi
tags: 
  - grafana
  - gözlemlenebilirlik
  - dashboard
  - veri görselleştirme
toc: true
---

Grafana panosu tasarlamak, ekrana mümkün olduğunca çok grafik sığdırmak değildir; doğru kişiye, doğru anda, doğru kararı verdirecek sinyali sunmaktır. Sunucu gecikmesi, hata oranı, kaynak tüketimi ve iş metrikleri aynı ekranda bulunabilir. Ancak bu veriler bir bağlam ve hiyerarşi olmadan sunulursa pano, kokpitten çok renkli bir duvar kâğıdına dönüşür. İyi bir dashboard, teknik karmaşayı birkaç saniyede okunabilir bir hikâyeye çevirir.
``
## Önce soruyu, sonra paneli tasarlayın

Her pano tek bir temel soruya hizmet etmelidir: “Sistem sağlıklı mı?”, “Kullanıcılar neden yavaşlık yaşıyor?” ya da “Bu sürüm hata oranını artırdı mı?” gibi. Bu yaklaşım, metrik seçimini ve görsel türünü doğal biçimde sınırlar. Örneğin bir SRE için altyapı sağlığı panosu ile ürün ekibinin dönüşüm panosu aynı ölçümleri kullanabilir; fakat öncelikleri farklıdır.

Kullanışlı bir teorik çerçeve, **RED** yöntemidir: istek hızı (*Rate*), hata oranı (*Errors*) ve süre (*Duration*). Kaynak merkezli servislerde ise **USE** yöntemi öne çıkar: kullanım (*Utilization*), doygunluk (*Saturation*) ve hata (*Errors*). Hata oranını yalnızca hata sayısıyla değerlendirmek yanıltıcıdır. Daha anlamlı formül şöyledir:

$$\text{Hata Oranı} = \frac{\text{Başarısız İstekler}}{\text{Toplam İstekler}} \times 100$$

Dakikada 10 hata bazı sistemlerde kriz, bazılarında gürültü olabilir. Çünkü trafik hacmi bağlamı değiştirir. Bu nedenle Grafana’da aynı zaman aralığında toplam istek ve hata yüzdesini birlikte okumak güçlü bir alışkanlıktır.

| İhtiyaç | Uygun görsel | Neden |
|---|---|---|
| Zaman içindeki eğilim | Time series | Ani sıçrama ve mevsimsel davranışı gösterir |
| Anlık kritik değer | Stat | Tek bir KPI’ı hızla okunur yapar |
| Hedefe göre durum | Gauge / Bar gauge | Eşik ve kapasite karşılaştırması kolaydır |
| Kategorik dağılım | Bar chart | Servis, bölge veya hata kodlarını kıyaslar |
| Olay yoğunluğu | Heatmap | Gecikme dağılımı ve aykırı değerleri ortaya çıkarır |

## Görsel hiyerarşi: Önce alarm, sonra ayrıntı

Pano düzeninde en üst satıra karar verdiren özet metrikleri yerleştirin: kullanılabilirlik, p95 gecikme, hata oranı ve aktif alarm sayısı iyi adaylardır. Alt satırlarda ise teşhis için gereken ayrıntılar bulunmalıdır: endpoint bazında gecikme, veritabanı bağlantıları veya pod bellek tüketimi gibi.

Renkler dekorasyon değil, bir dil olmalıdır. Yeşil normal durumu, sarı dikkat gerektiren aralığı, kırmızı ise aksiyon gerektiren eşiği temsil etsin. Aynı panoda CPU için kırmızının “iyi”, hata oranı için “kötü” anlamına gelmesi kullanıcıyı gereksiz yere yorar. Ayrıca kırmızı-yeşil ayrımına güvenmek yerine etiket, ikon veya eşik çizgisi de kullanın.

Prometheus kullanan bir ortamda p95 gecikmesini hesaplayan örnek sorgu şöyledir:

```promql
histogram_quantile(
  0.95,
  sum by (le, service) (
    rate(http_request_duration_seconds_bucket{job="api"}[5m])
  )
)
```

Bu sorgu, son beş dakikadaki histogram kovalarını birleştirir ve her servis için isteklerin %95’inin altında kaldığı gecikmeyi üretir. Ortalama gecikmeye göre daha değerlidir; çünkü kullanıcı deneyimini bozan kuyruk sonunu görünür kılar. Panelin birimine `seconds` ya da `milliseconds` atamak, eksen ve tooltip değerlerini otomatik olarak anlaşılır hale getirir.

## Etiketler, değişkenler ve gürültü kontrolü

Grafana değişkenleriyle `environment`, `cluster` ve `service` filtreleri eklemek, tek panoyu tekrar kullanılabilir kılar. Fakat her etiketi filtre yapmak iyi fikir değildir. Yüksek kardinaliteli `user_id` veya `request_id` gibi etiketler sorguları pahalılaştırabilir ve seçimi anlamsızlaştırabilir.

| Tasarım hatası | Sonuç | Daha iyi yaklaşım |
|---|---|---|
| Her metriği eklemek | Bilişsel yük artar | Soruyla ilişkili KPI’ları seçin |
| Ortalama gecikmeye bakmak | Uç kullanıcı sorunu saklanır | p95 ve p99 kullanın |
| Sabit zaman aralığı | Olay bağlamı kaybolur | Zaman seçiciyi görünür bırakın |
| İsimsiz paneller | Yorumlama yavaşlar | Başlığı soru veya anlamlı metrik yapın |

Son dokunuş olarak panellere kısa açıklamalar, veri kaynağı bağlantıları ve runbook URL’leri ekleyin. Bir alarm çaldığında pano yalnızca “ne oldu?” sorusunu değil, “nereden başlamalıyım?” sorusunu da yanıtlamalıdır. Başarılı Grafana panosu, izleyiciyi grafikleri okumaya zorlamaz; grafikleri, sistemin hikâyesini anlatacak şekilde konuşturur.

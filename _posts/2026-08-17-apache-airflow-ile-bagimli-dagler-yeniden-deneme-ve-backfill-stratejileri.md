---
layout: post
title: "Apache Airflow ile Bağımlı DAG’ler, Yeniden Deneme ve Backfill Stratejileri"
math: true
categories: 
  - Program
tags: 
  - Apache Airflow
  - DAG
  - Veri Mühendisliği
---

Veri boru hatları, tek seferlik çalışan betiklerden çok daha fazlasıdır: Her sabah veriyi çekmek, dönüştürmek, raporlamak ve olası aksaklıklarda sistemi güvenle toparlamak gerekir. Apache Airflow, bu süreci **DAG** (Directed Acyclic Graph — yönlü döngüsüz grafik) yaklaşımıyla yönetir. Her görev bir düğüm, görevler arasındaki sıralama ise bir yönlü kenardır. “Döngüsüz” olması önemlidir; A görevi B’yi, B de tekrar A’yı beklerse orkestrasyon sonsuza dek kahve molasına çıkar.

``

Bir DAG’in temel amacı, *ne yapılacağını* ve *hangi sırayla yapılacağını* açıkça ifade etmektir. Örneğin `extract`, `transform` ve `load` görevlerinden oluşan ETL akışında bağımlılık matematiksel olarak $extract \rightarrow transform \rightarrow load$ biçiminde gösterilebilir. Toplam çalışma süresi, görevler tamamen sıralıysa yaklaşık olarak $T = t_e + t_t + t_l$ olur. Ancak bağımsız görevler paralelleştirildiğinde kritik yol belirleyici hâle gelir: $T \approx \max(T_{paralel}) + T_{bagimli}$.

Airflow’da görev bağımlılıkları `>>` ve `<<` operatörleriyle okunaklı şekilde kurulur. Aşağıdaki örnekte veri alınmadan dönüşüm, dönüşüm bitmeden de yükleme başlamaz:

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

args = {
    "owner": "data-team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="gunluk_satis_etl",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=args,
) as dag:
    extract = PythonOperator(task_id="extract", python_callable=veri_cek)
    transform = PythonOperator(task_id="transform", python_callable=veri_donustur)
    load = PythonOperator(task_id="load", python_callable=veri_yukle)

    extract >> transform >> load
```

Buradaki `retries=3`, başarısız olan bir görevin toplamda üç kez daha denenmesini sağlar. Ağ kesintisi, geçici API kotası veya kısa süreli veritabanı kilidi gibi hatalar için oldukça değerlidir. Ancak her hata yeniden denemeye uygun değildir: Şema değişmişse aynı görevi dört kez çalıştırmak sorunu çözmez; sadece log dosyalarını dramatik biçimde büyütür.

| Kavram | Ne yapar? | Uygun kullanım |
|---|---|---|
| `retries` | Başarısız task’ı tekrar çalıştırır | Geçici ağ ve servis hataları |
| `retry_delay` | Denemeler arasındaki beklemeyi belirler | API veya DB üzerindeki yükü azaltma |
| `execution_timeout` | Görevin azami süresini sınırlar | Takılı kalan işlemleri durdurma |
| `catchup` | Geçmiş zaman aralıkları için DAG run üretir | Tarihsel periyotların otomatik işlenmesi |

Daha dayanıklı akışlar için yeniden deneme beklemesi sabit değil, üstel artan olabilir. Basit fikir şudur: $d_n = d_0 \times 2^n$. İlk bekleme 5 dakika ise sonraki beklemeler 5, 10 ve 20 dakika olur. Airflow’da `retry_exponential_backoff=True` kullanmak, özellikle dış servisleri gereksiz istek yağmuruna tutmamak için iyi bir vatandaştır.

Backfill ise geçmişte kaçırılmış veya hatalı işlenmiş tarih aralıklarını tekrar çalıştırma işlemidir. Diyelim ki 10–15 Mart arasındaki satış verisi yanlış bir kur dönüşümüyle işlendi. Kod düzeltildikten sonra sadece bu aralığı hedeflemek mantıklıdır:

```bash
airflow dags backfill gunluk_satis_etl \
  --start-date 2025-03-10 \
  --end-date 2025-03-15
```

Backfill güvenliği için görevlerin **idempotent** olması gerekir: Aynı tarih için görev iki kez çalışsa bile sonuç bozulmamalıdır. Bunun için çıktı tablolarını tarih bölümüne yazmak, `INSERT` yerine `MERGE` veya `UPSERT` kullanmak ve her çalışmada `logical_date` değerini veri filtresine katmak iyi pratiklerdir.

| Strateji | Avantaj | Dikkat edilmesi gereken |
|---|---|---|
| Otomatik retry | Geçici hatalarda operasyon yükünü azaltır | Kalıcı hataları maskeleyebilir |
| Manuel backfill | Hatalı tarihleri kontrollü düzeltir | Üretim kaynaklarını zorlayabilir |
| `catchup=True` | Eksik tüm periyotları otomatik tamamlar | Çok sayıda DAG run oluşturabilir |
| İdempotent task | Tekrar çalıştırmayı güvenli kılar | Yazma mantığı dikkatle tasarlanmalıdır |

Son olarak bağımlı DAG’leri yalnızca zamanlama ile değil, veri hazır olma koşullarıyla da tasarlayın. Bir üst akış tamamlanmadan alt akışı başlatmak, “iş bitti” ile “veri gerçekten kullanılabilir” arasındaki farkı pahalı biçimde öğretir. Sağlam bağımlılıklar, ölçülü retry ayarları ve kontrollü backfill; Airflow’u basit bir zamanlayıcıdan güvenilir bir veri operasyon platformuna dönüştürür.

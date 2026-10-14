---
layout: post
title: "Kritik Yol Metodu: Projenin En Kısa Tamamlanma Süresini Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - kritik yol
  - cpm
  - proje yönetimi
  - graf algoritmaları
  - python
  - dinamik programlama
toc: true
image: /img/kritik-yol-metodu-42.png
---

![kritik-yol-metodu-42](/img/kritik-yol-metodu-42.svg)


Bir projedeki görevleri yalnızca yapılacaklar listesine yazmak yeterli değildir; bazı görevler diğerleri tamamlanmadan başlayamaz. Kritik Yol Metodu, yani CPM, bu bağımlılıkları analiz ederek projenin mümkün olan en kısa tamamlanma süresini ve gecikmesine tahammül edilemeyen görevleri bulur. Kısacası CPM, proje planının “hangi görev gecikirse alarm çalar?” sorusuna matematiksel bir cevap verir.

``

## Problemin teorik modeli

CPM’de proje, yönlendirilmiş döngüsüz bir grafik (**DAG**) olarak modellenir. Her düğüm bir görevi, yönlendirilmiş kenarlar ise öncelik ilişkilerini temsil eder. Örneğin $A \rightarrow B$, B görevinin ancak A tamamlandıktan sonra başlayabileceğini belirtir.

Her görev için dört temel zaman değeri hesaplanır:

| Değer | Anlamı | Hesaplama yönü |
|---|---|---|
| ES | En erken başlama zamanı | İleri geçiş |
| EF | En erken bitiş zamanı | İleri geçiş |
| LS | En geç başlama zamanı | Geri geçiş |
| LF | En geç bitiş zamanı | Geri geçiş |

Bir $i$ görevinin süresi $d_i$ olsun. En erken bitiş zamanı:

$$EF_i = ES_i + d_i$$

Görevin birden fazla öncülü varsa en erken başlama zamanı, bu öncüllerin en geç bitenine göre belirlenir:

$$ES_i = \max_{j \in pred(i)} EF_j$$

Bu işlem, görevler **topolojik sırada** dolaşılarak yapılır. Son görevler için bulunan en büyük $EF$ değeri, projenin minimum tamamlanma süresidir.

## Geri geçiş ve bolluk

İleri geçiş “En erken ne zaman biteriz?” sorusunu cevaplarken geri geçiş, görevlerin projeyi geciktirmeden ne kadar ertelenebileceğini hesaplar. Bir görevin en geç başlama zamanı şöyledir:

$$LS_i = LF_i - d_i$$

Birden fazla ardılı bulunan görev için:

$$LF_i = \min_{j \in succ(i)} LS_j$$

Görevin **bolluk** veya **esneklik** değeri ise:

$$Slack_i = LS_i - ES_i$$

$Slack_i = 0$ olan görevler kritiktir. Bu görevlerin oluşturduğu zincir kritik yoldur. Kritik görevlerden biri iki gün gecikirse, başka bir düzenleme yapılmadığı sürece proje de iki gün gecikir.

| Görev türü | Bolluk | Gecikmenin etkisi |
|---|---:|---|
| Kritik görev | $0$ | Proje doğrudan gecikebilir |
| Esnek görev | $> 0$ | Bolluk sınırına kadar tolere edilir |

## Python ile ileri geçiş

Aşağıdaki örnek, görevleri topolojik sırada işleyerek en erken zamanları hesaplar. `dependencies` sözlüğü her görevin öncüllerini tutar.

```python
from graphlib import TopologicalSorter

durations = {
    "analiz": 3,
    "tasarım": 4,
    "backend": 6,
    "frontend": 5,
    "test": 3
}

dependencies = {
    "analiz": set(),
    "tasarım": {"analiz"},
    "backend": {"tasarım"},
    "frontend": {"tasarım"},
    "test": {"backend", "frontend"}
}

order = list(TopologicalSorter(dependencies).static_order())
earliest_start = {}
earliest_finish = {}

for task in order:
    predecessors = dependencies[task]
    earliest_start[task] = max(
        (earliest_finish[p] for p in predecessors),
        default=0
    )
    earliest_finish[task] = (
        earliest_start[task] + durations[task]
    )

project_duration = max(earliest_finish.values())
print("Topolojik sıra:", order)
print("En erken bitişler:", earliest_finish)
print("Proje süresi:", project_duration)
```

Bu projede analiz ve tasarım ortak başlangıç zinciridir. Ardından backend ile frontend paralel ilerleyebilir; test ise ikisinin de bitmesini bekler. Backend daha uzun sürdüğü için testin başlama zamanını o belirler. Minimum proje süresi $3+4+6+3=16$ gündür.

## Karmaşıklık ve pratik notlar

Topolojik sıralama ile ileri ve geri geçişlerin toplam zaman karmaşıklığı $O(V+E)$ düzeyindedir. Burada $V$ görev, $E$ bağımlılık sayısıdır. Bu nedenle yöntem büyük projelerde de verimlidir.

CPM sürelerin kesin kabul edildiği deterministik bir modeldir. Gerçek hayatta tahminler belirsizse iyimser, olası ve kötümser süreleri kullanan PERT tercih edilebilir. Ayrıca grafikte döngü bulunursa geçerli bir plan yoktur: “A, B’yi; B de A’yı bekliyor” durumu algoritmik bir çıkmazdır. CPM, doğru bağımlılıklar ve gerçekçi sürelerle kullanıldığında takvimi göstermekten fazlasını yapar; yöneticinin dikkatini projenin gerçekten hassas noktalarına taşır.

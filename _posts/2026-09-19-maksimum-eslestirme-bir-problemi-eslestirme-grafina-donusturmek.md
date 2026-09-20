---
layout: post
title: "Maksimum Eşleştirme: Bir Problemi Eşleştirme Grafına Dönüştürmek"
math: true
categories: 
  - Bilgi
tags: 
  - graf teorisi
  - maksimum eşleştirme
  - algoritma
  - hopcroft-karp
  - problem modelleme
toc: true
image: /img/maksimum-eslestirme-bir-47.png
---

Bazı algoritma soruları kendilerini “öğrencileri projelere ata”, “işçileri görevlere yerleştir” veya “sunucuları isteklere bağla” diye tanıtır. Kılıkları farklı olsa da ortak hedef şudur: Birbiriyle uyumlu çiftlerden, hiçbir öğeyi iki kez kullanmadan mümkün olduğunca çok seçmek. İşte bu cümleyi fark ettiğimiz anda problem, maksimum eşleştirme grafına dönüşmeye başlar.
``
## Eşleştirme tam olarak nedir?

Bir graf $G=(V,E)$ üzerinde **eşleştirme**, ortak uç noktası bulunmayan kenarlardan oluşan bir $M$ kümesidir. Başka bir ifadeyle, seçilen her düğüm en fazla bir seçilmiş kenara katılabilir.

Maksimum eşleştirme ise kenar sayısı en büyük eşleştirmedir:

$$
\vert M^*\vert  = max_{M} \vert M\vert 
$$

Buradaki “maksimum” ile “maksimal” kavramlarını karıştırmamak önemlidir. Maksimal eşleştirmeye yeni kenar eklenemez; fakat bu, onun mümkün olan en büyük eşleştirme olduğu anlamına gelmez.

| Kavram | Anlamı | En iyi sonucu garanti eder mi? |
|---|---|---|
| Eşleştirme | Düğüm paylaşmayan kenarlar kümesi | Hayır |
| Maksimal eşleştirme | Daha fazla kenar eklenemeyen eşleştirme | Hayır |
| Maksimum eşleştirme | En çok kenara sahip eşleştirme | Evet |

![maksimum-eslestirme-bir-47](/img/maksimum-eslestirme-bir-47.svg)


## Problemi iki parçalı grafa çevirme

Atama problemlerinde çoğunlukla iki farklı varlık grubu bulunur. Örneğin öğrenciler ve projeler. Bu durumda $V=L union R$ olacak biçimde iki parçalı bir graf kurarız:

- $L$: Atanacak varlıklar, örneğin öğrenciler
- $R$: Hedefler, örneğin projeler
- $(u,v)$ kenarı: $u$ öğrencisinin $v$ projesine atanabilmesi

Diyelim ki Ayşe Python ve Web projelerini, Berk Web projesini, Ceren ise Python ve Mobil projelerini yapabiliyor. Her uygunluk için bir kenar ekleriz. Seçilen bir eşleştirme, geçerli atamaları temsil eder. Hiçbir öğrenci veya proje iki kez kullanılamadığı için eşleştirme kısıtı, problemin kuralını otomatik olarak uygular.

Dönüşüm yaparken şu kontrol listesi oldukça kullanışlıdır:

| Problem ifadesi | Graf karşılığı |
|---|---|
| İki farklı öğe grubu | Sol ve sağ düğüm kümeleri |
| Bir öğe diğerine atanabilir | Kenar |
| Her öğe en fazla bir kez kullanılabilir | Eşleştirme kısıtı |
| En çok sayıda atama istenir | Maksimum eşleştirme |

## Hopcroft–Karp ile çözüm

İki parçalı graflarda Hopcroft–Karp algoritması maksimum eşleştirmeyi $O(E sqrt(V))$ zamanda bulur. Algoritma BFS ile en kısa artırma yollarının katmanlarını oluşturur; DFS ile bu yollardan mümkün olduğunca çoğunu aynı turda kullanır.

Aşağıdaki Python kodu, sol taraftaki düğümler için verilen uygunluk listesini işler:

```python
from collections import deque

def maximum_matching(graph):
    left_match = {}
    right_match = {}
    distance = {}

    def bfs():
        queue = deque()
        for u in graph:
            if u not in left_match:
                distance[u] = 0
                queue.append(u)
            else:
                distance[u] = -1

        path_exists = False
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                partner = right_match.get(v)
                if partner is None:
                    path_exists = True
                elif distance[partner] < 0:
                    distance[partner] = distance[u] + 1
                    queue.append(partner)
        return path_exists

    def dfs(u):
        for v in graph[u]:
            partner = right_match.get(v)
            if partner is None or (
                distance.get(partner) == distance[u] + 1 and dfs(partner)
            ):
                left_match[u] = v
                right_match[v] = u
                return True
        distance[u] = -1
        return False

    while bfs():
        for u in graph:
            if u not in left_match:
                dfs(u)

    return left_match
```

Örnek girdi `{'Ayşe': ['Python', 'Web'], 'Berk': ['Web'], 'Ceren': ['Python', 'Mobil']}` biçimindedir. Sonuç sözlüğündeki her anahtar-değer çifti bir atamayı gösterir.

## Dönüşümün sınırlarını bilmek

Her atama problemi doğrudan basit eşleştirme değildir. Bir proje birden fazla öğrenci kabul ediyorsa kapasiteyi modellemek için düğümü kopyalamak veya akış ağı kurmak gerekebilir. Kenarların kazançları farklıysa maksimum sayıda değil, maksimum ağırlıklı eşleştirme aranır. Bir öğe birden fazla eşleşmeye katılabiliyorsa da klasik eşleştirme kısıtı artık yeterli değildir.

Özetle sihirli soru şudur: “Uyumlu çiftler seçerken her öğeyi en fazla bir kez mi kullanıyorum?” Yanıt evetse, grafı kurun; düğümleri varlıklara, kenarları uygunluklara dönüştürün. Problemin hikâyesi değişse bile algoritmik iskelet aynı kalacaktır.

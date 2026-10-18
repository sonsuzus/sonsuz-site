---
layout: post
title: "Çoklu Robotlarda Görev Tahsisi: Optimizasyon Neden Bu Kadar Zor?"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - optimizasyon
  - görev tahsisi
  - çoklu robot sistemleri
  - algoritmalar
  - karmaşıklık
toc: true
image: /img/coklu-robotlarda-gorev-73.png
---

Bir depoda onlarca robotun paket taşıdığını düşünün. Hangi robot hangi paketi almalı, görevler hangi sırada yapılmalı ve bataryası azalan robot ne zaman şarja gitmeli? İlk bakışta basit bir iş bölümü gibi görünen bu problem, seçeneklerin sayısı büyüdükçe kombinatoryal bir canavara dönüşür. Çoklu robot görev tahsisi, robotların yeteneklerini ve görevlerin gereksinimlerini eşleştirirken zaman, enerji ve mesafe gibi maliyetleri en aza indirmeyi amaçlar.


![coklu-robotlarda-gorev-73](/img/coklu-robotlarda-gorev-73.svg)

``

## Temel matematiksel model

$n$ robot ve $m$ görev bulunan bir sistemde $x_{ij}$, robot $i$ görev $j$ için seçildiyse 1, aksi durumda 0 olsun. $C_{ij}$ ise bu atamanın maliyetini temsil etsin. Basit model şöyledir:

$$
\min \sum_{i=1}^{n}\sum_{j=1}^{m} C_{ij}x_{ij}
$$

Her görevin tam olarak bir robota verilmesi istenirse:

$$
\sum_{i=1}^{n}x_{ij}=1, \qquad x_{ij}\in\{0,1\}
$$

Yalnızca bu koşullar mevcutsa problem, klasik doğrusal atama problemine dönüşür ve Macar algoritmasıyla yaklaşık $O(n^3)$ zamanda çözülebilir. Fakat gerçek robotlar matematik kitaplarındaki kadar uysal değildir. Kapasite sınırları, görev öncelikleri, zaman pencereleri, çarpışmalar, bağımlı görevler ve birlikte çalışması gereken robot ekipleri eklendiğinde problem çoğunlukla **NP-zor** hâle gelir.

## Karmaşıklığı artıran unsurlar

| Sistem özelliği | Optimizasyona etkisi | Tipik yaklaşım |
|---|---|---|
| Tek robot, tek görev | Basit eşleştirme | Macar algoritması |
| Bir robota çok görev | Sıralama da gerekir | Rotalama, MILP |
| Bir görevde çok robot | Ekip kombinasyonları oluşur | Koalisyon oluşturma |
| Zaman pencereleri | Uygun çözümler azalır | Kısıt programlama |
| Dinamik görev gelişi | Plan sürekli değişir | Çevrim içi algoritmalar |
| İletişim kısıtları | Küresel bilgi bulunmaz | Dağıtık açık artırma |

Örneğin $n$ robotun $n$ farklı göreve bire bir atanmasında $n!$ olası eşleştirme vardır. Yalnızca 10 robot için $10!=3.628.800$ seçenek bulunur. Görevlerin yapılma sırası da hesaba katıldığında arama uzayı daha hızlı büyür. Bu nedenle bütün olasılıkları deneyen kaba kuvvet yaklaşımı, küçük deneyler dışında pratik değildir.

Aşağıdaki Python kodu, bire bir atamalarda olası tahsisleri inceleyerek en düşük maliyetli çözümü bulur:

```python
from itertools import permutations

def en_iyi_tahsis(maliyetler):
    robot_sayisi = len(maliyetler)
    en_iyi_maliyet = float("inf")
    en_iyi_plan = None

    # Permütasyondaki indeks robotu, değer ise görevi temsil eder.
    for plan in permutations(range(robot_sayisi)):
        toplam = sum(
            maliyetler[robot][gorev]
            for robot, gorev in enumerate(plan)
        )
        if toplam < en_iyi_maliyet:
            en_iyi_maliyet = toplam
            en_iyi_plan = plan

    return en_iyi_plan, en_iyi_maliyet
```

Kod optimum sonucu garanti eder; ancak çalışma süresi $O(n!)$ olduğu için robot sayısı arttığında hızla kullanılamaz duruma gelir. Başka bir deyişle, doğru cevabı bulur ama kahveniz soğuyana kadar değil, bazen robotlar emekli olana kadar bekletebilir.

## Kesin çözüm mü, hızlı çözüm mü?

**MILP**, dal-sınır ve dinamik programlama gibi kesin yöntemler optimum çözüm sunabilir. Buna karşın büyük ve dinamik filolarda genetik algoritmalar, parçacık sürü optimizasyonu, tabu arama ve karınca kolonisi gibi sezgisel yöntemler tercih edilir. Bu yöntemler optimum garantisi vermese de kısa sürede kaliteli planlar üretir.

Merkezi sistemlerde tek bir sunucu tüm maliyetleri görerek karar verir. Dağıtık sistemlerde ise robotlar görevler için teklif verebilir. Bir robotun teklifi örneğin $b_{ij}=C_{ij}+\lambda E_{ij}$ biçiminde hesaplanabilir; burada $E_{ij}$ enerji tüketimi, $\lambda$ ise enerjinin önem katsayısıdır. Açık artırma tabanlı yöntemler iletişim kesintilerine daha dayanıklıdır, fakat küresel optimumdan uzaklaşabilir.

Sonuç olarak görev tahsisinin zorluğu yalnızca robot ve görev sayısından kaynaklanmaz. Görev bağımlılıkları, belirsizlik, hareket planlama ve gerçek zamanlı değişimler de karmaşıklığı belirler. Pratik tasarımlarda en iyi yaklaşım genellikle hibrittir: küçük alt problemler kesin yöntemlerle çözülür, büyük ölçekli kararlar sezgisel veya dağıtık algoritmalarla hızlandırılır. Robotlara iş dağıtırken asıl görev, mükemmel planı aramak ile zamanında karar vermek arasındaki dengeyi kurmaktır.

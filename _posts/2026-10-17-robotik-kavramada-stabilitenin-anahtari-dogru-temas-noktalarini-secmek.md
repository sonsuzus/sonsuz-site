---
layout: post
title: "Robotik Kavramada Stabilitenin Anahtarı: Doğru Temas Noktalarını Seçmek"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - grasp planning
  - temas mekaniği
  - optimizasyon
  - python
toc: true
image: /img/robotik-kavramada-stabilitenin-27.png
---

Bir robotun bardağı kavraması ilk bakışta yalnızca parmaklarını kapatmasından ibaret görünebilir. Oysa parmakların nesneye **nerede** dokunduğu; bardağın güvenle kaldırılması, kayması veya dramatik biçimde yere düşmesi arasındaki farkı belirler. Grasp planning, geometrik modeller ve fiziksel kısıtlar yardımıyla uygun temas noktalarını seçerek dış kuvvetlere dayanıklı bir kavrama üretmeyi amaçlar.

``

## Temas noktası neden bu kadar önemli?

Her temas noktası, nesneye uygulanabilecek kuvvetlerin yönünü sınırlar. Parmağın yüzeye uyguladığı normal kuvvet $f_n$, yüzeye dik yöndedir. Kaymayı engelleyen teğetsel kuvvet $f_t$ ise sürtünme katsayısı $\mu$ ile sınırlıdır:

$$
\vert f_t\vert  \leq \mu f_n
$$

Bu eşitsizlik, **Coulomb sürtünme modeli** olarak bilinir. İzin verilen kuvvetler üç boyutta bir sürtünme konisi, iki boyutta ise bir sürtünme kaması oluşturur. Temas noktaları kötü seçilmişse parmaklar güçlü motorlara sahip olsa bile gerekli yönde kuvvet üretemeyebilir.

Örneğin iki parmakla küresel bir nesne tutulurken temas noktalarının karşılıklı ve yüzey normallerinin yaklaşık aynı doğru üzerinde olması avantajlıdır. İki parmak birbirine yakın bölgelerde konumlandırılırsa nesne kolayca dönebilir. Yani mesele yalnızca kuvvet değil, kuvvetin oluşturduğu **torktur**.

Bir temas kuvvetinin nesne merkezine göre oluşturduğu tork:

$$
\tau_i = r_i \times f_i
$$

şeklindedir. Burada $r_i$, kütle merkezinden temas noktasına uzanan vektördür. Kuvvet ve tork birlikte **wrench** adı verilen $w_i = [f_i,\tau_i]$ gösterimiyle incelenir.

## Stabilite ölçütleri

İyi bir kavrama, yalnızca yer çekimini dengelememeli; farklı yönlerden gelebilecek küçük bozucu kuvvetlere de direnebilmelidir. Yaygın ölçütler aşağıda karşılaştırılmıştır:

| Ölçüt | Ne değerlendirir? | Avantajı | Sınırlaması |
|---|---|---|---|
| Force closure | Her yöndeki kuvvet ve torkun dengelenmesi | Güçlü teorik garanti | Kuvvet büyüklüğünü dikkate almayabilir |
| Form closure | Sürtünme olmadan geometrik kilitleme | Çok yüksek stabilite | Genellikle daha fazla temas ister |
| Ferrari-Canny | Wrench uzayındaki en zayıf yön | Kavramaları sıralamaya uygundur | Hesaplama maliyeti yüksektir |
| Temas mesafesi | Noktaların dağılımı ve açıklığı | Hızlı hesaplanır | Tek başına fiziksel garanti vermez |

**Force closure**, temas kuvvetlerinin pozitif kombinasyonlarıyla her dış wrench’in dengelenebilmesini ifade eder. Geometrik olarak temasların ürettiği wrench uzayının konveks örtüsü orijini içeriyorsa kavrama force closure sağlayabilir. Ferrari-Canny metriğinde ise orijinden bu örtünün en yakın sınırına olan mesafe kalite skoru olarak kullanılır. Mesafe büyüdükçe kavramanın en zayıf yöndeki dayanıklılığı artar.

## Basitleştirilmiş bir temas seçici

Aşağıdaki Python kodu, iki boyutlu bir nesne üzerindeki aday temas çiftlerini değerlendirir. Karşılıklı yüzey normallerini ve noktalar arasındaki uzaklığı ödüllendirir:

```python
import numpy as np
from itertools import combinations

def grasp_score(a, b):
    pa, na = a["point"], a["normal"]
    pb, nb = b["point"], b["normal"]

    distance = np.linalg.norm(pa - pb)
    opposition = np.clip(-np.dot(na, nb), 0.0, 1.0)
    center_error = np.linalg.norm((pa + pb) / 2)

    return 2.0 * opposition + distance - center_error

def best_pair(candidates):
    pairs = combinations(candidates, 2)
    return max(pairs, key=lambda pair: grasp_score(*pair))
```

`opposition`, normallerin zıt yönlere bakmasını teşvik eder. `distance`, temasların geniş bir taban oluşturmasını ödüllendirirken `center_error`, temas çiftinin nesne merkezinden gereksiz yere uzaklaşmasını cezalandırır. Gerçek sistemlerde bu skora sürtünme konileri, çarpışma kontrolü, eklem limitleri ve robotun temas noktalarına erişebilirliği de eklenir.

## Geometrik olarak iyi, robot için imkânsız olabilir

Nesne modeli üzerinde kusursuz görünen temaslar her zaman uygulanabilir değildir. Robot kolu hedef poza ulaşamayabilir, parmak başka bir yüzeye çarpabilir veya temas bölgesi sensör gürültüsü nedeniyle hatalı algılanabilir. Bu nedenle pratik grasp planning süreci; aday üretme, fiziksel kalite hesaplama, ters kinematik kontrolü ve çarpışma testini birlikte yürütür.

Sonuç olarak stabilite, parmak sayısından çok temasların ürettiği kuvvet ve tork çeşitliliğine bağlıdır. Doğru seçilmiş birkaç temas noktası, rastgele yerleştirilmiş çok sayıda temastan daha güvenilir olabilir. Robotik kavramanın küçük sırrı şudur: Robotun ne kadar güçlü tuttuğundan önce, **nereden tuttuğuna** bakmak gerekir.

![robotik-kavramada-stabilitenin-27](/img/robotik-kavramada-stabilitenin-27.svg)


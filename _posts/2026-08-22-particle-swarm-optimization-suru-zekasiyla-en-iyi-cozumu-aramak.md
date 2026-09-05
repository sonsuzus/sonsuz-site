---
layout: post
title: "Particle Swarm Optimization: Sürü Zekâsıyla En İyi Çözümü Aramak"
math: true
categories: 
  - Bilgi
tags: 
  - particle swarm optimization
  - optimizasyon
  - sürü zekâsı
image: /img/particle-swarm-optimization-71.png
---

![particle-swarm-optimization-71](/img/particle-swarm-optimization-71.svg)


Bir kuş sürüsünün yiyecek ararken lider beklemeden, hem kendi deneyiminden hem de komşularının hareketlerinden öğrenmesini düşünün. Particle Swarm Optimization (PSO), tam olarak bu gözlemden doğan sezgisel bir optimizasyon algoritmasıdır. Türev hesabına ihtiyaç duymadan karmaşık, doğrusal olmayan ve hatta gürültülü problemlerde iyi çözümler arar. Amaç, bir hedef fonksiyonun en küçük ya da en büyük değerini bulmaktır; sürü ise çözüm uzayında dolaşan aday çözümlerden oluşur.
``
PSO'da her **parçacık**, problemin olası bir çözümünü temsil eder. Örneğin iki değişkenli bir fonksiyonu minimize ediyorsak, parçacığın konumu $x_i = (x_{i1}, x_{i2})$ şeklinde iki sayıdır. Parçacığın ayrıca bir hızı $v_i$ vardır. Hız, bir sonraki turda hangi yönde ve ne kadar ilerleyeceğini söyler. Her parçacık şimdiye kadar gördüğü en iyi konumu, yani **kişisel en iyisini** ($pbest_i$), saklar. Tüm sürünün keşfettiği en başarılı konum ise **küresel en iyi** ($gbest$) adını alır.

Algoritmanın kalbi, hız güncelleme denklemidir:

$$v_i(t+1)=w v_i(t)+c_1 r_1(pbest_i-x_i(t))+c_2 r_2(gbest-x_i(t))$$

Ardından konum basitçe güncellenir:

$$x_i(t+1)=x_i(t)+v_i(t+1)$$

Buradaki $w$ ataleti temsil eder: yüksek olduğunda parçacık eski yönünü korur ve daha geniş keşif yapar. $c_1$ bilişsel katsayıdır; parçacığın kendi başarısına güvenmesini sağlar. $c_2$ sosyal katsayıdır; sürünün ortak bilgisine yönelmeyi güçlendirir. $r_1$ ve $r_2$ ise $[0,1]$ aralığında rastgele sayılardır. Bu rastlantısallık, bütün parçacıkların aynı noktaya mekanik biçimde çökmesini zorlaştırır.

| Kavram | Sürüdeki karşılığı | Algoritmadaki görevi |
|---|---|---|
| Konum | Aday çözüm | Parametre değerlerini taşır |
| Hız | Hareket eğilimi | Sonraki adımı belirler |
| $pbest$ | Bireysel hafıza | Yerel deneyimi korur |
| $gbest$ | Sürü bilgisi | Başarılı bölgeye yön verir |

PSO'nun önemli dengesi **keşif** ve **sömürü** arasındadır. Keşif, çözüm uzayının farklı bölgelerini denemektir. Sömürü ise umut vadeden bir bölgeyi daha ayrıntılı taramaktır. Çok yüksek $c_2$, sürüyü erken bir çözüme kilitleyebilir; buna erken yakınsama denir. Çok yüksek hızlar ise parçacıkların iyi bölgelerin üzerinden adeta roket gibi geçmesine yol açar. Bu yüzden hız genellikle $[-v_{max}, v_{max}]$ aralığında sınırlandırılır.

Aşağıdaki Python örneği, $f(x,y)=x^2+y^2$ fonksiyonunun minimumunu arar. Teorik minimum $(0,0)$ noktasındadır; kod, sürünün bu noktaya yaklaşmasını izler.

```python
import numpy as np

def objective(position):
    return np.sum(position ** 2, axis=1)

n_particles, dimensions, iterations = 30, 2, 80
positions = np.random.uniform(-5, 5, (n_particles, dimensions))
velocities = np.random.uniform(-1, 1, (n_particles, dimensions))
pbest = positions.copy()
pbest_scores = objective(pbest)
gbest = pbest[np.argmin(pbest_scores)].copy()

for _ in range(iterations):
    r1, r2 = np.random.rand(n_particles, dimensions), np.random.rand(n_particles, dimensions)
    velocities = (0.7 * velocities + 1.4 * r1 * (pbest - positions)
                  + 1.4 * r2 * (gbest - positions))
    positions += velocities

    scores = objective(positions)
    improved = scores < pbest_scores
    pbest[improved] = positions[improved]
    pbest_scores[improved] = scores[improved]
    gbest = pbest[np.argmin(pbest_scores)].copy()

print('En iyi konum:', gbest)
```

| Yöntem | Güçlü yanı | Sınırlaması |
|---|---|---|
| PSO | Türev gerektirmez, uygulanması kolaydır | Parametre seçimine duyarlıdır |
| Gradyan inişi | Düz ve türevlenebilir problemlerde hızlıdır | Yerel minimuma takılabilir |
| Genetik algoritma | Çeşitliliği uzun süre koruyabilir | Genellikle daha fazla işlem ister |

PSO; hiperparametre ayarı, özellik seçimi, rota planlama ve sinir ağı ağırlıklarının aranması gibi alanlarda kullanılır. Başarısının sırrı karmaşık biyolojik davranışı birebir taklit etmek değil; basit bireysel hafıza ile kolektif paylaşımın güçlü bir arama stratejisine dönüşmesidir.

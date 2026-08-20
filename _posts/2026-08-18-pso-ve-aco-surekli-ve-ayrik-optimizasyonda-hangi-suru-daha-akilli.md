---
layout: post
title: "PSO ve ACO: Sürekli ve Ayrık Optimizasyonda Hangi Sürü Daha Akıllı?"
math: true
categories: 
  - Bilgi
tags: 
  - optimizasyon
  - pso
  - aco
toc: true
---

Doğadaki kolektif davranışlar, zor optimizasyon problemlerine şaşırtıcı derecede iyi fikirler verir. Parçacık Sürüsü Optimizasyonu (PSO), kuş sürülerinin hedefe birlikte yönelmesinden; Karınca Kolonisi Optimizasyonu (ACO) ise karıncaların feromon izleriyle en kısa yolu bulmasından esinlenir. İkisi de türev bilgisi istemeyen, yerel minimum tuzaklarını aşmaya çalışan metasezgisel yöntemlerdir. Ancak çözüm uzayının sürekli mi yoksa ayrık mı olduğu, kazananı ciddi biçimde değiştirir.
``

## Ortak amaç, farklı hafıza biçimleri

Bir optimizasyon problemi genel olarak aşağıdaki gibi yazılır:

$$
\min_{x \in \Omega} f(x)
$$

Burada $f(x)$ maliyet fonksiyonu, $\Omega$ ise geçerli çözümlerin kümesidir. Sürekli problemlerde $x$ gerçek sayılardan oluşabilir; örneğin bir modelin öğrenme oranı, filtre katsayıları veya robot kolu açıları. Ayrık problemlerde ise rota sıralaması, görev ataması ya da seçilecek özellik kümesi gibi kombinasyonel kararlar bulunur.

PSO'da her parçacık bir aday çözüm taşır. Parçacık, kendi en iyi deneyimi ($pbest$) ile sürünün en iyi deneyimini ($gbest$) harmanlayarak hareket eder:

$$
v_i^{t+1}=\omega v_i^t+c_1r_1(pbest_i-x_i^t)+c_2r_2(gbest-x_i^t)
$$

$$
x_i^{t+1}=x_i^t+v_i^{t+1}
$$

ACO'da ise doğrudan konum güncellemek yerine çözüm adım adım inşa edilir. Bir karıncanın $i$ düğümünden $j$ düğümüne geçme olasılığı, feromon yoğunluğu $\tau_{ij}$ ve sezgisel bilginin $\eta_{ij}$ birleşimidir:

$$
P_{ij}=\frac{\tau_{ij}^{\alpha}\eta_{ij}^{\beta}}{\sum_{k \in N_i}\tau_{ik}^{\alpha}\eta_{ik}^{\beta}}
$$

Bu fark kritik: PSO "iyi konuma yaklaşmayı", ACO ise "iyi karar dizilerini tekrar üretmeyi" öğrenir.

| Özellik | PSO | ACO |
|---|---|---|
| Doğal çözüm temsili | Gerçek değerli vektör | Rota, permütasyon, seçim dizisi |
| Kolektif hafıza | En iyi parçacık konumları | Kenarlar/kararlar üzerindeki feromon |
| Güçlü olduğu alan | Sürekli parametre ayarı | Kombinasyonel ve graf tabanlı problemler |
| Başlıca risk | Erken yakınsama | Feromonun aşırı yoğunlaşması |

## Sürekli uzayda PSO'nun çevikliği

Sürekli fonksiyonlarda PSO genellikle daha doğal ve hesaplıdır. Konum ile hız kavramları zaten gerçek değerli uzaya uygundur. Örneğin bir sinir ağının hiperparametrelerini ayarlarken parçacık doğrudan `[öğrenme_oranı, dropout, katman_sayısı]` benzeri bir vektörü temsil edebilir. ACO'yu bu alana uyarlamak için değer aralıklarını bölmelere ayırmak gerekir; bu da hassasiyet kaybı veya çok büyük bir karar grafiği yaratabilir.

Basit bir PSO güncellemesi şöyle görünür:

```python
velocity = w * velocity + c1 * r1 * (pbest - position) \
           + c2 * r2 * (gbest - position)
position = position + velocity
```

Bu kod, parçacığın ataleti korumasını, kendi başarısından ders almasını ve sürünün liderine yönelmesini sağlar. Buna karşılık PSO, çok tepeli fonksiyonlarda tüm sürünün erken dönemde hatalı bir lidere kilitlenmesiyle zorlanabilir. Atalet ağırlığını zamanla azaltmak veya yerel komşuluklu PSO kullanmak bu riski düşürür.

## Ayrık dünyada ACO'nun feromon avantajı

Gezgin Satıcı Problemi (TSP), çizelgeleme ve araç rotalama gibi ayrık problemlerde ACO çoğu zaman daha anlamlıdır. Çünkü çözümün kalitesi sadece tek tek değerlerden değil, kararların sırasından doğar. ACO, iyi turlardaki kenarları feromonla güçlendirirken bu yapısal bilgiyi korur:

```python
for edge in best_tour:
    pheromone[edge] += Q / best_tour_length
pheromone *= (1 - evaporation)
```

İlk satır başarılı turun kenarlarını ödüllendirir; buharlaşma ise eski kararların sonsuza dek baskın kalmasını engeller. ACO'nun bedeli ise yüksektir: Her iterasyonda birçok karınca tam çözüm kurar ve büyük grafikte olasılık hesapları pahalılaşır.

| Problem türü | Genellikle tercih | Neden |
|---|---|---|
| Sürekli fonksiyon minimizasyonu | PSO | Doğrudan vektör hareketi ve az temsil maliyeti |
| Hiperparametre optimizasyonu | PSO veya hibrit | Gürültülü amaç fonksiyonlarında esnek arama |
| TSP ve rota planlama | ACO | Kenar bağımlılıklarını feromonla öğrenme |
| Özellik seçimi | İkisi de | İkili PSO hızlı, ACO daha yapı odaklı olabilir |

Sonuç olarak PSO ve ACO rakipten çok farklı arazi araçlarıdır. Düz ve sürekli bir parametre vadisinde PSO hızlı bir sürü halinde ilerler. Kavşaklar, sıralamalar ve yasak geçişlerle dolu ayrık bir şehirdeyse ACO, kolektif hafızasını izlere işleyerek daha güçlü bir rehber olur. En iyi seçim, algoritmanın popülerliğinden değil çözüm temsilinizin doğasından doğar.

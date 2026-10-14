---
layout: post
title: "Sıralama Algoritmalarında Kararlılık: Eşitler Arasında Düzeni Korumak"
math: true
categories: 
  - Bilgi
tags: 
  - sıralama algoritmaları
  - kararlılık
  - algoritma
  - veri yapıları
  - python
toc: true
image: /img/siralama-algoritmalarinda-kararlilik-74.png
---

Bir sıralama algoritması yalnızca elemanları küçükten büyüğe dizmekle kalmaz; bazen eşit kabul edilen elemanların geçmişine de saygı göstermelidir. İşte **kararlılık (stability)**, aynı sıralama anahtarına sahip elemanların başlangıçtaki göreli sırasının korunmasını ifade eder. İlk bakışta küçük bir ayrıntı gibi görünse de çok alanlı kayıtlar, raporlar ve kullanıcı arayüzleri söz konusu olduğunda sonuçları belirgin biçimde etkiler.

``

## Kararlılık tam olarak nedir?

Bir dizide $a_i$ ve $a_j$ elemanlarının sıralama anahtarları eşitse ve başlangıçta $a_i$, $a_j$ elemanından önce geliyorsa kararlı algoritma bu ilişkiyi sıralamadan sonra da korur.

Matematiksel olarak koşulu şöyle gösterebiliriz:

$$i < j \land k(a_i)=k(a_j) \Rightarrow p(a_i)<p(a_j)$$

Burada $k(a)$ elemanın sıralama anahtarını, $p(a)$ ise sıralanmış dizideki yeni konumunu temsil eder. Algoritma bu koşulu garanti etmiyorsa **kararsız** olarak adlandırılır. Kararsızlık, sonucun yanlış sıralandığı anlamına gelmez; yalnızca eşit elemanların kendi aralarında yer değiştirebileceğini söyler.

## Küçük ama açıklayıcı bir örnek

Bir yarışma listesinin geliş sırasıyla kaydedildiğini düşünelim:

| Başlangıç sırası | İsim | Puan |
|---:|---|---:|
| 1 | Ada | 90 |
| 2 | Ece | 75 |
| 3 | Mert | 90 |
| 4 | Can | 75 |

![siralama-algoritmalarinda-kararlilik-74](/img/siralama-algoritmalarinda-kararlilik-74.svg)


Listeyi puana göre azalan biçimde sıraladığımızda kararlı sonuç şöyledir:

| Yeni sıra | İsim | Puan |
|---:|---|---:|
| 1 | Ada | 90 |
| 2 | Mert | 90 |
| 3 | Ece | 75 |
| 4 | Can | 75 |

Ada ile Mert eşit puanlıdır ve Ada başlangıçta önce geldiği için yeni listede de öndedir. Benzer şekilde Ece, Can’ın önünde kalmıştır. Kararsız bir algoritma aynı puan sıralamasını üretirken bu ikililerin yerlerini değiştirebilir.

## Hangi algoritmalar kararlıdır?

Algoritmanın klasik uygulanışı dikkate alındığında genel görünüm şöyledir:

| Algoritma | Genellikle kararlı mı? | Temel neden |
|---|---|---|
| Bubble Sort | Evet | Yalnızca yanlış sıradaki komşuları değiştirir |
| Insertion Sort | Evet | Eşit elemanı gereksiz yere öne taşımaz |
| Merge Sort | Evet | Birleştirmede soldaki eşit eleman önce seçilebilir |
| Selection Sort | Hayır | Uzak eleman değişimleri göreli sırayı bozabilir |
| Quick Sort | Hayır | Bölümleme sırasında eşitler yer değiştirebilir |
| Heap Sort | Hayır | Kök ve uzak konum değişimleri düzeni korumaz |

Bu özellik algoritmanın isminden çok **uygulama biçimine** bağlıdır. Örneğin Merge Sort, eşitlik durumunda sağ taraftaki elemanı önce seçerse kararlılığını kaybedebilir.

## Kod üzerinde kararlı sıralama

Python’daki `sorted` fonksiyonu kararlıdır. Bu sayede kayıtları aşamalı olarak güvenle sıralayabiliriz:

```python
users = [
    {'name': 'Ada', 'department': 'Yazılım', 'age': 28},
    {'name': 'Mert', 'department': 'Tasarım', 'age': 28},
    {'name': 'Ece', 'department': 'Yazılım', 'age': 24},
]

# Önce ikincil anahtara göre sıralanır.
users = sorted(users, key=lambda user: user['name'])

# Kararlılık sayesinde isim sırası eşit bölümlerde korunur.
users = sorted(users, key=lambda user: user['department'])
```

İkinci sıralama bölümleri düzenlerken aynı bölümdeki kullanıcıların önceden oluşturulmuş isim sırasını bozmaz. Böylece birden fazla ölçüte göre sıralama yapılabilir. Bunun tek çağrılı karşılığı `key=lambda user: (user['department'], user['name'])` biçiminde bir demet kullanmaktır.

## Neden önemlidir?

Kararlılık özellikle veritabanı sonuçları, e-ticaret ürün listeleri, günlük kayıtları ve tablo arayüzlerinde önem kazanır. Kullanıcı ürünleri önce tarihe, ardından fiyata göre sıraladığında eşit fiyatlı ürünlerin tarih düzeninin korunmasını bekleyebilir. Düzen rastgele değişirse uygulama hatalı olmasa bile öngörülemez görünür.

Bununla birlikte her problem kararlı algoritma gerektirmez. Elemanlar benzersizse veya yalnızca sayısal nihai sıra önemliyse daha hızlı, daha az bellek kullanan kararsız bir yöntem tercih edilebilir. Doğru seçim; zaman karmaşıklığı, bellek tüketimi ve kararlılık beklentisinin birlikte değerlendirilmesiyle yapılır. Kısacası kararlılık, eşitlerin sıkıcı bir teknik detayı değil, verinin hikâyesini koruyan görünmez bir nezaket kuralıdır.

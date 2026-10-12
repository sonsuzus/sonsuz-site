---
layout: post
title: "Basamaklı Sıralama (Radix Sort): Karşılaştırmadan Sıralamanın Matematiği"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - radix-sort
  - sıralama
  - veri-yapıları
  - python
  - karmaşıklık
toc: true
image: /img/basamakli-siralama-radix-16.png
---

![basamakli-siralama-radix-16](/img/basamakli-siralama-radix-16.svg)


Bir sayı listesini sıralarken ilk refleksimiz sayıları ikişer ikişer karşılaştırmaktır. Radix Sort ise masaya farklı bir fikir koyar: “Sayıların tamamını karşılaştırmak yerine basamaklarını sırayla incelesek?” Bu yaklaşım sayesinde uygun koşullarda karşılaştırmaya dayalı algoritmaların $O(n \log n)$ sınırını aşarak doğrusal zamana yaklaşabiliriz.

``

## Temel fikir: Sayının tamamına değil, basamaklarına bak

Basamaklı Sıralama, sayıları birler, onlar, yüzler gibi basamaklarına göre gruplandırır. En yaygın sürüm olan **LSD Radix Sort**, işleme en sağdaki, yani en az anlamlı basamaktan başlar.

Örneğin şu sayıları ele alalım:

`170, 45, 75, 90, 802, 24, 2, 66`

İlk turda birler basamağına, ikinci turda onlar basamağına, üçüncü turda yüzler basamağına bakılır. Her turun sonunda sayılar ilgili basamağa göre düzenlenir. Son basamak işlendiğinde liste tamamen sıralanmış olur.

| Tur | İncelenen basamak | Örnek sonuç |
|---|---|---|
| 1 | Birler | 170, 90, 802, 2, 24, 45, 75, 66 |
| 2 | Onlar | 802, 2, 24, 45, 66, 170, 75, 90 |
| 3 | Yüzler | 2, 24, 45, 66, 75, 90, 170, 802 |

Buradaki kritik ayrıntı, her basamak sıralamasının **kararlı** olmasıdır. Kararlı bir sıralama, aynı anahtar değerine sahip elemanların önceki göreli sırasını korur. Aksi hâlde önceki basamaklarda oluşturulan düzen bozulur ve algoritmanın sihri, pek de sihirli olmayan bir şekilde kaybolur.

## Neden doğrusal olabilir?

$n$ eleman, en büyük sayıda $d$ basamak ve kullanılan sayı tabanında $b$ farklı rakam bulunsun. Her basamak için Counting Sort benzeri bir işlem uygulanırsa zaman karmaşıklığı şöyledir:

$$T(n) = O(d(n+b))$$

Ondalık sayılarda $b=10$ sabittir. Basamak sayısı $d$ de sınırlıysa karmaşıklık yaklaşık olarak $O(n)$ kabul edilir. Ancak sayıların basamak sayısı veri büyüklüğüyle birlikte ciddi biçimde artıyorsa “her zaman doğrusal” demek doğru değildir.

| Algoritma | Ortalama süre | Karşılaştırma yapar mı? | Ek bellek |
|---|---:|---|---:|
| Radix Sort | $O(d(n+b))$ | Hayır | $O(n+b)$ |
| Merge Sort | $O(n \log n)$ | Evet | $O(n)$ |
| Quick Sort | $O(n \log n)$ | Evet | Genellikle $O(\log n)$ |
| Counting Sort | $O(n+k)$ | Hayır | $O(k)$ |

## Python ile Radix Sort

Aşağıdaki uygulama negatif olmayan tam sayıları LSD yaklaşımıyla sıralar. Her turda on adet kova oluşturulur; sayılar ilgili basamaklarına göre bu kovalara dağıtılır ve aynı sırayla yeniden birleştirilir.

```python
def radix_sort(numbers):
    if not numbers:
        return []

    result = numbers.copy()
    maximum = max(result)
    place = 1

    while maximum // place > 0:
        buckets = [[] for _ in range(10)]

        # Sayıları mevcut basamağa göre kovalara dağıt.
        for number in result:
            digit = (number // place) % 10
            buckets[digit].append(number)

        # Kovaların sırası korunarak listeyi yeniden oluştur.
        result = [number for bucket in buckets for number in bucket]
        place *= 10

    return result

values = [170, 45, 75, 90, 802, 24, 2, 66]
print(radix_sort(values))
```

Kovaların liste olarak kullanılması kararlılığı doğal biçimde sağlar. Aynı rakama sahip sayılar kovaya giriş sıralarını koruyarak çıkar.

## Ne zaman tercih edilmeli?

Radix Sort; kimlik numaraları, sabit uzunluktaki sayısal kodlar, IP adresleri veya çok sayıda tam sayı gibi yapılandırılmış verilerde oldukça etkilidir. Buna karşılık değişken uzunluklu veriler, ondalıklı sayılar ve negatif değerler ek uyarlamalar gerektirir. Negatif sayılar genellikle mutlak değerlerine göre ayrı sıralanıp ters çevrilerek pozitiflerle birleştirilir.

Kısacası Radix Sort, karşılaştırma yapmadan sıralamanın mümkün olduğunu gösteren zarif bir algoritmadır. Doğru veri türünde kullanıldığında basamakları tek tek tırmanır ve listenin zirvesine beklenmedik bir hızla ulaşır.

---
layout: post
title: "En Uzun Tekrar Eden Alt Dizgi: Son Ek Dizileriyle Metnin Gizli Tekrarlarını Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - son-ek-dizisi
  - metin-işleme
  - python
  - lcp
  - veri-yapıları
toc: true
image: /img/en-uzun-tekrar-83.png
---

![en-uzun-tekrar-83](/img/en-uzun-tekrar-83.svg)


Bir metnin içinde en az iki kez geçen en uzun parça hangisidir? İlk bakışta bütün alt dizgileri üretip karşılaştırmak makul görünebilir. Ancak metin büyüdüğünde bu yöntem, samanlıkta iğne ararken önce bütün samanları tek tek numaralandırmaya dönüşür. Son ek dizisi ve LCP dizisi ise tekrarları düzenli, hızlı ve şaşırtıcı derecede zarif biçimde ortaya çıkarır.
``
## Problem tam olarak nedir?

Bir $S$ metni verildiğinde, metin içinde farklı başlangıç konumlarında en az iki kez bulunan en uzun **alt dizgiyi** ararız. Örneğin `banana` metninde cevap `ana` olur:

- İlk geçiş: `b[ana]na`
- İkinci geçiş: `ban[ana]`

Geçişlerin çakışmasına izin verilebilir. Örneğin `aaaa` içinde `aaa`, 0 ve 1 indislerinden başlayarak iki kez görünür.

Naif yaklaşım tüm alt dizgileri karşılaştırır. Uzunluğu $n$ olan bir metinde yaklaşık $n(n+1)/2$ alt dizgi bulunduğundan maliyet hızla büyür.

| Yaklaşım | Temel fikir | Yaklaşık zaman | Bellek |
|---|---|---:|---:|
| Kaba kuvvet | Bütün alt dizgileri karşılaştır | $O(n^3)$ | $O(1)$–$O(n^2)$ |
| Hash tabanlı arama | Uzunluğu ikili arayıp hash karşılaştır | $O(n \log n)$ | $O(n)$ |
| Son ek dizisi + LCP | Sıralı son eklerin ortak öneklerini ölç | $O(n \log n)$ | $O(n)$ |

## Son ek dizisi neden işe yarar?

Bir **son ek**, metnin herhangi bir konumundan başlayıp sona kadar giden parçadır. `banana` için son ekler şöyledir:

| Başlangıç | Son ek |
|---:|---|
| 0 | banana |
| 1 | anana |
| 2 | nana |
| 3 | ana |
| 4 | na |
| 5 | a |

Bunlar alfabetik sıralandığında başlangıç indisleri `[5, 3, 1, 0, 4, 2]` olur. Bu indis listesine **son ek dizisi** denir.

Kritik fikir şudur: Ortak başlangıca sahip son ekler alfabetik sıralamada yan yana gelir. Dolayısıyla bütün son ek çiftlerini karşılaştırmak yerine yalnızca komşuları incelemek yeterlidir.

Komşu son eklerin ortak önek uzunluklarını tutan yapıya **LCP** (*Longest Common Prefix*) dizisi denir. Aradığımız sonuç:

$$L = \max_{1 \le i < n} LCP[i]$$

`banana` için en büyük LCP değeri 3'tür; ilgili parça `ana`dır.

## Python ile çözüm

Aşağıdaki uygulama, son ek dizisini önek katlama yöntemiyle kurar. Her turda karşılaştırılan önek uzunluğu iki katına çıkar. Ardından Kasai algoritması LCP dizisini doğrusal zamanda hesaplar.

```python
def suffix_array(text):
    n = len(text)
    sa = list(range(n))
    rank = [ord(ch) for ch in text]
    k = 1

    while k < n:
        sa.sort(key=lambda i: (
            rank[i],
            rank[i + k] if i + k < n else -1
        ))

        new_rank = [0] * n
        for j in range(1, n):
            previous, current = sa[j - 1], sa[j]
            prev_key = (rank[previous],
                        rank[previous + k] if previous + k < n else -1)
            curr_key = (rank[current],
                        rank[current + k] if current + k < n else -1)
            new_rank[current] = new_rank[previous] + (prev_key != curr_key)

        rank = new_rank
        if rank[sa[-1]] == n - 1:
            break
        k *= 2

    return sa


def longest_repeated_substring(text):
    if not text:
        return ""

    sa = suffix_array(text)
    rank = [0] * len(text)
    for position, suffix_start in enumerate(sa):
        rank[suffix_start] = position

    best_length = best_start = common = 0

    for i in range(len(text)):
        position = rank[i]
        if position == 0:
            continue

        j = sa[position - 1]
        while (i + common < len(text) and
               j + common < len(text) and
               text[i + common] == text[j + common]):
            common += 1

        if common > best_length:
            best_length, best_start = common, i

        common = max(0, common - 1)

    return text[best_start:best_start + best_length]


print(longest_repeated_substring("banana"))  # ana
```

Kasai algoritmasındaki `common` değerinin her adımda tamamen sıfırlanmaması önemlidir. Bir sonraki son eke geçildiğinde ortak önek uzunluğu en fazla bir azalır; böylece tekrar tekrar aynı karakterleri okumaktan kaçınılır.

## Karmaşıklık ve kullanım alanları

Bu Python uygulamasında sıralama nedeniyle son ek dizisinin kurulması yaklaşık $O(n \log^2 n)$, LCP hesabı ise $O(n)$ sürer. Özel sıralama teknikleriyle toplam süre $O(n \log n)$, gelişmiş yöntemlerle $O(n)$ seviyesine indirilebilir.

Aynı yaklaşım DNA dizilerindeki tekrarları, belgelerdeki kopya bölümleri, sıkıştırılabilir kalıpları ve kod içindeki benzer parçaları bulmak için kullanılabilir. Kısacası son ek dizisi, metni yalnızca sıralamaz; görünmeyen tekrarların yan yana gelmesini sağlayarak problemi kolay bir maksimum aramasına dönüştürür.

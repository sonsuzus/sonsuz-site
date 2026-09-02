---
layout: post
title: "Katalan Sayılarının Geometrik Dünyası: Parantezlerden Çokgenlere"
math: true
categories: 
  - Bilgi
tags: 
  - katalan sayıları
  - kombinatorik
  - geometri
toc: true
---

Bir sayı dizisinin hem düzgün parantez ifadelerini hem de çokgenlerin üçgenlere ayrılma biçimlerini sayması ilk bakışta matematiksel bir tesadüf gibi görünebilir. Oysa Katalan sayıları, farklı görünen bu problemlerin altında aynı dallanma ve özyineleme yapısının bulunduğunu gösterir. Dizi $1, 1, 2, 5, 14, 42, 132, \ldots$ biçiminde ilerler ve kombinatoriğin adeta İsviçre çakısıdır.

``

## Katalan sayısı nedir?

$n$ indisli Katalan sayısının kapalı formülü şöyledir:

$$
C_n = \frac{1}{n+1}\binom{2n}{n}
$$

Buradaki $\binom{2n}{n}$, $2n$ adım arasından $n$ tanesini seçmenin sayısını verir. Ancak bütün seçimler geçerli değildir. Örneğin parantez probleminde hiçbir noktada kapanan parantezlerin sayısı açılanlardan fazla olamaz. Formüldeki $\frac{1}{n+1}$ çarpanı, bu geçersiz düzenlemelerin elenmesinin sonucudur.

Katalan sayıları ayrıca şu özyinelemeli bağıntıyı sağlar:

$$
C_n = \sum_{i=0}^{n-1} C_i C_{n-1-i}, \qquad C_0=1
$$

Bu formülün temel fikri bir yapıyı ilk ayrılma noktasından iki bağımsız alt yapıya bölmektir. Sol tarafta $i$ eleman, sağ tarafta ise $n-1-i$ eleman bulunur.

## Parantez eşleştirme ve Dyck yolları

$n$ çift parantezin kaç farklı geçerli biçimde eşleştirilebileceğini $C_n$ verir. Örneğin $n=3$ için beş düzenleme vardır:

```text
((()))   (()())   (())()   ()(())   ()()()
```

Bu ifadeleri geometrik bir yürüyüşe dönüştürebiliriz. Her `(` karakterini bir birim yukarı, her `)` karakterini bir birim aşağı giden adım olarak düşünelim. Geçerli bir ifade, yüksekliği hiçbir zaman sıfırın altına inmeyen ve başladığı seviyeye dönen bir yol üretir. Bu yapılara **Dyck yolu** denir.

| Kombinatoryal nesne | Geometrik karşılığı | Geçerlilik koşulu |
|---|---|---|
| Açılan parantez | Yukarı adım | Yeni bir yapı başlatır |
| Kapanan parantez | Aşağı adım | Açılmış yapıyı kapatır |
| Geçerli ifade | Dyck yolu | Yol eksenin altına inmez |
| Tam eşleşme | Başlangıca dönüş | Yukarı ve aşağı adımlar eşittir |

Böylece parantez kontrolü, soyut bir metin problemi olmaktan çıkıp bir yol sayma problemine dönüşür.

## Çokgen üçgenleme

Köşegenleri kesiştirmeden dışbükey bir $(n+2)$-geni üçgenlere ayırmanın farklı yollarının sayısı da $C_n$ değeridir. Örneğin beşgen için $n=3$ olur ve sonuç $C_3=5$ biçimindedir.

Belirli bir kenarı taban olarak seçelim. Bu tabanın içinde bulunduğu üçgenin üçüncü köşesi, çokgeni sol ve sağ olmak üzere iki küçük çokgene ayırır. Alt çokgenlerin üçgenleme sayıları bağımsız olduğundan sonuçlar çarpılır; üçüncü köşenin bütün konumları toplandığında Katalan özyinelemesi ortaya çıkar. Parantezlerdeki iç ve dış gruplar ile çokgendeki sol ve sağ bölgeler aslında aynı matematiksel iskeleti taşır.

## Python ile hesaplama

Aşağıdaki kod, özyinelemeli bağıntıyı dinamik programlama ile uygular. Önceden hesaplanan değerleri sakladığı için aynı alt problemleri tekrar çözmez:

```python
def katalan(n):
    sayilar = [0] * (n + 1)
    sayilar[0] = 1

    for boyut in range(1, n + 1):
        for sol in range(boyut):
            sag = boyut - 1 - sol
            sayilar[boyut] += sayilar[sol] * sayilar[sag]

    return sayilar[n]

print(katalan(5))  # 42
```

Algoritmanın zaman karmaşıklığı $O(n^2)$, bellek karmaşıklığı ise $O(n)$ düzeyindedir. Kapalı formül büyük indislerde daha hızlı olabilir; dinamik programlama ise dizinin yapısını daha görünür kılar.

Katalan sayıları ikili ağaçları, yığınla üretilebilen permütasyonları ve dağ silüetlerini de sayar. Yaklaşık büyümeleri

$$
C_n \sim \frac{4^n}{n^{3/2}\sqrt{\pi}}
$$

olduğundan oldukça hızlı çoğalırlar. Sonuç olarak aynı sayıların farklı problemlerde belirmesi sihir değil, aralarındaki yapıyı koruyan bire bir eşlemelerin, yani bijeksiyonların doğal sonucudur.

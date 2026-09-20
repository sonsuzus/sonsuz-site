---
layout: post
title: "Coordinate Compression: Dev Koordinatları Küçük Dizilere Dönüştürmek"
math: true
categories: 
  - Bilgi
tags: 
  - coordinate-compression
  - algoritma
  - veri-yapıları
  - c-plus-plus
  - rekabetçi-programlama
toc: true
image: /img/coordinate-compression-dev-90.png
---

![coordinate-compression-dev-90](/img/coordinate-compression-dev-90.svg)


Bir milyara kadar uzanan koordinatlarınız olduğunu düşünün. Elinizde yalnızca birkaç bin nokta bulunmasına rağmen `int dizi[1000000001]` oluşturmak, küçük bir kargo için uçak kiralamaya benzer. Coordinate Compression, yani koordinat sıkıştırma, büyük fakat seyrek değerleri sıralarını koruyarak küçük indislerle temsil etmemizi sağlar. Böylece dev koordinatlar, standart diziler ve verimli veri yapılarıyla işlenebilir hâle gelir.

``

## Temel fikir

Elimizde şu koordinatlar olsun:

```text
[1000000000, 25, 900, 25, -40]
```

Önce değerlerin kopyasını alır, sıralar ve tekrarları kaldırırız:

```text
[-40, 25, 900, 1000000000]
```

Ardından her değeri sıralı listedeki konumuyla değiştiririz:

```text
1000000000 -> 3
25         -> 1
900        -> 2
-40        -> 0
```

Matematiksel olarak sıkıştırma fonksiyonu şöyle tanımlanabilir:

$$f(x) = \operatorname{rank}(x)$$

Buradaki `rank`, değerin sıralanmış benzersiz değerler arasındaki sırasıdır. Eğer $a < b$ ise mutlaka $f(a) < f(b)$ olur. Yani gerçek uzaklıklar korunmaz; yalnızca sıralama ilişkisi korunur. Örneğin `25` ile `900` arasındaki fark sıkıştırılmış dizide yalnızca `1` olabilir. Bu nedenle yöntem, mesafe hesabından çok sıralama ve aralık sorgularında kullanışlıdır.

| Özellik | Orijinal koordinat | Sıkıştırılmış koordinat |
|---|---:|---:|
| Değer aralığı | Çok büyük olabilir | $0$ ile $k-1$ arası |
| Sıralama ilişkisi | Korunur | Korunur |
| Gerçek mesafe | Mevcuttur | Korunmaz |
| Dizi indisi olarak kullanım | Riskli veya imkânsız | Güvenli |
| Bellek ihtiyacı | Koordinat aralığına bağlı | Benzersiz değer sayısına bağlı |

## C++ ile uygulama

Aşağıdaki kod, koordinatları sıkıştırır ve sonuçları sıfır tabanlı indisler olarak üretir:

```cpp
#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

int main() {
    vector<long long> coordinates = {
        1000000000LL, 25, 900, 25, -40
    };

    // Orijinal veriyi bozmamak için bir kopya oluşturuyoruz.
    vector<long long> sorted = coordinates;

    sort(sorted.begin(), sorted.end());

    // unique tekrarları sona taşır; erase bu kısmı siler.
    sorted.erase(unique(sorted.begin(), sorted.end()), sorted.end());

    vector<int> compressed;

    for (long long value : coordinates) {
        int index = lower_bound(
            sorted.begin(), sorted.end(), value
        ) - sorted.begin();

        compressed.push_back(index);
    }

    for (int index : compressed) {
        cout << index << ' ';
    }
}
```

Programın çıktısı şöyledir:

```text
3 1 2 1 0
```

`lower_bound`, aranan değerin sıralı vektördeki ilk konumunu bulur. Sıralama işlemi $O(n \log n)$, her arama ise $O(\log n)$ sürer. Toplam zaman karmaşıklığı:

$$O(n \log n)$$

Ek bellek ihtiyacı ise $O(n)$ seviyesindedir.

## Nerelerde kullanılır?

Coordinate Compression özellikle Fenwick Tree, Segment Tree ve prefix sum gibi indis tabanlı yapılarda parlar. Örneğin koordinatları `10`, `500000` ve `900000000` olan üç olay için bir milyarlık dizi oluşturmak yerine yalnızca üç elemanlık yapı kullanılabilir.

| Senaryo | Sıkıştırma uygun mu? | Neden? |
|---|---|---|
| Noktaların sırasını karşılaştırmak | Evet | Küçüklük-büyüklük ilişkisi korunur |
| Aralıkta kaç eleman bulunduğunu bulmak | Evet | İndis tabanlı yapılar kullanılabilir |
| İki nokta arasındaki gerçek mesafeyi hesaplamak | Tek başına hayır | Sayısal farklar korunmaz |
| Dev ve seyrek koordinatlarla dizi oluşturmak | Evet | Bellek tüketimini ciddi biçimde azaltır |

Gerçek koordinatlara daha sonra ihtiyaç duyulacaksa sıralanmış benzersiz vektörü saklamak yeterlidir. Sıkıştırılmış `i` indisinin asıl değeri `sorted[i]` ile geri alınabilir.

Özetle coordinate compression, sayıları küçültmekten ziyade onları akıllıca yeniden etiketler. Büyük koordinat evrenini, yalnızca gerçekten kullanılan değerlerden oluşan kompakt bir mahalleye dönüştürür. Özellikle rekabetçi programlamada “koordinatlar çok büyük ama eleman sayısı küçük” ipucunu gördüğünüzde, bu teknik güçlü bir adaydır.

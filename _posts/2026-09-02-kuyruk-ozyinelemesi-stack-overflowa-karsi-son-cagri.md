---
layout: post
title: "Kuyruk Özyinelemesi: Stack Overflow’a Karşı Son Çağrı"
math: true
categories: 
  - Bilgi
tags: 
  - tail-recursion
  - algoritmalar
  - bellek-yonetimi
toc: true
---

Özyineleme, bir fonksiyonun problemi küçülterek kendisini çağırmasıdır. Zarif görünür; fakat her çağrı bellekte yeni bir yığın çerçevesi oluşturduğunda binlerce adım sonra programımız dramatik biçimde “Stack Overflow!” diye bağırabilir. Kuyruk özyinelemesi (tail recursion), özyinelemeli çağrıyı fonksiyonun son işlemi hâline getirerek çalışma zamanına bu çerçeveleri yeniden kullanma fırsatı verir.
``
## Çağrı yığını neden büyür?

Bir fonksiyon çağrıldığında dönüş adresi, parametreler ve yerel değişkenler genellikle **call stack** üzerindeki bir çerçevede saklanır. Normal özyinelemede eski çağrı, yeni çağrının sonucunu beklediği için bellekte kalır.

Faktöriyel fonksiyonunu düşünelim:

```javascript
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}
```

Burada `factorial(n - 1)` döndükten sonra çarpma yapılacaktır. Dolayısıyla bekleyen işlemler şöyle birikir:

```text
factorial(4)
4 * factorial(3)
4 * 3 * factorial(2)
4 * 3 * 2 * factorial(1)
```

Zaman karmaşıklığı $T(n)=T(n-1)+O(1)=O(n)$ olur. Yığın belleği de $S(n)=O(n)$ seviyesine çıkar. `n` yeterince büyürse kullanılabilir yığın alanı tükenir.

## Kuyruk çağrısının püf noktası

Bir çağrıdan sonra yapılacak hiçbir işlem kalmıyorsa bu çağrı **kuyruk konumundadır**. Ara sonucu bir akümülatörde taşıyarak faktöriyeli dönüştürebiliriz:

```javascript
function factorialTail(n, accumulator = 1) {
  if (n <= 1) return accumulator;

  // Son işlem doğrudan özyinelemeli çağrıdır.
  return factorialTail(n - 1, n * accumulator);
}
```

Artık çarpma, bir sonraki çağrıdan **önce** yapılır. Fonksiyonun saklanması gereken bekleyen işi yoktur. Kuyruk çağrısı optimizasyonu (TCO) destekleyen bir çalışma zamanı, yeni çerçeve açmak yerine mevcut çerçevenin parametrelerini güncelleyip başlangıca sıçrayabilir.

| Özellik | Normal özyineleme | Optimize kuyruk özyinelemesi | Döngü |
|---|---|---|---|
| Zaman karmaşıklığı | $O(n)$ | $O(n)$ | $O(n)$ |
| Yığın kullanımı | $O(n)$ | $O(1)$ | $O(1)$ |
| Bekleyen işlem | Vardır | Yoktur | Yoktur |
| Matematiksel anlatım | Güçlü | Güçlü | Daha mekanik |

Önemli ayrıntı şudur: Bir fonksiyonun kuyruk özyinelemeli yazılması, otomatik olarak sabit bellek kullanacağı anlamına gelmez. **Derleyici veya çalışma zamanı TCO uygulamalıdır.** Scheme gibi diller bunu garanti ederken Python bilinçli olarak desteklemez. JavaScript standardında uygun kuyruk çağrıları tanımlanmış olsa da motor desteği yaygın ve tutarlı değildir. Java ve çoğu JVM uygulaması da genel bir garanti sunmaz.

## Güvenli alternatif: Döngüye dönüştürmek

Çalışma ortamınız TCO sağlamıyorsa aynı durum yönetimini açıkça bir döngüyle gerçekleştirebilirsiniz:

```python
def factorial_iterative(n):
    accumulator = 1

    while n > 1:
        accumulator *= n
        n -= 1

    return accumulator
```

Bu sürümde `n` ve `accumulator`, özyinelemeli fonksiyonun durumunu temsil eder. Her turda aynı yerel değişkenler güncellendiğinden çağrı yığını büyümez. Başka bir ifadeyle çalışma zamanı optimizasyonuna güvenmek yerine optimizasyonu kendimiz yazmış oluruz.

## Her özyineleme kuyruk özyinelemesi değildir

Ağaç dolaşımı gibi bir çağrıdan sonra ikinci dalın işlenmesi gereken algoritmalar doğrudan kuyruk konumunda olmayabilir. Örneğin `return visit(left) + visit(right)` ifadesinde toplama ve ikinci çağrı beklemektedir. Böyle durumlarda açık bir yığın veri yapısı, trampoline tekniği veya continuation-passing style kullanılabilir.

Kısacası kuyruk özyinelemesi yalnızca “fonksiyonun sonunda kendini çağırması” değil, çağrı döndükten sonra **hiçbir iş kalmaması** ilkesidir. Dil desteği varsa özyinelemenin okunabilirliğini $O(1)$ yığın tüketimiyle birleştirir; yoksa aynı modeli döngüye çevirmek, stack overflow canavarını uzak tutan en güvenilir kalkandır.

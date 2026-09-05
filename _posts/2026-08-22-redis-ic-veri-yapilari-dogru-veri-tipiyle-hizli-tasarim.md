---
layout: post
title: "Redis İç Veri Yapıları: Doğru Veri Tipiyle Hızlı Tasarım"
math: true
categories: 
  - Bilgi
tags: 
  - redis
  - veri yapıları
  - performans
toc: true
image: /img/redis-ic-veri-81.png
---

![redis-ic-veri-81](/img/redis-ic-veri-81.svg)


Redis, çoğu zaman yalnızca "anahtar-değer önbelleği" olarak tanıtılır; ancak bu tanım onun asıl gücünü biraz saklar. Redis, bellekte yaşayan ve her anahtar altında farklı veri yapıları sunan bir veri sunucusudur. Doğru veri tipini seçmek, hem komut sayısını hem de bellek tüketimini azaltır. Daha da önemlisi, veriye erişim maliyetini uygulamanın kullanım senaryosuna uygun hale getirir.
``
## Neden veri tipi seçimi önemlidir?

Bir veritabanı işleminin maliyeti kabaca veri boyutuna ve algoritmanın karmaşıklığına bağlıdır. Örneğin bir listenin başına eleman eklemek çoğunlukla $O(1)$ iken, sıralanmamış bir koleksiyonda belirli bir öğeyi bulmak $O(n)$ olabilir. Buradaki $n$, koleksiyondaki eleman sayısıdır. Redis komutlarının beklenen zaman karmaşıklıklarını bilmek, yoğun trafikte sürpriz gecikmeleri önler.

| Veri tipi | En iyi kullanım alanı | Örnek komutlar | Tipik maliyet |
|---|---|---|---|
| String | Sayaç, oturum, önbellek | `GET`, `SET`, `INCR` | $O(1)$ |
| Hash | Nesne özellikleri | `HSET`, `HGET`, `HINCRBY` | $O(1)$ |
| List | Kuyruk, son olaylar | `LPUSH`, `BRPOP`, `LRANGE` | Uçlarda $O(1)$ |
| Set | Benzersiz üyelik | `SADD`, `SISMEMBER`, `SINTER` | Üyelikte $O(1)$ |
| Sorted Set | Skor tablosu, zaman sırası | `ZADD`, `ZRANGE` | $O(\log n)$ |

## String: Küçük ama çok yönlü

Redis String değeri metin, sayı veya ikili veri taşıyabilir. Bir sayacı uygulama tarafında okuyup artırıp tekrar yazmak yerine `INCR` kullanmak atomiktir. Yani iki istek aynı anda geldiğinde güncelleme kaybı yaşanmaz. Ayrıca `EX` veya `SETEX` ile yaşam süresi (TTL) vermek, geçici önbellek kayıtları için idealdir.

```redis
SET session:42 "user-data" EX 3600
INCR page:home:views
GET session:42
```

Bu örnekte oturum bir saat sonra otomatik silinir, sayfa görüntüleme sayısı ise güvenli biçimde artar. String, tek parça halinde okunacak veriler için harikadır; fakat bir kullanıcının yalnızca e-posta alanını güncellemek istiyorsanız Hash daha mantıklıdır.

## Hash: Nesneleri alan alan saklamak

Hash, bir anahtar altında alan-değer çiftleri tutar. `user:42` gibi bir anahtarın içinde `name`, `email` ve `login_count` alanları bulunabilir. Böylece küçük bir değişiklik için tüm JSON belgesini alıp yeniden yazmak gerekmez.

```redis
HSET user:42 name "Ada" email "ada@example.com" login_count 0
HINCRBY user:42 login_count 1
HMGET user:42 name login_count
```

Hash, profil, ürün özeti veya ayar kayıtları için uygundur. Ancak derin iç içe JSON sorguları gerekiyorsa Redis'in temel Hash modeli tek başına yeterli olmayabilir; RedisJSON gibi ek modüller değerlendirilmelidir.

## List, Set ve Sorted Set: Koleksiyonların üç karakteri

List sıralıdır ve aynı elemanı tekrar içerebilir. Bu nedenle görev kuyruğu veya "son 20 işlem" akışı için doğal bir tercihtir. `LPUSH` ile ekleyip `BRPOP` ile bekleyen tüketiciye iş dağıtabilirsiniz.

Set ise benzersiz üyelik sunar. Bir kullanıcının hangi etiketi takip ettiğini veya bir makaleyi beğenen benzersiz kullanıcıları saklamak için kullanılır. Kesişim işlemleri özellikle güçlüdür: iki kullanıcının ortak ilgi alanları `SINTER` ile bulunabilir.

| İhtiyaç | Tercih | Neden? |
|---|---|---|
| FIFO iş kuyruğu | List | Uçlardan hızlı ekleme ve çıkarma |
| Tekrarsız kullanıcı kimlikleri | Set | Benzersizlik otomatik korunur |
| En yüksek puanlı oyuncular | Sorted Set | Skora göre sıralı erişim |

Sorted Set, her üyeye sayısal bir skor bağlar. İç yapısındaki sıralama sayesinde liderlik tablosunda ilk 10 kişiyi almak verimlidir. Ekleme maliyeti $O(\log n)$ olsa da sıralamayı uygulama kodunda yeniden kurmaktan çok daha etkilidir.

```redis
ZADD leaderboard 980 "ayse" 1200 "mehmet" 1050 "deniz"
ZREVRANGE leaderboard 0 2 WITHSCORES
```

Son olarak, veri tipini yalnızca bugünkü ihtiyaca göre değil, sorgu desenine göre seçin. "Bu kaydı nasıl saklarım?" yerine "Bu veriyi en sık nasıl okuyacak, güncelleyecek ve sıralayacağım?" sorusunu sorun. Redis'te iyi modelleme, daha az komut, daha az ağ turu ve daha öngörülebilir gecikme demektir.

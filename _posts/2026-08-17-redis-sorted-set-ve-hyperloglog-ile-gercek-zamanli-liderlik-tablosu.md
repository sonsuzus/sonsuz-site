---
layout: post
title: "Redis Sorted Set ve HyperLogLog ile Gerçek Zamanlı Liderlik Tablosu"
math: true
categories: 
  - Bilgi
tags: 
  - redis
  - sorted set
  - hyperloglog
toc: true
---

Bir oyun uygulamasında en iyi oyuncuları saniyeler içinde sıralamak ya da bir kampanyayı kaç farklı kullanıcının gördüğünü hesaplamak, ilk bakışta basit görünür. Ancak trafik arttığında klasik SQL sorguları, sürekli güncellenen sayaçlar ve büyük `DISTINCT` işlemleri pahalılaşır. Redis; bellekte çalışan, düşük gecikmeli veri yapıları sayesinde bu iki problemi zarif biçimde çözer: lider tabloları için Sorted Set, yaklaşık tekil sayım için ise HyperLogLog.
``
## Neden iki farklı yapı?

Bu problemlerin ihtiyaçları farklıdır. Lider tablosunda her oyuncunun puanı saklanmalı, puan değiştiğinde sırası güncellenmeli ve en yüksek puanlılar okunmalıdır. Tekil ziyaretçi sayımında ise çoğu zaman kullanıcı listesinin kendisine değil, yalnızca kaç farklı kullanıcı olduğuna ihtiyacımız vardır. Redis veri yapısı seçimi, tam olarak hangi bilgiyi korumak istediğimize bağlıdır.

| İhtiyaç | Redis yapısı | Sonuç doğruluğu | Bellek yaklaşımı |
|---|---|---:|---|
| Oyuncuları puana göre sıralamak | Sorted Set (ZSET) | Kesin | Üye sayısıyla büyür |
| Farklı kullanıcı sayısını bulmak | HyperLogLog | Yaklaşık | Sabite yakın, yaklaşık 12 KB |
| Kullanıcıların kim olduğunu görmek | Set | Kesin | Her kullanıcı için ek alan |

## Sorted Set: Puan + sıralama ikilisi

Sorted Set içinde her üye benzersizdir ve her üyeye bir `score` atanır. Redis üyeleri puana göre sıralı tuttuğu için güncelleme ve sıralama işlemleri verimlidir. Bir oyuncunun puanını artırmak için `ZINCRBY`, en iyi oyuncuları almak için `ZREVRANGE` kullanılır.

Bir ZSET operasyonunun karmaşıklığı genel olarak $O(\log N)$ düzeyindedir. Buradaki $N$, lider tablosundaki oyuncu sayısıdır. En iyi $K$ oyuncuyu çekmek ise yaklaşık olarak $O(\log N + K)$ maliyetindedir. Bu nedenle milyonlarca üyede bile yalnızca ilk 10 kişiyi göstermek oldukça pratiktir.

```redis
ZINCRBY leaderboard:global 25 player:42
ZINCRBY leaderboard:global 10 player:7
ZREVRANGE leaderboard:global 0 9 WITHSCORES
ZREVRANK leaderboard:global player:42
```

İlk iki komut oyuncuların puanını artırır. `ZREVRANGE`, büyükten küçüğe ilk 10 oyuncuyu ve skorlarını döndürür. `ZREVRANK` ise oyuncunun sıfırdan başlayan sırasını verir. Ekranda insan dostu sıra göstermek için genellikle sonuca 1 eklenir.

Uygulama tarafında skor güncellemesini atomik tutmak önemlidir. Aynı anda gelen etkinliklerde önce puanı okuyup sonra yazmak yarış koşulu doğurabilir. `ZINCRBY` tek komut olduğu için bu riski doğal olarak azaltır. Sezon bazlı tablolar için `leaderboard:season:2026` gibi anahtarlar kullanmak, eski sezonları ayırmayı kolaylaştırır.

## HyperLogLog: Listeyi değil, kardinaliteyi saklamak

HyperLogLog, elemanların tamamını depolamadan farklı eleman sayısını tahmin eden olasılıksal bir yapıdır. Her kullanıcı kimliği, hash uzayında rastgele dağılmış kabul edilir. Algoritma hash değerlerindeki karakteristik bit desenlerinden kardinalite tahmini üretir.

Temel fikir kabaca şudur: Gözlenen nadirlik arttıkça evrende daha fazla farklı eleman bulunma olasılığı yükselir. Tahmin $\hat{N}$, gerçek sayı $N$ için küçük bir bağıl hata taşır:

$$\text{bağıl hata} = \frac{\vert \hat{N} - N\vert }{N}$$

Redis HyperLogLog için standart hata oranı yaklaşık %0,81'dir. Bu, analitik paneller ve erişim metrikleri için çoğu zaman mükemmel bir dengedir; fakat faturalandırma veya kesin ödül dağıtımı için uygun değildir.

```redis
PFADD visitors:2026-08-02 user:42 user:7 user:42
PFCOUNT visitors:2026-08-02
PFMERGE visitors:week32 visitors:2026-07-30 visitors:2026-07-31 visitors:2026-08-02
PFCOUNT visitors:week32
```

`PFADD` aynı kullanıcı tekrar gönderilse bile tekil sayımı hedefler. `PFCOUNT` tahmini farklı ziyaretçi sayısını verir. `PFMERGE` ise günlük kümeleri haftalık bir görünümde birleştirir; böylece aynı kullanıcı farklı günlerde gelmiş olsa da toplamda bir kez değerlendirilir.

## Doğru tasarım: kesinlik nerede gerekli?

Lider tablosunda kullanıcı kimliği, puanı ve sırası görünür olduğu için ZSET zorunlu olarak daha fazla bellek kullanır; karşılığında kesin sonuç sağlar. HyperLogLog ise kullanıcı listesini geri veremez. Bu nedenle ikisini aynı işe zorlamak yerine, onları birlikte kullanmak akıllıcadır: ZSET ile rekabet ekranını, HyperLogLog ile günlük aktif oyuncu metriğini yönetin. Redis burada yalnızca hızlı bir önbellek değil, probleme uygun veri yapısı seçildiğinde gerçek zamanlı ürün deneyiminin temel taşıdır.

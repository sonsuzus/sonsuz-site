---
layout: post
title: "Dağıtık Kilitler: Redis ve ZooKeeper ile Çakışmaları Yönetmek"
math: true
categories: 
  - Bilgi
tags: 
  - dağıtık-sistemler
  - redis
  - zookeeper
  - eşzamanlılık
  - distributed-lock
  - backend
toc: true
image: /img/dagitik-kilitler-redis-93.png
---

Bir e-ticaret sisteminde iki sunucunun aynı son ürünü eş zamanlı sattığını düşünün. Her ikisi de stok değerini 1 olarak okur, siparişi onaylar ve stoğu 0 yapar. Sonuç: Bir ürün, iki mutlu müşteri ve kısa süre sonra pek de mutlu olmayan bir destek ekibi! Dağıtık kilitler, farklı makinelerde çalışan süreçlerin ortak bir kaynağı kontrollü biçimde değiştirmesini sağlar.
``

## Neden normal kilit yetmez?

Tek uygulama sürecindeki `mutex` veya `synchronized`, yalnızca aynı belleği paylaşan iş parçacıklarını koordine eder. Uygulama üç sunucuda çalışıyorsa her sunucunun kendi kilidi vardır. Sunucu A'nın kilidi, Sunucu B için görünmezdir.

Dağıtık kilitte hedef, belirli anda yalnızca bir istemcinin kritik bölgeye girmesidir. İdeal olarak şu özellikler beklenir:

- **Karşılıklı dışlama:** Aynı kaynak için tek sahip bulunur.
- **Canlılık:** Kilit sahibi çökerse kaynak sonsuza kadar kilitli kalmaz.
- **Sahiplik doğrulaması:** Bir istemci başka istemcinin kilidini açamaz.
- **Hata toleransı:** Ağ veya düğüm arızaları sistemi tamamen durdurmaz.

Bir kritik işlemin süresi $T_i$, kilidin geçerlilik süresi de $T_k$ olsun. Güvenli çalışma için kabaca $T_i < T_k$ gerekir. Ancak ağ gecikmesi $L$ ve saat belirsizliği $D$ hesaba katıldığında daha gerçekçi koşul şudur:

$$T_i + L + D < T_k$$

Bu eşitsizlik sağlanmazsa işlem devam ederken kilidin süresi dolabilir ve ikinci bir istemci aynı kaynağa girebilir.

## Redis ile dağıtık kilit

Redis'te temel yöntem, anahtarı yalnızca mevcut değilse ve süre sonu vererek oluşturmaktır:

```text
SET lock:product:42 7f9a-client-token NX PX 10000
```

Burada `NX`, kilidin yalnızca anahtar yoksa alınmasını; `PX 10000` ise 10 saniye sonra otomatik silinmesini sağlar. Rastgele token, kilidin sahibini temsil eder. İş tamamlandığında anahtarı doğrudan `DEL` ile silmek tehlikelidir: Kilit süresi dolmuş ve başka istemci yeni kilit almış olabilir.

Kontrollü bırakma için atomik Lua betiği kullanılır:

```lua
if redis.call("GET", KEYS[1]) == ARGV[1] then
    return redis.call("DEL", KEYS[1])
end
return 0
```

Betik, saklanan token istemcinin token'ıyla eşleşiyorsa kilidi siler. Böylece gecikmiş bir süreç, yeni sahibin kilidini yanlışlıkla açamaz.

Tek Redis örneği hızlıdır fakat tek hata noktası oluşturabilir. Birincil düğüm kilit verisini replikaya aktarmadan çökerse yeni birincil aynı kilidi başka istemciye verebilir. Redlock algoritması birden fazla bağımsız Redis düğümünden çoğunluk onayı almayı önerir; yine de sıkı doğruluk gerektiren sistemlerde ağ bölünmeleri ve zaman varsayımları nedeniyle dikkatle değerlendirilmelidir.

## ZooKeeper yaklaşımı

ZooKeeper, koordinasyon için tasarlanmıştır. İstemci `/locks/product-42/lock-` altında **ephemeral sequential** bir znode oluşturur. ZooKeeper buna artan bir sıra numarası ekler. En küçük numaraya sahip istemci kilidi kazanır; diğerleri yalnızca kendilerinden önceki düğümü izler.

```text
/locks/product-42/lock-00000012
/locks/product-42/lock-00000013
/locks/product-42/lock-00000014
```

`12` sahibi çalışırken diğerleri bekler. Oturum kapanırsa ephemeral düğüm otomatik silinir ve `13` uyanır. Bu yapı adil sıralama sağlar ve bütün istemcilerin aynı düğümü izlemesinden kaynaklanan “sürü etkisini” azaltır.

| Özellik | Redis | ZooKeeper |
|---|---|---|
| Temel amaç | Hızlı veri deposu | Dağıtık koordinasyon |
| Kilit modeli | Süreli anahtar | Ephemeral sequential znode |
| Performans | Çok yüksek | Daha kontrollü, görece düşük |
| Adil sıralama | Varsayılan olarak yok | Doğal olarak var |
| Kurulum | Daha basit | Daha karmaşık |

## Kilit tek başına yeterli mi?

Eski kilit sahibinin duraklayıp süre dolduktan sonra işlemi sürdürmesi mümkündür. Bunu önlemek için her kilit alımında artan bir **fencing token** üretilir. Depolama katmanı yalnızca önceki değerden büyük token'ları kabul eder:

$$f_{yeni} > f_{son}$$

Böylece kilidi kaybetmiş eski istemcinin gecikmiş yazması reddedilir. Sonuç olarak Redis, kısa süreli ve performans odaklı işler için pratiktir; ZooKeeper ise güçlü koordinasyon ve sıralama gereken senaryolarda öne çıkar. Para, stok veya lider seçimi gibi kritik alanlarda kilitle birlikte fencing token, idempotency ve veritabanı kısıtları kullanmak en güvenli yaklaşımdır.

![dagitik-kilitler-redis-93](/img/dagitik-kilitler-redis-93.svg)


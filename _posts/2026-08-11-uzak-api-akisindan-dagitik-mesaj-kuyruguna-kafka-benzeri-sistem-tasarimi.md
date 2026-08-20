---
layout: post
title: "Uzak API Akışından Dağıtık Mesaj Kuyruğuna: Kafka Benzeri Sistem Tasarımı"
math: true
categories: 
  - Proje
tags: 
  - sistem tasarımı
  - kafka
  - dağıtık sistemler
image: /img/uzak-api-akisindan-71.png
---

![uzak-api-akisindan-71](/img/uzak-api-akisindan-71.svg)


Uzak bir API’den durmaksızın veri çekmek, ilk bakışta basit bir `while` döngüsü gibi görünür. Ancak ağ gecikmeleri, API kota sınırları, yinelenen kayıtlar, çöken düğümler ve tüketicilerin farklı hızları devreye girince bu iş küçük bir dağıtık sistem macerasına dönüşür. Amaç; veriyi kaybetmeden almak, sıralı şekilde saklamak, birden çok tüketiciye dağıtmak ve tek bir makinenin arızasında sistemi ayakta tutmaktır.

``

Bu tasarımın temelinde **append-only log** fikri bulunur. Üretici, her mesajı değiştirilemeyen bir günlüğün sonuna ekler. Mesajın konumu `offset` ile tanımlanır. Tüketici ise mesaj silinmiş gibi davranmak yerine, kendi okuma konumunu ilerletir. Böylece aynı olay; analiz, bildirim ve arşiv servisleri tarafından bağımsız biçimde okunabilir.

Bir topic, ölçeklenmek için partition’lara ayrılır. Aynı anahtara sahip olayları aynı partition’a göndermek, örneğin bir kullanıcının işlemlerindeki sırayı korur. Basit bir yönlendirme fonksiyonu şöyledir:

$$p = hash(key) \bmod N$$

Burada $N$ partition sayısıdır. Kritik ayrıntı şudur: `N` değişirse anahtarların dağılımı da değişebilir. Bu nedenle partition artırma kararını kapasite planıyla birlikte vermek gerekir.

| Kavram | Görevi | Sağladığı garanti |
|---|---|---|
| Topic | Mantıksal mesaj kanalı | Olayların sınıflandırılması |
| Partition | Sıralı fiziksel günlük parçası | Partition içinde sıra |
| Offset | Mesaj konumu | Yeniden okuma ve takip |
| Consumer group | Tüketici kümesi | Yatay paralellik |
| Replica | Kopya düğüm | Düğüm arızasına tolerans |

## Uzak API alıcısı: nazik ama inatçı üretici

API alıcısı bir `poller` veya destekleniyorsa webhook istemcisi olarak çalışır. Her başarılı sayfalamadan sonra son görülen `cursor`, zaman damgası ya da olay kimliği kalıcı depoya yazılır. Böylece süreç yeniden başladığında baştan değil, kaldığı yerden devam eder. Ağ hatalarında üstel geri çekilme kullanılır:

$$delay_k = min(delay_{max}, delay_0 \times 2^k) + jitter$$

`jitter`, yüzlerce istemcinin aynı saniyede API’ye tekrar saldırmasını engeller. Ayrıca API’nin aynı olayı tekrar göndermesi normal kabul edilmelidir. Bu yüzden her mesaja kaynak sistemden gelen benzersiz `eventId` eklenir.

```python
async def ingest(api, producer, checkpoint):
    cursor = checkpoint.load() or "0"
    async for page in api.stream(cursor):
        for event in page.events:
            await producer.send(
                topic="remote-events",
                key=event.customer_id,
                value={"eventId": event.id, "payload": event.data}
            )
        await producer.flush()  # Kalıcı yazım onayı beklenir
        cursor = page.next_cursor
        checkpoint.save(cursor)
```

Bu kodun önemli noktası sıralamadır: önce mesajlar kuyruğa dayanıklı biçimde yazılır, ardından checkpoint güncellenir. Tersi yapılırsa çökme anında olaylar atlanabilir. Buna rağmen yeniden denemeler nedeniyle **at-least-once** teslimat oluşabilir; tüketici tarafında `eventId` ile idempotent yazım yapılmalıdır.

## Dayanıklılık ve çoğaltma

Her partition için bir lider ve takipçi replikalar seçilir. Üretici lider düğüme yazar; lider mesajı yeterli sayıda takipçiye ulaştırdığında onay döner. Çoğaltma faktörü $R=3$ ve en az eşzamanlı kopya sayısı `min.insync.replicas=2` seçilirse, tek düğüm kaybında yazma güvenliği korunur.

| Teslimat modeli | Avantaj | Bedel |
|---|---|---|
| At-most-once | Hızlı, tekrar yok | Mesaj kaybı mümkün |
| At-least-once | Kayıp riski düşük | Tekrar işleme mümkün |
| Exactly-once | En güçlü semantik | İşlemsel altyapı ve maliyet |

Pratikte en iyi başlangıç noktası, kuyrukta **at-least-once**, iş kurallarında ise idempotency kullanmaktır. Tüketici yalnızca iş sonucunu kalıcılaştırdıktan sonra offset onaylamalıdır. Örneğin veritabanında `eventId` için benzersiz indeks, aynı olay ikinci kez gelse bile ikinci yazımı etkisiz bırakır.

Son olarak sistem gözlemlenebilir olmalıdır: API gecikmesi, üretim hızı, partition başına gecikme, tüketici lag’i, yeniden deneme sayısı ve replikasyon geriliği metrik olarak izlenmelidir. Lag büyüyorsa daha fazla tüketici eklemek çözüm olabilir; fakat tüketici sayısı partition sayısını aşarsa yeni tüketiciler boşta kalır. Dağıtık kuyruk tasarımında sihir yoktur: doğru sıralama, kalıcı durum, kontrollü tekrar ve görünür metrikler vardır.

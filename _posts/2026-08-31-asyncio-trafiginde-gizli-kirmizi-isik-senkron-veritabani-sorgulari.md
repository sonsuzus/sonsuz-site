---
layout: post
title: "Asyncio Trafiğinde Gizli Kırmızı Işık: Senkron Veritabanı Sorguları"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - asyncio
  - veritabanı
toc: true
---

Asenkron bir bot geliştirirken yüzlerce mesajı aynı anda işleyebildiğinizi düşünüyor olabilirsiniz. Fakat olay döngüsünün ortasına yerleştirilen tek bir senkron veritabanı sorgusu, çok şeritli görünen bu yolu bir anda bariyerle kapatabilir. Bot çevrim içidir, işlemci çoğunlukla boştadır, hata mesajı da yoktur; buna rağmen komutlar cevap bekler. Suçlu genellikle olay döngüsünü fark ettirmeden bloke eden I/O işlemidir.
``

## Olay döngüsü gerçekte nasıl çalışır?

`asyncio`, her görevi ayrı bir işletim sistemi iş parçacığında çalıştırmaz. Varsayılan modelde tek bir iş parçacığında bulunan **event loop**, coroutine'leri sırayla ilerletir. Bir coroutine `await` ile kontrolü bıraktığında döngü başka bir hazır göreve geçebilir.

Kooperatif zamanlamanın temel fikri şöyledir:

$$T_{toplam} \approx \max(T_1, T_2, \ldots, T_n)$$

Bu yaklaşım yalnızca görevler bekleme anlarında kontrolü döngüye geri veriyorsa geçerlidir. Senkron bir sorgu çalıştırıldığında ise ilgili fonksiyon tamamlanana kadar Python kodu ilerleyemez. Böylece gecikme yaklaşık olarak şu hale gelir:

$$T_{gecikme} = T_{bloklayan\ sorgu} + T_{kuyrukta\ bekleme}$$

Örneğin sorgu beş saniye sürerse mesaj dinleyicisi, zamanlayıcılar, bağlantı kalp atışları ve diğer komutlar da beş saniye boyunca bekleyebilir.

| Yaklaşım | Event loop bloke olur mu? | Eşzamanlılık davranışı | Uygun kullanım |
|---|---:|---|---|
| Senkron sürücü | Evet | Tüm görevleri bekletir | Klasik senkron uygulamalar |
| `asyncio.to_thread` | Hayır | İş ayrı thread'de bekler | Eski sürücüyü geçici uyarlama |
| Asenkron sürücü | Hayır | I/O sırasında kontrol bırakılır | Üretim tipi async sistemler |

## Sorunun küçük ama tehlikeli hali

Aşağıdaki komut, `sqlite3` senkron olduğu için sorgu tamamlanana kadar olay döngüsünü elinde tutar:

```python
import sqlite3

async def kullanici_getir(user_id: int):
    connection = sqlite3.connect("bot.db")
    cursor = connection.execute(
        "SELECT name FROM users WHERE id = ?", (user_id,)
    )
    row = cursor.fetchone()  # Event loop burada bloke olabilir
    connection.close()
    return row
```

Fonksiyonun `async def` ile tanımlanması içindeki işlemleri sihirli biçimde asenkron yapmaz. Bir fonksiyon, ancak kullandığı I/O aracı kontrolü gerçekten bırakıyorsa asenkron davranır. Üstelik `await kullanici_getir(...)` yazmak da çözüm değildir; `await`, senkron sorgunun içine müdahale edemez.

## Geçiş çözümü: sorguyu thread'e taşıma

Mevcut senkron sürücüyü hemen değiştiremiyorsanız bloklayan işi `asyncio.to_thread` ile olay döngüsünün dışına taşıyabilirsiniz:

```python
import asyncio
import sqlite3

def senkron_sorgu(user_id: int):
    with sqlite3.connect("bot.db") as connection:
        return connection.execute(
            "SELECT name FROM users WHERE id = ?", (user_id,)
        ).fetchone()

async def kullanici_getir(user_id: int):
    return await asyncio.to_thread(senkron_sorgu, user_id)
```

Burada event loop, thread sorguyu beklerken diğer bot görevlerini çalıştırabilir. Ancak sınırsız sayıda thread başlatmak yeni bir darboğaz yaratabilir. Bağlantı paylaşımı, thread güvenliği ve bağlantı havuzu sınırları ayrıca değerlendirilmelidir.

## Kalıcı çözüm: asenkron sürücü

PostgreSQL için `asyncpg`, SQLite için `aiosqlite`, SQLAlchemy için async engine kullanılabilir:

```python
import aiosqlite

async def kullanici_getir(user_id: int):
    async with aiosqlite.connect("bot.db") as database:
        async with database.execute(
            "SELECT name FROM users WHERE id = ?", (user_id,)
        ) as cursor:
            return await cursor.fetchone()
```

Asenkron sürücü tek başına hızlı sorgu garantisi vermez; sadece bekleme sırasında sistemi kullanılabilir tutar. İndeksler, sorgu planları, zaman aşımı ve havuz boyutu yine önemlidir.

Bloklamayı yakalamak için event loop debug modu, yavaş callback uyarıları ve sorgu süreleri izlenmelidir. Basit bir kalp atışı görevi de gecikmeleri görünür kılar. Sonuç olarak temel kural nettir: Event loop üzerinde uzun süren senkron I/O çalıştırmayın. Ya işlemi kontrollü biçimde thread'e aktarın ya da uçtan uca asenkron bir veritabanı katmanı kurun.

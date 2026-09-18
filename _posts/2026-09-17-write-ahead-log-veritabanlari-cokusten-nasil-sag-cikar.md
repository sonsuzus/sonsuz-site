---
layout: post
title: "Write-Ahead Log: Veritabanları Çöküşten Nasıl Sağ Çıkar?"
math: true
categories: 
  - Bilgi
tags: 
  - veritabanı
  - wal
  - write-ahead-log
  - transaction
  - recovery
  - acid
toc: true
image: /img/write-ahead-log-91.png
---

Bir veritabanı sunucusu tam sipariş kaydedilirken kapanırsa ne olur? Para hesaptan düşmüş, fakat sipariş oluşmamış olabilir mi? Modern veritabanları bu korku filmini **Write-Ahead Log (WAL)** sayesinde mutlu sonla bitirir. WAL, değişiklikleri asıl veri dosyasına uygulamadan önce dayanıklı bir günlükte kaydederek sistemin çöküş sonrasında ne yaptığını hatırlamasını sağlar.

![write-ahead-log-91](/img/write-ahead-log-91.svg)

``
## Önce günlük, sonra veri

WAL'ın temel kuralı şaşırtıcı derecede basittir:

> Bir değişiklik veri sayfasına yazılmadan önce, o değişikliğin günlük kaydı kalıcı depolamaya yazılmalıdır.

Bir transaction, $T_i$, verinin eski değerini $V_{eski}$ değerinden $V_{yeni}$ değerine getiriyorsa günlük kaydı kavramsal olarak şöyle düşünülebilir:

$$
L_i = (T_i, adres, V_{eski}, V_{yeni})
$$

Buradaki eski değer gerektiğinde işlemi geri almak, yeni değer ise tamamlanmış işlemi yeniden uygulamak için kullanılabilir. Her günlük kaydına genellikle artan bir **Log Sequence Number (LSN)** verilir. Böylece veritabanı olayların sırasını bilir; dijital dedektiflik yaparken ayak izleri birbirine karışmaz.

| Yaklaşım | Yazma sırası | Çöküşte sonuç |
|---|---|---|
| WAL yok | Veri doğrudan değiştirilir | Yarım ve belirsiz güncellemeler oluşabilir |
| WAL var | Önce log, sonra veri | REDO ve UNDO ile tutarlılık kurulabilir |
| Yalnızca yedek | Belirli aralıklarla kopya alınır | Son yedekten sonraki işlemler kaybolabilir |

## COMMIT gerçekten ne demektir?

Bir uygulamanın `COMMIT` yanıtını alması, ilgili transaction'ın log kayıtlarının ve commit kaydının kalıcı ortama ulaştığı anlamına gelmelidir. Veri sayfasının aynı anda diske yazılması zorunlu değildir. Bu modele **no-force** denir ve performansı artırır; kirli sayfalar daha sonra topluca yazılabilir.

Bazı sistemler ayrıca **steal** politikasını kullanır: Henüz commit edilmemiş bir transaction'ın değiştirdiği sayfa diske gönderilebilir. Bu durumda toparlanma sırasında hem REDO hem UNDO gerekir.

| Transaction durumu | Kurtarma işlemi | Amaç |
|---|---|---|
| Commit edilmiş | REDO | Kalıcı olması gereken değişikliği yeniden uygula |
| Commit edilmemiş | UNDO | Yarım kalmış değişikliği geri al |
| Hiç başlamamış | İşlem yok | Günlükte etkisi bulunmaz |

## Çöküş sonrası üç aşama

ARIES gibi gelişmiş kurtarma algoritmaları genel olarak üç aşamalı düşünülür:

1. **Analiz:** Son checkpoint'ten itibaren log taranır; aktif transaction'lar ve kirli sayfalar belirlenir.
2. **REDO:** Gerekli günlük kayıtları ileri yönde uygulanır. İşlem mümkün olduğunca idempotent olmalıdır; aynı kayıt ikinci kez işlense bile sonuç değişmemelidir.
3. **UNDO:** Commit kaydı bulunmayan transaction'lar ters sırada geri alınır.

Checkpoint, bütün verileri anında diske zorlamak zorunda değildir. Asıl görevi toparlanmanın nereden başlayabileceğine ilişkin güvenilir bir işaret bırakmaktır. Böylece sistem yılların günlüğünü baştan okumaz.

## Küçük bir kurtarma simülasyonu

Aşağıdaki Python kodu, günlük kayıtlarından commit edilmiş işlemleri yeniden uygular. Gerçek sistemlerde sayfa LSN'leri, checksum'lar ve eşzamanlılık denetimi de bulunur.

```python
log = [
    {'tx': 1, 'key': 'bakiye', 'new': 900, 'type': 'update'},
    {'tx': 1, 'type': 'commit'},
    {'tx': 2, 'key': 'stok', 'new': 4, 'type': 'update'}
]

def recover(records, database):
    committed = {
        item['tx'] for item in records
        if item['type'] == 'commit'
    }

    for item in records:
        if item['type'] == 'update' and item['tx'] in committed:
            database[item['key']] = item['new']

    return database

print(recover(log, {'bakiye': 1000, 'stok': 5}))
```

Burada transaction 1 commit edildiği için bakiye yeniden uygulanır. Transaction 2'nin commit kaydı yoktur; stok güncellemesi yok sayılır. Gerçek bir UNDO mekanizması, değişiklik veri dosyasına önceden sızmışsa eski değeri kullanarak onu geri çevirir.

## WAL yedek değildir

WAL dayanıklılık sağlar, fakat disk tamamen kaybolursa tek başına yeterli olmayabilir. Sağlam strateji; **tam yedek + arşivlenmiş WAL + düzenli geri yükleme testi** birleşimidir. PostgreSQL'deki point-in-time recovery gibi yöntemler, bir yedeği açıp WAL kayıtlarını hedef zamana kadar oynatarak veritabanını belirli bir ana döndürebilir.

Kısacası WAL, veritabanının kara kutusudur: Çöküşü engellemez, ancak sistem uyandığında hangi işlemlerin tamamlandığını ve hangilerinin geri alınması gerektiğini anlatır.

---
layout: post
title: "SQLite WAL Modu: Yazarken Okumaya Devam Etmenin Sırrı"
math: true
categories: 
  - Bilgi
tags: 
  - sqlite
  - wal
  - veritabanı
  - eşzamanlılık
  - sql
  - performans
toc: true
image: /img/sqlite-wal-modu-29.png
---

![sqlite-wal-modu-29](/img/sqlite-wal-modu-29.svg)


SQLite küçük görünür ama tarayıcılardan mobil uygulamalara kadar milyarlarca cihazda çalışan ciddi bir veritabanıdır. Geleneksel günlükleme yönteminde bir yazma işlemi okuyucuları kısa süreliğine bekletebilir. WAL, yani Write-Ahead Logging modu ise değişiklikleri ana veritabanı dosyasına hemen yazmak yerine ayrı bir günlüğe ekleyerek okuyucuların tutarlı bir eski sürümü görmeye devam etmesini sağlar.

``

## Geleneksel günlükleme nasıl çalışır?

SQLite'ın varsayılan rollback journal yaklaşımında değiştirilecek sayfaların eski hâlleri bir günlük dosyasına kopyalanır. Ardından ana veritabanı güncellenir. İşlem başarısız olursa günlükteki sayfalar geri yüklenir.

Bu mekanizma güvenlidir; fakat yazıcının ana dosyayı değiştirdiği kritik aşamada okuyucularla kilit çatışmaları oluşabilir. Basitleştirilmiş bekleme süresini şöyle düşünebiliriz:

$$
T_{toplam} = T_{kilit} + T_{okuma} + T_{işleme}
$$

WAL modunun amacı özellikle $T_{kilit}$ bileşenini okuyucular açısından büyük ölçüde azaltmaktır.

## WAL'ın temel mantığı

WAL etkin olduğunda değiştirilen veritabanı sayfaları doğrudan ana dosyanın üzerine yazılmaz. Bunun yerine `veritabani.db-wal` dosyasının sonuna eklenir. Bir işlem `COMMIT` yaptığında günlüğe özel bir commit kaydı bırakılır.

Okuyucu sorguya başladığı anda WAL içerisindeki belirli bir noktayı kendi **end mark** değeri olarak kabul eder. Daha sonra gelen değişiklikleri görmez. İhtiyaç duyduğu sayfanın güncel sürümü bu sınırdan önce WAL'da bulunuyorsa onu, bulunmuyorsa ana veritabanındaki sürümü okur. Böylece snapshot benzeri tutarlı bir görünüm elde edilir.

| Özellik | Rollback journal | WAL |
|---|---|---|
| Yazma sırasında okuma | Kilit nedeniyle bekleyebilir | Genellikle devam eder |
| Aynı anda yazıcı sayısı | Bir | Bir |
| Değişikliklerin konumu | Ana dosya | Önce WAL dosyası |
| Geri alma yaklaşımı | Eski sayfaları saklar | Yeni sayfaları ekler |
| Ağ dosya sistemi uyumu | Daha elverişli | Genellikle önerilmez |

Buradaki önemli ayrıntı şudur: WAL, SQLite'ı çok yazıcılı bir veritabanına dönüştürmez. Aynı anda yalnızca **bir yazıcı** bulunabilir; kazanç, yazıcının okuyucuları engellememesidir.

## WAL modu nasıl etkinleştirilir?

Aşağıdaki SQL komutu günlükleme modunu değiştirir ve oluşan sonucu döndürür:

```sql
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 5000;
```

`busy_timeout`, başka bir yazıcı kilidi tuttuğunda bağlantının hemen hata vermek yerine belirtilen milisaniye kadar beklemesini sağlar. Python ile kullanım da oldukça sadedir:

```python
import sqlite3

connection = sqlite3.connect('uygulama.db', timeout=5)
connection.execute('PRAGMA journal_mode=WAL')
connection.execute('PRAGMA synchronous=NORMAL')
connection.execute('INSERT INTO olaylar(mesaj) VALUES (?)', ('WAL aktif!',))
connection.commit()
```

Burada `synchronous=NORMAL`, çoğu uygulamada dayanıklılık ile hız arasında iyi bir denge kurar. Elektrik kesintilerine karşı mümkün olan en katı garantiler gerekiyorsa `FULL` seçeneği değerlendirilmelidir.

## Checkpoint neden gereklidir?

WAL sonsuza kadar büyüyemez. **Checkpoint**, günlüğe eklenen tamamlanmış sayfaları uygun zamanda ana veritabanına aktarır. Yaklaşık maliyet, taşınan sayfa sayısı $N$ ve sayfa boyutu $P$ ile ilişkilidir:

$$
M_{checkpoint} \approx N \times P
$$

SQLite varsayılan olarak WAL belirli sayıda sayfaya ulaştığında otomatik checkpoint çalıştırır. Manuel kontrol için şu komut kullanılabilir:

```sql
PRAGMA wal_checkpoint(TRUNCATE);
```

`TRUNCATE`, aktarım mümkünse WAL dosyasını sıfır boyutuna indirir. Ancak uzun süren bir okuyucu eski snapshot'ı kullanıyorsa checkpoint onun ihtiyaç duyduğu kayıtların ötesine geçemez. Sonuç olarak WAL dosyası büyüyebilir.

## Ne zaman tercih edilmeli?

WAL; web servisleri, masaüstü programları, mobil uygulamalar ve arka planda veri yazılırken arayüzün sorgu çalıştırdığı sistemler için güçlü bir seçenektir. Buna karşılık veritabanı ağ paylaşımındaysa, çok sayıda eşzamanlı yazıcı gerekiyorsa veya uzun okuma işlemleri kontrol edilemiyorsa istemci-sunucu veritabanı daha uygun olabilir.

Kısacası WAL bir sihir değil, akıllıca düzenlenmiş bir zaman çizelgesidir: yazıcı geleceği günlüğe eklerken okuyucular güvenli bir geçmiş fotoğrafına bakar. Doğru checkpoint ve kısa işlemlerle SQLite, boyundan beklenmeyecek kadar akıcı bir eşzamanlılık sunar.

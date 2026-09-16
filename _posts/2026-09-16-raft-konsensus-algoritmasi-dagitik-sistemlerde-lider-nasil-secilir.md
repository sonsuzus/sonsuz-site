---
layout: post
title: "Raft Konsensüs Algoritması: Dağıtık Sistemlerde Lider Nasıl Seçilir?"
math: true
categories: 
  - Bilgi
tags: 
  - raft
  - dağıtık sistemler
  - konsensüs
  - lider seçimi
  - replikasyon
  - algoritma
toc: true
---

Bir dağıtık sistemde sunucuların aynı karar üzerinde anlaşmasını sağlamak, kalabalık bir arkadaş grubuyla nerede yemek yeneceğine karar vermeye benzer: herkes konuşursa gürültü çıkar, kimse konuşmazsa aç kalınır. Raft konsensüs algoritması bu sorunu anlaşılır bir liderlik modeliyle çözer. Sunuculardan biri lider olur, diğerleri onu takip eder ve lider ortadan kaybolursa sistem demokratik sayılabilecek yeni bir seçim başlatır.

``

## Raft neden gereklidir?

Dağıtık sistemlerde makineler bozulabilir, ağ paketleri gecikebilir veya sunucular birbirleriyle geçici olarak iletişim kuramayabilir. Buna rağmen sistemin tutarlı davranması gerekir. Örneğin bir banka bakiyesine yapılan işlemlerin farklı sunucularda farklı sırayla uygulanması kabul edilemez.

Raft, **çoğaltılmış durum makinelerinin** aynı komut günlüğünü paylaşmasını sağlar. Temel fikir, istemci komutlarının önce liderin günlüğüne yazılması, ardından diğer sunuculara kopyalanmasıdır. Bir kayıt çoğunluk tarafından kabul edildiğinde kalıcı, yani `committed`, sayılır.

Toplam sunucu sayısı $N$ ise karar için gereken çoğunluk:

$$
Q = \left\lfloor \frac{N}{2} \right\rfloor + 1
$$

Örneğin beş sunuculu bir kümede üç onay yeterlidir. Böylece sistem iki sunucu kaybetse bile çalışmayı sürdürebilir.

## Üç temel rol

Her Raft düğümü aynı anda yalnızca bir rolde bulunur:

| Rol | Temel görevi | Davranışı |
|---|---|---|
| Lider | Komutları yönetmek | Günlük kayıtlarını takipçilere yollar |
| Takipçi | Lideri dinlemek | İsteklere ve kalp atışlarına yanıt verir |
| Aday | Seçim kazanmak | Diğer düğümlerden oy ister |

Sistem normal çalışırken bir lider ve birden fazla takipçi vardır. Lider, düzenli aralıklarla boş `AppendEntries` mesajları gönderir. Kalp atışı adı verilen bu mesajlar, takipçilere liderin hâlâ hayatta olduğunu bildirir.

## Liderlik seçimi nasıl başlar?

Bir takipçi belirli süre boyunca kalp atışı alamazsa seçim zaman aşımı gerçekleşir. Düğüm aday rolüne geçer, mevcut **term** değerini artırır, kendine oy verir ve diğer düğümlere `RequestVote` mesajı yollar.

Term, Raft dünyasındaki mantıksal dönem numarasıdır. Her yeni seçim yeni bir term açar. Daha yüksek term gören bir düğüm, eski bilgisini bırakıp takipçiye dönüşür. Bu mekanizma bayat liderlerin sistemi yönetmesini engeller.

Seçim süreci şöyledir:

1. Aday kendi term değerini artırır.
2. Önce kendisine oy verir.
3. Kümedeki diğer düğümlerden oy ister.
4. Çoğunluğu elde ederse lider olur.
5. Hemen kalp atışı göndererek otoritesini duyurur.

Takipçiler aynı term içinde yalnızca bir adaya oy verebilir. Ayrıca adayın günlüğü, oy veren düğümün günlüğü kadar güncel olmalıdır. Böylece eksik kayıtlara sahip bir sunucunun lider seçilmesi zorlaşır.

## Neden rastgele zaman aşımı kullanılır?

Tüm takipçiler aynı anda aday olursa oylar bölünebilir. Raft bunu önlemek için seçim zaman aşımını rastgele seçer:

```python
import random

# Her düğüm farklı bir bekleme süresi seçerek
# aynı anda başlayan seçimlerin olasılığını azaltır.
election_timeout_ms = random.randint(150, 300)

if heartbeat_wait_ms > election_timeout_ms:
    role = "candidate"
    current_term += 1
    voted_for = node_id
```

Bu örnekte kalp atışı bekleme süresi eşiği aşarsa düğüm aday olur. Aralıkların farklı seçilmesi, genellikle tek bir adayın diğerlerinden önce davranıp çoğunluğu toplamasını sağlar.

| Sabit zaman aşımı | Rastgele zaman aşımı |
|---|---|
| Eş zamanlı adaylık sıklaşabilir | Oy bölünmesi olasılığı azalır |
| Yeni seçimler tekrarlanabilir | Lider daha hızlı belirlenir |
| Uygulaması basittir | Biraz daha fazla durum yönetimi ister |

## Ağ bölünürse ne olur?

Ağ iki parçaya ayrıldığında yalnızca çoğunluğa ulaşabilen taraf yeni lider seçebilir. Eski lider azınlık tarafında kalırsa komutları kalıcı hâle getiremez. Bağlantı düzeldiğinde daha yüksek term değerini görür, takipçiye dönüşür ve günlüğünü geçerli liderle eşitler.

Raft’ın gücü yalnızca lider seçmesinde değil, seçimi günlük tutarlılığıyla birleştirmesindedir. Çoğunluk kuralı, term numaraları ve rastgele zaman aşımı birlikte çalışarak sistemin tek bir karar çizgisinde ilerlemesini sağlar. Kısacası Raft, dağıtık sistemlerin kaotik toplantısını gündemi belli, oylaması düzenli ve gerektiğinde başkanı değişebilen bir kurula dönüştürür.

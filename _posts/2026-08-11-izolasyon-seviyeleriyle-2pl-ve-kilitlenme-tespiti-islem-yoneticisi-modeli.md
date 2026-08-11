---
layout: post
title: "İzolasyon Seviyeleriyle 2PL ve Kilitlenme Tespiti: İşlem Yöneticisi Modeli"
math: true
categories: 
  - Program
tags: 
  - veritabanı
  - transaction
  - 2PL
  - deadlock
  - izolasyon
---

Bir veritabanı işlem yöneticisi, aynı anda gelen yüzlerce isteğin veriyi birbirinin ayağına basmadan değiştirmesini sağlar. Bu yöneticinin temel görevi, işlemlere doğru izolasyon garantisini vermek, kilitleri düzenlemek ve iki işlem birbirini sonsuza dek beklediğinde alarmı çalmaktır. Bu yazıda, farklı izolasyon seviyelerini destekleyen; iki fazlı kilitleme (2PL) kullanan ve kilitlenmeleri tespit eden bir model kuracağız.

``

Bir işlemi $T_i$, veri öğesini ise $X$ ile gösterelim. Bir işlem okumadan önce paylaşılmış kilit ($S$), yazmadan önce münhasır kilit ($X$) ister. Aynı veri üzerinde iki $S$ kilidi uyumludur; fakat bir $X$ kilidi, diğer tüm okuma ve yazma kilitleriyle çatışır. Bu basit kural, eşzamanlılığın temel trafik lambasıdır.

| İstenen / Mevcut kilit | S | X |
|---|---:|---:|
| **S** | Uyumlu | Çatışır |
| **X** | Çatışır | Çatışır |

İzolasyon seviyesi, yöneticinin kilitleri ne kadar süre tuttuğunu ve hangi anomalilere izin verdiğini belirler. `READ UNCOMMITTED`, pratikte okuma kilidi almadan kirli okumaya izin verebilir. `READ COMMITTED`, okuma kilitlerini ifade sonunda bırakırken yazma kilitlerini işlem sonuna kadar korur. `REPEATABLE READ` ise okunan satırlardaki $S$ kilitlerini de işlem bitene kadar tutar. Tam seri hale getirilebilirlik için aralık veya predicate kilitleri gerekir; aksi halde hayalet kayıtlar aradan sıyrılabilir.

| Seviye | Kirli okuma | Tekrarlanamayan okuma | Hayalet kayıt |
|---|---|---|---|
| Read Uncommitted | Mümkün | Mümkün | Mümkün |
| Read Committed | Engellenir | Mümkün | Mümkün |
| Repeatable Read | Engellenir | Engellenir | Mümkün olabilir |
| Serializable | Engellenir | Engellenir | Engellenir |

İki fazlı kilitlemede işlem önce **büyüme fazında** kilit edinir, ardından **küçülme fazında** kilit bırakır. Kilit bıraktıktan sonra yeni kilit istemesi yasaktır. Sıkı 2PL (Strict 2PL) modelinde özellikle $X$ kilitleri `COMMIT` veya `ROLLBACK` anına kadar bırakılmaz. Böylece geri alınmış bir işlemin geçici verisini başka işlemlerin görmesi engellenir ve kurtarma süreci sadeleşir.

Aşağıdaki Python benzeri iskelet, kilit tablosu ve bekleme grafiğini birlikte tutar. Gerçek bir sistemde kuyruk adaleti, zaman aşımı ve satır/aralık ayrımı da eklenmelidir.

```python
from collections import defaultdict

class LockManager:
    def __init__(self):
        self.holders = defaultdict(list)      # veri -> [(tx, kip)]
        self.waits_for = defaultdict(set)     # bekleyen tx -> engelleyen tx'ler

    def compatible(self, requested, current):
        return requested == "S" and current == "S"

    def acquire(self, tx, item, mode):
        blockers = [owner for owner, held in self.holders[item]
                    if owner != tx and not self.compatible(mode, held)]
        if blockers:
            self.waits_for[tx].update(blockers)
            if self.has_cycle(tx, tx, set()):
                raise RuntimeError(f"Deadlock: kurban seç -> {tx}")
            return False
        self.holders[item].append((tx, mode))
        return True

    def has_cycle(self, start, node, seen):
        if node in seen:
            return node == start
        seen.add(node)
        return any(self.has_cycle(start, nxt, seen.copy())
                   for nxt in self.waits_for[node])
```

Kilitlenme, örneğin $T_1$'in `A`yı tutup `B`yi beklemesi; $T_2$'nin de `B`yi tutup `A`yı beklemesiyle oluşur. Bekleme grafiğinde $T_1 \rightarrow T_2 \rightarrow T_1$ çevrimi görülür. Çevrim varsa yönetici bir kurban işlem seçer, onu `ROLLBACK` eder, kilitlerini serbest bırakır ve bekleyen işlemleri uyandırır. Kurban seçiminde en genç işlem, en az değişiklik yapan işlem veya yeniden çalıştırma maliyeti düşük işlem tercih edilebilir.

Modelin kritik ayrıntısı, izolasyon politikasını kilit yöneticisinden ayırmaktır. İşlem yöneticisi, seçilen seviyeye göre hangi kilidin isteneceğini ve ne zaman bırakılacağını belirler; kilit yöneticisi ise yalnızca uyumluluk, kuyruk ve çevrim tespitiyle ilgilenir. Bu ayrım, yarın MVCC gibi farklı bir eşzamanlılık stratejisine geçmek istediğinizde tasarımın tamamını söküp takmanızı önler.

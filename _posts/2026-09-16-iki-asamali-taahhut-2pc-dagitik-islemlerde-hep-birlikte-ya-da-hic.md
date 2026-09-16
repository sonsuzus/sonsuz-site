---
layout: post
title: "İki Aşamalı Taahhüt (2PC): Dağıtık İşlemlerde Hep Birlikte, Ya Da Hiç"
math: true
categories: 
  - Bilgi
tags: 
  - 2pc
  - dağıtık-sistemler
  - veritabanı
  - tutarlılık
  - transaction
  - mikroservis
toc: true
---

Bir para transferinin iki farklı veritabanına dokunduğunu düşünün: İlk sistem bakiyeyi azaltırken ikinci sistem alıcının hesabını artırıyor. Sistemlerden biri işlemi tamamlayıp diğeri çökerse para dijital boşlukta kaybolabilir! İki Aşamalı Taahhüt, yani Two-Phase Commit (2PC), dağıtık bir işlemin tüm katılımcılarda birlikte onaylanmasını veya tamamen geri alınmasını sağlayarak bu tehlikeyi azaltan klasik bir koordinasyon protokolüdür.

``

## Temel problem: Dağıtık atomiklik

Tek bir veritabanındaki işlem, çoğunlukla ACID özellikleriyle korunur. Dağıtık bir işlemde ise farklı makineler, veritabanları veya servisler aynı mantıksal sonucun parçalarını yürütür. Ağ gecikmeleri, süreç çökmeleri ve mesaj kayıpları nedeniyle herkesin aynı kararı verdiğinden emin olmak zorlaşır.

Katılımcı kümesini $P = \{p_1, p_2, \ldots, p_n\}$ olarak tanımlayalım. 2PC'nin hedeflediği atomiklik kuralı şöyledir:

$$
Commit(T) \iff \bigwedge_{i=1}^{n} Prepared(p_i, T)
$$

Yani $T$ işlemi ancak bütün katılımcılar hazırlanabildiyse tamamlanabilir. Tek bir katılımcının bile olumsuz cevap vermesi küresel geri alma kararı için yeterlidir.

## Oyuncular kimler?

2PC iki role dayanır:

- **Koordinatör:** Süreci başlatır, oyları toplar ve nihai kararı duyurur.
- **Katılımcılar:** Yerel işlemleri yürütür, hazırlanıp hazırlanamayacaklarını bildirir ve kararı uygular.

Protokolün adı, karar sürecindeki iki aşamadan gelir:

| Aşama | Koordinatör | Katılımcı | Olası sonuç |
|---|---|---|---|
| Hazırlık | `PREPARE` yollar | Kaynakları kilitler, günlüğe yazar | `YES` veya `NO` |
| Karar | Oyları değerlendirir | Nihai komutu uygular | `COMMIT` veya `ROLLBACK` |

### 1. Hazırlık aşaması

Koordinatör bütün katılımcılara işlemi tamamlamaya hazır olup olmadıklarını sorar. Bir katılımcı `YES` demeden önce gerekli kilitleri almalı, değişiklikleri kalıcı işlem günlüğüne yazmalı ve çökme sonrasında devam edebileceğinden emin olmalıdır. Bu cevap, “Şimdilik tamamlamadım ama artık sözümden dönemem” anlamına gelir.

### 2. Karar aşaması

Bütün oylar `YES` ise koordinatör `COMMIT` kararı verir. Herhangi bir `NO`, zaman aşımı veya erişilemeyen katılımcı varsa güvenli tercih `ROLLBACK` olur. Karar dayanıklı biçimde kaydedildikten sonra katılımcılara gönderilir.

Aşağıdaki sade Python benzeri kod koordinatör mantığını gösterir:

```python
def two_phase_commit(participants, transaction):
    votes = []

    for participant in participants:
        votes.append(participant.prepare(transaction))

    decision = 'COMMIT' if all(votes) else 'ROLLBACK'
    durable_log.write(transaction.id, decision)

    for participant in participants:
        participant.finish(transaction, decision)

    return decision
```

Buradaki `prepare`, katılımcının yerel kontrollerini ve kaynak kilitlemesini gerçekleştirir. Kararın `durable_log` içine yazılması kritiktir; koordinatör yeniden başladığında hangi komutu göndermesi gerektiğini buradan öğrenir. Gerçek uygulamalarda ayrıca zaman aşımı, tekrar deneme ve yinelenen mesajlara karşı idempotency gerekir.

## Güçlü ama kusursuz değil

2PC atomiklik sağlar; ancak otomatik olarak yüksek erişilebilirlik veya performans sağlamaz. En önemli problemi **bloklanabilen** bir protokol olmasıdır. Katılımcı `YES` dedikten sonra koordinatör çökerse nihai kararı öğrenene kadar kilitleri tutabilir.

| Yaklaşım | Tutarlılık | Erişilebilirlik | Tipik kullanım |
|---|---|---|---|
| 2PC | Güçlü atomiklik | Koordinatöre bağımlı | Veritabanı odaklı kritik işlemler |
| Saga | Nihai tutarlılık | Daha yüksek | Uzun süren mikroservis akışları |
| 3PC | Daha az bloklanma hedefi | Daha karmaşık | Nadir ve kontrollü ortamlar |

CAP perspektifinden bakıldığında ağ bölünmesi sırasında güçlü tutarlılığı korumak, bazı işlemlerin beklemesini veya reddedilmesini gerektirebilir. Bu nedenle 2PC, “her yerde kullanalım” çözümü değildir. Kısa süren işlemler, güvenilir ağlar ve güçlü atomiklik gereksinimi varsa oldukça değerlidir. Uzun iş akışlarında ise Saga ve telafi işlemleri daha esnek olabilir.

Özetle 2PC, dağıtık sistemlere şu disiplinli mesajı verir: Herkes hazır olmadan kutlama yok! Buna karşılık koordinatörün güvenilirliği, günlüklerin kalıcılığı, kilit süreleri ve hata senaryoları dikkatle tasarlanmalıdır.

---
layout: post
title: "Paxos’un Karmaşıklığı: Raft’tan Önce Konsensüsün Zor Yolu"
math: true
categories: 
  - Bilgi
tags: 
  - paxos
  - konsensüs
  - dağıtık-sistemler
  - raft
  - algoritma
  - hata-toleransı
toc: true
image: /img/paxosun-karmasikligi-rafttan-63.png
---

Dağıtık sistemlerde birkaç sunucunun aynı gerçek üzerinde anlaşmasını sağlamak, dışarıdan bakıldığında basit bir oylama problemi gibi görünür. Fakat mesajlar gecikebilir, makineler çökebilir ve ağ ikiye bölünebilir. Paxos, bu kaos içinde güvenli biçimde karar vermeyi sağlayan en önemli konsensüs algoritmalarından biridir; aynı zamanda ünü kadar korkutucu notasyonuyla da geliştiricilerin rüyalarına girer.

``

## Konsensüs neden bu kadar zor?

Birden fazla düğümün tek bir değer üzerinde anlaşması gerekir. Örneğin dağıtık bir veritabanı, `bakiye = 100` ile `bakiye = 50` komutlarından hangisinin kabul edildiğini kesin olarak bilmelidir. İstenen temel özellikler şunlardır:

- **Güvenlik:** İki farklı değer aynı anda seçilemez.
- **Canlılık:** Sistem uygun koşullarda sonunda bir değer seçer.
- **Hata toleransı:** Bazı düğümler çökse bile sistem çalışabilir.

Toplam düğüm sayısı $N$, tolere edilmek istenen hata sayısı $f$ ise çoğunluğa dayalı bir sistemde genel koşul şöyledir:

$$N \geq 2f + 1$$

Dolayısıyla iki arızayı tolere etmek için en az beş düğüm gerekir. Çoğunluk kümeleri mutlaka kesiştiğinden, önceki kararın bilgisi tamamen kaybolmaz.

## Paxos’un oyuncuları

Paxos aynı düğüm üzerinde çalışabilen üç mantıksal rol tanımlar:

| Rol | Görevi | Benzetme |
|---|---|---|
| Proposer | Bir değer önerir | Teklif veren milletvekili |
| Acceptor | Tekliflere söz verir ve oy verir | Seçmen |
| Learner | Seçilen sonucu öğrenir | Sonucu izleyen vatandaş |

![paxosun-karmasikligi-rafttan-63](/img/paxosun-karmasikligi-rafttan-63.svg)


Algoritmanın kalbinde monoton artan **öneri numarası** bulunur. Her öneri $(n, v)$ biçimindedir; burada $n$ benzersiz numara, $v$ ise önerilen değerdir.

## İki aşamalı dans

İlk aşama **Prepare/Promise** sürecidir. Proposer, acceptor’lara bir öneri numarası yollar. Acceptor daha büyük bir numaraya söz vermediyse bu numaradan küçük önerileri artık kabul etmeyeceğini bildirir. Daha önce kabul ettiği bir değer varsa onu da cevabına ekler.

İkinci aşama **Accept/Accepted** sürecidir. Proposer, çoğunluktan yanıt aldıktan sonra değer gönderir. Yanıtlarda daha önce kabul edilmiş değerler varsa en büyük numaralı önerinin değerini kullanmak zorundadır. Yoksa kendi değerini seçebilir. Bu kural, yeni liderin eski kararı yanlışlıkla ezmesini önler.

Basitleştirilmiş proposer mantığı şöyle gösterilebilir:

```python
def propose(number, preferred_value, acceptors):
    promises = send_prepare(number, acceptors)

    if len(promises) <= len(acceptors) // 2:
        return retry_with_larger_number()

    accepted = [p.accepted for p in promises if p.accepted]
    value = max(accepted).value if accepted else preferred_value
    return send_accept(number, value, acceptors)
```

Bu kod üretim kullanımı için eksiktir; ancak proposer’ın çoğunluğu beklediğini ve geçmişte kabul edilmiş en güncel değeri koruduğunu açıkça gösterir.

## Paxos neden anlaşılmaz bulundu?

Paxos’un güvenlik fikri zariftir, fakat orijinal anlatımı tek bir kararın nasıl verildiğine odaklanır. Gerçek sistemler ise sürekli komut üretir, lider değiştirir, günlük çoğaltır ve üyelik günceller. Bu ihtiyaçlar **Multi-Paxos** gibi genişletmeleri doğurmuştur.

| Özellik | Paxos | Raft |
|---|---|---|
| Temel anlatım | Öneriler ve çoğunluklar | Lider ve çoğaltılmış günlük |
| Lider | Temel modelde zorunlu değil | Merkezi kavram |
| Öğrenme eğrisi | Dik | Daha erişilebilir |
| Güvenlik | Çok güçlü | Çok güçlü |
| Uygulama rehberliği | Daha soyut | Daha yapılandırılmış |

Paxos ayrıca eş zamanlı proposer’lar yüzünden canlılık sorunu yaşayabilir. İki proposer sürekli daha büyük numaralar üretip birbirini geçersiz kılabilir. Güvenlik bozulmaz, fakat ilerleme durabilir. Pratik çözümler kararlı bir lider ve rastgele geri çekilme süreleri kullanır.

## Raft’tan önceki miras

Raft, Paxos’un matematiksel temelini çöpe atmadı; aynı çoğunluk kesişimi fikrini daha anlaşılır lider seçimi, dönem numaraları ve günlük kurallarıyla paketledi. Paxos’u öğrenmek bu nedenle yalnızca tarih dersi değildir. Dağıtık sistemlerde güvenliğin neden birkaç `if` koşulundan ibaret olmadığını, bilginin arızalar arasında nasıl korunduğunu ve çoğunluğun neden sihirli sayı olduğunu gösteren güçlü bir zihinsel egzersizdir.

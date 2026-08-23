---
layout: post
title: "Paxos Algoritmasını Anlamak: Dağıtık Sistemlerde Güvenilir Karar Sanatı"
math: true
categories: 
  - Bilgi
tags: 
  - paxos
  - dağıtık sistemler
  - hata toleransı
---

Dağıtık sistemlerde en zor soru çoğu zaman “veri nerede?” değil, “herkes aynı kararı verdi mi?” sorusudur. Ağ gecikebilir, makineler kapanabilir ve mesajlar kaybolabilir; buna rağmen banka bakiyesinin, lider seçiminin ya da sipariş durumunun tek bir doğru geçmişi olmalıdır. Paxos, düğümlerin çökebildiği bu kaotik ortamda ortak bir değerde uzlaşmayı sağlayan klasik consensus algoritmasıdır.
``

Paxos’un temel hedefi **güvenliktir**: Sistem iki farklı değeri aynı anda seçilmiş kabul etmemelidir. Canlılık, yani sonunda karar verebilmek ise ağın sonunda sakinleşmesi ve yeterli sayıda düğümün erişilebilir olması gibi varsayımlara bağlıdır. Bu ayrım önemlidir; Paxos, sonsuz ağ bölünmesinde sihirli biçimde ilerleyemez, fakat yanlış bir karar da üretmez.

Algoritmada üç rol bulunur: **proposer** bir değer önerir, **acceptor** önerileri kabul ederek oylama gücünü taşır, **learner** ise seçilen sonucu öğrenir. Pratikte tek bir sunucu birden fazla rolü üstlenebilir. Kararın dayanıklılığı çoğunluk kesişimine dayanır. Toplam $N$ acceptor varsa gerekli çoğunluk şöyledir:

$$q = \left\lfloor \frac{N}{2} \right\rfloor + 1$$

İki çoğunluğun en az bir ortak acceptor içermesi, eski bir kabulün yeni turda kaybolmamasını sağlar. Örneğin 5 acceptor için $q=3$ olur; herhangi iki adet üçlü grubun mutlaka ortak bir üyesi vardır.

| Kavram | Görevi | Neden gerekli? |
|---|---|---|
| Proposer | Numaralı öneri başlatır | Eşzamanlı talepleri düzenler |
| Acceptor | Söz verir ve kabul eder | Kararın kalıcı oylama kaydıdır |
| Learner | Sonucu uygular | Uygulama durumunu günceller |
| Çoğunluk | En az $q$ oy | Çelişkili kararları engeller |

Paxos iki ana turla çalışır. İlk turda proposer, benzersiz ve artan bir teklif numarasıyla **Prepare(n)** mesajı yollar. Acceptor, daha büyük numaralı bir prepare görmedikçe daha küçük teklifleri kabul etmeyeceğine söz verir ve varsa daha önce kabul ettiği en yüksek numaralı değeri döndürür. İkinci turda proposer **Accept(n, value)** mesajını gönderir. Kritik kural şudur: Prepare yanıtlarında daha önce kabul edilmiş bir değer varsa proposer kendi istediği değeri değil, en yüksek numaralı önceki değeri teklif etmelidir.

Aşağıdaki sade kod, proposer’ın değer seçme mantığını gösterir:

```python
def choose_value(promises, requested_value):
    accepted = [p for p in promises if p.accepted_number is not None]
    if not accepted:
        return requested_value
    latest = max(accepted, key=lambda p: p.accepted_number)
    return latest.accepted_value
```

Bu fonksiyon yeni bir öneri başlatıldığında çalışır. Hiçbir acceptor geçmişte değer kabul etmemişse istemcinin talebi kullanılabilir. Aksi durumda en yeni kabul edilmiş değer korunur; Paxos’un “iki farklı karar çıkmasın” garantisinin küçük ama hayati parçası budur.

| Durum | Paxos’un davranışı | Sonuç |
|---|---|---|
| Bir acceptor çöker | Çoğunluk varsa devam eder | Hata toleransı korunur |
| Mesaj gecikir | Daha yüksek teklif turu açılabilir | Güvenlik bozulmaz |
| İki proposer yarışır | Teklif numaraları rekabeti çözer | Geçici canlılık kaybı olabilir |
| Çoğunluk kaybolur | Karar ertelenir | Yanlış karar verilmez |

Paxos çoğu zaman “anlaşılması zor” diye ünlenir; çünkü ağ başarısızlıklarını ciddiye alır. Production ortamında lideri sık değişmeyen **Multi-Paxos**, ilk hazırlık turunun maliyetini amorti ederek ardışık log kayıtlarını verimli biçimde seçer. Raft gibi daha öğretici tasarımlar popüler olsa da Paxos’un fikri değişmez: çoğunlukların kesişimi ve teklif numaraları sayesinde, dağıtık bir kalabalık tek bir geçmiş üzerinde uzlaşabilir.

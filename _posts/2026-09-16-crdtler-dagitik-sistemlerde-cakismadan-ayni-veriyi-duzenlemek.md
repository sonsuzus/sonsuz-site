---
layout: post
title: "CRDT’ler: Dağıtık Sistemlerde Çakışmadan Aynı Veriyi Düzenlemek"
math: true
categories: 
  - Bilgi
tags: 
  - crdt
  - dağıtık-sistemler
  - veri-yapıları
  - eventual-consistency
  - javascript
toc: true
image: /img/crdtler-dagitik-sistemlerde-99.png
---

İki kullanıcının çevrimdışı çalışırken aynı belgeyi değiştirdiğini düşünün. İnternet geri geldiğinde hangi sürüm kazanmalı? Birini seçmek veri kaybına, her değişikliği sırayla işlemek ise koordinasyon maliyetine yol açabilir. **CRDT** (Conflict-free Replicated Data Type), farklı kopyalarda yapılan eş zamanlı değişikliklerin merkezi bir hakeme ihtiyaç duymadan güvenli biçimde birleştirilmesini sağlayan veri yapıları ailesidir.


![crdtler-dagitik-sistemlerde-99](/img/crdtler-dagitik-sistemlerde-99.svg)

``

## Temel problem: sıralama olmadan uzlaşmak

Dağıtık bir sistemde ağ gecikebilir, cihazlar çevrimdışı kalabilir ve mesajlar farklı sırada ulaşabilir. Klasik bir veritabanı çoğunlukla kilit, lider düğüm veya konsensüs protokolü kullanarak işlemleri sıralar. CRDT yaklaşımıysa işlemleri engellemek yerine veri yapısını, olası birleşmeler her durumda aynı sonuca ulaşacak biçimde tasarlar.

Bunun arkasındaki sihir aslında cebirsel özelliklerdir. Birleştirme işlemini $\sqcup$ ile gösterirsek şu kurallar önemlidir:

- **Değişme:** $a \sqcup b = b \sqcup a$
- **Birleşme:** $(a \sqcup b) \sqcup c = a \sqcup (b \sqcup c)$
- **Tekrarlama:** $a \sqcup a = a$

Böylece mesajın önce, sonra veya yanlışlıkla iki kez gelmesi sonucu değiştirmez. Tüm güncellemeler sonunda her replikaya ulaştığında sistem **güçlü nihai tutarlılık** sağlar.

## CRDT ve geleneksel yaklaşım

| Özellik | Kilit/Konsensüs yaklaşımı | CRDT yaklaşımı |
|---|---|---|
| Çevrimdışı yazma | Genellikle zor | Doğal olarak desteklenir |
| Anlık tutarlılık | Sağlanabilir | Genellikle sağlanmaz |
| Ağ bölünmesine dayanıklılık | Sınırlı olabilir | Yüksektir |
| Çakışma çözümü | Çalışma anında veya sonradan | Veri yapısına gömülüdür |
| Ek metadata | Daha az olabilir | Çoğu zaman gereklidir |

CRDT, “her problem için bedava çözüm” değildir. Kullanıcı bakiyesinin sıfırın altına düşmemesi gibi küresel kurallar, koordinasyon gerektirebilir. Buna karşılık sayaçlar, beğeniler, ortak belgeler, çevrimdışı uygulamalar ve çok bölgeli sistemler için oldukça uygundur.

## İki ana CRDT ailesi

**Durum tabanlı CRDT’lerde** replikalar mevcut durumlarını paylaşır. Alıcı, iki durumu bir `merge` fonksiyonuyla birleştirir. Birleştirme güvenlidir ancak büyük durumların taşınması pahalı olabilir.

**İşlem tabanlı CRDT’lerde** yalnızca “A elemanını ekle” gibi operasyonlar gönderilir. Ağ trafiği azalır; fakat teslimat garantileri ve işlem kimlikleri daha önemli hâle gelir.

| Aile | Paylaşılan şey | Avantaj | Bedel |
|---|---|---|---|
| State-based | Tüm durum veya delta | Tekrarlı teslimata dayanıklı | Daha fazla veri aktarımı |
| Operation-based | Güncelleme işlemi | Küçük mesajlar | Daha güçlü ağ varsayımları |

## Örnek: G-Counter

Yalnızca artabilen bir sayaçta her replika kendi hücresini artırır. Birleştirme sırasında aynı hücrelerin maksimumu alınır. Toplam değer ise hücrelerin toplamıdır:

$$value = c_1 + c_2 + \dots + c_n$$

```javascript
class GCounter {
  constructor(nodeId, state = {}) {
    this.nodeId = nodeId;
    this.state = { ...state };
    this.state[nodeId] ??= 0;
  }

  increment(amount = 1) {
    if (amount < 0) throw new Error("G-Counter azaltılamaz");
    this.state[this.nodeId] += amount;
  }

  merge(other) {
    for (const node of Object.keys(other.state)) {
      this.state[node] = Math.max(
        this.state[node] ?? 0,
        other.state[node]
      );
    }
  }

  value() {
    return Object.values(this.state).reduce((sum, n) => sum + n, 0);
  }
}
```

Burada `increment` yalnızca yerel düğümün değerini değiştirir. `merge`, her düğüm için en büyük değeri seçtiğinden eski veya tekrarlı mesajlar sayacı yanlışlıkla büyütmez. Azaltma gerekiyorsa, biri artışları diğeri azalışları izleyen iki G-Counter kullanılarak **PN-Counter** oluşturulabilir.

## Başka CRDT türleri

**LWW-Register**, zaman damgası en yeni değeri seçer; basittir ama saat sapmaları risklidir. **OR-Set**, eklenen öğelere benzersiz kimlikler vererek ekleme ve silme yarışlarını yönetir. Metin CRDT’leri ise karakterleri konum yerine kalıcı kimliklerle ilişkilendirir; böylece iki kullanıcı aynı noktaya yazdığında iki ekleme de korunabilir.

Özetle CRDT’ler çakışmaları sonradan “tamir etmek” yerine, çakışmanın güvenli birleşeceği kuralları baştan tanımlar. Bunun karşılığında metadata, silinmiş kayıtları izleyen mezar taşları ve dikkatli veri modelleme maliyeti getirir. Doğru problemde kullanıldığında ise çevrimdışı çalışabilen, hızlı ve dayanıklı dağıtık uygulamaların en güçlü araçlarından biridir.

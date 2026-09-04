---
layout: post
title: "Raft Konsensüs Algoritması: Lider Seçimi ve Tutarlı Verinin Anatomisi"
math: true
categories: 
  - Bilgi
tags: 
  - raft
  - dağıtık sistemler
  - konsensüs
  - lider seçimi
toc: true
image: /img/raft-konsensus-algoritmasi-13.png
---

Dağıtık sistemlerde aynı veriyi birden fazla makinede tutmak harikadır; tek bir sunucu bozulduğunda sistem ayakta kalır. Fakat işin zor kısmı şudur: Ağ gecikebilir, makineler sessizce kapanabilir ve iki sunucu aynı anda farklı şeylerin doğru olduğuna inanabilir. Raft, bu kaosu yönetmek için tasarlanmış, anlaşılabilirliği önceleyen bir konsensüs algoritmasıdır. Temel hedefi, tüm sağlıklı düğümlerin işlemleri aynı sırayla uygulamasını sağlamaktır.

![raft-konsensus-algoritmasi-13](/img/raft-konsensus-algoritmasi-13.svg)

``

Raft kümesindeki her düğüm üç rolden birindedir: **lider**, **takipçi** veya **aday**. Normal koşullarda tek bir lider bulunur; istemci yazma istekleri önce ona gelir. Lider, isteği kendi günlük kaydına ekler ve diğer düğümlere çoğaltır. Takipçiler ise lideri dinler. Lider ortadan kaybolursa, takipçilerden biri aday olur ve seçim sürecini başlatır.

| Rol | Temel sorumluluk | Ne zaman ortaya çıkar? |
|---|---|---|
| Takipçi | Liderin kayıtlarını çoğaltmak | Normal çalışma sırasında |
| Aday | Oy toplayarak lider olmaya çalışmak | Zaman aşımı yaşandığında |
| Lider | İstekleri sıralamak ve çoğaltmak | Çoğunluk oyu aldığında |

## Kalp Atışları ve Lider Seçimi

Lider, takipçilere düzenli olarak **heartbeat** (kalp atışı) mesajları yollar. Bir takipçi belirli bir süre boyunca bu mesajı almazsa liderin düştüğünü varsayar. Ardından dönem numarasını, yani `term` değerini artırır; aday olur ve diğer düğümlerden oy ister.

Her dönem, sistemin mantıksal saatidir. Bir düğüm her dönemde yalnızca bir kez oy verir. Aday, kümenin çoğunluğunun oyunu alırsa liderdir. Çoğunluk eşiği şu şekilde ifade edilir:

$$
quorum = \left\lfloor \frac{N}{2} \right\rfloor + 1
$$

Burada $N$, toplam düğüm sayısıdır. Örneğin beş düğümlü bir kümede lider olmak veya bir kaydı onaylamak için en az üç düğüm gerekir. Bu kural, ağ ikiye bölünse bile iki farklı liderin kalıcı olarak karar vermesini engeller.

| Küme boyutu | Arızaya dayanıklılık | Gerekli çoğunluk |
|---:|---:|---:|
| 3 | 1 düğüm | 2 |
| 5 | 2 düğüm | 3 |
| 7 | 3 düğüm | 4 |

Rastgele seçilen seçim zaman aşımı, adayların aynı anda yarışıp sürekli berabere kalma ihtimalini azaltır. Yani Raft, teknik olarak ciddi; pratikte ise toplantıya geç kalanların arasından doğal biçimde bir sözcü seçmeye oldukça benzer.

## Günlük Çoğaltma ve Güvenli Onay

İstemci `SET tema=karanlik` gibi bir komut gönderdiğinde lider bunu günlüğüne ekler. Sonra `AppendEntries` RPC çağrısıyla takipçilere iletir. Kayıt, ancak çoğunluğa ulaştığında **commit** edilir ve durum makinesine uygulanır. Böylece istemciye başarı yanıtı verilmeden önce veri güvence altına alınmış olur.

```text
İstemci -> Lider: SET tema=karanlik
Lider   -> Takipçiler: AppendEntries(index=42, command=SET ...)
Takipçiler -> Lider: ACK
Lider   -> Küme: commitIndex = 42
```

Bu akıştaki kritik ayrım şudur: Bir kaydın lidere yazılması, onun kesinleştiği anlamına gelmez. Kesinlik için çoğunluk onayı gerekir. Lider seçim sırasında da en güncel günlüğe sahip adayların avantajlı olması sağlanır; böylece onaylanmış kayıtlar yeni lider tarafından kaybedilmez.

## Neden Raft Tercih Edilir?

Raft, Paxos ailesindeki algoritmalarla benzer güvenlik hedeflerine ulaşır; ancak lider merkezli akışı ve açık kurallarıyla uygulaması daha pratiktir. etcd, Consul ve CockroachDB gibi araçlarda bu yaklaşımın izlerini görmek mümkündür.

Raft kullanırken düğüm sayısını tek sayı seçmek, disk kalıcılığını ihmal etmemek ve ağ gecikmelerine uygun zaman aşımı değerleri belirlemek önemlidir. Sonuçta Raft sihir değildir: çoğunluk erişilemezse yazma işlemlerini durdurur. Ancak bu ödün, bölünmüş bir ağda yanlış veri yazmaktan çok daha güvenlidir.

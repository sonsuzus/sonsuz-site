---
layout: post
title: "LRU, LFU ve CLOCK: İşletim Sistemi Hangi Sayfayı Bellekten Atıyor?"
math: true
categories: 
  - Bilgi
tags: 
  - işletim sistemi
  - bellek yönetimi
  - sayfa değiştirme
  - lru
  - lfu
  - clock
toc: true
---

Bir program çalışırken ihtiyaç duyduğu bütün sayfalar fiziksel belleğe sığmayabilir. İşletim sistemi bu durumda disk ile RAM arasında küçük bir sandalye kapmaca oyunu oynar: Yeni sayfa gelecek, fakat boş çerçeve yoksa içerideki sayfalardan biri çıkarılmalıdır. Peki kurban kim olacak? LRU, LFU ve CLOCK algoritmaları aynı soruya farklı ipuçlarıyla cevap verir.
``

## Önce sahneyi kuralım

Sanal bellek, süreçlerin fiziksel RAM’den daha büyük ve kesintisiz görünen bir adres alanı kullanmasını sağlar. İşlemci RAM’de bulunmayan bir sayfaya eriştiğinde **sayfa hatası** oluşur. İşletim sistemi sayfayı diskten getirir; boş çerçeve yoksa bir **sayfa değiştirme algoritması** çalıştırır.

Bir erişim dizisi $R=(r_1,r_2,\ldots,r_n)$ ve $F$ adet çerçeve için temel hedef, sayfa hatalarının sayısını azaltmaktır:

$$
\text{Hata Oranı}=\frac{\text{Sayfa Hatası Sayısı}}{n}
$$

Ancak yalnızca hata sayısı önemli değildir. Algoritmanın tuttuğu metadata, güncelleme maliyeti ve donanım desteği de gerçek sistemlerde sonucu belirler.

## LRU: En uzun süredir dokunulmayan gitsin

**Least Recently Used**, yakın geçmişin yakın geleceği tahmin ettiğini varsayar. Bir sayfa uzun süredir kullanılmadıysa yeniden kullanılma ihtimali düşük kabul edilir. Örneğin üç çerçevede son erişim sırası `A, C, B` ise ve `D` gelirse en eski kullanılan `A` atılır.

Gerçek LRU uygulamak için her erişimin zamanını kaydetmek veya sayfaları sıralı bir yapıda taşımak gerekir. Bu oldukça pahalı olabilir. Sayaç taşmaları ve eşzamanlı güncellemeler de cabasıdır. Bu nedenle işletim sistemleri çoğunlukla LRU’nun yaklaşık biçimlerini kullanır.

## LFU: En az çalışan kapının önüne

**Least Frequently Used**, her sayfanın kaç kez erişildiğini sayar ve frekansı en düşük olanı seçer:

$$
\operatorname{victim}=\arg\min_{p\in M} \operatorname{frequency}(p)
$$

Bu yaklaşım sık kullanılan sayfaları korur. Fakat başlangıçta çok kullanılan, daha sonra tamamen unutulan bir sayfa yüksek sayacı yüzünden bellekte gereksiz yere kalabilir. Buna karşı sayaçlar belirli aralıklarla azaltılabilir; örneğin $f \leftarrow \lfloor f/2 \rfloor$. Eşitlik durumunda LRU gibi ikinci bir kural gerekir.

## CLOCK: LRU’ya ekonomik yaklaşım

CLOCK, sayfaları dairesel bir listede düşünür. Her sayfanın bir **referans biti** vardır. Donanım sayfaya erişildiğinde bu biti `1` yapar. Saat ibresi aday sayfaları dolaşır:

- Bit `0` ise sayfa kurban seçilir.
- Bit `1` ise bit sıfırlanır ve ibre ilerler.
- Böylece yakın zamanda kullanılan sayfalara ikinci şans verilir.

```python
def clock_victim(reference_bits, hand):
    """Kurban çerçeveyi ve ibrenin yeni konumunu döndürür."""
    while reference_bits[hand] == 1:
        reference_bits[hand] = 0
        hand = (hand + 1) % len(reference_bits)

    victim = hand
    hand = (hand + 1) % len(reference_bits)
    return victim, hand
```

Kod, gerçek çekirdek uygulamalarındaki kilitleri ve kirli sayfa kontrollerini içermez; ancak ikinci şans mantığını gösterir. En kötü durumda ibre birkaç tur atabilir, pratikte ise işlem maliyeti gerçek LRU’dan düşüktür.

| Algoritma | Karar ölçütü | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| LRU | Son erişim zamanı | Yerellik davranışını iyi yakalar | Kesin takibi pahalıdır |
| LFU | Erişim sayısı | Sürekli popüler sayfaları korur | Eski popülerliği unutamaz |
| CLOCK | Referans biti | Basit, hızlı ve uygulanabilirdir | Kesin LRU sonucu vermez |

## İşletim sistemi gerçekte hangisini seçer?

Modern işletim sistemleri genellikle saf LRU veya LFU yerine CLOCK benzeri, yaşlandırmalı ve çok listeli yöntemler kullanır. Ayrıca sayfanın **kirli** olup olmadığı önemlidir: Kirli sayfa değiştirilmiş olduğu için diske yazılmalıdır; temiz sayfa ise doğrudan atılabilir. Bu nedenle kurban seçimi yalnızca geçmiş erişimlere değil, I/O maliyetine de dayanabilir.

Kısacası LRU “en eski ziyaretçiyi”, LFU “en seyrek ziyaretçiyi”, CLOCK ise “ikinci şansını tüketeni” dışarı çıkarır. Teoride en sezgisel aday LRU, belirli iş yüklerinde LFU, genel amaçlı sistemlerde ise düşük maliyeti sayesinde CLOCK ve türevleridir. Bellek yönetiminde tek bir şampiyon yoktur; kazananı erişim deseni belirler.

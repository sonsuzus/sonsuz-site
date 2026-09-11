---
layout: post
title: "Veritabanında Trafik Sıkışıklığı: Deadlock ve İki Fazlı Kilitleme"
math: true
categories: 
  - Bilgi
tags: 
  - veritabanı
  - deadlock
  - eşzamanlılık
toc: true
---

Bir veritabanında yüzlerce işlemin aynı anda çalışması, kavşaktan birlikte geçmeye çalışan araçlara benzer. Her işlem hızla ilerlemek ister; fakat ortak verilere kontrolsüz erişim, kayıp güncelleme ve tutarsız okuma gibi sorunlar doğurur. Kilitler bu trafiği düzenlerken yanlış sırada alınmaları işlemleri birbirini sonsuza kadar bekleyen bir deadlock durumuna sokabilir.

``

## Eşzamanlılık neden önemlidir?

Bir **transaction**, veritabanının tek bir mantıksal iş olarak değerlendirdiği komutlar bütünüdür. Örneğin hesaptan para aktarma işlemi hem kaynak hesabı azaltmalı hem hedef hesabı artırmalıdır. Bu sırada başka bir transaction aynı hesapları güncellerse sonuç hatalı olabilir.

Kilit yöneticisi, transaction’ların veri üzerinde hangi işlemleri yapabileceğini belirler. En yaygın iki kilit türü şunlardır:

| Kilit | Amaç | Başka ortak kilitle uyumlu mu? | Özel kilitle uyumlu mu? |
|---|---|---:|---:|
| Ortak kilit (`S`) | Veriyi okumak | Evet | Hayır |
| Özel kilit (`X`) | Veriyi değiştirmek | Hayır | Hayır |

Bir veri öğesi üzerindeki kilit durumunu $L(x)$ ile gösterelim. Bir transaction yazma yapmak istiyorsa $X(x)$ kilidini edinmelidir. Aynı anda başka bir transaction $S(x)$ veya $X(x)$ tutuyorsa yazan işlem bekletilir. Böylece doğruluk korunur; ancak beklemeler döngü oluşturabilir.

## Deadlock nasıl meydana gelir?

İki transaction’ın farklı kaynakları ters sırayla kilitlediğini düşünelim:

1. $T_1$, `HesapA` için özel kilit alır.
2. $T_2$, `HesapB` için özel kilit alır.
3. $T_1`, `HesapB` kilidini bekler.
4. $T_2`, `HesapA` kilidini bekler.

Artık iki işlem de elindeki kilidi bırakmadan diğerini beklemektedir. Bekleme ilişkisini bir **wait-for graph** ile gösterebiliriz. $T_i \rightarrow T_j$ kenarı, $T_i$ işleminin $T_j$ tarafından tutulan bir kilidi beklediği anlamına gelir. Grafikte bir çevrim bulunması deadlock göstergesidir:

$$T_1 \rightarrow T_2 \rightarrow T_1$$

Basitleştirilmiş bir çevrim tespiti şöyle yazılabilir:

```python
def deadlock_var_mi(graf):
    ziyaret, aktif = set(), set()

    def tara(islem):
        if islem in aktif:
            return True
        if islem in ziyaret:
            return False

        ziyaret.add(islem)
        aktif.add(islem)
        for beklenen in graf.get(islem, []):
            if tara(beklenen):
                return True
        aktif.remove(islem)
        return False

    return any(tara(t) for t in graf)
```

Kod, derinlik öncelikli arama sırasında hâlen aktif olan bir düğüme yeniden ulaşırsa çevrim bulur. Gerçek veritabanları benzer bir kontrolün ardından kurban transaction seçer, onu geri alır ve kilitlerini serbest bırakır. Kurban seçilirken işlem maliyeti, değiştirdiği satır sayısı veya yaşı değerlendirilebilir.

## İki fazlı kilitleme mekanizması

**Two-Phase Locking (2PL)**, kilit alma ve bırakma işlemlerini iki ayrı evreye böler:

| Evre | Yapılabilen işlem | Yapılamayan işlem |
|---|---|---|
| Büyüme | Yeni kilit alma | Kilit bırakma |
| Küçülme | Kilit bırakma | Yeni kilit alma |

Transaction ilk kilidini bıraktığı anda küçülme evresine geçer ve artık yeni kilit alamaz. Bu kural, çalışma sonucunun işlemler seri çalışmış gibi olmasını sağlayan **çatışma serileştirilebilirliğine** temel oluşturur. Ancak standart 2PL deadlock’u engellemez; yalnızca tutarlı bir yürütme düzeni sağlar.

**Strict 2PL** yaklaşımında bütün özel kilitler `COMMIT` veya `ROLLBACK` anına kadar tutulur. **Rigorous 2PL** ise ortak ve özel kilitlerin tamamını işlem sonuna kadar saklar. Bu yöntemler geri alma sürecini kolaylaştırır, fakat bekleme sürelerini artırabilir.

## Deadlock’u azaltma stratejileri

Kaynakları her zaman aynı sırada kilitlemek döngü ihtimalini ciddi ölçüde azaltır. Ayrıca zaman aşımı, kısa transaction tasarımı ve `wait-die` ya da `wound-wait` gibi zaman damgası tabanlı yöntemler kullanılabilir. Özetle kilit, veritabanının emniyet kemeridir: doğru kullanıldığında korur, yanlış sırada takıldığında ise herkesi araçta mahsur bırakabilir.

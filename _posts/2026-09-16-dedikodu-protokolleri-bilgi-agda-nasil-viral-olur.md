---
layout: post
title: "Dedikodu Protokolleri: Bilgi Ağda Nasıl Viral Olur?"
math: true
categories: 
  - Bilgi
tags: 
  - dağıtık-sistemler
  - gossip-protokolü
  - ağ
  - algoritma
  - python
  - tutarlılık
toc: true
---

Bir sunucunun öğrendiği haberi rastgele birkaç komşusuna söylediğini, onların da aynı şeyi başkalarına aktardığını düşünün. Bir süre sonra bütün ağ haberdar olur; üstelik ortada süreci yöneten bir merkez yoktur. Dağıtık sistemlerde bu modele **gossip**, yani dedikodu protokolü denir. İnsan topluluklarında bazen baş ağrıtan dedikodu, bilgisayar ağlarında ölçeklenebilirlik ve arıza toleransı sağlayan son derece kullanışlı bir mekanizmadır.

``

## Temel fikir: Herkes birkaç kişiyle konuşur

Gossip protokollerinde her düğüm, belirli aralıklarla rastgele seçtiği düğümlerle bilgi paylaşır. Bu bilgi yeni bir olay, servis durumu, sayaç değeri veya küme üyeliği olabilir. Bir düğümün herkese tek tek mesaj göndermesi gerekmez; haber dalgalar hâlinde yayılır.

Basit bir turda şu adımlar gerçekleşir:

1. Düğüm, ağdan rastgele bir eş seçer.
2. Bildiği veriyi veya veri özetini eşine yollar.
3. İki taraf eksik ya da eski kayıtlarını günceller.
4. İşlem sonraki turda başka eşlerle tekrarlanır.

Her bilgili düğümün bir turda bir yeni düğümü bilgilendirdiği ideal durumda, haberi bilenlerin sayısı yaklaşık olarak ikiye katlanır:

$$I(t) \approx \min(N, 2^t)$$

Burada $I(t)$, $t$ tur sonra bilgili düğüm sayısını; $N$ ise toplam düğüm sayısını gösterir. Dolayısıyla yayılım süresi ideal koşullarda yaklaşık $O(\log N)$ turdur. Gerçek ağlarda aynı eşin tekrar seçilmesi, paket kaybı ve çevrimdışı düğümler süreci yavaşlatır; fakat rastgelelik sistemi tek bir rotaya bağımlı olmaktan kurtarır.

## Push, pull ve push-pull

Dedikodunun birkaç farklı konuşma tarzı vardır:

| Yaklaşım | İletişim biçimi | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| Push | Bildiğini karşı tarafa gönderir | Yeni bilgi hızla yayılır | Son aşamada gereksiz mesaj üretir |
| Pull | Karşı taraftan eksik bilgiyi ister | Eski düğümleri yakalamada etkilidir | İlk yayılım daha yavaş olabilir |
| Push-pull | İki taraf da veri karşılaştırır | Hızlı ve dengelidir | Mesaj içeriği daha büyüktür |

Sistemler çoğunlukla tam veriyi sürekli taşımak yerine sürüm numarası, zaman damgası veya hash özeti gönderir. Böylece iki düğüm yalnızca farklı kayıtları aktarır. Bu yaklaşım, “Bende 42. sürüm var, sende kaç?” diye soran ekonomik bir dedikoducuya benzer.

## Küçük bir Python simülasyonu

Aşağıdaki örnek, haberi bilen her düğümün her turda rastgele bir düğüm seçmesini simüle eder:

```python
import random


def gossip(node_count, source=0):
    informed = {source}
    round_no = 0

    while len(informed) < node_count:
        newly_informed = set(informed)

        # Yalnızca mevcut tur başında haberi bilenler konuşur.
        for node in informed:
            peer = random.randrange(node_count)
            newly_informed.add(peer)

        informed = newly_informed
        round_no += 1
        print(f"Tur {round_no}: {len(informed)}/{node_count}")

    return round_no


gossip(100)
```

`set` kullanımı aynı düğümün birden fazla kez sayılmasını engeller. Sonuç her çalıştırmada değişir; çünkü protokolün merkezinde rastgele seçim vardır. Deneyi binlerce düğümle tekrarlayarak tur sayısının logaritmik büyümesini gözlemleyebilirsiniz.

## Tutarlılık mı, erişilebilirlik mi?

Gossip çoğunlukla **eventual consistency** sağlar: Güncellemeler anında her yerde görünmeyebilir, fakat yeni değişiklik gelmezse düğümler zamanla aynı duruma yakınsar. Bu nedenle banka bakiyesini kesin olarak kilitlemekten ziyade servis keşfi, önbellek geçersizleştirme, hata algılama ve izleme metrikleri için uygundur.

| Özellik | Merkezi yayın | Gossip |
|---|---|---|
| Tek hata noktası | Genellikle vardır | Yoktur |
| Mesaj kontrolü | Öngörülebilir | Olasılıksal |
| Anlık kesinlik | Daha kolay | Genellikle garanti edilmez |
| Büyük ağlara uyum | Merkez darboğaz olabilir | Yüksek |

Cassandra’nın küme durumunu paylaşması ve bazı dağıtık veritabanlarının üyelik bilgilerini yayması bu fikre dayanır. Özetle gossip, her mesajın kesin zamanda ulaşmasını değil, yeterince çok bağımsız temas sayesinde bilginin sonunda yayılmasını hedefler. Biraz rastgele, biraz geveze, fakat arızalar karşısında şaşırtıcı derecede dayanıklıdır.

---
layout: post
title: "Robotlarda Çarpışma Tespiti: Gerçek Zamanlı Planlamanın Görünmeyen Hesaplama Yükü"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - çarpışma tespiti
  - hareket planlama
  - gerçek zamanlı sistemler
  - algoritmalar
  - optimizasyon
toc: true
image: /img/robotlarda-carpisma-tespiti-50.png
---

Bir robotun A noktasından B noktasına ilerlemesi kolay görünür; ta ki masalar, insanlar, diğer robotlar ve robotun kendi eklemleri sahneye çıkana kadar! Gerçek zamanlı hareket planlamasında sistem yalnızca bir rota üretmez, bu rota üzerindeki binlerce aday durumun güvenli olup olmadığını da sınar. Bu nedenle çarpışma tespiti, planlayıcının görünmeyen ama çoğu zaman en pahalı çalışanıdır.

``

## Hesaplama yükü nereden geliyor?

Bir hareket planlayıcısı, robotun konfigürasyon uzayında çok sayıda örnek üretir. Robotun eklem açılarını içeren bir durum

$$q=(q_1,q_2,\ldots,q_n)$$

şeklinde gösterilebilir. Her $q$ için robot geometrisi ileri kinematikle dünya koordinatlarına taşınır ve engellerle kesişip kesişmediği araştırılır. Toplam süre kabaca

$$T_{plan}=N_{kontrol}(T_{kinematik}+T_{broad}+T_{narrow})$$

olarak düşünülebilir. Burada $N_{kontrol}$ test edilen durum sayısıdır. Robotun serbestlik derecesi arttıkça arama uzayı büyür; dolayısıyla tek bir test hızlı olsa bile milyonlarca tekrar sistemi zorlayabilir.

Üstelik yalnızca robot–engel çarpışmaları değil, robotun kendi bağlantıları arasındaki öz çarpışmalar da kontrol edilmelidir. Yedi eksenli bir kol, geometrik açıdan oldukça sosyal bir makinedir: Her bağlantı diğerleriyle tanışmak ister!

## Broad phase ve narrow phase

Modern motorlar çarpışma testini iki aşamaya böler. Broad phase, çarpışması mümkün olmayan nesne çiftlerini ucuz yöntemlerle eler. Narrow phase ise geriye kalan adaylar üzerinde hassas geometrik hesap yapar.

| Yaklaşım | Amaç | Tipik maliyet | Hassasiyet |
|---|---|---:|---|
| AABB | Eksen hizalı kutularla hızlı eleme | Çok düşük | Düşük |
| OBB | Döndürülmüş sınırlayıcı kutular | Düşük-orta | Orta |
| Bounding Volume Hierarchy | Geometriyi ağaç biçiminde gruplama | Genellikle $O(\log n)$ | Orta-yüksek |
| GJK | Konveks cisimler arasındaki mesafe | Orta | Yüksek |
| Üçgen-üçgen testi | Ayrıntılı yüzey kontrolü | Yüksek | Çok yüksek |
| Signed Distance Field | Noktadan engele yaklaşık mesafe | Sorguda düşük | Çözünürlüğe bağlı |

Her nesneyi her üçgenle karşılaştırmak, $m$ ve $n$ üçgenli iki model için yaklaşık $O(mn)$ maliyet doğurabilir. BVH kullanıldığında ağacın büyük bölümü erkenden elenir. Bu, kalabalık bir partide herkese tek tek kimlik sormak yerine önce davetli listesini bölümlere ayırmaya benzer.

## Ayrık ve sürekli çarpışma kontrolü

Ayrık kontrolde yörünge belirli zaman noktalarında örneklenir. İki güvenli örnek arasında robot ince bir engelin içinden geçebilir; buna tünelleme problemi denir. Sürekli çarpışma tespiti, hareket eden geometrinin bütün zaman aralığını inceler ve ilk temas zamanını arar.

| Yöntem | Avantaj | Dezavantaj |
|---|---|---|
| Ayrık kontrol | Hızlı ve basit | Küçük engelleri kaçırabilir |
| Sık örnekleme | Daha güvenli | Kontrol sayısını büyütür |
| Sürekli kontrol | Aralık boyunca güvence sağlar | Matematiksel olarak pahalıdır |

Örnekleme aralığı küçüldükçe kontrol sayısı yaklaşık olarak

$$N \approx \frac{T}{\Delta t}$$

artar. Yani zaman çözünürlüğünü iki katına çıkarmak, çarpışma sorgularını da yaklaşık iki katına çıkarabilir.

## Basitleştirilmiş bir kontrol döngüsü

Aşağıdaki Python benzeri kod, pahalı ayrıntılı testin yalnızca sınırlayıcı kutular kesiştiğinde çalıştırılmasını gösterir:

```python
def durum_guvenli(robot, engeller, q):
    # Eklem durumundan bağlantıların dünya pozlarını hesaplar.
    parcalar = robot.ileri_kinematik(q)

    for parca in parcalar:
        for engel in engeller:
            # Ucuz eleme testi, gereksiz ayrıntılı sorguları azaltır.
            if not parca.aabb.kesisir(engel.aabb):
                continue

            # Gerçek geometriler üzerinde daha pahalı test yapılır.
            if ayrintili_carpisma(parca.mesh, engel.mesh):
                return False

    return True
```

Bu yapı anlaşılır olsa da iç içe döngüler sahnedeki nesne sayısıyla hızla büyür. Gerçek sistemlerde uzamsal karma tablolar, sweep-and-prune, BVH ve önbellekleme kullanılarak aday çift sayısı azaltılır.

## Gerçek zaman için denge sanatı

Optimizasyonun amacı her zaman en hassas modeli kullanmak değildir; güvenlik ile gecikme arasında doğru dengeyi kurmaktır. Basitleştirilmiş çarpışma geometrileri, paralel sorgular, önceki zaman adımından sıcak başlangıç, adaptif örnekleme ve GPU hızlandırma önemli kazançlar sağlar. Dinamik engellerde yalnızca değişen bölgelerin güncellenmesi de tüm sahneyi yeniden hesaplamaktan kaçınır.

Sonuç olarak çarpışma tespiti, hareket planlamasının yardımcı ayrıntısı değil, performans bütçesinin merkezidir. İyi tasarlanmış bir sistem hassas testi her yerde çalıştırmaz; ucuz filtrelerle şüpheli durumları bulur ve hesaplama gücünü gerçekten tehlikeli adaylara harcar.

![robotlarda-carpisma-tespiti-50](/img/robotlarda-carpisma-tespiti-50.svg)


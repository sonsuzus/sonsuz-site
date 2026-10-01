---
layout: post
title: "Spot Sunucularla Ucuza Hesaplama: Kesilse de Yola Devam Eden Sistemler"
math: true
categories: 
  - Bilgi
tags: 
  - bulut bilişim
  - spot instance
  - dağıtık sistemler
  - devops
  - hata toleransı
  - kubernetes
toc: true
image: /img/spot-sunucularla-ucuza-89.png
---

![spot-sunucularla-ucuza-89](/img/spot-sunucularla-ucuza-89.svg)


Bulut faturanız roket gibi yükselirken spot sunucular bir indirim kuponu gibi yetişebilir. Bulut sağlayıcıları, boşta duran işlem kapasitesini standart fiyatın oldukça altında kiralar. Ancak küçük bir şartları vardır: Sağlayıcı kapasiteye ihtiyaç duyduğunda sunucunuzu kısa bir bildirimle kapatabilir. Dolayısıyla spot dünyasında temel soru “Sunucu kapanır mı?” değil, “Kapandığında uygulama ne yapar?” olmalıdır.
``
## Spot sunucu mantığı

Standart bir sanal makineyi kiraladığınızda kapasitenin size ayrılması beklenir. Spot modelinde ise kullanılmayan kapasiteyi geçici olarak tüketirsiniz. Bunun karşılığında bazı platformlarda %70-90 düzeyine ulaşabilen indirimler elde edebilirsiniz.

Yaklaşık tasarrufu şöyle ifade edebiliriz:

$$
Tasarruf\ Oranı = \frac{C_{standart} - C_{spot}}{C_{standart}} \times 100
$$

Saatlik standart fiyatı $0.40$, spot fiyatı $0.10$ olan bir makinenin teorik tasarrufu %75’tir. Fakat kesinti nedeniyle işlerin tekrar çalıştırılması gerekiyorsa gerçek maliyet değişir:

$$
C_{gerçek} = C_{spot} + C_{tekrar} + C_{operasyon}
$$

Yani yalnızca etiketteki fiyata bakmak, ucuz uçak bileti alıp bagaj ücretini unutmaya benzer.

| Özellik | Standart sunucu | Spot sunucu |
|---|---|---|
| Fiyat | Daha yüksek ve kararlı | Çok düşük, değişken olabilir |
| Kullanılabilirlik | Uzun süreli çalışmaya uygun | Sağlayıcı tarafından kesilebilir |
| İdeal iş yükü | Veritabanı, kritik API | Batch, render, test, veri işleme |
| Mimari beklenti | Kesinti toleransı önerilir | Kesinti toleransı zorunludur |

## Hangi işler spot için uygundur?

En iyi adaylar, küçük ve bağımsız parçalara bölünebilen işlerdir. Video dönüştürme, makine öğrenmesi eğitimi, CI/CD testleri, log analizi ve kuyruktan görev tüketen worker süreçleri buna örnektir. Bir görev yarıda kalırsa başka bir sunucu aynı görevi yeniden alabilmelidir.

Tek bir makinede çalışan kritik veritabanı ise kötü bir adaydır. Sunucu kapanınca hem hizmet hem de yerel disk üzerindeki veri kaybolabilir. Veritabanını standart kapasitede tutup yoğun hesaplama görevlerini spot worker’lara vermek daha güvenli bir hibrit yaklaşımdır.

## Kesintiye dayanıklı tasarımın kuralları

İlk kural, uygulamayı **stateless** tasarlamaktır. Oturum, görev durumu ve sonuçlar makinenin yerel diskinde değil; harici veritabanı, nesne depolama veya dağıtık önbellekte saklanmalıdır.

İkinci kural **checkpoint** kullanmaktır. Üç saatlik bir hesaplamanın her on dakikada bir ilerlemesini kaydetmesi, kesinti sonrasında sıfırdan başlamasını engeller. Checkpoint aralığı küçüldükçe kayıp iş azalır, ancak depolama maliyeti artar.

Üçüncü kural, görevleri bir mesaj kuyruğu üzerinden dağıtmaktır. Aşağıdaki Python benzeri worker, görevi işlerken sonucunu kalıcı depoya yazar; hata oluşursa mesajı onaylamayarak yeniden denenmesini sağlar:

```python
while True:
    task = queue.reserve(timeout=30)
    if task is None:
        continue

    try:
        result = process(task.payload)
        object_store.save(task.id, result)
        queue.ack(task)
    except Exception:
        queue.release(task, delay=60)
```

Burada `ack`, görevin başarıyla tamamlandığını bildirir. Sunucu `ack` çağrısından önce kapanırsa görünürlük süresi dolan görev başka bir worker’a gider. İşlemin iki kez çalışması mümkün olduğundan `process` fonksiyonu **idempotent**, yani tekrarlandığında sonucu bozmayan yapıda olmalıdır.

## Kesinti sinyalini değerlendirmek

Sağlayıcılar çoğunlukla kapanmadan kısa süre önce metadata servisi veya olay sistemi üzerinden bildirim gönderir. Uygulama bu sinyali yakaladığında yeni görev kabul etmeyi durdurmalı, mevcut ilerlemeyi kaydetmeli ve yük dengeleyiciden çıkmalıdır.

Kubernetes kullanılıyorsa spot düğümler etiketlenebilir; kritik pod’lar standart düğümlerde, toleranslı worker’lar spot havuzunda çalıştırılabilir. Birden fazla makine tipi ve erişilebilirlik bölgesi kullanmak da kapasite kesintilerinin aynı anda bütün sistemi vurma olasılığını azaltır.

Spot sunucular sihirli biçimde ucuz altyapı sağlamaz; dayanıklılık karşılığında indirim sunar. Kuyruklar, checkpoint’ler, otomatik ölçeklendirme, kalıcı depolama ve idempotent görevler doğru kurulduğunda ise fişi çekilen bir makine felaket değil, sıradan bir vardiya değişimi olur.

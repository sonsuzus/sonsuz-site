---
layout: post
title: "Fırlatmadan Önce Dijital Prova: Roket Yazılımında Hardware-in-the-Loop"
math: true
categories: 
  - Bilgi
tags: 
  - roket-yazılımı
  - hardware-in-the-loop
  - simülasyon
  - gömülü-sistemler
  - yazılım-testi
toc: true
image: /img/firlatmadan-once-dijital-90.png
---

Bir roketin uçuş bilgisayarına “Önce deneyelim, hata çıkarsa yeniden başlatırız” demek pek iyi bir mühendislik stratejisi değildir. Gerçek fırlatma pahalıdır, tekrarı zordur ve hata toleransı düşüktür. Hardware-in-the-Loop, yani HIL, gerçek elektronik donanımı sanal bir araçla buluşturarak yazılıma güvenli bir prova sahnesi sunar.


![firlatmadan-once-dijital-90](/img/firlatmadan-once-dijital-90.svg)

``

## HIL tam olarak neyi test eder?

HIL düzeninde uçuş bilgisayarı ve üzerinde çalışan yazılım gerçektir; aracın hareketi, çevresi ve bazı fiziksel bileşenleri ise modellerle temsil edilir. Simülatör, bilgisayara sensörlerden geliyormuş gibi veriler gönderir. Bilgisayarın ürettiği çıkışlar da modele geri aktarılır. Böylece tek yönlü veri oynatımından farklı olarak kapalı bir geri besleme döngüsü oluşur.

| Yaklaşım | Gerçek olan | Temel katkısı |
|---|---|---|
| SIL | Yazılım mantığı | Algoritmaları hızlı sınamak |
| HIL | İşlemci, yazılım ve seçilen arayüzler | Donanım-yazılım etkileşimini sınamak |
| Fiziksel sistem testi | Test edilen fiziksel bileşenler | Modelin kapsamadığı etkileri gözlemek |

SIL, Software-in-the-Loop anlamına gelir. Burada hedef donanım yerine bilgisayar ortamı kullanılır. HIL ise işlemci yükü, iletişim gecikmesi ve sürücü davranışı gibi “masada çalışıyordu!” sürprizlerini görünür kılar. İkisi rakip değil, birbirini tamamlayan test katmanlarıdır.

## Teorik temel: Model ve zaman aynı sahnede

Bir simülasyon modeli genel biçimde $x_{k+1}=f(x_k,u_k,w_k)$ ile gösterilebilir. Burada $x_k$ sistemin durumunu, $u_k$ bilgisayardan gelen çıkışları, $w_k$ ise çevresel etkileri veya bozucuları temsil eder. Sensör modeli de bu durumdan ölçüm üretir; ölçümlere gecikme, gürültü ve çözünürlük sınırları eklenebilir.

HIL için doğru değer üretmek kadar doğru zamanda üretmek de önemlidir. Sabit adımlı bir döngüde kabaca şu bütçe korunmalıdır:

$$T_{model}+T_{comm}+T_{io}<\Delta t$$

Yani model hesaplama, haberleşme ve giriş-çıkış işlemleri ayrılan zaman adımına sığmalıdır. Ancak ortalama süre yeterli değildir: En kötü gecikme ve zamanlama değişkenliği de izlenmelidir. Simülasyon sürekli yetişemiyorsa test, gerçek donanım davranışı hakkında yanıltıcı sonuçlar verebilir.

## Sanal araç, gerçek bağlantılar

Tipik düzenek; gerçek uçuş bilgisayarı, gerçek zamanlı simülatör, arayüz donanımı ve kayıt sisteminden oluşur. Arayüz katmanı dijital mesajları veya analog sinyalleri hedef bilgisayarın beklediği biçime dönüştürür. Paket içeriği kadar elektriksel seviyeler ve zaman damgaları da önemlidir.

Tehlikeli eyleyiciler yerine izole edilmiş yükler veya güvenli benzetimler kullanılmalıdır. Amaç motor çalıştırmak değil, bilgisayarın kararlarını gözlemlemektir. Hangi bileşenlerin gerçek, hangilerinin benzetim olduğu test raporunda açıkça belirtilmelidir.

## Hataları davet edin, sonuçları ölçün

Başarılı senaryonun yanında arızalı senaryolar da gerekir. Her arıza için beklenen davranış önceden tanımlanmalıdır; aksi hâlde renkli grafikler yalnızca pahalı bir ekran koruyucuya dönüşür.

| Enjekte edilen durum | Kontrol edilen davranış |
|---|---|
| Geçersiz sensör verisi | Veri kalitesi bilgisinin işlenmesi |
| Gecikmiş mesaj | Zaman aşımı ve hata kaydı |
| Tekrarlanan paket | Eski verinin ayırt edilmesi |
| Yoğun iletişim trafiği | Görev sürelerinin korunması |

Kabul ölçütleri; tepki süresi, kayıp paket sayısı ve gereksinimle eşleştirilmiş durum geçişleri olabilir. Test girdileri, yazılım sürümü ve model parametreleri kaydedilirse aynı hata yeniden üretilebilir. Rastgele senaryolarda kullanılan tohum değeri de saklanmalıdır.

## Python ile kavramsal bir test akışı

Aşağıdaki örnekte `bench` gerçek karta bağlanan test arayüzünü, `plant` ise fiziksel sistem modelini temsil eder. Bunlar hazır kütüphaneler değildir; kullanılan düzeneğe göre uygulanması gereken soyut arayüzlerdir. Örnek, kısa süreli sıcaklık verisi geçersizliği enjekte eder.

```python
from time import monotonic, sleep


def run_case(bench, plant, steps=200, dt=0.01):
    deadline = monotonic()
    trace = []

    for k in range(steps):
        t = k * dt
        sensors = dict(plant.sample())
        if 0.5 <= t < 0.6:
            sensors["temperature_valid"] = False

        bench.send_sensors(sensors, timestamp=t)
        outputs = bench.read_outputs(timeout=dt / 2)
        plant.step(outputs, dt)
        trace.append((t, outputs))

        deadline += dt
        remaining = deadline - monotonic()
        if remaining <= 0:
            raise RuntimeError("Zaman bütçesi aşıldı")
        sleep(remaining)

    return trace
```

Döngü, sensör verisini gönderir, kartın çıkışını toplar ve modeli ilerletir. Birikimli son tarih kullanılması zaman kaymasını azaltır. Bununla birlikte standart Python ve `sleep`, kesin gerçek zaman garantisi vermez; örnek üretim düzeneği değil, akışı açıklayan bir iskelettir. Gerçek testte kayıtların ayrıca otomatik doğrulayıcılardan geçirilmesi gerekir.

## HIL güçlüdür, ama sihir değildir

Model yanlışsa test kusursuz görünse bile sonuç yanlış olabilir. Bu nedenle modeller deneysel verilerle doğrulanmalı, belirsizlikler belgelenmeli ve farklı koşullar taranmalıdır. HIL; titreşim, elektromanyetik uyumluluk veya gerçek fiziksel sistem testlerinin yerine geçmez. En büyük kazancı, pahalı denemelerden önce hataları tekrarlanabilir biçimde yakalamaktır: Roketi değil, önce varsayımlarımızı havaya uçururuz.

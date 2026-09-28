---
layout: post
title: "APIC Sahne Arkası: Çok Çekirdekli Sistemlerde Kesme Dağıtımı"
math: true
categories: 
  - Bilgi
tags: 
  - apic
  - kesmeler
  - çok çekirdek
  - işletim sistemleri
  - donanım
  - linux
toc: true
image: /img/apic-sahne-arkasi-38.png
---

Fare düğmesine bastığınızda işlemcilerin hep bir ağızdan “Ben bakarım!” diye bağırdığını düşünebilirsiniz. Gerçekte donanım, işletim sistemi ve **Gelişmiş Programlanabilir Kesme Denetleyicisi (APIC)** birlikte çalışarak sinyalin hangi çekirdeğe gönderileceğini belirler. Bu mekanizma yalnızca kullanıcı girişlerini değil; ağ paketlerini, disk işlemlerini ve zamanlayıcı olaylarını da düzenleyen görünmez bir trafik polisidir.
``
## Kesme neden dağıtılmalı?

Bir aygıt işlemcinin ilgilenmesini istediğinde bir **kesme isteği (IRQ)** üretir. Tek çekirdekli bir makinede hedef bellidir. Çok çekirdekli sistemde ise bütün kesmeleri aynı çekirdeğe göndermek darboğaz yaratır.

Bir çekirdeğin kesmeler için harcadığı yaklaşık işlem yükünü şöyle gösterebiliriz:

$$L_i = \sum_{k=1}^{n} r_k \times c_k$$

Burada $L_i$, $i$ çekirdeğinin yükü; $r_k$, bir kesme kaynağının saniyedeki olay sayısı; $c_k$ ise olayı işleme maliyetidir. Amaç, yükü çekirdekler arasında dengelerken önbellek yerelliğini ve uygulama gecikmesini de korumaktır.

## APIC ailesinin oyuncuları

Klasik PIC yalnızca az sayıda IRQ hattını yönetebiliyordu. APIC mimarisi daha fazla kesme vektörü, çoklu işlemci desteği ve esnek hedef seçimi sundu.

| Bileşen | Konum | Görevi |
|---|---|---|
| Local APIC | Her mantıksal işlemcide | Kesme kabul eder, önceliklendirir ve EOI işler |
| I/O APIC | Anakart/yonga seti tarafında | Fiziksel IRQ hatlarını APIC hedeflerine yönlendirir |
| MSI/MSI-X | PCIe aygıt mekanizması | Kesme yerine özel bir bellek yazma işlemi gönderir |
| Interrupt Remapping | IOMMU tarafında | Kesme hedeflerini doğrular ve güvenli biçimde yeniden eşler |

**xAPIC**, hedefleri APIC kimlikleriyle belirlerken kayıtlarına bellek eşlemeli erişim kullanır. Daha yeni **x2APIC** ise genişletilmiş kimlik alanı ve MSR tabanlı erişim sayesinde çok daha fazla mantıksal işlemciyi destekler.

## Hedef çekirdek nasıl seçiliyor?

I/O APIC yönlendirme tablosundaki her kayıt; kesme vektörünü, hedefi, tetikleme biçimini ve teslim modunu içerir. **Fixed** modunda kesme belirli bir APIC kimliğine gider. **Lowest Priority** modunda ise uygun hedef kümesi içinden öncelik durumu elverişli olan işlemci seçilebilir.

Modern ağ kartları çoğunlukla **MSI-X** kullanır. Kart, birden fazla kesme vektörü oluşturabilir; işletim sistemi de her alım-gönderim kuyruğunu farklı çekirdeğe bağlayabilir:

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Tek çekirdeğe sabitleme | İyi önbellek yerelliği | Yoğun trafikte darboğaz |
| Çekirdeklere dağıtma | Yüksek paralellik | Önbellek ve senkronizasyon maliyeti |
| NUMA uyumlu dağıtma | Bellek erişim gecikmesi düşer | Yapılandırması daha karmaşıktır |

Örneğin ağ kuyruğu 0 çekirdek 2’ye, kuyruk 1 çekirdek 3’e atanabilir. Paket işleme uygulaması da aynı çekirdeklerde çalıştırılırsa veriler önbellekte sıcak kalır.

## Linux üzerinde kesme yakınlığı

Linux, her IRQ için bir çekirdek maskesi sunar. Aşağıdaki komutlar önce kesmeleri listeler, ardından 44 numaralı IRQ’yu maske değeri `4`, yani çekirdek 2 ile sınırlar:

```bash
# IRQ sayaçlarını ve aygıt adlarını görüntüle
grep -E 'CPU|eth|xhci' /proc/interrupts

# 0b0100 maskesi: kesmeyi yalnızca CPU 2 alır
echo 4 | sudo tee /proc/irq/44/smp_affinity

# Çekirdek listesini daha okunabilir biçimde doğrula
cat /proc/irq/44/smp_affinity_list
```

Gerçek IRQ numarası sistemden sisteme değişir. Ayrıca `irqbalance` hizmeti yükü otomatik dağıttığından elle yapılan ayarı daha sonra değiştirebilir.

## Fare tıklamasından ağ paketine

USB fare tıklaması önce USB denetleyicisine ulaşır. Denetleyici bir kesme üretir; I/O APIC veya MSI mekanizması bunu seçilen Local APIC’e yollar. İşlemci mevcut işini uygun noktada durdurur, kesme işleyicisini çalıştırır ve sonunda **EOI** bildirerek işlemi tamamlar.

Ağ kartında süreç benzerdir ancak saniyede milyonlarca olay oluşabilir. Bu yüzden MSI-X kuyrukları, kesme birleştirme ve çekirdek yakınlığı kritik hâle gelir. Kısacası APIC yalnızca “hangi çekirdek?” sorusunu yanıtlamaz; sistemin gecikme, verim ve ölçeklenebilirlik dengesini de belirler.

![apic-sahne-arkasi-38](/img/apic-sahne-arkasi-38.svg)


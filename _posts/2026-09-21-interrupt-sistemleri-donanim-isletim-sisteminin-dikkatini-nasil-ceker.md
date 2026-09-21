---
layout: post
title: "Interrupt Sistemleri: Donanım İşletim Sisteminin Dikkatini Nasıl Çeker?"
math: true
categories: 
  - Bilgi
tags: 
  - interrupt
  - işletim sistemi
  - donanım
  - kesme
  - cpu
  - çekirdek
toc: true
---

Bilgisayarınızın işlemcisi milyonlarca komutu yürütürken klavyede bir tuşa bastığınızı nasıl fark eder? İşlemcinin sürekli “Klavye hazır mı, ağdan veri geldi mi?” diye sorması mümkün olsa da oldukça verimsizdir. Interrupt, yani kesme sistemi, donanımın işlemciye nazikçe değil, adeta omzuna dokunarak “Önemli bir olay oldu!” demesini sağlar.

``

## Sürekli sormak mı, haber beklemek mi?

Donanımla iletişim kurmanın basit yöntemi **polling** yaklaşımıdır. CPU, aygıtın durum yazmacını belirli aralıklarla kontrol eder. Interrupt yaklaşımında ise CPU diğer işlerini sürdürür; aygıt yalnızca gerektiğinde bir kesme sinyali üretir.

| Özellik | Polling | Interrupt |
|---|---|---|
| CPU kullanımı | Sürekli kontrol nedeniyle yüksek | Olay gerçekleşene kadar düşük |
| Tepki süresi | Kontrol sıklığına bağlı | Genellikle hızlı |
| Uygulama kolaylığı | Daha basit | Ek donanım ve çekirdek desteği gerekir |
| Uygun senaryo | Çok sık gerçekleşen olaylar | Düzensiz donanım olayları |

Polling sırasında her kontrolün maliyeti $C$, saniyedeki kontrol sayısı $f$ ise yaklaşık işlem yükü şöyle düşünülebilir:

$$Yük = C \times f$$

Olaylar seyrekse bu kontrollerin çoğu boşa gider. Interrupt sisteminin temel kazancı tam olarak budur.

## Kesme yolculuğu

Örneğin ağ kartına yeni bir paket geldiğinde süreç genel olarak şu adımlarla ilerler:

1. Aygıt, interrupt hattı üzerinden bir sinyal üretir.
2. Kesme denetleyicisi sinyali alır ve önceliğini değerlendirir.
3. Denetleyici, CPU’ya uygun kesme numarasını bildirir.
4. CPU yürüttüğü komutu tamamlar ve mevcut bağlamı saklar.
5. İşletim sistemi ilgili **Interrupt Service Routine** (ISR) koduna geçer.
6. ISR aygıtın durumunu okur, gerekli veriyi alır ve kesmeyi onaylar.
7. Saklanan bağlam geri yüklenir; yarıda kalan iş devam eder.

Buradaki “bağlam”; program sayacı, bayraklar ve bazı işlemci yazmaçları gibi bilgileri kapsar. CPU’nun kesmeye geçiş süresine **interrupt latency** denir:

$$T_{latency} = T_{algılama} + T_{bağlam} + T_{yönlendirme}$$

Gerçek zamanlı sistemlerde bu sürenin kısa olmasının yanında öngörülebilir olması da önemlidir.

## Kesme denetleyicisi ne yapar?

Eski sistemlerde PIC, modern çok çekirdekli makinelerde ise çoğunlukla APIC benzeri denetleyiciler kullanılır. Bu birimler kesmeleri önceliklendirir, maskeleyebilir ve belirli bir CPU çekirdeğine yönlendirebilir. Böylece fare hareketi ile kritik bir disk hatası aynı önemde değerlendirilmez.

| Kesme türü | Davranış | Örnek |
|---|---|---|
| Kenar tetiklemeli | Sinyaldeki değişim olayı bildirir | Tuşa basılması |
| Seviye tetiklemeli | Hat belirli seviyede kaldıkça aktiftir | Ağ veya disk aygıtı |
| Maskelenebilir | CPU tarafından geçici olarak engellenebilir | Zamanlayıcı kesmesi |
| Maskelenemez | Kritik olduğu için ertelenemez | Donanım arızası |

## Basitleştirilmiş bir ISR

Aşağıdaki C benzeri kod, ağ kartı kesmesinin temel mantığını gösterir:

```c
void network_isr(void) {
    unsigned int status = read_device_status();

    if (status & PACKET_READY) {
        copy_packet_to_kernel_buffer();
        schedule_network_processing();
    }

    acknowledge_interrupt();
}
```

ISR önce aygıt durumunu okur, hazır paketi güvenli bir çekirdek tamponuna taşır ve ağır işlemleri daha sonra çalışacak göreve bırakır. Son satır kesmenin işlendiğini denetleyiciye bildirir. Bu onay verilmezse aygıt aynı kesmeyi tekrar tekrar üretebilir.

ISR’lerin kısa tutulması kritik bir tasarım kuralıdır. Paket çözümleme, dosya yazma veya uzun döngüler gibi işler ISR içinde yapılırsa diğer kesmeler gecikebilir. İşletim sistemleri bu nedenle işi genellikle **üst yarı** ve **alt yarı** olarak böler: üst yarı acil donanım işlemlerini, alt yarı ertelenebilir işleri yürütür.

Sonuç olarak interrupt sistemi, donanım ile işletim sistemi arasında hızlı bir alarm mekanizmasıdır. CPU’yu gereksiz sorgulamalardan kurtarır; ancak öncelik, eşzamanlılık, bağlam saklama ve gecikme gibi yeni sorunlar getirir. Bilgisayarın sakin görünmesinin ardında aslında durmadan çalan, dikkatle yönetilen küçük dijital alarmlar vardır.

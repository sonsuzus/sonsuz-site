---
layout: post
title: "Interrupt-Driven Embedded Programming: Mikrodenetleyicinin Olaylarla Dansı"
math: true
categories: 
  - Bilgi
tags: 
  - embedded
  - interrupt
  - mikrodenetleyici
  - c
  - isr
  - gerçek-zamanlı-sistemler
toc: true
image: /img/interrupt-driven-embedded-28.png
---

Bir mikrodenetleyicinin sürekli düğmeye basılıp basılmadığını kontrol ettiğini düşünün. Biraz, kapının önünde bekleyip zil çalacak mı diye saniyede binlerce kez bakmaya benzer! Interrupt-driven, yani kesme güdümlü programlama, mikrodenetleyicinin başka işlerle uğraşırken önemli bir olay gerçekleştiğinde haberdar edilmesini sağlar. Böylece işlemci zamanı daha verimli kullanılır ve olaylara çok daha hızlı tepki verilir.

``

## Kesme nedir?

Kesme, donanım veya yazılım tarafından işlemciye gönderilen bir **“Şu an ilgilenmen gereken bir olay var!”** sinyalidir. Bir GPIO pinindeki seviye değişimi, zamanlayıcının taşması, UART üzerinden veri gelmesi veya ADC dönüşümünün tamamlanması kesme üretebilir.

İşlemci normal programı çalıştırırken kesme geldiğinde genel olarak şu adımlar gerçekleşir:

1. Mevcut komut tamamlanır.
2. Program sayacı ve gerekli işlemci durumu saklanır.
3. Kesme vektör tablosundan ilgili fonksiyonun adresi bulunur.
4. **Interrupt Service Routine** (ISR) çalıştırılır.
5. Saklanan durum geri yüklenir ve ana programa dönülür.

Kesmenin algılanmasından ISR içerisindeki ilk komutun çalışmasına kadar geçen süreye **kesme gecikmesi** denir. Yaklaşık olarak:

$$T_{tepki} = T_{gecikme} + T_{ISR}$$

Burada $T_{ISR}$, kesme fonksiyonunun çalışma süresidir. Gerçek zamanlı bir sistemde bu toplam süre, olayın izin verdiği maksimum süreden küçük olmalıdır:

$$T_{tepki} < T_{son\_tarih}$$

Aksi hâlde işlemci olayı yakalasa bile cevabı geç kalabilir.

## Polling ve interrupt karşılaştırması

| Özellik | Polling | Interrupt |
|---|---|---|
| Olay kontrolü | Sürekli sorgulanır | Olay işlemciyi haberdar eder |
| CPU kullanımı | Genellikle yüksektir | Daha verimlidir |
| Tepki süresi | Döngü hızına bağlıdır | Genellikle daha kısadır |
| Program yapısı | Basit başlayabilir | Eşzamanlılık dikkat ister |
| Güç tüketimi | Daha yüksek olabilir | Uyku modlarına uygundur |

Polling tamamen kötü değildir. Çok basit veya sürekli veri işleyen sistemlerde mantıklı olabilir. Ancak pille çalışan sensör düğümlerinde işlemci uykuya geçip bir kesmeyle uyanabildiği için interrupt yaklaşımı büyük avantaj sağlar.

## Basit bir düğme kesmesi

Aşağıdaki genel C örneğinde düğme kesmesi ağır işi doğrudan yapmaz; yalnızca ana döngüye bir olay olduğunu bildirir:

```c
#include <stdint.h>
#include <stdbool.h>

volatile bool button_event = false;

void GPIO_IRQHandler(void)
{
    if (gpio_interrupt_pending()) {
        gpio_clear_interrupt();
        button_event = true;
    }
}

int main(void)
{
    gpio_button_interrupt_init();

    while (1) {
        if (button_event) {
            button_event = false;
            toggle_led();
        }

        enter_sleep_mode();
    }
}
```

`volatile`, değişkenin ISR gibi normal akışın dışında değiştirilebileceğini derleyiciye bildirir. Böylece derleyici değeri bir kez okuyup sonsuza kadar önbellekte tutmaya kalkmaz. Ancak önemli bir ayrıntı var: `volatile`, işlemleri otomatik olarak **atomik** veya thread-safe yapmaz.

## ISR yazmanın altın kuralları

ISR mümkün olduğunca kısa tutulmalıdır. Kesme içinde uzun döngüler çalıştırmak, gecikme fonksiyonları çağırmak, büyük hesaplamalar yapmak veya bloklayan I/O kullanmak diğer olayların gecikmesine neden olur. En iyi yaklaşım, bayrak ayarlamak ya da veriyi küçük bir kuyruğa bırakıp asıl işi ana döngüye veya bir RTOS görevine devretmektir.

Birden fazla kesme aynı anda oluşursa **öncelik** mekanizması devreye girer. Motor kontrolü gibi kritik bir zamanlayıcı kesmesi, kullanıcı düğmesinden daha yüksek öncelikli olabilir. Yine de aşırı yüksek öncelikli ve uzun bir ISR, düşük öncelikli kesmeleri aç bırakabilir.

Mekanik düğmeler ayrıca tek basışta çok sayıda elektriksel geçiş üretir. Buna **bounce** denir. Donanımsal filtre, zamanlayıcı veya yazılımsal debounce uygulanmazsa kahraman mikrodenetleyicimiz bir basışı küçük bir davul solosu sanabilir.

Sonuç olarak interrupt-driven programlama, olaylara hızlı tepki veren ve düşük güç tüketen gömülü sistemlerin temelidir. Başarının sırrı kesmeleri yalnızca acil bildirim mekanizması olarak kullanmak, ISR’leri kısa tutmak ve paylaşılan verileri dikkatle yönetmektir.

![interrupt-driven-embedded-28](/img/interrupt-driven-embedded-28.svg)


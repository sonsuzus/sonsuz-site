---
layout: post
title: "Mikrodenetleyicide RTOS Mantığıyla Görev Zamanlayıcı ve Öncelikli Kesme Yöneticisi"
math: true
categories: 
  - Proje
tags: 
  - mikrodenetleyici
  - rtos
  - gömülü sistemler
image: /img/mikrodenetleyicide-rtos-mantigiyla-17.png
toc: true
---

![mikrodenetleyicide-rtos-mantigiyla-17](/img/mikrodenetleyicide-rtos-mantigiyla-17.svg)


Bir mikrodenetleyicide aynı anda ekran güncellemek, sensör okumak, haberleşme paketi göndermek ve motor kontrol etmek isterseniz, `delay()` çağrılarıyla dolu bir program kısa sürede kontrolden çıkar. Gerçek zamanlı işletim sistemi (RTOS) prensipleri, bu karmaşayı görevleri bölerek, zamanlayarak ve kritik olaylara doğru önceliği vererek yönetir. Bu yazıda tam teşekküllü bir RTOS yazmak yerine, onun temel fikirlerini taşıyan küçük bir görev zamanlayıcı ve öncelikli kesme yöneticisi tasarlayacağız.
``

Gerçek zamanlılık, kodun yalnızca “hızlı” çalışması değildir; işin **öngörülebilir bir son teslim zamanında** tamamlanmasıdır. Bir motorun aşırı akım koruması 1 ms geç çalışırsa, ortalama işlemci kullanımı düşük olsa bile sistem başarısız sayılabilir. Bu nedenle tasarımın temel sorusu şudur: “Hangi iş, en geç ne zaman bitmeli?”

Bir periyodik görev için basit zamanlama koşulu şöyle ifade edilebilir:

$$U = \sum_{i=1}^{n}\frac{C_i}{T_i}$$

Burada $C_i$ görevin en kötü durum çalışma süresi, $T_i$ ise periyodudur. Toplam işlemci kullanımı $U$ büyüdükçe görevlerin son teslim zamanını kaçırma riski artar. Pratikte kesme maliyeti, bağlam değiştirme ve güvenlik payı da hesaba katılmalıdır.

| Kavram | Anlamı | Örnek |
|---|---|---|
| Periyot ($T$) | Görevin tekrar aralığı | Sensörü her 10 ms okumak |
| Çalışma süresi ($C$) | Görevin CPU’da kaldığı süre | Okumanın 200 µs sürmesi |
| Deadline | İşin bitmesi gereken an | PWM güncellemesinin 1 ms içinde bitmesi |
| Jitter | Başlangıç zamanındaki sapma | Görevin 10 ms yerine 10.3 ms’de çalışması |

## Kooperatif görev zamanlayıcı

İlk katmanımız, bir donanım zamanlayıcısının ürettiği sistem tikini kullanan kooperatif bir scheduler’dır. Kooperatif yaklaşımda görevler CPU’yu kendileri bırakır; yani hiçbir görev uzun süren, bloklayıcı işlem yapmamalıdır. Bu model küçük RAM’li mikrodenetleyiciler için şaşırtıcı derecede etkilidir.

```c
volatile uint32_t tick_ms = 0;

typedef struct {
    void (*run)(void);
    uint32_t period_ms;
    uint32_t next_run;
} Task;

void SysTick_Handler(void) {
    tick_ms++;
}

void scheduler_run(Task *tasks, uint8_t count) {
    for (uint8_t i = 0; i < count; i++) {
        if ((int32_t)(tick_ms - tasks[i].next_run) >= 0) {
            tasks[i].run();
            tasks[i].next_run += tasks[i].period_ms;
        }
    }
}
```

`next_run += period_ms` kullanımı önemlidir. Eğer bunun yerine `next_run = tick_ms + period_ms` yazarsak, görevin kendi çalışma süresi her turda periyoda eklenir ve zamanla kayma oluşur. İlk yaklaşım, görev geç kalsa bile teorik zaman çizelgesine yeniden yaklaşır.

Örnek görev tablosu şu şekilde kurulabilir:

```c
Task tasks[] = {
    { read_sensor,  10, 10 },
    { update_pwm,    1,  1 },
    { send_telemetry, 100, 100 }
};

int main(void) {
    timer_init_1ms();
    while (1) {
        scheduler_run(tasks, 3);
        idle_sleep();
    }
}
```

## Öncelikli kesme yöneticisi

Kesme (interrupt), işlemcinin normal akışını kritik bir olay için durdurmasıdır. Fakat her kesmeye en yüksek önceliği vermek, “acil” kelimesini herkes için kullanmaya benzer: sonunda hiçbir şey gerçekten acil değildir. NVIC destekli ARM mikrodenetleyicilerinde daha küçük sayısal değer genellikle daha yüksek öncelik demektir.

| Kesme kaynağı | Önerilen öncelik | Gerekçe |
|---|---:|---|
| Aşırı akım / acil durdurma | 0 | Donanım ve kullanıcı güvenliği |
| PWM zamanlayıcısı | 1 | Motor kontrol kararlılığı |
| ADC dönüşüm tamamlandı | 2 | Hızlı kontrol döngüsü |
| UART alımı | 3 | Veri kaybını önleme |
| SysTick | 4 | Genel zaman tabanı |

```c
void interrupt_manager_init(void) {
    NVIC_SetPriority(OVERCURRENT_IRQn, 0);
    NVIC_SetPriority(PWM_TIMER_IRQn,   1);
    NVIC_SetPriority(ADC_IRQn,         2);
    NVIC_SetPriority(USART1_IRQn,      3);
    NVIC_SetPriority(SysTick_IRQn,     4);
}

void USART1_IRQHandler(void) {
    uint8_t byte = USART1->RDR;
    ring_buffer_push(&rx_buffer, byte);
}
```

Kesme yordamlarında ağır hesap, `printf`, bekleme döngüsü veya dinamik bellek ayırma yapılmamalıdır. UART örneğinde kesme yalnızca baytı ring buffer’a taşır; paketi çözümleme işi düşük öncelikli görevde yapılır. Böylece yüksek öncelikli kesmeler kısa sürer ve gecikme zinciri büyümez.

Son olarak ölçmeden gerçek zamanlı sistem tasarlamayın: GPIO piniyle görev sürelerini osiloskopta izleyin, en kötü durum çalışma süresini ölçün ve kesme iç içe geçmelerini test edin. Küçük scheduler’ınız bu disiplinle, daha büyük bir RTOS’a geçmeden önce sağlam bir mühendislik laboratuvarına dönüşür.

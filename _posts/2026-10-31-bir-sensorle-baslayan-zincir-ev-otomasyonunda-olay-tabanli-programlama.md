---
layout: post
title: "Bir Sensörle Başlayan Zincir: Ev Otomasyonunda Olay Tabanlı Programlama"
math: true
categories: 
  - Bilgi
tags: 
  - ev otomasyonu
  - olay tabanlı programlama
  - python
  - sensörler
  - asenkron programlama
  - mqtt
toc: true
image: /img/bir-sensorle-baslayan-18.png
---

Gece koridora çıktığınızda lamba yanıyor, ardından telefonunuza aydınlatmanın açıldığı bilgisi geliyor. Siz yalnızca yürüdünüz; eviniz ise küçük bir yazılım orkestrası gibi çalıştı. Bu davranışın arkasında, cihazları sürekli sorgulamak yerine değişikliklere tepki veren olay tabanlı programlama bulunur. Gelin, tek bir sensör sinyalinin nasıl kontrollü bir otomasyon zincirine dönüştüğünü keşfedelim.

``

## Olay nedir, komuttan farkı ne?

**Olay**, gerçekleşmiş bir durumun kaydıdır: “Hareket algılandı.” **Komut** ise yapılması istenen iştir: “Lambayı aç.” Bu ayrım önemlidir; hareket sensörü lambanın nasıl çalıştığını bilmek zorunda değildir. Yalnızca gözlemini yayınlar, otomasyon kuralları da uygun komutları üretir.

Tipik mimaride üç rol vardır: olayı üreten sensör, mesajı taşıyan olay veri yolu ve mesajı işleyen tüketiciler. MQTT kullanılan sistemlerde aracı sunucu mesajları abonelere iletir. Bununla birlikte, MQTT tek başına otomasyon kurallarını değerlendirmez; bu görev uygulamanıza veya otomasyon platformuna aittir.

| Yaklaşım | Çalışma biçimi | Temel özellik |
|---|---|---|
| Periyodik sorgulama | Sensöre düzenli aralıklarla sorar | Tepki süresi sorgulama aralığına bağlıdır |
| Olay tabanlı model | Sensör değişikliği bildirir | Gereksiz sorgulamayı azaltabilir |
| Zamanlanmış görev | Belirlenen saatte çalışır | Sensör değişimi gerektirmez |

Bu yöntemler rakip değil, takım arkadaşıdır. Örneğin hareket olayı lambayı açarken, zamanlanmış bir görev gecenin sonunda açık kalan lambaları kapatabilir.

## Zincirin matematiği: olay, koşul ve durum

Bir kuralı “olay geldi, koşul doğruysa eylemi gerçekleştir” şeklinde düşünebiliriz. Hareketi $H$, gece koşulunu $G$, lambayı açma kararını $L$ ile gösterirsek:

$$L = H \land G$$

Ancak yalnızca koşulları değerlendirmek yetmez. Lambanın mevcut durumunu da bilmeliyiz. Durum geçişini $S_{t+1} = f(S_t, E_t)$ olarak yazabiliriz: yeni durum, önceki durum ve gelen olay tarafından belirlenir.

Lamba zaten açıksa tekrar açma komutu göndermemek, gereksiz işlemleri azaltır. Üstelik zincirin bir sonraki halkasını yalnızca gerçek durum değiştiğinde tetiklememizi sağlar. Böylece eviniz, aynı düğmeye heyecanla yüz kere basan bir robot gibi davranmaz.

## Python ile küçük bir olay zinciri

Aşağıdaki örnek, sensör olayını bir kuyruğa bırakır. Hareket işleyicisi gece koşulunu değerlendirir; lamba açıldığında yeni bir olay üretir. İkinci işleyici de telefon bildirimini temsil eden çıktıyı oluşturur. Gerçek cihaz bağlantıları yerine simülasyon kullanıyoruz.

```python
import asyncio
from dataclasses import dataclass

@dataclass
class Event:
    kind: str
    data: dict

bus = asyncio.Queue()
state = {"light": False}

async def on_motion(event):
    hour = event.data["hour"]
    is_night = hour >= 22 or hour < 6
    if is_night and not state["light"]:
        state["light"] = True
        print("Koridor lambası açıldı.")
        await bus.put(Event("light.changed", {"on": True}))

async def on_light(event):
    if event.data["on"]:
        print("Telefon bildirimi: Koridor aydınlatıldı.")

handlers = {
    "motion.detected": on_motion,
    "light.changed": on_light,
}

async def main():
    await bus.put(Event("motion.detected", {"hour": 23}))
    while not bus.empty():
        event = await bus.get()
        try:
            handler = handlers.get(event.kind)
            if handler:
                await handler(event)
        finally:
            bus.task_done()

asyncio.run(main())
```

`handlers` sözlüğü, olay türlerini ilgili fonksiyonlarla eşleştirir. Kuyruk ise üretici ile tüketiciyi birbirinden ayırır. Bu örnekte işleyiciler sırayla beklenir; `async` kullanılması bütün işlemlerin otomatik olarak paralel çalıştığı anlamına gelmez. Ayrıca döngü kuyruk boşalınca biter; sürekli çalışan uygulamada yeni olaylar `await bus.get()` ile beklenir.

Gerçek lambada durum değişikliğini, komut gönderildiği anda değil cihazdan doğrulama geldiğinde yayınlamak daha güvenilirdir. Aksi hâlde bağlantısı kopmuş bir lambayı yazılımda açık sanabilirsiniz.

## Zinciri güvenilir tutmak

Olay tabanlı sistemlerin eğlenceli tarafı bağlantı kurmaktır; zor tarafı ise bağlantıları kontrol altında tutmaktır.

- **Tekrarlanan mesajlar:** Olay kimliği ve idempotent işleyiciler kullanın. Aynı olayın yeniden gelmesi sonucu değiştirmemelidir.
- **Sonsuz döngüler:** Lambanın değişimi sensör kuralını yeniden tetikliyorsa döngü oluşabilir. Kaynak bilgisi ve açık geçiş kuralları ekleyin.
- **Sensör titreşimi:** Çok kısa aralıklarla gelen sinyalleri filtrelemek için debounce uygulayın. Hareketli bir perdeyi misafir sanmayın!
- **Bağlantı kesintileri:** Yeniden deneme, zaman aşımı ve durum uzlaştırma mekanizmaları tasarlayın. Tek bir mesajı mutlak gerçek kabul etmeyin.
- **Güvenlik:** MQTT erişimini kimlik doğrulama ve konu bazlı yetkilerle sınırlandırın; kritik cihazlarda manuel kontrolü koruyun.

Sonuç olarak iyi otomasyon, yalnızca cihazları bağlamak değildir. Olayın anlamını, koşullarını ve oluşturduğu durum değişikliklerini açıkça tanımlamaktır. Bu temel sağlam olduğunda, tek bir sensör evinizin geri kalanıyla düzenli ve anlaşılır bir sohbet başlatabilir.

![bir-sensorle-baslayan-18](/img/bir-sensorle-baslayan-18.svg)


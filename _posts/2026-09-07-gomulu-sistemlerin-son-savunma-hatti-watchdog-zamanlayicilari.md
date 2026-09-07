---
layout: post
title: "Gömülü Sistemlerin Son Savunma Hattı: Watchdog Zamanlayıcıları"
math: true
categories: 
  - Bilgi
tags: 
  - gömülü sistemler
  - watchdog
  - mikrodenetleyici
toc: true
---

Bir mikrodenetleyici çalışırken kodun sonsuz döngüye girmesi, bir çevre biriminin yanıt vermemesi veya beklenmeyen bir bellek hatası tüm sistemi sessizce kilitleyebilir. İnsan müdahalesinin mümkün olmadığı otomobillerde, endüstriyel kontrol kartlarında ve uzaktaki IoT cihazlarında bu durum ciddi sonuçlar doğurur. Watchdog zamanlayıcısı, yazılımın hâlâ sağlıklı olduğunu düzenli olarak kanıtlamasını isteyen ve kanıt gelmezse sistemi otomatik olarak yeniden başlatan küçük ama etkili bir güvenlik mekanizmasıdır.
``
## Watchdog nasıl çalışır?

Watchdog, temel olarak belirli bir başlangıç değerinden sıfıra doğru sayan donanımsal bir zamanlayıcıdır. Program normal çalışırken bu sayacı periyodik olarak yeniler. Bu işleme **watchdog beslemek**, **kicklemek** veya **refresh etmek** denir. Sayaç sıfıra ulaşırsa watchdog, işlemcinin kontrolü kaybettiğini varsayarak reset sinyali üretir.

Watchdog zaman aşımı $T_w$, yazılımın en kötü durumdaki sağlıklı çalışma süresinden büyük seçilmelidir:

$$T_w > T_{görev} + T_{kesme} + T_{gecikme}$$

Örneğin ana döngü en fazla $80\,ms$, kesmeler $15\,ms$ ve beklenmeyen haberleşme gecikmesi $25\,ms$ sürüyorsa toplam süre $120\,ms$ olur. Bu sistem için $T_w = 200\,ms$ gibi güvenlik payı içeren bir değer seçilebilir. Çok kısa süre gereksiz resetlere, çok uzun süre ise arızanın geç fark edilmesine yol açar.

| Yaklaşım | Avantajı | Riski |
|---|---|---|
| Yazılımsal watchdog | Esnek ve kolay özelleştirilir | İşlemci tamamen kilitlenirse çalışamaz |
| Donanımsal watchdog | CPU hatalarında bile reset üretebilir | Yanlış yapılandırma reset döngüsü oluşturabilir |
| Bağımsız watchdog | Ayrı saat kaynağı sayesinde daha güvenilirdir | Zamanlama toleransları dikkatle hesaplanmalıdır |
| Pencereli watchdog | Çok erken ve çok geç beslemeyi algılar | Uygulama tasarımı daha karmaşıktır |

## Watchdog’u doğru yerde beslemek

Watchdog’u ana döngünün her turunda koşulsuz beslemek yaygın fakat tehlikeli bir hatadır. Program döngü içinde dönmeye devam ederken sensör okuma görevi veya haberleşme modülü kilitlenmiş olabilir. Watchdog beslenmeye devam ettiği için bu **kısmi kilitlenmeyi** fark edemez.

Daha güvenli yaklaşım, kritik görevlerin sağlık bayraklarını kontrol ettikten sonra sayacı yenilemektir:

```c
#include <stdbool.h>

bool sensor_ok = false;
bool communication_ok = false;
bool control_ok = false;

void main_loop(void)
{
    while (1) {
        sensor_ok = read_sensors();
        communication_ok = process_messages();
        control_ok = update_control_output();

        if (sensor_ok && communication_ok && control_ok) {
            watchdog_refresh();
        }

        run_diagnostics();
    }
}
```

Bu örnekte `watchdog_refresh()` yalnızca üç kritik işlem başarıyla tamamlandığında çağrılır. İşlevlerden biri kalıcı biçimde başarısız olursa sayaç yenilenmez ve donanım sistemi yeniden başlatır. Gerçek zamanlı işletim sistemlerinde benzer yöntem, her görevin ayrı bir yaşam sinyali üretmesiyle uygulanabilir.

## Pencereli watchdog neden daha sıkıdır?

Klasik watchdog yalnızca geç beslemeyi denetler. Pencereli watchdog ise besleme işleminin belirli bir zaman aralığında yapılmasını ister:

$$T_{min} < T_{besleme} < T_{max}$$

Kod beklenenden hızlı dönerek watchdog’u sürekli besliyorsa bu durum da bir arıza belirtisi olabilir. Örneğin önemli görevlerin yanlışlıkla atlanması ana döngüyü hızlandırabilir. Pencereli yapı hem geç hem de şüpheli derecede erken beslemeyi yakalar.

## Reset sonrasında ne yapılmalı?

Yeniden başlatma, hatayı ortadan kaldırmaz; yalnızca sistemi tekrar çalışabilir duruma getirir. Açılış kodu reset nedenini mikrodenetleyicinin durum yazmacından okumalı, kalıcı belleğe hata kaydı bırakmalı ve çıkışları güvenli başlangıç durumuna getirmelidir. Art arda oluşan watchdog resetleri sayılarak cihazın sonsuz açılış döngüsüne girmesi de önlenebilir. Belirli bir eşik aşıldığında güvenli mod, yedek firmware veya sınırlı çalışma modu etkinleştirilebilir.

Watchdog sihirli bir hata düzeltici değil, emniyet kemeridir: kazayı önlemeyebilir fakat sistemin yolda kontrolsüz biçimde kalmasını engeller. Bağımsız saat kaynağı, dikkatli zaman aşımı hesabı, anlamlı sağlık kontrolleri ve reset kayıtlarıyla kullanıldığında gömülü yazılımın dayanıklılığını büyük ölçüde artırır.

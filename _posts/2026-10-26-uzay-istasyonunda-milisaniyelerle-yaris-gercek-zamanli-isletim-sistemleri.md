---
layout: post
title: "Uzay İstasyonunda Milisaniyelerle Yarış: Gerçek Zamanlı İşletim Sistemleri"
math: true
categories: 
  - Bilgi
tags: 
  - rtos
  - uzay
  - iss
  - gömülü sistemler
  - zamanlama
  - güvenlik kritik sistemler
toc: true
image: /img/uzay-istasyonunda-milisaniyelerle-81.png
---

![uzay-istasyonunda-milisaniyelerle-81](/img/uzay-istasyonunda-milisaniyelerle-81.svg)


Dünya’dan yüzlerce kilometre uzakta ilerleyen bir uzay istasyonunda bilgisayarın birkaç saniyeliğine “donması”, masaüstündeki küçük bir aksaklığa benzemez. Atmosfer kontrolü, yönelim, enerji dağıtımı ve kenetlenme gibi görevlerde gecikme; ekipman kaybına, görevin tehlikeye girmesine veya astronotların yaşam destek koşullarının bozulmasına yol açabilir. Bu nedenle ISS gibi ortamlarda genel amaçlı yazılımların yanında deterministik davranabilen gerçek zamanlı sistemlerden yararlanılır.
``

## Gerçek zamanlı olmak, yalnızca hızlı olmak değildir

Gerçek zamanlı işletim sistemi veya **RTOS**, görevlerin sadece hızlı değil, belirlenen zaman sınırları içinde tamamlanmasını hedefler. Bir işlemin ortalama süresinin düşük olması yeterli değildir; en kötü durumda ne kadar gecikeceği de öngörülebilmelidir.

Bir görevin bitiş zamanı $C$, teslim süresi $D$ ile karşılaştırıldığında temel koşul şöyledir:

$$C \leq D$$

Buradaki teslim süresi kaçırılırsa sonucun etkisine göre sistemler üç gruba ayrılır:

| Sistem türü | Zaman sınırı kaçırılırsa | Uzay ortamından örnek |
|---|---|---|
| Sert gerçek zamanlı | Sonuç kabul edilemez | Acil valf kapatma |
| Sıkı gerçek zamanlı | Hesaplanan sonuç değersizleşir | Güncelliğini yitiren konum verisi |
| Yumuşak gerçek zamanlı | Kalite düşer, sistem çalışabilir | Mürettebat video aktarımı |

ISS tek bir bilgisayardan oluşmaz. Farklı dönemlerde geliştirilmiş, farklı sorumluluklara sahip çok sayıda bilgisayar, denetleyici, sensör ve veri yolu birlikte çalışır. Güvenlik açısından kritik kontrol döngüleri daha deterministik platformlarda yürütülürken kullanıcı arayüzleri veya deney yazılımları daha genel amaçlı sistemlerde çalışabilir.

## Zamanlayıcı sahnenin yönetmenidir

RTOS içindeki zamanlayıcı, işlemciyi hangi görevin ne zaman kullanacağını belirler. Öncelik tabanlı önleyici zamanlamada kritik bir görev hazır olduğunda daha düşük öncelikli görev durdurulabilir. Böylece örneğin sıcaklık kaydı beklerken basınç alarmı hemen işlenir.

Periyodik görevlerin yaklaşık işlemci kullanımı şu şekilde hesaplanabilir:

$$U = \sum_{i=1}^{n} \frac{C_i}{T_i}$$

Burada $C_i$ görevin çalışma süresi, $T_i$ ise tekrarlanma periyodudur. Kullanım oranının düşük olması tek başına garanti sağlamaz; kesmeler, paylaşılan kaynaklar ve görevler arası engelleme de en kötü durum analizine katılmalıdır.

Aşağıdaki sadeleştirilmiş C benzeri örnek, her 10 milisaniyede bir sensör okuyup güvenli sınırı denetleyen görevi gösterir:

```c
void pressure_task(void *arg) {
    TickType_t next = get_tick_count();

    while (true) {
        float pressure = read_pressure_sensor();

        if (pressure < MIN_PRESSURE) {
            send_emergency_event(pressure);
        }

        delay_until(&next, milliseconds_to_ticks(10));
    }
}
```

`delay_until`, görevi “10 milisaniye uyutmak” yerine sabit bir zaman çizelgesine bağlar. İşlem süresindeki küçük değişimler böylece üst üste eklenip periyot kaymasına dönüşmez. Gerçek uçuş yazılımında sensör doğrulama, yedek kanal karşılaştırması, zaman aşımı ve hata kaydı gibi ek katmanlar bulunur.

## Öncelik terslenmesi ve güvenilirlik

Düşük öncelikli bir görev ortak kaynağı kilitlerken yüksek öncelikli görev aynı kaynağı bekleyebilir. Araya orta öncelikli görevler girerse **öncelik terslenmesi** oluşur. RTOS’lar bunu öncelik mirası gibi protokollerle azaltır: Kilidi tutan görev geçici olarak daha yüksek öncelik kazanır ve kaynağı hızla serbest bırakır.

Uzay sistemlerinde güvenilirlik yalnızca zamanlamadan ibaret değildir. Radyasyon bit hatalarına neden olabileceğinden hata düzeltmeli bellek, watchdog zamanlayıcıları, yedek bilgisayarlar ve çoğunluk oylaması kullanılabilir. Bir görev yanıt vermediğinde watchdog sistemi yeniden başlatır; kritik veriler ise bağımsız kanallardan karşılaştırılabilir.

Sonuç olarak RTOS, uzay istasyonundaki dijital orkestranın şefidir. Başarısı en yüksek hızı yakalamasından değil, doğru işi öngörülebilir zamanda yapmasından gelir. Uzayda “biraz geciktim” mazereti yoktur; milisaniyeler bile görev planının resmi bir parçasıdır.

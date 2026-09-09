---
layout: post
title: "Serverless Bedava Değildir: Gizli Maliyetler ve Soğuk Başlangıç Gerçeği"
math: true
categories: 
  - Bilgi
tags: 
  - serverless
  - bulut maliyetleri
  - performans
toc: true
---

Sunucusuz mimari, adındaki “sunucusuz” ifadesi yüzünden bulut dünyasının en yanlış anlaşılan modellerinden biridir. Ortada hâlâ sunucular vardır; yalnızca işletim sistemi güncelleme, kapasite planlama ve fiziksel altyapı yönetimi sağlayıcıya devredilir. Buna karşılık her çağrı, çalışma süresi, bellek tüketimi ve yan servis kullanımı faturaya dönüşebilir. Üstelik uzun süre boşta kalan fonksiyonların ilk istekte yaşadığı soğuk başlangıç gecikmesi, kullanıcı deneyimini sessizce baltalayabilir.
``
## Yanılgı: “Kullanmadığımda ödemem, dolayısıyla ucuzdur”

Serverless platformların temel avantajı, boşta duran kapasite yerine gerçek kullanım için ödeme yapılmasıdır. Ancak “kullandığın kadar öde” ifadesi, “her koşulda az öde” anlamına gelmez. Bir fonksiyonun yaklaşık işlem maliyeti şöyle modellenebilir:

$$
C = N \times (C_r + m \times t \times C_c) + C_e
$$

Burada $N$ çağrı sayısını, $C_r$ istek başına ücreti, $m$ ayrılan belleği, $t$ çalışma süresini, $C_c$ kaynak birimi ücretini ve $C_e$ harici servis maliyetlerini temsil eder. Harici servisler; API ağ geçidi, günlük kaydı, veri tabanı erişimi, kuyruklar ve dışarı veri aktarımı olabilir.

Örneğin dakikada bir çalışan masum bir zamanlayıcı ayda yaklaşık $43.200$ çağrı üretir. Aynı fonksiyon bir hata yüzünden tekrar denendiğinde veya kuyruktaki her kayıt için ayrı tetiklendiğinde sayı hızla katlanır. Trafik döngüsü şu hâle gelebilir: fonksiyon hata verir, olay kuyruğa döner, yeniden denenir, tekrar günlük oluşturur ve bütün adımlar ayrı ayrı ücretlendirilir. Küçük bir sonsuz döngü, büyük bir finans ekibi toplantısına dönüşebilir.

| Durum | Geleneksel sunucu | Serverless fonksiyon |
|---|---|---|
| Boşta bekleme | Kapasite için ödeme sürer | Genellikle işlem ücreti oluşmaz |
| Ani trafik | Ölçekleme planı gerekir | Otomatik ölçeklenebilir |
| Sürekli yüksek yük | Sabit kapasite avantajlı olabilir | Çağrı maliyeti büyüyebilir |
| Hatalı tekrar deneme | Kaynak tüketir | Kaynak ve çağrı faturası üretir |
| Operasyon | Sunucu yönetimi gerekir | Politika ve gözlemlenebilirlik gerekir |

## Soğuk başlangıç neden oluşur?

Bir fonksiyon uzun süre çalışmadığında platform yürütme ortamını kapatabilir. Yeni istek geldiğinde ortamın hazırlanması, çalışma zamanının yüklenmesi, uygulama kodunun başlatılması ve bağlantıların kurulması gerekir. Toplam gecikme kabaca şöyledir:

$$
T_{toplam} = T_{ağ} + T_{başlatma} + T_{kod} + T_{bağımlılıklar}
$$

Sıcak başlangıçta $T_{başlatma}$ büyük ölçüde ortadan kalkar. Soğuk başlangıçta ise büyük paketler, ağır framework’ler, sanal ağ bağlantıları ve başlangıç sırasında açılan veri tabanı oturumları bu süreyi artırır.

| Özellik | Sıcak başlangıç | Soğuk başlangıç |
|---|---|---|
| Ortam | Hazır | Yeniden hazırlanır |
| Gecikme | Düşük ve daha tutarlı | Yüksek ve değişken |
| Bağımlılıklar | Bellekte olabilir | Baştan yüklenebilir |
| Kullanıcı etkisi | Çoğunlukla fark edilmez | İlk istekte hissedilir |

Aşağıdaki JavaScript örneği, pahalı istemciyi her çağrıda oluşturmak yerine yürütme ortamı boyunca yeniden kullanır:

```javascript
import { DatabaseClient } from "./database.js";

// Global kapsam, sıcak çağrılarda bağlantının yeniden kullanılmasını sağlar.
const database = new DatabaseClient();

export async function handler(event) {
  const user = await database.findUser(event.userId);

  return {
    statusCode: user ? 200 : 404,
    body: JSON.stringify(user ?? { error: "Kullanıcı bulunamadı" })
  };
}
```

Bu yaklaşım başlatma maliyetini azaltabilir; fakat bağlantı sınırları yine izlenmelidir. Binlerce eşzamanlı fonksiyon, veri tabanını bağlantı yağmuruna tutabilir. Bağlantı havuzu veya yönetilen proxy kullanmak bu riski azaltır.

## Faturayı ve gecikmeyi kontrol altında tutmak

Öncelikle bütçe alarmları, eşzamanlılık sınırları ve başarısız olaylar için dead-letter queue tanımlanmalıdır. Tekrar denemeler üstel geri çekilme ile sınırlandırılmalı, fonksiyonlar idempotent tasarlanmalıdır. Günlüklerde her nesneyi yazdırmak yerine örnekleme ve saklama politikaları kullanılmalıdır.

Gecikmeye duyarlı uç noktalar için ayrılmış sıcak kapasite düşünülebilir; ancak bu seçenek serverless modeline sabit maliyet ekler. Paket boyutunu küçültmek, gereksiz bağımlılıkları kaldırmak ve başlangıç kodunu hafifletmek de etkilidir. Sonuç olarak serverless, altyapıyı yok etmez; kapasite yönetimini maliyet, olay akışı ve performans yönetimine dönüştürür. Doğru ölçülmeyen otomasyon ise yalnızca çok hızlı çalışan bir fatura makinesidir.

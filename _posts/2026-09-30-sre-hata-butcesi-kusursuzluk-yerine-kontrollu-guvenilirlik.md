---
layout: post
title: "SRE Hata Bütçesi: Kusursuzluk Yerine Kontrollü Güvenilirlik"
math: true
categories: 
  - Bilgi
tags: 
  - sre
  - hata bütçesi
  - devops
  - güvenilirlik
  - slo
  - gözlemlenebilirlik
toc: true
image: /img/sre-hata-butcesi-89.png
---

Bir sistemin hiç bozulmamasını istemek kulağa harika gelir; ancak yüzde yüz güvenilirlik hedefi, ekipleri yenilik yapmak yerine sonsuza kadar risk azaltmaya sürükleyebilir. Google’ın Site Reliability Engineering yaklaşımıyla yaygınlaştırdığı **hata bütçesi**, kullanıcıların kabul edebileceği arıza payını ölçülebilir bir geliştirme özgürlüğüne dönüştürür. Böylece ekip, “Hiç hata olmasın!” gibi gerçekçi olmayan bir hedef yerine, “Ne kadar hata kabul edilebilir ve bu payı nasıl yöneteceğiz?” sorusunu sorar.
``

## Önce SLI, SLO ve SLA’yı Ayıralım

Hata bütçesini anlayabilmek için üç kavramı birbirine karıştırmamak gerekir:

| Kavram | Anlamı | Örnek |
|---|---|---|
| **SLI** | Gerçekte ölçülen hizmet göstergesi | Başarılı istek oranı %99,93 |
| **SLO** | Ekip tarafından hedeflenen güvenilirlik seviyesi | Aylık erişilebilirlik %99,9 |
| **SLA** | Müşteriyle yapılan, yaptırım içerebilen sözleşme | %99,5 altına düşülürse ücret iadesi |

![sre-hata-butcesi-89](/img/sre-hata-butcesi-89.svg)


SLI bize sistemin durumunu, SLO ulaşmak istediğimiz seviyeyi, SLA ise ticari sınırı anlatır. Hata bütçesi çoğunlukla SLO üzerinden hesaplanır:

$$Hata\ Bütçesi = 1 - SLO$$

Aylık SLO değeri %99,9 ise izin verilen başarısızlık oranı şöyledir:

$$1 - 0.999 = 0.001 = \%0.1$$

Otuz günlük bir ayda toplam süre 43.200 dakikadır. Dolayısıyla teorik kesinti payı:

$$43.200 \times 0.001 = 43.2\ dakika$$

Aynı hesap istek sayısıyla da yapılabilir. Ayda bir milyon istek alan bir servisin %99,9 SLO’su varsa yaklaşık 1.000 başarısız isteğe izin verilir. Buradaki “izin”, hataların önemsenmediği anlamına gelmez; kabul edilebilir riskin önceden tanımlandığını gösterir.

## Bütçe Nasıl Tüketilir?

Dağıtım hataları, zaman aşımı sorunları ve kritik bağımlılıkların çökmesi bütçeyi tüketebilir. Tüketim oranı basitçe şöyle izlenebilir:

$$Tüketim\ Oranı = Gerçekleşen\ Hata / İzin\ Verilen\ Hata$$

Aşağıdaki Python örneği, istek tabanlı bir hata bütçesinin durumunu hesaplar:

```python
def error_budget(total_requests, failed_requests, slo):
    allowed_failures = total_requests * (1 - slo)
    consumption = failed_requests / allowed_failures
    remaining = max(allowed_failures - failed_requests, 0)

    return {
        'izin_verilen_hata': round(allowed_failures),
        'kalan_hata_payi': round(remaining),
        'tuketim_orani': round(consumption, 2)
    }

result = error_budget(1_000_000, 650, 0.999)
print(result)
```

Bu örnekte izin verilen 1.000 hatanın 650’si tüketilmiştir. Tüketim oranı 0,65, yani %65’tir. Bütçe tamamen bitmeden ekip yeni sürümler yayımlayabilir; ancak hızlı tüketim görülüyorsa dağıtım sıklığını azaltmak veya dayanıklılık çalışmalarına yönelmek mantıklıdır.

## Bütçe Aynı Zamanda Bir Karar Mekanizmasıdır

Hata bütçesinin asıl gücü hesaplamadan değil, ekip davranışını yönlendirmesinden gelir. Ürün ekibi özellik geliştirmek, operasyon ekibi ise sistemi korumak ister. Ortak ve sayısal bir bütçe, bu doğal gerilimi kişisel tartışma olmaktan çıkarır.

| Bütçe durumu | Önerilen yaklaşım |
|---|---|
| Büyük bölümü duruyor | Yeni özellikler ve daha sık dağıtım yapılabilir |
| Hızla tüketiliyor | Riskli değişiklikler azaltılır, kök nedenler incelenir |
| Tamamen tükendi | Özellik çalışmaları geçici olarak durdurulur |
| Sürekli kullanılmıyor | SLO gereğinden katı olabilir veya daha fazla yenilik yapılabilir |

Örneğin ekip, bütçe tükendiğinde yalnızca güvenilirlik iyileştirmelerinin üretime alınacağını önceden kararlaştırabilir. Otomatik geri alma, canary deployment, kapasite artırımı ve zaman aşımı düzenlemeleri bu dönemde öncelik kazanır.

## Neden %100 Değil?

%100 hedefi yalnızca pahalı değildir; çoğu zaman ölçülmesi de imkânsızdır. Kullanıcının internet bağlantısı, tarayıcısı veya üçüncü taraf servisler zaten kusursuz değildir. %99,9’dan %99,99’a çıkmak için gereken mimari karmaşıklık, sağlanan kullanıcı değerinden daha yüksek olabilir.

İyi bir hata bütçesi “Arıza çıkarabiliriz!” bileti değildir. Aksine güvenilirliği, geliştirme hızını ve kullanıcı beklentisini aynı masaya oturtan bir risk yönetimi aracıdır. Doğru SLI’lar seçildiğinde ve bütçe politikası gerçekten uygulandığında ekipler hem daha cesur yenilik yapar hem de sistem tehlikeli sınıra yaklaştığında frene ne zaman basacağını bilir.

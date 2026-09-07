---
layout: post
title: "Kodlamada Siper Etkisi: Ekipler Aynı Projede, Ama Farklı Dünyalarda"
math: true
categories: 
  - Bilgi
tags: 
  - silo effect
  - yazılım mimarisi
  - ekip iletişimi
toc: true
---

Büyük bir yazılım projesinde mobil ekip yeni bir özellik geliştirirken backend ekibi API’yi değiştirmiş, güvenlik ekibi farklı bir kimlik doğrulama standardına geçmiş ve operasyon ekibi bunların hiçbirinden haberdar olmamış olabilir. Her ekip kendi bölgesini başarıyla savunur; fakat ortaya çıkan ürün, birbirine uymayan parçalarla dolu teknolojik bir yapboza dönüşür. İşte bu görünmez ayrışmaya **Siper Etkisi**, yani *Silo Effect* denir.
``

## Siper Etkisi Nedir?

Siper etkisi, ekiplerin bilgi, hedef ve kararlarını diğer birimlerle yeterince paylaşmadan çalışmasıdır. Birinci Dünya Savaşı siperleri gibi herkes kendi alanını korur, başını dışarı çıkarmamaya çalışır. Yazılım dünyasında bunun cephanesi Jira görevleri, duvarları ise departman sınırlarıdır.

Sorun ekiplerin uzmanlaşması değildir. Uzmanlaşma gereklidir; problem, uzmanlığın **izolasyona** dönüşmesidir. Backend ekibi yalnızca servis performansını, frontend ekibi kullanıcı deneyimini, DevOps ekibi dağıtım güvenliğini optimize ederse yerel başarılar elde edilebilir. Ancak bütün sistem için en iyi sonuç ortaya çıkmayabilir.

Bu durumu basitçe şöyle gösterebiliriz:

$$Sistem\ Başarısı \neq \sum Yerel\ Optimizasyonlar$$

Ekipler arasındaki iletişim kaybını kabaca ölçmek için de şu düşünsel model kullanılabilir:

$$İletişim\ Kaybı = 1 - \frac{Gerçekleşen\ Bilgi\ Akışı}{Gerekli\ Bilgi\ Akışı}$$

Oran büyüdükçe sürpriz entegrasyon hataları ve yeniden çalışma ihtiyacı artar.

## Conway Yasası ve Mimari Yansıma

Conway Yasası, sistem tasarımlarının onları geliştiren organizasyonların iletişim yapısını yansıttığını söyler. Birbirleriyle konuşmayan üç ekip, çoğu zaman birbirleriyle zar zor konuşan üç servis üretir.

| Siperleşmiş yapı | İş birliğine açık yapı |
|---|---|
| Ekip içi hedefler önceliklidir | Ortak ürün hedefleri önceliklidir |
| API değişiklikleri sonradan duyulur | Sözleşmeler birlikte tasarlanır |
| Dokümantasyon ekip klasöründe kalır | Bilgi ortak platformda tutulur |
| Hatalarda suçlu aranır | Süreç ve sistem incelenir |
| Entegrasyon proje sonunda yapılır | Sürekli entegrasyon uygulanır |

Örneğin ödeme ekibi para miktarını kuruş cinsinden tamsayı olarak döndürürken mobil ekip bunu lira cinsinden ondalıklı sayı sanabilir. Her iki tarafın kodu kendi başına doğrudur; birlikte ise müşteriye 100 kat pahalı bir kahve gösterebilir.

## Koddan Önce Sözleşme

Ekipler arası uyumsuzluğu azaltmanın güçlü yollarından biri, API sözleşmesini uygulamadan önce paylaşmaktır:

```yaml
openapi: 3.0.3
paths:
  /payments/{id}:
    get:
      responses:
        "200":
          content:
            application/json:
              schema:
                type: object
                required: [id, amount, currency]
                properties:
                  id:
                    type: string
                  amount:
                    type: integer
                    description: Tutar, para biriminin en küçük birimindedir.
                  currency:
                    type: string
                    example: TRY
```

Bu tanım yalnızca endpoint’i belgelemekle kalmaz; `amount` alanının ne anlama geldiğini açıkça belirtir. Frontend, backend ve test ekipleri aynı sözleşmeden istemci, sahte servis ve doğrulama testleri üretebilir. Böylece bilgi bir kişinin hafızasında değil, çalıştırılabilir bir belgede yaşar.

## Siperleri Nasıl Kaldırabiliriz?

İlk adım daha fazla toplantı yapmak değildir. Kontrolsüz toplantı çoğalması, iletişimi güçlendirmek yerine takvimleri Tetris oyununa çevirebilir. Amaç, doğru bilginin doğru zamanda doğru ekibe ulaşmasıdır.

- Özellik ekiplerine farklı uzmanlıklardan kişiler dahil edin.
- Mimari kararları **ADR** belgeleriyle kayıt altına alın.
- API ve olay şemaları için ortak sahiplik oluşturun.
- Ekipler arası kod incelemeleri ve kısa teknik demolar düzenleyin.
- Entegrasyon testlerini geliştirme sürecinin sonuna bırakmayın.
- Başarıyı yalnızca ekip hızıyla değil, uçtan uca teslim süresiyle ölçün.

Örneğin teslim süresi şu şekilde ele alınabilir:

$$T_{teslim} = T_{geliştirme} + T_{bekleme} + T_{yeniden\ çalışma}$$

Siper etkisinde asıl büyüyen bölüm çoğunlukla kodlama süresi değil, bekleme ve yeniden çalışma süresidir.

## Sonuç

Siper etkisi kötü niyetli çalışanlardan değil; yanlış teşviklerden, kapalı bilgi kanallarından ve parçalı sorumluluklardan doğar. Çözüm herkesi her ayrıntıya boğmak değil, ekipler arasında açık sözleşmeler ve düzenli geri bildirim döngüleri kurmaktır. Çünkü iyi mimari yalnızca temiz kodla değil, sağlıklı iletişimle inşa edilir. Ekipler duvar örmek yerine köprü kurduğunda sistem de aynı davranışı sergiler.

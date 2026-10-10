---
layout: post
title: "No-Code Uygulama Arenası: Appsmith, Budibase ve ToolJet Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - no-code
  - low-code
  - appsmith
  - budibase
  - tooljet
  - iç araçlar
toc: true
image: /img/no-code-uygulama-67.png
---

Bir yönetim paneli, onay ekranı veya müşteri takip aracı geliştirmek için her zaman sıfırdan arayüz kodlamak gerekmez. Appsmith, Budibase ve ToolJet; veri kaynaklarını hazır bileşenlerle buluşturarak uygulama geliştirme süresini kısaltan no-code/low-code platformlarıdır. Ancak üçü de aynı sihirli değneği sallıyor gibi görünse de kullanım tarzları, özelleştirme seviyeleri ve hedef kullanıcıları bakımından önemli farklara sahiptir.

``

## No-code uygulama oluşturucu nasıl çalışır?

Bu platformların temel mantığı üç katmandan oluşur: **veri kaynağı**, **uygulama mantığı** ve **kullanıcı arayüzü**. Örneğin PostgreSQL veritabanından siparişleri çeker, bir JavaScript ifadesiyle filtreler ve sonucu tablo bileşeninde gösterirsiniz.

Geleneksel geliştirmede toplam süreyi kabaca şöyle düşünebiliriz:

$$T_{geleneksel} = T_{arayüz} + T_{backend} + T_{entegrasyon} + T_{test}$$

No-code yaklaşımında hazır bileşenler ve bağlayıcılar ilk üç kalemi küçültür:

$$T_{no-code} \approx T_{yapılandırma} + T_{iş\ mantığı} + T_{test}$$

Buradaki kazanç, kodun tamamen yok olmasından değil, tekrar eden altyapı işlerinin platform tarafından üstlenilmesinden gelir. Karmaşık yetkilendirme, sıra dışı iş akışları veya özel kullanıcı deneyimleri gerektiğinde low-code tarafına geçip JavaScript yazmanız hâlâ gerekebilir.

## Üç platformun kısa karşılaştırması

| Özellik | Appsmith | Budibase | ToolJet |
|---|---|---|---|
| Temel odak | İç araçlar ve paneller | Formlar, iş akışları ve iş uygulamaları | İç araçlar ve veri odaklı paneller |
| Kullanım tarzı | JavaScript ağırlıklı low-code | No-code yaklaşımı daha belirgin | Görsel geliştirme ve sorgu odaklı yapı |
| Veri katmanı | Harici API ve veritabanları | Dahili veri yapısı ve harici kaynaklar | Harici veri kaynakları ve API'ler |
| Özelleştirme | Yüksek | Orta-yüksek | Yüksek |
| Self-hosting | Var | Var | Var |
| Uygun kullanıcı | Geliştirici ekipleri | Operasyon ve ürün ekipleri | Teknik ekipler ve hızlı prototipleme |

![no-code-uygulama-67](/img/no-code-uygulama-67.svg)


## Appsmith: JavaScript sevenlerin oyun alanı

Appsmith, sürükle-bırak kolaylığını JavaScript esnekliğiyle birleştirir. Bir tablonun seçili satırını başka bir sorguya aktarmak veya API sonucunu dönüştürmek oldukça doğaldır.

```javascript
// API'den gelen aktif kullanıcıları ada göre sıralar.
const users = GetUsers.data ?? [];
return users
  .filter(user => user.active)
  .sort((a, b) => a.name.localeCompare(b.name));
```

Bu kod, veri gelmediğinde boş dizi kullanarak hatayı önler; ardından yalnızca aktif kullanıcıları seçer. Appsmith özellikle SQL, REST API ve JavaScript bilgisi bulunan ekiplerde hızlı sonuç verir. Dezavantajı ise teknik olmayan kullanıcıların bağlama ifadelerine alışmakta zorlanabilmesidir.

## Budibase: Formlar ve iş akışları ön planda

Budibase, veri tabanlı iş uygulamalarını mümkün olduğunca az kodla üretmeye odaklanır. Dahili veri tabloları sayesinde küçük bir envanter veya izin takip uygulaması için ayrıca veritabanı kurmadan başlanabilir. Otomasyon özellikleriyle kayıt oluşturulduğunda e-posta gönderme, durum değiştirme ya da webhook çağırma gibi süreçler tasarlanabilir.

Bu nedenle insan kaynakları formları, onay süreçleri ve operasyon uygulamaları için güçlü bir adaydır. Çok özel arayüz davranışlarında ise Appsmith kadar geliştirici merkezli hissettirmeyebilir.

## ToolJet: Bağlantılar ve sorgular merkezde

ToolJet, farklı veri kaynaklarını tek panelde birleştirmek isteyen ekipler için pratiktir. SQL sorguları, REST ve GraphQL servisleriyle çalışabilir; sonuçlar tablo, grafik veya form bileşenlerine bağlanabilir. Arayüzü, sorguyu çalıştır ve sonucu bileşene aktar yaklaşımını anlaşılır biçimde sunar.

Birden fazla sistemden veri toplayan destek panelleri, satış ekranları ve operasyon araçları için dengeli bir seçenektir. Yine de kullanılacak bağlayıcıların, sürümün ve dağıtım modelinin ihtiyaçları karşıladığı önceden doğrulanmalıdır.

## Hangisini seçmelisiniz?

Seçimi puanlamak için basit bir ağırlıklı model kullanılabilir:

$$P = 0.35E + 0.25V + 0.20O + 0.20K$$

Burada $E$ esneklik, $V$ veri entegrasyonu, $O$ operasyon kolaylığı ve $K$ kullanıcı dostu olma puanıdır. Teknik ekibiniz JavaScript ile rahat çalışıyorsa **Appsmith**, süreç ve form ağırlıklı ilerliyorsanız **Budibase**, çok sayıda kaynağı hızlıca panele bağlamak istiyorsanız **ToolJet** öne çıkar.

Son kararı özellik listesine bakarak değil, gerçek verinizle küçük bir prototip geliştirerek verin. Çünkü no-code dünyasında en güzel demo değil, pazartesi sabahı sorunsuz çalışan uygulama kazanır.

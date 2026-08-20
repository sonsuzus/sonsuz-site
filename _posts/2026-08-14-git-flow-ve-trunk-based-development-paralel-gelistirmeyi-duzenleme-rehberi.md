---
layout: post
title: "Git Flow ve Trunk-Based Development: Paralel Geliştirmeyi Düzenleme Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - git
  - git flow
  - trunk-based development
toc: true
---

Bir ekipte aynı anda özellik geliştirmek, hata düzeltmek ve sürüm hazırlamak yalnızca `git branch` komutunu bilmekle çözülmez. Asıl mesele, değişikliklerin hangi dalda ne kadar yaşayacağını, ne zaman gözden geçirileceğini ve üretime hangi kuralla taşınacağını ortaklaştırmaktır. Git Flow ile Trunk-Based Development (TBD), bu ortak çalışma sözleşmesini kurmak için yaygın iki yaklaşımdır.

``

## Dallanma neden bir organizasyon problemidir?

Bir dal, teknik olarak commit geçmişinin ayrıldığı bir çizgidir; ekip açısından ise **riskin ve işin izole edildiği alan**dır. Çok sayıda uzun ömürlü dal birleşme çatışması olasılığını artırırken, herkesin doğrudan ana hatta çalışması da yeterli test ve koruma yoksa üretim riskini büyütebilir.

Basitçe, birleşme maliyetini şu sezgisel modelle düşünebiliriz:

$$M \approx D \times C \times T$$

Burada $D$ değişen dosya/alan miktarını, $C$ aynı alanlarda eşzamanlı çalışma yoğunluğunu, $T$ ise dalın ana hattan uzak kaldığı zamanı temsil eder. Stratejilerin temel farkı, özellikle $T$ değerini nasıl yönettikleridir.

## Git Flow: Sürümler için belirgin şeritler

Git Flow, `main` ve `develop` adlı iki kalıcı dal etrafında kurulur. Yeni işler `feature/*`, sürüm hazırlıkları `release/*`, acil üretim düzeltmeleri ise `hotfix/*` dallarında yürütülür. `main`, yayınlanmış kodu; `develop` ise bir sonraki sürümün entegrasyon noktasını temsil eder.

Örneğin ödeme özelliği üzerinde çalışan ekip şu akışı izleyebilir:

```bash
git switch develop
git switch -c feature/payment-retry
# geliştirme, test ve commitler
git push -u origin feature/payment-retry
# Pull Request: feature/payment-retry -> develop
```

Özellik tamamlanınca `develop` dalına alınır. Yayın yaklaşınca `release/2.4.0` oluşturulur; burada yalnızca sürüm notu, versiyon ve kritik hata düzeltmeleri yapılır. Bu yapı, planlı ve seyrek sürüm çıkaran ürünlerde sürüm kapsamını netleştirir.

## Trunk-Based Development: Küçük değişiklik, hızlı entegrasyon

TBD'de merkez dal genellikle `main` ya da `trunk` olarak adlandırılır. Geliştiriciler doğrudan bu dala veya çok kısa ömürlü dallara çalışır. Amaç, değişiklikleri en geç bir-iki gün içinde ana hatta entegre etmektir. Henüz tamamlanmamış bir özellik, **feature flag** ile kullanıcıdan gizlenebilir.

```javascript
if (flags.isEnabled("payment_retry")) {
  return retryPayment(payment);
}
return processPayment(payment);
```

Bu örnekte kod ana hatta erken katılabilir; ancak `payment_retry` bayrağı açılmadan yeni davranış aktif olmaz. Böylece ekip, büyük bir özelliği haftalarca ayrı bir dalda bekletmek yerine küçük ve doğrulanabilir parçalar halinde birleştirir.

| Kriter | Git Flow | Trunk-Based Development |
|---|---|---|
| Kalıcı dallar | `main` ve `develop` | Genellikle yalnızca `main` |
| Dal ömrü | Orta veya uzun | Saatler ya da birkaç gün |
| Yayın modeli | Planlı, sürüm odaklı | Sık, mümkünse sürekli |
| Ana risk | Geç birleşme çatışmaları | Yetersiz testte hızlı hata yayılımı |
| Güçlü olduğu ortam | Versiyonlu ürünler, kontrollü yayınlar | CI/CD olgunluğu yüksek ekipler |

## Hangisini seçmeli?

Git Flow, mobil uygulama mağazası sürümleri, kurumsal paket dağıtımları veya uzun test pencereleri olan ekiplerde anlaşılır bir çerçeve sunar. Buna karşılık günde birçok kez dağıtım yapan web servisleri için `develop` ve uzun feature dalları gereksiz bekleme yaratabilir; TBD daha uygun olur.

Ancak strateji tek başına sihir değildir. Her iki modelde de zorunlu kod incelemesi, otomatik test, küçük commitler ve net geri alma planı gerekir. TBD için özellikle güçlü CI kritik önemdedir: ana hatta gelen her commit derlenmeli, test edilmeli ve mümkünse dağıtıma hazır olmalıdır. Git Flow içinse release dalına hangi değişikliklerin kabul edileceği açıkça tanımlanmalıdır.

En iyi başlangıç sorusu şudur: “Kodumuz ana hattan ne kadar süre ayrı kalıyor ve bunun maliyeti ne?” Cevap günlerce süren çatışmalar ve geciken entegrasyonlarsa, daha kısa dallara yönelin. Cevap karmaşık sürüm sertifikasyonlarıysa, Git Flow'un kontrollü şeritleri ekibin trafik ışıkları olabilir.

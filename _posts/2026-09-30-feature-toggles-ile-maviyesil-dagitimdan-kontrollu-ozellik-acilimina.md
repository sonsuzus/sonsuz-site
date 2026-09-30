---
layout: post
title: "Feature Toggles ile Mavi/Yeşil Dağıtımdan Kontrollü Özellik Açılımına"
math: true
categories: 
  - Bilgi
tags: 
  - feature-toggles
  - feature-flags
  - devops
  - dağıtım
  - canary-release
  - sürekli-teslimat
toc: true
image: /img/feature-toggles-ile-21.png
---

![feature-toggles-ile-21](/img/feature-toggles-ile-21.svg)


Mavi/yeşil dağıtım, iki ayrı üretim ortamı arasında trafik değiştirerek sürüm riskini azaltır. Ancak yalnızca bir özelliği açmak için bütün trafiği yeni ortama taşımak bazen balyozla ceviz kırmaya benzer. Feature toggle yaklaşımında yeni kod önceden canlıya çıkar; davranış ise dağıtım yapmadan, bir yönetim paneli veya yapılandırma servisi üzerinden etkinleştirilir.
``
## Dağıtım ile yayınlama aynı şey değildir

Klasik süreçte kodun üretime dağıtılması, özelliğin kullanıcıya sunulması anlamına gelir. Feature flag bu iki olayı ayırır:

- **Dağıtım:** Kodun üretim ortamına yerleştirilmesidir.
- **Yayınlama:** Özelliğin belirli kullanıcılara görünür hâle getirilmesidir.

Bir özelliği `yeni_odeme_akisi` bayrağının arkasına koyduğumuzu düşünelim. Kod üretimde bulunmasına rağmen bayrak kapalıyken eski ödeme akışı çalışır. Panelden bayrağı açtığımızda yeni davranış etkinleşir; sorun görülürse yeniden derleme veya dağıtım beklenmeden kapatılır.

Risk kabaca olasılık ve etkinin çarpımıyla düşünülebilir:

$$R = P(\text{hata}) \times I(\text{etki})$$

Feature flag hatanın oluşma olasılığını doğrudan sıfırlamaz. Bunun yerine özelliği önce küçük bir kullanıcı grubuna açarak etkiyi sınırlar. Kullanıcıların yalnızca $p$ oranı özelliği görüyorsa yaklaşık maruziyet şöyle modellenebilir:

$$R_{kontrollü} \approx p \times P(\text{hata}) \times I(\text{etki})$$

Bu basitleştirilmiş modelde özelliği kullanıcıların yüzde 5’ine açmak, olası hasarın yayılım alanını ciddi biçimde küçültür.

## Mavi/yeşil ve feature flag karşılaştırması

| Özellik | Mavi/Yeşil Dağıtım | Feature Flag |
|---|---|---|
| Kontrol birimi | Ortam veya sürüm | Tek özellik |
| Geri dönüş | Trafiği eski ortama yönlendirme | Panelden bayrağı kapatma |
| Altyapı maliyeti | İki paralel ortam gerektirebilir | Flag servisi ve izleme gerektirir |
| Hedefleme | Genellikle trafik düzeyinde | Kullanıcı, rol, ülke veya yüzde |
| Veritabanı değişiklikleri | Dikkatli uyumluluk ister | Yine dikkatli uyumluluk ister |

Feature flag, mavi/yeşil dağıtımın her durumda birebir yerine geçmez. Altyapı, çalışma zamanı veya geri uyumsuz veritabanı değişikliklerinde mavi/yeşil yaklaşım hâlâ değerlidir. En güçlü model, güvenli dağıtım için mavi/yeşili; kontrollü yayınlama için flag sistemini birlikte kullanmaktır.

## Basit bir uygulama örneği

Aşağıdaki JavaScript kodu, ödeme akışını kullanıcı bazında seçer:

```javascript
async function checkout(user, cart) {
  const enabled = await flags.isEnabled("new_checkout", {
    userId: user.id,
    country: user.country,
    plan: user.plan
  });

  if (enabled) {
    return newCheckout.process(user, cart);
  }

  return legacyCheckout.process(user, cart);
}
```

`isEnabled` çağrısı merkezi flag servisinden kural sonucunu alır. Üretim sistemlerinde bu sorgu için önbellek ve güvenli varsayılan kullanılmalıdır. Flag servisi ulaşılamazsa ödeme sisteminin tamamen durması yerine eski akışa dönmek daha mantıklıdır:

```javascript
const enabled = await flags
  .isEnabled("new_checkout", context)
  .catch(() => false);
```

## Güvenli açılım planı

Özellik önce şirket çalışanlarına, ardından beta kullanıcılarına ve daha sonra trafiğin yüzde 5, 25 ve 100’üne açılabilir. Her aşamada hata oranı, gecikme ve dönüşüm metriği izlenmelidir. Örneğin yeni akışın hata oranı $e_n$, eski akışın hata oranı $e_o$ ise şu eşik kullanılabilir:

$$e_n - e_o > 0.01 \Rightarrow \text{flag kapat}$$

Bayrakların da teknik borç ürettiği unutulmamalıdır. Her flag için sorumlu kişi, son kullanma tarihi ve kaldırma görevi tanımlanmalıdır. Kalıcılaşan eski dallar test kombinasyonlarını çoğaltır ve kodu labirente çevirir. Kısacası feature toggle, doğru izleme ve temizlik disipliniyle kullanıldığında dağıtımı sıradanlaştırır, yayınlamayı kontrollü hâle getirir ve panik anındaki geri dönüşü tek tıklamaya indirir.

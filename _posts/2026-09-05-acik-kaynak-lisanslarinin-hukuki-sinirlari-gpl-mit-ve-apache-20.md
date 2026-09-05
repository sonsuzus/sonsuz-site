---
layout: post
title: "Açık Kaynak Lisanslarının Hukuki Sınırları: GPL, MIT ve Apache 2.0"
math: true
categories: 
  - Bilgi
tags: 
  - açık kaynak
  - yazılım lisansları
  - gpl mıt apache
toc: true
---

Bir GitHub deposundaki “open source” etiketi, yazılımı istediğiniz gibi kullanabileceğiniz anlamına gelmez. GPL, MIT ve Apache 2.0 lisanslarının üçü de ticari kullanıma izin verir; ancak kaynak kodunu paylaşma, telif bildirimlerini koruma, patent hakları ve türev eserlerin dağıtımı konusunda farklı yükümlülükler doğurur. Kısacası lisans dosyası, projenin sıkıcı aksesuarı değil, kullanım sözleşmesidir.
``

## Önce temel denklem: Haklar ve yükümlülükler

Bir açık kaynak lisansını kabaca şu ilişkiyle düşünebiliriz:

$$Kullanım\ Serbestliği = Verilen\ Haklar - Uyulması\ Gereken\ Yükümlülükler$$

Buradaki “serbestlik”, ücretsiz olmayı ifade etmez. Açık kaynak yazılım satılabilir, ücretli destek hizmetiyle sunulabilir veya ticari bir ürünün parçası olabilir. Asıl mesele, yazılım müşteriye **dağıtıldığında** hangi koşulların devreye girdiğidir.

| Özellik | MIT | Apache 2.0 | GPLv3 |
|---|---|---|---|
| Ticari kullanım | Evet | Evet | Evet |
| Kaynak kodunu değiştirme | Evet | Evet | Evet |
| Kapalı kaynak üründe kullanma | Genellikle evet | Genellikle evet | Türev eserlerde genellikle hayır |
| Telif/lisans bildirimini koruma | Evet | Evet | Evet |
| Açık patent lisansı | Belirgin değil | Evet | Evet |
| Dağıtımda kaynak sunma | Hayır | Hayır | Evet, ilgili eser için |

## MIT: Kısa, esnek ve sorumluluğu sınırlı

MIT, izin verici lisansların en sade örneklerinden biridir. Kodu kullanabilir, değiştirebilir, satabilir ve kapalı kaynak bir ürüne ekleyebilirsiniz. Temel koşul, telif hakkı ve lisans metnini kopyalarda korumaktır.

Bu nedenle MIT, ticari SDK’lar, mobil uygulamalar ve şirket içi araçlar için düşük sürtünmeli bir tercihtir. Ancak lisansın açık bir patent hibesi içermemesi, patent riski bulunan sektörlerde ayrıca değerlendirme gerektirebilir. Ayrıca “garanti verilmez” maddesi, geliştiriciyi her ülkede ve her durumda mutlak biçimde koruyan sihirli bir kalkan değildir.

## Apache 2.0: MIT’nin patent zırhlı kuzeni

Apache 2.0 da kapalı kaynak ticari ürünlere entegrasyona izin verir. Fakat patent lisansı, katkıların belirtilmesi ve varsa `NOTICE` dosyasının korunması gibi daha ayrıntılı hükümler getirir.

En dikkat çekici mekanizma patent misillemesidir: Lisanslanan yazılımla ilgili patent davası açan kişinin belirli patent hakları sona erebilir. Büyük şirketlerin Apache 2.0’ı sevmesinin nedenlerinden biri budur. Değiştirilen dosyalarda değişiklik yapıldığını belirtmek de önemli bir dağıtım yükümlülüğüdür.

## GPL: Ticaret yasağı değil, copyleft zinciri

GPL hakkında en yaygın yanlış bilgi, GPL’li yazılımın satılamayacağıdır. Satılabilir; fakat ikili dosyayı dağıtırken karşılık gelen kaynak kodu sunmanız ve alıcının GPL haklarını kısıtlamamanız gerekir.

GPL koduyla tek bir türev program oluşturan bağlantı veya entegrasyon, tüm birleşik eserin GPL altında dağıtılmasını gerektirebilir. Buna karşılık ayrı süreçler arasında standart protokollerle iletişim kurmak her zaman aynı sonucu doğurmaz. Statik bağlantı, dinamik bağlantı, eklenti mimarisi ve süreçler arası iletişim hukuken aynı şey değildir; somut yapı incelenmelidir.

GPL’nin dağıtım odaklı olduğunu da unutmayın. Yazılım yalnızca şirket içinde kullanılıyorsa kaynak kodunu kamuya açma zorunluluğu genellikle doğmaz. Standart GPL kapsamında bir uygulamayı yalnızca SaaS olarak çalıştırmak da çoğu durumda dağıtım sayılmaz; ağ üzerinden kaynak paylaşımını hedefleyen lisans AGPL’dir.

## Projede lisans denetimi

Bağımlılıkların SPDX lisans bilgisini kontrol eden basit bir Python adımı, sürprizleri erken yakalayabilir:

```python
import json

with open("dependencies.json", encoding="utf-8") as file:
    dependencies = json.load(file)

review_required = {"GPL-3.0-only", "AGPL-3.0-only", "UNKNOWN"}

for package in dependencies:
    license_id = package.get("license", "UNKNOWN")
    if license_id in review_required:
        print(f"İnceleme gerekli: {package['name']} ({license_id})")
```

Bu kod hukuki karar vermez; yalnızca uyumluluk ekibine aday paketleri gösterir. Sağlam süreçte bağımlılık envanteri, kaynak kodu teklifleri, `NOTICE` dosyaları ve dağıtım modeli birlikte değerlendirilmelidir.

Sonuç olarak MIT maksimum esneklik, Apache 2.0 patent konusunda daha açık güvence, GPL ise yazılım özgürlüğünü sonraki dağıtımlara taşıyan güçlü copyleft sunar. Lisans seçimi yalnızca teknik değil, ürün stratejisidir. Özellikle karma lisanslı ticari projelerde nihai değerlendirme için uzman hukuk görüşü alınmalıdır.

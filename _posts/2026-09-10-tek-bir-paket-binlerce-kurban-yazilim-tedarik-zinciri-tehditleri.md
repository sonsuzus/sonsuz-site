---
layout: post
title: "Tek Bir Paket, Binlerce Kurban: Yazılım Tedarik Zinciri Tehditleri"
math: true
categories: 
  - Bilgi
tags: 
  - siber güvenlik
  - açık kaynak
  - tedarik zinciri
toc: true
---

Modern bir uygulama geliştirirken her şeyi sıfırdan yazmayız; doğrulama, tarih biçimlendirme veya metin renklendirme gibi işler için açık kaynak paketlerden yararlanırız. Ancak birkaç satırlık masum bir kütüphanenin geliştirici hesabı ele geçirilirse saldırgan, zararlı kodu resmi güncelleme gibi dağıtabilir. Sonuçta tek bir kişiye yapılan saldırı, aynı paketi kullanan binlerce kurumun kapısını aynı anda açan dijital bir maymuncuğa dönüşebilir.
``

## Yazılım tedarik zinciri nedir?

Yazılım tedarik zinciri; kaynak koddan derleme sunucusuna, paket yöneticisinden dağıtım altyapısına kadar ürünü oluşturan bütün bileşenlerin toplamıdır. NPM, PyPI, Maven Central veya NuGet üzerinden indirilen bağımlılıklar da bu zincirin halkalarıdır.

Örneğin uygulamanız doğrudan `A` paketini kullanabilir. Fakat `A`, kendi içinde `B` paketine; `B` de küçük bir `C` paketine güvenebilir. Siz `C` paketini seçmemiş olsanız bile kodu sisteminizde çalışır. Buna **geçişli bağımlılık** denir.

Bir projedeki yaklaşık saldırı yüzeyini şöyle düşünebiliriz:

$$R = \sum_{i=1}^{n} p_i \times e_i \times y_i$$

Burada $p_i$ bileşenin ele geçirilme olasılığını, $e_i$ erişebildiği sistemlerin etkisini, $y_i$ ise yayılma kapsamını temsil eder. Küçük bir paketin teknik işlevi önemsiz görünse de milyonlarca kez indirilmesi, $y_i$ değerini dramatik biçimde büyütür.

## Saldırgan zincire nasıl girer?

En bilinen senaryoda saldırgan, paket geliştiricisinin hesabını kimlik avı veya çalınmış erişim anahtarıyla ele geçirir. Ardından paketin yeni sürümüne arka kapı, bilgi hırsızı ya da uzaktan komut indiren bir kod ekler. Otomatik güncelleme kullanan sistemler bu sürümü sorgulamadan yükleyebilir.

| Saldırı yöntemi | Hedef | Muhtemel sonuç |
|---|---|---|
| Geliştirici hesabını ele geçirme | Paket deposu | Zararlı resmi sürüm |
| Typosquatting | Paket adı | Yanlış paketin kurulması |
| Derleme sunucusuna sızma | CI/CD hattı | Temiz kaynak, zararlı çıktı |
| Bağımlılık karmaşası | Özel paket adları | Saldırganın paketinin seçilmesi |
| Bakımcıyı kandırma | Proje yetkileri | Uzun vadeli yayın erişimi |

Bu saldırıları tehlikeli yapan nokta, zararlı kodun güvenilen kanaldan gelmesidir. Güvenlik duvarı paketi engellemeyebilir; çünkü indirme işlemini bizzat kurumun derleme sistemi başlatmıştır.

## Basit ama etkili savunmalar

İlk adım, bağımlılık sürümlerini kilitlemektir. Örneğin Node.js projelerinde yaklaşık sürüm aralığı yerine kesin sürüm tercih edilebilir:

```json
{
  "dependencies": {
    "ornek-paket": "2.4.1"
  }
}
```

Bu tanım tek başına güvenlik garantisi vermez; ancak beklenmedik bir `2.5.0` sürümünün otomatik kurulmasını önler. Kilit dosyaları depoya eklenmeli, bütünlük özetleri doğrulanmalı ve güncellemeler kontrollü biçimde uygulanmalıdır.

CI/CD hattında bilinen açıkları denetlemek için şu tür bir kontrol kullanılabilir:

```bash
npm ci
npm audit --audit-level=high
```

`npm ci`, kilit dosyasındaki sürümleri tekrarlanabilir şekilde kurar. İkinci komut ise yüksek önem derecesindeki bilinen güvenlik açıklarını raporlar. Benzer araçlar farklı ekosistemlerde de bulunur; ancak otomatik tarama, kötü niyetli fakat henüz raporlanmamış bir sürümü her zaman yakalayamaz.

## Güveni doğrulanabilir hâle getirmek

Kurumlar bir **SBOM**, yani Yazılım Malzeme Listesi oluşturmalıdır. Böylece hangi uygulamanın hangi paket sürümünü kullandığı hızla bulunabilir. Paket imzaları, çok faktörlü kimlik doğrulama, minimum yetkili derleme hesapları ve ağ erişimi kısıtlanmış çalışma ortamları da saldırının etkisini azaltır.

| Zayıf yaklaşım | Daha güvenli yaklaşım |
|---|---|
| Her güncellemeyi otomatik almak | Güncellemeyi inceleyip aşamalı dağıtmak |
| Sadece doğrudan paketleri izlemek | Geçişli bağımlılıkları da envantere almak |
| Derleme sistemine sınırsız yetki vermek | En az ayrıcalık ilkesini uygulamak |
| Tek bakımcıya körü körüne güvenmek | İmza ve çoklu onay kullanmak |

Açık kaynak kullanmak başlı başına tehlikeli değildir; görünmeyen bağımlılıkları kontrolsüzce güvenilir kabul etmek tehlikelidir. Tedarik zinciri güvenliğinin temel sorusu artık yalnızca “Kodumuz güvenli mi?” değil, “Kodumuzu oluşturan herkes ve her araç güvenilir mi?” olmalıdır.

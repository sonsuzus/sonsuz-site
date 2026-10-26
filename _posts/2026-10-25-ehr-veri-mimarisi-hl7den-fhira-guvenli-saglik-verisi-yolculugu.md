---
layout: post
title: "EHR Veri Mimarisi: HL7’den FHIR’a Güvenli Sağlık Verisi Yolculuğu"
math: true
categories: 
  - Bilgi
tags: 
  - ehr
  - hl7
  - fhir
  - sağlık bilişimi
  - veri mimarisi
  - siber güvenlik
toc: true
image: /img/ehr-veri-mimarisi-74.png
---

Bir hastanın alerjileri aile hekiminde, laboratuvar sonuçları hastanede, reçeteleri ise başka bir sistemde tutuluyorsa ortaya dijital bir yapboz çıkar. Elektronik Sağlık Kayıtları (EHR), bu parçaları anlamlı bir hasta geçmişine dönüştürür. Ancak farklı kurumların aynı dili konuşabilmesi için yalnızca bağlantı kurmak yetmez; verinin yapısını, anlamını ve güvenli aktarımını tanımlayan HL7 ve FHIR gibi standartlara ihtiyaç vardır.

``

## EHR veri mimarisinin temel katmanları

EHR mimarisi yalnızca büyük bir hasta tablosundan oluşmaz. Sağlıklı bir tasarım genellikle dört katmana ayrılır:

1. **Kaynak katmanı:** Hastane bilgi sistemleri, laboratuvarlar, görüntüleme cihazları ve eczane uygulamaları veriyi üretir.
2. **Entegrasyon katmanı:** HL7 mesajları, FHIR API'leri veya entegrasyon motorları sistemler arasında çeviri yapar.
3. **Klinik veri katmanı:** Hasta, tanı, gözlem, ilaç ve işlem kayıtları ilişkilendirilerek saklanır.
4. **Erişim ve güvenlik katmanı:** Kimlik doğrulama, yetkilendirme, denetim kayıtları ve hasta onayı uygulanır.

Bir kaydın kullanılabilirliği basitçe şu mantıkla düşünülebilir:

$$K = D \times A \times G$$

Burada $D$ doğruluk, $A$ erişilebilirlik, $G$ ise güvenilirliktir. Katsayılardan biri sıfıra yaklaşırsa kaydın klinik değeri de düşer. Çok hızlı erişilen fakat yanlış hastaya ait bir sonuç, faydadan çok tehlike üretir.

## HL7 ve FHIR arasındaki fark

HL7 aslında tek bir teknoloji değil, sağlık verisi alışverişi için geliştirilmiş standartlar ailesidir. HL7 Version 2, olay tabanlı mesajlaşmasıyla yıllardır hastanelerde kullanılır. Örneğin bir hasta kabul edildiğinde `ADT` mesajı gönderilebilir. FHIR ise aynı problemi modern web yaklaşımıyla ele alır ve veriyi küçük, yeniden kullanılabilir **kaynaklara** böler.

| Özellik | HL7 v2 | FHIR |
|---|---|---|
| Veri biçimi | Ayraçlarla bölünmüş metin | JSON, XML veya RDF |
| İletişim | Mesaj ve olay tabanlı | REST API, mesaj veya belge |
| Temel yapı | Segmentler | Kaynaklar |
| Web uyumu | Ek entegrasyon gerektirir | Doğal HTTP desteği sunar |
| Öğrenme eğrisi | Kuruma özel yorumlar zorlayabilir | Web geliştiricileri için daha tanıdıktır |

![ehr-veri-mimarisi-74](/img/ehr-veri-mimarisi-74.svg)


FHIR'daki `Patient`, `Observation`, `MedicationRequest` ve `Encounter` gibi kaynaklar birlikte klinik hikâyeyi oluşturur. Bu yaklaşım, bütün dosyayı taşımak yerine gereken parçayı paylaşmaya imkân verir.

## Basit bir FHIR kaynağı

Aşağıdaki örnek, hastanın kimliğini temsil eden sadeleştirilmiş bir FHIR `Patient` kaynağıdır:

```json
{
  "resourceType": "Patient",
  "id": "hasta-42",
  "identifier": [
    {
      "system": "https://kurum.example/hasta-no",
      "value": "A1042"
    }
  ],
  "name": [
    {
      "family": "Yılmaz",
      "given": ["Deniz"]
    }
  ]
}
```

`resourceType`, nesnenin türünü; `identifier`, kurum içindeki veya ulusal sistemdeki kimliği belirtir. Gerçek uygulamalarda doğum tarihi, iletişim bilgileri ve onay kayıtları eklenebilir. Bununla birlikte gereksiz kişisel veri taşımamak, veri minimizasyonunun önemli bir gereğidir.

## Güvenli paylaşım nasıl sağlanır?

FHIR kullanmak veriyi kendiliğinden güvenli yapmaz. Aktarım sırasında TLS, kullanıcı girişinde OpenID Connect, API yetkilendirmesinde OAuth 2.0 ve sağlık uygulamalarında SMART on FHIR profilleri kullanılabilir. Ayrıca her erişim için “kim, hangi kaydı, ne zaman görüntüledi?” sorusunu cevaplayan denetim izi tutulmalıdır.

| Risk | Önerilen kontrol |
|---|---|
| Yetkisiz erişim | Rol ve kapsam tabanlı yetkilendirme |
| Aktarımın dinlenmesi | TLS ile şifreleme |
| Kayıtların değiştirilmesi | Bütünlük kontrolü ve dijital imza |
| Yanlış hasta eşleşmesi | Ana hasta indeksi ve güçlü tanımlayıcılar |
| Gereksiz veri paylaşımı | Onay yönetimi ve veri minimizasyonu |

Sonuç olarak HL7 v2 mevcut hastane altyapılarının çalışkan emektarı, FHIR ise web dostu yeni nesil temsilcisidir. Başarılı bir EHR mimarisi çoğu zaman ikisini rakip görmek yerine entegrasyon motorlarıyla birlikte kullanır. Amaç daha fazla veri toplamak değil; doğru veriyi, doğru sağlık çalışanına, doğru zamanda ve hastanın mahremiyetini koruyarak ulaştırmaktır.

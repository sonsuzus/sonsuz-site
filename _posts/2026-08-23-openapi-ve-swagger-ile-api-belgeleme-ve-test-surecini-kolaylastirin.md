---
layout: post
title: "OpenAPI ve Swagger ile API Belgeleme ve Test Sürecini Kolaylaştırın"
math: true
categories: 
  - Bilgi
tags: 
  - OpenAPI
  - Swagger
  - API
  - REST
  - Dokümantasyon
---

Bir API geliştirmek, yalnızca çalışan endpoint'ler yazmaktan ibaret değildir. Bu endpoint'lerin hangi veriyi beklediği, hangi yanıtları döndüğü, hata durumlarında nasıl davranacağı ve yetkilendirmenin nasıl yapılacağı da açıkça anlatılmalıdır. İşte OpenAPI ve Swagger, API geliştiricileri ile API tüketicileri arasındaki bu iletişim sorununu standartlaştırılmış, canlı ve test edilebilir bir sözleşmeye dönüştürür.

``

## OpenAPI nedir, Swagger nedir?

**OpenAPI Specification (OAS)**, HTTP tabanlı API'leri makinenin ve insanın okuyabileceği biçimde tanımlayan açık bir standarttır. Endpoint yolları, HTTP metotları, parametreler, istek gövdeleri, yanıt şemaları ve güvenlik yöntemleri tek bir YAML veya JSON dosyasında ifade edilir.

Swagger ise tarihsel olarak hem bu tanım formatının adı hem de onu kullanan araç ekosistemiydi. Günümüzde teknik ayrım şudur: **OpenAPI standarttır; Swagger ise bu standardı üretmek, görüntülemek ve denemek için kullanılan araç ailesidir.** Swagger UI, Swagger Editor ve Swagger Codegen bu ekosistemin tanınan parçalarıdır.

| Kavram | Temel rolü | Örnek kullanım |
|---|---|---|
| OpenAPI | API sözleşmesi standardı | `openapi.yaml` yazmak |
| Swagger UI | Etkileşimli dokümantasyon arayüzü | Tarayıcıdan endpoint çağırmak |
| Swagger Editor | Tanım dosyası düzenleyicisi | YAML doğrulamak |
| OpenAPI Generator | İstemci/sunucu kodu üretmek | TypeScript SDK üretmek |

Bu yaklaşımın merkezindeki fikir şudur: API'nin gerçek davranışı ile dokümantasyonu aynı kaynaktan beslenmelidir. Aksi halde doküman hızla eskir ve meşhur “dokümanda çalışıyor görünüyordu” cümlesi ortaya çıkar.

## Bir API sözleşmesinin matematiği

Bir endpoint'i basitleştirerek bir fonksiyon gibi düşünebiliriz. İstek uzayı $R$, başarı yanıtları $S$, hata yanıtları ise $E$ olsun. Endpoint davranışı kabaca şöyle modellenebilir:

$$f: R \rightarrow S \cup E$$

OpenAPI, bu fonksiyondaki $R$, $S$ ve $E$ kümelerini açık biçimde tarif eder. Örneğin `POST /users` için istek gövdesinde `email` alanının zorunlu olduğunu; başarılı durumda `201`, geçersiz veride `400` döneceğini belirtir. Böylece frontend, mobil uygulama ve backend ekipleri varsayımla değil sözleşmeyle çalışır.

## Basit ama anlamlı bir OpenAPI örneği

Aşağıdaki YAML, kullanıcı oluşturma endpoint'ini tanımlar. `schema` bölümü veri biçimini, `responses` bölümü ise olası sonuçları anlatır.

```yaml
openapi: 3.0.3
info:
  title: Kullanıcı API
  version: 1.0.0
paths:
  /users:
    post:
      summary: Yeni kullanıcı oluşturur
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [name, email]
              properties:
                name:
                  type: string
                  example: Ada Lovelace
                email:
                  type: string
                  format: email
      responses:
        '201':
          description: Kullanıcı oluşturuldu
        '400':
          description: Geçersiz istek verisi
```

Bu dosya Swagger UI'a verildiğinde otomatik bir ekran oluşur. Kullanıcı `Try it out` düğmesiyle örnek JSON gönderir, sunucunun gerçek yanıtını görür ve hata senaryolarını hızla keşfeder. Yani dokümantasyon pasif bir PDF olmaktan çıkar; küçük bir test konsoluna dönüşür.

## Dokümantasyon ve test birlikte neden güçlüdür?

| Geleneksel yaklaşım | OpenAPI odaklı yaklaşım |
|---|---|
| Doküman elle güncellenir | Sözleşme kaynak kodla sürümlenir |
| Test için Postman koleksiyonu aranır | Swagger UI üzerinden hızlı deneme yapılır |
| Alan adları ekipler arasında değişebilir | Şema herkes için tek doğruluk kaynağıdır |
| SDK'lar manuel yazılır | İstemci kodu üretilebilir |

Özellikle CI/CD sürecinde OpenAPI dosyasını doğrulamak büyük fayda sağlar. Örneğin kırıcı bir değişiklikte `email` alanını kaldırmak, istemcileri etkileyebilir. Şema karşılaştırma araçları bu tür değişiklikleri dağıtımdan önce raporlayabilir. Böylece entegrasyon hatalarının maliyeti üretim ortamına ulaşmadan düşer.

## Uygulama için pratik öneriler

Önce kaynak koddan dokümantasyon üretme (**code-first**) veya önce sözleşmeyi tasarlama (**design-first**) yöntemlerinden birini seçin. Hızlı başlayan küçük ekiplerde code-first rahat olabilir; çok sayıda istemcinin bulunduğu projelerde design-first, ekipler arası anlaşmayı erkenden netleştirir. Her iki durumda da örnek istekler, gerçekçi hata yanıtları, `401`/`403` güvenlik açıklamaları ve sürüm bilgisi eklemeyi ihmal etmeyin.

Sonuç olarak OpenAPI, API'nizin teknik kimlik kartıdır; Swagger ise bu kartı okunur, denenebilir ve paylaşılabilir hale getirir. İyi yazılmış bir sözleşme, hem geliştirici deneyimini hem de ürünün teslim hızını belirgin biçimde iyileştirir.

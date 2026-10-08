---
layout: post
title: "API Dokümantasyon Sistemi Kurmak: Swagger UI, Redoc ve Docusaurus"
math: true
categories: 
  - Proje
tags: 
  - api
  - swagger-ui
  - redoc
  - docusaurus
  - openapi
  - dokümantasyon
toc: true
image: /img/api-dokumantasyon-sistemi-62.png
---

Bir API geliştirmek yalnızca çalışan endpoint’ler yazmak değildir; diğer geliştiricilerin bu endpoint’leri keşfedebilmesini, deneyebilmesini ve doğru kullanabilmesini sağlamak da işin parçasıdır. Swagger UI, Redoc ve Docusaurus aynı dokümantasyon evreninde yaşasa da farklı sorunları çözer. Gelin bu araçları yarıştırmak yerine birlikte çalıştırabileceğimiz sürdürülebilir bir sistem tasarlayalım.
``
## Önce temel: OpenAPI nedir?

OpenAPI, REST tabanlı bir API’nin insanlar ve makineler tarafından okunabilen sözleşmesidir. Endpoint yolları, HTTP metotları, parametreler, veri modelleri, kimlik doğrulama yöntemleri ve olası yanıtlar YAML veya JSON biçiminde tanımlanır.

Bir API sözleşmesini kabaca şu fonksiyonla düşünebiliriz:

$$
S = P + R + M + A + E
$$

Burada $P$ yolları, $R$ istekleri, $M$ veri modellerini, $A$ kimlik doğrulamayı ve $E$ hata yanıtlarını temsil eder. Sözleşme ne kadar eksiksizse istemci üretimi, test otomasyonu ve geliştirici deneyimi o kadar başarılı olur.

Swagger UI ve Redoc bu sözleşmeyi görselleştirir. Docusaurus ise rehberler, eğitimler, sürüm notları ve kavramsal açıklamalar için genel bir dokümantasyon sitesi sunar.

## Araçların karşılaştırması

| Özellik | Swagger UI | Redoc | Docusaurus |
|---|---|---|---|
| Ana amaç | API’yi etkileşimli denemek | Okunabilir API referansı | Tam dokümantasyon portalı |
| OpenAPI desteği | Doğrudan | Doğrudan | Eklentiyle |
| İstek gönderme | Güçlü | Sınırlı veya sürüme bağlı | Yerleşik değil |
| Özelleştirme | Orta | Güçlü tema seçenekleri | React ile çok güçlü |
| En uygun kullanım | Test ve keşif | Referans dokümanı | Rehber ve içerik yönetimi |

![api-dokumantasyon-sistemi-62](/img/api-dokumantasyon-sistemi-62.svg)


Kısacası Swagger UI laboratuvar, Redoc düzenli bir ansiklopedi, Docusaurus ise bütün kampüstür.

## Küçük bir OpenAPI sözleşmesi

Aşağıdaki dosya, kullanıcı bilgisini kimliğe göre döndüren bir endpoint tanımlar:

```yaml
openapi: 3.0.3
info:
  title: Kullanıcı API
  version: 1.0.0
paths:
  /users/{id}:
    get:
      summary: Kimliğe göre kullanıcı getirir
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Kullanıcı bulundu
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: Kullanıcı bulunamadı
components:
  schemas:
    User:
      type: object
      required: [id, name]
      properties:
        id:
          type: integer
        name:
          type: string
```

Bu tanım tek bir doğruluk kaynağıdır. Aynı dosya arayüz oluşturmak, sözleşme testi yapmak veya istemci SDK’sı üretmek için kullanılabilir.

## Swagger UI ve Redoc’u çalıştırmak

En hızlı yöntem Docker kullanmaktır:

```bash
# Etkileşimli Swagger UI

docker run --rm -p 8080:8080 \
  -e SWAGGER_JSON=/spec/openapi.yaml \
  -v "$PWD:/spec" swaggerapi/swagger-ui

# Okuma odaklı Redoc

docker run --rm -p 8081:80 \
  -e SPEC_URL=openapi.yaml redocly/redoc
```

İlk komut API’yi `localhost:8080` üzerinde deneyebilmenizi sağlar. İkinci komut aynı sözleşmeyi daha sade ve referans odaklı bir görünümle sunar. Gerçek projede dosyayı Redoc sunucusunun erişebileceği dizine kopyalamak veya bir URL üzerinden yayımlamak gerekir.

## Docusaurus ile merkezi portal

Docusaurus projesinde kavramsal rehberleri Markdown ile tutabilir, API referansına menüden bağlantı verebilirsiniz:

```js
// docusaurus.config.js
export default {
  themeConfig: {
    navbar: {
      items: [
        { to: '/docs/intro', label: 'Rehberler' },
        { href: '/api/redoc.html', label: 'API Referansı' },
        { href: '/swagger/', label: 'API’yi Dene' }
      ]
    }
  }
};
```

Bu yapı kullanıcıya üç katman sunar: “Neden kullanmalıyım?” sorusunu rehberler, “Hangi alanlar var?” sorusunu Redoc, “Bu istek gerçekten çalışıyor mu?” sorusunu Swagger UI cevaplar.

## Sürdürülebilir iş akışı

OpenAPI dosyasını uygulama koduyla aynı depoda saklayın. CI sürecinde sözdizimini doğrulayın, kırıcı değişiklikleri karşılaştırın ve başarılı derlemeden sonra üç aracı da yayımlayın. Sürüm numarasını URL’ye eklemek, eski istemcilerin dokümantasyona erişmesini kolaylaştırır.

Ayrıca örneklerde gerçek erişim anahtarları kullanmayın. Swagger UI üzerindeki yetkilendirme alanlarını yalnızca güvenli test ortamlarına bağlayın. Böylece güzel görünen değil; güncel, test edilebilir ve güvenilir bir API dokümantasyon sistemi elde edersiniz.

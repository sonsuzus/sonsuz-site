---
layout: post
title: "OpenAPI ile REST Servislerini Konuşturan Dokümantasyon Kültürü"
math: true
categories: 
  - Bilgi
tags: 
  - openapı
  - rest apı
  - apı dokümantasyonu
toc: true
---

Bir REST servisini geliştirmek bazen kalabalık bir restoranda sipariş vermeye benzer: İstemci başka bir şey söyler, sunucu başka bir şey anlar, test ekibi ise menüde hiç bulunmayan bir yanıtla karşılaşır. OpenAPI Standardı, diğer adıyla Açık API Standardı, bu iletişim kazalarını azaltmak için endpoint’leri, parametreleri, veri modellerini ve olası yanıtları makineler tarafından da okunabilen ortak bir sözleşmede tanımlar.
``

## OpenAPI tam olarak nedir?

OpenAPI; HTTP tabanlı API’lerin davranışını YAML veya JSON biçiminde tarif eden, dilden bağımsız bir standarttır. Bir OpenAPI belgesi servisin nasıl çalıştığını uygulamaz; servisin **nasıl çalışması gerektiğini** açıklar. Bu nedenle onu yalnızca dokümantasyon dosyası değil, geliştirici, test uzmanı ve tüketici arasında yaşayan bir kontrat olarak düşünmek gerekir.

Bir endpoint’in sözleşmesi kabaca şu bileşenlerden oluşur:

- HTTP yolu ve metodu
- İstek parametreleri ve gövdesi
- Kimlik doğrulama yöntemi
- Başarılı ve hatalı yanıtlar
- Veri şemaları ve doğrulama kuralları

```yaml
openapi: 3.1.0
info:
  title: Kitaplık API
  version: 1.0.0
paths:
  /books/{id}:
    get:
      operationId: getBook
      summary: Kimliğe göre kitap getirir
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Kitap bulundu
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Book'
        '404':
          description: Kitap bulunamadı
```

Bu taslak, `GET /books/{id}` çağrısının ne beklediğini açıkça belirtir. Araçlar bu dosyadan etkileşimli dokümantasyon, istemci kodu, mock sunucu ve otomatik test üretebilir.

## Önce kod mu, önce sözleşme mi?

OpenAPI iki temel çalışma kültürünü destekler:

\vert  Yaklaşım \vert  Başlangıç noktası \vert  Güçlü yanı \vert  Olası sorun \vert 
\vert ---\vert ---\vert ---\vert ---\vert 
\vert  Code-first \vert  Uygulama kodu \vert  Hızlı geliştirme \vert  Doküman kodun gerisinde kalabilir \vert 
\vert  Design-first \vert  OpenAPI sözleşmesi \vert  Ekipler paralel çalışabilir \vert  Taslağın disiplinle yönetilmesi gerekir \vert 

Design-first yaklaşımında backend henüz yazılmadan frontend ekibi mock sunucu üzerinden ilerleyebilir. Test ekibi beklenen durum kodlarını hazırlarken ürün ekibi de API davranışını erken aşamada inceleyebilir. Böylece entegrasyon günü sürprizlerle dolu bir macera filmi olmaktan çıkar.

## Otomasyonun matematiği

Bir projede her sürümde elle yapılan doğrulama sayısı $M$, sürüm sayısı $R$ ve işlem başına hata olasılığı $p$ olsun. Basitleştirilmiş beklenen hata yükü şöyle ifade edilebilir:

$$E = M \times R \times p$$

OpenAPI tabanlı doğrulama, kod üretimi ve sözleşme testleri $M$ değerini düşürür. Amaç insanı süreçten çıkarmak değil, insanın sürekli aynı kontrol listesini tekrarlamasını engellemektir.

## Sözleşmeden çalışan sisteme

Bir OpenAPI belgesi CI/CD hattına bağlandığında gerçek değerini gösterir. Örneğin şu adımlar otomatikleştirilebilir:

1. YAML dosyasını sözdizimi ve standart kuralları açısından denetlemek.
2. Geriye dönük uyumsuz değişiklikleri önceki sürümle karşılaştırmak.
3. Mock servis veya SDK üretmek.
4. Gerçek yanıtların tanımlanan şemaya uyduğunu test etmek.
5. Swagger UI ya da Redoc ile güncel dokümantasyon yayımlamak.

```bash
# OpenAPI belgesindeki biçim ve tasarım sorunlarını denetler
npx @redocly/cli lint openapi.yaml

# Belgeden tarayıcıda açılabilen HTML dokümantasyonu üretir
npx @redocly/cli build-docs openapi.yaml
```

Ancak otomasyon kötü tasarlanmış bir sözleşmeyi sihirli biçimde düzeltmez. Açık `operationId` değerleri kullanılmalı, ortak modeller `components/schemas` altında tekrar kullanılmalı ve yalnızca `200` yanıtı değil, `400`, `401`, `404` ve `500` gibi hata senaryoları da tanımlanmalıdır.

Sonuç olarak OpenAPI, güzel görünen bir dokümantasyon sayfasından çok daha fazlasıdır. Doğru uygulandığında API tasarımını tartışılabilir, test edilebilir ve otomatikleştirilebilir hâle getirir. Takımlar aynı sözleşmeye baktığında “Ben endpoint’i böyle anlamamıştım” cümlesi azalır; geriye daha güvenilir servisler ve daha huzurlu entegrasyon günleri kalır.

---
layout: post
title: "Hexagonal Architecture Nedir? İş Mantığını Altyapıdan Özgürleştirmek"
math: true
categories: 
  - Bilgi
tags: 
  - hexagonal architecture
  - clean architecture
  - yazılım mimarisi
toc: true
---

Bir uygulamanın veritabanını PostgreSQL’den MongoDB’ye taşımak, REST API yerine mesaj kuyruğu kullanmak ya da ödeme sağlayıcısını değiştirmek neden iş kurallarını kırmalıdır? Hexagonal Architecture, bu soruya güçlü bir “kırmamalı” yanıtı verir. Alistair Cockburn tarafından ortaya atılan bu yaklaşım, uygulamanın kalbi olan iş mantığını kullanıcı arayüzü, veritabanı ve harici servis gibi değişken ayrıntılardan izole eder.
``

## Altıgen bir şekilden daha fazlası

“Altıgen” adı, mimarinin katı olarak altı kenar gerektirmesinden gelmez. Şekil; uygulamanın dış dünyayla birden çok yoldan iletişim kurabildiğini anlatan görsel bir metafordur. Merkezde **domain** yani iş kuralları bulunur. Kenarlarda ise bu kurallara ulaşan veya onların ihtiyaçlarını karşılayan bağlantılar yer alır.

Bu bağlantılar iki temel kavramla açıklanır:

- **Port:** Uygulamanın sunduğu ya da ihtiyaç duyduğu sözleşmedir. Genellikle arayüz (interface) olarak modellenir.
- **Adapter:** Bir portu somut teknolojiye bağlayan uygulamadır. HTTP controller, CLI komutu, SQL repository veya e-posta istemcisi birer adapter olabilir.

Bağımlılık yönü kritik noktadır: Dış katmanlar merkeze bağımlıdır; merkez dış katmanlara değil. Bunu kabaca $D_{core} = 0$ dış teknoloji bağımlılığı olarak düşünebiliriz. Pratikte domain katmanının framework import etmemesi hedeflenir.

| Kavram | Görevi | Örnek |
|---|---|---|
| Domain | İş kurallarını taşır | `Order`, indirim hesaplama |
| Inbound Port | Uygulamanın sunduğu işlemi tanımlar | `PlaceOrder` |
| Outbound Port | Uygulamanın dışarıdan beklediğini tanımlar | `OrderRepository` |
| Adapter | Portu teknolojiyle birleştirir | REST controller, PostgreSQL repository |

## Giriş ve çıkış adapter’ları

Bir kullanıcı HTTP isteği gönderdiğinde REST controller bir **giriş (driving/inbound) adapter’ı** olur. Controller, isteği domain nesnelerine çevirir ve bir use case çağırır. Buna karşılık uygulamanın veriyi saklaması gerektiğinde repository portu devreye girer. PostgreSQL implementasyonu ise **çıkış (driven/outbound) adapter’ıdır**.

Örneğin sipariş oluşturma akışı şöyle okunabilir:

$$HTTP\ Request \rightarrow Controller \rightarrow PlaceOrder\ UseCase \rightarrow Repository\ Port \rightarrow Database$$

Burada veritabanı değişse bile use case’in değişmemesi amaçlanır. Asıl değer, teknolojik değişim maliyetini merkezin dışına itmektir.

```java
public interface OrderRepository {
    void save(Order order);
}

public class PlaceOrderService {
    private final OrderRepository repository;

    public PlaceOrderService(OrderRepository repository) {
        this.repository = repository;
    }

    public void place(String customerId, int quantity) {
        if (quantity <= 0) throw new IllegalArgumentException("Adet pozitif olmalı");
        repository.save(new Order(customerId, quantity));
    }
}
```

Bu örnekte `PlaceOrderService`, verinin SQL ile mi, dosya ile mi yoksa uzak bir servisle mi saklandığını bilmez. Sadece portun söz verdiği `save` davranışına güvenir. Dependency Injection ile gerçek adapter çalışma anında bağlanır.

## Katmanlı mimariden farkı nedir?

Hexagonal Architecture katmanlı mimariyle düşman değildir; hatta birlikte kullanılabilir. Fark, bağımlılık disiplinindedir. Geleneksel tasarımlarda servis katmanının ORM sınıflarına veya web framework tiplerine sızması yaygındır. Hexagonal yaklaşımda teknoloji ayrıntıları sınırın dışında kalır.

| Ölçüt | Geleneksel katmanlı yaklaşım | Hexagonal yaklaşım |
|---|---|---|
| Bağımlılık | Sıklıkla üstten alta | Dıştan merkeze |
| Test | Altyapı kurulumu gerekebilir | Portlar fake/mock ile değiştirilebilir |
| Teknoloji değişimi | Geniş etki alanı oluşturabilir | Adapter düzeyinde sınırlanır |
| Odak | Teknik katmanlar | Use case ve iş davranışı |

## Ne zaman kullanılmalı?

Uzun ömürlü, karmaşık iş kuralları içeren ve birden fazla entegrasyona sahip sistemlerde bu mimari oldukça değerlidir. Ödeme, kargo, bildirim ve farklı istemci kanalları olan bir e-ticaret sistemi iyi bir adaydır. Ancak küçük bir CRUD uygulamasında her işlem için port ve adapter üretmek gereksiz tören maliyeti yaratabilir.

Özetle Hexagonal Architecture, “veritabanı uygulamanın merkezi değildir; iş kuralı merkezdir” fikrini kod yapısına dönüştürür. Bu sayede test edilebilir, değişime dayanıklı ve teknolojik modası geçse bile iş değerini koruyan uygulamalar tasarlamak kolaylaşır.

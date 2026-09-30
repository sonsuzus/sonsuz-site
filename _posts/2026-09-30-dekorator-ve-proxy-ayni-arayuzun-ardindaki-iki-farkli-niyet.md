---
layout: post
title: "Dekorator ve Proxy: Aynı Arayüzün Ardındaki İki Farklı Niyet"
math: true
categories: 
  - Bilgi
tags: 
  - tasarım kalıpları
  - decorator
  - proxy
  - nesne yönelimli programlama
  - java
  - yazılım mimarisi
toc: true
image: /img/dekorator-ve-proxy-50.png
---

Decorator ve Proxy kalıpları ilk bakışta birbirinin ikizi gibidir: İkisi de başka bir nesneyi içinde tutar, onunla aynı arayüzü uygular ve çağrıları sarılmış nesneye iletir. Ancak tasarım kalıplarında yalnızca sınıf diyagramına bakmak yanıltıcı olabilir. İnce çizgiyi belirleyen şey yapı değil, **niyettir**: Decorator davranışı zenginleştirirken Proxy erişimi yönetir.
``
## Ortak yapı, farklı amaç

Her iki kalıpta da istemci gerçek nesne yerine aynı sözleşmeyi uygulayan bir sarmalayıcıyla konuşur. Temel ilişkiyi şöyle gösterebiliriz:

$$Client \rightarrow Wrapper \rightarrow RealObject$$

Buradaki `Wrapper`, Decorator olduğunda çağrıdan önce veya sonra yeni sorumluluklar ekler. Proxy olduğunda ise çağrının gerçekleşip gerçekleşmeyeceğine, ne zaman gerçekleşeceğine ya da hangi koşullarda gerçekleşeceğine karar verir.

Bir çağrının toplam maliyetini kabaca şu şekilde düşünebiliriz:

$$T_{toplam} = T_{kontrol} + T_{gerçek\ işlem} + T_{ek\ davranış}$$

Decorator çoğunlukla $T_{ek\ davranış}$ kısmını büyütür; örneğin sıkıştırma, şifreleme veya biçimlendirme ekler. Proxy ise $T_{kontrol}$ kısmına odaklanır; yetkilendirme, önbellekleme veya tembel yükleme yapabilir.

| Özellik | Decorator | Proxy |
|---|---|---|
| Temel niyet | Yeni davranış eklemek | Erişimi kontrol etmek |
| Nesne genellikle hazır mı? | Evet | Her zaman değil |
| Birden fazla katman | Çok yaygın | Mümkün, fakat ikincil |
| Tipik örnek | Şifreleme, sıkıştırma | Yetki, cache, lazy loading |
| İstemci açısından | Yetenekler artar | Erişim biçimi değişir |

![dekorator-ve-proxy-50](/img/dekorator-ve-proxy-50.svg)


## Decorator: Nesneyi yetenekli hâle getirmek

Aşağıdaki Java örneğinde temel bildirime önce yıldız, ardından ünlem ekleyen iki dekoratör bulunuyor:

```java
interface Message {
    String render();
}

class PlainMessage implements Message {
    public String render() {
        return "Merhaba";
    }
}

abstract class MessageDecorator implements Message {
    protected final Message wrapped;

    protected MessageDecorator(Message wrapped) {
        this.wrapped = wrapped;
    }
}

class BoldDecorator extends MessageDecorator {
    BoldDecorator(Message wrapped) {
        super(wrapped);
    }

    public String render() {
        return "**" + wrapped.render() + "**";
    }
}

class ExcitedDecorator extends MessageDecorator {
    ExcitedDecorator(Message wrapped) {
        super(wrapped);
    }

    public String render() {
        return wrapped.render() + "!";
    }
}
```

Kullanımda dekoratörler LEGO parçaları gibi birleştirilebilir:

```java
Message message = new ExcitedDecorator(
    new BoldDecorator(new PlainMessage())
);
System.out.println(message.render()); // **Merhaba**!
```

Gerçek nesneye erişim engellenmez; aksine çıktısı adım adım geliştirilir. Kalıtımla onlarca alt sınıf üretmek yerine davranışlar çalışma anında bir araya getirilir.

## Proxy: Kapıdaki görevli

Proxy aynı arayüzü korur, fakat asıl nesneye ulaşmadan önce kuralları uygular. Aşağıdaki koruma proxy’si yalnızca yönetici rolüne izin verir:

```java
interface ReportService {
    String readReport();
}

class RealReportService implements ReportService {
    public String readReport() {
        return "Gizli finans raporu";
    }
}

class SecureReportProxy implements ReportService {
    private final String role;
    private RealReportService service;

    SecureReportProxy(String role) {
        this.role = role;
    }

    public String readReport() {
        if (!"ADMIN".equals(role)) {
            throw new SecurityException("Erişim reddedildi");
        }
        if (service == null) {
            service = new RealReportService();
        }
        return service.readReport();
    }
}
```

Burada Proxy iki görev üstlenir: yetki kontrolü yapar ve pahalı olabileceği varsayılan gerçek servisi ihtiyaç doğana kadar oluşturmaz. Uzak sunucuyu temsil eden **remote proxy**, nesneyi geç oluşturan **virtual proxy** ve izinleri denetleyen **protection proxy** aynı fikrin farklı yüzleridir.

## Hangisini seçmeliyiz?

Kendinize şu soruyu sorun: “Bu sarmalayıcıyı kaldırırsam nesne yalnızca bir yeteneğini mi kaybeder, yoksa erişim politikası mı ortadan kalkar?” İlk durumda Decorator, ikinci durumda Proxy kullanıyorsunuz demektir.

Aynı sınıf teknik olarak hem loglama ekleyip hem erişim kontrol edebilir; fakat bu, sorumlulukları bulanıklaştırır. Daha temiz tasarımda Proxy kapıyı korur, Decorator ise içeri giren nesneye pelerin takar. Biri fedai, diğeri stil danışmanıdır; ikisi de sarar ama aynı nedenle değil!

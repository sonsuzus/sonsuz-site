---
layout: post
title: "Java Paketler ve Arayüzler: Düzenli Koddan Esnek Mimariye"
math: true
categories: 
  - Bilgi
tags: 
  - java
  - paketler
  - arayüzler
  - oop
  - yazılım-mimarisi
toc: true
image: /img/java-paketler-ve-68.png
---

Java projesi büyüdükçe sınıfları aynı klasöre doldurmak, çorap çekmecesinde USB kablosu aramaya benzer. Paketler kodu anlamlı bölümlere ayırırken arayüzler sınıfların hangi davranışları sunacağını tanımlar. Böylece hem düzenli hem de farklı implementasyonlara açık bir mimari kurulur.
``
## Paketler neden gereklidir?

Paket, ilişkili sınıfları, arayüzleri ve diğer türleri gruplandıran bir ad alanıdır. Örneğin bir e-ticaret uygulamasında ödeme kodları `com.magaza.payment`, kullanıcı işlemleri ise `com.magaza.user` altında tutulabilir.

Paketlerin sağladığı temel avantajlar şunlardır:

- Aynı isimli sınıflar arasındaki çakışmaları önler.
- Erişim kontrolüne katkı sağlar.
- Projenin mimari katmanlarını görünür hâle getirir.
- Kodun bakımını ve yeniden kullanımını kolaylaştırır.

Bir sınıfın paket bildirimi dosyanın ilk anlamlı satırında yer alır:

```java
package com.magaza.payment;

public class CreditCardPayment {
    public void pay(double amount) {
        System.out.println(amount + " TL kartla ödendi.");
    }
}
```

Başka bir paketteki sınıf `import` ile kullanılabilir:

```java
package com.magaza.app;

import com.magaza.payment.CreditCardPayment;

public class Main {
    public static void main(String[] args) {
        CreditCardPayment payment = new CreditCardPayment();
        payment.pay(750.0);
    }
}
```

`java.lang` paketi otomatik içe aktarılır; `String` ve `Math` için ayrıca `import` yazılmamasının nedeni budur. `import`, sınıfı kopyalamaz; yalnızca derleyiciye kısa adın hangi türe ait olduğunu söyler.

| Özellik | Paket | Klasör |
|---|---|---|
| Temel amacı | Ad alanı ve erişim düzeni sağlamak | Dosyaları fiziksel olarak saklamak |
| Java tarafından anlamlı mı? | Evet | Paket yapısıyla eşleştiğinde |
| Kullanımı | `package`, `import` | Dosya sistemi araçları |
| Çakışmayı önler mi? | Evet | Tek başına hayır |

İyi bir projede paket adı klasör yapısıyla eşleşir. Örneğin `com.magaza.payment` paketi genellikle `com/magaza/payment` dizininde bulunur.

## Arayüz: Davranış sözleşmesi

Java, bir sınıfın birden fazla sınıftan kalıtım almasına izin vermez. Yani `class C extends A, B` geçersizdir. Bunun önemli nedenlerinden biri, aynı metodun iki üst sınıfta farklı uygulanması hâlinde oluşan belirsizliktir. Bu problem genellikle elmas problemi olarak bilinir.

Arayüzler ise implementasyon mirasından çok davranış sözleşmesi sunar. Bir sınıf yalnızca bir sınıfı genişletebilir fakat birden fazla arayüzü uygulayabilir:

```java
interface Payable {
    void pay(double amount);
}

interface Refundable {
    void refund(double amount);
}

class BankTransfer implements Payable, Refundable {
    @Override
    public void pay(double amount) {
        System.out.println("Havale ile ödeme: " + amount);
    }

    @Override
    public void refund(double amount) {
        System.out.println("İade edilen tutar: " + amount);
    }
}
```

Buradaki ilişkiyi küme mantığıyla düşünürsek, `BankTransfer` türü iki davranış kümesinin kesişimindedir:

$$BankTransfer \in Payable \cap Refundable$$

Bu yaklaşım polimorfizmi mümkün kılar. Kod, somut sınıfa değil arayüze bağımlı olur:

```java
public class CheckoutService {
    public void complete(Payable method, double amount) {
        method.pay(amount);
    }
}
```

`CheckoutService`, ödemenin kartla mı, havaleyle mi yoksa gelecekte eklenecek sihirli bir cüzdanla mı yapıldığını bilmez. Yalnızca `Payable` sözleşmesine güvenir.

| Sınıf | Arayüz |
|---|---|
| Durum ve davranış taşıyabilir | Öncelikle davranış sözleşmesi tanımlar |
| Tek sınıftan kalıtım alınabilir | Birden fazla arayüz uygulanabilir |
| Nesnesi üretilebilir | Doğrudan nesnesi üretilemez |
| `extends` ile genişletilir | `implements` ile uygulanır |

Arayüzlerde `default` ve `static` metotlar da bulunabilir. İki arayüz aynı imzalı `default` metodu sağlarsa sınıf bu metodu ezerek belirsizliği çözmelidir. Dolayısıyla arayüzler çoklu davranış kazandırır, ancak mimari karar verme sorumluluğunu ortadan kaldırmaz.

Sonuç olarak paketler projenin haritasını, arayüzler ise trafik kurallarını oluşturur. Paketleri iş alanlarına göre tasarlamak ve somut sınıflar yerine arayüzlere bağımlı olmak; düşük bağımlılık, kolay test ve genişletilebilirlik sağlar.

![java-paketler-ve-68](/img/java-paketler-ve-68.svg)


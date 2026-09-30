---
layout: post
title: "SOLID'in O'su: Açık/Kapalı Prensibini Polimorfizmle Uygulamak"
math: true
categories: 
  - Bilgi
tags: 
  - solid
  - açık-kapalı-prensibi
  - polimorfizm
  - nesne-yönelimli-programlama
  - typescript
  - yazılım-tasarımı
toc: true
image: /img/solidin-osu-acikkapali-60.png
---

Bir uygulamaya yeni özellik eklemek bazen küçük bir değişiklik gibi başlar, ardından onlarca `if` bloğuna dokunulan riskli bir operasyona dönüşür. SOLID ilkelerinin O harfiyle temsil edilen Açık/Kapalı Prensibi, yazılım bileşenlerinin **genişletilmeye açık, değiştirilmeye kapalı** olmasını önererek bu soruna çözüm getirir. Amaç mevcut kodu sonsuza kadar dondurmak değil, yeni davranışları mümkün olduğunca yeni kod yazarak sisteme katabilmektir.
``
## Prensibin teorik temeli

Open/Closed Principle, Bertrand Meyer tarafından ortaya atılmıştır. Basit ifadesi şöyledir:

> Bir yazılım varlığı genişletilmeye açık, değiştirilmeye kapalı olmalıdır.

Buradaki yazılım varlığı bir sınıf, fonksiyon, modül veya servis olabilir. Yeni bir gereksinim geldiğinde çalışan ve test edilmiş kodu sürekli değiştirmek hata olasılığını artırır. Bunu kabaca şöyle düşünebiliriz:

$$R \propto D \times B$$

Burada $R$ değişiklik riski, $D$ dokunulan mevcut kod miktarı, $B$ ise bu kodun bağımlılık sayısıdır. Bu kesin bir mühendislik formülü değildir; fakat daha fazla bağımlılığı olan daha fazla satıra dokundukça regresyon riskinin büyüdüğünü güzelce anlatır.

| Yaklaşım | Yeni özellik ekleme | Regresyon riski | Bağımlılık |
|---|---|---|---|
| Koşul blokları | Mevcut kod değiştirilir | Yüksek | Somut türlere |
| Polimorfik tasarım | Yeni sınıf eklenir | Daha düşük | Soyutlamaya |
| Dev `switch` yapısı | Her türde güncellenir | Orta-yüksek | Tür listesine |

![solidin-osu-acikkapali-60](/img/solidin-osu-acikkapali-60.svg)


## OCP'yi ihlal eden örnek

Bir ödeme servisinin yalnızca kredi kartını desteklediğini, daha sonra havale seçeneğinin geldiğini düşünelim:

```typescript
class PaymentService {
  pay(type: string, amount: number): void {
    if (type === 'credit-card') {
      console.log(`Karttan ${amount} TL çekildi.`);
    } else if (type === 'bank-transfer') {
      console.log(`${amount} TL havale ile ödendi.`);
    }
  }
}
```

Her yeni ödeme yönteminde `PaymentService` değiştirilir. Kripto para, dijital cüzdan ve kapıda ödeme geldikçe sınıf bir koşul koleksiyonuna dönüşür. Üstelik ödeme yöntemlerinin kendilerine özgü doğrulama adımları da aynı yerde birikmeye başlar.

## Polimorfizmle genişletilebilir tasarım

Çözüm, değişen davranışı bir soyutlamanın arkasına taşımaktır. TypeScript'te bunun için bir arayüz kullanabiliriz:

```typescript
interface PaymentMethod {
  pay(amount: number): void;
}

class CreditCardPayment implements PaymentMethod {
  pay(amount: number): void {
    console.log(`Karttan ${amount} TL çekildi.`);
  }
}

class BankTransferPayment implements PaymentMethod {
  pay(amount: number): void {
    console.log(`${amount} TL havale ile ödendi.`);
  }
}

class PaymentService {
  constructor(private readonly method: PaymentMethod) {}

  process(amount: number): void {
    this.method.pay(amount);
  }
}
```

`PaymentService` artık ödemenin nasıl yapıldığını bilmez; yalnızca `PaymentMethod` sözleşmesini kullanır. Bu durum aynı zamanda bağımlılıkların somut sınıflar yerine soyutlamalara yönelmesini sağlar.

Yeni bir dijital cüzdan desteği eklemek için mevcut servise dokunmayız:

```typescript
class DigitalWalletPayment implements PaymentMethod {
  pay(amount: number): void {
    console.log(`Cüzdandan ${amount} TL ödendi.`);
  }
}

const method = new DigitalWalletPayment();
const service = new PaymentService(method);
service.process(250);
```

Sistem yeni sınıfla genişletilmiş, mevcut ödeme servisi ise değiştirilmemiştir. Polimorfizmin sihri de burada ortaya çıkar: Servis çalışma anında hangi somut nesneyi aldığından bağımsız olarak aynı sözleşme üzerinden davranır.

## Her koşulu sınıfa çevirmeli miyiz?

Hayır. OCP, iki satırlık sabit bir koşul için on sınıf üretme yarışması değildir. Davranışın sık değişmesi, yeni türlerin düzenli eklenmesi veya koşulların karmaşıklaşması güçlü birer işarettir.

| Durum | Tercih |
|---|---|
| Sabit ve basit iki seçenek | Koşul yeterli olabilir |
| Sürekli eklenen davranışlar | Polimorfizm uygundur |
| Algoritmalar çalışma anında değişiyor | Strategy deseni düşünülebilir |
| Nesne üretimi karmaşıklaşıyor | Factory kullanılabilir |

İyi OCP uygulaması geleceği kusursuz tahmin etmekten çok, **değişken noktaları doğru belirlemekle** ilgilidir. Bir gereksinim ailesi büyüyorsa onu arayüzle sınırlandırmak, sınıfları küçük tutmak ve bağımlılık enjeksiyonu kullanmak sistemi daha güvenli genişletir. Böylece yeni özellik geldiğinde eski kod korkuyla açılan bir sandık değil, yeni parçaların kolayca takıldığı sağlam bir LEGO tabanı olur.

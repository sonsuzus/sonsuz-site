---
layout: post
title: "Soyut Veri Tipleri: İçeriyi Gizle, Güvenli Arayüzler Tasarla"
math: true
categories: 
  - Bilgi
tags: 
  - soyut veri tipleri
  - adt
  - veri yapıları
  - kapsülleme
  - arayüz tasarımı
  - typescript
toc: true
image: /img/soyut-veri-tipleri-24.png
---

Bir kahve makinesini kullanmak için içindeki pompanın basıncını veya ısıtıcının devresini bilmemiz gerekmez; düğmeye basar, kahvemizi alırız. Soyut Veri Tipleri de benzer biçimde çalışır: Kullanıcıya **ne yapılabileceğini** gösterirken bunun **nasıl yapıldığını** gizler. Böylece veri yapıları daha güvenli, değiştirilebilir ve anlaşılır hâle gelir.
``
## Soyut Veri Tipi nedir?

Soyut Veri Tipi veya kısaca **ADT (Abstract Data Type)**, bir veri koleksiyonunu yalnızca değerleri ve izin verilen işlemleri üzerinden tanımlar. ADT, doğrudan bir sınıf ya da belirli bir kod parçası değildir; daha çok uygulanması gereken davranışsal bir sözleşmedir.

Bir ADT kabaca şu bileşenlerle ifade edilebilir:

$$ADT = (D, O, A)$$

Burada $D$ olası değerler kümesini, $O$ sunulan işlemleri, $A$ ise bu işlemlerin uyması gereken kuralları belirtir. Örneğin yığın ADT'sinde `push`, `pop`, `peek` ve `isEmpty` işlemleri bulunur. Ancak elemanların bir diziyle mi, bağlı listeyle mi tutulduğu sözleşmenin parçası değildir.

| Kavram | Cevapladığı soru | Yığın örneği |
|---|---|---|
| Arayüz | Ne yapabilirim? | `push`, `pop`, `peek` |
| Uygulama | Nasıl yapılıyor? | Dizi veya bağlı liste |
| Değişmez | Her zaman ne doğru kalmalı? | Eleman sayısı negatif olamaz |
| İstemci | ADT'yi kim kullanır? | Uygulama kodu |

![soyut-veri-tipleri-24](/img/soyut-veri-tipleri-24.svg)


## Temsil bağımsızlığı ve kapsülleme

ADT tasarımının süper gücü **temsil bağımsızlığıdır**. İstemci kodu iç depolama biçimine erişemiyorsa uygulama daha sonra değiştirilebilir. Başlangıçta dizi kullanan bir yığın, performans ihtiyacı nedeniyle bağlı listeye geçirilebilir; arayüz aynı kaldığı sürece kullanıcı bunu fark etmez.

İç veriyi doğrudan dışarı açmak ise değişmezlerin bozulmasına yol açar. Örneğin istemci yığının eleman dizisini temizleyip sayaç değerini değiştirmezse nesne tutarsız hâle gelir. Bu nedenle veri `private`, güvenli işlemler ise `public` tutulmalıdır.

```typescript
interface Stack<T> {
  push(value: T): void;
  pop(): T;
  peek(): T;
  isEmpty(): boolean;
  size(): number;
}

class ArrayStack<T> implements Stack<T> {
  private items: T[] = [];

  push(value: T): void {
    this.items.push(value);
  }

  pop(): T {
    if (this.isEmpty()) {
      throw new Error("Boş yığından eleman çıkarılamaz");
    }
    return this.items.pop() as T;
  }

  peek(): T {
    if (this.isEmpty()) {
      throw new Error("Boş yığının tepesi yoktur");
    }
    return this.items[this.items.length - 1];
  }

  isEmpty(): boolean {
    return this.items.length === 0;
  }

  size(): number {
    return this.items.length;
  }
}
```

Bu kodda `Stack<T>` davranış sözleşmesini, `ArrayStack<T>` ise dizi tabanlı uygulamayı temsil eder. `items` alanının özel olması, istemcinin yığını kuralları atlayarak değiştirmesini engeller.

## Ön koşullar, son koşullar ve değişmezler

Güvenli bir arayüz tasarlanırken her işlem için üç soru sorulabilir:

- **Ön koşul:** İşlem çağrılmadan önce ne doğru olmalı?
- **Son koşul:** İşlem tamamlandığında ne garanti edilir?
- **Değişmez:** Nesnenin ömrü boyunca hangi kural korunur?

Yığın için `pop` işleminin ön koşulu $size > 0$ olabilir. Başarılı işlemden sonra:

$$size_{sonra} = size_{önce} - 1$$

Ayrıca LIFO kuralı gereği son eklenen eleman ilk çıkar. Ön koşul sağlanmadığında sessizce `undefined` döndürmek yerine açık bir hata üretmek, hatanın kaynağını görünür kılar.

| Zayıf tasarım | Güvenli ADT tasarımı |
|---|---|
| İç koleksiyonu dışarı açar | Kontrollü metotlar sunar |
| Belirsiz hata davranışı vardır | Hata sözleşmesi tanımlıdır |
| Uygulamaya bağımlıdır | Temsil bağımsızdır |
| Her işi tek metotta toplar | Küçük ve anlamlı işlemler kullanır |

## İyi bir ADT için kısa kontrol listesi

Arayüzü mümkün olduğunca küçük tutun, metotlara niyet belirten adlar verin ve iç nesnelerin değiştirilebilir kopyalarını dışarı sızdırmayın. Geçersiz durumları mümkünse oluşturulamaz hâle getirin; mümkün değilse girişleri doğrulayın. Son olarak testleri iç diziye göre değil, gözlemlenebilir davranışa göre yazın.

Özetle ADT tasarlamak yalnızca veriyi saklamak değildir. Asıl amaç, yanlış kullanımı zorlaştıran ve uygulama ayrıntılarının özgürce değişmesine izin veren bir sözleşme kurmaktır. İyi bir ADT, kullanıcıya düğmeleri gösterir; kablo karmaşasını ise kapağın altında bırakır.

---
layout: post
title: "Java’da enum, Autoboxing ve Anotasyonlar: Tip Sisteminin Güçlü Üçlüsü"
math: true
categories: 
  - Bilgi
tags: 
  - java
  - enum
  - autoboxing
  - anotasyon
  - metadata
  - reflection
toc: true
image: /img/javada-enum-autoboxing-17.png
---

Java yalnızca sınıflardan ve metotlardan ibaret değildir; dilin tip güvenliğini artıran `enum`, ilkel tiplerle nesneler arasında köprü kuran autoboxing ve koda metadata ekleyen anotasyonlar da önemli oyunculardır. Bu üç yapı doğru kullanıldığında kod daha okunabilir, güvenli ve otomasyona uygun hâle gelir. Yanlış kullanıldıklarında ise özellikle `null`, karşılaştırma ve reflection kaynaklı küçük sürprizler hazırlayabilirler.

``

## Güçlü numaralandırmalar: enum

Bir değer yalnızca belirli seçeneklerden biri olabiliyorsa `String` veya rastgele sayılar yerine `enum` kullanmak daha güvenlidir. Örneğin sipariş durumunu `"HAZIRLANIYOR"` şeklinde saklamak yazım hatalarına açıktır. `enum` ise derleyicinin kontrol edebildiği sınırlı bir değer kümesi oluşturur.

Matematiksel olarak bir enum, sonlu bir küme gibi düşünülebilir:

$$Durum = \{BEKLIYOR, HAZIRLANIYOR, GONDERILDI, IPTAL\}$$

Java enum’ları basit sabit listelerinden daha güçlüdür. Alan, kurucu metot ve davranış taşıyabilirler:

```java
public enum SiparisDurumu {
    BEKLIYOR("Sipariş sırada", false),
    HAZIRLANIYOR("Mutfak çalışıyor", false),
    GONDERILDI("Kurye yolda", true),
    IPTAL("Sipariş iptal edildi", true);

    private final String aciklama;
    private final boolean sonDurum;

    SiparisDurumu(String aciklama, boolean sonDurum) {
        this.aciklama = aciklama;
        this.sonDurum = sonDurum;
    }

    public String getAciklama() {
        return aciklama;
    }

    public boolean isSonDurum() {
        return sonDurum;
    }
}
```

Bu örnek, durumla ilgili veriyi farklı `if` bloklarına dağıtmak yerine doğrudan enum içinde toplar. Enum değerleri tekil nesneler olduğundan `==` ile güvenle karşılaştırılabilir. Dış sistemlerden gelen metinleri `valueOf()` ile dönüştürürken geçersiz değerlerin `IllegalArgumentException` üreteceği unutulmamalıdır.

| Yaklaşım | Tip güvenliği | Davranış taşıma | Yazım hatası riski |
|---|---:|---:|---:|
| `String` sabitleri | Düşük | Hayır | Yüksek |
| Sayısal sabitler | Düşük | Hayır | Orta |
| `enum` | Yüksek | Evet | Düşük |

![javada-enum-autoboxing-17](/img/javada-enum-autoboxing-17.svg)


## Autoboxing ve unboxing

Java’nın `int`, `double` ve `boolean` gibi ilkel tipleri nesne değildir. Koleksiyonlar ise nesne bekler. Autoboxing, ilkel değeri karşılık gelen sarmalayıcı sınıfa otomatik dönüştürür; unboxing bunun tersidir.

```java
List<Integer> puanlar = new ArrayList<>();
puanlar.add(90);          // int -> Integer: autoboxing
int ilkPuan = puanlar.get(0); // Integer -> int: unboxing
```

Derleyici zihninde yaklaşık olarak şu dönüşüm gerçekleşir:

$$int \xrightarrow{boxing} Integer$$
$$Integer \xrightarrow{unboxing} int$$

| İlkel tip | Sarmalayıcı sınıf |
|---|---|
| `int` | `Integer` |
| `long` | `Long` |
| `double` | `Double` |
| `boolean` | `Boolean` |
| `char` | `Character` |

Kolaylık güzel olsa da `null` değer unboxing sırasında `NullPointerException` üretir:

```java
Integer adet = null;
// int toplam = adet + 1; // Unboxing sırasında hata oluşur
```

Ayrıca `Integer` nesnelerini `==` ile karşılaştırmak tehlikelidir. Java bazı küçük sayıları önbelleğe aldığı için sonuçlar şaşırtıcı olabilir. Değer karşılaştırmasında `equals()` kullanılmalıdır. Yoğun döngülerde gereksiz boxing işlemleri ek nesne maliyeti de oluşturabilir.

## Anotasyonlar: Kodun üzerine iliştirilen metadata

Anotasyonlar doğrudan iş mantığını çalıştırmaz; derleyiciye, araçlara veya çalışma zamanı kütüphanelerine ek bilgi verir. `@Override`, metodun üst sınıftaki bir metodu ezdiğini doğrulatır. Spring’deki `@Service` veya JPA’deki `@Entity` ise framework davranışlarını yönlendirir.

Kendi anotasyonumuzu da oluşturabiliriz:

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface YetkiGerekli {
    String rol();
}
```

Buradaki `@Retention`, bilginin çalışma zamanına kadar korunacağını; `@Target` ise yalnızca metotlarda kullanılabileceğini belirtir. Ardından `@YetkiGerekli(rol = "ADMIN")` biçiminde işaretlenen metotlar reflection ile bulunabilir ve çağrıdan önce yetki kontrolü yapılabilir.

| Saklama politikası | Ne zamana kadar yaşar? | Yaygın amaç |
|---|---|---|
| `SOURCE` | Derleme öncesi | Kod üretimi, analiz |
| `CLASS` | Bytecode içinde | Araç desteği |
| `RUNTIME` | Çalışma zamanı | Reflection, framework |

Özetle enum değer alanını sınırlar, autoboxing ilkel ve nesne dünyalarını yakınlaştırır, anotasyonlar ise kod hakkında kod dışı bilgi taşır. Üçü birlikte kullanıldığında Java uygulamaları daha açıklayıcı, denetlenebilir ve framework dostu olur.

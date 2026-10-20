---
layout: post
title: "Java İstisna Yönetimi: try, catch ve finally ile Güvenli Kod"
math: true
categories: 
  - Bilgi
tags: 
  - java
  - exception
  - hata-yönetimi
  - try-catch
  - finally
  - programlama
toc: true
image: /img/java-istisna-yonetimi-75.png
---

Bir uygulamada her şey planlandığı gibi gitmez: Dosya bulunamaz, kullanıcı sayı yerine metin girer veya ağ bağlantısı aniden kesilir. Java istisna yönetimi, bu beklenmeyen durumları kontrollü biçimde karşılayarak programın dramatik bir şekilde sahneden düşmesini engeller. Amaç hataları gizlemek değil; onları anlamlı, izlenebilir ve güvenli bir akış içinde yönetmektir.
``
## İstisna nedir?

İstisna, programın normal çalışma akışını bozan bir olaydır. Java’da istisnalar nesne olarak temsil edilir ve temel olarak `Throwable` sınıfından türetilir. Bir sorun oluştuğunda istisna “fırlatılır”; uygun bir yönetici bulunduğunda ise “yakalanır”.

Bu davranışı basitçe şöyle düşünebiliriz:

$$
\text{Güvenli Akış} = \text{Riskli İşlem} + \text{Hata Yakalama} + \text{Temizlik}
$$

Java’daki hata hiyerarşisinin iki önemli kolu vardır:

| Tür | Açıklama | Örnek |
|---|---|---|
| Checked exception | Derleyicinin yönetilmesini zorunlu tuttuğu istisnalardır | `IOException`, `SQLException` |
| Unchecked exception | Genellikle programlama hatalarından doğar | `NullPointerException`, `ArithmeticException` |
| Error | Uygulamanın çoğunlukla düzeltemeyeceği ciddi JVM sorunlarıdır | `OutOfMemoryError` |

![java-istisna-yonetimi-75](/img/java-istisna-yonetimi-75.svg)


## try ve catch nasıl çalışır?

Risk oluşturabilecek kod `try` bloğuna yazılır. Bir istisna meydana gelirse Java, ilgili türü karşılayan `catch` bloğunu arar. Böylece uygulama tamamen sonlanmak yerine alternatif bir davranış gösterebilir.

```java
public class BolmeOrnegi {
    public static void main(String[] args) {
        int bolunen = 24;
        int bolen = 0;

        try {
            int sonuc = bolunen / bolen;
            System.out.println("Sonuç: " + sonuc);
        } catch (ArithmeticException e) {
            System.out.println("Bir sayı sıfıra bölünemez.");
            System.out.println("Teknik ayrıntı: " + e.getMessage());
        }

        System.out.println("Program çalışmaya devam ediyor.");
    }
}
```

Burada sıfıra bölme işlemi `ArithmeticException` üretir. `catch` bloğu hatayı yakalar, kullanıcıya anlaşılır bir mesaj verir ve programın sonraki satırlara devam etmesini sağlar.

Birden fazla hata türü için birden fazla `catch` kullanılabilir. Ancak özel istisnalar önce, daha genel olanlar sonra yazılmalıdır. Aksi hâlde genel blok diğerlerini erişilemez yapabilir.

## finally neden kullanılır?

`finally` bloğu, istisna oluşsa da oluşmasa da çalıştırılması gereken işlemler içindir. Dosya kapatmak, bağlantıyı sonlandırmak veya geçici kaynakları temizlemek klasik kullanım örnekleridir.

```java
try {
    System.out.println("Veritabanı işlemi başlatıldı.");
    // Riskli sorgular burada çalıştırılır.
} catch (RuntimeException e) {
    System.out.println("İşlem başarısız: " + e.getMessage());
} finally {
    System.out.println("Bağlantı ve kaynaklar temizleniyor.");
}
```

| Blok | Ne zaman çalışır? | Temel görevi |
|---|---|---|
| `try` | Her zaman ilk olarak | Riskli kodu çalıştırmak |
| `catch` | Eşleşen istisna oluşursa | Hatayı kontrollü biçimde ele almak |
| `finally` | Normalde her durumda | Kaynakları temizlemek |

Modern Java’da dosya ve benzeri `AutoCloseable` kaynaklar için `try-with-resources` daha güvenlidir:

```java
try (var okuyucu = new java.io.BufferedReader(
        new java.io.FileReader("veriler.txt"))) {
    System.out.println(okuyucu.readLine());
} catch (java.io.IOException e) {
    System.out.println("Dosya okunamadı: " + e.getMessage());
}
```

Bu yapı, okuyucuyu otomatik kapatır ve unutulan kaynaklar yüzünden oluşabilecek sızıntıları azaltır.

## Sağlam istisna yönetimi için ipuçları

- Boş bir `catch` bloğu kullanarak hatayı sessizce yutmayın.
- Kullanıcıya anlaşılır, geliştiriciye ayrıntılı günlük mesajları sağlayın.
- Yalnızca gerçekten yönetebileceğiniz istisnaları yakalayın.
- `Exception` gibi aşırı genel türleri gereksiz yere kullanmayın.
- İstisnaları normal karar mekanizması yerine koymayın.

İyi tasarlanmış istisna yönetimi, uygulamanın hiç hata vermemesi anlamına gelmez. Asıl başarı; hata geldiğinde paniklemeyen, kaynaklarını temizleyen, kullanıcıyı bilgilendiren ve mümkünse güvenli biçimde yoluna devam eden bir sistem kurmaktır.

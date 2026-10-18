---
layout: post
title: "Java Tarihçesi ve Evrimi: Oak Ağacından JVM Dünyasına"
math: true
categories: 
  - Bilgi
tags: 
  - java
  - jvm
  - bayt-kod
  - programlama-tarihi
  - sanal-makine
  - nesne-yönelimli-programlama
toc: true
image: /img/java-tarihcesi-ve-53.png
---

Java, bugün kurumsal uygulamalardan Android ekosistemine kadar pek çok alanda karşımıza çıksa da yolculuğuna web için değil, etkileşimli elektronik cihazlar için başladı. Dilin asıl başarısı yalnızca sözdiziminden kaynaklanmadı; farklı donanımlarda aynı programı çalıştırmayı hedefleyen taşınabilir mimarisi, yazılım dünyasının önemli problemlerinden birine güçlü bir cevap verdi.

``

## Green Project ve Oak’ın Doğuşu

Java’nın hikâyesi 1991 yılında Sun Microsystems bünyesindeki **Green Project** ile başladı. James Gosling, Mike Sheridan ve Patrick Naughton gibi mühendisler, televizyon kutuları ve ev cihazları için güvenilir bir yazılım platformu geliştirmeye çalışıyordu. C ve C++ güçlüydü; ancak donanıma bağımlılık, elle bellek yönetimi ve işaretçi hataları bu cihazlar için ciddi risk oluşturuyordu.

Gosling tarafından geliştirilen dil önce, ofisinin önündeki ağaçtan esinlenilerek **Oak** adını aldı. Oak isminin başka bir şirket tarafından tescillenmiş olması nedeniyle dilin adı daha sonra Java olarak değiştirildi. Projenin cihaz pazarı beklenen hızda büyümese de internetin yükselişi, taşınabilir kod fikrine yeni bir sahne hazırladı. Java, 1995 yılında resmen tanıtıldı.

Java’nın temel felsefesi şu sloganla özetlendi: **Write Once, Run Anywhere** — bir kez yaz, her yerde çalıştır.

| Özellik | C/C++ yaklaşımı | Java yaklaşımı |
|---|---|---|
| Derleme hedefi | Belirli işlemci ve işletim sistemi | JVM üzerinde çalışan bayt kod |
| Bellek yönetimi | Çoğunlukla geliştiriciye ait | Garbage Collector tarafından yönetilir |
| İşaretçiler | Doğrudan kullanılabilir | Güvenli referans modeli kullanılır |
| Taşınabilirlik | Yeniden derleme gerekebilir | Uygun JVM yeterlidir |
| Güvenlik | Ortama ve koda bağlıdır | Doğrulama ve çalışma zamanı kontrolleri vardır |

![java-tarihcesi-ve-53](/img/java-tarihcesi-ve-53.svg)


## Kaynak Koddan Bayt Koda

Java derleyicisi, kaynak kodunu doğrudan belirli bir işlemcinin makine diline dönüştürmez. Bunun yerine JVM’nin anlayabileceği ara temsil olan **bayt kodu** üretir.

```java
public class MerhabaJVM {
    public static void main(String[] args) {
        int javaYasi = 2026 - 1995;
        System.out.println("Java yaklaşık " + javaYasi + " yaşında!");
    }
}
```

Bu sınıf şu komutla derlenir:

```bash
javac MerhabaJVM.java
java MerhabaJVM
```

`javac` komutu kaynak dosyadan `MerhabaJVM.class` dosyasını üretir. Bu dosya işlemciye özel makine kodu değil, JVM komutları içerir. `javap -c MerhabaJVM` komutu kullanılarak bayt kod talimatları incelenebilir.

Süreci matematiksel bir dönüşüm gibi gösterebiliriz:

$$
Kaynak\ Kod \xrightarrow{javac} Bayt\ Kod \xrightarrow{JVM} Makine\ Kodu
$$

Aynı `.class` dosyasının farklı sistemlerde çalışabilmesinin koşulu, her sistem için uygun bir JVM bulunmasıdır. Dolayısıyla taşınabilir olan JVM’nin kendisi değil, JVM üzerinde çalışacak şekilde üretilen bayt koddur.

## JVM Tam Olarak Ne Yapar?

**Java Virtual Machine**, fiziksel işlemci ile Java programı arasında soyut bir bilgisayar gibi davranır. Sınıfları yükler, bayt kodunu doğrular, belleği düzenler ve kodu çalıştırır. JVM’nin başlıca bileşenleri şunlardır:

- **Class Loader:** Gerekli sınıfları çalışma anında yükler.
- **Bytecode Verifier:** Talimatların güvenli ve kurallara uygun olduğunu denetler.
- **Execution Engine:** Bayt kodu yorumlar veya makine koduna dönüştürür.
- **Garbage Collector:** Kullanılmayan nesnelerin belleğini otomatik olarak geri kazanır.
- **Runtime Data Areas:** Heap, stack ve metot alanı gibi bellek bölgelerini yönetir.

İlk JVM’ler bayt kodu çoğunlukla yorumluyordu. Modern JVM’lerdeki **JIT derleyici**, sık çalışan kod bölümlerini çalışma sırasında yerel makine koduna çevirir. Basitleştirilmiş performans fikri şöyle ifade edilebilir:

$$
T_{toplam} = T_{yükleme} + T_{JIT} + n \cdot T_{çalıştırma}
$$

Başlangıçta JIT maliyeti oluşsa da tekrar sayısı $n$ büyüdükçe optimize edilmiş kod önemli hız kazandırır.

## Java’nın Evrimi

Java zaman içinde yalnızca bir dil olmaktan çıkıp büyük bir platforma dönüştü. Java 5 generics ve annotation özelliklerini, Java 8 lambda ifadelerini ve Stream API’yi getirdi. Java 9 modül sistemini tanıttı; sonraki sürümler record, sealed class, pattern matching ve virtual thread gibi modern yetenekler ekledi.

Bugün Java’nın gücü; olgun kütüphane ekosistemi, geriye dönük uyumluluk yaklaşımı ve JVM’nin gelişmiş optimizasyonlarında yatıyor. Üstelik Kotlin, Scala ve Clojure gibi diller de JVM üzerinde çalışabiliyor. Kısacası Oak’ın küçük cihazlar için filizlenen fikri, milyonlarca uygulamayı taşıyan oldukça büyük bir ormana dönüştü.

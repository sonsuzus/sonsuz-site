---
layout: post
title: "Java I/O ve NIO: Dosyalardan Asenkron Kanallara Veri Yolculuğu"
math: true
categories: 
  - Bilgi
tags: 
  - java
  - io
  - nio
  - dosya-işlemleri
  - asenkron-programlama
  - performans
toc: true
image: /img/java-io-ve-94.png
---

Java’da veri okumak veya yazmak, ilk bakışta bir dosyayı açıp birkaç baytı taşımaktan ibaret görünebilir. Ancak işin içine büyük dosyalar, ağ bağlantıları ve binlerce eşzamanlı istemci girdiğinde I/O dünyası küçük bir performans laboratuvarına dönüşür. Klasik I/O akışları sadelik sunarken NIO; tamponlar, kanallar ve asenkron işlemlerle veri yolculuğunu daha verimli hâle getirir.

![java-io-ve-94](/img/java-io-ve-94.svg)

``

## Klasik Java I/O nasıl çalışır?

`java.io` paketi, veriyi bir **akış** üzerinden taşır. `InputStream` bayt okumak, `OutputStream` ise bayt yazmak için kullanılır. Metin tabanlı verilerde bunların karşılığı `Reader` ve `Writer` sınıflarıdır.

Akış modelinde veri genellikle sırayla okunur. Bir okuma işlemi tamamlanana kadar çalışan iş parçacığı bekleyebilir; buna **bloklayan I/O** denir. Basit uygulamalarda bu davranış anlaşılır ve yeterlidir.

```java
import java.io.*;
import java.nio.charset.StandardCharsets;

public class IoExample {
    public static void main(String[] args) throws IOException {
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(
                    new FileInputStream("notlar.txt"),
                    StandardCharsets.UTF_8))) {

            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        }
    }
}
```

Burada `BufferedReader`, dosyaya her karakter için ayrı ayrı erişmek yerine veriyi geçici bir belleğe alır. `try-with-resources` ise iş bitince akışın otomatik kapatılmasını sağlar.

## Tamponlama neden önemlidir?

Disk erişimi, RAM erişiminden çok daha yavaştır. Tampon kullanılmadan $n$ adet küçük okuma yapılırsa yaklaşık maliyet

$$T \approx n \times (t_{erişim} + t_{aktarım})$$

şeklinde düşünülebilir. Veriler $b$ büyüklüğündeki tamponlarla taşındığında erişim sayısı yaklaşık $\lceil n/b \rceil$ olur. Böylece işletim sistemi çağrıları azalır. Ancak devasa tamponlar da gereksiz bellek tüketebilir; yaygın başlangıç değerleri 8 KB ile 64 KB arasındadır.

| Yaklaşım | Veri birimi | Bekleme modeli | Uygun kullanım |
|---|---|---|---|
| `InputStream` / `OutputStream` | Bayt | Genellikle bloklayan | İkili dosyalar |
| `Reader` / `Writer` | Karakter | Genellikle bloklayan | Metin dosyaları |
| `BufferedReader` | Satır veya karakter | Bloklayan, tamponlu | Satır tabanlı metin |
| NIO Channel | Buffer | Bloklayan veya seçilebilir | Büyük dosya ve ağ işlemleri |
| Asynchronous Channel | Buffer | Bloklamayan | Yüksek eşzamanlılık |

## NIO: Buffer ve Channel ortaklığı

`java.nio` yaklaşımında veri doğrudan akıştan çekilmez. Bir **Channel**, veriyi bir `Buffer` içine yazar veya oradan okur. Buffer’ın `position`, `limit` ve `capacity` değerleri hangi bölümün kullanılabileceğini belirler.

```java
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.*;

public class NioCopy {
    public static void main(String[] args) throws Exception {
        try (FileChannel source = FileChannel.open(Path.of("girdi.bin"));
             FileChannel target = FileChannel.open(
                 Path.of("cikti.bin"),
                 StandardOpenOption.CREATE,
                 StandardOpenOption.WRITE,
                 StandardOpenOption.TRUNCATE_EXISTING)) {

            ByteBuffer buffer = ByteBuffer.allocate(8192);
            while (source.read(buffer) != -1) {
                buffer.flip();
                while (buffer.hasRemaining()) {
                    target.write(buffer);
                }
                buffer.clear();
            }
        }
    }
}
```

`flip()`, tamponu yazma modundan okuma moduna geçirir. `clear()` ise sonraki veri grubuna yer açar. Bu ikili unutulursa tampon, “Ben doluyum ama kimse beni anlamıyor!” diyerek uygulamayı şaşırtabilir.

## Files API ile daha kısa işlemler

Küçük dosyalarda düşük seviyeli kanallara ihtiyaç yoktur. `Files` sınıfı okunabilir ve güvenli yardımcı metotlar sunar:

```java
Path path = Path.of("ayarlar.txt");
Files.writeString(path, "mode=production");
String content = Files.readString(path);
```

Büyük dosyalarda `readString()` bütün içeriği belleğe yüklediğinden `Files.lines()` veya kanal tabanlı okuma tercih edilmelidir.

## Asenkron NIO.2

`AsynchronousFileChannel`, işlem sürerken çağıran iş parçacığının başka işler yapmasına izin verir. Sonuç bir `Future` ile alınabilir veya `CompletionHandler` kullanılarak olay tamamlandığında kod çalıştırılabilir.

```java
try (var channel = java.nio.channels.AsynchronousFileChannel.open(
        Path.of("veri.dat"), StandardOpenOption.READ)) {

    ByteBuffer buffer = ByteBuffer.allocate(1024);
    var future = channel.read(buffer, 0);

    System.out.println("Okuma sürerken başka işler yapılabilir.");
    int bytesRead = future.get();
    System.out.println("Okunan bayt: " + bytesRead);
}
```

Asenkron model her zaman daha hızlı değildir; avantajı, bekleyen iş parçacığı sayısını azaltmasıdır. Küçük komut satırı araçlarında klasik I/O yeterliyken yüksek trafikli sunucularda NIO ve asenkron kanallar daha ölçeklenebilir bir temel sağlar. Doğru seçim; veri boyutuna, eşzamanlı bağlantı sayısına ve kodun sürdürülebilirliğine bağlıdır.

---
layout: post
title: "Dart Isolate’leri: Tek İplikli Dünyada Arayüzü Dondurmadan Ağır İşler"
math: true
categories: 
  - Bilgi
tags: 
  - dart
  - flutter
  - isolate
  - eşzamanlılık
  - performans
  - asenkron programlama
toc: true
image: /img/dart-isolateleri-tek-94.png
---

Flutter uygulamanız akıcı biçimde kayarken bir JSON dosyasını ayrıştırmaya başladınız ve ekran aniden buza mı dönüştü? Suçlu çoğu zaman Dart değil, ağır işi arayüzün çalıştığı isolate üzerinde yapmamızdır. Dart isolate’leri; hesaplama, ayrıştırma ve veri dönüştürme gibi pahalı görevleri bağımsız çalışma alanlarına taşıyarak kullanıcı arayüzünün nefes almaya devam etmesini sağlar.
``
## Isolate tam olarak nedir?

Dart kodu varsayılan olarak tek bir **isolate** içinde çalışır. Her isolate’ın kendi belleği, olay döngüsü ve yürütme akışı vardır. Isolate’ler klasik thread’lerden farklı olarak değişkenleri doğrudan paylaşmaz. Birbirleriyle yalnızca mesaj göndererek haberleşirler.

Bu modelin önemli sonucu şudur: Paylaşılan belleğin olmadığı yerde kilit, mutex ve yarış durumu gibi dertler büyük ölçüde ortadan kalkar. Bunun karşılığında verilerin isolate’ler arasında kopyalanması veya aktarılması gerekir.

Bir işin toplam süresini kabaca şöyle düşünebiliriz:

$$T_{toplam} = T_{başlatma} + T_{aktarım} + T_{hesaplama}$$

Dolayısıyla iki sayıyı toplamak için isolate oluşturmak performansı artırmaz; başlatma maliyeti kazancı yutar. Isolate’ler, $T_{hesaplama}$ yeterince büyük olduğunda anlamlıdır.

| Özellik | `async` / `await` | Isolate |
|---|---|---|
| Çalışma alanı | Aynı isolate | Ayrı isolate |
| Bellek | Aynı bellek | Bağımsız bellek |
| Uygun görev | Ağ, dosya, veritabanı bekleme | CPU ağırlıklı hesaplama |
| Paralel çalışma | Garanti etmez | Uygun platformda mümkündür |
| İletişim | Future ve Stream | Mesaj portları |

![dart-isolateleri-tek-94](/img/dart-isolateleri-tek-94.svg)


`async` bir işlemi otomatik olarak başka işlemci çekirdeğine taşımaz. Yalnızca bekleme sırasında olay döngüsünün başka görevlerle ilgilenmesine izin verir. Dev bir döngü hâlâ ana isolate’ı meşgul eder.

## En pratik yöntem: Isolate.run

Modern Dart sürümlerinde tek seferlik ağır işler için `Isolate.run` oldukça kullanışlıdır. Aşağıdaki fonksiyon büyük bir sayı aralığındaki asal sayıları sayar:

```dart
import 'dart:isolate';

Future<int> countPrimesWithoutBlocking(int limit) {
  return Isolate.run(() {
    var count = 0;

    for (var number = 2; number <= limit; number++) {
      var isPrime = true;
      for (var divisor = 2;
          divisor * divisor <= number;
          divisor++) {
        if (number % divisor == 0) {
          isPrime = false;
          break;
        }
      }
      if (isPrime) count++;
    }

    return count;
  });
}
```

Bu kod hesaplamayı ayrı bir isolate’ta gerçekleştirir ve sonucu `Future<int>` olarak döndürür. Flutter tarafında fonksiyon `await` edilirken animasyonlar ve dokunma olayları ana isolate üzerinde işlenmeye devam eder.

## Uzun ömürlü isolate ve mesajlaşma

Tekrarlanan işler için her defasında isolate başlatmak pahalı olabilir. Bu durumda `ReceivePort`, `SendPort` ve `Isolate.spawn` ile yaşayan bir çalışan oluşturulur:

```dart
import 'dart:isolate';

void worker(SendPort mainPort) {
  final inbox = ReceivePort();
  mainPort.send(inbox.sendPort);

  inbox.listen((message) {
    final data = message as List<dynamic>;
    final value = data[0] as int;
    final replyPort = data[1] as SendPort;
    replyPort.send(value * value);
  });
}

Future<void> startWorker() async {
  final workerReady = ReceivePort();
  await Isolate.spawn(worker, workerReady.sendPort);

  final workerPort = await workerReady.first as SendPort;
  final response = ReceivePort();
  workerPort.send([12, response.sendPort]);

  final result = await response.first;
  print('Sonuç: $result');
  response.close();
  workerReady.close();
}
```

Burada önce ana isolate çalışana bir cevap adresi verir. Çalışan kendi `SendPort` nesnesini gönderir; sonraki görevler bu kanal üzerinden iletilir. Adeta iki ofis arasında evrak taşıyan kurye sistemi gibi çalışır.

## Ne zaman kullanılmalı?

Büyük JSON ayrıştırma, görüntü işleme, şifreleme, sıkıştırma ve yoğun matematiksel hesaplamalar iyi adaylardır. HTTP isteği gibi bekleme ağırlıklı işlemlerde ise çoğunlukla `async` yeterlidir. Ayrıca Flutter web ortamında isolate davranışının platform sınırlamalarına tabi olabileceğini unutmayın.

Özetle: Arayüz isolate’ını resepsiyon görevlisi gibi düşünün. Ona tonlarca hesap yaptırırsanız müşteriler kapıda bekler. Ağır işi arka taraftaki isolate’a gönderin; resepsiyon gülümsemeye, uygulama da akıcı kalmaya devam etsin.

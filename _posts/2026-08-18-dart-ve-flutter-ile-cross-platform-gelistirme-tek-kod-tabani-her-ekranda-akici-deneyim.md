---
layout: post
title: "Dart ve Flutter ile Cross-Platform Geliştirme: Tek Kod Tabanı, Her Ekranda Akıcı Deneyim"
math: true
categories: 
  - Program
tags: 
  - Dart
  - Flutter
  - Cross-Platform
  - Animasyon
  - Mobil Geliştirme
---

Bir uygulamayı Android, iOS, web ve masaüstünde çalıştırmak eskiden ayrı ekipler, ayrı kod tabanları ve bolca senkronizasyon toplantısı anlamına gelirdi. Flutter bu tabloyu değiştirmeyi hedefler: Dart ile yazılan tek bir arayüz kodu, farklı platformlarda yerel hissi veren deneyimlere dönüşür. Üstelik mesele yalnızca “bir kere yaz, her yerde çalıştır” değildir; Flutter’ın güçlü çizim altyapısı sayesinde geçişler, mikro etkileşimler ve karmaşık animasyonlar da tutarlı biçimde üretilebilir.

``

Cross-platform yaklaşımının merkezinde ortak iş mantığı ve ortak görünüm katmanı bulunur. Ancak her platformun pencere sistemi, giriş yöntemleri ve dağıtım biçimi farklıdır. Flutter, uygulama arayüzünü platformun hazır bileşenlerini tek tek sarmalamak yerine büyük ölçüde kendi render motoruyla çizer. Bu yaklaşım, piksel düzeyinde daha öngörülebilir bir görünüm sağlar. Gerektiğinde platform kanalları veya eklentiler aracılığıyla kamera, bildirim, dosya sistemi ve sensör gibi yerel özelliklere de erişilir.

| Yaklaşım | Arayüz üretimi | Güçlü yanı | Dikkat edilmesi gereken |
|---|---|---|---|
| Ayrı yerel uygulamalar | Her platform için ayrı kod | Platforma tam özgü davranış | Yüksek bakım maliyeti |
| Web tabanlı hibrit | Web görünümü içinde çalışır | Hızlı prototipleme | Yoğun animasyonda performans |
| Flutter | Widget ağacı ve render motoru | Tutarlı tasarım, akıcı çizim | Platform ayrıntılarını ayrıca test etmek |

Flutter’daki her görsel parça bir **widget**’tır. Metin, boşluk, düğme, sayfa iskeleti ve hatta uygulamanın tamamı widget olarak düşünülür. Widget’lar değişmez tanımlardır; durum değiştiğinde Flutter yeni bir widget ağacı üretir ve yalnızca gereken çizim farklarını uygular. Bu düşünce biçimi, arayüzü “ekrana doğrudan müdahale etmek” yerine “mevcut durum için ekranın nasıl görünmesi gerektiğini tarif etmek” olarak ele alır.

Akıcılığın temel ölçütü kare süresidir. Ekranın yenileme hızı $f$ ise, bir karenin yaklaşık zaman bütçesi şöyledir:

$$t_{frame} = \frac{1000}{f}\text{ ms}$$

Örneğin $60\,Hz$ bir ekranda hedef yaklaşık $16.67\,ms$’dir. Build, layout, paint veya GPU işlemlerinden biri bu bütçeyi aşarsa kullanıcı takılma hisseder. Bu yüzden animasyonlarda gereksiz yeniden oluşturmalardan kaçınmak, büyük listelerde `ListView.builder` kullanmak ve pahalı çizimleri sınırlandırmak önemlidir.

Aşağıdaki örnek, kullanıcı düğmeye bastığında kutunun boyutunu ve rengini yumuşak biçimde değiştirir. `AnimatedContainer`, ara kareleri otomatik hesapladığı için başlangıç seviyesi animasyonlar için oldukça pratiktir:

```dart
import 'package:flutter/material.dart';

class PulseCard extends StatefulWidget {
  const PulseCard({super.key});

  @override
  State<PulseCard> createState() => _PulseCardState();
}

class _PulseCardState extends State<PulseCard> {
  bool expanded = false;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: GestureDetector(
        onTap: () => setState(() => expanded = !expanded),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 350),
          curve: Curves.easeOutBack,
          width: expanded ? 220 : 140,
          height: expanded ? 220 : 140,
          alignment: Alignment.center,
          decoration: BoxDecoration(
            color: expanded ? Colors.teal : Colors.indigo,
            borderRadius: BorderRadius.circular(expanded ? 32 : 16),
          ),
          child: const Text('Dokun!', style: TextStyle(color: Colors.white)),
        ),
      ),
    );
  }
}
```

Bu kodda `setState`, durumun değiştiğini bildirir; Flutter da ilgili bölümü yeniden değerlendirir. `duration` animasyon süresini, `curve` ise hareketin karakterini belirler. `easeOutBack` eğrisi hedefe yaklaşırken hafifçe taşarak daha canlı bir his üretir. Karmaşık senaryolarda `AnimationController`, zaman çizelgesi üzerinde daha ayrıntılı kontrol sunar.

| Hedef platform | Tasarımda öncelik | Test ipucu |
|---|---|---|
| Mobil | Dokunma alanları, güvenli alanlar | Küçük ekran ve düşük güçlü cihaz |
| Web | Fare, klavye, URL yönlendirmesi | Farklı tarayıcı ve pencere boyutu |
| Masaüstü | Kısayollar, yeniden boyutlandırma | Geniş ekran ve çoklu pencere davranışı |

Tek kod tabanı, her yerde aynı tasarım demek değildir. `LayoutBuilder`, `MediaQuery` ve uyarlanabilir widget’larla ekran genişliğine göre düzen değiştirmek gerekir. Sonuçta iyi bir Flutter uygulaması, kodu paylaşırken deneyimi körü körüne kopyalamaz; her platformun alışkanlıklarına saygı gösterir. Bu denge kurulduğunda Dart ve Flutter, fikirden çok ekranlı ürüne uzanan yolu ciddi biçimde hızlandırır.

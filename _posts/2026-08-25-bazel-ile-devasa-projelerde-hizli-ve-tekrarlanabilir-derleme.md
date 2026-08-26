---
layout: post
title: "Bazel ile Devasa Projelerde Hızlı ve Tekrarlanabilir Derleme"
math: true
categories: 
  - Bilgi
tags: 
  - bazel
  - derleme sistemleri
  - yazılım mimarisi
toc: true
---

Büyük bir yazılım projesinde derleme süresi, kahve molasından uzun sürmeye başladıysa Bazel ile tanışma vakti gelmiş olabilir. Google tarafından geliştirilen Bazel; C++, Java, Python, Go ve daha birçok dili aynı depoda yönetebilen, bağımlılıkları açıkça tanımlayan ve sonuçları önbelleğe alan modern bir derleme sistemidir. Temel hedefi basittir: Makineniz, işletim sisteminiz veya ekip arkadaşınız değişse bile aynı kaynak kodundan aynı çıktıyı hızlı biçimde üretmek.
``
## Bazel neden farklı çalışır?

Klasik derleme araçları çoğunlukla komutların hangi sırayla çalıştırılacağını tarif eder. Bazel ise **ne üretmek istediğinizi** ve bunun hangi girdilere bağlı olduğunu bildirmenizi ister. Bu yaklaşım deklaratif derleme olarak adlandırılır. Her hedef; kaynak dosyaları, araç zinciri, derleme bayrakları ve bağımlılıklardan oluşan bir işlem düğümüdür.

Bazel bu düğümleri bir yönlü çevrimsiz grafikte, yani DAG yapısında ele alır. Bir hedefin çıktısı yalnızca kendi gerçek girdilerine bağlıysa, değişmeyen düğümlerin tekrar derlenmesine gerek kalmaz. Kabaca toplam süre şöyle ifade edilebilir:

$$T_{build} \approx \max(T_{kritik\ yol}) + T_{kaçınılmaz\ I/O}$$

Buradaki kritik yol, paralel çalıştırılamayan bağımlılık zinciridir. Bazel bağımsız düğümleri eşzamanlı çalıştırarak işlemci çekirdeklerini daha verimli kullanır.

| Özellik | Geleneksel yaklaşım | Bazel yaklaşımı |
|---|---|---|
| Bağımlılık tanımı | Dolaylı veya dağınık | Açık ve hedef tabanlı |
| Artımlı derleme | Dosya zaman damgalarına dayanabilir | Girdi içeriği ve bağımlılık grafiğine dayanır |
| Önbellek | Genellikle yerel | Yerel, uzak ve paylaşılabilir |
| İzolasyon | Ortamdan etkilenebilir | Sandbox ile daha kontrollü |
| Çoklu dil desteği | Ayrı araçlar gerekebilir | Tek çatı altında yönetilebilir |

## BUILD dosyaları: Projenin haritası

Bazel yapılandırmasının merkezinde `BUILD` veya `BUILD.bazel` dosyaları bulunur. Bu dosyalarda hedefler ve aralarındaki ilişkiler tanımlanır. Örneğin küçük bir C++ uygulaması için aşağıdaki yapı yeterlidir:

```python
cc_library(
    name = "hesaplama",
    srcs = ["hesaplama.cc"],
    hdrs = ["hesaplama.h"],
    visibility = ["//visibility:public"],
)

cc_binary(
    name = "uygulama",
    srcs = ["main.cc"],
    deps = [":hesaplama"],
)
```

Bu örnekte `cc_library`, tekrar kullanılabilir bir kütüphane üretir. `cc_binary` ise çalıştırılabilir programı oluşturur ve `deps` alanıyla hangi kütüphaneye ihtiyaç duyduğunu net biçimde söyler. Derleme komutu da oldukça okunaklıdır:

```bash
bazel build //uygulama:uygulama
bazel test //...
bazel run //uygulama:uygulama
```

`//uygulama:uygulama` ifadesi, depo kökünden itibaren `uygulama` paketindeki `uygulama` hedefini belirtir. `bazel test //...` ise depodaki erişilebilir tüm test hedeflerini bulup çalıştırır.

## Tekrarlanabilirliğin sırrı: Hermetik derleme

Bir derlemenin hermetik olması, sonucunun tanımlı girdiler dışındaki unsurlardan etkilenmemesi demektir. Sisteminizde rastgele kurulu bir kütüphane, farklı bir saat dilimi veya ortam değişkeni çıktıyı değiştirmemelidir. İdeal durumda:

$$Çıktı = f(Kaynak, Bağımlılıklar, Araçlar, Bayraklar)$$

Bazel bu hedefe sandbox, kesin bağımlılık bildirimi ve araç zinciri yönetimiyle yaklaşır. Bunun pratik faydası çok büyüktür: CI sunucusunda çalışan derleme ile geliştiricinin dizüstü bilgisayarındaki derleme arasında sürpriz sayısı azalır.

## Önbellek ve uzaktan yürütme

Bazel her eylem için girdilerden bir anahtar üretir. Aynı anahtar daha önce üretildiyse sonuç önbellekten alınabilir. Basitleştirilmiş olarak:

$$K = H(girdiler + komut + araç\ zinciri)$$

Yerel önbellek bireysel geliştiriciyi hızlandırırken, uzak önbellek ekip genelinde büyük kazanç sağlar. Bir kişinin ürettiği derleme çıktısı, başka bir geliştiricinin makinesinde tekrar hesaplanmadan kullanılabilir. Daha ileri seviyede uzak yürütme ile derleme görevleri güçlü sunuculara dağıtılabilir.

Bazel'e geçişte en önemli kural küçük başlamaktır. Önce bağımsız bir modülü `BUILD` dosyasına taşıyın, test hedeflerini ekleyin ve bağımlılıkları görünür hâle getirin. İlk günlerde katı kurallar biraz huysuz görünebilir; fakat proje büyüdükçe bu disiplin, dakikalar süren derlemeleri saniyelere indiren sessiz bir süper güce dönüşür.

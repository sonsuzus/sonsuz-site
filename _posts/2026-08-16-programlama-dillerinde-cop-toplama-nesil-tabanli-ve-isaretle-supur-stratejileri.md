---
layout: post
title: "Programlama Dillerinde Çöp Toplama: Nesil Tabanlı ve İşaretle-Süpür Stratejileri"
math: true
categories: 
  - Bilgi
tags: 
  - çöp toplama
  - bellek yönetimi
  - garbage collector
---

Modern programlama dillerinde belleği elle yönetmek, güçlü ama hata üretmeye açık bir sorumluluktur. Java, C#, Go, JavaScript ve birçok sanal makine tabanlı dil bu yükü çöp toplayıcıya (Garbage Collector, GC) devreder. GC'nin temel görevi basittir: Programın artık ulaşamadığı nesneleri bulmak ve alanlarını yeniden kullanılabilir hâle getirmek. Fakat bu basit cümle; gecikme, bellek tüketimi, CPU maliyeti ve uygulama akıcılığı arasında dikkatli tercihler gerektirir.
``

Bir nesnenin canlı olup olmadığı genellikle **erişilebilirlik** ile belirlenir. Yığın (stack) üzerindeki yerel değişkenler, statik alanlar ve çalışma zamanının tuttuğu referanslar *kök küme*yi oluşturur. Köklerden başlayarak erişilebilen her nesne canlıdır. Erişilemeyen nesne ise çöptür. Bu yaklaşımın teorik modeli, nesneleri düğüm ve referansları kenar kabul eden yönlü bir grafiktir.

$$Canlı\ Nesneler = Reachable(Kök\ Küme)$$

İşaretle-süpür (mark-and-sweep), bu grafiği doğrudan kullanan klasik yöntemdir. İlk aşamada toplayıcı köklerden yürür, karşılaştığı nesneleri işaretler. Ardından heap taranır; işaretsiz nesneler serbest bırakılır, işaretli olanların bayrakları bir sonraki tur için temizlenir. Döngüsel referanslar burada sorun değildir: Birbirini gösteren iki nesne, köklerden ulaşılamıyorsa birlikte toplanır.

```text
mark(root):
  her referans için:
    nesne işaretli değilse
      nesneyi işaretle
      mark(nesne)

sweep(heap):
  her nesne için:
    işaretsizse alanını serbest bırak
    işaretliyse işaretini temizle
```

Bu algoritma anlaşılırdır; ancak süpürme sonrası boş alanlar heap içinde dağınık kalabilir. Buna **parçalanma** denir. Büyük ve bitişik bir nesne için yeterli toplam boş alan olsa bile uygun tek parça bulunamayabilir. Bu nedenle bazı çalışma zamanları işaretle-süpür sonrasına sıkıştırma (compaction) ekler. Nesneler taşınır, referanslar güncellenir ve bellek daha düzenli hâle gelir; bedeli ise ek işlem ve olası duraklamadır.

Nesil tabanlı toplama ise gözleme dayalı daha pragmatik bir fikri kullanır: Nesnelerin çoğu genç ölür. Buna **zayıf nesil hipotezi** denir. Yeni nesneler genç nesil (young generation) alanına yerleştirilir. Sık ama küçük toplama turlarıyla kısa ömürlü geçici nesneler temizlenir. Hayatta kalmayı başaranlar yaşlanır ve yaşlı nesle (old generation) terfi eder. Böylece her küçük toplamada devasa heap'in tamamı gezilmez.

| Özellik | İşaretle-Süpür | Nesil Tabanlı GC |
|---|---|---|
| Ana fikir | Tüm erişilebilir grafiği işaretler | Nesneleri yaşlarına göre ayırır |
| Toplama kapsamı | Genellikle tüm heap | Çoğunlukla genç nesil |
| Kısa ömürlü nesneler | Tüm heap taramasına yol açabilir | Çok verimli temizlenir |
| Parçalanma | Sıkıştırma yoksa oluşabilir | Genç alanda kopyalama ile azalır |
| Karmaşıklık | Görece sade | Terfi ve referans takibi nedeniyle daha karmaşık |

Genç nesil çoğu zaman kopyalama (copying) yaklaşımıyla çalışır. Canlı nesneler bir alandan diğerine kopyalanır; geride kalan her şey tek hamlede çöptür. Maliyet yaklaşık olarak toplam nesne sayısına değil, canlı nesne sayısına bağlıdır:

$$Maliyet_{minor} \approx O(Canlı_{genç})$$

Ancak yaşlı bir nesnenin genç bir nesneyi göstermesi özel takip gerektirir. GC, bu bağlantıları kaçırmamak için yazma bariyeri (write barrier) ve hatırlanan küme (remembered set) kullanır. Referans ataması sırasında küçük bir kayıt tutulur; minor GC yalnızca gerekli yaşlı nesneleri inceleyebilir.

Pratik seçim uygulamanın karakterine bağlıdır. Komut satırı aracı için nadir ama uzun bir toplama kabul edilebilirken, oyun, finans ekranı veya ses işleme uygulaması milisaniyelik duraklamalara bile hassastır. Bu yüzden modern çalışma zamanları nesil tabanlı yapıyı eşzamanlı, artımlı veya düşük gecikmeli işaretleme teknikleriyle birleştirir. Özetle işaretle-süpür güvenilir temel mekanizmadır; nesil tabanlı GC ise programların nesne ömrü alışkanlıklarından yararlanarak bu temeli hızlandıran akıllı bir optimizasyondur.

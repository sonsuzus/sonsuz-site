---
layout: post
title: "COBOL ile Eski Bankacılık Sistemlerini Anlama: Anaframe Miras Kodlarını Okuma Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - cobol
  - anaframe
  - bankacılık
  - miras kod
  - jcl
---

Bir bankanın ekranında saniyeler içinde görünen bakiye, çoğu zaman bulut üzerindeki parlak bir mikroservisten değil, onlarca yıldır çalışan bir ana bilgisayar programından gelir. COBOL (Common Business-Oriented Language), insan diline yakın söz dizimi ve güçlü kayıt işleme modeli sayesinde bankacılıkta kalıcı olmuştur. Bu sistemleri anlamak, yalnızca eski bir dili öğrenmek değildir; faiz, tahakkuk, mutabakat, hesap hareketi ve denetim izlerinin iş kurallarına nasıl dönüştüğünü keşfetmektir.

``

COBOL programlarını okumaya başlamanın en doğru yolu, kodu modern nesne yönelimli dillerle bire bir karşılaştırmamaktır. COBOL çoğunlukla toplu işleme (batch) ve çevrim içi işlem (online transaction) dünyası için tasarlanmıştır. Bir program genellikle dosyadan veya DB2 tablosundan kayıt okur, iş kuralını uygular, sonucu başka bir veri kümesine yazar. Temel düşünce basittir: her hesap kaydı için belirli dönüşümler uygulanır.

Matematiksel olarak bir gece sonu işlemini şöyle düşünebiliriz:

$$B_{yeni} = B_{eski} + T_{borç} - T_{alacak} + F - V$$

Burada $B$ bakiye, $T$ hareket tutarları, $F$ faiz veya ücret, $V$ ise vergi gibi kesintileri temsil eder. Gerçek sistemde bu formül; para birimi, valör tarihi, limit, bloke ve yuvarlama kurallarıyla büyür. Miras kodun değeri, işte bu istisnaların yıllar boyunca test edilmiş biçimde saklanmasıdır.

| Kavram | COBOL dünyası | Modern uygulama dünyası |
|---|---|---|
| Veri birimi | Sabit genişlikli kayıt | JSON nesnesi / ORM modeli |
| İş akışı | Batch job, CICS işlemi | Worker, API, kuyruk tüketicisi |
| Veri erişimi | VSAM, sequential file, DB2 | SQL, NoSQL, REST API |
| Hata yaklaşımı | Durum kodu ve `FILE STATUS` | Exception ve loglama |
| Güçlü yanı | Öngörülebilirlik, yüksek hacim | Esneklik, hızlı geliştirme |

Bir COBOL kaynak dosyasında ilk durak `IDENTIFICATION DIVISION`, ardından `ENVIRONMENT DIVISION`, `DATA DIVISION` ve `PROCEDURE DIVISION` olmalıdır. İlk üç bölüm programın kimliğini, çalışma ortamını ve veri şemasını anlatır. Asıl iş mantığı `PROCEDURE DIVISION` içinde yaşar. Özellikle `PERFORM`, `IF`, `EVALUATE`, `READ`, `WRITE` ve `COMPUTE` ifadeleri bir programın hikâyesini takip etmek için kritik işaretlerdir.

Aşağıdaki örnek, hesap hareketine göre bakiyeyi günceller. `PIC` tanımları veri alanının uzunluğunu ve biçimini gösterir; bu nedenle veri yapısını anlamada son derece önemlidir.

```cobol
       01  HESAP-KAYDI.
           05 HESAP-NO          PIC 9(10).
           05 BAKIYE            PIC S9(11)V99 COMP-3.
           05 HAREKET-TIPI      PIC X.
           05 HAREKET-TUTARI    PIC 9(09)V99 COMP-3.

       PROCEDURE DIVISION.
           EVALUATE HAREKET-TIPI
               WHEN 'A'
                   ADD HAREKET-TUTARI TO BAKIYE
               WHEN 'B'
                   SUBTRACT HAREKET-TUTARI FROM BAKIYE
               WHEN OTHER
                   DISPLAY 'GECERSIZ HAREKET TIPI'
           END-EVALUATE.
```

Bu örnekte `A` alacak, `B` borç hareketidir. `COMP-3`, ondalıklı parasal değerleri paketli ondalık biçimde saklar; ikili kayan nokta hatalarından kaçınmak için bankacılıkta yaygındır. Örneğin $0.1 + 0.2$ bazı kayan nokta sistemlerinde tam olarak $0.3$ olmayabilirken, sabit ondalık temsil para hesaplarında daha güvenlidir.

| Okuma ipucu | Neden önemlidir? | Aranacak işaret |
|---|---|---|
| Kayıt şemasını çıkarın | Alanların iş anlamını belirler | `01`, `05`, `PIC`, `COPY` |
| Girdi/çıktıyı bulun | Programın sınırlarını gösterir | `SELECT`, `FD`, `READ`, `WRITE` |
| Karar noktalarını listeleyin | Kural ve istisnaları açığa çıkarır | `IF`, `EVALUATE` |
| Tarih alanlarını izleyin | Faiz ve valör mantığını etkiler | `ISLEM-TARIHI`, `VALOR-TARIHI` |

Anaframe dünyasında bir program nadiren tek başına çalışır. JCL (Job Control Language), hangi programın hangi veri setiyle, hangi sırada çalışacağını belirler. `COPY` ifadeleri ise ortak kayıt tanımlarını çağırır. Bu nedenle bir hesap güncelleme programını çözerken kaynak kod, copybook, JCL ve veri sözlüğünü birlikte incelemek gerekir.

Sonuç olarak COBOL okumak bir arkeoloji çalışması değil, çalışan bir finansal makineyi haritalamaktır. Önce veri akışını, sonra kayıt alanlarını, ardından karar kurallarını takip edin. Kodun yaşı göz korkutmasın: Bankacılık mantığı çoğu zaman satır aralarında değil, dikkatle adlandırılmış alanlar ve yıllardır ayakta kalan süreçlerde saklıdır.

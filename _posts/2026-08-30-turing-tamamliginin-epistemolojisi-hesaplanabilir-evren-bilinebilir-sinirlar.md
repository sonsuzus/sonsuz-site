---
layout: post
title: "Turing Tamamlığının Epistemolojisi: Hesaplanabilir Evren, Bilinebilir Sınırlar"
math: true
categories: 
  - Bilgi
tags: 
  - turing tamamlığı
  - hesaplanabilirlik
  - felsefe
  - bilgisayar bilimi
---

Turing tamamlığı çoğu zaman bir programlama dili rozetine indirgenir: Döngüsü ve koşulu varsa, yeterli bellekle her şeyi hesaplar denir. Fakat bu ifade yalnızca teknik bir özellik değildir; bilginin ne olduğu, hangi soruların ilkesel olarak yanıtlanabileceği ve evrenin bir algoritma gibi düşünülebilip düşünülemeyeceği üzerine güçlü bir felsefi provokasyondur. Kritik ayrım şudur: Bir şeyi *ifade edebilmek*, onu pratikte hızlıca çözebilmek ve onun hakkında kesin bilgiye ulaşabilmek aynı şey değildir.

``

Bir sistem, Turing makinesinin simüle edebileceği genel amaçlı hesaplamaları gerçekleştirebiliyorsa Turing tamdır. Turing makinesi; sonlu bir denetleyici, semboller yazabilen sınırsız bir şerit ve şerit üzerinde hareket eden bir kafadan oluşan soyut bir modeldir. Modern bilgisayarlar, Python, C ve hatta yeterince yaratıcı biçimde kullanılan bazı oyun sistemleri bu modele denk hesaplama gücü sunabilir. Bu durum, donanımın biçiminden çok algoritmik kuralların önem taşıdığını söyler.

Hesaplanabilirlik fikrini biçimsel olarak şöyle düşünebiliriz. Bir fonksiyon için

$$f: \mathbb{N} \rightarrow \mathbb{N}$$

bir Turing makinesi her girdi $n$ için duruyor ve $f(n)$ sonucunu üretiyorsa, $f$ hesaplanabilirdir. Ancak burada “her fonksiyon” yoktur. Doğal sayıların fonksiyonlarının sayısı sayılamazken, yazılabilir programların sayısı sayılabilirdir. Dolayısıyla tarif edilebilir görünen bazı matematiksel ilişkiler için hiçbir algoritma bulunamaz.

| Kavram | Sorduğu soru | Sınırın türü |
|---|---|---|
| Turing tamamlığı | Hangi işlemler ilkece simüle edilebilir? | Modelin ifade gücü |
| Hesaplama karmaşıklığı | Çözüm ne kadar zaman/bellek ister? | Pratik kaynak sınırı |
| Karar verilemezlik | Her girdi için kesin algoritma var mı? | Mantıksal, mutlak sınır |
| Kaos | Başlangıç koşullarına hassasiyet var mı? | Ölçüm ve öngörü sınırı |

Bu tablodaki en sarsıcı satır karar verilemezliktir. Durma problemi, rastgele bir programın belirli bir girdide sonsuza dek çalışıp çalışmayacağını bütün programlar için doğru biçimde saptayan genel bir programın var olamayacağını kanıtlar. Yani daha güçlü bir bilgisayar, yeterince RAM veya daha şık bir yapay zekâ bu engeli ortadan kaldırmaz. Engel mühendislikte değil, ispatın kendisindedir.

Aşağıdaki Python parçası, durma problemini çözmez; tersine, neden genel bir çözümün çelişki üreteceğini anlatan klasik fikrin küçük bir tiyatro uyarlamasıdır:

```python
def durur_mu(program, girdi):
    # Varsayımsal: Her program için kusursuz karar verdiğini kabul ediyoruz.
    return True

def celiski(program):
    if durur_mu(program, program):
        while True:
            pass  # "Durur" denirse bilerek durmuyoruz.
    return "Bitti"
```

`celiski` fonksiyonuna kendisini verdiğimizi düşünelim. Eğer `durur_mu` “durur” derse fonksiyon sonsuz döngüye girer; “durmaz” derse normal biçimde biter. Sorun Python sözdiziminde değil, programın kendi davranışı hakkında evrensel yargı kurma iddiasındadır. Bu öz-gönderim, Gödel’in eksiklik teoremleriyle akraba bir fikir taşır: Yeterince zengin biçimsel sistemler, kendi içlerinden tamamen kapatılamayan doğrular üretir.

Buradan “evren hesaplanamazdır” sonucu doğmaz. Bir evren Turing-tam kurallarla işliyor olabilir; hatta bazı fizikçiler dijital fizik görüşüyle bunu araştırır. Fakat Turing tam bir evren, içindeki gözlemcilerin her geleceği kısa yoldan hesaplayabileceği anlamına gelmez. Simülasyonun en hızlı yolu bazen simülasyonu gerçekten çalıştırmaktır. Kuantum süreçleri ise verimlilik ve fiziksel model tartışmasını büyütür; yine de bilinen kuantum bilgisayarlar genel anlamda karar verilemezliği sihirli biçimde çözmez.

Epistemolojik ders zarif ama alçakgönüllü olmaya zorlayıcıdır: Bilgi, yalnızca veri toplamak değildir; hangi soruların algoritmik olarak çözülebileceğini bilmek de bilgidir. Turing tamamlığı bize aklın evrensel bir hesaplama dili kurabileceğini söyler. Durma problemi ise bu dilin, kendi sınırlarının tamamını tek bir sonlu prosedürle haritalayamayacağını hatırlatır.

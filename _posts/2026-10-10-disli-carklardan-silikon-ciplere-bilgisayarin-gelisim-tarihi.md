---
layout: post
title: "Dişli Çarklardan Silikon Çiplere: Bilgisayarın Gelişim Tarihi"
math: true
categories: 
  - Bilgi
tags: 
  - bilgisayar tarihi
  - işlemci
  - teknoloji
  - programlama
  - donanım
  - yapay zeka
toc: true
image: /img/disli-carklardan-silikon-55.png
---

Bugün cebimizde taşıdığımız telefonlar, birkaç on yıl önce odaları dolduran bilgisayarlardan milyonlarca kat daha güçlü. Ancak bu teknolojik yolculuk bir anda başlamadı. Dişli çarklarla çalışan hesap makinelerinden vakum tüplerine, transistörlerden milyarlarca bileşen içeren işlemcilere uzanan bilgisayar tarihi; matematik, mühendislik ve insan merakının ortak ürünüdür.

``

## Mekanik hesaplamanın doğuşu

Bilgisayarların uzak atalarından biri, 1642 yılında Blaise Pascal tarafından geliştirilen **Pascaline** adlı mekanik hesap makinesiydi. Dişli çarklar kullanan bu cihaz toplama ve çıkarma yapabiliyordu. Gottfried Wilhelm Leibniz ise 1670'lerde sistemi geliştirerek çarpma ve bölme işlemlerini de mekanikleştirdi.

Bu makinelerin temel fikri, sayıları fiziksel konumlarla temsil etmekti. Örneğin bir çarkın on farklı konumu, 0 ile 9 arasındaki rakamlara karşılık geliyordu. Günümüzde aynı yaklaşım elektrik sinyalleriyle uygulanır; ancak on durum yerine çoğunlukla iki durum kullanılır:

$$bit \in \{0,1\}$$

Mekanik sistemlerde hareket eden parçalar bilgiyi taşırken modern bilgisayarlarda bu görevi gerilim seviyeleri üstlenir.

## Programlanabilir makine fikri

1800'lerin başında Joseph Marie Jacquard, dokuma tezgâhlarını **delikli kartlarla** kontrol etti. Kartlardaki delikler bir tür komut dizisi oluşturuyordu. Charles Babbage bu fikirden etkilenerek 1837'de **Analitik Makine** tasarımını ortaya koydu.

Babbage'ın makinesi tamamlanamamış olsa da işlem birimi, bellek, giriş ve çıkış gibi modern bilgisayar bileşenlerini teorik olarak içeriyordu. Ada Lovelace ise makinenin Bernoulli sayılarını hesaplaması için bir algoritma hazırladı ve tarihin ilk bilgisayar programcısı kabul edildi.

## Elektronik bilgisayarlar sahneye çıkıyor

1940'larda mekanik parçaların yerini röleler ve vakum tüpleri aldı. 1946'da tanıtılan **ENIAC**, yaklaşık 18.000 vakum tüpü kullanıyor ve saniyede binlerce işlem gerçekleştirebiliyordu. Ne var ki devasa boyutlu, enerji oburu ve arızaya yatkındı.

| Dönem | Temel teknoloji | Başlıca avantaj | Başlıca sorun |
|---|---|---|---|
| 1600–1800 | Dişli çarklar | Hesabı otomatikleştirme | Yavaşlık ve aşınma |
| 1940'lar | Vakum tüpleri | Elektronik hız | Isınma ve yüksek enerji |
| 1950–1960 | Transistörler | Küçük boyut, güvenilirlik | Üretim maliyeti |
| 1970 sonrası | Mikroişlemciler | Yüksek entegrasyon | Isı ve karmaşıklık |
| Günümüz | Çok çekirdekli çipler | Paralel işlem | Güç tüketimi sınırları |

## Transistör ve mikroişlemci devrimi

1947'de transistörün geliştirilmesi bilgisayarları küçülttü, hızlandırdı ve daha güvenilir hâle getirdi. Ardından çok sayıda transistörün aynı yüzeye yerleştirildiği **entegre devreler** ortaya çıktı. 1971'de Intel 4004, ticari açıdan başarılı ilk mikroişlemcilerden biri oldu.

İşlemci performansı kabaca saat frekansı, çekirdek sayısı ve saat başına tamamlanan komut miktarıyla ilişkilendirilebilir:

$$P \approx f \times C \times IPC$$

Burada $f$ frekansı, $C$ çekirdek sayısını, $IPC$ ise döngü başına işlenen komut sayısını temsil eder. Gerçek performans bellek, önbellek ve yazılım tasarımından da etkilenir.

İkili sistemin temel mantığını küçük bir Python örneğiyle görebiliriz:

```python
def ikili_topla(a, b):
    # Metin biçimindeki ikili sayıları onlu sisteme çevirir.
    toplam = int(a, 2) + int(b, 2)

    # Sonucu yeniden ikili gösterime dönüştürür.
    return bin(toplam)[2:]

print(ikili_topla("1010", "0111"))  # 10001
```

Bu kod, işlemcideki gerçek mantık kapılarının yaptığı işi soyut düzeyde taklit eder. Donanımda toplama; AND, OR ve XOR gibi devrelerle gerçekleştirilir.

## Günümüz: Paralellik ve uzmanlaşma

Transistör sayısının yaklaşık iki yılda bir artacağını öngören **Moore Yasası**, onlarca yıl boyunca sektöre yön verdi. Fiziksel küçülmenin zorlaşmasıyla üreticiler yalnızca frekansı artırmak yerine çok çekirdekli mimarilere yöneldi. GPU'lar grafik işlemlerinin yanında yapay zekâ ve bilimsel hesaplama için kullanılmaya başlandı. NPU gibi özel birimler ise belirli görevleri daha az enerjiyle tamamlıyor.

Kısacası bilgisayarın gelişimi, “daha hızlı hesaplama” arzusundan “doğru işi doğru donanımla yapma” anlayışına evrildi. Pascal'ın çarklarından modern işlemcilerin nanometre ölçeğindeki transistörlerine kadar değişmeyen temel amaç ise aynı kaldı: bilgiyi temsil etmek, kurallara göre işlemek ve anlamlı sonuç üretmek.

![disli-carklardan-silikon-55](/img/disli-carklardan-silikon-55.svg)


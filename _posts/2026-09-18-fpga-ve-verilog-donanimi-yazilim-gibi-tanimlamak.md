---
layout: post
title: "FPGA ve Verilog: Donanımı Yazılım Gibi Tanımlamak"
math: true
categories: 
  - Bilgi
tags: 
  - fpga
  - verilog
  - sayısal tasarım
  - donanım tanımlama dili
  - hdl
  - elektronik
toc: true
---

Bir işlemcinin komutları sırayla çalıştırmasına alışkınsanız, FPGA dünyası ilk bakışta biraz büyülü görünebilir. Verilog ile birkaç satır yazıyor, ardından kabloların, mantık kapılarının ve register’ların gerçekten oluşmasını sağlıyorsunuz. Ancak burada önemli bir ayrım var: Verilog, klasik anlamda donanıma ne yapacağını söyleyen bir yazılım dili değil; donanımın nasıl davranacağını ve bağlanacağını tanımlayan bir donanım tanımlama dilidir.

``

## FPGA tam olarak nedir?

FPGA, yani **Field-Programmable Gate Array**, üretildikten sonra kullanıcı tarafından yapılandırılabilen sayısal bir devredir. İçinde programlanabilir mantık blokları, bağlantı hatları, flip-flop’lar, bellek birimleri ve çoğu zaman DSP blokları bulunur. Sentez aracı, Verilog tanımınızı bu kaynaklara eşler.

Bir mikrodenetleyicide yazdığınız program işlemci üzerinde yürütülür. FPGA’de ise tarif ettiğiniz devre fiziksel mantık kaynaklarına dönüştürülür. Bu nedenle birbirinden bağımsız iki devre aynı anda çalışabilir. FPGA’nin asıl süper gücü paralelliktir.

| Özellik | Yazılım / İşlemci | Verilog / FPGA |
|---|---|---|
| Çalışma modeli | Komutlar çoğunlukla sıralıdır | Devreler paralel çalışır |
| Temel unsur | Değişken ve fonksiyon | Sinyal, register ve kapı |
| Zamanlama | İşletim akışına bağlıdır | Saat çevrimleriyle tasarlanır |
| Sonuç | Makine kodu | Donanım yapılandırması |
| Hata türü | Mantık veya çalışma zamanı hatası | Mantık, zamanlama ve bağlantı hatası |

## Saat, durum ve paralellik

Senkron tasarımlarda işlemler genellikle bir saat sinyalinin yükselen kenarında gerçekleşir. Saat frekansı $f$ ise bir çevrimin süresi şu şekilde hesaplanır:

$$T = \frac{1}{f}$$

Örneğin $f = 100\,\text{MHz}$ için çevrim süresi $T = 10\,\text{ns}$ olur. Tasarladığınız kombinasyonel yolun veriyi bu süreden daha kısa zamanda üretmesi gerekir. Aksi hâlde devre simülasyonda doğru görünse bile gerçek FPGA üzerinde zamanlama ihlali yaşayabilir.

Verilog’daki `always` blokları da sırayla çağrılan fonksiyonlar değildir. Farklı `always` blokları aynı donanımın paralel çalışan parçalarını temsil eder. Bu zihinsel model, başlangıçtaki pek çok sürprizi önler.

## Basit bir sayaç tasarlayalım

Aşağıdaki modül, saatin her yükselen kenarında değeri artırılan sekiz bitlik bir sayaç oluşturur. Reset etkin olduğunda sayaç sıfırlanır:

```verilog
module counter (
    input  wire       clk,
    input  wire       reset,
    output reg  [7:0] count
);

always @(posedge clk) begin
    if (reset)
        count <= 8'd0;
    else
        count <= count + 1'b1;
end

endmodule
```

Buradaki `posedge clk`, işlemin saat yükselirken gerçekleşeceğini belirtir. `count` sekiz flip-flop ile saklanan bir durum bilgisidir. `<=` ise ardışıl mantıkta tercih edilen **non-blocking assignment** operatörüdür. Sayaç taşınca hata vermez; sekiz bitlik değer $255$ sonrasında modüler aritmetik gereği sıfıra döner:

$$count_{yeni} = (count_{eski} + 1) \bmod 256$$

## Simülasyon neden şarttır?

Verilog kodunu karta göndermeden önce bir testbench ile sınamak gerekir. Testbench fiziksel donanıma dönüşmez; giriş sinyalleri üretir ve tasarımın tepkisini gözlemlememizi sağlar.

```verilog
initial begin
    reset = 1;
    #20 reset = 0;
    #200 $finish;
end

always #5 clk = ~clk;
```

Bu örnekte saat her 5 zaman biriminde terslenir. Reset kısa süre etkin tutulur, ardından sayaç çalışmaya bırakılır. Dalga biçimi görüntüleyicisinde `count` sinyalinin düzenli artması beklenir.

## Kod yazmak mı, devre çizmek mi?

Aslında ikisi de! Verilog metin tabanlı olduğu için yazılım hissi verir; fakat her satırın arkasında oluşacak donanımı düşünmek gerekir. Sınırsız döngüler, kontrolsüz gecikmeler veya yazılımda ucuz görünen bazı işlemler donanımda mümkün olmayabilir ya da çok fazla kaynak tüketebilir.

İyi bir FPGA geliştiricisi yalnızca sözdizimini bilmez; saat alanlarını, gecikmeleri, kaynak kullanımını ve paralel veri akışını da hesaba katar. Verilog’u öğrenmenin en etkili yolu LED yakma, sayaç, PWM ve UART gibi küçük projelerle başlayıp sentez raporlarını incelemektir. Böylece kodun kapılara dönüşmesini izler, donanımı gerçekten “yazmaya” başlarsınız.

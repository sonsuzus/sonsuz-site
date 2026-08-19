---
layout: post
title: "Verilog ile Sayısal Devre Simülasyonu: Kombinasyonelden İşlemci Bileşenlerine"
math: true
categories: 
  - Program
tags: 
  - Verilog
  - Sayısal Devreler
  - Simülasyon
  - FPGA
  - İşlemci Tasarımı
---

Bir işlemcinin içinde mucize değil, saat sinyaliyle uyum içinde çalışan çok sayıda küçük devre vardır. Verilog, bu devreleri fiziksel olarak üretmeden önce davranışlarını modellemeyi ve simüle etmeyi sağlayan bir donanım tanımlama dilidir (HDL). Böylece bir ALU’nun toplama yapıp yapmadığını, register’ın veriyi doğru anda saklayıp saklamadığını veya kontrol biriminin yanlış sinyal üretip üretmediğini dalga şekilleri üzerinden görebiliriz.

``

Verilog yazılım dillerine benzer görünse de temel farkı önemlidir: C veya Python komutları sıralı biçimde çalıştırırken, Verilog’daki donanım blokları **eşzamanlı** çalışmayı temsil eder. Bir `assign` ifadesi, kabloya bağlanmış sürekli bir mantık devresi gibidir. `always` blokları ise hassasiyet listesine ya da saat kenarına bağlı davranış tanımlar. Simülasyon aracı bu tanımlardan zaman içinde değişen sinyalleri üretir.

## Kombinasyonel mantık: Geçmişi olmayan devreler

Kombinasyonel devrelerin çıkışı yalnızca o andaki girişlere bağlıdır. Matematiksel olarak bu ilişki şu şekilde yazılabilir:

$$Y(t) = f(X_1(t), X_2(t), \dots, X_n(t))$$

Toplayıcılar, çoklayıcılar (MUX), kod çözücüler ve işlemcideki ALU’nun büyük bölümü bu sınıftadır. Örneğin iki 8 bitlik sayıyı toplayan basit bir ALU parçası şöyle modellenebilir:

```verilog
module alu_add (
    input  wire [7:0] a,
    input  wire [7:0] b,
    input  wire       sub,
    output wire [7:0] result,
    output wire       carry
);
    wire [8:0] sum;

    // sub=1 iken iki'nin tümleyeniyle çıkarma yapılır.
    assign sum    = {1'b0, a} + {1'b0, (sub ? ~b : b)} + sub;
    assign result = sum[7:0];
    assign carry  = sum[8];
endmodule
```

Burada `sub` sinyali 0 olduğunda toplama, 1 olduğunda ise $a-b$ işlemi gerçekleştirilir. `assign` kullanımı devrenin giriş değiştiğinde anında yeniden hesaplanan kombinasyonel bir yapı olduğunu açıkça anlatır.

## Ardışıl mantık: Devrenin hafızası

Ardışıl devreler, mevcut girişlerin yanında önceki durumlarını da kullanır. Bu nedenle register, sayaç, program sayacı (PC) ve durum makineleri saat sinyaline ihtiyaç duyar. Genel model şöyledir:

$$Q(t+1) = g(Q(t), X(t))$$

| Özellik | Kombinasyonel Mantık | Ardışıl Mantık |
|---|---|---|
| Çıkışı belirleyen | Anlık girişler | Girişler ve önceki durum |
| Saat sinyali | Genellikle gerekmez | Genellikle zorunludur |
| Örnek | MUX, kod çözücü, ALU | Register, PC, sayaç |
| Verilog yaklaşımı | `assign`, `always @(*)` | `always @(posedge clk)` |

Aşağıdaki register modülü, işlemcinin bir veri yolundaki değeri saat yükselen kenarında saklamasını simüle eder:

```verilog
module register8 (
    input  wire       clk,
    input  wire       rst,
    input  wire       enable,
    input  wire [7:0] d,
    output reg  [7:0] q
);
    always @(posedge clk) begin
        if (rst)
            q <= 8'b0;
        else if (enable)
            q <= d;
    end
endmodule
```

`<=` non-blocking ataması, flip-flop davranışını doğru modellemek için tercih edilir. `enable` kapalıyken `q` değişmez; yani register eski değerini korur. Bu küçük ayrıntı, ardışıl tasarımın “hafıza” karakterini oluşturur.

## Testbench: Devreyi konuşturmak

Bir modülün doğru olduğunu söylemek için onu farklı girişlerle denemek gerekir. Testbench, sentezlenmeyen; yalnızca simülasyonda çalışan doğrulama ortamıdır. Saat üretir, reset uygular ve sonuçları denetler.

```verilog
module tb_register8;
    reg clk = 0, rst = 1, enable = 0;
    reg [7:0] d = 8'h00;
    wire [7:0] q;

    register8 dut (.clk(clk), .rst(rst), .enable(enable), .d(d), .q(q));
    always #5 clk = ~clk;

    initial begin
        #12 rst = 0;
        enable = 1; d = 8'h3C;
        #10 enable = 0; d = 8'hFF;
        #10 $finish;
    end
endmodule
```

Dalga formunda `q` değerinin reset sırasında sıfırlandığını, ardından yalnızca saat kenarında `3C` olduğunu ve `enable` kapandığında `FF`’ye geçmediğini görmelisiniz. Bu yaklaşım ALU, register dosyası, program sayacı ve kontrol birimi gibi parçaları tek tek doğrulayıp sonunda küçük bir işlemci tasarımında birleştirmenin güvenli yoludur.

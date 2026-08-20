---
layout: post
title: "VHDL ile FPGA Tabanlı Donanım Tasarımı: Paralelliği Devreye Dönüştürmek"
math: true
categories: 
  - Bilgi
tags: 
  - vhdl
  - fpga
  - donanım tasarımı
---

VHDL, yazılım yazıyormuş gibi görünen ama aslında fiziksel dijital devreleri tarif eden güçlü bir donanım tanımlama dilidir. Bir FPGA üzerinde VHDL ile sayaçtan görüntü işleme hızlandırıcısına, haberleşme denetleyicisinden makine öğrenmesi çıkarım motoruna kadar özel devreler kurulabilir. Kritik fark şudur: CPU’da yazılan komutlar sırayla yürütülürken, FPGA’ya sentezlenen mantık blokları aynı anda çalışır. Bu yüzden doğru tasarlanmış bir FPGA devresi, belirli bir işi çok düşük gecikmeyle ve yüksek enerji verimliliğiyle gerçekleştirebilir.
``

## Yazılım Değil, Donanım Tarifi

VHDL kodu bir işlemcinin doğrudan yorumladığı komutlardan oluşmaz. Sentez aracı, kodunuzu flip-flop, lojik kapı, çoklayıcı, RAM ve yönlendirme hatları gibi fiziksel FPGA kaynaklarına dönüştürür. Örneğin bir `if` ifadesi çoğu zaman yazılımdaki gibi dallanma maliyeti oluşturmaz; bunun yerine bir çoklayıcıya dönüşür.

Senkron tasarımın kalbinde saat sinyali bulunur. Saatin her aktif kenarında kayıtçılar yeni veriyi yakalar. İki ardışık kayıtçı arasındaki birleşimsel mantığın gecikmesi, sistemin çalışabileceği en yüksek frekansı belirler:

$$T_{clock} \geq T_{cq} + T_{logic} + T_{setup} + T_{skew}$$

Burada $T_{cq}$ kayıtçının çıkış gecikmesi, $T_{logic}$ aradaki mantık gecikmesi, $T_{setup}$ kurulum süresi ve $T_{skew}$ saat dağıtım farkıdır. Bu denklem, neden uzun hesaplamaların boru hattına bölündüğünü açıklar.

| Kavram | Yazılım dünyasındaki karşılığı | FPGA/VHDL karşılığı |
|---|---|---|
| Fonksiyon | Çalışma anında çağrılan kod | Devresel mantık bloğu |
| Değişken | Bellekteki değiştirilebilir değer | Süreç içi geçici hesaplama |
| Sinyal | Yoksa da olur | Modüller arası fiziksel bağlantı |
| Döngü | Tekrarlı komut yürütme | Sentezde çoğunlukla çoğaltılmış mantık |
| Paralellik | Thread veya SIMD | Gerçek eşzamanlı donanım |

## Sinyal, Süreç ve Eşzamanlılık

VHDL’de mimari gövdesindeki ifadeler eşzamanlıdır. `process` blokları da birbirinden bağımsız devre parçaları gibi çalışır. Bir saatli süreç içinde sinyal ataması yapıldığında yeni değer hemen görünmez; süreç tamamlandığında planlanır. Bu davranış, donanımdaki flip-flop modelini doğru kurmak için önemlidir.

Aşağıdaki örnek, bir LED’i belirli bir sayaç değerine ulaşıldığında değiştiren senkron devredir. `unsigned` kullanımı, aritmetiğin bit vektörleri üzerinde açıkça tanımlanmasını sağlar.

```vhdl
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity led_blink is
  port (
    clk : in  std_logic;
    rst : in  std_logic;
    led : out std_logic
  );
end entity;

architecture rtl of led_blink is
  signal count : unsigned(23 downto 0) := (others => '0');
  signal led_r : std_logic := '0';
begin
  process(clk)
  begin
    if rising_edge(clk) then
      if rst = '1' then
        count <= (others => '0');
        led_r <= '0';
      elsif count = 0 then
        count <= to_unsigned(12_499_999, count'length);
        led_r <= not led_r;
      else
        count <= count - 1;
      end if;
    end if;
  end process;

  led <= led_r;
end architecture;
```

Bu devrede sayaç ve LED durumu flip-floplarda saklanır. 25 MHz saat için yaklaşık her yarım saniyede LED durumu değişir. Simülasyonda hızlı görünen kodun gerçek kartta neden farklı davrandığını anlamak için saat frekansını mutlaka hesaba katın.

## Paralellikten Yararlanmak

FPGA’nın süper gücü, aynı işlemi birçok veri üzerinde aynı çevrimde yapabilmesidir. Örneğin dört adet toplayıcıyı yan yana kurarak dört veri çiftini paralel toplayabilirsiniz. Teorik olarak verim:

$$\text{Throughput} = \frac{N \times W}{T_{clock}}$$

şeklinde düşünülebilir. Burada $N$ paralel işlemci sayısı, $W$ işlem başına veri miktarıdır. Ancak kaynak kullanımı arttıkça LUT, DSP ve bellek sınırları devreye girer.

| Yaklaşım | Gecikme | Kaynak tüketimi | Uygun kullanım |
|---|---:|---:|---|
| Tek işlem birimi | Yüksek | Düşük | Basit kontrol mantığı |
| Paralel birimler | Düşük | Yüksek | Görüntü, filtreleme, DSP |
| Boru hattı | İlk sonuç geç gelir | Orta | Sürekli veri akışı |

Başarılı bir VHDL projesi; RTL tasarımı, testbench ile simülasyon, sentez, zamanlama analizi ve kart üzerinde doğrulama adımlarını içerir. Önce davranışı simüle edin, sonra zamanlama raporundaki kritik yolları inceleyin. FPGA tasarımında en iyi hata ayıklama aracı, kart üzerindeki LED’den önce iyi yazılmış bir testbench’tir.

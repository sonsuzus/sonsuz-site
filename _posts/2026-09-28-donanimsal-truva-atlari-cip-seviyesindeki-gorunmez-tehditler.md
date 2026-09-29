---
layout: post
title: "Donanımsal Truva Atları: Çip Seviyesindeki Görünmez Tehditler"
math: true
categories: 
  - Bilgi
tags: 
  - donanım güvenliği
  - siber güvenlik
  - çip tasarımı
  - donanımsal truva atı
  - yarı iletkenler
  - sistem güvenliği
toc: true
image: /img/donanimsal-truva-atlari-94.png
---

Modern bir işlemciye baktığımızda milyarlarca transistörden oluşan kusursuz bir şehir görürüz. Peki bu şehrin kullanılmayan bir sokağına, yalnızca çok özel bir koşulda uyanan zararlı bir devre yerleştirilmişse? Donanımsal Truva Atı ya da Hardware Trojan, çipin tasarımına veya üretimine gizlenen kötü amaçlı değişikliktir. İşletim sisteminin altında bulunduğu için klasik antivirüsler açısından adeta görünmezdir.

``

## Donanımsal Truva Atı nedir?

Bu tehditler, normal devrenin işlevini çoğu zaman bozmayan küçük eklemelerdir. Saldırgan; HDL kaynak kodu, üçüncü taraf IP çekirdeği, sentez araçları, fiziksel yerleşim veya fabrikasyon aşamasında müdahale edebilir. Eklenen yapı genellikle iki parçadan oluşur:

- **Tetikleyici:** Nadir bir olayın gerçekleşmesini bekler.
- **Yük:** Tetiklenince veri sızdırır, sistemi bozar veya güvenlik mekanizmasını etkisizleştirir.

Bir tetikleyicinin etkinleşme koşulu kabaca

$$T = (x_1 \land x_2 \land \cdots \land x_n)$$

şeklinde modellenebilir. Girişlerin bağımsız ve eşit olasılıklı olduğu basitleştirilmiş durumda tetiklenme olasılığı $P(T)=2^{-n}$ olur. Örneğin 32 bitlik özel bir desen yalnızca test ediliyorsa rastlantısal doğrulamada yakalanması son derece güçtür. Truva Atı, milyarlarca test vektörü boyunca uyuyan bir casus gibidir.

## Yazılım zararlısından farkı

| Özellik | Yazılım zararlısı | Donanımsal Truva Atı |
|---|---|---|
| Yerleşim | Dosya, bellek veya işletim sistemi | Mantık kapıları ve silikon |
| Tespit | Antivirüs, EDR, imza analizi | Fiziksel ölçüm ve tasarım doğrulama |
| Temizleme | Dosyayı silme veya sistemi kurma | Çipi değiştirme gerekebilir |
| Kalıcılık | Depolamaya bağlı | Donanım ömrü boyunca sürebilir |
| Tetikleme | Komut, ağ paketi, zaman | Sinyal dizisi, sayaç veya fiziksel koşul |

![donanimsal-truva-atlari-94](/img/donanimsal-truva-atlari-94.svg)


Antivirüs yalnızca işlemcinin kendisine sunduğu dünyayı gözlemleyebilir. İşlemci ölçümleri veya yetki kontrollerini manipüle ediyorsa yazılım, güvenilir olmayan bir hakeme güvenmek zorunda kalır.

## Tehdit çipe nasıl girer?

Küresel yarı iletken tedarik zinciri çok sayıda aktör içerir. Tasarım ekibi hazır IP blokları kullanabilir, üretim başka ülkedeki bir fabrikada yapılabilir ve paketleme farklı bir yükleniciye bırakılabilir. Saldırganın olası müdahale noktaları RTL tasarımı, EDA araçları, maske verileri, üretim süreci ve test altyapısıdır.

Truva Atlarının etkileri arasında gizli anahtarların yan kanal üzerinden sızdırılması, rastgele sayı üretecinin zayıflatılması, ayrıcalık denetimlerinin atlanması ve belirli bir zamanda hizmet dışı bırakma bulunur. Her değişiklik büyük olmak zorunda değildir; birkaç kapı bile kritik bir karşılaştırmayı değiştirebilir.

## Savunma ve doğrulama

Tek bir sihirli tarayıcı yoktur. Savunma, birbirini tamamlayan yöntemlerden oluşur:

| Yöntem | Güçlü yönü | Sınırlaması |
|---|---|---|
| Mantıksal doğrulama | Beklenmeyen davranışı arar | Nadir tetikleyicileri kaçırabilir |
| Güç ve zaman analizi | Fiziksel sapmaları ölçer | Üretim değişkenliği gürültü yaratır |
| Görüntüleme | Devre yapısını karşılaştırır | Pahalı ve yıkıcı olabilir |
| Biçimsel doğrulama | Matematiksel güvence sağlar | Büyük tasarımlarda zorlaşır |
| Tedarik zinciri denetimi | Müdahale olasılığını azaltır | Tüm taraflarda disiplin gerektirir |

Tasarım sırasında güvenlik özellikleri assertion adı verilen kurallarla denetlenebilir:

```systemverilog
property no_secret_on_debug;
  @(posedge clk)
  secret_valid |-> !debug_enable;
endproperty

assert property (no_secret_on_debug);
```

Bu SystemVerilog örneği, gizli veri geçerliyken hata ayıklama arayüzünün açık olmamasını şart koşar. Biçimsel doğrulama araçları olası durumları inceleyerek kuralı bozan yolları arar. Ancak yalnızca yazılmış özellikleri doğrulayabildikleri unutulmamalıdır; belirtilmeyen bir güvenlik beklentisi korunamaz.

## Silikon çağında güven

Donanımsal Truva Atları, güvenliğin yalnızca güçlü parola ve güncel antivirüs olmadığını gösterir. Güven; tasarım kaynaklarının izlenmesi, bağımsız doğrulama, ölçülebilir üretim süreçleri ve güvenilir referans çiplerle karşılaştırma üzerine kurulmalıdır. En ürkütücü tehdit çalışan değil, yıllarca sessizce doğru anı bekleyen devredir.

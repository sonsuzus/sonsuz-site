---
layout: post
title: "Mars Kolonilerinde Kaynak Yönetimi: Oksijen, Su ve Enerjiyi Algoritmalarla Dengelemek"
math: true
categories: 
  - Proje
tags: 
  - mars
  - optimizasyon
  - simülasyon
  - kaynak-yönetimi
  - python
  - algoritma
toc: true
image: /img/mars-kolonilerinde-kaynak-38.png
---

Mars’ta koloni kurmak yalnızca roket göndermekten ibaret değildir. Asıl macera, astronotlar indikten sonra başlar: Her nefes oksijen tüketir, her duş su rezervini azaltır ve çalışan her cihaz enerji ister. Dünya’da musluğu açık unutmak küçük bir hata olabilir; Mars’ta ise simülasyonun kırmızı alarm vermesine neden olur. Bu nedenle koloni tasarımlarında kaynakların üretim, tüketim, depolama ve geri dönüşüm süreçleri algoritmik olarak modellenmelidir.

``

## Kaynak dengesinin temel modeli

Bir kaynağın belirli bir andaki miktarı basitçe stok denklemiyle gösterilebilir:

$$R_{t+1} = R_t + P_t + G_t - C_t - L_t$$

Burada $R_t$ mevcut rezervi, $P_t$ yerel üretimi, $G_t$ geri kazanılan miktarı, $C_t$ tüketimi ve $L_t$ sızıntı ya da sistem kayıplarını temsil eder. Denklem oksijen, su ve enerji için ayrı ayrı uygulanır. Ancak kaynaklar bağımsız değildir. Örneğin suyu elektroliz ederek oksijen üretmek su ve enerji harcar. Dolayısıyla bir kaynağı kurtaran karar, diğer ikisini tehlikeye atabilir.

Kolonide $n$ astronot varsa günlük temel oksijen tüketimi yaklaşık olarak şu şekilde modellenebilir:

$$O_{gun} = n \cdot o + O_{sera} + O_{yedek}$$

Buradaki $o$, kişi başına tüketimdir. Sera bitkileri gündüz oksijen üretebilirken gece tüketiciye dönüşebilir. Bu ayrıntı, simülasyonda zaman dilimlerinin neden önemli olduğunu gösterir.

| Kaynak | Başlıca üretim yöntemi | Büyük tüketiciler | Kritik risk |
|---|---|---|---|
| Oksijen | Elektroliz, bitkiler | İnsanlar, yanma sistemleri | Basınç kaybı |
| Su | Buz madenciliği, geri dönüşüm | İnsanlar, tarım, elektroliz | Donma ve kirlenme |
| Enerji | Güneş, nükleer reaktör | Yaşam desteği, ısıtma | Toz fırtınası |

## Optimizasyon problemi

Amaç yalnızca kaynakları sıfırın üzerinde tutmak değildir. Sistem güvenlik paylarını korurken enerji maliyetini ve ekipman yıpranmasını da azaltmalıdır. Örnek bir amaç fonksiyonu şöyle kurulabilir:

$$\min Z = w_1 E_{tuketim} + w_2 Su_{kaybi} + w_3 Risk$$

$w_1$, $w_2$ ve $w_3$ katsayıları koloninin önceliklerini belirler. Büyük bir toz fırtınası sırasında risk katsayısı artırılabilir. Normal günlerde ise enerji verimliliği öne çıkarılabilir.

Karar değişkenleri arasında elektroliz cihazının çalışma süresi, seraya ayrılan su, bataryaların şarj oranı ve ertelenebilir cihazların programı bulunabilir. Kısıtlar ise rezervlerin güvenli eşiklerin altına düşmemesini sağlar:

$$O_t \geq O_{min}, \quad W_t \geq W_{min}, \quad E_t \geq E_{min}$$

Bu yapı doğrusal programlama, dinamik programlama veya pekiştirmeli öğrenme ile çözülebilir.

| Yaklaşım | Güçlü yönü | Zayıf yönü |
|---|---|---|
| Doğrusal programlama | Hızlı ve açıklanabilir | Karmaşık ilişkilerde sınırlı |
| Dinamik programlama | Zaman bağlı kararları işler | Durum uzayı hızla büyür |
| Pekiştirmeli öğrenme | Değişen koşullara uyum sağlar | Eğitim ve doğrulama zordur |

## Basit bir Python simülasyonu

Aşağıdaki kod, saatlik oksijen stokunu izler ve kritik eşikte elektroliz sistemini çalıştırır:

```python
oxygen = 120.0
critical_level = 45.0
hourly_consumption = 2.4
electrolysis_output = 5.0
energy = 100.0

for hour in range(24):
    oxygen -= hourly_consumption

    if oxygen < critical_level and energy >= 8:
        oxygen += electrolysis_output
        energy -= 8
        action = "Elektroliz çalıştırıldı"
    else:
        action = "Normal çalışma"

    print(hour, round(oxygen, 1), round(energy, 1), action)
```

Bu kontrolcü reaktiftir; yalnızca sorun yaklaşınca davranır. Daha gelişmiş bir model, gelecek güne ait mürettebat faaliyetlerini ve güneş enerjisi tahminlerini kullanarak elektrolizi önceden planlar. Böylece cihaz, enerjinin bol olduğu saatlerde çalıştırılabilir.

Gerçekçi bir Mars simülasyonu ayrıca rastgele arızalar, toz fırtınaları, nüfus artışı ve geri dönüşüm verimindeki azalma gibi senaryoları Monte Carlo yöntemiyle sınamalıdır. Binlerce olası gelecek çalıştırıldığında, yalnızca ortalama koşullarda değil kötü senaryolarda da hayatta kalan politikalar bulunabilir. Kısacası Mars’ta iyi kaynak yönetimi, koloniye “bugünü atlat” demek yerine “yarına güvenli stok bırak” diyebilen algoritmalar tasarlamaktır.

![mars-kolonilerinde-kaynak-38](/img/mars-kolonilerinde-kaynak-38.svg)


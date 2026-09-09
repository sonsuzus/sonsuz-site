---
layout: post
title: "Hipervizör Arenası: Tip 1 ve Tip 2 Sanallaştırmanın Kaynak Mücadelesi"
math: true
categories: 
  - Bilgi
tags: 
  - sanallaştırma
  - hipervizör
  - sanal makineler
toc: true
---

Bir fiziksel bilgisayarda birden fazla işletim sistemi çalıştırmak, teknoloji dünyasının en kullanışlı illüzyonlarından biridir. Bu illüzyonun arkasındaki sihirbaz ise **hipervizördür**. Ancak her hipervizör aynı sahnede gösteri yapmaz: Tip 1 hipervizör doğrudan donanımın üzerine kurulurken Tip 2 hipervizör mevcut bir işletim sisteminin üzerinde çalışır. Bu mimari fark; işlemci, bellek, disk ve ağ kaynaklarının nasıl tüketildiğini doğrudan etkiler.
``

## Hipervizör tam olarak ne yapar?

Hipervizör, fiziksel kaynakları sanal makinelere paylaştıran bir yönetim katmanıdır. Her sanal makine kendi işlemcisine, belleğine ve diskine sahip olduğunu düşünür. Gerçekte ise hipervizör, donanım kaynaklarını sıraya koyan son derece disiplinli bir trafik polisi gibi davranır.

Basitleştirilmiş toplam kaynak maliyeti şöyle düşünülebilir:

$$R_{toplam} = R_{VM} + R_{hipervizor} + R_{ana\ sistem}$$

Tip 1 mimarisinde ayrı bir ana işletim sistemi bulunmadığından $R_{ana\ sistem}$ oldukça küçüktür veya yönetim katmanıyla bütünleşmiştir. Tip 2'de ise Windows, Linux ya da macOS gibi ana işletim sistemi de kaynak tüketir.

## Tip 1: Donanımla doğrudan konuşan hipervizör

**Bare-metal** olarak da bilinen Tip 1 hipervizör, fiziksel sunucuya doğrudan kurulur. VMware ESXi, Microsoft Hyper-V Server ve Xen bu sınıfa örnektir. Arada genel amaçlı bir masaüstü işletim sistemi bulunmadığı için sanal makinelerin donanıma ulaşırken geçtiği katman sayısı azalır.

Bu yaklaşımın önemli avantajları şunlardır:

- Daha düşük işlemci ve bellek ek yükü
- Daha tutarlı disk ve ağ gecikmesi
- Güçlü kaynak izolasyonu
- Merkezi yönetim ve yüksek erişilebilirlik desteği
- Büyük veri merkezlerine uygun ölçeklenebilirlik

Tip 1, özellikle onlarca sanal makinenin aynı sunucuyu paylaştığı ortamlarda avantajlıdır. Fakat kurulumu ve yönetimi masaüstü uygulamalarına göre daha fazla uzmanlık gerektirir.

## Tip 2: İşletim sistemi üzerinde çalışan hipervizör

Tip 2 hipervizör normal bir uygulama gibi ana işletim sistemine kurulur. VirtualBox, VMware Workstation ve Parallels Desktop yaygın örneklerdir. Kullanıcı birkaç tıklamayla sanal makine oluşturabilir; bu nedenle eğitim, yazılım testi ve farklı işletim sistemlerini deneme senaryolarında oldukça pratiktir.

Dezavantajı, sanal makine ile donanım arasında ek bir katman bulunmasıdır:

$$VM \rightarrow Hipervizor \rightarrow Ana\ Isletim\ Sistemi \rightarrow Donanim$$

Örneğin sanal makine diske veri yazmak istediğinde istek önce Tip 2 hipervizöre, ardından ana işletim sisteminin dosya sistemine ve sürücülerine ulaşır. Bu yolculuk ek gecikme ve işlem maliyeti oluşturabilir.

## Kaynak kullanımı karşılaştırması

| Ölçüt | Tip 1 Hipervizör | Tip 2 Hipervizör |
|---|---|---|
| Kurulum yeri | Doğrudan donanım | Ana işletim sistemi |
| Kaynak ek yükü | Düşük | Orta veya yüksek |
| Performans | Fiziksele daha yakın | Ek katmanlardan etkilenebilir |
| İzolasyon | Daha güçlü | Ana sisteme bağımlı |
| Kullanım alanı | Sunucu ve veri merkezi | Masaüstü, eğitim ve test |
| Yönetim kolaylığı | Uzmanlık gerektirir | Başlangıç dostudur |

Aynı anda ayrılan sanal bellek miktarı fiziksel belleği aşarsa **overcommitment** oluşabilir. Yaklaşık oran şu şekilde hesaplanır:

$$O = \frac{Toplam\ sanal\ bellek}{Fiziksel\ bellek}$$

$O > 1$ olduğunda sistem bellek sıkıştırma veya disk üzerinde takas işlemlerine başvurabilir. Bu durum iki tipte de performansı düşürür; ancak Tip 2'de ana işletim sisteminin bellek ihtiyacı baskıyı artırır.

## Küçük bir kaynak kontrolü

Linux üzerinde sanal makine çalıştırmadan önce kaynakları şu komutlarla gözlemleyebiliriz:

```bash
# İşlemci sanallaştırma desteğini gösterir
lscpu | grep Virtualization

# Kullanılabilir belleği okunabilir biçimde listeler
free -h

# Disk ve bölüm kullanımını gösterir
df -h
```

Bu çıktılar, sanal makineye kaç çekirdek ve ne kadar RAM ayrılabileceğini tahmin etmeye yardımcı olur. Kaynakların tamamını sanal makineye vermek iyi fikir değildir; ana sistemin de nefes almaya ihtiyacı vardır.

## Hangisi seçilmeli?

Üretim sunucuları, yoğun iş yükleri ve yüksek erişilebilirlik gerekiyorsa Tip 1 daha verimli ve güvenilir seçimdir. Bilgisayarında Linux denemek, zararlı yazılım analizi yapmak veya uygulamayı farklı sistemlerde test etmek isteyen kullanıcı için Tip 2 çok daha pratiktir. Kısacası Tip 1 performans yarışçısı, Tip 2 ise günlük kullanımın becerikli çok amaçlı aracıdır.

---
layout: post
title: "Out-of-Order Execution: İşlemci Program Sırasını Neden Bazen Umursamaz?"
math: true
categories: 
  - Bilgi
tags: 
  - işlemci
  - out-of-order
  - bilgisayar-mimarisi
  - performans
  - cpu
  - paralellik
toc: true
---

Bir programdaki komutlar belirli bir sırayla yazılır; fakat modern işlemciler bu sıraya harfiyen uymak zorunda değildir. Sonuç değişmediği sürece hazır olan komutları erkenden çalıştırabilirler. **Out-of-order execution**, yani sıra dışı yürütme, işlemcinin boş boş beklemek yerine komutlar arasında küçük bir lojistik operasyon yürütmesidir.
``
## Sorun: Hızlı işlemci, yavaş bekleyiş

Aşağıdaki işlemleri düşünelim:

```c
int x = data[index];   // Bellekten veri bekleniyor
int y = a + b;         // x'e bağlı değil
int z = y * 2;         // y'ye bağlı
int result = x + z;    // Hem x hem z gerekli
```

İlk satır RAM veya önbellekten veri ister. Veri hemen gelmezse katı biçimde program sırasını izleyen bir işlemci, toplama birimi kullanılabilir durumda olsa bile bekleyebilir. Out-of-order çalışan işlemci ise `y = a + b` komutunun `x` değerine bağlı olmadığını fark eder ve onu öne alır.

Buradaki temel amaç, tek bir komutu hızlandırmak değil, işlemcinin farklı yürütme birimlerini aynı anda meşgul tutmaktır. Performans kabaca şu bağıntıyla düşünülebilir:

$$
\text{CPU süresi} = \text{Komut sayısı} \times \text{CPI} \times \text{Saat periyodu}
$$

CPI, komut başına düşen ortalama saat çevrimidir. Sıra dışı yürütme, bekleme boşluklarını başka işler ile doldurarak CPI değerini azaltmaya çalışır.

## Bağımlılıklar patron koltuğunda

İşlemci komutları rastgele karıştırmaz. Önce veri bağımlılıklarını inceler:

| Bağımlılık | Anlamı | Yeniden sıralama durumu |
|---|---|---|
| RAW | Sonraki komut öncekinin ürettiği değeri okur | Gerçek bağımlılık, korunmalıdır |
| WAR | Sonraki komut, öncekinin okuyacağı yere yazar | Register renaming ile çözülebilir |
| WAW | İki komut aynı hedefe yazar | Register renaming ile çözülebilir |
| Bağımsızlık | Komutlar ortak veriye ihtiyaç duymaz | Genellikle paralel yürütülebilir |

Örneğin `z = y * 2`, `y` hesaplanmadan başlayamaz. Buna **Read After Write**, yani RAW bağımlılığı denir. Buna karşılık farklı kayıtlar kullanan iki toplama işlemi aynı anda farklı yürütme birimlerine gönderilebilir.

## Mutfak benzetmesi

Bir aşçı önce makarnanın suyunu kaynatıp ardından salata hazırlamak zorunda değildir. Suyu ocağa koyduktan sonra beklerken sebzeleri doğrayabilir. Ancak makarna haşlanmadan onu süzemez. İşlemci de benzer şekilde bağımsız işleri erkenden yapar, gerçek bağımlılıkları ise bekletir.

| In-order işlemci | Out-of-order işlemci |
|---|---|
| Komutları sırayla yürütür | Hazır komutları önce yürütebilir |
| Daha basit donanım kullanır | Karmaşık zamanlama mantığı gerektirir |
| Beklemelerde kaynaklar boş kalabilir | Yürütme birimlerini daha iyi kullanır |
| Düşük güç tüketimine uygun olabilir | Genellikle daha yüksek performans sağlar |

## Sonuç nasıl hâlâ doğru kalıyor?

İşlemcinin sihirli araçlarından biri **Reorder Buffer**, yani ROB yapısıdır. Komutlar farklı sırada yürütülse bile sonuçlar mimari duruma program sırasıyla aktarılır. Bu aşamaya **retirement** veya **commit** denir.

Genel akış şöyledir:

1. Komutlar getirilir ve çözümlenir.
2. Yazma çakışmalarını azaltmak için fiziksel kayıtlar yeniden adlandırılır.
3. Hazır girdilere sahip komutlar yürütme birimlerine gönderilir.
4. Sonuçlar geçici yapılarda tutulur.
5. Komutlar program sırasıyla tamamlanmış kabul edilir.

Bu düzen, bir hata veya istisna oluştuğunda da önemlidir. Örneğin spekülatif olarak çalıştırılan yanlış bir dalın sonuçları ROB üzerinden iptal edilebilir. Program, işlemcinin perde arkasındaki telaşını görmez.

## Bedelsiz performans yok

Out-of-order execution; daha fazla transistör, enerji tüketimi ve tasarım karmaşıklığı getirir. Ayrıca spekülatif yürütmeyle birleştiğinde Spectre gibi yan kanal açıklarının ortaya çıkmasına katkıda bulunabilir. Bu nedenle küçük mikrodenetleyiciler sıklıkla basit in-order tasarımları seçerken masaüstü ve sunucu işlemcileri performans uğruna daha gelişmiş yapılar kullanır.

Kısacası işlemci program sırasını gerçekten yok saymaz; yalnızca **yürütme sırasını esnetir**, görünür sonuçları ise doğru sırada sunar. Sahne arkasında herkes koşturabilir, yeter ki perde açıldığında oyuncular doğru yerde olsun.

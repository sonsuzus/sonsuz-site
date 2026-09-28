---
layout: post
title: "İşlemci Mimarisinde Out-of-Order Execution: Mantık Sırasını Bozan Hızlandırma"
math: true
categories: 
  - Bilgi
tags: 
  - işlemci mimarisi
  - out-of-order execution
  - cpu
  - performans
  - komut düzeyi paralellik
  - mikromimari
toc: true
image: /img/islemci-mimarisinde-out-90.png
---

Bir programdaki komutlar bize düzgün bir sıra hâlinde görünür: önce oku, sonra hesapla, en sonunda sonucu yaz. Modern işlemciler ise bu sırayı kutsal kabul etmez. Bir komut veriyi beklerken ondan bağımsız başka komutları çalıştırır, sonuçları geçici olarak saklar ve dışarıdan bakıldığında her şey sırayla gerçekleşmiş gibi davranır. Bu kontrollü karmaşanın adı **out-of-order execution**, yani sıra dışı yürütmedir.


![islemci-mimarisinde-out-90](/img/islemci-mimarisinde-out-90.svg)

``

## Neden sırayı bozmak gerekiyor?

İşlemci ile ana bellek aynı hızda değildir. Bir toplama işlemi birkaç saat çevriminde bitebilirken önbellekte bulunamayan verinin gelmesi yüzlerce çevrim sürebilir. İşlemci bu süre boyunca beklerse değerli yürütme birimleri boş kalır.

Örneğin şu işlemleri düşünelim:

```c
x = memory[index];   // Bellekten veri bekleyebilir
y = a + b;           // x değerinden bağımsızdır
z = y * 4;           // y hazır olduğunda çalışabilir
result = x + z;      // Hem x hem z gereklidir
```

Sıralı bir işlemci ilk satır geciktiğinde diğer satırları da bekletir. Sıra dışı işlemci ise `y` ve ardından `z` hesaplamasını aradan çıkarır. `x` geldiğinde yalnızca son toplama kalır.

| Yaklaşım | Komut başlatma sırası | Sonuçların görünür olma sırası | Kaynak kullanımı |
|---|---|---|---|
| In-order | Program sırası | Program sırası | Gecikmelerde düşer |
| Out-of-order | Hazır olma durumuna göre | Program sırası | Genellikle daha yüksektir |
| Çok çekirdek | Farklı iş parçacıklarına göre | Yazılım modeline bağlı | Çekirdekler arasında dağılır |

Buradaki önemli ayrım şudur: İşlemci komutları farklı sırada **yürütebilir**, fakat sonuçları mimari duruma program sırasıyla **emekli eder**.

## Bağımlılıkların matematiği

Komutlar bir yönlü çizgeyle modellenebilir. Her komut bir düğüm, veri bağımlılıkları ise kenardır. $I_i \rightarrow I_j$ kenarı, $I_j$ komutunun çalışmak için $I_i$ sonucunu beklediğini belirtir.

Bir komutun en erken başlama zamanı yaklaşık olarak şöyle yazılabilir:

$$
S_j = \max_{i \in pred(j)}(S_i + L_i)
$$

Burada $S_j$ başlangıç zamanını, $L_i$ önceki komutun gecikmesini ve $pred(j)$ doğrudan bağımlı olunan komutları gösterir. Öncel kümesi boş olan komutlar aynı anda yürütülmeye adaydır. İşlemcinin amacı, donanım kaynakları izin verdiği ölçüde bu bağımsız düğümleri paralel çalıştırmaktır.

İdeal performans kabaca komut düzeyi paralellik ile sınırlıdır:

$$
IPC \leq \min(W, ILP)
$$

$IPC$, çevrim başına tamamlanan komut sayısıdır. $W$ işlemcinin yürütme genişliği, $ILP$ ise programda o anda bulunan bağımsız komut miktarıdır. Sekiz yürütme birimi bulunması, bağımlılık zinciri yüzünden yalnızca iki hazır komut varsa sekiz kat hız sağlamaz.

## Donanım bu numarayı nasıl yapıyor?

Komutlar önce çözülür ve **reservation station** benzeri bekleme alanlarına gönderilir. Operandları hazır olan mikro işlemler uygun toplama, çarpma veya yükleme birimine seçilir. Sonuçlar doğrudan programın gördüğü kayıtlara yazılmak yerine geçici fiziksel kayıtlarda tutulur.

**Register renaming**, sahte bağımlılıkları ortadan kaldırır. Örneğin iki komut aynı mimari kayda yazsa bile işlemci onları farklı fiziksel kayıtlara eşleyebilir. Böylece yalnızca gerçek veri akışı korunur.

Tamamlanan işlemler **reorder buffer (ROB)** içinde program sırasını bekler. ROB başındaki komut hatasız tamamlandıysa sonucu görünür hâle gelir. Bir istisna oluşursa veya dallanma tahmini yanlış çıkarsa daha genç spekülatif komutlar iptal edilir.

```text
getir -> çöz -> yeniden adlandır -> hazır komutu seç
      -> yürüt -> ROB'a yaz -> program sırasıyla emekli et
```

Bu akış, hızlı yürütme ile kesin program davranışını uzlaştırır.

## Bedava hız mı?

Elbette değil. Büyük ROB yapıları, fiziksel kayıt dosyaları, bağımlılık kontrolü ve seçim mantığı enerji tüketir. Dallanma tahmini yanlışsa yapılan spekülatif işler çöpe gider. Ayrıca Spectre gibi saldırılar, iptal edilen komutların bile önbellekte gözlemlenebilir izler bırakabileceğini göstermiştir.

Yine de out-of-order execution, modern CPU performansının temel direklerinden biridir. İşlemci mantık sırasını gerçekten yok etmez; onu geçici olarak esnetir, bağımsız işleri öne alır ve finalde bütün parçaları programın beklediği sıraya ustaca dizer.

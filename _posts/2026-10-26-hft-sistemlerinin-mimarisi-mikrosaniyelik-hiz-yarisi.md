---
layout: post
title: "HFT Sistemlerinin Mimarisi: Mikrosaniyelik Hız Yarışı"
math: true
categories: 
  - Bilgi
tags: 
  - hft
  - düşük gecikme
  - algoritmik işlem
  - finansal teknolojiler
  - c++
  - sistem mimarisi
toc: true
image: /img/hft-sistemlerinin-mimarisi-21.png
---

Bir göz kırpma yaklaşık 100–300 milisaniye sürer. Yüksek frekanslı işlem (HFT) sistemlerinde ise bu süre, binlerce karar vermek için yeterince uzundur. Fiyat değişikliklerini herkesten önce değerlendirmeye çalışan bu sistemlerde hız yalnızca güçlü bir işlemci meselesi değildir; ağ kartından veri yapısına kadar bütün mimari, mikrosaniyeleri koruyacak şekilde tasarlanır.

![hft-sistemlerinin-mimarisi-21](/img/hft-sistemlerinin-mimarisi-21.svg)

``

## HFT tam olarak ne yapar?

HFT sistemleri piyasa verilerini gerçek zamanlı olarak alır, algoritmik stratejilerle değerlendirir ve saniyenin çok küçük bir bölümünde emir üretir. Piyasa yapıcılığı, farklı platformlar arasındaki fiyat uyuşmazlıklarını izleme ve portföy riskini dengeleme yaygın kullanım alanlarıdır.

Bir işlemin basitleştirilmiş beklenen değeri şöyle ifade edilebilir:

$$
E[P] = p_f \cdot G - (1-p_f) \cdot Z - C
$$

Burada $p_f$ emrin istenen koşullarda gerçekleşme olasılığı, $G$ beklenen kazanç, $Z$ olumsuz fiyat hareketinden doğan zarar ve $C$ komisyon ile altyapı maliyetidir. Gecikme arttığında emir sırasındaki konum kötüleşebilir; dolayısıyla $p_f$ düşerken zarar ihtimali büyüyebilir.

## Temel mimari katmanları

Tipik bir HFT hattı aşağıdaki bileşenlerden oluşur:

1. **Piyasa veri alıcısı:** Borsanın gönderdiği ham paketleri yakalar.
2. **Feed handler:** Paketleri çözer ve dahili fiyat defteri modelini günceller.
3. **Strateji motoru:** Fiyat, hacim ve risk sinyallerinden işlem kararı üretir.
4. **Risk katmanı:** Pozisyon, emir büyüklüğü ve kayıp limitlerini denetler.
5. **Emir geçidi:** Kararı borsanın protokolüne çevirerek iletir.
6. **Telemetri sistemi:** Gecikme dağılımlarını ve hataları kaydeder.

Bu yolun toplam gecikmesi kabaca

$$
L_{toplam}=L_{ağ}+L_{çözümleme}+L_{strateji}+L_{risk}+L_{emir}
$$

şeklindedir. Her katmanda kazanılan birkaç mikrosaniye, toplamda ciddi bir avantaj oluşturabilir.

| Yaklaşım | Geleneksel sistem | HFT sistemi |
|---|---|---|
| Ağ erişimi | Standart TCP/IP yığını | Kernel bypass, optimize UDP |
| Bellek | Dinamik tahsis yaygın | Önceden ayrılmış bellek |
| Veri yapısı | Esnek koleksiyonlar | Cache dostu sabit diziler |
| İş parçacıkları | Genel amaçlı zamanlama | CPU çekirdeğine sabitleme |
| Performans ölçümü | Ortalama gecikme | Kuyruk yüzdelikleri ve jitter |

## Mikrosaniyeler neden önemlidir?

Borsalarda aynı fiyat seviyesindeki emirler çoğunlukla zaman önceliğine göre sıralanır. İki şirket aynı alış emrini gönderirse birkaç mikrosaniye önce ulaşan emir kuyruğun önüne geçebilir. Bu nedenle gecikme yalnızca kararın hızını değil, gerçekleşme olasılığını da etkiler.

Ayrıca ortalama gecikme tek başına yeterli değildir. Sistem çoğu zaman 10 mikrosaniyede yanıt verip nadiren 2 milisaniyeye sıçrıyorsa kritik anlarda geride kalabilir. Bu değişkenliğe **jitter** denir. HFT ekipleri ortalama yerine $p99$, $p99.9$ ve maksimum gecikme değerlerini özellikle takip eder.

## Sıcak yol üzerinde kod tasarımı

Aşağıdaki C++ örneği, alış ve satış fiyatından orta noktayı hesaplayan küçük bir sıcak yol fonksiyonudur:

```cpp
struct Quote {
    double bid;
    double ask;
};

inline double midpoint(const Quote& quote) noexcept {
    return (quote.bid + quote.ask) * 0.5;
}

bool shouldBuy(const Quote& quote, double reference) noexcept {
    return midpoint(quote) < reference;
}
```

`const` referans gereksiz kopyayı önler, `noexcept` fonksiyonun istisna üretmeyeceğini bildirir ve `inline` çağrı maliyetinin azaltılmasına yardımcı olabilir. Gerçek sistemlerde kayan nokta yerine sabit noktalı tamsayılar tercih edilebilir; böylece fiyatlar örneğin kuruş cinsinden kesin biçimde saklanır.

## Donanım da mimarinin parçasıdır

Borsaya fiziksel olarak yakın veri merkezlerinde sunucu barındırmak, fiber üzerindeki yayılma süresini azaltır. Optimize ağ kartları, FPGA’ler, yüksek saat hızlı CPU’lar ve NUMA farkındalığı da gecikme bütçesine katkıda bulunur. Ancak hız uğruna risk kontrollerini kaldırmak doğru değildir. İyi bir mimari, kontrolleri atlamak yerine onları tahmin edilebilir ve düşük gecikmeli hâle getirir.

Sonuç olarak HFT, yalnızca hızlı kod yazma sanatı değildir. Ağ, işletim sistemi, işlemci önbelleği, algoritma, risk yönetimi ve fiziksel mesafenin birlikte optimize edildiği uçtan uca bir mühendislik disiplinidir. Mikrosaniyeler önemlidir; çünkü elektronik piyasalarda küçük bir zaman farkı, kuyrukta ilk veya son olmak arasındaki fark olabilir.

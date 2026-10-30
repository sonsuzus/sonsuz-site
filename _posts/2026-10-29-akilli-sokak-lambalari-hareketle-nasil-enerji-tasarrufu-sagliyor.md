---
layout: post
title: "Akıllı Sokak Lambaları Hareketle Nasıl Enerji Tasarrufu Sağlıyor?"
math: true
categories: 
  - Bilgi
tags: 
  - akıllı aydınlatma
  - enerji tasarrufu
  - nesnelerin interneti
  - hareket sensörü
  - akıllı şehirler
  - otomasyon
toc: true
image: /img/akilli-sokak-lambalari-80.png
---

Gece boyunca tam güçte çalışan sokak lambaları güvenliği artırır; ancak boş bir caddenin saatlerce aydınlatılması ciddi enerji kaybına yol açar. Akıllı aydınlatma sistemleri, yaya ve araç hareketini algılayarak ışık seviyesini gerçek zamanlı biçimde değiştirir. Böylece sokak tamamen karanlık bırakılmadan yalnızca ihtiyaç duyulan yerde ve zamanda yüksek parlaklık sağlanır.

``

## Sistem hangi bileşenlerden oluşur?

Hareket tabanlı bir aydınlatma sistemi yalnızca lambaya bağlanmış basit bir sensörden ibaret değildir. Sensörler, kontrol birimi, haberleşme ağı ve dim edilebilir LED sürücüler birlikte çalışır.

- **PIR sensörü:** İnsan ve hayvanların yaydığı kızılötesi enerjideki değişimi algılar.
- **Mikrodalga radar:** Radyo dalgaları göndererek hareketi ve bazı sistemlerde hızı ölçer.
- **Kamera veya görüntü sensörü:** Yaya, bisiklet ve araç sınıflandırması yapabilir.
- **Ortam ışığı sensörü:** Sistemin gündüz gereksiz yere çalışmasını engeller.
- **Kontrolcü:** Sensör verilerini işleyerek lambanın parlaklık kararını verir.
- **Haberleşme modülü:** Komşu lambalarla veya merkezi yönetim platformuyla veri paylaşır.

| Algılama yöntemi | Güçlü yönü | Sınırlaması | Uygun kullanım |
|---|---|---|---|
| PIR | Ucuz ve düşük enerji tüketimli | Araç hızını ölçemez | Yaya yolları |
| Radar | Yağmur ve karanlıktan az etkilenir | Daha pahalıdır | Ana yollar |
| Kamera | Nesne türünü ayırt edebilir | Gizlilik ve işlem yükü doğurur | Yoğun kavşaklar |

![akilli-sokak-lambalari-80](/img/akilli-sokak-lambalari-80.svg)


## Parlaklık kararı nasıl verilir?

Lambalar genellikle hareket yokken tamamen kapanmaz. Örneğin temel parlaklık yüzde 25 seviyesinde tutulur. Bir yaya algılandığında yüzde 60'a, hızlı bir araç algılandığında ise yüzde 100'e çıkılabilir. Belirli bir bekleme süresinden sonra ışık yumuşak biçimde başlangıç seviyesine döner. Bu geçiş, sürücülerin ani ışık değişiminden rahatsız olmasını da önler.

Basitleştirilmiş bir parlaklık modeli şöyle yazılabilir:

$$
L = \min(L_{max}, L_{base} + w_p P + w_v V)
$$

Burada $L$ hedef parlaklığı, $L_{base}$ bekleme seviyesini, $P$ yaya varlığını ve $V$ normalize edilmiş araç hızını temsil eder. $w_p$ ile $w_v$ ise belediyenin güvenlik politikasına göre belirlenen ağırlıklardır.

Enerji tüketimi yaklaşık olarak güç ve çalışma süresinin çarpımıdır:

$$
E = \sum_{i=1}^{n} P_i \times t_i
$$

100 watt gücündeki bir lamba 10 saat tam parlaklıkta çalışırsa 1 kWh tüketir. Aynı lamba gecenin yüzde 70'inde yüzde 25 güçte, kalanında tam güçte çalışırsa yaklaşık $0.475$ kWh tüketir. Gerçek değer LED sürücüsünün verim eğrisine bağlı olsa da tasarruf potansiyeli oldukça açıktır.

## Basit bir kontrol algoritması

Aşağıdaki Python örneği, algılanan nesneye göre hedef parlaklığı belirler. Gerçek sistemde bu değer PWM sinyaline veya akıllı LED sürücüsüne gönderilebilir.

```python
def hedef_parlaklik(hareket, nesne_turu, hiz=0):
    if not hareket:
        return 25  # Güvenlik için düşük bekleme ışığı

    if nesne_turu == "yaya":
        return 60
    elif nesne_turu == "bisiklet":
        return 75
    elif nesne_turu == "arac":
        return min(100, 70 + hiz * 0.5)

    return 50

parlaklik = hedef_parlaklik(True, "arac", 50)
print(f"Lamba seviyesi: %{parlaklik}")
```

Algoritmanın yalnızca mevcut lambayı değil, ilerideki birkaç lambayı da etkinleştirmesi önemlidir. Araç bir direğe ulaştığında komşu direklere mesaj gönderilirse aracın önünde hareket eden bir **ışık koridoru** oluşur.

## Tasarruf kadar güvenlik de önemli

Akıllı aydınlatmada amaç en düşük enerji tüketimini elde etmek değil, güvenlik koşullarını koruyarak gereksiz tüketimi azaltmaktır. Sensör arızaları, yanlış algılamalar, hava koşulları ve ağ kesintileri hesaba katılmalıdır. Haberleşme başarısız olduğunda lambaların güvenli bir sabit seviyeye geçmesi iyi bir yedekleme yaklaşımıdır.

Doğru tasarlanmış sistemler enerji maliyetlerini düşürür, LED ömrünü uzatır ve ışık kirliliğini azaltır. Kısacası geleceğin sokak lambaları yalnızca çevreyi aydınlatmayacak; çevresini gözlemleyip ne kadar ışığa ihtiyaç olduğunu da kendileri hesaplayacaktır.

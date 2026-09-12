---
layout: post
title: "Dijital Karıncalar İş Başında: Çok Ajanlı Sistemlerde Sürü Zekâsı"
math: true
categories: 
  - Bilgi
tags: 
  - sürü zekâsı
  - çok ajanlı sistemler
  - yapay zekâ
toc: true
---

Bir karıncanın tek başına trafik rotası hesaplamasını veya karmaşık bir lojistik ağını yönetmesini beklemeyiz. Ancak binlerce karınca, merkezi bir yönetici olmadan yiyeceğe giden kısa yolları keşfedebilir. Sürü zekâsı, doğadaki bu şaşırtıcı kolektif davranışı ufak ve otonom yazılım ajanlarına taşır. Her ajan yalnızca basit kurallara uyar; ortaya çıkan sistem ise tek bir ajanın kapasitesini aşan problemleri çözebilir.
``

## Sürü zekâsı nedir?

Sürü zekâsı, çok sayıda görece basit ajanın birbirleriyle ve çevreleriyle yerel etkileşim kurması sonucunda oluşan kolektif problem çözme yeteneğidir. Sistemin başında bütün emirleri veren bir patron bulunmaz. Bunun yerine ajanlar yakın komşularını gözlemler, çevreden veri toplar ve küçük kararlar verir.

Bu yaklaşımın kalbinde **beliren davranış** bulunur. Beliren davranış, sistem düzeyindeki düzenin ajanlara açıkça programlanmamış olmasıdır. Örneğin hiçbir karıncaya “en kısa yolu bul” komutu verilmez. Karıncalar feromon bırakır, güçlü feromon izlerini daha sık takip eder ve feromon zamanla buharlaşır. Kısa rotalar daha hızlı güçlendiği için koloni sonunda iyi bir yol üzerinde uzlaşır.

## Matematiksel mantık: İzleri takip etmek

Karınca Kolonisi Optimizasyonu yönteminde bir ajanın $i$ noktasından $j$ noktasına gitme olasılığı şöyle modellenebilir:

$$P_{ij} = \frac{\tau_{ij}^{\alpha} \eta_{ij}^{\beta}}{\sum_k \tau_{ik}^{\alpha} \eta_{ik}^{\beta}}$$

Burada $\tau_{ij}$ ilgili rotadaki feromon miktarını, $\eta_{ij}$ ise mesafe gibi sezgisel kalite bilgisini temsil eder. $\alpha$ ve $\beta$, geçmiş deneyim ile anlık bilginin önemini ayarlar.

Feromonun güncellenmesi ise genel olarak şu fikre dayanır:

$$\tau_{ij} \leftarrow (1-\rho)\tau_{ij} + \Delta\tau_{ij}$$

$\rho$ buharlaşma oranıdır. Buharlaşma olmasaydı ajanlar erken keşfedilen kötü bir rotaya sonsuza kadar saplanabilirdi. Yani unutmak, bu sistemlerde bir hata değil; keşif yapabilmenin önemli bir parçasıdır.

| Özellik | Merkezi sistem | Sürü zekâsı |
|---|---|---|
| Karar verme | Tek yönetici | Dağıtık ajanlar |
| Arıza etkisi | Kritik olabilir | Genellikle sınırlıdır |
| Bilgi kapsamı | Küresel | Yerel |
| Ölçeklenme | Darboğaz oluşabilir | Yeni ajanlarla güçlenebilir |
| Davranış | Önceden planlı | Etkileşimlerden belirir |

## Küçük bir dijital karınca

Aşağıdaki Python kodu, bir ajanın feromon ve mesafe değerlerine göre sonraki yolu seçmesini gösteren sadeleştirilmiş bir örnektir:

```python
import random

def yol_secenekleri(feromonlar, mesafeler, alpha=1, beta=2):
    agirliklar = []

    for feromon, mesafe in zip(feromonlar, mesafeler):
        sezgisel_deger = 1 / mesafe
        agirlik = (feromon ** alpha) * (sezgisel_deger ** beta)
        agirliklar.append(agirlik)

    return random.choices(
        range(len(agirliklar)),
        weights=agirliklar,
        k=1
    )[0]

secim = yol_secenekleri(
    feromonlar=[1.0, 2.5, 0.8],
    mesafeler=[10, 14, 6]
)
print('Seçilen yol:', secim)
```

Fonksiyon doğrudan en güçlü izi seçmez; seçeneklere ağırlıkları oranında şans tanır. Bu rastlantısallık, ajanların yeni yolları keşfetmesini sağlar. Yalnızca en iyi görünen yol seçilseydi sistem hızla tekdüzeleşir ve daha kaliteli alternatifleri gözden kaçırabilirdi.

## Basit kurallardan karmaşık sonuçlara

Başarılı bir sürü sistemi iki davranışı dengeler: **keşif** ve **sömürü**. Keşif, bilinmeyen seçeneklerin denenmesidir. Sömürü ise daha önce iyi sonuç vermiş bilginin kullanılmasıdır. Fazla keşif kararsızlığa, fazla sömürü ise yerel optimuma hapsolmaya yol açar.

Bu sistemler robot filolarında, teslimat rotalarının planlanmasında, ağ trafiğinin yönlendirilmesinde, oyun karakterlerinde ve afet bölgelerinin taranmasında kullanılabilir. Bir drone devre dışı kaldığında görev tamamen durmaz; diğer ajanlar yerel kuralları izleyerek boşluğu doldurabilir.

Sürü zekâsının en çarpıcı dersi şudur: Karmaşık bir problemi çözmek için her zaman karmaşık bir birey gerekmez. Doğru etkileşim kuralları, geri bildirim mekanizmaları ve biraz kontrollü rastlantısallık sayesinde dijital karıncalar oldukça büyük işlerin altından kalkabilir.

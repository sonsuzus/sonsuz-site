---
layout: post
title: "Küplerden Sonsuz Dünyalara: Voksel Tabanlı Dünya Temsili"
math: true
categories: 
  - Bilgi
tags: 
  - voksel
  - minecraft
  - oyun geliştirme
  - grafik programlama
  - performans
  - prosedürel üretim
toc: true
image: /img/kuplerden-sonsuz-dunyalara-19.png
---

![kuplerden-sonsuz-dunyalara-19](/img/kuplerden-sonsuz-dunyalara-19.svg)


Minecraft dünyasına uzaktan bakınca dağlar, mağaralar ve ormanlar görürüz; motorun gözünden bakınca ise devasa bir üç boyutlu tablo vardır. Bu tablonun her hücresi, belirli bir konumdaki bloğun türünü saklar. İşte hacimsel piksel anlamına gelen **voksel**, küplerle kurulan bu dijital evrenin temel yapı taşıdır.
``

## Voksel tam olarak nedir?

İki boyutlu bir görüntüde piksel, $(x, y)$ koordinatındaki rengi temsil eder. Voksel ise buna derinlik ekleyerek $(x, y, z)$ konumundaki hacimsel bilgiyi temsil eder. Bir voksel yalnızca “dolu” veya “boş” olmak zorunda değildir; taş, su, cam ya da toprak gibi bir blok kimliği de taşıyabilir.

Boyutları $W$, $H$ ve $D$ olan yoğun bir dünyanın toplam hücre sayısı:

$$N = W × H × D$$

Örneğin $1024^3$ hücre, bir milyardan fazla voksel demektir. Her voksel yalnızca 2 bayt kullansa bile yaklaşık 2 GB bellek gerekir. Üstelik blok ışığı, nem ve biyom gibi ek veriler bu miktarı büyütür. Bu nedenle oyunlar bütün dünyayı tek parça hâlinde belleğe yüklemez.

| Temsil yöntemi | Güçlü yanı | Zayıf yanı |
|---|---|---|
| Yoğun 3B dizi | Hızlı ve doğrudan erişim | Boş alanlarda bellek israfı |
| Seyrek yapı | Boş dünyalarda verimli | Erişim ve güncelleme daha karmaşık |
| Chunk sistemi | Yükleme ve kayıt kolaylığı | Sınır yönetimi gerekir |
| Octree | Farklı ayrıntı seviyeleri | Uygulaması zor olabilir |

## Dünyayı parçalara ayırmak: Chunk sistemi

Minecraft benzeri oyunlar dünyayı **chunk** adı verilen bölgelere böler. Oyuncuya yakın chunk’lar belleğe alınır; uzaktakiler kaydedilip kaldırılır. Böylece teorik olarak sınırsız bir dünya, sınırlı RAM ile gezilebilir.

Bir chunk’ın $16 × 256 × 16$ bloktan oluştuğunu varsayarsak:

$$16 × 256 × 16 = 65\,536$$

hücre elde edilir. Oyuncu hareket ettiğinde yalnızca görüş mesafesine giren yeni chunk’lar üretilir veya diskten okunur. Bu yaklaşım hem prosedürel dünya üretimini hem de paralel işlemeyi kolaylaştırır.

```csharp
public class Chunk
{
    public const int Width = 16;
    public const int Height = 256;
    private readonly ushort[,,] blocks =
        new ushort[Width, Height, Width];

    public ushort GetBlock(int x, int y, int z)
        => blocks[x, y, z];

    public void SetBlock(int x, int y, int z, ushort blockId)
        => blocks[x, y, z] = blockId;
}
```

Bu orta düzey C# örneği, blok kimliklerini bir chunk içinde saklar. `ushort`, 65.536 farklı blok durumunu temsil edebilir. Gerçek bir motorda sınır kontrolleri, ışık verisi ve değiştirilmiş blokların diske kaydı da eklenir.

## Her küpü çizmek neden kötü bir fikir?

Bir küpün 6 yüzü ve genellikle 12 üçgeni vardır. Bir milyon bloğu ayrı ayrı çizmek, görünmeyen iç yüzler yüzünden ekran kartını gereksiz yere yorar. Çözüm, yalnızca havaya komşu yüzleri mesh’e eklemektir. İki katı blok yan yana geldiğinde aralarındaki yüzler görünmez ve üretilmez.

| Optimizasyon | Etkisi |
|---|---|
| Yüz eleme | Kapalı yüzleri çizmez |
| Greedy meshing | Bitişik yüzleri büyük dörtgenlerde birleştirir |
| Frustum culling | Kamera dışında kalan chunk’ları atlar |
| Occlusion culling | Başka nesnelerin arkasındakileri atlar |
| LOD | Uzaktaki bölgeleri daha basit gösterir |

Greedy meshing özellikle değerlidir: Yan yana duran 100 aynı çim yüzü, 100 ayrı dörtgen yerine tek bir büyük dörtgene dönüşebilir. Böylece üçgen sayısı ve çizim maliyeti ciddi biçimde azalır.

## Değiştirilebilir dünyanın bedeli

Voksellerin en büyük avantajı, dünyayı düzenlemeyi doğal hâle getirmesidir. Bir blok kırıldığında ilgili hücre “hava” yapılır. Ancak değişiklik chunk mesh’inin yeniden oluşturulmasını gerektirir. Blok chunk sınırındaysa komşu chunk da etkilenebilir.

Bu yüzden iyi bir motor; mesh üretimini arka plan iş parçacıklarında yapar, yalnızca değişen chunk’ları günceller ve GPU’ya gönderilen veriyi sınırlar. Sonuç olarak voksel dünyalar basit küplerden oluşsa da performanslı çalışmaları; veri sıkıştırma, görünürlük hesaplama, paralel üretim ve akıllı mesh tekniklerinin uyumuna bağlıdır. Küpler masum görünür, fakat milyonlarcası bir araya geldiğinde motor geliştiricisini gerçek bir optimizasyon madencisine dönüştürür.

---
layout: post
title: "Prosedürel Animasyon Sistemleri: Hareketi Oynatmak Yerine Hesaplamak"
math: true
categories: 
  - Bilgi
tags: 
  - prosedürel animasyon
  - oyun geliştirme
  - ters kinematik
  - karakter kontrolü
  - unity
  - gerçek zamanlı grafikler
toc: true
image: /img/prosedurel-animasyon-sistemleri-95.png
---

Bir karakterin merdivene bastığında ayağını gerçekten basamağa koyduğunu, eğimli arazide dengesini koruduğunu veya dev bir yaratığın her adımda çevreye uyum sağladığını düşünün. Bu hareketlerin tamamını önceden hazırlamak yerine çalışma anında hesaplamak, **prosedürel animasyonun** temel fikridir. Böylece karakter yalnızca bir animasyon klibini oynatan kukla olmaktan çıkar; çevresine tepki veren dinamik bir sisteme dönüşür.


![prosedurel-animasyon-sistemleri-95](/img/prosedurel-animasyon-sistemleri-95.svg)

``

## Önceden kaydedilmiş animasyon mu, prosedürel hareket mi?

Geleneksel sistemlerde sanatçı; yürüme, koşma ve zıplama gibi hareketleri önceden üretir. Oyun motoru uygun klibi seçerek kemiklere uygular. Prosedürel yaklaşımda ise kemiklerin konum ve dönüşleri; hedefler, fizik kuralları, arazi verileri ve karakterin mevcut durumu kullanılarak hesaplanır.

| Özellik | Hazır animasyon | Prosedürel animasyon |
|---|---|---|
| Hareket kaynağı | Önceden hazırlanmış klip | Gerçek zamanlı hesaplama |
| Çevreye uyum | Sınırlı | Yüksek |
| Sanatçı kontrolü | Çok yüksek | Kurallara bağlı |
| İşlem maliyeti | Genellikle düşük | Daha yüksek olabilir |
| Tekrar hissi | Belirginleşebilir | Daha doğal çeşitlilik sağlar |

Bu iki yöntem rakip olmak zorunda değildir. Modern oyunlar çoğunlukla temel yürüyüş klibini oynatır, ardından ayakları zemine yerleştirmek veya karakterin başını hedefe çevirmek için prosedürel düzeltmeler uygular.

## Matematiksel temel

Karakter iskeleti, birbirine bağlı dönüşümlerden oluşan bir hiyerarşidir. Bir kemiğin dünya uzayındaki dönüşümü, ebeveynlerinin dönüşümleriyle çarpılarak bulunur:

$$T_{dunya} = T_0 T_1 T_2 ... T_n$$

Buradaki her $T$, konum, dönüş ve ölçek bilgisi taşıyan bir dönüşüm matrisidir. El veya ayak gibi uç noktanın istenen hedefe ulaşması gerektiğinde **ters kinematik** (Inverse Kinematics, IK) kullanılır. İleri kinematik eklem açılarını kullanarak elin yerini bulurken ters kinematik, hedef konumdan yola çıkarak gerekli eklem açılarını arar.

İki kemikli bir bacakta kosinüs teoremi önemli bir rol oynar:

$$c^2 = a^2 + b^2 - 2ab\cos(\theta)$$

$a$ ve $b$ kemik uzunluklarını, $c$ kalça ile ayak hedefi arasındaki mesafeyi temsil eder. Buradan elde edilen $\theta$, dizin ne kadar büküleceğini belirlemeye yardım eder. Hedef erişim alanının dışındaysa sistem mesafeyi sınırlandırmalıdır; aksi hâlde bacak lastik gibi uzayabilir.

## Zemine uyum sağlayan ayaklar

Basit bir ayak yerleştirme sistemi, ayağın üstünden aşağı doğru ışın göndererek zemini bulur. Çarpışma noktası ayağın hedef konumu, yüzey normali ise yaklaşık yönelimi olur.

```csharp
void UpdateFoot(Transform foot, Vector3 hipPosition)
{
    Vector3 origin = foot.position + Vector3.up * 0.5f;

    if (Physics.Raycast(origin, Vector3.down, out RaycastHit hit, 1.5f))
    {
        Vector3 target = hit.point + hit.normal * 0.05f;
        foot.position = Vector3.Lerp(
            foot.position,
            target,
            Time.deltaTime * 12f
        );

        Quaternion rotation = Quaternion.FromToRotation(
            foot.up,
            hit.normal
        ) * foot.rotation;

        foot.rotation = Quaternion.Slerp(
            foot.rotation,
            rotation,
            Time.deltaTime * 10f
        );
    }
}
```

Bu Unity örneği zemini `Raycast` ile algılar, ayağı çarpışma noktasına yaklaştırır ve yüzey normaline göre döndürür. `Lerp` ile `Slerp` kullanılması ani sıçramaları azaltır. Üretim ortamında doğrudan kemik dönüşümünü değiştirmek yerine motorun IK katmanı kullanılmalı; ayrıca ayağın havada olduğu adım evresi kontrol edilmelidir.

## Sistemi doğal gösteren ayrıntılar

Tamamen doğru hesaplanan hareket her zaman doğal görünmez. Karakterin ağırlık merkezi, adım ritmi ve küçük gecikmeler algıyı ciddi biçimde etkiler. Hedefler arasında yumuşak geçiş yapmak için şu karışım kullanılabilir:

$$P = (1-t)P_0 + tP_1$$

Ancak sabit hızla ilerleyen $t$, robotik sonuç verebilir. Yumuşatma eğrileri, yay modelleri ve gürültü fonksiyonları harekete canlılık katar. Örneğin nefes alma için düşük frekanslı sinüs, robot anteni için Perlin gürültüsü uygulanabilir.

Prosedürel animasyon güçlüdür fakat hata ayıklaması zordur. Hedef noktalarını, ışınları ve eklem sınırlarını sahnede renkli çizgilerle göstermek büyük kolaylık sağlar. En başarılı çözüm genellikle hibrittir: Sanatçının hazırladığı güçlü pozlar temel alınır, matematik ise karakteri dünyaya bağlayan görünmez animatör olur.

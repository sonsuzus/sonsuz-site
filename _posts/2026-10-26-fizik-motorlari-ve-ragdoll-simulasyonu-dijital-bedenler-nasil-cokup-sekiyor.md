---
layout: post
title: "Fizik Motorları ve Ragdoll Simülasyonu: Dijital Bedenler Nasıl Çöküp Sekiyor?"
math: true
categories: 
  - Bilgi
tags: 
  - fizik motoru
  - ragdoll
  - oyun geliştirme
  - unity
  - simülasyon
  - karakter animasyonu
toc: true
image: /img/fizik-motorlari-ve-66.png
---

Bir oyun karakteri merdivenden düştüğünde neden tahta gibi devrilmek yerine kıvrılır, basamaklara çarpar ve sonunda doğal görünen bir pozda durur? Bu küçük dijital dramın arkasında fizik motorları, eklemler, çarpışma şekilleri ve bol miktarda matematik vardır. Ragdoll simülasyonu, önceden hazırlanmış bir animasyonu oynatmak yerine karakter bedenini fizik kurallarına teslim ederek her düşüşü benzersiz hâle getirir.

``

## Fizik motoru neyi hesaplar?

Fizik motoru, sanal dünyadaki nesnelerin kuvvetler karşısında nasıl hareket edeceğini belirleyen sistemdir. Her fizik adımında nesnelerin konumları, hızları ve çarpışmaları yeniden hesaplanır. Temel doğrusal hareket Newton’un ikinci yasasına dayanır:

$$F = m \cdot a$$

Burada $F$ toplam kuvveti, $m$ kütleyi ve $a$ ivmeyi temsil eder. Yerçekimi altında duran bir beden parçasına yaklaşık olarak $F_g = m \cdot g$ kuvveti uygulanır. Motor, bu ivmeyi küçük zaman aralıklarıyla hıza ve konuma dönüştürür:

$$v_{yeni} = v_{eski} + a\Delta t$$

$$x_{yeni} = x_{eski} + v_{yeni}\Delta t$$

$\Delta t$ küçüldükçe simülasyon genellikle daha kararlı olur; ancak işlemci yükü artar. Yani gerçekçilik menüsünde ücretsiz öğle yemeği yoktur.

## Ragdoll bedeninin anatomisi

Ragdoll, tek parça karmaşık bir model olarak değil, birbirine eklemlerle bağlanan katı cisimler olarak ele alınır. Baş, gövde, üst kol, ön kol, uyluk ve baldır gibi parçaların her biri kendi kütlesine ve çarpışma hacmine sahiptir.

| Bileşen | Görevi | Yaygın tercih |
|---|---|---|
| Katı cisim | Kütle, hız ve dönüşü taşır | Rigidbody |
| Çarpıştırıcı | Temas yüzeyini yaklaşıklar | Kapsül, kutu, küre |
| Eklem | Parçaları birbirine bağlar | Configurable Joint |
| Sönümleme | Sonsuz sallanmayı azaltır | Linear/Angular Drag |
| Açı sınırı | Anatomik olmayan dönüşleri engeller | Joint Limits |

Karakterin görsel ağı çok ayrıntılı olabilir; fakat fizik hesaplarında basit kapsüller kullanılır. Çünkü binlerce üçgenle çarpışma aramak yerine birkaç geometrik şekli test etmek çok daha hızlıdır.

## Çökme, çarpışma ve sekme

İki cisim temas ettiğinde fizik motoru iç içe geçmeyi önlemek için bir çarpışma normali belirler ve karşı yönde itki uygular. Sekme miktarı, esneklik katsayısı $e$ ile özetlenebilir:

$$v_{sonra} = -e \cdot v_{önce}$$

$e=0$ olduğunda parça zemine yapışmaya yakın davranır; $e=1$ ise enerjiyi büyük ölçüde koruyarak seker. İnsan bedeni benzeri bir ragdoll için düşük esneklik ve orta-yüksek sürtünme daha inandırıcıdır. Aksi hâlde karakter, trajik bir düşüşten çok lastik top seçmelerine katılmış gibi görünür.

| Ayar | Çok düşükse | Çok yüksekse |
|---|---|---|
| Sürtünme | Beden kayar | Parçalar zemine takılır |
| Esneklik | Darbe cansız görünür | Karakter zıplar |
| Eklem sertliği | Beden pelteleşir | Hareket robotikleşir |
| Sönümleme | Titreme sürer | Hareket aniden ölür |

## Unity’de basit etkinleştirme

Aşağıdaki C# örneği, animasyon sistemini kapatıp çocuk nesnelerdeki fizik bileşenlerini etkinleştirir. Böylece karakter kontrollü animasyondan fizik tabanlı ragdoll durumuna geçer:

```csharp
using UnityEngine;

public class RagdollController : MonoBehaviour
{
    [SerializeField] private Animator animator;
    private Rigidbody[] bodyParts;

    void Awake()
    {
        bodyParts = GetComponentsInChildren<Rigidbody>();
        SetRagdoll(false);
    }

    public void SetRagdoll(bool enabled)
    {
        animator.enabled = !enabled;

        foreach (Rigidbody part in bodyParts)
        {
            part.isKinematic = !enabled;
            part.detectCollisions = enabled;
        }
    }
}
```

`isKinematic` açıkken parçaları fizik değil animasyon yönetir. Ragdoll etkinleştirildiğinde bu özellik kapanır ve yerçekimi, darbeler ile eklem kısıtları kontrolü devralır. Geçiş sırasında karakterin mevcut hızını beden parçalarına aktarmak, özellikle koşarken vurulan karakterlerde sürekliliği güçlendirir.

## Gerçekçilik ile kararlılık arasındaki denge

İyi bir ragdoll yalnızca doğru denklemlerden oluşmaz. Kütle dağılımı, eklem limitleri, sabit fizik zaman adımı ve çözücü yineleme sayısı birlikte ayarlanmalıdır. Gövde genellikle uzuvlardan ağır tutulmalı, komşu parçaların çarpıştırıcıları gereksiz yere birbirine çarpmamalıdır. Ayrıca yüksek hızlarda tünelleme yaşanmaması için sürekli çarpışma algılama kullanılabilir.

Sonuçta gerçekçi çökme hareketi; kuvvetlerin, itkinin, sürtünmenin ve anatomik kısıtların ortak ürünüdür. Başarılı bir ragdoll, oyuncuya matematiği göstermez; yalnızca düşüşün ağırlığını hissettirir.

![fizik-motorlari-ve-66](/img/fizik-motorlari-ve-66.svg)


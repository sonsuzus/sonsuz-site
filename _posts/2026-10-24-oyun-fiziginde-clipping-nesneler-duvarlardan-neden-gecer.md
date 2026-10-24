---
layout: post
title: "Oyun Fiziğinde Clipping: Nesneler Duvarlardan Neden Geçer?"
math: true
categories: 
  - Bilgi
tags: 
  - oyun fiziği
  - clipping
  - çarpışma algılama
  - unity
  - simülasyon
  - kararlılık
toc: true
image: /img/oyun-fiziginde-clipping-42.png
---

Bir merminin duvara çarpması gerekirken öbür tarafta belirmesi, karakterin zemine gömülmesi veya kutuların üst üste binerek titremesi yalnızca görsel birer aksilik değildir. Bu davranışlar, gerçek dünyadaki sürekli hareketin bilgisayarda ayrık zaman adımlarıyla taklit edilmesinden kaynaklanır. Fizik motoru kusursuz bir kâhin değil; nesnelerin geleceğini küçük aralıklarla hesaplayan, bazen de aradaki önemli olayları kaçıran çalışkan bir muhasebecidir.
``

## Simülasyon neden sürekli değildir?

Gerçek dünyada bir nesnenin konumu zamanla kesintisiz değişir. Oyunlarda ise fizik motoru konumu belirli aralıklarla günceller. Basit Euler integrasyonunda yeni konum yaklaşık olarak şöyle hesaplanır:

$$x_{yeni} = x_{eski} + v · Δt$$

Burada $v$ hız, $Δt$ ise fizik adımının süresidir. Hızı 100 m/s olan bir mermi, $Δt = 0.02$ saniyelik adımda tek güncellemede 2 metre ilerler. Duvar yalnızca 20 santimetre kalınlığındaysa mermi bir karede duvarın önünde, sonraki karede arkasında olabilir. Motor sadece iki konumu kontrol ediyorsa çarpışmayı hiç görmez. Bu olaya genellikle **tunneling**, sonucunda oluşan görsel probleme ise **clipping** denir.

| Yaklaşım | Çalışma biçimi | Avantajı | Riski |
|---|---|---|---|
| Ayrık çarpışma | Yalnızca mevcut konumdaki örtüşmeyi test eder | Hızlıdır | Hızlı nesneleri kaçırabilir |
| Sürekli çarpışma | Önceki ve yeni konum arasını tarar | Tunneling azalır | Daha pahalıdır |
| Alt adımlama | Bir fizik adımını küçük parçalara böler | Simülasyonu kararlı kılar | CPU maliyetini artırır |
| Işın veya şekil taraması | Hareket yolu boyunca engel arar | Mermiler için etkilidir | Ek uygulama mantığı ister |

![oyun-fiziginde-clipping-42](/img/oyun-fiziginde-clipping-42.svg)


## Tek suçlu yüksek hız değil

Clipping hatalarının birkaç suç ortağı vardır:

- **Büyük zaman adımı:** $Δt$ büyüdükçe nesnenin tek adımda aldığı mesafe artar.
- **İnce collider:** Duvarın çarpışma hacmi ne kadar inceyse atlanması o kadar kolaydır.
- **Yetersiz çözücü iterasyonu:** Üst üste giren gövdeleri ayıran solver yeterince çalışmazsa nesneler gömülü kalabilir.
- **Doğrudan Transform değiştirmek:** Fizik gövdesini motorun hareket API'si yerine ışınlanmış gibi taşımak, hız ve temas hesaplarını bozar.
- **Kayan nokta hassasiyeti:** Dünya merkezinden çok uzakta küçük konum farkları duyarlılığını kaybeder.
- **Aşırı kütle farkı:** Çok hafif ve çok ağır cisimlerin teması çözücüyü zorlayabilir.

Sayısal kararlılık açısından önemli oran, nesnenin bir adımda aldığı mesafenin engel kalınlığına oranıdır:

$$r = (\vert v\vert  · Δt) / d$$

$d$ engel kalınlığıdır. $r > 1$ olduğunda nesne tek adımda engelin tamamını aşabilir. Bu kesin bir hata garantisi değildir ancak parlak bir alarm lambasıdır.

## Unity ile hareket yolunu taramak

Aşağıdaki örnek, hızlı bir küreyi taşımadan önce gideceği yönde `SphereCast` uygular. Böylece yalnızca hedef konum değil, iki konum arasındaki yol da denetlenir:

```csharp
using UnityEngine;

public class SafeProjectile : MonoBehaviour
{
    public float speed = 80f;
    public float radius = 0.1f;

    void FixedUpdate()
    {
        Vector3 direction = transform.forward;
        float distance = speed * Time.fixedDeltaTime;

        if (Physics.SphereCast(transform.position, radius, direction,
                               out RaycastHit hit, distance))
        {
            transform.position = hit.point - direction * radius;
            Debug.Log("Çarpılan nesne: " + hit.collider.name);
            Destroy(gameObject);
            return;
        }

        transform.position += direction * distance;
    }
}
```

`Raycast` yerine `SphereCast` kullanılması, hacmi olan merminin kenardan temaslarını daha güvenilir yakalar. Fizik tabanlı bir gövde kullanılıyorsa doğrudan `Transform` taşımak yerine `Rigidbody.MovePosition`, hız veya kuvvet yöntemleri tercih edilmelidir. Motorun sunduğu **Continuous Dynamic** gibi sürekli çarpışma seçenekleri de hızlı gövdelerde etkinleştirilebilir.

## Dengeli çözüm nasıl seçilir?

Her nesneye en pahalı çarpışma modunu vermek doğru değildir. Yavaş dekor kutularında ayrık algılama yeterliyken mermiler, hızlı araçlar ve oyuncu karakterleri daha dikkatli ele alınmalıdır. Sabit fizik adımını küçültmek doğruluğu artırır fakat saniyedeki hesap sayısını yükseltir. Bu nedenle kritik nesnelerde sürekli algılama, çok hızlı mühimmatta şekil taraması ve büyük dünyalarda kayan başlangıç noktası yaklaşımı kullanılabilir.

Kısacası clipping, fizik motorunun “duvarları sevmemesi” değil, zaman ve konumu örnekleme biçiminin doğal sonucudur. Hız, zaman adımı, collider kalınlığı ve çözücü ayarları birlikte değerlendirildiğinde hayalet mermiler azalır; duvarlar da yeniden duvar gibi davranmaya başlar.

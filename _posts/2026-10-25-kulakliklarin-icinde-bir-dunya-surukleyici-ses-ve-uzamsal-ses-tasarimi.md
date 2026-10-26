---
layout: post
title: "Kulaklıkların İçinde Bir Dünya: Sürükleyici Ses ve Uzamsal Ses Tasarımı"
math: true
categories: 
  - Bilgi
tags: 
  - uzamsal ses
  - 3d ses
  - oyun geliştirme
  - ses tasarımı
  - hrtf
  - ambisonics
toc: true
image: /img/kulakliklarin-icinde-bir-15.png
---

![kulakliklarin-icinde-bir-15](/img/kulakliklarin-icinde-bir-15.svg)


Bir korku oyununda arkanızdan gelen ayak sesini duyduğunuzda neden istemsizce dönersiniz? Çünkü beyniniz sesi yalnızca işitmez; onun yönünü, uzaklığını ve bulunduğu ortamı da tahmin eder. Sürükleyici ses tasarımı, bu doğal konumlandırma mekanizmasını taklit ederek oyuncunun sanal dünyayı gerçek bir mekân gibi algılamasını sağlar.

``

## Uzamsal ses nedir?

Geleneksel stereo sistemlerde ses, sol ve sağ kanal arasında dağıtılır. Uzamsal ses ise bir kaynağı üç boyutlu koordinatlarla tanımlar. Böylece oyuncu sesin sağda veya solda olmasının yanı sıra yukarıda, aşağıda, önde ya da arkada bulunduğunu da hissedebilir.

Beyin bu konumu belirlerken iki temel ipucundan yararlanır:

- **Kulaklar arası zaman farkı (ITD):** Ses, yakın kulağa biraz daha erken ulaşır.
- **Kulaklar arası seviye farkı (ILD):** Başımız bir engel oluşturduğu için uzak kulağa ulaşan ses daha zayıftır.

Basitleştirilmiş zaman farkı şöyle ifade edilebilir:

$$\Delta t = \frac{d \sin(\theta)}{c}$$

Burada $d$ kulaklar arasındaki mesafe, $\theta$ sesin geliş açısı ve $c$ ses hızıdır. Fark mikro saniyeler düzeyinde olsa bile beynimiz bunu şaşırtıcı bir hassasiyetle yorumlar.

## HRTF: Kulakların kişisel ses filtresi

**Head-Related Transfer Function (HRTF)**, sesin baş, omuz ve kulak kepçesiyle etkileşime girdikten sonra kulağa nasıl ulaştığını matematiksel olarak modeller. Özellikle dikey konum ve ön-arka ayrımı için önemlidir. Kulaklıkla çalışan binaural sistemler, kaynak sesi sağ ve sol kulağa farklı HRTF filtreleri uygulayarak işler.

| Teknoloji | Temel yaklaşım | Güçlü yanı | Yaygın kullanım |
|---|---|---|---|
| Stereo | İki sabit kanal | Basit ve ucuz | Müzik, arayüz sesleri |
| Surround | Çevrede fiziksel kanallar | Odayı kapsayan yön hissi | Sinema, ev sistemleri |
| Binaural/HRTF | Kulakların duyumunu taklit eder | Kulaklıkta güçlü 3D algı | VR ve oyunlar |
| Ambisonics | Ses alanını küresel olarak kaydeder | Dinleyici döndükçe uyarlanabilir | 360° video, VR |
| Nesne tabanlı ses | Her kaynak bağımsız bir nesnedir | Dinamik ve esnek konumlandırma | Modern oyun motorları |

## Uzaklık yalnızca sesi kısmak değildir

Gerçek dünyada uzaklaşan ses hem zayıflar hem de frekans karakterini değiştirir. Basit bir modelde ses şiddeti, mesafenin karesiyle ters orantılıdır:

$$I(r) = \frac{P}{4\pi r^2}$$

Ancak oyunlarda bu fiziksel model doğrudan kullanılırsa ses çok hızlı kaybolabilir. Bu nedenle tasarımcılar logaritmik veya özel zayıflama eğrileri kullanır. Duvarların yüksek frekansları süzmesi, kapı aralığından geçen sesin yön değiştirmesi ve büyük salonlarda yankının uzaması da mekân algısını kuvvetlendirir.

## Oyun motorunda temel uygulama

Aşağıdaki Unity C# örneği, bir ses kaynağının dinleyiciye göre uzaklığını ölçerek alçak geçiren filtreyi kontrol eder. Amaç, uzaktaki seslerin daha boğuk duyulmasını sağlamaktır:

```csharp
using UnityEngine;

public class DistanceAudioFilter : MonoBehaviour
{
    public Transform listener;
    public AudioLowPassFilter lowPass;
    public float nearFrequency = 22000f;
    public float farFrequency = 2500f;
    public float maxDistance = 30f;

    void Update()
    {
        float distance = Vector3.Distance(transform.position, listener.position);
        float ratio = Mathf.Clamp01(distance / maxDistance);
        lowPass.cutoffFrequency = Mathf.Lerp(nearFrequency, farFrequency, ratio);
    }
}
```

Bu yaklaşım tek başına fiziksel bir simülasyon değildir; fakat görsel mesafe ile işitsel mesafeyi tutarlı hâle getirir. Daha gelişmiş sistemlerde ışın izleme tabanlı ses yayılımı, yüzey malzemeleri ve gerçek zamanlı yankı hesaplamaları kullanılabilir.

## Tasarım teknolojiden önce gelir

Her sesi üç boyutlu yapmak iyi bir fikir değildir. Arayüz bildirimleri ve müzik gibi öğeler sabit kalırken düşmanlar, mermiler ve çevresel ipuçları uzamsallaştırılabilir. Rekabetçi oyunlarda ses yönü oynanışı destekler; korku oyunlarında ise görünmeyen bir tehdidi oyuncunun zihninde canlandırır.

Başarılı sürükleyici ses, “Bak, burada 3D teknoloji var!” diye bağırmaz. Oyuncuya bulunduğu mekânın boyutunu, tehlikenin yönünü ve yüzeylerin karakterini fark ettirmeden anlatır. Görüntü dünyayı gösterirken uzamsal ses, oyuncuyu o dünyanın gerçekten içine yerleştirir.

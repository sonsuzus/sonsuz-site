---
layout: post
title: "Işın İzleme: Piksellerin Arkasındaki Optik Fizik ve Algoritmalar"
math: true
categories: 
  - Bilgi
tags: 
  - ray tracing
  - bilgisayar grafikleri
  - optik fizik
toc: true
---

Bir ekrandaki parlak metal, saydam cam veya yumuşak gölge yalnızca estetik bir hile değildir. Işın izleme, ışığın gerçek dünyadaki davranışını matematiksel bir modele dönüştürerek her pikselin rengini hesaplar. İşin eğlenceli tarafı şudur: Algoritma, doğadaki sayısız fotonu ileri doğru takip etmek yerine kameradan sahneye ters yönde ışın göndererek yalnızca görüntüye katkı sağlayan yolları araştırır.

``

## Işığı neden geriye doğru izliyoruz?

Bir ampul gerçekte her yöne olağanüstü miktarda foton yollar; bunların yalnızca çok küçük bir bölümü kameraya ulaşır. Tüm fotonları simüle etmek hesaplama açısından pahalıdır. Bu nedenle klasik **backward ray tracing**, kamera merkezinden görüntü düzlemindeki her piksele birincil ışın gönderir.

Bir ışının parametrik denklemi şöyledir:

$$P(t) = O + tD, \qquad t \ge 0$$

Burada $O$ ışının başlangıcı, $D$ normalize edilmiş yönü, $t$ ise ışın üzerindeki ilerleme miktarıdır. Algoritma, bu doğrunun sahnedeki üçgen, küre veya başka geometrilerle kesişip kesişmediğini araştırır. En küçük pozitif $t$ değeri, kameraya en yakın görünür yüzeyi verir.

| Yaklaşım | İzlenen yol | Avantaj | Dezavantaj |
|---|---|---|---|
| Rasterizasyon | Üçgenden piksele | Çok hızlıdır | Yansıma ve gölgeler ek teknik ister |
| Geriye ışın izleme | Kameradan sahneye | Görünür yolları verimli bulur | Çok sayıda kesişim testi yapar |
| Path tracing | Rastgele çoklu sekmeler | Gerçekçi küresel aydınlatma üretir | Gürültülü sonuç için çok örnek gerekir |

## Yüzeyle karşılaşınca ne olur?

Bir ışın yüzeye çarptığında renk yalnızca cismin kaplama renginden gelmez. Işık; soğurulabilir, yansıyabilir veya kırılarak ortam değiştirebilir. Basit Phong aydınlatma modeli bu katkıları ortam, dağınık ve parlak bileşenlere ayırır:

$$I = I_a k_a + I_l k_d\max(0, N \cdot L) + I_l k_s\max(0, R \cdot V)^n$$

$N$ yüzey normali, $L$ ışık yönü, $V$ kamera yönü ve $R$ yansıma yönüdür. $N \cdot L$ değeri, ışığın yüzeye ne kadar dik geldiğini ölçer. Işık yüzeye paralelleştikçe enerji daha geniş alana yayıldığından parlaklık azalır.

Kusursuz aynadaki yansıma yönü şu formülle bulunur:

$$R = D - 2(D \cdot N)N$$

Saydam malzemelerde ise Snell yasası devreye girer:

$$n_1\sin(\theta_1) = n_2\sin(\theta_2)$$

Kırılma indisleri arasındaki fark büyüdükçe ışının yön değişimi de belirginleşir. Kritik açı aşılırsa ışık dışarı çıkamaz ve **tam iç yansıma** oluşur.

## Temel algoritma

Aşağıdaki sözde kod, bir ışının en yakın yüzeyle etkileşimini ve gölge kontrolünü gösterir:

```python
def trace(ray, depth):
    if depth <= 0:
        return background

    hit = scene.closest_intersection(ray)
    if hit is None:
        return background

    color = hit.material.ambient

    for light in lights:
        to_light = normalize(light.position - hit.point)
        shadow_ray = Ray(hit.point + hit.normal * EPSILON, to_light)

        if not scene.is_occluded(shadow_ray, light):
            diffuse = max(0, dot(hit.normal, to_light))
            color += hit.material.diffuse * light.color * diffuse

    reflected = reflect(ray.direction, hit.normal)
    color += hit.material.reflectivity * trace(
        Ray(hit.point + hit.normal * EPSILON, reflected), depth - 1
    )
    return color
```

`EPSILON`, yeni ışının aynı yüzeye tekrar çarpmasını önleyerek gölge aknesi denen sayısal hatayı azaltır. `depth` ise aynaların birbirini sonsuza kadar yansıtmasına karşı özyinelemeyi sınırlar.

## Gerçekçilik neden pahalıdır?

Her piksel için birden fazla ışın, her yansıma için yeni ışınlar ve her ışık kaynağı için gölge testi gerekir. $W \times H$ çözünürlükte, piksel başına $S$ örnek kullanıldığında başlangıç maliyeti yaklaşık $WHS$ ışındır. Bu yüzden BVH gibi uzamsal hızlandırma yapıları, tüm nesneleri tek tek denemek yerine olası kesişmeleri daraltır.

Path tracing bu yapıyı rastgele örnekleme, enerji korunumu ve Monte Carlo integrasyonu ile genişletir. Az örnek gürültü üretirken çok örnek daha temiz fakat daha yavaş sonuç verir. Kısacası her göz alıcı pikselin arkasında optik, olasılık, geometri ve sabırlı bir işlemci birlikte çalışır.

---
layout: post
title: "Oyunlarda Işık ve Gölgeleme: Ray Tracing mi, Önceden Hesaplanmış Aydınlatma mı?"
math: true
categories: 
  - Bilgi
tags: 
  - oyun geliştirme
  - ray tracing
  - ışıklandırma
  - gölgeleme
  - grafik programlama
  - render
toc: true
image: /img/oyunlarda-isik-ve-37.png
---

Bir oyun sahnesindeki ışık, yalnızca çevreyi görünür hâle getirmez; atmosferi, derinlik algısını ve oyuncunun dikkatini de yönetir. Karanlık bir koridordaki titrek lamba gerilim yaratırken gün batımının yumuşak gölgeleri huzur verebilir. Bu görüntüler üretilirken geliştiricilerin karşısına iki temel yaklaşım çıkar: ışığı çalışma anında fiziksel olarak simüle eden gerçek zamanlı ışın izleme ve aydınlatma sonuçlarını önceden hesaplayıp saklayan baked lighting.
``

## Işığın arkasındaki temel matematik

Bilgisayar grafiklerinde bir yüzeyin görünen rengi; ışık kaynağına, yüzey malzemesine ve kameraya bağlıdır. Basit Lambert aydınlatmasında dağınık ışık şu şekilde ifade edilir:

$$I_d = k_d I_l \max(0, \vec{N} \cdot \vec{L})$$

Burada $I_l$ ışık şiddetini, $k_d$ malzemenin ışığı yansıtma oranını, $\vec{N}$ yüzey normalini ve $\vec{L}$ ışığın yönünü temsil eder. Normal ile ışık yönü birbirine yaklaştıkça yüzey daha parlak görünür.

Gerçekçi sahnelerde ışık yalnızca kaynaktan yüzeye gelmez. Duvarlardan sekebilir, parlak yüzeylerde yansıyabilir ve saydam nesnelerden kırılarak geçebilir. Render denklemi bu davranışı genel biçimde açıklar:

$$L_o = L_e + \int_{\Omega} f_r L_i (\vec{N} \cdot \vec{L})\,d\omega$$

Bu integralin eksiksiz hesaplanması pahalıdır. Oyun motorları bu nedenle hız ile doğruluk arasında çeşitli numaralar yapar; grafik programlamanın sihri biraz da buradadır.

## Gerçek zamanlı ray tracing

Ray tracing, kameradan sahneye ışınlar göndererek bu ışınların hangi üçgenlerle kesiştiğini araştırır. Çarpışma noktasından gölge, yansıma veya dolaylı aydınlatma için yeni ışınlar üretilebilir. Böylece ekran alanının dışında kalan nesneler bile yansımalarda görülebilir.

Bir ışının parametrik gösterimi şöyledir:

$$P(t) = O + tD$$

$O$ başlangıç noktası, $D$ yön ve $t$ ilerleme mesafesidir. Modern ekran kartlarındaki özel çekirdekler ve BVH gibi hızlandırma yapıları, milyonlarca üçgen arasındaki kesişme aramasını yönetir.

Aşağıdaki sade HLSL örneği, gölge ışını sonucuna göre görünürlüğü belirler:

```hlsl
float visibility = 1.0;
RayDesc shadowRay;
shadowRay.Origin = hitPosition + normal * 0.001;
shadowRay.Direction = lightDirection;
shadowRay.TMin = 0.0;
shadowRay.TMax = distanceToLight;

TraceRay(scene, RAY_FLAG_ACCEPT_FIRST_HIT_AND_END_SEARCH,
         0xFF, 0, 0, 0, shadowRay, visibility);
```

Buradaki küçük normal ofseti, ışının çıktığı yüzeye tekrar çarpmasını önler. İlk engelde aramayı durdurmak da gölge hesabını hızlandırır.

## Önceden hesaplanmış aydınlatma

Baked lighting yönteminde doğrudan ve dolaylı ışık, oyun yayınlanmadan önce hesaplanır. Sonuçlar lightmap adı verilen dokulara veya light probe verilerine kaydedilir. Çalışma sırasında ağır ışık simülasyonu yerine bu veriler okunur.

Bu yaklaşım özellikle duvarların, zeminin ve ışıkların hareket etmediği sahnelerde son derece verimlidir. Ancak bir oyuncu lambayı devirdiğinde lightmap bunu umursamaz; gölge hâlâ eski yerde kalabilir. Dinamik nesneler için probe, shadow map veya ekran alanı teknikleriyle destek gerekir.

| Özellik | Gerçek zamanlı ray tracing | Önceden hesaplanmış ışık |
|---|---|---|
| Hesaplama zamanı | Oyun çalışırken | Geliştirme aşamasında |
| Dinamik sahneler | Çok başarılı | Sınırlı |
| Donanım maliyeti | Yüksek | Düşük |
| Yansıma doğruluğu | Fiziksel olarak daha tutarlı | Genellikle yaklaşık |
| Bellek ihtiyacı | Hızlandırma yapıları | Lightmap dokuları |
| Düzenleme süreci | Anlık geri bildirim | Yeniden bake gerekebilir |

## Hangisini seçmeli?

Hareketli ışıkların, aynaların ve yıkılabilir çevrenin öne çıktığı bir oyunda ray tracing güçlü bir seçenektir. Mobil oyunlarda, düşük sistem gereksinimi hedeflerinde veya büyük ölçüde sabit mekânlarda baked lighting daha mantıklıdır.

Pratikte kazanan çoğunlukla hibrit yaklaşımdır. Statik ortamın dolaylı ışığı lightmap ile saklanırken karakter gölgeleri shadow map, parlak yansımalar ise ray tracing ile üretilebilir. Gürültülü ışın izleme sonuçları temporal accumulation ve denoiser filtreleriyle temizlenir. Böylece kalite bütçesi gerçekten görünür alanlara harcanır; ekran kartı da küçük bir güneşi simüle etmeye çalışırken tamamen ter içinde kalmaz.

![oyunlarda-isik-ve-37](/img/oyunlarda-isik-ve-37.svg)


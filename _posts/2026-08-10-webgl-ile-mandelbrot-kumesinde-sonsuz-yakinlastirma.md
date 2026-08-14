---
layout: post
title: "WebGL ile Mandelbrot Kümesinde Sonsuz Yakınlaştırma"
math: true
categories: 
  - Proje
tags: 
  - WebGL
  - GLSL
  - Fraktal
  - JavaScript
  - Shader
---

Mandelbrot kümesi, basit bir denklemin ekranda bitmek bilmeyen kıvrımlar, spiraller ve minyatür evrenler üretmesinin en güzel kanıtıdır. Bu projede hesaplamayı JavaScript işlemcisine bırakmak yerine WebGL ve GLSL gölgelendiricilerine taşıyarak akıcı bir sonsuz yakınlaştırma deneyimi kuracağız. Fare tekerleğiyle yaklaşacak, sürükleyerek gezecek ve her pikselin kendi matematik macerasını ekran kartında yaşamasını sağlayacağız.

``

## Mandelbrot’un matematik motoru

Kümenin temeli şu yinelemeli fonksiyondur:

$$z_{n+1}=z_n^2+c$$

Burada başlangıç değeri $z_0=0$ seçilir; $c$, karmaşık düzlemdeki her pikselin karşılığıdır. Bir nokta için değerler sınırsız büyümezse nokta Mandelbrot kümesine dahildir. Pratikte sonsuz adım atamayacağımız için bir **iterasyon sınırı** koyarız. Eğer herhangi bir adımda $ \vert z \vert >2$ olursa kaçış garanti edilir. Hesaplama maliyetini azaltmak için karekök yerine şu kontrol yapılır:

$$ \vert z \vert ^2=x^2+y^2>4$$

| Kavram | Matematikteki rolü | Uygulamadaki karşılığı |
|---|---|---|
| $c$ | İncelenen karmaşık sayı | Pikselin düzlem koordinatı |
| $z$ | Her turdaki ara değer | Shader içindeki `vec2` |
| İterasyon | Yaklaşık üyelik testi | Renk ayrıntısı ve performans |
| Zoom | Daha küçük alanı inceleme | `scale` değerinin azalması |

## Neden WebGL?

Canvas 2D ile her pikseli JavaScript döngüsünde hesaplamak, yüksek çözünürlükte hızla yorucu olur. Fragment shader ise ekranın her pikselini paralel biçimde işler. Böylece aynı formül binlerce çekirdekte eşzamanlı değerlendirilir. JavaScript’in görevi yalnızca kamera durumunu, çözünürlüğü ve iterasyon sayısını shader’a `uniform` olarak göndermektir.

| Yaklaşım | Güçlü yanı | Sınırı |
|---|---|---|
| Canvas 2D + JavaScript | Öğrenmesi kolay | Piksel döngüleri yavaştır |
| WebGL + fragment shader | Paralel ve akıcıdır | GLSL hata ayıklaması daha zordur |
| WebGPU | Modern hesaplama imkânları | Tarayıcı desteği ve kurulum değişken |

Önce ekranı kaplayan iki üçgenden oluşan basit bir quad çizin. Ardından fragment shader’da UV koordinatlarını karmaşık düzleme dönüştürün. `uCenter` gezinti merkezini, `uScale` görünür alan genişliğini temsil eder:

```glsl
precision highp float;
uniform vec2 uResolution;
uniform vec2 uCenter;
uniform float uScale;
uniform int uMaxIter;

void main() {
  vec2 uv = (gl_FragCoord.xy / uResolution - 0.5) * 2.0;
  uv.x *= uResolution.x / uResolution.y;
  vec2 c = uCenter + uv * uScale;
  vec2 z = vec2(0.0);
  int i;

  for (i = 0; i < 1000; i++) {
    if (i >= uMaxIter || dot(z, z) > 4.0) break;
    z = vec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + c;
  }

  float t = float(i) / float(uMaxIter);
  vec3 color = vec3(t, t*t, 0.5 + 0.5*sin(8.0*t));
  gl_FragColor = vec4(i == uMaxIter ? vec3(0.0) : color, 1.0);
}
```

Bu kodda `dot(z, z)`, karmaşık sayının büyüklük karesini verir. Kaçan noktalar iterasyon sayısına göre renklendirilir; kümenin içi ise siyah kalır. Daha yumuşak şeritler için düz iterasyon rengi yerine kaçış anını kesirli hesaplayan smooth coloring uygulanabilir.

## Kamera ve etkileşim

Fare tekerleğinde yakınlaştırma çarpanını değiştirin: `scale *= 0.85` yaklaşır, `scale /= 0.85` uzaklaşır. Kritik ayrıntı, imlecin altındaki dünya koordinatını zoom öncesi ve sonrası hesaplayıp merkezi buna göre kaydırmaktır; aksi halde görüntü ekran merkezine doğru zıplar. Sürükleme sırasında piksel hareketini ölçek ve en-boy oranıyla çarparak `uCenter` değerinden çıkarın.

Yakınlaştıkça sınır detayları karmaşıklaşacağından `uMaxIter` değerini artırın. Ancak standart `float` hassasiyeti çok derin zoom seviyelerinde bozulur. İlk sürüm için $10^{-8}$ civarı yakınlaştırma yeterince etkileyicidir; daha derin keşif için çift hassasiyet emülasyonu veya perturbation algoritmaları sonraki maceranız olabilir.

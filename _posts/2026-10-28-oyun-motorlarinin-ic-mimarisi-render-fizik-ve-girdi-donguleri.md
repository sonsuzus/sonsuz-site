---
layout: post
title: "Oyun Motorlarının İç Mimarisi: Render, Fizik ve Girdi Döngüleri"
math: true
categories: 
  - Bilgi
tags: 
  - oyun motoru
  - unity
  - unreal engine
  - render
  - fizik motoru
  - game loop
toc: true
image: /img/oyun-motorlarinin-ic-45.png
---

Bir oyun motoru, ekrandaki karakterleri hareket ettiren basit bir programdan çok daha fazlasıdır. Unity ve Unreal Engine gibi motorlar; oyuncu girdilerini okumak, fizik kurallarını hesaplamak, yapay zekâyı güncellemek ve görüntüyü çizmek gibi görevleri son derece düzenli döngüler içinde yürütür. Perde arkasında çalışan bu mimariyi anlamak, hem performans sorunlarını çözmeyi hem de daha kararlı oyun sistemleri geliştirmeyi kolaylaştırır.

``

## Her Şeyin Kalbi: Oyun Döngüsü

Oyun motorlarının merkezinde **game loop**, yani oyun döngüsü bulunur. Motor çalıştığı sürece bu döngü girdiyi okur, oyun dünyasını günceller ve yeni kareyi ekrana gönderir.

Basitleştirilmiş akış şöyledir:

```text
while oyun_calışıyor:
    girdileri_oku()
    fiziği_hesapla()
    oyun_mantığını_güncelle()
    sahneyi_render_et()
```

Bir karenin işlenme süresi ile saniyedeki kare sayısı arasındaki ilişki şu formülle gösterilebilir:

$$FPS = \frac{1}{\Delta t}$$

Örneğin bir kare $0.0166$ saniyede hazırlanıyorsa oyun yaklaşık $60$ FPS üretir. Ancak bütün sistemleri değişken $\Delta t$ ile güncellemek doğru değildir. Render döngüsü ekran hızına göre değişebilirken fizik hesaplamaları çoğunlukla sabit zaman aralıklarında çalıştırılır.

## Render Döngüsü Nasıl Çalışır?

Render sistemi, oyun dünyasındaki nesneleri GPU’nun anlayabileceği komutlara dönüştürür. Kamera dışında kalan nesneler ayıklanır, görünür yüzeyler belirlenir, materyaller hazırlanır ve çizim komutları GPU’ya gönderilir.

| Aşama | Görevi | Olası Darboğaz |
|---|---|---|
| Culling | Görünmeyen nesneleri eler | CPU hesaplaması |
| Geometry | Üçgenleri işler | Yüksek poligon sayısı |
| Shading | Işık ve materyalleri hesaplar | Karmaşık shader’lar |
| Post-processing | Bloom, renk ve efekt uygular | GPU bant genişliği |

Unity; Built-in, URP ve HDRP gibi farklı render yaklaşımları sunar. Unreal Engine ise deferred rendering, Nanite ve Lumen gibi sistemlerle yüksek detaylı sahneleri yönetir. Her iki motorda da amaç aynıdır: Görsel kaliteyi korurken kare süresini bütçe içinde tutmak. 60 FPS hedefinde bu bütçe yaklaşık $16.67$ milisaniyedir.

## Fizik Neden Sabit Döngü Kullanır?

Fizik motorları çarpışma, hız, ivme ve kuvvet hesaplarını mümkün olduğunca tutarlı gerçekleştirmelidir. Temel hareket denklemlerinden biri şöyledir:

$$x_{yeni} = x_{eski} + v\Delta t$$

$\Delta t$ sürekli değişirse aynı kuvvet farklı bilgisayarlarda farklı sonuçlar üretebilir. Unity bu nedenle fizik işlemlerini ağırlıklı olarak `FixedUpdate` düzeninde yürütür. Unreal Engine tarafında fizik güncellemeleri tick grupları ve alt adımlar aracılığıyla kontrol edilebilir.

| Döngü | Zamanlama | Uygun Kullanım |
|---|---|---|
| Değişken güncelleme | Her render karesinde | Kamera, arayüz, görsel animasyon |
| Sabit güncelleme | Belirli aralıklarla | Fizik, kuvvet ve çarpışma |
| Geç güncelleme | Ana güncellemeden sonra | Takip kamerası, son konum düzeltmeleri |

## Girdi Sistemi ve Gecikme

Klavye, fare veya kontrolcü verileri işletim sisteminden alınır ve motorun girdi katmanına aktarılır. Girdi mümkün olduğunca erken okunursa oyuncunun yaptığı hareket ile ekrandaki sonuç arasındaki gecikme azalır.

```csharp
void Update()
{
    float yatay = Input.GetAxis("Horizontal");
    hareketYonü = new Vector3(yatay, 0f, 0f);
}

void FixedUpdate()
{
    govde.AddForce(hareketYonü * kuvvet);
}
```

Bu Unity örneğinde girdi her karede okunur; fiziksel kuvvet ise sabit döngüde uygulanır. Böylece kısa süreli tuş hareketleri kaçırılmaz ve fizik davranışı kare hızından daha az etkilenir. Modern Unity Input System ve Unreal Enhanced Input, girdileri eylem tabanlı tanımlayarak farklı cihazları ortak bir soyutlama altında toplar.

## İş Parçacıkları ve Senkronizasyon

Güncel motorlar tüm işleri tek çekirdekte yürütmez. Render hazırlığı, animasyon, ses ve fizik görevleri iş parçacıklarına dağıtılabilir. Unity Job System ve Unreal Task Graph bu yaklaşımın örnekleridir. Yine de render, fizik ve oyun mantığı birbirinin verisine ihtiyaç duyduğundan senkronizasyon noktaları oluşur. Bir görev geciktiğinde diğer sistemler bekleyebilir.

Sonuç olarak oyun motoru, farklı hızlarda çalışan orkestraya benzer. Girdi sistemi notaları toplar, fizik ritmi korur, render sistemi ise performansı seyirciye sunar. Başarılı bir oyun mimarisi, bu döngülerin doğru sırada ve mümkün olduğunca az bekleyerek çalışmasını sağlar.

![oyun-motorlarinin-ic-45](/img/oyun-motorlarinin-ic-45.svg)


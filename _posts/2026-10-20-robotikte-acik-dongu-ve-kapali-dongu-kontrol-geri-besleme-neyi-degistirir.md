---
layout: post
title: "Robotikte Açık Döngü ve Kapalı Döngü Kontrol: Geri Besleme Neyi Değiştirir?"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - kontrol-sistemleri
  - geri-besleme
  - açık-döngü
  - kapalı-döngü
  - python
toc: true
image: /img/robotikte-acik-dongu-55.png
---

Bir robota “motoru iki saniye çalıştır” demek ile “hedef konuma ulaşana kadar motoru çalıştır” demek aynı şey değildir. İlk komutta robot yalnızca verilen talimatı uygular; ikinci komutta ise bulunduğu konumu ölçerek davranışını sürekli düzeltir. Açık döngü ve kapalı döngü kontrol arasındaki temel ayrım, sistemin kendi sonucundan haberdar olup olmamasıdır.


![robotikte-acik-dongu-55](/img/robotikte-acik-dongu-55.svg)

``

## Açık döngü kontrol nedir?

Açık döngü kontrol sisteminde denetleyici, ürettiği komutun sonucunu ölçmez. Giriş belirlenir, eyleyici çalışır ve bir çıktı oluşur. Ancak çıktı yanlış olsa bile sistem bunu fark edemez.

Basit bir hareket komutu şöyle düşünülebilir:

$$u(t) \rightarrow \text{Motor} \rightarrow y(t)$$

Burada $u(t)$ motora gönderilen kontrol sinyali, $y(t)$ ise robotun gerçek hareketidir. $y(t)$ değerini denetleyiciye geri taşıyan bir bağlantı bulunmaz.

Örneğin çizgi izleyen bir robot yerine, tekerleklerini önceden hesaplanan süre boyunca döndüren bir araç düşünelim. Motorların 100 devir yapmasının aracı bir metre ilerleteceğini varsayabiliriz. Fakat zemin kaygansa, pil zayıfsa veya tekerleklerden biri sıkıştıysa gerçek mesafe değişir. Robot yine de görevini başarıyla tamamladığını “zanneder”. Bir bakıma gözleri kapalı yürür.

Açık döngü yaklaşımı; basit, ucuz ve hızlıdır. Sensör ya da karmaşık hesaplama gerektirmediği için zaman kontrollü sulama sistemleri, basit taşıma bantları ve bazı oyuncak robotlarda kullanılabilir.

## Kapalı döngü kontrol nedir?

Kapalı döngü sistem, çıktıyı sensörlerle ölçerek hedef değerle karşılaştırır. Aradaki fark **hata** olarak adlandırılır:

$$e(t) = r(t) - y(t)$$

Burada $r(t)$ hedef değer, $y(t)$ ölçülen gerçek değer ve $e(t)$ kontrol hatasıdır. Denetleyici bu hatayı kullanarak yeni bir kontrol sinyali üretir:

$$u(t) = K_p e(t)$$

Bu ifade basit bir oransal denetleyiciyi gösterir. $K_p$ kazancı büyüdükçe robot hataya daha sert tepki verir. Ancak aşırı büyük değerler robotun hedef çevresinde titreşmesine neden olabilir. Yani robot, “Biraz geçtim, geri döneyim; şimdi de fazla geri geldim!” döngüsüne girebilir.

Kapalı döngüde bilgi akışı şöyledir:

$$r(t) \rightarrow \text{Denetleyici} \rightarrow \text{Robot} \rightarrow y(t) \rightarrow \text{Sensör}$$

Sensörden gelen ölçüm tekrar denetleyiciye ulaştığı için çevrim kapanır. Enkoder, kamera, jiroskop, ivmeölçer ve mesafe sensörü gibi bileşenler geri besleme kaynağı olabilir.

## İki yaklaşımın karşılaştırması

| Özellik | Açık döngü | Kapalı döngü |
|---|---|---|
| Geri besleme | Yoktur | Vardır |
| Sensör gereksinimi | Genellikle yok | Genellikle var |
| Hata düzeltme | Yapamaz | Otomatik yapabilir |
| Maliyet | Daha düşük | Daha yüksek |
| Tasarım | Basit | Daha karmaşık |
| Bozucu etkilere dayanım | Zayıf | Daha güçlü |
| Robotik örnek | Süreye göre motor sürme | Enkoderle konum kontrolü |

## Küçük bir Python örneği

Aşağıdaki kod, hedefi 100 birim olan basit bir kapalı döngü konum kontrolünü simüle eder:

```python
hedef = 100.0
konum = 0.0
Kp = 0.2

for adim in range(20):
    hata = hedef - konum
    motor_komutu = Kp * hata
    konum += motor_komutu

    print(
        f"Adım: {adim:2d} | "
        f"Hata: {hata:6.2f} | "
        f"Konum: {konum:6.2f}"
    )
```

Kod her adımda hedef ile mevcut konum arasındaki farkı hesaplar. Robot hedefe yaklaştıkça hata ve motor komutu küçülür. Açık döngü sürümünde ise hata hesaplanmadan motora sabit bir komut gönderilirdi; oluşan konum sapması bilinmezdi.

## Hangisi seçilmeli?

Görev tekrarlanabilir, çevre sabit ve küçük hatalar önemsizse açık döngü yeterli olabilir. Hassas konumlandırma, değişken yük, güvenlik veya çevresel belirsizlik söz konusuysa kapalı döngü daha uygundur. Endüstriyel robot kollarının, dronların ve otonom araçların geri besleme kullanması tesadüf değildir.

Özetle açık döngü sistem komut verir ve sonucuna bakmaz; kapalı döngü sistem ise ölçer, karşılaştırır ve düzeltir. Robotikte geri besleme, makineye yalnızca hareket etme değil, hatasını fark ederek daha doğru hareket etme yeteneği kazandırır.

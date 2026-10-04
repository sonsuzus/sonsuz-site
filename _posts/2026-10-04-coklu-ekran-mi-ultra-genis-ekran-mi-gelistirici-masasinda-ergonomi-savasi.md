---
layout: post
title: "Çoklu Ekran mı Ultra Geniş Ekran mı? Geliştirici Masasında Ergonomi Savaşı"
math: true
categories: 
  - Bilgi
tags: 
  - ergonomi
  - verimlilik
  - pencere yönetimi
  - ultra geniş ekran
  - çoklu monitör
  - yazılım geliştirme
toc: true
image: /img/coklu-ekran-mi-29.png
---

Bir tarafta kod editörü, diğer tarafta dokümantasyon, köşede terminal ve sürekli dikkat isteyen Slack… Geliştirici masasının ekran ihtiyacı bazen küçük bir hava trafik kontrol merkezini andırır. Peki uygulamaları farklı fiziksel ekranlara dağıtmak mı, yoksa tek bir ultra geniş ekranı sanal bölgelere ayırmak mı konsantrasyon açısından daha verimlidir? Yanıt yalnızca piksel sayısında değil; göz hareketlerinde, boyun açısında ve zihinsel bağlam değişimlerinde saklıdır.

``

## Piksel sayısı her şeyi anlatmaz

İki adet 27 inç QHD monitör, toplamda $2 \times 2560 \times 1440 = 7.372.800$ piksel sunar. 3440×1440 çözünürlüklü bir ultra geniş ekran ise $4.953.600$ piksele sahiptir. Çoklu ekran kâğıt üzerinde daha geniş bir çalışma alanı sağlar; ancak çerçeveler, farklı renk profilleri ve fiziksel yerleşim bu alanın kesintisiz kullanılmasını engeller.

Ekran verimliliğini basitleştirilmiş biçimde şöyle düşünebiliriz:

$$V = \frac{K \times A}{B + Z + 1}$$

Burada $K$ kullanılabilir piksel alanını, $A$ aktif odak süresini, $B$ boyun hareketi maliyetini ve $Z$ zihinsel geçiş sayısını temsil eder. Formül bilimsel bir standart değil; daha fazla ekran alanının, kötü yerleşim nedeniyle otomatik olarak daha yüksek verimlilik getirmediğini anlatan pratik bir modeldir.

## Ergonomik karşılaştırma

| Ölçüt | Çoklu fiziksel ekran | Tek ultra geniş ekran |
|---|---|---|
| Boyun hareketi | Yan ekranlarda belirgin olabilir | İçerik merkeze yakın tutulabilir |
| Göz odağı | Çerçeve geçişleri odağı bölebilir | Daha akıcı yatay tarama sağlar |
| Pencere düzeni | İşletim sistemi doğal olarak ayırır | Bölgeleme yazılımı gerektirir |
| Tam ekran kullanımı | Bir uygulama tek ekranı kaplar | Tam ekran gereğinden fazla büyüyebilir |
| Bağlam ayrımı | Görevler fiziksel olarak ayrılır | Görevler sanal bölgelerle ayrılır |
| Masa ve kablo düzeni | Daha fazla alan ve kablo ister | Daha sade bir kurulum sunar |

Çoklu monitörde ana ekran tam karşınızda değilse başınızı gün boyunca sürekli çevirmek zorunda kalırsınız. Küçük açılar masum görünse de uzun süreli statik dönüş kas yorgunluğu oluşturabilir. En sık kullanılan editör doğrudan karşıya, ikincil araçlar ise mümkün olduğunca merkeze yakın yerleştirilmelidir.

Ultra geniş ekranda fiziksel dönüş azalır, fakat gözler büyük bir yatay alanı tarar. Ayrıca 49 inçlik bir ekranı tek pencereyle doldurmak, kod satırlarını küçük bir romana dönüştürür. Okunabilirlik için editör genişliğini sınırlamak ve yan alanları terminal, test çıktısı veya dokümantasyona ayırmak daha mantıklıdır.

## Pencere yönetimi neden kritik?

Ultra geniş ekran, bölgeleme olmadan büyük bir boş arazi gibidir. Windows PowerToys FancyZones, macOS Rectangle veya Linux pencere yöneticileri bu alanı işlevsel bölgelere dönüştürür. Örneğin AutoHotkey v2 ile aktif pencereyi ekranın merkezindeki çalışma bölgesine taşıyan küçük bir kısayol hazırlanabilir:

```autohotkey
#Requires AutoHotkey v2.0

; Win+Alt+C aktif pencereyi merkez çalışma alanına taşır.
#!c:: {
    monitorWidth := A_ScreenWidth
    targetWidth := Round(monitorWidth * 0.55)
    targetX := Round((monitorWidth - targetWidth) / 2)
    WinMove targetX, 40, targetWidth, A_ScreenHeight - 80, "A"
}
```

Bu kod aktif pencereyi ekran genişliğinin yüzde 55’ine ayırır ve merkeze taşır. Böylece editör ergonomik bölgede kalırken iki yanda yardımcı uygulamalar için alan açılır. Benzer kısayollar terminal ve tarayıcı için de oluşturulabilir.

## Konsantrasyon için doğru seçim

Sık sık dokümantasyon, canlı ön izleme veya izleme panelleri kullanan geliştiriciler çoklu ekranın fiziksel görev ayrımından yararlanabilir. Buna karşılık tek bir projeye uzun süre odaklanan, kablo karmaşasını azaltmak isteyen ve pencerelerini disiplinli biçimde düzenleyen kişiler ultra geniş ekranda daha akıcı çalışabilir.

En iyi sistem, en fazla pencereyi gösteren değil, gereksiz pencereleri görünmez kılan sistemdir. Bildirimleri yan ekrana taşımak çözüm gibi görünse de göz ucuyla parlayan her mesaj dikkati böler. Hangi ekranı seçerseniz seçin; ana çalışma alanını karşıya alın, ekranın üst kenarını göz hizasına yaklaştırın, yaklaşık bir kol mesafesi bırakın ve görev bazlı pencere düzenleri oluşturun. Sonuçta verimliliği belirleyen monitör sayısından çok, dikkatinizi kaç farklı yöne çevirdiğinizdir.

![coklu-ekran-mi-29](/img/coklu-ekran-mi-29.svg)


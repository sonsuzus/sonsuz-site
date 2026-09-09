---
layout: post
title: "Seçenek Bolluğu, Karar Kıtlığı: Seçim Paradoksunun Arayüz Tasarımına Etkisi"
math: true
categories: 
  - Bilgi
tags: 
  - bilişsel psikoloji
  - ux tasarımı
  - seçim paradoksu
toc: true
---

Bir e-ticaret sitesinde yalnızca “siyah mı, beyaz mı?” sorusuyla karşılaşmak kolaydır. Fakat renk, beden, kumaş, teslimat, satıcı ve kampanya seçenekleri aynı anda önümüze döküldüğünde beynimiz küçük bir yönetim kurulu toplantısı başlatır. Seçenek sayısı arttıkça özgürlük hissi büyüyebilir; buna karşılık karar verme süresi, zihinsel yük ve sayfayı terk etme ihtimali de artabilir. Bilişsel psikolojide bu gerilim **seçim paradoksu** ile açıklanır.
``

## Daha fazla seçenek neden daha zor olabilir?

İnsanların çalışma belleği sınırlıdır. Her seçeneğin fiyatını, avantajını ve riskini aynı anda değerlendirmek bilişsel yük oluşturur. Özellikle seçenekler birbirine yakınsa kullanıcı yalnızca ürünleri değil, “yanlış karar verirsem ne kaybederim?” sorusunu da karşılaştırır.

Karar süresiyle seçenek sayısı arasındaki ilişkiyi açıklamak için **Hick–Hyman Yasası** kullanılabilir:

$$T = a + b\log_2(n+1)$$

Burada $T$ karar süresini, $n$ seçenek sayısını, $a$ temel tepki süresini ve $b$ arayüz ile kullanıcının özelliklerine bağlı katsayıyı temsil eder. Formül, karar süresinin seçeneklerle doğrusal değil, logaritmik arttığını söyler. Ancak seçeneklerin karmaşıklığı ve benzerliği yükseldiğinde pratikte gecikme çok daha can sıkıcı hissedilebilir.

| Arayüz durumu | Bilişsel sonuç | Olası kullanıcı davranışı |
|---|---|---|
| Az ve belirgin seçenek | Düşük karşılaştırma yükü | Hızlı karar |
| Çok fakat kategorize edilmiş seçenek | Yönetilebilir zihinsel yük | Filtreleme ve keşif |
| Çok ve birbirine benzer seçenek | Karar çatışması | Erteleme veya terk |
| Önerilen varsayılan seçenek | Daha az karar maliyeti | Daha hızlı dönüşüm |

## Reçel deneyi ne anlatıyor?

Sheena Iyengar ve Mark Lepper’ın 2000 yılında yayımlanan ünlü saha deneyinde bir markette müşterilere farklı sayılarda reçel sunuldu. Geniş seçenekli stant daha fazla ilgi çekerken, sınırlı seçenekli stanttan alışveriş yapma oranı daha yüksek çıktı. Basit mesaj şuydu: **Çeşitlilik dikkat çekebilir, fakat seçim yapmak başka bir iştir.**

Yine de bu sonuç “çok seçenek her zaman kötüdür” şeklinde okunmamalıdır. Sonraki çalışmalar, etkinin ürün türüne, kullanıcının uzmanlığına, tercihlerin netliğine ve seçeneklerin nasıl düzenlendiğine bağlı olduğunu gösterdi. Örneğin profesyonel bir fotoğrafçı çok sayıda lens filtresinden memnun olabilirken, ilk kamerasını alan biri aynı sayfada kaybolabilir.

## Terk edilme oranını nasıl ölçeriz?

Bir arayüzde seçenek yoğunluğunun etkisini anlamanın güvenilir yolu A/B testidir. A sürümü 24 ürünü aynı anda, B sürümü ise önce dört kategori göstererek ilerlemeli seçim sunabilir.

Terk edilme oranı şöyle hesaplanır:

$$R_{terk} = \frac{Ziyaretçi - Hedefi\ tamamlayan}{Ziyaretçi} \times 100$$

Yalnızca dönüşüme bakmak yeterli değildir. Karar süresi, filtre kullanımı, geri dönüşler ve satın alma sonrası iptaller de izlenmelidir. Aşağıdaki JavaScript örneği, kullanıcının karar ekranında geçirdiği süreyi analitik sisteme gönderir:

```javascript
const decisionStart = performance.now();

function trackChoice(optionId) {
  const durationMs = Math.round(performance.now() - decisionStart);

  analytics.track("option_selected", {
    optionId,
    durationMs,
    visibleOptionCount: document.querySelectorAll(".option").length
  });
}
```

Kod, ekran açıldıktan sonra geçen süreyi ölçer ve seçim yapıldığında görünen seçenek sayısıyla birlikte kaydeder. Böylece “çok seçenek vardı” iddiası ölçülebilir bir hipoteze dönüşür.

## Arayüzü nasıl sadeleştirmeli?

Seçenekleri körlemesine silmek yerine **aşamalı açıklama** kullanılabilir: Önce temel kategoriler, ardından ayrıntılar gösterilir. Akıllı varsayılanlar, “en popüler” etiketi, karşılaştırma tabloları ve kişiselleştirilmiş öneriler de karar maliyetini azaltır. Filtreler kullanıcının dilini konuşmalı; “teknik empedans” yerine gerekirse “telefonla uyumlu” denmelidir.

İyi arayüz, kullanıcıdan kararı almaz; kararın zihinsel faturasını küçültür. Amaç seçenekleri yok etmek değil, anlamlı kümelere dönüştürmektir. Çünkü dijital dünyada bazen en değerli özellik, yeni bir seçenek eklemek değil, hangisinin seçileceğini berraklaştırmaktır.

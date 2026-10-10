---
layout: post
title: "Zekâ Soruları Platformu: H5P, Moodle ve Özel Soru Bankasıyla Akıllı Bir Sistem Kurmak"
math: true
categories: 
  - Proje
tags: 
  - h5p
  - moodle
  - soru-bankası
  - eğitim-teknolojileri
  - javascript
  - oyunlaştırma
toc: true
image: /img/zeka-sorulari-platformu-27.png
---

Zekâ soruları yalnızca “Doğru cevap hangisi?” demekten ibaret değildir; süre yönetimi, ipucu kullanımı, zorluk dengesi ve çözüm yolunun açıklanması da deneyimin parçasıdır. H5P’nin etkileşimli içeriklerini, Moodle’ın öğrenme yönetimi yeteneklerini ve özel bir soru bankasının esnekliğini birleştirerek hem eğlenceli hem de ölçülebilir bir zekâ soruları platformu geliştirebiliriz.

``

## Sistemin temel mantığı

Platformu üç katmanlı düşünmek işleri kolaylaştırır. H5P, sorunun kullanıcıya nasıl sunulacağını belirler. Moodle; kullanıcı, ders, yetki, not ve raporlama süreçlerini yönetir. Özel soru bankası ise soruların kategorilerini, zorluk seviyelerini, sürümlerini ve istatistiklerini saklar.

Bir sorunun zorluk değeri yalnızca geliştiricinin tahminiyle belirlenmemelidir. Kullanıcıların başarı oranından yararlanılabilir. Bir soruyu $N$ kişi çözmüş ve $D$ kişi doğru cevaplamışsa kolaylık indeksi şöyle hesaplanır:

$$p = \frac{D}{N}$$

$p$ değeri 1’e yaklaştıkça soru kolaylaşır. Zorluk puanını $z = 1-p$ olarak tanımlarsak yüksek değerler daha zor soruları temsil eder. Örneğin 100 kişiden 25’i doğru cevap verdiyse $p=0.25$ ve $z=0.75$ olur.

## Hangi bileşen ne yapmalı?

| Bileşen | Güçlü tarafı | Sınırlaması | Önerilen rol |
|---|---|---|---|
| H5P | Etkileşimli ve görsel soru tipleri | Karmaşık veri analizinde sınırlı | Soru arayüzü ve geri bildirim |
| Moodle | Kullanıcı, ders, not ve yetki yönetimi | Özel oyun mekanikleri ek geliştirme ister | Ana platform ve raporlama |
| Özel soru bankası | Tam esneklik ve gelişmiş filtreleme | Bakım ve güvenlik sorumluluğu getirir | Merkezi içerik ve istatistik servisi |

![zeka-sorulari-platformu-27](/img/zeka-sorulari-platformu-27.svg)


H5P içeriği Moodle içine eklentiyle yerleştirilebilir. Ancak sorular farklı uygulamalarda da kullanılacaksa içerikleri yalnızca H5P dosyalarında tutmak yerine merkezi bir API üzerinden sunmak daha sağlıklıdır. Böylece mobil uygulama, web sitesi ve Moodle aynı kaynaktan beslenir.

## Örnek soru veri modeli

Aşağıdaki JavaScript nesnesi, çoktan seçmeli bir mantık sorusunun sadeleştirilmiş veri yapısını gösterir:

```javascript
const question = {
  id: "logic-1042",
  type: "multiple-choice",
  category: "örüntü",
  difficulty: 0.65,
  prompt: "2, 6, 12, 20 dizisindeki sonraki sayı nedir?",
  options: [28, 30, 32, 36],
  correctIndex: 1,
  explanation: "Terimler n × (n + 1) düzenini izler.",
  timeLimit: 45,
  tags: ["matematik", "örüntü"]
};
```

Bu modelde `difficulty` uyarlanabilir test üretmek, `explanation` öğretici geri bildirim göstermek, `timeLimit` ise süreye dayalı puanlama yapmak için kullanılır. API, bu veriyi H5P’ye uygun biçime dönüştürebilir veya doğrudan özel arayüzde gösterebilir.

## Puanlama ve oyunlaştırma

Sadece doğru cevaba puan vermek, rastgele tahminleri ödüllendirebilir. Süreyi ve ipucu kullanımını hesaba katan bir formül daha dengelidir:

$$P = B \times d \times \max(0.4, 1-\frac{t}{T}) - 10h$$

Burada $B$ temel puan, $d$ zorluk çarpanı, $t$ harcanan süre, $T$ süre sınırı ve $h$ kullanılan ipucu sayısıdır. `max` bölümü, doğru fakat yavaş çözümlerin tamamen puansız kalmasını önler. Rozetler, günlük seriler ve kategori bazlı seviyeler de motivasyonu artırabilir; fakat liderlik tablosu zorunlu olmamalıdır.

## Uygulama yol haritası

İlk sürümde Moodle kurulumu, H5P eklentisi, kullanıcı girişi ve temel soru API’si hazırlanmalıdır. İkinci aşamada soru editörü, sürümleme, ayrıntılı çözüm açıklamaları ve zorluk analizi eklenebilir. Son aşamada uyarlanabilir sınav motoru devreye girer: Kullanıcı doğru cevapladıkça daha zor, zorlandıkça daha öğretici sorular seçilir.

Ayrıca soru metinleri kullanıcı girdisi içeriyorsa XSS filtreleri uygulanmalı, API erişimi yetkilendirilmeli ve deneme kayıtları kişisel verilerden ayrıştırılmalıdır. Böylece platform, “birkaç bilmece yayınlayan site” olmaktan çıkıp ölçülebilir, genişletilebilir ve gerçekten öğretici bir öğrenme ekosistemine dönüşür.

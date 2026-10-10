---
layout: post
title: "Rastgele Soru Üretme Sistemleri: H5P, Moodle Question Bank ve Özel Algoritmalar"
math: true
categories: 
  - Bilgi
tags: 
  - h5p
  - moodle
  - soru-bankası
  - algoritma
  - eğitim-teknolojileri
  - rastgeleleştirme
toc: true
image: /img/rastgele-soru-uretme-18.png
---

Her öğrenciye farklı görünen ama aynı kazanımı ölçen bir sınav hazırlamak, eğitim teknolojilerinin en eğlenceli problemlerinden biridir. Rastgele soru üretme sistemleri; hazır bir havuzdan soru seçebilir, seçeneklerin sırasını değiştirebilir veya matematiksel parametrelerden yepyeni sorular oluşturabilir. H5P hızlı etkileşimler, Moodle Question Bank kapsamlı sınav yönetimi, özel algoritmalar ise neredeyse sınırsız üretim özgürlüğü sunar.

``

## Rastgelelik gerçekte ne anlama gelir?

Bir sistemde $N$ adet soru varsa ve sınav için bunlardan $k$ tanesi eşit olasılıkla seçiliyorsa, belirli bir sorunun sınava girme olasılığı yaklaşık olarak

$$P(\text{sorunun seçilmesi}) = \frac{k}{N}$$

olur. Örneğin 100 soruluk havuzdan 20 soru seçildiğinde her sorunun sınavda görünme olasılığı $0.20$ seviyesindedir. Ancak gerçek kalite yalnızca rastgele seçimden gelmez. Zorluk, konu dağılımı ve öğrenme çıktıları da dengelenmelidir.

Daha kontrollü bir modelde sınav; 4 kolay, 4 orta ve 2 zor sorudan oluşturulabilir. Buna **katmanlı rastgele seçim** denir. Böylece bir öğrenci tamamen kolay, başka biri tamamen zor bir sınavla karşılaşmaz.

## Üç yaklaşımın karşılaştırması

| Yaklaşım | Güçlü yanı | Sınırlaması | En uygun kullanım |
|---|---|---|---|
| H5P | Görsel ve etkileşimli içerik | Gelişmiş soru üretimi sınırlı | Ders içi alıştırmalar |
| Moodle Question Bank | Kategori, etiket ve sınav analizi | Yapılandırma zaman alabilir | Ölçme ve değerlendirme |
| Özel algoritma | Parametrik ve sınırsız üretim | Yazılım geliştirme gerektirir | Uyarlanabilir sınavlar |

## H5P ile hızlı etkileşim

H5P; Multiple Choice, Fill in the Blanks ve Question Set gibi içerik türleriyle çalışır. Seçenek sıralaması karıştırılabilir ve bir soru setinden belirli sayıda içerik gösterilebilir. En büyük avantajı, öğrencinin anında geri bildirim almasıdır.

Bununla birlikte H5P çoğunlukla önceden hazırlanmış içerikleri rastgele sunar. Örneğin her seferinde farklı katsayılara sahip bir denklem oluşturmak istiyorsanız ek JavaScript geliştirmesi veya harici bir servis gerekebilir.

## Moodle Question Bank ile kontrollü seçim

Moodle soruları kategoriler altında saklayabilir. “Cebir/Kolay” ve “Cebir/Zor” gibi kategoriler oluşturup sınava her kategoriden rastgele soru eklemek mümkündür. Ayrıca **Calculated Question** türü, değişkenleri belirli aralıklardan seçerek parametrik sorular üretir.

Örneğin $a$ ve $b$ rastgele seçildiğinde öğrenciye $a+b$ sorulabilir. $a \in [2,10]$ ve $b \in [5,20]$ tanımlanırsa sistem çok sayıda varyasyon oluşturur. Tolerans, birim ve ondalık hassasiyeti gibi ayrıntılar da Moodle üzerinden yönetilebilir.

## Özel algoritma nasıl kurulur?

Basit bir JavaScript fonksiyonu, iki katsayı seçip birinci dereceden denklem üretebilir:

```javascript
function denklemUret() {
  const x = Math.floor(Math.random() * 9) + 1;
  const a = Math.floor(Math.random() * 8) + 2;
  const b = Math.floor(Math.random() * 20) + 1;

  return {
    soru: `${a}x + ${b} = ${a * x + b} denkleminde x kaçtır?`,
    cevap: x
  };
}

console.log(denklemUret());
```

Kod önce doğru cevabı belirler, ardından bu cevaba uygun denklem kurar. Bu yaklaşım önemlidir; rastgele bir soru üretip sonradan çözmeye çalışmak yerine, **cevaptan soruya doğru üretim** hatalı veya çözümsüz örneklerin önüne geçer.

## Adil ve güvenilir bir sistem için

Gerçek sınavlarda sözde rastgele sayı üreteci için bir `seed` saklamak yararlıdır. Aynı seed kullanıldığında aynı sınav yeniden oluşturulabilir; böylece öğrenci itirazları incelenebilir. Ayrıca algoritma şu kontrollerden geçmelidir:

- Aynı sorunun sınav içinde tekrarlanmaması
- Yanlış seçeneklerin doğru cevaptan farklı olması
- Zorluk dağılımının korunması
- Üretilen değerlerin anlamlı aralıklarda kalması
- Soru sürümlerinin ve seed bilgilerinin kaydedilmesi

Hızlı ve görsel etkinliklerde H5P, kurumsal sınavlarda Moodle, benzersiz ve uyarlanabilir senaryolarda ise özel algoritmalar öne çıkar. En güçlü çözüm çoğu zaman bunları yarıştırmak değil, H5P’nin etkileşimini Moodle’ın soru bankası ve özel bir üretim servisinin esnekliğiyle birleştirmektir.

![rastgele-soru-uretme-18](/img/rastgele-soru-uretme-18.svg)


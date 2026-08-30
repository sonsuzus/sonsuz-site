---
layout: post
title: "Üstün Yetenekli Öğrenciler İçin Kodlama Müfredatı: Hızdan Derinliğe"
math: true
categories: 
  - Bilgi
tags: 
  - kodlama eğitimi
  - üstün yetenek
  - proje tabanlı öğrenme
---

Zihinsel işlem hızı yüksek öğrenciler için kodlama eğitimi, sadece daha fazla alıştırma vermek değildir; daha belirsiz, daha çok çözüm yolu bulunan ve düşünme kalitesini görünür kılan problemler tasarlamaktır. Bu öğrenciler temel sözdizimini hızla geçebilir, fakat asıl potansiyelleri algoritma seçerken, varsayımları sorgularken ve kendi projelerinin sınırlarını çizerken ortaya çıkar. İyi bir müfredat, onları “ilk çalışan çözüm” ile yetinmek yerine daha zarif, adil ve sürdürülebilir çözümler aramaya davet eder.
``

## Neden hız tek başına hedef değildir?

Bir öğrencinin kısa sürede doğru sonuca ulaşması değerlidir; ancak yazılım geliştirme çok boyutlu bir süreçtir. Bir algoritmanın başarısını kabaca şu şekilde düşünebiliriz:

$$Başarı = Doğruluk \times Verimlilik \times Açıklanabilirlik$$

Örneğin iki öğrencinin de çalışan bir arama programı yazdığını varsayalım. Birincisi listedeki her elemanı kontrol eden doğrusal arama kullanabilir: $O(n)$. İkincisi sıralı veri için ikili aramayı keşfedebilir: $O(\log n)$. Fakat üstün yetenekli öğrenci için bir sonraki soru şudur: “Veri sıralı değilse, sıralama maliyeti ne olur? Çok sayıda sorguda hangi yaklaşım avantajlıdır?” Müfredatın görevi bu tür ikinci ve üçüncü seviye soruları üretmektir.

| Yaklaşım | Öğrenciye verilen görev | Beklenen düşünme biçimi |
|---|---|---|
| Hızlandırma | Daha zor konuya erken geçiş | Bilgi edinme |
| Zenginleştirme | Aynı konuyu farklı bağlamlarda kullanma | Bağlantı kurma |
| Açık uçlu proje | Problemi ve ölçütleri öğrencinin belirlemesi | Tasarım ve eleştirel düşünme |

## Müfredatın üç katmanlı yapısı

İlk katman, Python veya JavaScript ile sağlam programlama temelleridir: değişkenler, fonksiyonlar, veri yapıları, hata ayıklama ve test. Ancak örnekler “not ortalaması hesaplama” düzeyinde kalmamalıdır. Öğrenciye hatalı veri içeren bir okul anketini temizletmek ya da farklı veri yapılarının performansını karşılaştırmak daha anlamlıdır.

İkinci katman algoritmik düşünmedir. Özyineleme, grafikler, dinamik programlama ve karmaşıklık analizi; ezberlenmesi gereken başlıklar değil, problem çözme araç çantası olarak ele alınmalıdır. Her ünitenin sonunda öğrenciler çözümünü savunmalıdır: Neden bu algoritma? Hangi durumda başarısız olur? Bellek ve zaman arasında hangi ödün verildi?

Üçüncü katman ise proje stüdyosudur. Burada öğretmen cevap dağıtan kişi değil, iyi sorular soran bir danışmandır. Proje değerlendirmesinde yalnızca çalışan ürün değil; araştırma günlüğü, başarısız denemeler, test senaryoları ve sunum da puanlanmalıdır.

## Açık uçlu proje fikirleri

“Akıllı şehir rotalama” projesinde öğrenci, okul servisi için en kısa rotayı değil, en adil veya en düşük karbonlu rotayı tasarlayabilir. Böylece graf teorisi ile etik kararlar birleşir. “Yanlılık avcısı” projesinde ise basit bir öneri sistemi oluşturulur; öğrenci veri kümesindeki dengesizliklerin sonucu nasıl değiştirdiğini deneylerle gösterir.

Aşağıdaki kod, rota maliyetine yalnızca mesafeyi değil, bekleme süresini de katan küçük bir modeldir. Öğrenci ağırlıkları değiştirerek farklı tasarım önceliklerini test edebilir:

```python
def rota_maliyeti(mesafe_km, bekleme_dk, mesafe_agirligi=1.0, zaman_agirligi=0.3):
    """Mesafe ve beklemeyi tek bir karşılaştırma puanına dönüştürür."""
    return mesafe_km * mesafe_agirligi + bekleme_dk * zaman_agirligi

rota_a = rota_maliyeti(8, 20)
rota_b = rota_maliyeti(10, 5)
print(f"A rotası: {rota_a:.1f}, B rotası: {rota_b:.1f}")
```

Bu kısa kodun asıl değeri sonuçtan çok tartışmadadır: $zaman\_agirligi$ neden 0.3? Tüm yolcular için aynı ağırlık adil mi? Yağmurlu günlerde model değişmeli mi?

## Değerlendirme: ürün değil, zihinsel iz

Üstün yetenekli öğrenciler için rubrikler tek doğru cevabı ödüllendirmemelidir. Özgünlük, algoritmik gerekçe, test kalitesi, iş birliği ve yansıtma ayrı ölçülmelidir. Böyle bir müfredat, hızlı düşünen öğrenciyi sürekli “bir sonraki konuya” koşturmaz; onun hızını daha derin sorulara, daha cesur denemelere ve toplumsal etkisi olan yazılım fikirlerine dönüştürür.

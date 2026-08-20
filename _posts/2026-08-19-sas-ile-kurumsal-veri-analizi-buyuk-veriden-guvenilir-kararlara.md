---
layout: post
title: "SAS ile Kurumsal Veri Analizi: Büyük Veriden Güvenilir Kararlara"
math: true
categories: 
  - Bilgi
tags: 
  - sas
  - veri analizi
  - iş zekası
  - veri madenciliği
---

Kurumsal veri analizi, yalnızca milyonlarca satırlık tabloyu hızlıca işlemek değildir; veriyi güvenilir, denetlenebilir ve karar verilebilir bir hikâyeye dönüştürme sanatıdır. SAS, özellikle banka, sigorta, perakende ve kamu gibi düzenlemelerin yoğun olduğu sektörlerde bu hikâyeyi kurmak için uzun yıllardır kullanılan güçlü bir platformdur. Veri entegrasyonundan istatistiksel modellemeye, zamanlanmış raporlardan veri madenciliğine kadar tek bir ekosistemde çalışmayı mümkün kılar.
``

SAS’ın kurumsal dünyadaki temel gücü, **tekrarlanabilir analitik süreçler** oluşturmasıdır. Bir Excel dosyasında yapılan manuel filtreleme hızlı başlayabilir; fakat aynı işlem her ay, farklı kaynaklardan ve yüz milyonlarca kayıtla yapılacaksa süreç kırılganlaşır. SAS programları ise veri adımlarını açık biçimde tanımlar, log üretir ve planlanmış görevlerle otomatik çalıştırılabilir.

Bir analitik sürecin değerini basitçe şu şekilde düşünebiliriz:

$$Karar\ Değeri = Veri\ Kalitesi \times Model\ Başarısı \times Operasyonel\ Hız$$

Bu çarpanlardan biri sıfıra yaklaşırsa en parlak tahmin modeli bile işe yaramaz. Örneğin müşteri terk olasılığı doğru hesaplanmış olsa da rapor satış ekibine üç hafta geç ulaşıyorsa ticari fırsat kaçabilir.

| İhtiyaç | Geleneksel yaklaşım | SAS ile kurumsal yaklaşım |
|---|---|---|
| Veri hazırlama | Manuel dosya birleştirme | Tekrarlanabilir DATA step ve SQL akışları |
| Raporlama | Statik elektronik tablolar | Zamanlanmış, standartlaştırılmış çıktılar |
| Modelleme | Dağınık araçlar | İstatistiksel prosedürler ve model yönetimi |
| Denetim | Belirsiz işlem geçmişi | Kod, log ve çıktı izlenebilirliği |

SAS programlamasında iki ana yapı sık kullanılır: **DATA step** ve **PROC** prosedürleri. DATA step, veriyi okuma, dönüştürme ve yeni değişken üretme işlerinde başarılıdır. PROC blokları ise özetleme, istatistik, grafik, regresyon veya kümeleme gibi hazır analitik yetenekleri çağırır. Aşağıdaki örnek, satış verisini temizleyip bölgesel performansı özetler:

```sas
/* Eksik satış tutarlarını sıfır kabul ederek net geliri hesaplar */
data satis_temiz;
    set ham.satislar;
    if missing(satis_tutari) then satis_tutari = 0;
    net_gelir = satis_tutari - iade_tutari;
run;

/* Bölge bazında toplam ve ortalama net geliri üretir */
proc summary data=satis_temiz nway;
    class bolge;
    var net_gelir;
    output out=bolge_raporu
        sum=toplam_net_gelir
        mean=ortalama_net_gelir;
run;
```

Bu kod küçük görünse de kurumsal ölçekte kritik bir prensibi temsil eder: iş kuralları kod içinde görünür ve tekrar uygulanabilir olmalıdır. `missing` kontrolü, eksik değerlerin raporu bozmasını önler; `PROC SUMMARY` ise yöneticilerin doğrudan kullanabileceği özet bir veri kümesi üretir.

Veri madenciliği tarafında SAS; segmentasyon, sahtecilik tespiti, kredi skorlama ve talep tahmini gibi senaryolarda kullanılır. Örneğin lojistik regresyon, bir müşterinin kampanyaya yanıt verme olasılığını hesaplayabilir:

$$P(Y=1)=\frac{1}{1+e^{-(\beta_0+\beta_1x_1+\cdots+\beta_nx_n)}}$$

Burada $Y=1$ müşterinin yanıt verdiğini, $x$ değişkenleri ise yaş, geçmiş harcama veya kanal tercihi gibi öznitelikleri temsil eder. Ancak model başarısını sadece doğruluk oranıyla değerlendirmek yanıltıcıdır. Dengesiz veri kümelerinde ROC-AUC, precision, recall ve maliyet matrisi birlikte değerlendirilmelidir.

| Ölçüt | Ne anlatır? | Ne zaman önemlidir? |
|---|---|---|
| Accuracy | Toplam doğru tahmin oranı | Sınıflar dengeliyse |
| Recall | Gerçek pozitifleri yakalama oranı | Sahtecilik veya risk tespiti |
| Precision | Pozitif tahminlerin isabeti | Gereksiz aksiyon maliyetliyse |
| ROC-AUC | Sınıfları ayırma kapasitesi | Model karşılaştırmasında |

Sonuç olarak SAS, sadece bir kodlama dili ya da raporlama aracı değildir; veri yönetişimi ile analitiği buluşturan kurumsal bir çalışma biçimidir. Başarılı bir SAS projesi, doğru prosedürü seçmekten önce doğru iş sorusunu, veri sahibini, kalite kurallarını ve çıktı tüketicisini tanımlar. Böylece büyük veri yığınları, karar vericilerin gerçekten kullanabileceği güvenilir içgörülere dönüşür.

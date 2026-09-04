---
layout: post
title: "Teknik Borcu Ölçmek: Hızlı Teslimatın Görünmeyen Faizi"
math: true
categories: 
  - Bilgi
tags: 
  - teknik borç
  - yazılım mimarisi
  - yazılım metrikleri
toc: true
---

Bir özelliği cuma akşamına yetiştirmek için katmanları atlamak, testleri ertelemek veya iki servisi geçici bir bağımlılıkla bağlamak oldukça caziptir. Üstelik sistem çalıştığı sürece kimse alarm zillerini duymaz. Fakat geniş ölçekli projelerde bu tavizler birikir; birkaç ay sonra küçük bir değişiklik bile onlarca dosyaya dokunan, günlerce test edilen bir operasyona dönüşür. Teknik borç tam olarak bu görünmeyen yavaşlamadır.

``

## Teknik borç neden finansal borca benzer?

Teknik borcun **ana parası**, bugün kaliteli çözüm yerine kısa yolu seçerek tasarruf edilen geliştirme süresidir. **Faizi** ise gelecekte yapılan her değişiklikte ödenen ek analiz, düzeltme, test ve koordinasyon maliyetidir.

Bir değişikliğin ideal süresi $T_i$, borçlu sistemdeki gerçek süresi $T_g$ ise değişiklik başına borç faizi şöyle düşünülebilir:

$$F = \frac{T_g - T_i}{T_i} \times 100$$

İdeal koşullarda iki saat sürecek bir iş sekiz saat sürüyorsa faiz oranı yüzde 300’dür. Elbette gerçek projelerde $T_i$ doğrudan bilinmez. Benzer işlerin geçmiş verileri, temiz modüllerdeki teslimat süreleri veya ekip tahminleri referans alınabilir.

## İzlenmesi gereken somut metrikler

Teknik borcu yalnızca statik analiz aracındaki “code smell” sayısına indirgemek yanıltıcıdır. Mimari borç; teslimat, kalite ve ekip davranışıyla birlikte ölçülmelidir.

| Metrik | Ne anlatır? | Borç sinyali |
|---|---|---|
| Lead Time for Changes | Commit ile üretim arasındaki süre | Düzenli yükseliş |
| Change Failure Rate | Hatalı dağıtımların oranı | Küçük değişikliklerde artış |
| MTTR | Arızadan sonra toparlanma süresi | Bağımlılıkların teşhisi zorlaştırması |
| Code Churn | Kısa sürede tekrar değişen kod | Yanlış soyutlama veya belirsiz tasarım |
| Coupling | Modüller arası bağımlılık | Bir değişikliğin geniş alana yayılması |
| Test süresi | Geri bildirim döngüsünün uzunluğu | Teslimatların seyrekleşmesi |

Özellikle **değişiklik yayılımı** güçlü bir mimari göstergedir. Bir iş talebi için değiştirilen modül sayısını ölçebiliriz:

$$Y = \frac{\text{Değiştirilen modül sayısı}}{\text{Toplam modül sayısı}}$$

Basit bir alan eklemek sistemin yüzde 40’ına dokunuyorsa mimariniz biraz fazla “sosyal” davranıyor olabilir.

## Borç Endeksi oluşturmak

Farklı metrikleri tek panoda izlemek için normalize edilmiş bir Teknik Borç Endeksi kullanılabilir:

$$TBE = 0.35L + 0.25C + 0.20F + 0.20R$$

Burada $L$ lead time artışını, $C$ coupling seviyesini, $F$ change failure rate’i ve $R$ yeniden çalışma oranını temsil eder. Ağırlıklar organizasyonun risklerine göre değiştirilmelidir; finans sisteminde hata oranı, içerik platformunda teslimat hızı daha ağır basabilir.

Aşağıdaki Python kodu ekiplerin aylık ölçümlerini basitçe puanlar:

```python
def debt_index(lead_time, coupling, failure_rate, rework):
    """Yüzde olarak normalize edilmiş metriklerden borç puanı üretir."""
    return round(
        0.35 * lead_time
        + 0.25 * coupling
        + 0.20 * failure_rate
        + 0.20 * rework,
        2
    )

score = debt_index(70, 60, 25, 45)
print(f"Teknik Borç Endeksi: {score}/100")
```

Kodun amacı kusursuz bilimsel sonuç vermek değil, zaman içindeki eğilimi görünür kılmaktır. Puan üç ay boyunca yükseliyorsa “hissediyoruz” demek yerine ölçülebilir bir iyileştirme görüşmesi başlatılabilir.

## Borcu yönetilebilir hâle getirmek

Her borç kötü değildir. Bilinçli alınmış, sahibi ve ödeme tarihi belirlenmiş bir taviz iş açısından mantıklı olabilir. Asıl tehlike, borcun kayıt dışı kalmasıdır. Mimari karar kayıtlarına gerekçe, beklenen kazanç, etkilenen modüller ve temizleme koşulu eklenmelidir.

Sprint kapasitesinin sabit bir bölümünü iyileştirmeye ayırmak da tek başına yeterli değildir. Önce en çok faiz üreten noktalar seçilmelidir. Lead time’ı uzatan ortak bileşeni sadeleştirmek, yalnızca estetik amaçlı yüzlerce dosyayı düzenlemekten daha değerlidir.

Sonuç olarak teknik borç, “kodumuz biraz dağınık” şikâyeti değil, geliştirme ekonomisini etkileyen ölçülebilir bir sistem özelliğidir. Teslimat süresi, hata oranı, yayılım ve yeniden çalışma birlikte izlendiğinde borç görünür olur; görünür olan borç da artık kader değil, planlanabilir bir yatırımdır.

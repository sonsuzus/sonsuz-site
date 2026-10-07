---
layout: post
title: "Vardiya Planlama Sistemi Seçimi: Sentrifugo, OrangeHRM ve OpenHRMS"
math: true
categories: 
  - Program
tags: 
  - vardiya planlama
  - insan kaynakları
  - sentrifugo
  - orangehrm
  - openhrms
  - optimizasyon
toc: true
image: /img/vardiya-planlama-sistemi-86.png
---

Vardiya planlamak, çalışan isimlerini bir takvime yerleştirmekten çok daha fazlasıdır. İzinler, yetkinlikler, çalışma süreleri ve adil dağılım aynı anda düşünülmelidir. Sentrifugo, OrangeHRM ve OpenHRMS gibi insan kaynakları sistemleri bu karmaşayı azaltabilir; ancak doğru seçim, yalnızca özellik listesindeki kutucukları sayarak yapılamaz.
``

## Vardiya planlamanın teorik temeli

Bir vardiya planı, kısıtlı optimizasyon problemi olarak modellenebilir. Çalışan $i$ ve vardiya $j$ için aşağıdaki karar değişkenini tanımlayalım:

$$
x_{ij} = \begin{cases}
1, & \text{çalışan } i \text{ vardiya } j\text{'ye atanırsa} \\
0, & \text{aksi durumda}
\end{cases}
$$

Her vardiyanın ihtiyaç duyduğu çalışan sayısı $r_j$ ise temel kapsama kısıtı şöyledir:

$$
\sum_i x_{ij} \geq r_j
$$

Buna haftalık çalışma süresi, dinlenme aralığı, izin günü ve yetkinlik gibi kurallar eklenir. Örneğin bir çalışanın toplam süresi $H_i$ sınırını aşmamalıdır:

$$
\sum_j h_jx_{ij} \leq H_i
$$

Gerçek hayatta amaç yalnızca boşlukları doldurmak değildir. Fazla mesaiyi, vardiyalar arasındaki dengesizliği ve çalışan tercihlerinin ihlalini azaltan bir maliyet fonksiyonu gerekir. Kısacası iyi plan, matematik ile insan mutluluğunun kahve molasında buluşmasıdır.

## Üç sistemin karşılaştırması

| Sistem | Temel yaklaşım | Güçlü yanı | Dikkat edilmesi gereken |
|---|---|---|---|
| Sentrifugo | Bağımsız, açık kaynak HRMS | İzin, çalışan ve performans süreçleri | Gelişmiş vardiya optimizasyonu özel geliştirme isteyebilir |
| OrangeHRM | Modüler insan kaynakları platformu | Kullanıcı dostu arayüz ve geniş ekosistem | Bazı gelişmiş özellikler sürüme veya ücretli modüllere bağlı olabilir |
| OpenHRMS | Odoo tabanlı modüler çözüm | Odoo uygulamalarıyla güçlü entegrasyon | Kurulum, uyarlama ve modül uyumluluğu teknik uzmanlık gerektirebilir |

![vardiya-planlama-sistemi-86](/img/vardiya-planlama-sistemi-86.svg)


### Sentrifugo

Sentrifugo, temel insan kaynakları verilerini merkezi biçimde yönetmek isteyen ekipler için sade bir başlangıç sunar. Çalışan profilleri, izin bilgileri ve organizasyon yapısı vardiya motoruna veri sağlayabilir. Buna karşılık karmaşık rotasyonlar, otomatik atama veya sektöre özel dinlenme kuralları için ek kod yazılması gerekebilir. Yazılım ekibi bulunan kurumlarda esneklik avantajdır; tak-çalıştır beklentisinde ise ek iş çıkarabilir.

### OrangeHRM

OrangeHRM, kullanım kolaylığı ve olgun HR ekosistemiyle öne çıkar. İzin, zaman takibi ve devamlılık verileri planlama sürecini besleyebilir. Bulut ve kurum içi seçeneklerinin bulunması farklı ölçeklere hitap eder. Yine de kullanılacak sürümün vardiya, devam takibi ve raporlama ihtiyaçlarını gerçekten karşıladığı doğrulanmalıdır. Demo ekranı güzeldir; fakat gece vardiyasındaki üç saatlik boşluğu demo heyecanı kapatmaz.

### OpenHRMS

OpenHRMS, Odoo altyapısının modülerliğinden yararlanır. Bordro, devam kontrolü, izin ve diğer operasyonel uygulamalarla bağlantı kurulabilmesi önemli avantajdır. Özellikle hâlihazırda Odoo kullanan işletmeler için doğal bir adaydır. Buna karşılık modül sürümleri, bağımlılıklar ve özelleştirmeler dikkatle yönetilmelidir.

## Basit bir vardiya kontrolü

Aşağıdaki Python kodu, planlanan saatlerin haftalık sınırı aşıp aşmadığını denetler. Bu bir optimizasyon motoru değildir; plan yayımlanmadan önce çalışan basit bir doğrulama katmanıdır.

```python
weekly_limit = 45
schedule = {
    "Ayşe": [8, 8, 8, 8, 8],
    "Mehmet": [10, 10, 10, 10, 8]
}

for employee, shifts in schedule.items():
    total = sum(shifts)
    status = "uygun" if total <= weekly_limit else "sınır aşıldı"
    print(f"{employee}: {total} saat — {status}")
```

Üretim ortamında bu kontrol; ardışık gece vardiyaları, minimum dinlenme süresi, yetkinlik eşleşmesi ve resmi tatillerle genişletilmelidir.

## Hangisini seçmeli?

Hızlı ve sade bir HR çekirdeği isteyen teknik ekipler Sentrifugo’yu değerlendirebilir. Hazır kullanım deneyimi ve geniş ürün ekosistemi arayanlar OrangeHRM’ye yönelebilir. Odoo ile bütünleşik, özelleştirilebilir bir yapı isteyen kurumlar için OpenHRMS daha anlamlıdır. Son karardan önce küçük bir pilot hazırlayın, gerçek vardiya verisini içe aktarın ve kısıtları test edin. En iyi sistem, en çok özelliğe sahip olan değil; pazartesi sabahı plan değiştiğinde ekibi paniğe sürüklemeyendir.

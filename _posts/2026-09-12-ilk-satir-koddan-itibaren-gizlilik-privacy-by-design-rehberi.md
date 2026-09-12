---
layout: post
title: "İlk Satır Koddan İtibaren Gizlilik: Privacy by Design Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - privacy by design
  - bilişim etiği
  - veri minimizasyonu
toc: true
---

Bir uygulama geliştirirken kullanıcıdan “Lazım olur” düşüncesiyle veri istemek, çekmeceye yıllarca kullanılmayan kablolar doldurmaya benzer. Aradaki önemli fark şudur: Kabloların sızdırılma, kötüye kullanılma veya bir insanın özel hayatını ihlal etme ihtimali yoktur. **Privacy by Design**, gizliliği sonradan eklenen bir onay kutusu değil; gereksinim analizinden veritabanına kadar bütün sistemi biçimlendiren temel bir tasarım ilkesi olarak ele alır.

``

## Privacy by Design nedir?

Privacy by Design, 1990’larda Ann Cavoukian tarafından geliştirilen ve gizliliğin sistemlerin varsayılan davranışı olması gerektiğini savunan yaklaşımdır. Temel fikir basittir: Toplanmayan veri çalınamaz, yanlış amaçla kullanılamaz ve silinmesi unutulamaz.

Bir sistemin oluşturduğu gizlilik riskini basitleştirilmiş biçimde şöyle düşünebiliriz:

$$R = D \times S \times T \times A$$

Burada $D$ toplanan veri miktarını, $S$ verinin hassasiyetini, $T$ saklama süresini, $A$ ise veriye erişebilen aktör sayısını temsil eder. Bu bilimsel bir ölçüm formülü olmaktan çok tasarım pusulasıdır. Çarpanlardan herhangi birini küçültmek toplam riski azaltır.

Privacy by Design yaklaşımı yedi temel ilkeye dayanır: Önleyici olmak, gizliliği varsayılan hâle getirmek, gizliliği tasarıma gömmek, işlevsellikle gizliliği birlikte korumak, veriyi yaşam döngüsü boyunca güvenceye almak, şeffaflık sağlamak ve kullanıcı çıkarlarına saygı göstermek.

## Geleneksel yaklaşım ile karşılaştırma

| Tasarım kararı | Geleneksel yaklaşım | Gizlilik odaklı yaklaşım |
|---|---|---|
| Kayıt formu | Çok sayıda zorunlu alan | Yalnızca gerekli alanlar |
| Analitik | Kullanıcı bazlı izleme | Toplulaştırılmış ölçüm |
| Saklama | Süresiz depolama | Otomatik silme süresi |
| Konum | Kesin GPS koordinatı | Yaklaşık bölge veya cihazda işleme |
| Yetkilendirme | Geniş ekip erişimi | En az ayrıcalık ilkesi |
| Günlükler | Tüm istek içeriği | Kimliksiz teknik olaylar |

Örneğin bir hava durumu uygulamasının sürekli GPS geçmişi tutması gerekmez. Konumu cihaz üzerinde yaklaşık bir şehre dönüştürüp sunucuya yalnızca şehir kodunu göndermek aynı işlevi çok daha az riskle sağlayabilir.

## Mimaride veri minimizasyonu

İlk adım, her veri alanı için üç soru sormaktır: **Neden topluyoruz, ne kadar süre saklayacağız ve kim erişecek?** Net cevap verilemiyorsa o alan büyük olasılıkla gereksizdir.

Veri akış şeması çıkararak bilginin kullanıcı cihazından hangi servislere gittiği belirlenmelidir. Ardından yerel işleme, takma adlandırma, şifreleme, kısa saklama süreleri ve rol tabanlı erişim uygulanabilir. Anonimleştirme ile takma adlandırma karıştırılmamalıdır: Takma adlı veri, ek bilgilerle yeniden bir kişiye bağlanabilir.

Aşağıdaki FastAPI örneği yalnızca hizmet için gerekli veriyi kabul eder ve gereksiz alanları reddeder:

```python
from datetime import date
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

app = FastAPI()

class NewsletterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: str
    consent_date: date

@app.post("/subscribe")
def subscribe(request: NewsletterRequest):
    # IP adresi veya cihaz kimliği kalıcı olarak kaydedilmez.
    save_subscription(
        email=request.email,
        consent_date=request.consent_date,
        delete_after_days=365
    )
    return {"status": "accepted"}
```

`extra="forbid"`, istemcinin beklenmeyen profil verileri göndermesini engeller. `delete_after_days` ise saklama politikasını sözlü bir vaatten uygulanabilir sistem davranışına dönüştürür. Gerçek projede silme işlemi zamanlanmış görevle yürütülmeli ve yedekler de aynı politikaya uymalıdır.

## Gizlilik bir özellik değil, süreçtir

Gizlilik odaklı mimari kurulduktan sonra tehdit modellemesi, erişim denetimleri ve silme testleri düzenli olarak tekrarlanmalıdır. Geliştirme günlüklerinde parola, erişim belirteci, e-posta veya kimlik numarası bulunmamalıdır. Test ortamlarında gerçek kullanıcı verisi yerine sentetik veri kullanılmalıdır.

Ayrıca kullanıcıya anlaşılır seçenekler sunulmalıdır. “Hizmeti kullanmak için her şeyi kabul et” ekranı hukuki görünse bile etik olmayabilir. İzinler belirli, geri alınabilir ve hizmetin amacıyla orantılı olmalıdır.

Privacy by Design’ın özü teknolojiden önce bir disiplin meselesidir: En güvenli veri, toplamaya hiç ihtiyaç duymadığımız veridir. Kod incelemelerinde performans ve güvenlik kadar “Bu veriye gerçekten gerek var mı?” sorusu da sorulduğunda gizlilik, belgedeki güzel bir cümle olmaktan çıkar ve mimarinin çalışan bir parçasına dönüşür.

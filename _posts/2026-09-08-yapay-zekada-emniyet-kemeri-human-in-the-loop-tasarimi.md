---
layout: post
title: "Yapay Zekâda Emniyet Kemeri: Human-in-the-Loop Tasarımı"
math: true
categories: 
  - Bilgi
tags: 
  - yapay zeka
  - human-in-the-loop
  - algoritmik güvenlik
toc: true
---

Bir yapay zekâ sistemi kredi başvurusunu reddettiğinde, ameliyat önerdiğinde veya şüpheli bir banka işlemini engellediğinde “Algoritma böyle söyledi” cevabı yeterli değildir. **Human-in-the-Loop (HITL)**, kritik karar noktalarında insan değerlendirmesini sürece dâhil ederek otomasyonun hızını insan muhakemesiyle birleştiren güvenli kontrol yaklaşımıdır. Amaç yapay zekâyı devre dışı bırakmak değil; belirsizlik, yüksek risk veya sıra dışı durumlarda ona deneyimli bir yardımcı pilot vermektir.

``

## Human-in-the-Loop tam olarak nedir?

HITL sisteminde algoritma verileri işler, bir tahmin veya öneri üretir; ancak belirlenmiş koşullar oluştuğunda karar doğrudan uygulanmaz. Çıktı bir uzmana gönderilir ve **onaylama, reddetme ya da düzeltme** yetkisi insanda kalır.

Bu yaklaşım üç temel bileşenden oluşur:

1. **Makine:** Veriyi hızlı biçimde analiz eder ve olasılık hesaplar.
2. **Kontrol politikası:** Hangi çıktıların insana yönlendirileceğini belirler.
3. **İnsan denetçi:** Bağlamı, etik sonuçları ve modelin göremediği istisnaları değerlendirir.

HITL ile yalnızca sonradan denetim yapan *human-on-the-loop* aynı şey değildir. İlkinde insan karar zincirinin içindedir; ikincisinde çalışan sistemi izler ve gerektiğinde müdahale eder.

| Yaklaşım | Kararı kim verir? | Hız | Risk kontrolü | Uygun kullanım |
|---|---|---:|---:|---|
| Tam otomasyon | Algoritma | Çok yüksek | Düşük/orta | Spam filtreleme |
| Human-in-the-Loop | Algoritma ve insan | Orta | Yüksek | Sağlık, kredi, işe alım |
| Tam insan kontrolü | İnsan | Düşük | Uzmanlığa bağlı | Benzersiz, stratejik vakalar |

## Belirsizlik, risk ve eşikler

Bir sınıflandırma modelinin tahmin güveni $p$ olsun. Basit bir kontrol politikası, güven belirli bir eşikten küçükse inceleme isteyebilir:

$$
p < \tau \Rightarrow \text{İnsan incelemesine gönder}
$$

Fakat yalnızca model güvenine bakmak tehlikelidir; model bazen yanlış kararından oldukça “emin” olabilir. Bu nedenle kararın etkisini de hesaba katmak gerekir. Örnek bir risk puanı şöyle tanımlanabilir:

$$
R = P(\text{hata}) \times C(\text{hatanın maliyeti})
$$

$R$ kabul edilebilir sınırı aştığında insan onayı zorunlu hâle gelir. On liralık kupon önerisiyle kanser teşhisini aynı eşikle yönetmemek gerektiği açıktır.

## Basit bir onay akışı

Aşağıdaki Python örneği, yüksek tutarlı veya düşük güvenli banka işlemlerini otomatik uygulamak yerine inceleme kuyruğuna yollar:

```python
REVIEW_LIMIT = 0.80
HIGH_VALUE = 50_000

def evaluate_transaction(transaction, model):
    fraud_probability = model.predict_proba(transaction)

    requires_review = (
        fraud_probability >= REVIEW_LIMIT
        or transaction.amount >= HIGH_VALUE
    )

    if requires_review:
        return {
            "status": "pending_human_approval",
            "reason": "high_risk_or_high_value",
            "score": fraud_probability
        }

    return {
        "status": "automatically_approved",
        "score": fraud_probability
    }
```

Buradaki önemli nokta `pending_human_approval` durumunun gerçek bir iş akışına bağlanmasıdır. Yetkili kişiye yeterli bağlam sunulmalı, karar zaman damgasıyla kaydedilmeli ve inceleme tamamlanmadan işlem uygulanmamalıdır.

## İyi bir HITL tasarımının kuralları

İnsan eklemek tek başına güvenlik sağlamaz. Denetçi yüzlerce benzer uyarı gördüğünde **otomasyon yanlılığına** kapılıp her öneriyi onaylayabilir. Bu nedenle arayüz, model sonucunun yanında gerekçeleri, kullanılan veriyi, belirsizlik seviyesini ve alternatifleri göstermelidir.

Ayrıca şu önlemler uygulanmalıdır:

- Kritik kararlar için rol tabanlı yetkilendirme kullanılmalıdır.
- Onay, ret ve düzeltmeler değiştirilemez denetim kayıtlarına yazılmalıdır.
- Süre aşımında karar otomatik onaylanmamalı; güvenli durum seçilmelidir.
- İnsan düzeltmeleri modelin yeniden eğitilmesinde kullanılmadan önce kalite kontrolünden geçmelidir.
- Farklı kullanıcı gruplarındaki hata ve onay oranları adalet açısından izlenmelidir.

## Sonuç

Human-in-the-Loop, yapay zekâ ile insan arasında yapılan basit bir görev paylaşımından çok daha fazlasıdır. Doğru kurulduğunda algoritma ölçek ve hız sağlar, insan ise bağlam, sorumluluk ve etik muhakeme getirir. En güvenli sistem, insana her düğmede “onayla” dedirten değil; insan dikkatini gerçekten kritik kararlara yönlendiren sistemdir.

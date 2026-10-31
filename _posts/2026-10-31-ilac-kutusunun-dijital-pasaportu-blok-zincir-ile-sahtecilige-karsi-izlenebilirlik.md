---
layout: post
title: "İlaç Kutusunun Dijital Pasaportu: Blok Zincir ile Sahteciliğe Karşı İzlenebilirlik"
math: true
categories: 
  - Bilgi
tags: 
  - blok zincir
  - sağlık teknolojileri
  - ilaç tedarik zinciri
  - izlenebilirlik
  - siber güvenlik
  - python
toc: true
image: /img/ilac-kutusunun-dijital-89.png
---

Bir ilaç kutusu fabrikadan eczaneye ulaşana kadar birçok el değiştirir. Peki kutunun gerçekten yetkili üreticiden geldiğini, yolculuk sırasında değiştirilmediğini ve uygun koşullarda taşındığını nasıl anlayabiliriz? Blok zincir, bu yolculuğa ortak bir dijital kayıt defteri sunar. Ancak sihirli bir sahtecilik dedektörü değildir; doğru tasarlandığında şüpheli hareketleri görünür kılan güçlü bir altyapıdır.


![ilac-kutusunun-dijital-89](/img/ilac-kutusunun-dijital-89.svg)

``

## Önce Mantık: Ortak Kayıt Defteri

Klasik sistemlerde üretici, dağıtıcı ve eczane kendi veritabanını tutar. Bir uyuşmazlık çıktığında kayıtları karşılaştırmak gerekir. Blok zincir yaklaşımında ise katılımcılar, üzerinde uzlaşılan olay geçmişini paylaşır. Her olay, önceki kayıtlarla kriptografik olarak ilişkilendirilir.

Sağlık sektöründe genellikle **izinli ağlar** tercih edilir. Katılımcıların kimlikleri bellidir; herkes istediği gibi kayıt yazamaz. Hangi kuruluşun hangi işlemi yapabileceği erişim kurallarıyla belirlenir. Mutabakat mekanizması da ağın yeni kayıtları hangi koşullarda kabul edeceğini düzenler. Bunun için enerji yoğun madencilik zorunlu değildir.

| Özellik | Ayrık veritabanları | İzinli blok zincir |
|---|---|---|
| Kayıt paylaşımı | Sistemler arası entegrasyon gerekir | Ortak olay geçmişi sunar |
| Değişiklik kontrolü | Merkezi yöneticiye bağlıdır | Ağ kurallarıyla yönetilir |
| Denetim | Kayıtları uzlaştırmak gerekir | Paylaşılan geçmiş incelenir |
| Veri doğruluğu | Kaynağa bağlıdır | Yine kaynağa bağlıdır |

Son satır kritik: Teknoloji, yanlış girilen bilgiyi kendiliğinden doğruya çeviremez.

## Kutunun Yolculuğu Nasıl Kaydedilir?

Üretici, her kutuya ürün kodu ve benzersiz seri numarası içeren bir kimlik verir. Parti numarası ve son kullanma tarihi gibi alanlar da kayda bağlanır. GS1 standartları ve EPCIS gibi olay paylaşım modelleri, farklı şirketlerin aynı dili konuşmasına yardımcı olabilir.

1. **Üretim:** Yetkili üretici, seri numarasını oluşturur ve üretim olayını imzalar.
2. **Devir:** Dağıtıcı teslim aldığında sahiplik veya gözetim değişikliği kaydedilir.
3. **Taşıma:** Gerekirse sıcaklık ölçümlerinin doğrulanabilir referansları eklenir.
4. **Teslim:** Eczane kutuyu okutur; beklenmeyen konum veya yinelenen seri kullanımı araştırılır.

Akıllı sözleşmeler, örneğin geri çağrılmış bir partinin devrini engelleyen kuralları çalıştırabilir. Fakat fiziksel kutunun hareketi ile dijital kaydın eşleşmesi ayrıca denetlenmelidir.

## Hash Bağlantısı Neden Önemli?

Basitleştirilmiş bir kayıt zincirinde her özet şöyle hesaplanabilir:

$$h_i = H(h_{i-1}, e_i)$$

Burada $e_i$ olay verisini, $h_{i-1}$ önceki özeti, $H$ ise kriptografik hash fonksiyonunu temsil eder. Eski bir olay değişirse sonraki özetler de değişir. Böylece geçmişe müdahale fark edilebilir. Hash, şifreleme değildir; veriyi gizlemez ve kaydı kimin oluşturduğunu tek başına kanıtlamaz.

## Python ile Küçük Bir İzlenebilirlik Deneyi

Aşağıdaki örnek, olayları önceki özete bağlar ve zinciri doğrular. Gerçek bir blok zincir değildir; bağlantı mantığını görmek için hazırlanmış küçük bir laboratuvardır.

```python
import hashlib
import json


def digest(record):
    raw = json.dumps(record, sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()


def append_event(chain, event):
    previous = chain[-1]["hash"] if chain else "0"
    record = {"previous": previous, "event": event}
    chain.append({**record, "hash": digest(record)})


def verify(chain, trusted_tip):
    previous = "0"
    for item in chain:
        record = {"previous": item["previous"],
                  "event": item["event"]}
        if item["previous"] != previous:
            return False
        if digest(record) != item["hash"]:
            return False
        previous = item["hash"]
    return previous == trusted_tip


chain = []
append_event(chain, {"serial": "ABC123", "action": "production"})
trusted_tip = chain[-1]["hash"]
print(verify(chain, trusted_tip))
```

`trusted_tip`, bağımsız ve güvenilir bir yerde saklanmalıdır. Aksi durumda saldırgan bütün özetleri yeniden hesaplayabilir. Üretim sisteminde ayrıca dijital imzalar, yetkilendirme, kalıcı depolama ve mutabakat gerekir. Kodumuz bunları uygulamıyor.

## Sahteciliği Azaltmak İçin Zincirin Dışına Bakın

Bir sahteci, gerçek kutunun karekodunu kopyalayabilir. Bu nedenle yalnızca kodun sistemde bulunması yeterli değildir. Aynı seri numarasının farklı yerlerde görünmesi, beklenmeyen transferler ve ambalaj bütünlüğü birlikte değerlendirilmelidir.

Sensörler de yanlış ölçebilir veya manipüle edilebilir. Kalibrasyon, güvenli cihaz kimliği ve denetimler bu yüzden önemlidir. Ticari sırlar ve hasta bilgileri herkese açık kayıt alanlarına yazılmamalıdır. Hassas veriler kontrollü depolarda tutulabilir; zincire yalnızca gerekli referanslar ve bütünlük kanıtları eklenebilir. Bu tasarımda bile erişim ve veri koruma yükümlülükleri ayrıca değerlendirilmelidir.

## Pilot Proje: Küçük Başlayın, Ölçerek Büyütün

İlk denemeyi bir üretici, bir dağıtıcı ve birkaç eczaneyle sınırlayın. Başarıyı yalnızca işlem sayısıyla değil; geri çağırma süresi, kayıt uyuşmazlığı oranı ve şüpheli seri numaralarını tespit etme süresiyle ölçün. Mevcut merkezi izlenebilirlik sistemleriyle entegrasyonu da planlayın. Çünkü bazen iyi yönetilen ortak bir veritabanı yeterlidir; blok zincir özellikle kurumlar arası ortak denetim ihtiyacı varsa anlam kazanır.

Sonuç: Dijital pasaport değerlidir, ama pasaporttaki bilgiyi fiziksel kutuyla eşleştiren süreçler olmadan güven yolculuğu tamamlanmaz.

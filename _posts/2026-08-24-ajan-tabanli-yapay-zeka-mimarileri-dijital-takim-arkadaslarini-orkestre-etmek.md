---
layout: post
title: "Ajan Tabanlı Yapay Zeka Mimarileri: Dijital Takım Arkadaşlarını Orkestre Etmek"
math: true
categories: 
  - Bilgi
tags: 
  - yapay zeka
  - ajan sistemleri
  - llm
  - mimari
  - python
toc: true
---

Tek bir büyük dil modeli etkileyici cevaplar üretebilir; ancak gerçek dünyadaki işler çoğunlukla araştırma, planlama, araç kullanımı, doğrulama ve raporlama gibi farklı uzmanlıklar ister. Ajan tabanlı yapay zeka mimarisi, bu yükü tek bir modele bırakmak yerine rolleri belirlenmiş birden fazla ajana dağıtır. Bunu küçük ama disiplinli bir yazılım ekibi gibi düşünebilirsiniz: biri işi parçalar, biri veri toplar, diğeri sonucu test eder, bir başkası da son kararı gözden geçirir.
``

Bir **ajan**, çevresinden bağlam alan, hedefe göre karar üreten ve eyleme geçebilen yazılım bileşenidir. Büyük dil modeli ajanın muhakeme motoru olabilir; fakat ajan yalnızca modelden ibaret değildir. Bellek, araç çağrıları, görev durumu, politika kuralları ve gözlem döngüsü de sistemin parçalarıdır. Temel çevrim genellikle şöyle ifade edilir:

$$A_t = \pi(O_t, M_t, G)$$

Burada $O_t$ anlık gözlemi, $M_t$ belleği, $G$ hedefi, $\pi$ ise karar politikasını temsil eder. Ajanın eylemi $A_t$, bir API isteği, veritabanı sorgusu, kod çalıştırma ya da başka bir ajana mesaj olabilir. Eylemden doğan sonuç yeni gözleme dönüşür ve döngü sürer.

## Neden Çoklu Ajan?

Çoklu ajan yaklaşımının ana fikri **uzmanlaşma**dır. Araştırmacı ajan web veya kurum içi kaynakları tarar; planlayıcı bağımlılıkları çıkarır; uygulayıcı araç çağrılarını yapar; denetçi ise halüsinasyon, güvenlik ve kalite risklerini kontrol eder. Böylece tek bir uzun isteme aşırı sorumluluk yüklemek yerine, daha küçük ve denetlenebilir karar noktaları oluşturursunuz.

| Mimari | Güçlü yönü | Dikkat edilmesi gereken |
|---|---|---|
| Tek ajan | Hızlı kurulum, düşük koordinasyon maliyeti | Karmaşık görevlerde bağlam ve hata yükü büyür |
| Merkezi orkestratör | Görev akışı görünür ve kontrollüdür | Orkestratör darboğaz veya tek hata noktası olabilir |
| Eşler arası ajanlar | Esnek, dağıtık iş birliği sağlar | Mesajlaşma ve anlaşmazlık yönetimi zordur |
| Hiyerarşik ekip | Yönetici ve uzman rolleri nettir | Fazla katman gecikmeyi artırabilir |

## Orkestrasyon: Herkes Konuşursa Toplantı Uzamaz mı?

Uzayabilir! Bu nedenle ajanlara yalnızca rol değil, açık **girdi-çıktı sözleşmeleri** de verilmelidir. Örneğin araştırmacı serbest metin yerine kaynak, güven puanı ve bulgular döndürmelidir. Denetçi ise sadece `onay`, `düzeltme` veya `engelle` kararlarından birini üretmelidir. Başarılı sistemler, doğal dilin esnekliğini yapılandırılmış veriyle dengeler.

Aşağıdaki sade örnek, bir yöneticinin araştırma ve denetim ajanlarını sırayla çalıştırmasını gösterir. Gerçek bir sistemde `call_llm` fonksiyonu model sağlayıcısına, araç katmanına ve kayıt altyapısına bağlanır.

```python
from dataclasses import dataclass

@dataclass
class Result:
    text: str
    confidence: float

def researcher(question: str) -> Result:
    # Kaynaklardan bulgu topladığı varsayılan uzman ajan
    return Result(text=f"'{question}' için kaynak özeti", confidence=0.82)

def reviewer(result: Result) -> str:
    # Kalite kapısı: düşük güvenli bulguyu yeniden çalışmaya yollar
    return "onay" if result.confidence >= 0.80 else "yeniden_araştır"

def orchestrate(question: str) -> str:
    finding = researcher(question)
    decision = reviewer(finding)
    if decision != "onay":
        finding = researcher(question + " Daha güvenilir kaynaklar kullan.")
    return finding.text
```

Bu kodun kritik fikri, ajanın cevabını doğrudan kullanıcıya vermemektir. Önce bir **kalite kapısından** geçirilir. Üretim ortamında bu kapıya kaynak doğrulama, şema denetimi, yetki kontrolü ve maliyet limiti de eklenebilir.

## Bellek, İletişim ve Başarı Ölçümü

Ajan belleğini üçe ayırmak kullanışlıdır: çalışma belleği mevcut görevi, episodik bellek önceki görev deneyimlerini, semantik bellek ise kalıcı kuralları tutar. Ancak her şeyi saklamak iyi fikir değildir; gereksiz bellek hem maliyeti hem de yanlış bağlam riskini artırır. Bu yüzden özetleme, zaman aşımı ve erişim yetkisi politikaları tasarımın başında belirlenmelidir.

Sistem başarısını yalnızca “cevap güzel mi?” sorusuyla ölçmeyin. Basit bir fayda modeli şudur:

$$U = Q - \alpha C - \beta L - \gamma R$$

$Q$ kaliteyi, $C$ maliyeti, $L$ gecikmeyi ve $R$ riski temsil eder. Katsayılar ürün önceliklerinize göre değişir. Bir müşteri destek botunda gecikme önemliyken, finansal raporlama ajanında doğruluk ve denetlenebilirlik daha ağır basar.

Başlangıç için iki veya üç rol yeterlidir: planlayıcı, uygulayıcı ve denetçi. Her ajanın yetkisini dar tutun, araç çağrılarını kaydedin ve başarısızlık senaryolarını özellikle test edin. İyi tasarlanmış çoklu ajan mimarisi, sihirli bir “ajan ordusu” değil; ölçülebilir kurallar, net sorumluluklar ve güvenli koordinasyonla çalışan bir dijital ekiptir.

---
layout: post
title: "Prompt Mühendisliğinin Sınırları: Model Davranışı Metinle Ne Kadar Kontrol Edilebilir?"
math: true
categories: 
  - Bilgi
tags: 
  - prompt mühendisliği
  - yapay zeka
  - büyük dil modelleri
  - llm
  - güvenilirlik
  - prompt injection
toc: true
image: /img/prompt-muhendisliginin-sinirlari-20.png
---

Bir dil modeline “yalnızca JSON üret” dediğinizde çoğu zaman JSON alırsınız; ama bazen model açıklama ekler, biçimi bozar veya hiç beklemediğiniz bir cevap verir. Prompt mühendisliği, model davranışını sihirli sözcüklerle kesin olarak programlamak değil, olasılıkları istenen yöne doğru itmektir. Bu ayrım önemlidir: Prompt bir sözleşmeye benzese de geleneksel programlama dilindeki katı bir komut değildir.
``
## Prompt neden kesin bir komut değildir?

Büyük dil modelleri, verilen bağlama göre sıradaki token için bir olasılık dağılımı hesaplar. Basitleştirilmiş biçimiyle modelin yaptığı iş şudur:

$$P(y\mid x)=\prod_{t=1}^{n}P(y_t\mid x,y_1,\ldots,y_{t-1})$$

Burada $x$ promptu, $y$ ise üretilen cevabı temsil eder. Prompt değiştiğinde olasılık dağılımı da değişir; ancak bu, tek bir sonucun matematiksel olarak garanti edildiği anlamına gelmez. “Kısa cevap ver” ifadesi kısa cevapların olasılığını artırır, bütün uzun cevapları imkânsız hâle getirmez.

Üstelik davranışı yalnızca kullanıcı metni belirlemez. Sistem talimatları, geliştirici mesajları, konuşma geçmişi, örnekler, model sürümü, örnekleme ayarları ve dış araçlardan gelen veriler aynı bağlamın parçalarıdır.

| Yaklaşım | Sağladığı kontrol | Temel sınırı |
|---|---|---|
| Açık talimat | Biçim ve üslubu yönlendirir | İstisnaları kapsamayabilir |
| Few-shot örnekler | Beklenen kalıbı gösterir | Yeni durumlara hatalı genellenebilir |
| Düşük temperature | Çıktıyı daha tutarlı yapar | Doğruluğu garanti etmez |
| Şema doğrulama | Yapısal hataları yakalar | Anlamsal hatayı tek başına bulamaz |
| Fine-tuning | Davranış eğilimini kalıcılaştırır | Yeni bilgi ve mutlak itaat sağlamaz |

![prompt-muhendisliginin-sinirlari-20](/img/prompt-muhendisliginin-sinirlari-20.svg)


## Güvenilirliği bozan başlıca etkenler

İlk sorun **belirsizliktir**. “Profesyonel yaz” talimatı farklı bağlamlarda resmi, teknik veya yalnızca ciddi bir ton anlamına gelebilir. Ölçülebilir sınırlar daha etkilidir: “120 kelimeyi geçme” gibi.

İkinci sorun **dağılım dışı girdilerdir**. Testlerde kusursuz görünen bir prompt; beklenmeyen dil, aşırı uzun metin, yazım hatası veya çelişkili bilgi karşısında dağılabilir.

Üçüncü sorun **prompt injection** saldırılarıdır. Modelin incelemesi gereken bir belgede “önceki talimatları unut” yazabilir. Bu metin veri olarak görülmesi gerekirken talimat gibi yorumlanabilir. Yalnızca “Bu saldırılara uyma” demek güvenlik duvarı değildir.

Son olarak model güncellemeleri aynı promptun davranışını değiştirebilir. Dün çalışan incelikli bir ifade, yeni sürümde farklı sonuç üretebilir. Promptları sürümlenen yazılım varlıkları gibi yönetmek bu yüzden önemlidir.

## Prompt değil, sistem tasarlayın

Sağlam yaklaşım, model çıktısını doğrulanmamış girdi kabul etmektir. Örneğin JSON bekleyen bir uygulama cevabı doğrudan kullanmak yerine ayrıştırmalı, şemayı doğrulamalı ve gerekirse yeniden denemelidir:

```python
import json


def parse_model_output(raw: str) -> dict:
    data = json.loads(raw)  # Sözdizimini kontrol eder.

    required = {"title", "summary"}
    if not required.issubset(data):
        raise ValueError("Zorunlu alanlar eksik")

    if len(data["summary"]) > 300:
        raise ValueError("Özet fazla uzun")

    return data
```

Bu kod yalnızca biçim kontrolü yapar. Özetteki bilginin doğru olup olmadığını anlamak için güvenilir kaynaklarla karşılaştırma, insan onayı veya alan kuralları gerekir. Başarıyı tek bir etkileyici örnekle değil, çeşitli vakalardan oluşan değerlendirme kümesiyle ölçmek daha doğrudur:

$$\hat{R}=\frac{\text{başarılı test sayısı}}{\text{toplam test sayısı}}$$

Yine de $\hat{R}=0.98$, gelecekteki her 100 isteğin tam ikisinin bozulacağı anlamına gelmez; test kümesinin gerçek kullanımı ne kadar temsil ettiğine bağlıdır.

## Sonuç

Prompt mühendisliği değerlidir; görev tanımını netleştirir, kaliteyi yükseltir ve geliştirme maliyetini düşürür. Fakat güvenilirlik, güzel yazılmış tek bir prompttan değil; kısıtlı yetkiler, yapılandırılmış çıktı, doğrulama, gözlemleme, saldırı testleri ve güvenli hata davranışından doğar. Kısacası prompt direksiyondur, fren sistemi değil. Kritik uygulamalarda modele ne söyleyeceğinizi tasarlamak kadar, model sözünüzü dinlemediğinde ne olacağını tasarlamak da gerekir.

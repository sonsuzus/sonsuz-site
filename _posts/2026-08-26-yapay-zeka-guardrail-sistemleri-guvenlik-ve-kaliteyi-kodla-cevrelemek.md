---
layout: post
title: "Yapay Zeka Guardrail Sistemleri: Güvenlik ve Kaliteyi Kodla Çevrelemek"
math: true
categories: 
  - Bilgi
tags: 
  - yapay zeka
  - guardrails
  - llm güvenliği
---

Bir yapay zeka uygulamasının etkileyici cevaplar üretmesi tek başına başarı değildir; doğru bağlamda, güvenli sınırlar içinde ve tutarlı kalitede çalışması gerekir. Guardrail sistemleri, büyük dil modellerinin (LLM) girişlerini, araç kullanımını ve çıktılarını denetleyen koruyucu katmanlardır. Amaç modeli “sansürlemek” değil; kullanıcı, kurum verisi ve iş süreçleri için öngörülebilir bir çalışma alanı tanımlamaktır.

``

## Guardrail neden ayrı bir katmandır?

Bir LLM olasılıksal çalışır: sonraki kelimeyi, önceki bağlama göre seçer. Basitleştirilmiş biçimde modelin ürettiği yanıt şu olasılığı maksimize eder:

$$P(y \mid x, c)$$

Burada $x$ kullanıcı girdisi, $c$ sistem bağlamı ve $y$ yanıttır. Ancak en olası yanıt, her zaman en güvenli veya şirket politikasına en uygun yanıt değildir. Guardrail, bu üretim döngüsüne politika ve doğrulama sinyalleri ekler. Pratikte karar mekanizması şöyle düşünülebilir:

$$\text{Kabul} = \text{PolitikaUygunluğu} \land \text{Güvenlik} \land \text{Kalite}$$

Bu yaklaşım, “tek bir mükemmel prompt” beklentisinden daha dayanıklıdır. Çünkü saldırgan girdiler, model güncellemeleri ve yeni kullanım senaryoları zamanla değişir.

| Katman | Denetlediği alan | Örnek kontrol |
|---|---|---|
| Girdi guardrail’i | Kullanıcı mesajı | Prompt injection, kişisel veri, zararlı istek |
| Bağlam guardrail’i | RAG ve sistem verisi | Yetkisiz doküman veya kirli kaynak |
| Araç guardrail’i | API ve fonksiyon çağrıları | Para transferi için onay, SQL sorgu sınırı |
| Çıktı guardrail’i | Model yanıtı | Halüsinasyon, gizli bilgi, zararlı içerik |

## Girdi ve çıktı kontrollerini birlikte tasarlamak

Yalnızca giriş filtresi kullanmak yeterli değildir. Masum görünen bir soru, modelin hassas bir veriyi bağlamdan sızdırmasına yol açabilir. Benzer şekilde yalnızca çıktı filtresi de maliyetlidir; model zararlı bir isteği işlemek için gereksiz token harcamış olur. Bu nedenle erken reddetme, güvenli yürütme ve son doğrulama birlikte uygulanmalıdır.

Aşağıdaki Python örneği, basit fakat genişletilebilir bir akışı gösterir. Gerçek projede anahtar kelime listesini tek başına güvenlik çözümü saymak yerine, sınıflandırıcılar ve politika motorlarıyla desteklemek gerekir.

```python
SENSITIVE_TERMS = {"api anahtarı", "şifre", "kart numarası"}


def input_guardrail(message: str) -> tuple[bool, str]:
    normalized = message.lower()
    if any(term in normalized for term in SENSITIVE_TERMS):
        return False, "Hassas bilgi içeren isteği işleyemem."
    if "sistem talimatlarını görmezden gel" in normalized:
        return False, "Talimat manipülasyonu algılandı."
    return True, message


def output_guardrail(answer: str) -> str:
    # Üretim ortamında burada PII taraması ve politika sınıflandırması eklenir.
    if "KESİN TIBBİ TANI" in answer.upper():
        return "Bu bilgi tıbbi tanı yerine geçmez; bir uzmana danışın."
    return answer


def safe_chat(message: str, llm) -> str:
    allowed, result = input_guardrail(message)
    if not allowed:
        return result

    draft = llm.generate(result)
    return output_guardrail(draft)
```

Bu kodda `input_guardrail`, model çağrısından önce riskli isteği durdurur. `output_guardrail` ise modelin ürettiği taslağı son kez inceler. Kritik nokta, reddetme mesajlarının da güvenli ve kullanıcıyı yönlendiren bir dil taşımasıdır.

## Kaliteyi ölçülebilir hale getirmek

Guardrail başarısı “filtre çalıştı” demek değildir. Yanlış pozitif oranı ($FP$), yanlış negatif oranı ($FN$), gecikme ve kullanıcı memnuniyeti birlikte izlenmelidir. Özellikle duyarlılık ve kesinlik faydalı iki metriktir:

$$Precision = \frac{TP}{TP+FP}, \qquad Recall = \frac{TP}{TP+FN}$$

Aşırı katı bir sistem yüksek güvenlik sağlarken meşru talepleri engelleyebilir. Fazla gevşek sistem ise riskli içeriği kaçırır. Bu nedenle politikaları sürümleyin, deneme veri setleri oluşturun ve her politika değişikliğini saldırı örnekleriyle test edin.

Son olarak, guardrail’i yalnızca modelin çevresindeki bir duvar gibi görmeyin. Loglama, kullanıcı geri bildirimi, insan onayı ve en az yetki ilkesiyle birleştiğinde guardrail; yapay zeka ürününüzün fren sistemi değil, güvenle hızlanmasını sağlayan yol tutuş sistemidir.

---
layout: post
title: "Prompt Chaining: Karmaşık Yapay Zeka Görevlerini Adım Adım Çözme Sanatı"
math: true
categories: 
  - Bilgi
tags: 
  - yapay zeka
  - prompt engineering
  - LLM
  - otomasyon
---

Bir büyük dil modelinden tek seferde kapsamlı bir rapor yazmasını, verileri analiz etmesini, kaynakları denetlemesini ve sonucu belirli bir formatta sunmasını istemek caziptir. Ancak bu yaklaşım çoğu zaman belirsiz, tutarsız veya kolayca doğrulanamayan çıktılar üretir. **Prompt chaining**, büyük bir hedefi birbirini besleyen küçük istemlere ayırarak bu sorunu azaltan tekniktir. Zincirde her adım, önceki adımın çıktısını girdi olarak kullanır; böylece görev hem denetlenebilir hem de yeniden üretilebilir hâle gelir.
``
## Neden tek dev prompt her zaman iyi çalışmaz?

Dil modelleri metin üretiminde güçlüdür; fakat uzun talimat listelerinde bazı koşulları ikinci plana atabilir. Ayrıca araştırma, sınıflandırma, hesaplama ve yazım gibi farklı bilişsel işleri aynı anda istemek hata olasılığını artırır. Prompt chaining'in temel fikri, problemi fonksiyonlara ayırmaya benzer:

$$
G = f_n(f_{n-1}(...f_2(f_1(x))))
$$

Burada $x$ ham girdiyi, $f_i$ zincirdeki bir adımı, $G$ ise nihai çıktıyı temsil eder. Her fonksiyonun tek ve açık bir sorumluluğu olmalıdır. Bu yaklaşım yazılımdaki **single responsibility principle** ile akrabadır.

| Yaklaşım | Avantajı | Riski |
|---|---|---|
| Tek büyük prompt | Hızlı kurulur, az çağrı yapar | Talimat çakışması ve denetim zorluğu |
| Prompt chain | Ara sonuçlar görünür, hata ayıklama kolaydır | Daha fazla tasarım ve çağrı gerekir |
| Agent yapısı | Dinamik karar verebilir | Maliyet, kontrol ve karmaşıklık artar |

## Sağlam bir zincirin anatomisi

İyi bir zincir genellikle dört aşamadan oluşur: **ayrıştırma**, **üretim**, **doğrulama** ve **sunum**. Örneğin “müşteri geri bildirimlerinden ürün yol haritası çıkar” görevini ele alalım. İlk prompt yorumları tema, duygu ve önem derecesine göre yapılandırılmış JSON'a dönüştürür. İkinci prompt bu veriden öncelik önerileri üretir. Üçüncü prompt ise çelişki, kanıtsız iddia veya eksik veri arar. Son aşama, denetlenmiş sonucu yöneticilere uygun Markdown raporuna çevirir.

Ara çıktıları serbest metin yerine şemalı veri olarak tutmak zinciri ciddi biçimde güçlendirir. Çünkü sonraki adım neyi beklediğini açıkça bilir. Örneğin:

```json
{
  "tema": "performans",
  "duygu": "olumsuz",
  "kanıt": "Uygulama açılırken çok bekliyorum.",
  "adet": 12,
  "guven": 0.86
}
```

Bu yapıdaki `guven` alanı mutlak gerçek değildir; modelin tahminine dair bir işarettir. Kritik kararlarda düşük güvenli kayıtlar insan inceleme kuyruğuna gönderilebilir.

## Bağlamı taşıyın, çöpü taşımayın

Zincir tasarımında en önemli denge, sonraki adıma yeterli bağlamı vermek ama tüm konuşma geçmişini kopyalamamaktır. Gereksiz bağlam maliyeti yükseltir ve modelin dikkatini dağıtır. Bunun yerine her aşamanın sonunda kısa bir durum özeti, yapılandırılmış çıktı ve açık kabul kriterleri üretin.

Aşağıdaki Python benzeri örnek, üç adımlı akışı gösterir:

```python
analiz = llm("Yorumları temalara ayır. Sadece JSON döndür.", yorumlar)
oncelik = llm("Bu JSON'a göre etki/efor matrisi oluştur.", analiz)
rapor = llm("Önerileri kanıtlarıyla Markdown rapora dönüştür.", oncelik)
```

Gerçek projede `analiz` çıktısının JSON şemasına uyup uymadığını ayrıca doğrulamalısınız. Başarısızsa modele aynı isteği körlemesine tekrar göndermek yerine, doğrulama hatasını ileten bir **repair prompt** kullanın. Örneğin: “`adet` alanı sayı olmalı; aşağıdaki çıktıyı şemaya uygun biçimde düzelt.”

## Kaliteyi ölçmek için kontrol noktaları ekleyin

Her zincir adımı için ölçülebilir başarı koşulları tanımlayın: kaynak alıntısı var mı, tüm zorunlu alanlar dolu mu, öneri ham verideki kanıtla destekleniyor mu? Basit bir kalite puanı şöyle modellenebilir:

$$
Q = 0.4D + 0.35T + 0.25F
$$

Burada $D$ doğruluk, $T$ tutarlılık, $F$ ise format uygunluğudur. Katsayılar ürün riskine göre değişir; hukuki veya tıbbi içerikte doğruluk katsayısı çok daha yüksek olmalıdır.

Sonuç olarak prompt chaining, modeli sihirli bir cevap makinesi gibi değil, uzmanlığı adımlara ayrılmış bir iş akışı motoru gibi kullanmanızı sağlar. Küçük, test edilebilir ve açık sorumluluklara sahip promptlar; özellikle raporlama, veri çıkarımı, içerik üretimi ve kod inceleme görevlerinde daha güvenilir sonuçların anahtarıdır.

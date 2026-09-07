---
layout: post
title: "Yapay Zekâ İmalı Konuşunca Şaşırıyor: Duygu Analizinde Sarkazm, Mecaz ve İroni"
math: true
categories: 
  - Bilgi
tags: 
  - duygu analizi
  - doğal dil işleme
  - yapay zekâ
toc: true
---

Bir forum kullanıcısı “Harika, uygulama yine çöktü; tam da ihtiyacım olan şeydi!” yazdığında insan zihni olumsuzluğu hemen sezer. Duygu analizi modeli ise “harika” ve “ihtiyacım olan” ifadelerine bakarak yorumu olumlu sınıflandırabilir. Çünkü sarkazm, mecaz ve ironi, sözcüklerin sözlük anlamıyla konuşanın gerçek niyeti arasına görünmez bir mesafe koyar.

``

## Duygu analizi aslında neyi ölçer?

Duygu analizi, bir metni genellikle **olumlu**, **olumsuz** veya **nötr** sınıflarından birine atayan doğal dil işleme problemidir. Bir sınıflandırıcı, metin $x$ verildiğinde en olası duygu etiketini seçmeye çalışır:

$$y^* = argmax_y P(y \vert  x)$$

Ancak burada kritik soru şudur: $x$ yalnızca yorumun kelimeleri midir, yoksa önceki mesajlar, yazarın alışkanlıkları, forum kültürü ve konuşulan olay da girdiye dâhil midir? Pratikte modellerin çoğu sınırlı bir metin penceresi görür. İnsan ise aynı ifadeyi sosyal bilgilerle birlikte değerlendirir.

| İfade | Yüzeyde görünen | Bağlama göre gerçek duygu |
|---|---|---|
| “Mükemmel, üç saatim boşa gitti.” | Olumlu | Olumsuz, sarkastik |
| “Bu bilgisayar kaplumbağa gibi.” | Hayvan benzetmesi | Yavaşlık eleştirisi |
| “Ne kadar düşüncelisin!” | Övgü | Duruma göre ironik eleştiri |
| “Fena değil.” | Hafif olumsuzluk | Çoğu bağlamda ölçülü olumlu |

## Sarkazm neden algoritmaları ters köşeye yatırır?

Sarkazmda olumlu sözcükler olumsuz niyeti gizleyebilir. Geleneksel kelime tabanlı yöntemler her kelimeye bir duygu puanı verir ve toplamı hesaplar:

$$S = \sum_{i=1}^{n} w_i$$

“Harika” için $+2$, “çöktü” için $-1$ verildiğinde sonuç pozitif çıkabilir. Oysa ünlem işareti, beklentiyle gerçeklik arasındaki çelişki ve önceki konuşma mesajın yönünü değiştirir. Emoji kullanımı bile güvenilir değildir; “🙂” bazen samimiyet, bazen pasif agresiflik taşıyabilir.

## Mecaz ve ironi aynı problem mi?

Bu kavramlar akraba olsa da aynı değildir. Mecaz, anlamı başka bir kavram üzerinden kurar: “Sunucu bugün can çekişiyor.” İroni, söylenenle kastedilen arasında karşıtlık oluşturur. Sarkazm ise çoğunlukla alay veya eleştiri amacı taşıyan daha keskin bir ironi biçimidir.

| Zorluk | Modelin yanılma nedeni | Olası ipucu |
|---|---|---|
| Sarkazm | Olumlu kelime, olumsuz niyet | Çelişki ve abartı |
| Mecaz | Sözcükler gerçek anlamda yorumlanır | Kavramsal benzetme |
| İroni | Söylenen ile durum uyuşmaz | Konuşma geçmişi |
| Forum dili | Argo ve topluluğa özel şakalar | Kullanıcı ve alan bilgisi |

## Basit bir yaklaşım ve sınırları

Aşağıdaki örnek, olumlu ve olumsuz kelimeleri sayan küçük bir sınıflandırıcıdır. Kod, yüzeysel yöntemlerin sarkazm karşısında neden zorlandığını gösterir:

```python
positive = {"harika", "mükemmel", "iyi", "şahane"}
negative = {"kötü", "çöktü", "yavaş", "berbat"}

def sentiment(text):
    words = set(text.lower().replace("!", "").split())
    score = len(words & positive) - len(words & negative)
    if score > 0:
        return "olumlu"
    if score < 0:
        return "olumsuz"
    return "nötr"

print(sentiment("Mükemmel, sistem yine çöktü!"))
```

Noktalama temizliği de kusursuz olmadığı için bu kod üretim sistemi değildir; yalnızca kelime sayımının bağlamı temsil edemediğini görünür kılar.

## Daha güçlü modeller ne yapabilir?

Transformer tabanlı modeller, kelimeleri çevrelerindeki ifadelerle birlikte temsil eder. Yine de yalnızca tek yorumu görmek yeterli olmayabilir. Başarıyı artırmak için konuşma zinciri, yanıt verilen mesaj, konu başlığı, alan özelinde eğitim verisi ve sarkazm etiketleri kullanılabilir. Çok görevli öğrenmede model hem duyguyu hem de “sarkastik mi?” etiketini tahmin eder.

Buna rağmen kullanıcı geçmişi gibi veriler mahremiyet riski taşır. Ayrıca forum kültürü zamanla değişir; dün samimi olan bir kalıp bugün alaycı kullanılabilir. Bu nedenle doğruluk tek başına yeterli değildir. Hata analizi, sınıf bazlı F1 skoru, veri güncelliği ve insan denetimi birlikte değerlendirilmelidir. Kısacası duygu analizi yalnızca kelimeleri değil, insanların söylemediklerini de anlamaya çalışır; eğlence de zorluk da tam burada başlar.

---
layout: post
title: "Program Sentezi: Örneklerden Çalışan Kod Üretmenin Mantığı"
math: true
categories: 
  - Bilgi
tags: 
  - program sentezi
  - yapay zeka
  - kod üretimi
---

Program sentezi, bir programcının her satırı elle yazması yerine sistemin verilen niyetten, kısıtlardan veya giriş-çıkış örneklerinden çalışan bir program üretmesidir. İlk bakışta “yapay zekâ kod yazıyor” kadar sihirli görünür; fakat mutfakta oldukça somut fikirler vardır: arama, mantıksal çıkarım, istatistiksel öğrenme ve doğrulama. Amaç yalnızca örnekleri ezberleyen bir fonksiyon değil, daha önce görülmemiş girdilerde de doğru davranan genellenebilir bir program bulmaktır.
``

En temel biçimi **örneklerden sentez** yaklaşımıdır. Elimizde giriş-çıkış çiftleri olsun: `"merhaba dünya" → "Merhaba Dünya"` ve `"program sentezi" → "Program Sentezi"`. Sistem, bu dönüşümü açıklayan aday programlar üretir. Örneğin kelimeleri boşluklardan ayırıp her kelimenin ilk harfini büyüten, sonra tekrar birleştiren bir program doğru adaydır. Ancak yalnızca iki örneği saklayıp eşleştiren bir tablo da eğitim verisinde başarılı olur. İşte sentezin zor sorusu burada başlar: Hangisi gerçekten niyeti temsil ediyor?

Bu problem çoğunlukla bir arama problemi olarak yazılır. Bir program uzayı $\mathcal{P}$, örnek kümesi $E$ ve doğrulama koşulu $\varphi$ için hedef şöyledir:

$$p^* = \arg\min_{p \in \mathcal{P}} C(p) \quad \text{öyle ki} \quad \forall (x,y) \in E,\; p(x)=y$$

Buradaki $C(p)$ genellikle programın uzunluğu, karmaşıklığı veya çalışma maliyetidir. Daha kısa programı tercih etmek, Occam’ın usturasının kod dünyasındaki karşılığıdır: Gereksiz dallarla dolu bir çözüm yerine, aynı davranışı açıklayan sade kural aranır.

| Yaklaşım | Temel fikir | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| Enumerative synthesis | Olası ifadeleri sistematik dener | Basit ve güvenilir | Arama uzayı hızla patlar |
| Constraint-based synthesis | İstenen davranışı mantıksal kısıtlara çevirir | Doğrulaması güçlüdür | Kısıt modellemek zor olabilir |
| Neural synthesis | Model, kod olasılıklarını öğrenir | Büyük örüntülerde hızlı öneri | Hatalı kod üretebilir |
| CEGIS | Aday üretir, karşı örnekle düzeltir | Hataları hedefli azaltır | Karmaşık alanlarda maliyetlidir |

Pratikte sık kullanılan döngü **CEGIS**’tir: *Counterexample-Guided Inductive Synthesis*. Sistem önce örneklerle uyumlu bir aday üretir. Bir doğrulayıcı bu adayın tüm koşulları karşılayıp karşılamadığını sınar. Hata bulursa, hata yaratan girdi bir karşı örnek olarak sentezleyiciye geri verilir. Böylece “bu testleri geçtim” düzeyinden “bu sınıftaki hatalara düşmüyorum” düzeyine ilerlenir.

Aşağıdaki küçük Python örneği, sınırlı bir ifade dilinde adayları test eden oyuncak bir sentezleyicidir. Gerçek sistemler SAT/SMT çözücüleri kullanır; burada fikir görünür olsun diye aday listesi elle tanımlanmıştır.

```python
candidates = [
    lambda s: s.upper(),
    lambda s: s.lower(),
    lambda s: " ".join(word.capitalize() for word in s.split()),
]

examples = [
    ("merhaba dünya", "Merhaba Dünya"),
    ("pYtHoN rehberi", "Python Rehberi"),
]

for program in candidates:
    if all(program(inp) == out for inp, out in examples):
        print("Bulunan program:", program("program sentezi"))
        break
```

Bu kod, her adayın tüm örnekleri sağlayıp sağlamadığını `all` ile denetler. Bulduğu aday yeni girdi üzerinde de çalıştırılır. Elbette bu yaklaşımın başarısı aday diline bağlıdır: Dilinizde tarih dönüştürme yoksa, sentezleyici ne kadar akıllı olursa olsun o işlemi ifade edemez. Bu nedenle program sentezinde **domain-specific language (DSL)** tasarımı kritik bir adımdır.

Program sentezinin kullanım alanları şaşırtıcı derecede geniştir: elektronik tablo formülleri, veri temizleme dönüşümleri, API çağrı zincirleri, test üretimi, donanım tasarımı ve kod tamamlama bunlardan bazılarıdır. Büyük dil modelleri niyeti doğal dilden yakalamada çok başarılıdır; sembolik doğrulayıcılar ise “bu kod gerçekten güvenli mi?” sorusunda öne çıkar. En sağlam mimariler, yaratıcı öneri gücü ile biçimsel doğruluğu birleştirir.

Özetle program sentezi, kod üretmekten çok niyeti matematiksel ve hesaplanabilir bir biçimde yakalama disiplinidir. İyi örnekler, doğru kısıtlar ve güçlü doğrulama birleştiğinde bilgisayar yalnızca komutları uygulamaz; çözüm uzayında sizin adınıza mantıklı programlar keşfeder.

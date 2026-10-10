---
layout: post
title: "Akıllı Bir Kelime Öğrenme Sistemi Nasıl Tasarlanır?"
math: true
categories: 
  - Proje
tags: 
  - kelime öğrenme
  - aralıklı tekrar
  - anki
  - mochi
  - mnemosyne
  - python
toc: true
image: /img/akilli-bir-kelime-63.png
---

Bir kelimeyi bugün öğrenip yarın unutmak beynimizin küçük bir şakasıdır; kötü hafızadan çok, yanlış zamanda tekrar yapmanın sonucudur. AnkiWeb, Mochi ve Mnemosyne gibi sistemler bu sorunu **aralıklı tekrar** algoritmalarıyla çözer. Gelin benzer bir uygulamanın arkasındaki teoriyi, araçların farklı yaklaşımlarını ve çalışır durumdaki basit bir zamanlama algoritmasını birlikte inceleyelim.


![akilli-bir-kelime-63](/img/akilli-bir-kelime-63.svg)

``

## Aralıklı tekrar neden işe yarar?

Hermann Ebbinghaus’un unutma eğrisi, bir bilginin hatırlanma gücünün zamanla üstel biçimde azaldığını öne sürer. Basitleştirilmiş bir model şöyledir:

$$R(t) = e^{-t/S}$$

Burada $R(t)$ hatırlama olasılığını, $t$ son çalışmadan beri geçen süreyi, $S$ ise anının dayanıklılığını temsil eder. Aynı kelimeyi başarıyla hatırladıkça $S$ büyür; böylece tekrarlar arasındaki süre uzatılabilir.

Örneğin “serendipity” kelimesini ilk gün öğrendiğimizi düşünelim. İlk tekrar bir gün sonra, sonraki tekrar üç gün sonra, ardından sekiz veya on gün sonra yapılabilir. Amaç, kartı tamamen unutmadan hemen önce göstermektir. Çok erken tekrar zaman kaybettirir, çok geç tekrar ise öğrenme sürecini başa sarar.

## AnkiWeb, Mochi ve Mnemosyne karşılaştırması

Bu araçların ortak hedefi aynı olsa da kullanıcı deneyimleri ve veri modelleri farklıdır:

| Sistem | Güçlü yönü | İçerik yaklaşımı | Kimler için uygun? |
|---|---|---|---|
| AnkiWeb | Geniş eklenti ve deste sistemi | Ön yüz, arka yüz ve alanlar | Ayrıntılı kontrol isteyenler |
| Mochi | Temiz arayüz ve Markdown desteği | Notlar arasında bağlantılar | Not alma ile ezberi birleştirenler |
| Mnemosyne | Araştırma odaklı sade yapı | Klasik soru-cevap kartları | Dikkat dağıtmayan araç arayanlar |

Anki ekosistem ve özelleştirme konusunda öne çıkar. Mochi, kartları birbirine bağlayarak kişisel bilgi ağı kurmayı kolaylaştırır. Mnemosyne ise daha sade ve akademik bir yaklaşım sunar. Kısacası Anki bir kontrol paneli, Mochi dijital bahçe, Mnemosyne ise sakin bir çalışma masası gibidir.

## Temel veri modeli

Kendi sistemimizde her kart için kelime, anlam, örnek cümle, tekrar tarihi, kolaylık katsayısı ve tekrar sayısı saklanabilir. Ayrıca öğrenme yönünü değiştirmek yararlıdır: “apple → elma” kartı tanımayı, “elma → apple” kartı ise aktif hatırlamayı ölçer.

Basit bir kart modeli şu alanları içerebilir:

- `front`: Sorulan kelime veya ipucu
- `back`: Anlam ve örnek cümle
- `interval`: Bir sonraki tekrara kalan gün
- `ease`: Kartın kişisel zorluk katsayısı
- `due`: Gösterileceği tarih

## Basitleştirilmiş SM-2 zamanlayıcısı

Aşağıdaki Python fonksiyonu, kullanıcının 0 ile 5 arasındaki cevabına göre yeni tekrar aralığını hesaplar:

```python
def schedule_card(quality, repetitions, interval, ease):
    # 3'ten düşük puan, kartın hatırlanamadığını gösterir.
    if quality < 3:
        repetitions = 0
        interval = 1
    else:
        repetitions += 1

        if repetitions == 1:
            interval = 1
        elif repetitions == 2:
            interval = 6
        else:
            interval = round(interval * ease)

    # Başarılı cevap kolaylığı artırır, zor cevap azaltır.
    ease += 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    ease = max(1.3, ease)

    return repetitions, interval, ease

print(schedule_card(4, 2, 6, 2.5))
```

Fonksiyon kart unutulduğunda programı sıfırlar; doğru cevaplarda ise mevcut aralığı kolaylık katsayısıyla büyütür. $I_{yeni} = I_{eski} \times E$ ilişkisi, uzun vadede tekrar sayısını ciddi biçimde azaltır. Gerçek bir uygulamada saat dilimi, günlük kart sınırı, gecikmiş tekrarlar ve kullanıcı alışkanlıkları da hesaba katılmalıdır.

## İyi bir sistemin sırrı

Algoritma tek başına mucize yaratmaz. Kartlar kısa olmalı, tek bir bilgiyi sınamalı ve kelimeyi bağlam içinde göstermelidir. Görsel, ses kaydı ve gerçek bir örnek cümle hatırlamayı güçlendirir. En iyi araç; en gelişmiş formüle sahip olan değil, her gün açmayı unutmadığınız araçtır. Beş dakikalık düzenli tekrar, pazar gecesi yapılan iki saatlik kelime maratonunu çoğu zaman rahatça yener.

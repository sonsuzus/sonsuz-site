---
layout: post
title: "Pair Programming ve Öğrenme: İki Kişi Bir Ekrana Bakınca Ne Değişir?"
math: true
categories: 
  - Bilgi
tags: 
  - pair programming
  - yazılım geliştirme
  - öğrenme
  - iş birliği
  - kod inceleme
  - eğitim
toc: true
image: /img/pair-programming-ve-42.png
---

Tek başına kod yazarken zihnimizde küçük bir tiyatro döner: Kodu yazar, kontrol eder, hata yapar ve bazen aynı hataya on dakika boyunca şaşkınlıkla bakarız. Pair programming, yani eşli programlama, bu tiyatroya ikinci bir oyuncu ekler. İki geliştirici aynı problem üzerinde çalıştığında yalnızca iş bölümü yapılmaz; düşünme biçimleri görünür hâle gelir, geri bildirim hızlanır ve öğrenme sosyal bir sürece dönüşür.

``

## Direksiyonda kim var?

Klasik pair programming modelinde iki temel rol bulunur:

- **Driver**, klavyeyi kullanır ve o anda yazılması gereken koda odaklanır.
- **Navigator**, kodu gözlemler; olası hataları, tasarım kararlarını ve sonraki adımları düşünür.

Bu roller düzenli olarak değiştirilir. Böylece bir kişi sürekli anlatan öğretmene, diğeri de pasif öğrenciye dönüşmez. Driver uygulama pratiği kazanırken navigator problemi daha yüksek bir soyutlama seviyesinde değerlendirmeyi öğrenir.

| Tek başına programlama | Pair programming |
|---|---|
| Hata geri bildirimi gecikebilir | Hatalar yazılırken fark edilebilir |
| Düşünceler çoğunlukla iç sestir | Kararlar sözel olarak açıklanır |
| Bilgi tek kişide kalabilir | Bilgi ekip içinde yayılır |
| Odak kolay dağılabilir | Sosyal sorumluluk odağı artırabilir |
| Kişisel alışkanlıklar baskındır | Alternatif yaklaşımlar görülür |

![pair-programming-ve-42](/img/pair-programming-ve-42.svg)


## Öğrenmenin arkasındaki mekanizma

Pair programming'in eğitsel gücü, yalnızca “iki çift göz daha iyidir” düşüncesinden gelmez. Asıl fark, zihinsel süreçlerin dışarı çıkarılmasıdır. Bir geliştirici “Burada neden bir sözlük kullandın?” diye sorduğunda driver kararını açıklamak zorunda kalır. Bu açıklama, bilginin yeniden düzenlenmesini sağlar. Eğitim bilimlerinde buna yakın etki, bir konuyu başkasına anlatırken daha iyi öğrenmemizi ifade eden **üretici öğrenme** yaklaşımıyla açıklanabilir.

Basitleştirilmiş bir öğrenme modeli şöyle gösterilebilir:

$$L = P \times F \times R$$

Burada $L$ öğrenme kazanımını, $P$ aktif katılımı, $F$ geri bildirimin hızını, $R$ ise düşünme ve açıklama tekrarını temsil eder. Pair programming bu üç değişkeni de artırabilir. Ancak taraflardan biri bütün işi yaparsa $P$ değeri diğer kişi için düşer; dolayısıyla yalnızca aynı ekrana bakmak öğrenme garantisi değildir.

Bilişsel yük açısından da ilginç bir paylaşım gerçekleşir. Driver sözdizimi ve uygulamayla uğraşırken navigator mimariyi ve uç durumları takip edebilir. Fakat sürekli konuşmak veya her satırı tartışmak gereksiz yük oluşturabilir. İyi bir eşleşmede iletişim, kodun önüne geçmez; kodu anlaşılır kılar.

## Küçük bir örnek

Aşağıdaki Python fonksiyonu bir listedeki tekrarları kaldırırken sırayı korur:

```python
def unique_items(items):
    seen = set()
    result = []

    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result
```

Driver bu kodu yazarken navigator şu soruları sorabilir: “Neden doğrudan `set(items)` kullanmıyoruz?”, “Elemanlar hash edilebilir değilse ne olur?” veya “Bellek maliyeti nedir?” Bu sorular kodu durdurmak için değil, gizli varsayımları görünür kılmak içindir. Driver da `set(items)` kullanımının özgün sırayı koruma niyetini yeterince açık anlatmayabileceğini fark eder.

## Her eşleşme verimli midir?

Hayır. Deneyim farkı çok büyükse kıdemli geliştirici klavyeyi ele geçirip canlı yayın yapan bir sihirbaza dönüşebilir. Öğrenen kişi ise yalnızca hızla akan sembolleri izler. Bunu önlemek için roller 15–25 dakikada bir değiştirilmeli, navigator doğrudan komut vermek yerine düşündürücü sorular sormalı ve oturumun hedefi başta belirlenmelidir.

| Verimsiz davranış | Öğrenmeyi destekleyen alternatif |
|---|---|
| “Şunu yaz, sonra buna tıkla” | “Burada hangi veri yapısı uygun olabilir?” |
| Klavyeyi sürekli tek kişinin kullanması | Zaman kutulu rol değişimi |
| Her ayrıntıyı anında düzeltmek | Önce düşünme süresi tanımak |
| Yalnızca görevi bitirmeye odaklanmak | Oturum sonunda çıkarımları özetlemek |

Pair programming bazen kısa vadede yavaş hissettirebilir; sonuçta tek klavyede iki maaş oturuyordur. Buna karşılık bilgi paylaşımı, erken hata yakalama ve kararları açıklama alışkanlığı uzun vadede güçlü bir öğrenme ortamı yaratır. İki kişi bir ekrana baktığında değişen şey piksel sayısı değil, düşüncenin artık yalnız kalmamasıdır.

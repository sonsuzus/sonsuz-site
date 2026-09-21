---
layout: post
title: "Pattern Matching’in Evrimi: switch İfadelerinden Yapısal Eşleşmeye"
math: true
categories: 
  - Bilgi
tags: 
  - pattern matching
  - switch
  - yapısal eşleşme
  - programlama dilleri
  - algoritma
  - python
toc: true
image: /img/pattern-matchingin-evrimi-94.png
---

Programlamada karar vermek uzun süre “Bu değer kaç?” sorusuna cevap aramak demekti. Ancak modern uygulamalarda değerler; listelerden, nesnelerden, ağaçlardan ve iç içe geçmiş veri yapılarından oluşuyor. Bu nedenle diller de basit `switch` ifadelerinden, verinin hem biçimini hem içeriğini inceleyebilen pattern matching yaklaşımına evrildi. Başka bir deyişle artık yalnızca kutunun etiketine değil, kutunun içine ve düzenine de bakıyoruz.


![pattern-matchingin-evrimi-94](/img/pattern-matchingin-evrimi-94.svg)

``

## Klasik switch: Değeri seç, dalı çalıştır

Geleneksel `switch`, bir ifadeyi sabit değerlerle karşılaştırır. Mantıksal olarak bunu bir fonksiyon gibi düşünebiliriz:

$$f(x) = \begin{cases} A, & x = a \\ B, & x = b \\ C, & diğer \end{cases}$$

Örneğin C# ile bir HTTP durum kodunu yorumlayalım:

```csharp
string Mesaj(int kod)
{
    switch (kod)
    {
        case 200:
            return "Her şey yolunda!";
        case 404:
            return "Kaynak bulunamadı.";
        case 500:
            return "Sunucu biraz üzgün.";
        default:
            return "Bilinmeyen durum.";
    }
}
```

Bu kod okunaklıdır ve derleyici bazı durumlarda hızlı bir atlama tablosu üretebilir. Fakat `kod` bir sayı yerine kullanıcı, sipariş veya sözdizimi ağacı olsaydı yalnızca eşitlik kontrolü yetersiz kalırdı.

## Pattern matching neyi değiştiriyor?

Pattern matching, bir değerin belirli bir **desene** uyup uymadığını sınar. Bir desen; sabit değer, tür, alanlar, liste uzunluğu veya bunların birleşimi olabilir. Temel ilişkiyi şöyle gösterebiliriz:

$$match(v, p) \rightarrow (başarılı, bağlam)$$

Buradaki `v` incelenen değer, `p` desen, bağlam ise eşleşme sırasında elde edilen değişkenlerdir. Örneğin `(x, y)` deseni bir çiftle eşleştiğinde, parçaları otomatik olarak `x` ve `y` isimlerine bağlar. Böylece kontrol ve veri çıkarma aynı işlemde gerçekleşir.

| Yaklaşım | Neyi inceler? | Veri çıkarabilir mi? | Tipik kullanım |
|---|---|---:|---|
| `if/else` | Her türlü koşul | Elle | Karmaşık mantıksal kontroller |
| Klasik `switch` | Genellikle sabit değer | Hayır | Menü, durum kodu, enum |
| Tür deseni | Değerin türü | Evet | Polimorfik nesneler |
| Yapısal eşleşme | İç yapı ve parçalar | Evet | JSON, AST, liste ve kayıtlar |

## Yapısal eşleşme sahneye çıkıyor

Python 3.10 ile gelen `match`, iç içe veri yapılarını oldukça doğal biçimde ayrıştırabilir:

```python
def komutu_isle(komut):
    match komut:
        case {"islem": "topla", "sayilar": [a, b]}:
            return a + b
        case {"islem": "yaz", "metin": str(metin)}:
            return metin.upper()
        case {"islem": "hareket", "konum": [x, y]} if x >= 0 and y >= 0:
            return f"Yeni konum: {x}, {y}"
        case _:
            return "Geçersiz komut"
```

İlk desen, sözlükte belirli anahtarların bulunmasını ve `sayilar` alanının tam iki elemanlı olmasını ister. Aynı anda elemanları `a` ve `b` değişkenlerine çıkarır. Üçüncü dalda kullanılan `if` ise **guard** olarak adlandırılır: Yapı eşleşse bile ek koşul sağlanmadığında dal çalışmaz.

## Neden sadece daha kısa bir if zinciri değil?

Yapısal eşleşmenin önemli avantajı, programın veri modelini görünür kılmasıdır. Özellikle derleyicilerde kullanılan soyut sözdizimi ağaçlarında işlemler desenlerle rahatça ifade edilir:

```python
def hesapla(ifade):
    match ifade:
        case ("sayi", n):
            return n
        case ("topla", sol, sag):
            return hesapla(sol) + hesapla(sag)
        case ("carp", sol, sag):
            return hesapla(sol) * hesapla(sag)
```

Bu örnek, ağacın düğümlerini ayrıştırırken özyinelemeli hesaplama yapar. Geleneksel yaklaşımda indeks kontrolleri, tür sorguları ve geçici değişkenler gerekebilirdi.

## Evrimin sonucu

Modern pattern matching; sabit karşılaştırma, tür kontrolü, parçalama ve koşullu doğrulamayı tek bir okunabilir yapı altında birleştirir. Yine de her yerde kullanılmamalıdır: Basit bir Boolean koşul için `if`, birkaç sabit seçenek için klasik `switch` hâlâ daha anlaşılır olabilir. İyi seçim şu soruya bağlıdır: “Bir değeri mi karşılaştırıyorum, yoksa bir veri biçimini mi tanıyorum?” İkinci sorunun cevabı evetse, yapısal eşleşme kodun İsviçre çakısı olmaya adaydır.

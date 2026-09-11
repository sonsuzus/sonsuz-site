---
layout: post
title: "Algoritmalar Patentlenebilir mi? Bilişim Hukuku ve Özgür Yazılımın İtirazı"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma patentleri
  - bilişim hukuku
  - özgür yazılım
toc: true
---

Bir algoritma, bilgisayara ne yapacağını söyleyen adımlar dizisidir; fakat aynı zamanda matematiksel düşüncenin uygulanmış hâlidir. Bu ikili kimlik önemli bir hukuk sorusu doğurur: Bir şirket, belirli bir hesaplama yöntemini patentleyerek başkalarının aynı mantığı kullanmasını engelleyebilir mi? Tartışma yalnızca hukukçuları değil, yazılımcıları, girişimcileri ve özgür yazılım savunucularını da yakından ilgilendirir.
``

## Algoritma neden matematiksel kabul edilir?

Algoritma, girdiyi belirli kurallarla çıktıya dönüştüren sonlu bir prosedürdür. Bunu soyut biçimde

$$f: X \rightarrow Y$$

fonksiyonu olarak düşünebiliriz. Örneğin bir sıralama algoritması, sayı dizisini girdi olarak alır ve aynı elemanların düzenlenmiş hâlini üretir. Temel amaç şu koşulu sağlamaktır:

$$a_1 \leq a_2 \leq \cdots \leq a_n$$

Bu ifade doğanın maddi bir ürününden çok matematiksel bir ilişkidir. Dolayısıyla “küçük olanı önce yerleştir” kuralının tekelleştirilmesi, Pisagor teoreminin kullanımını izne bağlamak kadar tuhaf görünebilir.

Ancak hukuk, soyut algoritma ile teknik etki üreten bilgisayar destekli buluşu her zaman aynı değerlendirmez. Patent başvurusu yalnızca formülü değil; yeni, buluş basamağı içeren ve sanayiye uygulanabilir bir teknik çözümü hedefliyorsa tartışmanın rengi değişir.

| Unsur | Genellikle patent dışı yaklaşım | Patent tartışmasına açık yaklaşım |
|---|---|---|
| Matematiksel formül | Soyut bilgi ve keşif | Teknik sistemin parçası olabilir |
| Algoritma | Zihinsel veya mantıksal yöntem | Ölçülebilir teknik etki üretebilir |
| Kaynak kodu | Çoğunlukla telif hakkıyla korunur | Tek başına patent sayılmaz |
| Cihazla bütünleşme | Basitçe “bilgisayarda çalışır” demek yetersizdir | Donanım, enerji veya iletişim sorununu çözebilir |

## Fikir, kod ve patent arasındaki sınır

Telif hakkı kodun ifade biçimini korur; patent ise koşulları sağlandığında yöntemin uygulanmasını kapsayabilir. Aynı işlevi farklı kodla yazmak telif ihlalini önleyebilirken patent ihlalini mutlaka önlemez.

```python
def ikili_arama(veri, hedef):
    sol, sag = 0, len(veri) - 1
    while sol <= sag:
        orta = (sol + sag) // 2
        if veri[orta] == hedef:
            return orta
        if veri[orta] < hedef:
            sol = orta + 1
        else:
            sag = orta - 1
    return -1
```

Bu kod, sıralı bir listede arama alanını her turda yarıya indirir. Yaklaşık çalışma maliyeti $O(\log n)$ olur. Kod satırları belirli bir ifade olduğundan telifle ilişkilidir; fakat “arama uzayını ikiye bölme” fikri soyut matematiksel yöntemdir. Patent sorunu, bu fikrin özgün bir teknik uygulamayla birleştirilmesi hâlinde belirginleşir.

Avrupa patent yaklaşımında bilgisayar programları “kendiliğinden” patentlenebilir kabul edilmez; teknik karakter ve ilave teknik etki aranır. Amerika Birleşik Devletleri’nde de soyut fikirlerin yalnızca genel amaçlı bir bilgisayarda uygulanması çoğu durumda yeterli değildir. Yine de ülkeye ve somut istemlere göre sonuç değişebileceğinden kesin bir küresel kuraldan söz edilemez.

## Özgür yazılım hareketinin felsefi itirazı

Özgür yazılım hareketi meseleyi yalnızca ücretsiz yazılım açısından ele almaz. Temel tez, kullanıcının programı çalıştırma, inceleme, değiştirme ve paylaşma özgürlüğüdür. Richard Stallman’ın yaklaşımında kaynak kodu toplumsal bilgi birikiminin parçasıdır; algoritma patentleri ise bağımsız olarak aynı fikre ulaşan geliştiriciyi bile kısıtlayabilir.

Bu itiraz üç noktada yoğunlaşır:

1. **Bilgi kümülatiftir:** Yazılım, önceki algoritmaların birleştirilmesiyle gelişir.
2. **Bağımsız keşif savunma değildir:** Bir geliştirici patenti hiç görmeden ihlal riskiyle karşılaşabilir.
3. **İşlem maliyeti yüksektir:** Patent araştırması ve dava riski küçük projeleri orantısız etkiler.

Patent savunucuları ise geçici tekelin araştırma yatırımını teşvik ettiğini ve açıklanan buluşların kamusal bilgiye dönüştüğünü söyler. Karşı taraf, yazılım sektöründe hızlı yenilik döngüsü ve telif koruması nedeniyle bu teşvikin faydadan çok engel yaratabileceğini savunur.

Sonuçta sorun “algoritma patentlenir mi?” kadar basit değildir. Asıl soru, talep edilen hakkın soyut matematiksel düşünceyi mi yoksa gerçekten yeni bir teknik çözümü mü kapsadığıdır. Hukukun görevi, mucidi ödüllendirirken programlama dilinin ortak alfabesini özel mülke dönüştürmemektir.

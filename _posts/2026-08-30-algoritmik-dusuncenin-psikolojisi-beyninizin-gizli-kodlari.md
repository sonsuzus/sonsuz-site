---
layout: post
title: "Algoritmik Düşüncenin Psikolojisi: Beyninizin Gizli Kodları"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmik düşünme
  - problem çözme
  - psikoloji
  - yazılım mantığı
---

Sabah işe yetişmeye çalışırken en kısa rotayı seçmeniz, markette bütçenize göre ürünleri elemeniz veya kayıp anahtarınızı odaları sırayla kontrol ederek aramanız tesadüf değildir: beyniniz küçük algoritmalar çalıştırır. Algoritmik düşünme, yalnızca bilgisayar bilimcilerinin süper gücü değil; belirsiz bir hedefi adımlara, koşullara ve tekrar eden kalıplara dönüştürme becerisidir. Yazılım öğrenmenin ilginç tarafı da şudur: Kod yazarken yeni bir mantık edinmekten çok, zaten kullandığınız zihinsel stratejileri görünür ve denetlenebilir hâle getirirsiniz.
``

## Beyin problemi nasıl parçalar?

Bir problemle karşılaştığımızda zihnimiz çoğu zaman dört temel hamle yapar: **ayrıştırma**, **örüntü tanıma**, **soyutlama** ve **adım adım çözüm tasarlama**. Örneğin “akşam yemeği hazırlama” görevi tek parça gibi görünür. Ancak deneyimli biri bunu malzeme kontrolü, tarif seçimi, hazırlık, pişirme ve servis gibi alt görevlere ayırır. Bu, yazılımdaki *decomposition* yani parçalama yaklaşımıdır.

Zihinsel enerji sınırlıdır. Bilişsel yük arttıkça, beynin kısa süreli belleği ayrıntıları taşımakta zorlanır. Bu nedenle iyi bir algoritma yalnızca doğru cevabı bulmaz; gereksiz kararları da azaltır. Kabaca çözüm maliyetini şöyle düşünebiliriz:

$$Toplam\ Maliyet = Zaman + Hata\ Riski + Bilişsel\ Yük$$

Gündelik hayatta sezgiler hızlıdır ama yanılabilir. Algoritmik yaklaşım ise biraz daha yavaş başlayıp sonucu daha güvenilir kılar. Özellikle tekrar eden işlerde bu fark büyür.

| Gündelik davranış | Zihinsel yapı | Yazılımdaki karşılığı |
|---|---|---|
| Dolapta tek tek ürün aramak | Sıralı kontrol | Linear search |
| “Yağmur varsa şemsiye al” demek | Koşullu karar | `if/else` |
| Her sabah aynı hazırlanma düzeni | Tekrarlanan işlem | Döngü |
| Önce en acil işi yapmak | Öncelik kuralı | Greedy yaklaşım |

## Sezgi, kurallar ve geri bildirim döngüsü

Beyin çoğu zaman kestirme yollara, yani *heuristic* yöntemlere başvurur. “En yakın kasaya git” hızlı bir kuraldır; fakat en kısa kuyruğu her zaman vermez. Algoritmik düşünme burada kritik bir soru sorar: **Kural hangi varsayımlar altında işe yarıyor?** Yazılımcının `if` koşulu yazması da tam olarak budur: kararın sınırlarını açıkça tanımlamak.

Bir görevin tekrarı, geri bildirim döngüsü oluşturur. Sonuç kötü ise kuralı güncellersiniz. Bu öğrenme mantığı aşağıdaki fikre benzer:

$$Yeni\ Strateji = Eski\ Strateji + Geri\ Bildirim$$

Elbette bu bir matematiksel modelden çok düşünme metaforudur. Ama önemli bir gerçeği taşır: Algoritmalar ilk denemede kusursuz olmak zorunda değildir; ölçülmeli, gözlemlenmeli ve iyileştirilmelidir.

## Bir gündelik problemi koda dönüştürmek

Diyelim ki yapılacak işler arasından en acil olanı seçmek istiyoruz. Önce işleri temsil eder, sonra öncelik değerine göre tararız. Aşağıdaki Python örneği, zihnimizdeki “en yüksek önceliği bul” kuralını açık hâle getirir:

```python
isler = [
    {"ad": "E-posta yanıtla", "oncelik": 2},
    {"ad": "Raporu teslim et", "oncelik": 5},
    {"ad": "Market alışverişi", "oncelik": 3}
]

en_acil = isler[0]
for is_ in isler:
    if is_["oncelik"] > en_acil["oncelik"]:
        en_acil = is_

print(f"Önce şunu yap: {en_acil['ad']}")
```

Kod, listedeki her işi bir kez inceler; bu yüzden zaman karmaşıklığı $O(n)$’dir. İnsan zihni de liste kısa olduğunda benzer bir tarama yapabilir. Liste büyüdüğünde ise not alma, etiketleme veya takvim kullanma gibi dış araçlar, belleğin yükünü azaltan veri yapıları gibi davranır.

| Yaklaşım | Avantaj | Risk |
|---|---|---|
| Sezgisel karar | Çok hızlıdır | Önyargıya açıktır |
| Açık adımlı algoritma | Tekrarlanabilir ve test edilebilirdir | Kurulması zaman alır |
| Hibrit yaklaşım | Hız ile tutarlılığı dengeler | Kuralların düzenli güncellenmesi gerekir |

Algoritmik düşünmenin amacı insanı robota çevirmek değildir. Asıl amaç, karmaşık anlarda “Şimdi hangi bilgiyi kullanıyorum, hangi kuralı izliyorum ve hata olursa nasıl düzelteceğim?” sorularını sorabilmektir. Bu sorulara alıştıkça gündelik kararlarınız daha şeffaf, yazdığınız programlar ise daha sağlam olur.

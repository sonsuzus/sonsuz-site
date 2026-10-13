---
layout: post
title: "NP-Zor Problemler ve P vs NP: Bilgisayar Biliminin Büyük Bulmacası"
math: true
categories: 
  - Bilgi
tags: 
  - karmaşıklık teorisi
  - p vs np
  - np-zor
  - algoritmalar
  - bilgisayar bilimi
  - optimizasyon
toc: true
image: /img/np-zor-problemler-52.png
---

Bir şehir turunda en kısa rotayı bulmak, sınav programını çakışmasız hazırlamak veya büyük bir lojistik ağını optimize etmek ilk bakışta sıradan görevler gibi görünebilir. Ancak girdi büyüdükçe bu problemlerin bazıları bilgisayarları adeta matematiksel bir bataklığa sürükler. Karmaşıklık teorisi, problemlerin ne kadar zor olduğunu ve kaynak ihtiyacının girdi boyutuyla nasıl değiştiğini inceler.

![np-zor-problemler-52](/img/np-zor-problemler-52.svg)

``
## Karmaşıklık neden önemlidir?

Bir algoritmanın çalışma süresini saniyeyle ölçmek yanıltıcıdır; sonuç işlemciye ve programlama diline göre değişebilir. Bunun yerine giriş boyutu $n$ büyürken gereken işlem sayısını inceleriz. Örneğin $O(n^2)$ süreli bir algoritmada veri iki katına çıktığında iş yükü yaklaşık dört katına çıkar.

Polinom zamanda çalışan algoritmalar genel olarak verimli kabul edilir:

$$T(n)=O(n^k)$$

Burada $k$ sabit bir sayıdır. Buna karşılık $O(2^n)$ veya $O(n!)$ gibi süreler küçük girdilerde bile hızla kontrolden çıkar. Örneğin $2^{100}$ olasılığın tamamını denemek, oldukça iyimser bir bilgisayarı bile uzun süre meşgul eder.

## P ve NP sınıfları

**P**, deterministik bir bilgisayar tarafından polinom zamanda çözülebilen karar problemlerinin sınıfıdır. Sıralama doğrudan bir karar problemi değildir; ancak “Bu listede değeri $x$ olan bir eleman var mı?” sorusu P içindedir.

**NP** ise verilen bir çözüm adayının doğruluğu polinom zamanda kontrol edilebilen karar problemlerini kapsar. Buradaki “NP”, “non-polynomial” değil, **nondeterministic polynomial time** ifadesinin kısaltmasıdır.

| Sınıf | Çözüm bulma | Aday çözümü doğrulama | Örnek |
|---|---|---|---|
| P | Polinom zamanda | Polinom zamanda | En kısa yolun belirli bir sınırdan kısa olması |
| NP | Hızlı yöntem bilinmeyebilir | Polinom zamanda | Gezgin satıcı karar problemi |
| NP-tam | NP içindeki en zor problemler | Polinom zamanda | SAT, 3-SAT |
| NP-zor | NP kadar veya daha zor | Hızlı doğrulama şart değil | Gezgin satıcının optimizasyon sürümü |

Her P problemi aynı zamanda NP içindedir; çünkü hızlıca bulunan bir sonuç hızlıca doğrulanabilir. Büyük soru bunun tersinin geçerli olup olmadığıdır:

$$P \stackrel{?}{=} NP$$

## Doğrulamak neden daha kolay olabilir?

Bir Sudoku çözmek zaman alabilir; fakat doldurulmuş tabloyu kontrol etmek kolaydır. Benzer şekilde, bir grafikte belirli uzunlukta Hamilton döngüsü verildiğinde bütün düğümlerin tam bir kez ziyaret edilip edilmediği hızla denetlenebilir.

```python
def rotayi_dogrula(rota, dugumler):
    # Her düğümün tam bir kez kullanıldığını kontrol eder.
    return len(rota) == len(dugumler) and set(rota) == set(dugumler)
```

Bu kod rotayı **bulmaz**; yalnızca sunulan adayın temel koşulu sağlayıp sağlamadığını doğrular. P ve NP arasındaki sezgisel fark tam olarak burada yatar: Bir cevabı tanımak, onu sıfırdan keşfetmekten çok daha kolay olabilir.

## NP-tam ve NP-zor ne demektir?

Bir problem hem NP içinde bulunuyor hem de NP’deki her problem ona polinom zamanda indirgenebiliyorsa **NP-tam** kabul edilir. İndirgeme, bir problemi başka bir problemin biçimine verimli şekilde dönüştürmektir. SAT’ın NP-tam olduğu Cook–Levin teoremiyle gösterilmiştir.

NP-zor problemler en az NP-tam problemler kadar zordur; ancak NP içinde olmak zorunda değildir. Karar sürümü “Maliyeti $K$ değerinden düşük tur var mı?” diye sorarken optimizasyon sürümü “En ucuz tur hangisi?” der. İkincisi genellikle NP-zor olarak sınıflandırılır.

| Yaklaşım | Kesin sonuç | Kullanım amacı |
|---|---:|---|
| Kaba kuvvet | Evet | Küçük girdiler |
| Dinamik programlama | Evet | Özel yapıdan yararlanma |
| Sezgisel algoritma | Garanti yok | Hızlı, iyi çözümler |
| Yaklaştırma | Belirli oranlarda | Büyük optimizasyon problemleri |

## P eşittir NP olursa ne olur?

Eğer $P=NP$ kanıtlanır ve pratik bir algoritma bulunursa çizelgeleme, ilaç tasarımı, lojistik ve otomatik ispat alanlarında büyük ilerlemeler yaşanabilir. Öte yandan birçok kriptografik sistem ciddi biçimde etkilenebilir. $P\ne NP$ kanıtı ise hızlı doğrulanabilen bazı problemlerin gerçekten hızlı çözülemeyeceğini gösterecektir.

2026 itibarıyla soru hâlâ açıktır ve Clay Matematik Enstitüsünün bir milyon dolarlık Milenyum Problemleri arasındadır. Şimdilik bildiğimiz şey şudur: Bazen bilgisayara doğru cevabı kontrol ettirmek kolay, o cevabı buldurmak ise evrendeki bütün kahveyi tüketebilecek kadar zordur.

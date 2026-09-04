---
layout: post
title: "SMT Çözücüleriyle Kısıt Programlama: Z3 ile Akıllı Arama ve Doğrulama"
math: true
categories: 
  - Bilgi
tags: 
  - smt
  - z3
  - kısıt programlama
image: /img/smt-cozuculeriyle-kisit-35.png
---

Karmaşık bir planı elle hazırlamak, binlerce olasılık içinden doğru kombinasyonu gözle seçmeye benzer: kısa süre sonra kahve biter, sabır biter, hata payı ise bitmez. SMT (Satisfiability Modulo Theories) çözücüleri bu noktada devreye girer. Z3 gibi araçlar, mantıksal kuralları ve matematiksel ilişkileri modele dönüştürerek bir problemin çözümü olup olmadığını otomatik biçimde araştırır; uygun olduğunda da somut bir çözüm üretir.

![smt-cozuculeriyle-kisit-35](/img/smt-cozuculeriyle-kisit-35.svg)

``

SMT'nin temelinde SAT problemi bulunur. SAT, yalnızca doğru/yanlış değerleri alan önermelerin aynı anda sağlanıp sağlanamayacağını sorar. Örneğin $A \lor B$ ve $\neg A$ ifadeleri birlikte sağlanabilir; çözüm olarak $A = false$, $B = true$ seçilir. SMT ise bu dünyayı genişletir: tamsayılar, reel sayılar, diziler, bit vektörleri, kümeler ve fonksiyonlar gibi teorileri mantıksal ifadelerle birleştirir. Böylece "iki görev aynı makinede çakışmasın" veya "bütçe 10.000'i geçmesin" gibi gerçek hayat kuralları ifade edilebilir.

| Yaklaşım | Güçlü yanı | Tipik kullanım |
|---|---|---|
| SAT | Çok hızlı Boole araması | Devre doğrulama, bağımlılık çözümü |
| SMT | Sayısal ve yapısal teoriler | Doğrulama, zamanlama, kaynak atama |
| Klasik optimizasyon | Amaç fonksiyonuna odaklıdır | Doğrusal programlama, maliyet azaltma |
| SMT tabanlı optimizasyon | Mantıksal koşullar + hedef | Karmaşık iş kuralları altında en iyi seçim |

Bir SMT modelinde önce **karar değişkenleri** tanımlanır. Ardından bu değişkenlerin uyması gereken **kısıtlar** eklenir. Son adımda çözücüden `sat` sonucu, yani çözüm olup olmadığı, istenir. Optimizasyon gerekiyorsa maliyet, süre veya risk gibi bir amaç fonksiyonu minimize ya da maksimize edilir. Matematiksel olarak fizibilite bölgesi şöyle düşünülebilir:

$$
\mathcal{F} = \{x \mid C_1(x) \land C_2(x) \land \dots \land C_n(x)\}
$$

Amaç en ucuz çözümü bulmaksa problem $\min_{x \in \mathcal{F}} f(x)$ biçimine dönüşür. Kritik ayrıntı şudur: Kısıtlar yalnızca lineer eşitsizliklerden oluşmak zorunda değildir. Koşullu kurallar, mantıksal çıkarımlar ve ayrık seçimler de modele doğal şekilde eklenebilir.

Aşağıdaki Python örneği, iki görevin başlangıç zamanını belirler. Görevler çakışamaz; ayrıca toplam bitiş zamanını mümkün olduğunca erkene çeker:

```python
from z3 import Int, Optimize, Or

basla_a = Int("basla_a")
basla_b = Int("basla_b")
sure_a, sure_b = 3, 5
bitis = Int("bitis")

cozucu = Optimize()
cozucu.add(basla_a >= 0, basla_b >= 0)
# A önce biter veya B önce biter: aynı anda makineyi kullanamazlar.
cozucu.add(Or(basla_a + sure_a <= basla_b,
              basla_b + sure_b <= basla_a))
cozucu.add(bitis >= basla_a + sure_a)
cozucu.add(bitis >= basla_b + sure_b)
cozucu.minimize(bitis)

if cozucu.check().r == 1:
    print(cozucu.model())
```

Buradaki `Or` ifadesi küçük görünse de güçlüdür: çözücü, iki olası sıralamayı da değerlendirebilir. Elle yazılmış bir algoritmada bu dallanmayı yönetmek gerekirken Z3, kısıt yayılımı ve akıllı arama teknikleriyle uygun dalı bulur. Elbette model büyüdükçe her şeyi "çözücüye bırakmak" sihirli değnek değildir; gereksiz simetri, zayıf sınırlar ve belirsiz değişken alanları performansı düşürür.

Doğrulama tarafında SMT daha da etkileyicidir. Bir güvenlik kuralının asla ihlal edilmediğini kanıtlamak için kuralın tersini çözücüye sorabilirsiniz. Örneğin $bakiye \ge 0$ olması gerekiyorsa, programın geçiş kurallarıyla birlikte $bakiye < 0$ kısıtını ekleyin. Sonuç `unsat` ise bu model altında ihlal mümkün değildir. Sonuç `sat` ise çözücünün verdiği model, çoğu zaman doğrudan hata senaryosudur.

| Sonuç | Anlamı | Sonraki adım |
|---|---|---|
| `sat` | En az bir model bulundu | Modeli çözüm veya karşı örnek olarak incele |
| `unsat` | Kısıtlar birlikte sağlanamaz | Kural çakışmalarını veya kanıtı değerlendir |
| `unknown` | Çözücü kesin karar veremedi | Teoriyi sadeleştir, zaman aşımını gözden geçir |

Başarılı bir SMT modeli, iyi isimlendirilmiş değişkenler, küçük ve test edilebilir kısıtlar, gerçekçi alt-üst sınırlar ile başlar. Önce fizibiliteyi doğrulayın, sonra optimizasyon ekleyin. Böylece Z3'ü yalnızca "cevap veren bir kara kutu" değil, tasarım hatalarını yakalayan mantıksal bir ekip arkadaşı hâline getirirsiniz.

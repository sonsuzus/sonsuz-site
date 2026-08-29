---
layout: post
title: "SMT Solver’lar Nasıl Çalışır? Program Doğrulamada Matematiksel Mantığın Gücü"
math: true
categories: 
  - Bilgi
tags: 
  - smt solver
  - program doğrulama
  - z3
  - matematiksel mantık
---

Bir programın her olası girdide güvenli çalıştığını kanıtlamak, yalnızca binlerce test yazmakla mümkün değildir. İşte bu noktada **SMT (Satisfiability Modulo Theories)** solver’ları devreye girer: Mantıksal formüllerin, tamsayı aritmetiği, diziler, bit vektörleri ve eşitlik gibi teoriler altında tutarlı olup olmadığını incelerler. Kısacası solver’a “Bu koşulları aynı anda sağlayan bir durum var mı?” diye sorarız; yanıt çoğu zaman programdaki hatayı ya da kanıtı ele verir.
``

SMT’nin temelinde **SAT problemi** bulunur. SAT solver, yalnızca doğru/yanlış değişkenlerinden oluşan bir formülün tatmin edilip edilemeyeceğini araştırır. Örneğin $A \land (\neg A \lor B)$ formülü, $A=true$ ve $B=true$ seçimiyle sağlanabilir. Ancak gerçek programlar `x + y > 10`, `array[i] == 0` veya taşma kontrolleri gibi daha zengin ifadeler kullanır. SMT, SAT motorunu korur ve bu mantıksal iskelete alan bilgisi ekleyen teori çözücülerini bağlar.

Bir formülün tatmin edilebilirliği şöyle ifade edilir:

$$
\exists x, y \in \mathbb{Z}:\quad x > 3 \land y = x + 2 \land y < 10
$$

Bu formül **sat** sonucuna sahiptir; örneğin $x=4$, $y=6$ bir modeldir. Buna karşılık $x > 3 \land x < 2$ ifadesi **unsat** olur. Program doğrulamada `unsat` genellikle güzel haberdir: “Hatalı durum erişilemez” anlamına gelir.

| Kavram | Sorduğu soru | Tipik çıktı | Kullanım alanı |
|---|---|---|---|
| SAT | Boole formülü sağlanabilir mi? | `sat` / `unsat` | Devreler, önerme mantığı |
| SMT | Teoriler altında formül sağlanabilir mi? | `sat` / `unsat` / `unknown` | Kod analizi, doğrulama |
| Optimize SMT | Geçerli modeller arasında en iyisi hangisi? | Model ve optimum değer | Planlama, kaynak dağıtımı |

Bir SMT solver kabaca üç adımda çalışır. İlk olarak ifadeyi mantıksal kararlar içeren bir yapıya dönüştürür. Ardından SAT çekirdeği, hangi atomik koşulların doğru kabul edileceğini dener. Son olarak teori çözücüsü bu kararların aritmetik veya veri yapısı kurallarıyla çelişip çelişmediğini kontrol eder. Çelişki varsa solver, benzer başarısız seçimleri tekrar denememek için bir **öğrenilmiş kısıt** üretir. Bu süreç, modern SAT tekniklerinden gelen conflict-driven learning yaklaşımının SMT’ye uyarlanmış halidir.

Örneğin bir fonksiyonun indeks sınırlarını aşıp aşmadığını Z3 ile sorgulayabiliriz:

```python
from z3 import Int, Solver, And

# i geçerli bir dizi indeksi mi, ayrıca erişim hatalı olabilir mi?
i = Int("i")
n = Int("n")
solver = Solver()

solver.add(n > 0)                 # Dizinin boyutu pozitif
solver.add(And(i >= 0, i < n))    # Fonksiyonun ön koşulu
solver.add(i >= n)                # Aradığımız hata durumu

print(solver.check())  # unsat
```

Kodda ilk iki kısıt, güvenli erişimin şartlarını tanımlar. Son kısıt ise kasıtlı olarak sınır aşımını talep eder. Sonucun `unsat` olması, ön koşullar doğruysa `i >= n` hatasının oluşamayacağını kanıtlar. Eğer bir hata mümkün olsaydı `sat` sonucu ile birlikte `model()` çağrısı bize somut bir karşı örnek sunabilirdi.

SMT solver’lar optimizasyonda da etkilidir. Amaç, kısıtları bozmayacak bir model bulmanın ötesine geçip hedef fonksiyonu en küçük ya da en büyük yapmaktır. Örneğin görev atamasında maliyeti $C=3x+5y$ olarak tanımlayıp $x+y\geq 10$ koşulu altında $\min C$ arayabiliriz. Tamsayı kısıtları, kapasite limitleri ve mantıksal seçimler aynı modelde birleştiğinde klasik yöntemler zorlanabilir; SMT burada oldukça okunabilir bir modelleme dili sağlar.

| Sonuç | Anlamı | Doğrulamadaki yorum |
|---|---|---|
| `sat` | En az bir model bulundu | Hata için karşı örnek olabilir |
| `unsat` | Hiçbir model yok | Hata durumu erişilemez olabilir |
| `unknown` | Solver karar veremedi | Farklı teori veya sınır gerekebilir |

Elbette `unsat` sonucu, modelin programa sadık kurulmasına bağlıdır. Yanlış ön koşul, eksik taşma modeli veya hatalı soyutlama, çok ikna edici ama yanlış bir kanıt üretebilir. Bu nedenle SMT’yi sihirli bir hata dedektörü değil; varsayımları açıkça yazdıran, karşı örnek üreten ve matematiksel güvence sağlayan güçlü bir ortak olarak görmek gerekir.

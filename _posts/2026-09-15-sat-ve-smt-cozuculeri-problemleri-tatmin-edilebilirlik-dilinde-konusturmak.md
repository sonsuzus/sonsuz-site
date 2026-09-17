---
layout: post
title: "SAT ve SMT Çözücüleri: Problemleri Tatmin Edilebilirlik Dilinde Konuşturmak"
math: true
categories: 
  - Bilgi
tags: 
  - sat
  - smt
  - mantık
  - z3
  - kısıt-programlama
  - doğrulama
toc: true
image: /img/sat-ve-smt-59.png
---

Bir sudoku çözmek, işlemci devresini doğrulamak veya çalışanların vardiyalarını planlamak ilk bakışta tamamen farklı problemlerdir. SAT ve SMT çözücüleri ise bu karmaşanın karşısına aynı soruyla çıkar: “Verilen bütün kuralları aynı anda sağlayan en az bir değer ataması var mı?” Problemi bu dile çevirebilirsek çözüm arama işini son derece gelişmiş algoritmalara bırakabiliriz.


![sat-ve-smt-59](/img/sat-ve-smt-59.svg)

``

## SAT: Boolean Dünyasında Doğruyu Aramak

**SAT** yani Boolean tatmin edilebilirlik problemi, yalnızca doğru ve yanlış değerleri alan değişkenlerden oluşan bir mantıksal formülün sağlanıp sağlanamayacağını sorar. Örneğin:

$$
(A \lor B) \land (\neg A \lor C) \land (\neg B \lor \neg C)
$$

Burada çözücü, $A$, $B$ ve $C$ için formülü doğru yapan bir atama arar. Örneğin $A=true$, $B=false$ ve $C=true$ seçimi bütün maddeleri sağlar; dolayısıyla formül **SAT** sonucuna sahiptir.

Modern çözücüler genellikle formülü **CNF** biçiminde ister:

$$
C_1 \land C_2 \land \dots \land C_n
$$

Her $C_i$, `OR` ile bağlanan literallerden oluşan bir maddedir. Çözücülerin temelinde DPLL ve onun daha güçlü hâli olan **CDCL** bulunur. CDCL bir değer seçer, sonuçlarını yayar, çelişki oluşursa çelişkinin nedenini öğrenir ve daha anlamlı bir noktaya geri döner. Yani labirentte aynı duvara ikinci kez kafa atmaz.

## SMT: Boolean Mantığa Matematik Eklemek

**SMT**, “Satisfiability Modulo Theories” ifadesinin kısaltmasıdır. SAT’ın doğru-yanlış dünyasını tam sayılar, gerçek sayılar, diziler, bit vektörleri ve fonksiyonlar gibi teorilerle genişletir.

Örneğin aşağıdaki kısıtlar bir SMT problemidir:

$$
x + y = 10 \land x > 3 \land y > x
$$

Çözücü yalnızca önermelerin mantıksal yapısını değil, aritmetik ilişkileri de anlamalıdır. $x=4$ ve $y=6$ geçerli bir modeldir.

| Özellik | SAT | SMT |
|---|---|---|
| Değişkenler | Boolean | Boolean, sayı, dizi, bit vektörü vb. |
| Temel soru | Formül doğru yapılabilir mi? | Teorik kısıtlar birlikte sağlanabilir mi? |
| Modelleme | Daha düşük seviyeli | Daha doğal ve açıklayıcı |
| Kullanım | Devreler, kombinatoryal problemler | Yazılım doğrulama, planlama, sembolik yürütme |

Her SMT problemi SAT’a dönüştürülebilir gibi görünse de sayıları bitlere ayırmak formülü hızla büyütebilir. SMT çözücüleri bu nedenle Boolean arama motorunu özel teori çözücüleriyle birlikte çalıştırır.

## Bir Problemi Kısıtlara İndirgemek

Üç görevimiz ve iki zaman dilimimiz olduğunu düşünelim. Her görev tam bir zaman dilimine atanmalı, ayrıca `A` ve `B` aynı anda çalışmamalıdır. Modelleme süreci şöyledir:

1. Karar değişkenlerini belirle: $slot_A$, $slot_B$, $slot_C$.
2. Değer alanlarını sınırla: $1 \le slot_i \le 2$.
3. İş kurallarını ekle: $slot_A \ne slot_B$.
4. Çözücüden bir model iste.

Python ve Z3 ile karşılığı oldukça okunaklıdır:

```python
from z3 import Int, Solver, sat

A, B, C = Int("A"), Int("B"), Int("C")
solver = Solver()

for task in (A, B, C):
    solver.add(task >= 1, task <= 2)

solver.add(A != B)

if solver.check() == sat:
    model = solver.model()
    print({"A": model[A], "B": model[B], "C": model[C]})
else:
    print("Geçerli plan yok")
```

Kod, değişkenlerin alanlarını ve çakışma kuralını tanımlar. `check()` çağrısı **sat**, **unsat** veya bazı durumlarda **unknown** döndürebilir. `sat` bulunursa `model()` somut bir çözüm verir. `unsat`, kuralların birlikte imkânsız olduğunu gösterir; örneğin hem $A=B$ hem de $A\ne B$ istemek gibi.

## Asıl Zorluk: Doğru Model

Çözücü sihirbaz değildir; yalnızca yazdığınız kısıtları çözer. Unutulan bir kural, teknik olarak geçerli ama gerçek hayatta saçma bir sonuç üretebilir. Bu nedenle değişkenleri küçük tutmak, simetrileri kırmak ve gereksiz kısıtlardan kaçınmak önemlidir.

SAT/SMT yaklaşımının gücü, “nasıl arayacağınızı” yazmak yerine “geçerli çözümün ne olduğunu” tarif etmenizdir. Böylece arama stratejisini çözücü üstlenir; size de problemi mantığın düzgün, kesin ve şaşırtıcı derecede etkili diline çevirmek kalır.

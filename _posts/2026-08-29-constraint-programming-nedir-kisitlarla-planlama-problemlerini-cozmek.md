---
layout: post
title: "Constraint Programming Nedir? Kısıtlarla Planlama Problemlerini Çözmek"
math: true
categories: 
  - Bilgi
tags: 
  - constraint programming
  - optimizasyon
  - python
---

Bir ders programı hazırladığınızı düşünün: öğretmenlerin uygun saatleri, sınıf kapasiteleri, ders çakışmaları ve öğrencilerin seçmeli tercihleri aynı anda dikkate alınmalı. Bu tür problemlerde tek tek kurallar yazıp olasılıkları denemek hızla kontrolden çıkar. **Constraint Programming (CP)**, yani kısıt programlama, çözümü doğrudan tarif etmek yerine çözümün uyması gereken kuralları tanımlayarak bu karmaşayı yönetir.

``

CP'nin temel fikri üç parçadan oluşur: **değişkenler**, bu değişkenlerin alabileceği **alanlar (domain)** ve aralarındaki **kısıtlar**. Örneğin üç toplantının başlangıç saatleri $x_1, x_2, x_3$ olsun. Her biri 9 ile 17 arasında başlayabilir:

$$x_i \in \{9,10,\ldots,17\}$$

Toplantılar aynı odada yapılıyorsa çakışmamalıdır. Süreler birer saat ise bunu basitçe $x_i \ne x_j$ biçiminde yazabiliriz. Bir toplantının diğerinden sonra başlaması gerekiyorsa $x_2 \ge x_1 + 1$ kısıtı kullanılır. Geliştirici, çözümün nasıl bulunacağını adım adım kodlamak yerine bu kuralları modele döker; CP çözücüsü geçerli atamaları araştırır.

Bu yaklaşımın sihri, **kısıt yayılımı (constraint propagation)** mekanizmasındadır. Çözücü bir değişkenin alanını daralttığında, ilgili diğer değişkenlerin imkânsız değerlerini de otomatik eler. Buna rağmen belirsizlik kalırsa kontrollü bir arama ve geri izleme (backtracking) başlatır. İyi bir çözücü, en kısıtlı değişkeni önce seçmek gibi sezgisel yöntemlerle arama ağacını ciddi biçimde küçültür.

| Kavram | Anlamı | Toplantı örneği |
|---|---|---|
| Değişken | Karar verilecek değer | `baslangic[0]` |
| Domain | İzin verilen değer kümesi | 9-17 saatleri |
| Sert kısıt | Mutlaka sağlanmalı | Aynı odada çakışmama |
| Yumuşak kısıt | İhlali maliyet yaratır | Sabah saatini tercih etme |
| Amaç fonksiyonu | En iyi geçerli çözümü seçer | En erken bitişi küçültme |

CP ile doğrusal programlama veya klasik algoritmalar rakip olmak zorunda değildir; farklı modelleme güçleri sunarlar:

| Yaklaşım | Güçlü olduğu durum | Tipik zorluk |
|---|---|---|
| Constraint Programming | Çizelgeleme, atama, mantıksal kurallar | Büyük arama uzayı |
| Doğrusal Programlama | Sayısal ve doğrusal maliyetler | Mantıksal koşulları modelleme |
| Açgözlü algoritma | Hızlı yaklaşık kararlar | Küresel optimum garantisi yok |

Python tarafında Google OR-Tools'un CP-SAT çözücüsü pratik bir başlangıç noktasıdır. Aşağıdaki örnek, üç görevi 0-8 aralığındaki saatlere yerleştirir. Görevlerin süreleri farklıdır, birbirleriyle çakışmazlar ve son bitiş zamanı en aza indirilmeye çalışılır.

```python
from ortools.sat.python import cp_model

model = cp_model.CpModel()
durations = [2, 3, 1]
starts = [model.NewIntVar(0, 8, f"start_{i}") for i in range(3)]
ends = [model.NewIntVar(0, 10, f"end_{i}") for i in range(3)]
intervals = []

for i, duration in enumerate(durations):
    model.Add(ends[i] == starts[i] + duration)
    intervals.append(model.NewIntervalVar(starts[i], duration, ends[i], f"job_{i}"))

model.AddNoOverlap(intervals)
makespan = model.NewIntVar(0, 10, "makespan")
model.AddMaxEquality(makespan, ends)
model.Minimize(makespan)

solver = cp_model.CpSolver()
if solver.Solve(model) in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    for i in range(3):
        print(f"Görev {i}: {solver.Value(starts[i])}-{solver.Value(ends[i])}")
```

Buradaki `AddNoOverlap`, ikili karşılaştırmaları elle yazmak yerine zaman aralıklarının çakışmamasını tek bir küresel kısıtla ifade eder. `AddMaxEquality` ise en geç biten görevi `makespan` değişkenine bağlar. Amaç fonksiyonumuz matematiksel olarak $\min \max_i(\text{end}_i)$ şeklindedir.

Başarılı bir CP modeli için önce sert kuralları netleştirin, gereksiz büyük domainlerden kaçının ve gerçek hayattaki tercihleri yumuşak kısıt ya da ceza terimi olarak ekleyin. Böylece “hangi adımlarla çözeyim?” sorusu, daha güçlü bir soruya dönüşür: “İyi bir çözüm hangi kurallara uymalı?”

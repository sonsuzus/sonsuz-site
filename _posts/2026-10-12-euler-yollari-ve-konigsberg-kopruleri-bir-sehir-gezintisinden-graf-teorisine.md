---
layout: post
title: "Euler Yolları ve Königsberg Köprüleri: Bir Şehir Gezintisinden Graf Teorisine"
math: true
categories: 
  - Bilgi
tags: 
  - graf teorisi
  - euler yolu
  - königsberg
  - algoritma
  - python
toc: true
image: /img/euler-yollari-ve-78.png
---

Bir pazar yürüyüşüne çıktığınızı ve şehirdeki her köprüden yalnızca bir kez geçmek istediğinizi düşünün. Başladığınız yere dönmeniz şart olmayabilir; ancak hiçbir köprüyü ikinci kez kullanamazsınız. Kulağa eğlenceli bir rota bulmacası gibi gelen bu soru, 18. yüzyılda matematikçi Leonhard Euler’in elinde yepyeni bir alanın, yani graf teorisinin doğmasına yol açtı.

![euler-yollari-ve-78](/img/euler-yollari-ve-78.svg)

``
## Königsberg Köprüleri Problemi

Prusya’nın Königsberg şehri, Pregel Nehri’nin ayırdığı dört kara parçası ve bunları birbirine bağlayan yedi köprüden oluşuyordu. Şehir halkının sorusu basitti: Her köprüden tam bir kez geçilen bir yürüyüş yapılabilir miydi?

Euler, kara parçalarının şekli veya köprülerin uzunluğu gibi ayrıntıların önemsiz olduğunu fark etti. Her kara parçasını bir **düğüm**, her köprüyü ise iki düğümü bağlayan bir **kenar** olarak temsil etti. Böylece fiziksel şehir, matematiksel bir grafa dönüştü.

| Gerçek dünyadaki öğe | Graf karşılığı |
|---|---|
| Kara parçası | Düğüm (vertex) |
| Köprü | Kenar (edge) |
| Bir kara parçasındaki köprü sayısı | Düğüm derecesi |
| Köprüleri kullanan yürüyüş | Graf üzerinde yol |

Aynı iki kara parçası arasında birden fazla köprü bulunabildiği için ortaya çıkan yapı teknik olarak bir **çoklu graf**tır.

## Düğüm Derecesi Neden Önemlidir?

Bir düğümün derecesi, o düğüme bağlı kenarların sayısıdır ve $\deg(v)$ ile gösterilir. Bir yol sırasında ara düğüme bir kenardan girip başka bir kenardan çıkmak gerekir. Dolayısıyla kullanılan kenarlar çiftler hâlinde eşleşir. Tek dereceli düğümler ise bu eşleşmenin bozulduğu başlangıç veya bitiş noktaları olabilir.

Grafın bütün düğüm dereceleri için şu önemli eşitlik geçerlidir:

$$\sum_{v \in V} \deg(v) = 2\vert E\vert $$

Her kenar iki uca sahip olduğundan dereceler toplamına iki katkı yapar. Bu sonuç, tek dereceli düğüm sayısının her zaman çift olduğunu da gösterir.

Königsberg grafındaki dört düğümün dereceleri $3, 3, 3$ ve $5$ idi. Yani dört düğüm de tek dereceliydi. Oysa her köprüden yalnızca bir kez geçen bir rota için tek dereceli düğüm sayısı en fazla iki olmalıdır. Sonuç: İstenen yürüyüş imkânsızdı!

## Euler Yolu ve Euler Devresi

| Kavram | Koşul | Başlangıç ve bitiş |
|---|---|---|
| Euler devresi | Tek dereceli düğüm yoktur | Aynı düğüm |
| Euler yolu | Tam iki tek dereceli düğüm vardır | Farklı düğümler |
| İmkânsız durum | İkiden fazla tek dereceli düğüm vardır | Uygun rota yoktur |

Bu koşullarda grafın, izole düğümler göz ardı edildiğinde, bağlantılı olduğu kabul edilir. Euler yolu **her kenarı** tam bir kez kullanır. Bu nedenle her düğümü bir kez ziyaret etmeye çalışan Hamilton yoluyla karıştırılmamalıdır.

## Python ile Euler Yolu Kontrolü

Aşağıdaki fonksiyon, komşuluk listesiyle verilen bağlantılı bir grafın Euler özelliğini dereceler üzerinden sınıflandırır:

```python
def euler_durumu(graf):
    tek_dereceliler = []

    for dugum, komsular in graf.items():
        if len(komsular) % 2 == 1:
            tek_dereceliler.append(dugum)

    if len(tek_dereceliler) == 0:
        return "Euler devresi var"
    elif len(tek_dereceliler) == 2:
        return f"Euler yolu var: {tek_dereceliler}"
    else:
        return "Euler yolu yok"

sehir = {
    "A": ["B", "B", "C"],
    "B": ["A", "A", "D"],
    "C": ["A", "D", "D"],
    "D": ["B", "C", "C", "D", "D"]
}

print(euler_durumu(sehir))
```

Listelerde aynı komşunun tekrarlanması paralel köprüleri temsil eder. Bir öz döngü ise düğüm derecesine iki katkı yaptığı için listede iki kez gösterilmiştir. Gerçek bir uygulamada ayrıca DFS veya BFS kullanarak grafın bağlantılı olup olmadığı doğrulanmalıdır.

Euler’in büyük başarısı belirli bir rotayı denemek değil, böyle bir rotanın var olup olamayacağını yapısal olarak kanıtlamaktı. Bugün aynı fikir; çöp toplama rotaları, ağ analizi, devre tasarımı ve DNA dizileme gibi pek çok alanda karşımıza çıkıyor. Bazen bir köprüden geçmeden önce dereceleri saymak, saatlerce dolaşmaktan çok daha akıllıcadır.

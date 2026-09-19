---
layout: post
title: "Tarjan Algoritması: Güçlü Bağlı Bileşenleri Tek DFS ile Yakalamak"
math: true
categories: 
  - Bilgi
tags: 
  - tarjan
  - graf algoritmaları
  - güçlü bağlı bileşenler
  - dfs
  - algoritma
  - c++
toc: true
---

Yönlü bir grafın içinde birbirine karşılıklı olarak ulaşabilen düğüm gruplarını bulmak, bağımlılık analizinden sosyal ağlara kadar pek çok alanda karşımıza çıkar. Tarjan algoritması, bu grupları yani **güçlü bağlı bileşenleri** yalnızca tek bir derinlik öncelikli arama sürecinde keşfeder. Üstelik bunu yaparken yanında yalnızca bir yığın, birkaç dizi ve etkileyici derecede zarif bir fikir taşır.

``

## Güçlü bağlı bileşen nedir?

Yönlü bir graf üzerinde $u$ düğümünden $v$ düğümüne ve $v$ düğümünden tekrar $u$ düğümüne ulaşılabiliyorsa bu iki düğüm aynı güçlü bağlı bileşende, kısaca **SCC** içinde bulunabilir. Bir SCC, bu özelliği sağlayan en büyük düğüm kümesidir.

Örneğin $A \rightarrow B$, $B \rightarrow C$ ve $C \rightarrow A$ kenarları varsa üç düğüm aynı bileşendedir. Ancak $C \rightarrow D$ bulunup $D$'den geri dönüş yolu yoksa $D$ başka bir bileşene aittir.

Tarjan algoritmasının temel değişkenleri şöyledir:

| Kavram | Anlamı |
|---|---|
| `index[u]` | Düğümün DFS sırasında aldığı keşif numarası |
| `low[u]` | `u` üzerinden ulaşılabilen, yığındaki en küçük keşif numarası |
| Yığın | Henüz bir SCC'ye kesin olarak atanmamış düğümler |
| `onStack[u]` | Düğümün aktif yığında olup olmadığı |

Kritik ilişki şudur:

$$low[u] = \min(index[u],\ low[v],\ index[w])$$

Burada $v$, DFS ağacında `u`nun ziyaret edilmemiş çocuğunu; $w$ ise hâlâ yığında bulunan ve geri kenarla ulaşılan bir düğümü temsil eder. Eğer arama sonunda

$$low[u] = index[u]$$

olursa `u`, bir güçlü bağlı bileşenin köküdür. Yığından `u` çıkana kadar alınan bütün düğümler aynı SCC'yi oluşturur. Küçük ama çok güçlü bir eşitlik!

## Neden yığın gerekiyor?

DFS sırasında ziyaret edilmiş her düğüm güncel bileşenin parçası olmayabilir. `onStack` kontrolü, tamamlanmış bir bileşene giden kenarın `low` değerini yanlışlıkla düşürmesini engeller. Başka bir deyişle Tarjan, yalnızca hâlâ “masada olan” düğümleri hesaba katar.

| Yaklaşım | DFS sayısı | Ek işlem | Karmaşıklık |
|---|---:|---|---:|
| Tarjan | 1 | Aktif düğüm yığını | $O(V+E)$ |
| Kosaraju | 2 | Grafın tersini oluşturma | $O(V+E)$ |
| Her düğümden erişim arama | Çok sayıda | Tekrarlı dolaşım | Yaklaşık $O(V(V+E))$ |

Tarjan'daki “tek geçiş”, her düğüm ve kenarın DFS kapsamında sabit sayıda işlenmesi anlamına gelir. Bu nedenle toplam zaman karmaşıklığı $O(V+E)$, yardımcı alan kullanımı ise $O(V)$ olur.

## C++ ile uygulama

Aşağıdaki kod, SCC'leri bulup her birini ayrı satırda yazdırır:

```cpp
#include <iostream>
#include <vector>
#include <stack>
#include <algorithm>
using namespace std;

vector<vector<int>> graph;
vector<int> idx, low;
vector<bool> onStack;
stack<int> active;
int timer = 0;

void dfs(int u) {
    idx[u] = low[u] = timer++;
    active.push(u);
    onStack[u] = true;

    for (int v : graph[u]) {
        if (idx[v] == -1) {
            dfs(v);
            low[u] = min(low[u], low[v]);
        } else if (onStack[v]) {
            low[u] = min(low[u], idx[v]);
        }
    }

    if (low[u] == idx[u]) {
        while (true) {
            int v = active.top();
            active.pop();
            onStack[v] = false;
            cout << v << ' ';
            if (v == u) break;
        }
        cout << '\n';
    }
}
```

Algoritmayı başlatırken `idx` dizisi `-1` ile doldurulur ve ziyaret edilmemiş her düğüm için `dfs` çağrılır. Böylece kopuk yönlü graflar da eksiksiz işlenir.

Tarjan algoritmasının güzelliği, DFS'in dönüş anlarını bilgiye çevirmesidir. `index` bize ne zaman geldiğimizi, `low` ise ne kadar geriye ulaşabildiğimizi söyler. Bu ikisi eşitlendiğinde yığın adeta “Bu bileşen tamamlandı!” diye bağırır. Derleyici bağımlılıklarını gruplayan araçlarda, döngüsel paketleri tespit ederken ve durum makinelerini sadeleştirirken bu teknik son derece kullanışlıdır.

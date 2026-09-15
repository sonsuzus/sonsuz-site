---
layout: post
title: "Dinic Algoritması: Katmanlı Ağlarla Maksimum Akışı Hızlandırmak"
math: true
categories: 
  - Bilgi
tags: 
  - dinic
  - maksimum-akış
  - graf-algoritmaları
  - katmanlı-ağ
  - c++
  - algoritma
toc: true
---

Bir boru hattından taşınabilecek suyu, bir ağın kaldırabileceği veri trafiğini veya depodan mağazalara gönderilebilecek ürün miktarını hesaplamak istediğimizi düşünelim. Bu problemlerin ortak noktası, belirli kapasitelere sahip bağlantılardan kaynaktan hedefe mümkün olan en büyük akışı göndermektir. Dinic algoritması, katmanlı ağ fikrini kullanarak bu maksimum akışı verimli biçimde bulur.
``
## Maksimum akışın teorik temeli

Yönlü bir $G=(V,E)$ grafında her $(u,v)$ kenarı için bir $c(u,v)$ kapasitesi bulunur. Akış değeri $f(u,v)$ şu kısıtları sağlamalıdır:

$$0 \leq f(u,v) \leq c(u,v)$$

Kaynak $s$ ve hedef $t$ dışındaki her düğümde akış korunur:

$$\sum_{u} f(u,v)=\sum_{w} f(v,w)$$

Başka bir deyişle, ara düğüme giren miktar oradan çıkmalıdır; düğüm gizlice su içemez! Amaç, $s$ düğümünden çıkan toplam akışı maksimize etmektir.

Algoritmalar bunu **artık ağ** üzerinden yapar. Bir kenardan akış gönderildiğinde ileri yöndeki kullanılabilir kapasite azalırken ters yönde aynı miktarda kapasite oluşur. Bu ters kenarlar, daha önce verilen kötü bir kararı geri alıp akışı farklı bir rotaya taşıyabilmemizi sağlar.

## Dinic’in iki temel adımı

Dinic algoritması her turda iki işlem gerçekleştirir:

1. **BFS ile katmanlı ağ kurar.** Her düğüme kaynaktan olan kenar mesafesi atanır. Yalnızca `level[v] = level[u] + 1` koşulunu sağlayan kenarlar kullanılır.
2. **DFS ile bloklayan akış gönderir.** Katmanlı ağda ilerletilebilecek akış kalmayıncaya kadar uygun yollar değerlendirilir.

Hedef BFS sonucunda erişilemez olduğunda artırma yolu kalmamıştır ve bulunan akış maksimumdur.

| Yaklaşım | Yol seçimi | Genel karmaşıklık | Temel fikir |
|---|---|---:|---|
| Ford–Fulkerson | Değişken | Kapasitelere bağlı | Herhangi bir artırma yolu |
| Edmonds–Karp | BFS | $O(VE^2)$ | En kısa artırma yolu |
| Dinic | BFS + DFS | $O(V^2E)$ | Katmanlı ağda bloklayan akış |

Dinic’in genel karmaşıklığı $O(V^2E)$ olsa da pratikte çoğu ağda oldukça hızlıdır. Birim kapasiteli özel graflarda daha güçlü sınırlar elde edilebilir.

## C++ ile uygulama

Aşağıdaki uygulamada her gerçek kenarla birlikte kapasitesi başlangıçta sıfır olan ters kenar eklenir. `work` dizisi, DFS’nin sonuç vermeyen kenarları tekrar tekrar incelemesini önler.

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Edge {
    int to, rev;
    long long cap;
};

class Dinic {
    vector<vector<Edge>> graph;
    vector<int> level, work;

    bool bfs(int source, int sink) {
        fill(level.begin(), level.end(), -1);
        queue<int> q;
        level[source] = 0;
        q.push(source);

        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (const Edge& e : graph[u]) {
                if (e.cap > 0 && level[e.to] == -1) {
                    level[e.to] = level[u] + 1;
                    q.push(e.to);
                }
            }
        }
        return level[sink] != -1;
    }

    long long dfs(int u, int sink, long long flow) {
        if (u == sink) return flow;

        for (int& i = work[u]; i < (int)graph[u].size(); ++i) {
            Edge& e = graph[u][i];
            if (e.cap <= 0 || level[e.to] != level[u] + 1) continue;

            long long sent = dfs(e.to, sink, min(flow, e.cap));
            if (sent > 0) {
                e.cap -= sent;
                graph[e.to][e.rev].cap += sent;
                return sent;
            }
        }
        return 0;
    }

public:
    explicit Dinic(int n) : graph(n), level(n), work(n) {}

    void addEdge(int from, int to, long long capacity) {
        Edge forward{to, (int)graph[to].size(), capacity};
        Edge reverse{from, (int)graph[from].size(), 0};
        graph[from].push_back(forward);
        graph[to].push_back(reverse);
    }

    long long maxFlow(int source, int sink) {
        long long total = 0, sent;
        const long long INF = numeric_limits<long long>::max();

        while (bfs(source, sink)) {
            fill(work.begin(), work.end(), 0);
            while ((sent = dfs(source, sink, INF)) > 0)
                total += sent;
        }
        return total;
    }
};
```

## Neden katmanlar hız kazandırır?

Sıradan artırma yaklaşımı aynı bölgelerde dolaşabilir. Katmanlı ağ ise DFS’yi yalnızca hedefe doğru ilerleyen kenarlarla sınırlar. Bir BFS turunda bulunan bloklayan akış, en az bir kritik geçişi tamamen doldurur. Sonraki turda hedefe olan katman mesafesi artar; bu mesafe en fazla $V-1$ olabileceğinden BFS turlarının sayısı da sınırlıdır.

Dinic; ağ yönlendirme, bipartite eşleme, görev atama ve kapasite planlama problemlerinde güçlü bir seçimdir. Özellikle graf büyük, fakat bağlantılar nispeten seyrekse katmanlama ile gereksiz aramaların azaltılması belirgin bir performans avantajı sağlar.

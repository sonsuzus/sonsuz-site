---
layout: post
title: "Köprüler ve Articulation Point’ler: Grafın Kritik Damarlarını Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - graf teorisi
  - dfs
  - köprüler
  - articulation point
  - algoritmalar
  - python
toc: true
---

Bir şehrin yol ağını, bilgisayar ağını veya sosyal bağlantıları bir graf olarak düşündüğümüzde bazı bağlantılar diğerlerinden çok daha kritiktir. Tek bir yol kapandığında şehir ikiye ayrılıyorsa o yol bir **köprü**, tek bir istasyon devre dışı kaldığında ağ parçalanıyorsa o istasyon bir **articulation point** yani **eklem noktasıdır**. Gelin grafın nabzını tutup bu kritik damarları nasıl bulacağımızı inceleyelim.
``
## Temel kavramlar

Yönsüz bir graf $G=(V,E)$ üzerinde çalışalım. Bir kenar silindiğinde bağlı bileşen sayısı artıyorsa bu kenara **köprü** denir. Benzer biçimde, bir düğüm ve ona bağlı kenarlar kaldırıldığında bağlı bileşen sayısı artıyorsa bu düğüm bir articulation point’tir.

| Yapı | Ne kaldırılır? | Kritik olma koşulu | Örnek kullanım |
|---|---|---|---|
| Köprü | Bir kenar | Bileşen sayısı artar | Kritik ağ kablosu |
| Articulation point | Bir düğüm | Bileşen sayısı artar | Merkezi yönlendirici |
| Normal kenar | Bir kenar | Alternatif rota vardır | Yedekli bağlantı |

Her kenarı veya düğümü sırayla silip grafı yeniden dolaşmak mümkündür; ancak bu yaklaşım pahalıdır. DFS sayesinde bütün kritik noktaları $O(\vert V\vert +\vert E\vert )$ zamanda bulabiliriz.

## DFS zamanları ve low-link değeri

Algoritmanın iki önemli değeri vardır:

- `tin[u]`: DFS sırasında `u` düğümüne ilk giriş zamanı.
- `low[u]`: `u` veya alt ağacından, en fazla bir geri kenar kullanılarak ulaşılabilen en eski düğümün giriş zamanı.

Başlangıçta $low[u]=tin[u]$ kabul edilir. Bir geri kenar görüldüğünde veya bir çocuk düğümün DFS’i tamamlandığında değer güncellenir:

$$
low[u] = \min(low[u], tin[v], low[child])
$$

Bir DFS ağaç kenarı $(u,v)$ için

$$
low[v] > tin[u]
$$

ise `v` alt ağacı, `u` düğümünün üst tarafına alternatif bir yoldan ulaşamıyor demektir. Dolayısıyla $(u,v)$ bir köprüdür.

Articulation point koşulu biraz farklıdır. Kök olmayan `u` için en az bir çocukta $low[v] \ge tin[u]$ olması yeterlidir. DFS kökü ise yalnızca birden fazla DFS çocuğuna sahipse kritik kabul edilir. Kök için bu özel kural unutulursa masum düğümler yanlışlıkla suçlanabilir!

## Python ile uygulama

Aşağıdaki kod kenarlara kimlik vererek paralel kenarları da doğru biçimde işler. Böylece ebeveyn düğümü değil, yalnızca DFS’te kullanılan ebeveyn kenarı atlanır.

```python
def critical_parts(n, edges):
    graph = [[] for _ in range(n)]
    for edge_id, (a, b) in enumerate(edges):
        graph[a].append((b, edge_id))
        graph[b].append((a, edge_id))

    timer = 0
    tin = [-1] * n
    low = [-1] * n
    bridges = []
    articulation = set()

    def dfs(u, parent_edge=-1):
        nonlocal timer
        tin[u] = low[u] = timer
        timer += 1
        children = 0

        for v, edge_id in graph[u]:
            if edge_id == parent_edge:
                continue

            if tin[v] != -1:          # Geri kenar
                low[u] = min(low[u], tin[v])
            else:
                dfs(v, edge_id)
                low[u] = min(low[u], low[v])
                children += 1

                if low[v] > tin[u]:
                    bridges.append((u, v))

                if parent_edge != -1 and low[v] >= tin[u]:
                    articulation.add(u)

        if parent_edge == -1 and children > 1:
            articulation.add(u)

    for node in range(n):
        if tin[node] == -1:
            dfs(node)

    return bridges, articulation
```

Dış döngü önemlidir; çünkü graf baştan bağlı olmayabilir. Her ziyaret edilmemiş düğüm için yeni bir DFS başlatılarak tüm bileşenler incelenir.

## Neden doğrusal zamanda çalışır?

DFS her düğümü bir kez ziyaret eder. Yönsüz grafın her kenarı iki komşuluk kaydında bulunsa da sabit sayıda işlenir. Bu nedenle zaman karmaşıklığı $O(\vert V\vert +\vert E\vert )$, komşuluk listeleri ve yardımcı diziler nedeniyle bellek karmaşıklığı da $O(\vert V\vert +\vert E\vert )$ olur.

Köprüler ve articulation point’ler; ağ dayanıklılığı, ulaşım planlaması, elektrik şebekeleri ve bağımlılık analizinde güçlü araçlardır. Kısacası DFS yalnızca grafı gezmez; sistemin hangi parçası koparsa ortalığın karışacağını da söyler.

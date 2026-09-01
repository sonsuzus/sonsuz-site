---
layout: post
title: "Tarjan Algoritması ile Güçlü Bağlı Bileşenleri Tek Geçişte Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - tarjan algoritması
  - graf teorisi
  - derinlik öncelikli arama
toc: true
---

Bir sosyal ağda Ayşe, Berk’e; Berk, Cem’e; Cem de Ayşe’ye ulaşabiliyorsa bu üçlü, yönler farklı olsa bile kendi içinde güçlü bir iletişim halkası oluşturur. Tarjan algoritması, yönlü çizgelerdeki bu halkaları yalnızca bir derinlik öncelikli arama geçişiyle keşfeder. Böylece bağımlılık analizi, ağ incelemesi ve döngü tespiti gibi işlemleri oldukça verimli hâle getirir.
``
## Güçlü bağlı bileşen nedir?

Yönlü bir çizgeyi $G=(V,E)$ biçiminde gösterelim. Bir düğüm kümesindeki her $u$ ve $v$ çifti için hem $u \leadsto v$ hem de $v \leadsto u$ yolu bulunuyorsa bu küme bir **güçlü bağlı bileşendir** (SCC).

Örneğin $A \to B$, $B \to C$ ve $C \to A$ kenarları üç düğümü aynı SCC içine yerleştirir. Buna karşılık yalnızca $C \to D$ varsa, $D$ geri dönemediği için aynı bileşene katılamaz. SCC’ler maksimaldir; kümeye karşılıklı erişilebilirliği bozmadan başka bir düğüm eklenemez.

Tarjan’ın temel fikri, DFS sırasında her düğüme iki değer vermektir:

- `index[u]`: Düğümün keşfedilme sırası.
- `low[u]`: DFS yolları ve yığındaki geri kenarlar kullanılarak ulaşılabilen en küçük keşif indeksi.

Bir düğüm için

$$low[u] = index[u]$$

olduğunda `u`, bir güçlü bağlı bileşenin köküdür. Algoritma bu noktada yığından `u` çıkana kadar düğümleri toplar.

| Kavram | Görevi | Değişir mi? |
|---|---|---|
| `index` | Keşif zamanını kaydeder | Hayır |
| `low` | Ulaşılabilen en eski aktif düğümü gösterir | Evet |
| Yığın | Henüz bir SCC’ye atanmış düğümleri tutar | Evet |
| `on_stack` | Geri kenarın geçerli olup olmadığını belirler | Evet |

## Algoritmanın işleyişi

DFS bir komşuyla ilk kez karşılaşırsa onu ziyaret eder ve dönüşte `low` değerini günceller. Komşu daha önce görülmüş ve hâlâ yığındaysa bir geri bağlantı bulunmuştur. Ancak yığından çıkarılmış düğümler artık tamamlanmış başka bileşenlere aittir; bunlar `low` hesabına katılmaz.

```python
def tarjan(graph):
    index = 0
    indices, low = {}, {}
    stack, on_stack, components = [], set(), []

    def dfs(node):
        nonlocal index
        indices[node] = low[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)

        for neighbor in graph[node]:
            if neighbor not in indices:
                dfs(neighbor)
                low[node] = min(low[node], low[neighbor])
            elif neighbor in on_stack:
                low[node] = min(low[node], indices[neighbor])

        if low[node] == indices[node]:
            component = []
            while True:
                current = stack.pop()
                on_stack.remove(current)
                component.append(current)
                if current == node:
                    break
            components.append(component)

    for node in graph:
        if node not in indices:
            dfs(node)

    return components
```

Kodda `dfs`, düğümlerin keşif ve düşük bağlantı değerlerini hesaplar. `low[node] == indices[node]` koşulu sağlandığında yeni bir SCC tamamlanır. Yığın kullanılması, aynı DFS dalındaki aktif düğümlerin birlikte çıkarılmasını sağlar.

## Neden hızlıdır?

Her düğüm bir kez ziyaret edilir, her kenar da en fazla bir kez incelenir. Bu nedenle zaman karmaşıklığı

$$T(\vert V\vert ,\vert E\vert )=O(\vert V\vert +\vert E\vert )$$

ve ek alan karmaşıklığı $O(\vert V\vert )$ olur.

| Yöntem | Geçiş yaklaşımı | Zaman | Öne çıkan yön |
|---|---:|---:|---|
| Tarjan | Tek DFS | $O(V+E)$ | Tek yığın ve tek geçiş |
| Kosaraju | İki DFS | $O(V+E)$ | Kavramsal olarak daha sade |
| Her düğümden arama | Çok sayıda arama | Yaklaşık $O(V(V+E))$ | Büyük ağlarda pahalı |

Tarjan algoritması; paket bağımlılıklarındaki döngüleri, çağrı çizgelerindeki karşılıklı fonksiyon gruplarını ve sosyal ağlardaki sıkı toplulukları belirlemek için kullanılabilir. SCC’ler tek düğüme indirgenerek döngüsüz bir yoğunlaştırma çizgesi de üretilebilir. Kısacası Tarjan, ağın karmaşık görünen döngülerini düzenli adacıklara ayıran hızlı ve zarif bir graf teorisi aracıdır.

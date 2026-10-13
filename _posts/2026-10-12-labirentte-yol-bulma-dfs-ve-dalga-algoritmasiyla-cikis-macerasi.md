---
layout: post
title: "Labirentte Yol Bulma: DFS ve Dalga Algoritmasıyla Çıkış Macerası"
math: true
categories: 
  - Proje
tags: 
  - algoritma
  - python
  - labirent
  - dfs
  - bfs
  - graf
toc: true
image: /img/labirentte-yol-bulma-11.png
---

Bir labirentin çıkışını bulmak, yalnızca duvarlara çarpmadan yürümek değildir; aynı zamanda bilgisayar bilimindeki graf gezinme problemlerinin eğlenceli bir temsilidir. Bu projede labirenti bir graf gibi modelleyecek, Derinine Arama (DFS) ve dalga algoritması olarak da bilinen Genişliğine Arama (BFS) ile çıkışa ulaşacağız.

``

## Labirenti grafa dönüştürmek

Labirentimiz iki boyutlu bir matris olsun. `0` geçilebilir hücreyi, `1` ise duvarı temsil etsin. Her geçilebilir hücre bir **düğüm**, yukarı, aşağı, sağ ve sol yönlerindeki geçişler de birer **kenar** kabul edilir.

Bir hücrenin koordinatı $(r,c)$ ise olası komşuları şunlardır:

$$N(r,c)=\{(r-1,c),(r+1,c),(r,c-1),(r,c+1)\}$$

Elbette matrisin dışına çıkan veya duvara denk gelen komşular listeye alınmaz. Böylece fiziksel görünen labirent, algoritmaların rahatça gezebileceği bir grafa dönüşür.

| Özellik | DFS | Dalga algoritması (BFS) |
|---|---|---|
| Temel yapı | Yığın veya özyineleme | Kuyruk |
| Gezinme biçimi | Bir yönde olabildiğince ilerler | Katman katman yayılır |
| En kısa yolu garanti eder mi? | Hayır | Evet, eşit maliyetli adımlarda |
| Bellek kullanımı | Genellikle daha düşük | Geniş alanlarda daha yüksek |
| Benzetme | Koridorda inatla ilerlemek | Su dalgasının her yöne yayılması |

Her iki algoritmanın zaman karmaşıklığı graf gösteriminde $O(V+E)$ şeklindedir. Burada $V$ hücre sayısını, $E$ ise hücreler arasındaki geçişleri belirtir.

## Derinine Arama ile çıkışı bulmak

DFS, seçtiği bir koridorda ilerleyebildiği kadar ilerler. Çıkmaz sokağa ulaşırsa geri döner ve denenmemiş başka bir yönü araştırır. Aşağıdaki kod, ziyaret edilen hücrelerin yanında yolu yeniden kurabilmek için ebeveyn bilgilerini de saklar:

```python
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def dfs(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    stack = [start]
    parent = {start: None}

    while stack:
        current = stack.pop()
        if current == goal:
            return build_path(parent, goal)

        r, c = current
        for dr, dc in MOVES:
            nxt = (r + dr, c + dc)
            nr, nc = nxt
            valid = 0 <= nr < rows and 0 <= nc < cols
            if valid and maze[nr][nc] == 0 and nxt not in parent:
                parent[nxt] = current
                stack.append(nxt)
    return None
```

Yığın, son eklenen hücreyi önce çıkardığı için algoritma derine dalar. `parent` sözlüğü aynı zamanda ziyaret kontrolü yaparak döngüye girilmesini engeller.

## Dalga algoritmasıyla en kısa yol

BFS başlangıçtan uzaklığı bir olan hücreleri, ardından uzaklığı iki olanları ziyaret eder. Kuyruk sayesinde ilk bulunan çıkış, adım sayısı bakımından en kısa yoldur.

```python
from collections import deque

def bfs(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            return build_path(parent, goal)

        r, c = current
        for dr, dc in MOVES:
            nxt = (r + dr, c + dc)
            nr, nc = nxt
            valid = 0 <= nr < rows and 0 <= nc < cols
            if valid and maze[nr][nc] == 0 and nxt not in parent:
                parent[nxt] = current
                queue.append(nxt)
    return None
```

Ortak yol oluşturma fonksiyonu, çıkıştan başlangıca doğru ebeveynleri takip eder ve sonucu ters çevirir:

```python
def build_path(parent, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    return path[::-1]
```

## Küçük bir test

```python
maze = [
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [1, 1, 0, 0],
    [0, 0, 0, 0]
]

print('DFS yolu:', dfs(maze, (0, 0), (3, 3)))
print('BFS yolu:', bfs(maze, (0, 0), (3, 3)))
```

DFS hızlıca bir çıkış bulabilir ancak dolaşık bir rota seçebilir. BFS ise tüm yakın seçenekleri sırayla değerlendirdiğinden en kısa rotayı üretir. Kısacası yalnızca kaçmak istiyorsanız DFS, çıkışa en az adımla ve kahramanca ulaşmak istiyorsanız BFS güçlü bir seçimdir.

![labirentte-yol-bulma-11](/img/labirentte-yol-bulma-11.svg)


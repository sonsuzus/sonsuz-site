---
layout: post
title: "Sanal Ağaç ile Seçili Düğümler Üzerinde Hızlı İşlem"
math: true
categories: 
  - Bilgi
tags: 
  - sanal ağaç
  - ağaç algoritmaları
  - lca
  - graf teorisi
  - c++
  - dinamik programlama
toc: true
---

Büyük bir ağaçta yalnızca birkaç seçili düğümle ilgilendiğinizi düşünün. Milyonlarca düğümü her sorguda dolaşmak, çay demlenene kadar çalışan algoritmalar üretir. **Sanal ağaç (virtual tree)** ise yalnızca önemli düğümleri ve bunların bağlantısını koruyarak sorguyu küçük bir ağaca indirger.
``
## Temel fikir

Elimizde $n$ düğümlü köklü bir ağaç ve bir sorguda seçilmiş $k$ düğüm olsun. Amaç; seçili düğümler arasındaki uzaklık, ortak ata, kapsanan yollar veya minimum bağlantı alt ağacı gibi değerleri hızlı hesaplamaktır.

Seçili düğümleri doğrudan birbirine bağlayamayız; çünkü aralarındaki dallanmayı belirleyen bazı **en yakın ortak atalar** da gereklidir. Bu nedenle sanal ağacın düğüm kümesi şu biçimde düşünülür:

$$V' = S \cup \{\operatorname{LCA}(u,v)\}$$

Burada $S$ seçili düğümler kümesidir. Euler turundaki giriş zamanına göre sıralanmış ardışık düğümlerin LCA’larını eklemek yeterlidir. Böylece düğüm sayısı en fazla yaklaşık $2k$ olur.

| Yaklaşım | İşlenen düğüm | Sorgu maliyeti | Uygun durum |
|---|---:|---:|---|
| Tüm ağacı dolaşma | $n$ | $O(n)$ | Az sayıda sorgu |
| Her çift için işlem | $k^2$ | $O(k^2)$ | Çok küçük $k$ |
| Sanal ağaç | En fazla $2k-1$ | $O(k\log k)$ | Büyük ağaç, çok sorgu |

## Sanal ağaç nasıl kurulur?

Önce gerçek ağaç üzerinde DFS yapılarak her düğümün giriş zamanı `tin`, derinliği ve ikili sıçrama tablosu hazırlanır. Böylece LCA sorguları $O(\log n)$ zamanda cevaplanabilir.

Her sorguda şu adımlar uygulanır:

1. Seçili düğümleri `tin` değerlerine göre sırala.
2. Ardışık düğümlerin LCA’larını listeye ekle.
3. Listeyi yeniden sırala ve tekrarları kaldır.
4. Bir yığın kullanarak her düğümü sanal ağaçtaki en yakın atasına bağla.

Atalık kontrolü Euler turuyla kolaydır:

$$u \text{, } v\text{'nin atasıdır} \iff tin[u] \le tin[v] \land tout[v] \le tout[u]$$

Aşağıdaki C++ fonksiyonu, önceden hazırlanmış `tin`, `isAncestor` ve `lca` araçlarını kullanarak sanal ağacın kenarlarını oluşturur:

```cpp
vector<pair<int, int>> buildVirtualTree(vector<int> nodes) {
    sort(nodes.begin(), nodes.end(),
         [&](int a, int b) { return tin[a] < tin[b]; });

    int originalSize = nodes.size();
    for (int i = 1; i < originalSize; ++i)
        nodes.push_back(lca(nodes[i - 1], nodes[i]));

    sort(nodes.begin(), nodes.end(),
         [&](int a, int b) { return tin[a] < tin[b]; });
    nodes.erase(unique(nodes.begin(), nodes.end()), nodes.end());

    vector<int> stack;
    vector<pair<int, int>> edges;

    for (int v : nodes) {
        while (!stack.empty() && !isAncestor(stack.back(), v))
            stack.pop_back();

        if (!stack.empty())
            edges.push_back({stack.back(), v});

        stack.push_back(v);
    }
    return edges;
}
```

Yığın, geçerli ata zincirini tutar. Yeni düğüm geldiğinde onun atası olmayan düğümler çıkarılır; tepede kalan düğüm, yeni düğümün sanal ebeveynidir.

## Kenar uzunlukları kaybolmaz

Sanal ağaç bazı gerçek düğümleri atlar ancak mesafeyi kaybetmez. Gerçek ağaçta kenarlar birim ağırlıklıysa sanal `u -> v` kenarının ağırlığı:

$$w(u,v)=depth[v]-depth[u]$$

Ağırlıklı ağaçta ise kökten uzaklık dizisi kullanılarak $w(u,v)=dist[v]-dist[u]$ alınır. Böylece sıkıştırılmış ağaç üzerinde DP çalıştırırken gerçek yol uzunlukları korunur.

Örneğin seçili düğümleri bağlayan minimum alt ağacın toplam uzunluğu, sanal ağaçta yalnızca gerekli kenarların ağırlıklarını toplamakla bulunabilir. Alt ağaçtaki seçili düğüm sayılarını hesaplayan bir DP ile seçili çiftlerin uzaklık toplamı da elde edilir. Bir kenarın altında $x$, dışında $k-x$ seçili düğüm varsa katkısı:

$$w \cdot x \cdot (k-x)$$

Sonuç olarak sanal ağaç, devasa ağacı fiziksel olarak değiştirmez; her sorgu için geçici ve küçük bir çalışma alanı oluşturur. Özellikle $\sum k$ makulken $n$ çok büyükse, bu teknik yarışma programlamasının en güçlü “yalnızca gerekeni işle” araçlarından biridir.

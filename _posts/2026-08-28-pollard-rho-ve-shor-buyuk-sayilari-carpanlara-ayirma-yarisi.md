---
layout: post
title: "Pollard Rho ve Shor: Büyük Sayıları Çarpanlara Ayırma Yarışı"
math: true
categories: 
  - Bilgi
tags: 
  - kriptografi
  - algoritmalar
  - kuantum hesaplama
---

Bir RSA anahtarını oluşturan büyük sayıyı çarpanlarına ayırmak, yalnızca matematiksel bir bulmaca değildir; modern açık anahtarlı kriptografinin güvenlik varsayımlarından biridir. Bu problemde Pollard Rho klasik dünyada akıllı bir rastgele yürüyüş yaklaşımı sunarken, Shor algoritması kuantum bilgisayarların teorik olarak oyunun kurallarını değiştirebileceğini söyler. Ancak önemli ayrım şudur: Shor'u klasik bilgisayarda **simüle etmek**, algoritmayı kuantum hızında çalıştırmak anlamına gelmez.
``

Bir bileşik sayı $N = p \cdot q$ için hedef, gizli asal çarpanlardan en az birini bulmaktır. Deneme bölmesi yaklaşık $O(\sqrt{N})$ kadar aday kontrolü gerektirebilir. Pollard Rho ise özellikle küçük veya orta boy asal çarpanı bulunan sayılarda, doğum günü paradoksuna benzer bir çakışma fikrinden yararlanır. Tipik beklenen maliyeti, en küçük asal çarpan $p$ için yaklaşık $O(\sqrt{p})$ işlem olarak düşünülebilir.

## Pollard Rho'nun “kapalı döngü” fikri

Algoritma, örneğin $f(x)=x^2+c \pmod N$ fonksiyonu ile bir dizi üretir. Dizi sonlu bir modüler uzayda dolaştığı için sonunda döngüye girer; Rho adı da şeklinin Yunan harfi $\rho$'ya benzemesinden gelir. Asıl numara, iki değerin farkının $N$ ile ortak bölenini hesaplamaktır:

$$d = \gcd(|x-y|, N)$$

Eğer $1 < d < N$ ise şanslıyız: $d$, $N$'in bir çarpanıdır. Floyd'un kaplumbağa-tavşan döngü algılama yöntemi bu iş için yeterince zariftir.

```python
from math import gcd

def pollard_rho(n, c=1):
    if n % 2 == 0:
        return 2
    x = y = 2
    d = 1
    while d == 1:
        x = (x * x + c) % n       # Kaplumbağa: tek adım
        y = (y * y + c) % n       # Tavşan: iki adım
        y = (y * y + c) % n
        d = gcd(abs(x - y), n)
    return None if d == n else d

print(pollard_rho(8051))  # Örnek çıktı: 83 veya 97
```

Bu kod, çarpanın her zaman ilk denemede bulunacağını garanti etmez. `c` ve başlangıç değeri değiştirilerek yeniden denenir; gerçek uygulamalarda Miller-Rabin gibi bir asallık testi ve özyinelemeli parçalama da eklenir.

| Özellik | Pollard Rho | Shor algoritması |
|---|---|---|
| Çalışma ortamı | Klasik bilgisayar | Hata düzeltmeli kuantum bilgisayar |
| Temel fikir | Rastgele yürüyüş ve EBOB | Periyot bulma ve kuantum Fourier dönüşümü |
| Teorik ölçeklenme | Çarpan boyutuna bağlı, üstel karakterli | $O((\log N)^3)$ civarı kuantum işlem |
| Güncel pratiklik | Yaygın ve kullanışlı | Donanım sınırları nedeniyle sınırlı |

## Shor neden etkileyici?

Shor algoritması, doğrudan çarpan aramak yerine $a^r \equiv 1 \pmod N$ koşulundaki periyodu, yani $r$ değerini bulur. Uygun bir $a$ seçildiğinde ve $r$ çift olduğunda:

$$\gcd(a^{r/2}-1, N) \quad \text{ve} \quad \gcd(a^{r/2}+1, N)$$

hesapları $N$'in çarpanlarını verebilir. Kuantum Fourier dönüşümü, bu periyodu kuantum süperpozisyonundan çıkarmanın ana aracıdır. Buradaki hız avantajı, çok sayıda değeri klasik anlamda paralel denemekten değil, olasılık genliklerindeki girişim deseninden bilgi almaktan doğar.

Fakat klasik simülasyonun acımasız bir bedeli vardır. $n$ kübitlik bir durum vektörü $2^n$ karmaşık genlik tutar. Çift duyarlıklı karmaşık sayı başına yaklaşık 16 bayt varsayılırsa bellek ihtiyacı kabaca $16 \cdot 2^n$ bayttır. Yani 30 kübit yaklaşık 16 GB seviyesine yaklaşırken, anlamlı RSA boyutları tamamen erişilemez olur.

| Simülasyon yaklaşımı | Güçlü yanı | Ana sınırı |
|---|---|---|
| Durum vektörü | Genel devreleri doğru simüle eder | Bellek $O(2^n)$ büyür |
| Tensor network | Düşük dolaşıklıkta verimlidir | Shor devresinde dolaşıklık maliyetlidir |
| Klasik periyot kontrolü | Mantığı öğretmek için idealdir | Kuantum hızlanmasını vermez |

Sonuç olarak Pollard Rho, klasik makinelerde gerçek faktorizasyon deneyleri için doğru başlangıç noktasıdır. Shor simülasyonu ise küçük sayılarda kavramları doğrulamak, devre kaynaklarını ölçmek ve kuantum programlama öğrenmek için değerlidir. Simülasyondaki yavaşlık Shor'un başarısızlığı değil; kuantum avantajını klasik donanım üzerinde taklit etmeye çalışmanın doğal maliyetidir.

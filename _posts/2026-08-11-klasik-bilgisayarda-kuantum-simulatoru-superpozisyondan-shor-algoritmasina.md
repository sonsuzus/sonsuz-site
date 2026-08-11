---
layout: post
title: "Klasik Bilgisayarda Kuantum Simülatörü: Süperpozisyondan Shor Algoritmasına"
math: true
categories: 
  - Proje
tags: 
  - kuantum-bilgisayar
  - python
  - shor-algoritması
---

Kuantum bilgisayarlar, bilgiyi yalnızca 0 veya 1 olarak değil, bu durumların olasılıksal birleşimi olarak işler. Peki bu tuhaf dünyayı evimizdeki klasik bilgisayarda deneyebilir miyiz? Evet: Bir kuantum **simülatörü**, kuantum donanımının fiziksel hız avantajını vermez; ancak kübitlerin durumlarını matematiksel olarak takip ederek süperpozisyon, girişim ve dolanıklığı görünür hâle getirir. Hedefimiz küçük devreleri simüle etmek ve Shor algoritmasının periyot bulma fikrini anlamaktır.
``

Bir kübitin genel durumu aşağıdaki karmaşık vektördür:

$$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$$

Burada $\alpha$ ve $\beta$ karmaşık sayılardır; ölçüm olasılıkları ise Born kuralıyla hesaplanır: $P(0)=|\alpha|^2$, $P(1)=|\beta|^2$ ve toplamları 1 olmalıdır. Klasik bit kesin bir kutudayken, kübit ölçülene kadar iki kutunun da kapısını aralık bırakır. Bu, “aynı anda her cevabı hesaplıyor” gibi romantik ama eksik bir anlatımdır: Asıl güç, doğru cevapları güçlendiren **girişim** desenlerindedir.

| Kavram | Klasik karşılığı | Kuantum davranışı |
|---|---|---|
| Bit / kübit | 0 veya 1 | $\alpha|0\rangle+\beta|1\rangle$ |
| Rastgelelik | İşlemden önce veya sonra seçilir | Ölçüm anında olasılıksal sonuç oluşur |
| Bağıntı | Ayrı değişkenlerle saklanır | Dolanıklıkta tek bir ortak durum vardır |
| Maliyet | $n$ bit için $n$ değer | $n$ kübit için $2^n$ genlik |

Simülatörün kalbi, $n$ kübitlik sistemi uzunluğu $2^n$ olan bir NumPy vektörüyle temsil etmektir. Başlangıç durumu $|00\ldots0\rangle$ olduğundan ilk genlik 1, diğerleri 0’dır. Hadamard kapısı süperpozisyon üretir; CNOT ise kontrol kübiti 1 olduğunda hedefi çevirir. Aşağıdaki örnek, iki kübitte Bell durumu $\frac{|00\rangle+|11\rangle}{\sqrt{2}}$ oluşturur:

```python
import numpy as np

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
I = np.eye(2, dtype=complex)
CNOT = np.array([
    [1, 0, 0, 0], [0, 1, 0, 0],
    [0, 0, 0, 1], [0, 0, 1, 0]
], dtype=complex)

state = np.array([1, 0, 0, 0], dtype=complex)  # |00>
state = np.kron(H, I) @ state                  # H, ilk kübite
state = CNOT @ state                            # ilk kübit kontrol
print(np.round(state, 3))
```

Çıktıda yalnızca $|00\rangle$ ve $|11\rangle$ genliklerinin dolu olması dolanıklığı gösterir. Bu, “ilk kübit 0, ikinci 0; ilk 1, ikinci 1” diye iki ayrı klasik kayıt tutmak değildir. Tek tek kübitler ölçülmeden belirli değere sahip değildir; ama birlikte ölçüldüklerinde sonuçları mükemmel biçimde ilişkilidir.

Shor algoritması, $N$ sayısını çarpanlara ayırmayı periyot bulma problemine dönüştürür. Rastgele bir $a$ seçilir ve

$$f(x)=a^x \bmod N$$

fonksiyonunun periyodu $r$ aranır. Eğer $r$ çiftse ve $a^{r/2}\not\equiv-1\pmod N$ ise, çarpan adayları $\gcd(a^{r/2}-1,N)$ ve $\gcd(a^{r/2}+1,N)$ olur. Örneğin $N=15$, $a=2$ için dizi $1,2,4,8,1,\ldots$ şeklindedir; yani $r=4$. Böylece $\gcd(2^2-1,15)=3$ ve $\gcd(2^2+1,15)=5$ bulunur.

| Shor adımı | Klasik görev | Kuantum devresindeki rol |
|---|---|---|
| Üs alma | $a^x \bmod N$ hesaplama | Tersinir modüler üs alma |
| Periyot çıkarma | Örnekleri analiz etme | QFT ile frekansı belirginleştirme |
| Çarpan üretme | EBOB hesaplama | Ölçüm sonrası klasik işlem |

Küçük bir projede modüler fonksiyonu durum vektörüne uygulayıp ardından Kuantum Fourier Dönüşümü (QFT) ekleyebilirsiniz. QFT, periyodik genlikleri frekans tepelerine dönüştürür; ölçümden gelen yaklaşık kesir de sürekli kesirler yöntemiyle $r$ adayına çevrilir. Ancak kritik gerçek şudur: klasik simülatör bellek açısından $O(2^n)$ büyür. Bu yüzden Shor’un büyük sayılardaki vaadini simülatörde değil, hata düzeltmeli gerçek kuantum donanımında bekleriz. Yine de Bell durumu, QFT ve 15’in çarpanlara ayrılması; kuantum programlamanın en eğlenceli laboratuvarıdır.

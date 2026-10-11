---
layout: post
title: "Stirling ve Bell Sayılarıyla Küme Parçalanmasının Matematiği"
math: true
categories: 
  - Bilgi
tags: 
  - stirling sayıları
  - bell sayıları
  - kombinatorik
  - küme teorisi
  - dinamik programlama
toc: true
image: /img/stirling-ve-bell-71.png
---

Bir sınıftaki öğrencileri takımlara, sunucuları kümelere veya görevleri bağımsız gruplara ayırdığınızı düşünün. Grupların sırası önemli değilse ve her eleman tam olarak bir gruba katılacaksa karşımıza **küme parçalanması** çıkar. Bu parçalanmaları belirli sayıda grup için Stirling, toplam olarak ise Bell sayılarıyla hesaplayabiliriz.

``

## Küme parçalanması nedir?

Bir kümenin parçalanması; boş olmayan, birbirinden ayrık alt kümelerden oluşan ve birleşimleri başlangıç kümesini veren bir koleksiyondur. Örneğin $A=\{a,b,c\}$ kümesinin bazı parçalanmaları şunlardır:

- $\{\{a,b,c\}\}$
- $\{\{a\},\{b,c\}\}$
- $\{\{a,b\},\{c\}\}$
- $\{\{a\},\{b\},\{c\}\}$

Burada grupların sırası önemli değildir. Dolayısıyla $\{\{a\},\{b,c\}\}$ ile $\{\{b,c\},\{a\}\}$ aynı parçalanmadır. Kombinatorikteki küçük ama kritik ayrıntı budur; aksi hâlde gereksiz yere aynı sonucu birkaç kez sayarız.

## İkinci tür Stirling sayıları

$n$ elemanlı bir kümeyi tam olarak $k$ tane boş olmayan gruba ayırma sayısı **ikinci tür Stirling sayısı** olarak adlandırılır ve $S(n,k)$ biçiminde gösterilir.

| İfade | Anlamı | Değeri |
|---|---|---:|
| $S(3,1)$ | Üç elemanı tek gruba ayırma | 1 |
| $S(3,2)$ | Üç elemanı iki gruba ayırma | 3 |
| $S(3,3)$ | Her elemanı ayrı gruba koyma | 1 |
| $S(n,0)$ | Pozitif sayıda elemanı sıfır gruba ayırma | 0 |
| $S(0,0)$ | Boş kümeyi sıfır gruba ayırma | 1 |

![stirling-ve-bell-71](/img/stirling-ve-bell-71.svg)


Bu sayıların temel bağıntısı şöyledir:

$$S(n,k)=kS(n-1,k)+S(n-1,k-1)$$

Bağıntının mantığını anlamak için yeni eklenen $n$'inci elemana odaklanalım. Bu eleman mevcut $k$ gruptan birine yerleşirse $kS(n-1,k)$ olasılık elde edilir. Tek başına yeni bir grup oluşturursa geriye kalan elemanların $k-1$ gruba ayrılması gerekir; bu da $S(n-1,k-1)$ seçenektir.

Kapalı form da kullanılabilir:

$$S(n,k)=\frac{1}{k!}\sum_{i=0}^{k}(-1)^{k-i}\binom{k}{i}i^n$$

Ancak programlamada özyinelemeli bağıntıyı dinamik programlamayla uygulamak çoğu zaman daha kolay ve güvenlidir.

## Bell sayıları: Kaç grup olduğunu bilmiyorsak

Grup sayısı önceden belirtilmiyorsa tüm olası $k$ değerlerini toplarız. Elde edilen sonuç **Bell sayısı**dır:

$$B_n=\sum_{k=0}^{n}S(n,k)$$

Örneğin $B_3=1+3+1=5$ olur. Yani üç elemanlı bir küme toplam beş farklı biçimde parçalanabilir. İlk değerler $B_0=1$, $B_1=1$, $B_2=2$, $B_3=5$, $B_4=15$ ve $B_5=52$ şeklindedir. Sayılar hızlı büyür; kümeler kalabalıklaştıkça kombinatorik parti kontrolden çıkar!

| Dizi | Sabit grup sayısı var mı? | Hesaplanan şey |
|---|---|---|
| Stirling $S(n,k)$ | Evet, $k$ grup | Belirli sayıdaki parçalanmalar |
| Bell $B_n$ | Hayır | Bütün parçalanmaların toplamı |

## Python ile hesaplama

Aşağıdaki fonksiyon bir tablo oluşturarak Stirling sayılarını hesaplar, ardından ilgili satırı toplayıp Bell sayısını verir:

```python
def stirling_ve_bell(n):
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    dp[0][0] = 1

    for eleman in range(1, n + 1):
        for grup in range(1, eleman + 1):
            dp[eleman][grup] = (
                grup * dp[eleman - 1][grup]
                + dp[eleman - 1][grup - 1]
            )

    return dp[n], sum(dp[n])

stirling_satiri, bell = stirling_ve_bell(5)
print(stirling_satiri)  # [0, 1, 15, 25, 10, 1]
print(bell)             # 52
```

Algoritma $O(n^2)$ zamanda ve $O(n^2)$ bellekte çalışır. Yalnızca Bell sayısı veya son satır gerekiyorsa bellek kullanımı iki satır saklanarak $O(n)$ seviyesine indirilebilir.

Bu diziler yalnızca teorik oyuncaklar değildir. Veri kümeleme, eşdeğerlik sınıfları, ağ bölümlendirme, görev gruplama ve dağıtık sistem tasarımı gibi alanlarda ortaya çıkar. Stirling sayıları “tam kaç grup?”, Bell sayıları ise “toplam kaç farklı düzen?” sorusunun zarif cevabıdır.

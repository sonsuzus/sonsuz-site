---
layout: post
title: "Nesneler Kutulara Nasıl Dağıtılır? Dört Temel Kombinatorik Senaryo"
math: true
categories: 
  - Bilgi
tags: 
  - kombinatorik
  - matematik
  - sayma
  - algoritma
  - python
  - olasılık
toc: true
image: /img/nesneler-kutulara-nasil-44.png
---

![nesneler-kutulara-nasil-44](/img/nesneler-kutulara-nasil-44.svg)


Bir çekmecedeki çorapları bölmelere, sunucudaki görevleri işlemcilere veya şekerleri çocuklara dağıttığımızı düşünelim. Bu örneklerin hepsi aynı soruya dönüşür: $n$ nesne, $m$ kutuya kaç farklı biçimde yerleştirilebilir? Ancak cevabı bulmadan önce nesnelerin ve kutuların ayırt edilip edilmediğini bilmeliyiz. Küçük bir ayrıntı gibi görünen bu özellik, sonucu üstel sayılardan bölüşüm sayılarına kadar değiştirebilir.
``
## Problemin iki kritik sorusu

Bir nesnenin ayırt edilebilir olması, ona bir kimlik verebilmemiz demektir. Örneğin Ali'nin kitabı ile Ece'nin kitabı farklıdır. Özdeş bilyeler ise ayırt edilemez. Benzer biçimde numaralandırılmış dolaplar ayırt edilebilirken aynı türden isimsiz kutular ayırt edilemez.

İkinci karar, boş kutulara izin verilip verilmediğidir. “Her kutuda en az bir nesne bulunmalı” koşulu, özellikle dahil etme–hariç tutma ve Stirling sayıları gibi araçları sahneye çıkarır.

| Nesneler | Kutular | Boş kutu serbestse | Boş kutu yasaksa |
|---|---|---:|---:|
| Ayırt edilebilir | Ayırt edilebilir | $m^n$ | $m!S(n,m)$ |
| Ayırt edilemez | Ayırt edilebilir | $\binom{n+m-1}{m-1}$ | $\binom{n-1}{m-1}$ |
| Ayırt edilebilir | Ayırt edilemez | $\sum_{k=1}^{m}S(n,k)$ | $S(n,m)$ |
| Ayırt edilemez | Ayırt edilemez | En fazla $m$ parçalı tamsayı bölüşümü | Tam $m$ parçalı tamsayı bölüşümü |

Buradaki $S(n,m)$, ikinci tür Stirling sayısıdır.

## Her şeyin etiketi varsa

Nesneler ve kutular ayırt edilebiliyorsa her nesnenin önünde $m$ bağımsız seçim bulunur. Çarpma ilkesiyle sonuç:

$$m \cdot m \cdots m=m^n$$

Örneğin üç farklı dosyayı iki farklı sunucuya dağıtmanın $2^3=8$ yolu vardır. Her sunucunun en az bir dosya alması istenirse, boş kalan kutuları çıkarmalıyız:

$$\sum_{i=0}^{m}(-1)^i\binom{m}{i}(m-i)^n=m!S(n,m)$$

Bu ifade örten fonksiyonların sayısıdır. Ayrıca $n<m$ ise bütün kutuları doldurmak imkânsızdır ve sonuç sıfır olur.

## Yıldızlar ve çubuklar

Nesneler özdeş, kutular etiketliyse dağılım şu denklemin negatif olmayan tam sayı çözümlerini saymaya dönüşür:

$$x_1+x_2+\cdots+x_m=n$$

Nesneleri yıldız, kutu sınırlarını çubuk olarak gösteririz. $n$ yıldız ile $m-1$ çubuğun sıralanması sonucu $\binom{n+m-1}{m-1}$ elde edilir. Her kutu dolu olacaksa önce her kutuya birer nesne koyarız; kalan $n-m$ nesne dağıtılır ve sonuç $\binom{n-1}{m-1}$ olur.

## Kutuların etiketi kaybolursa

Farklı nesneleri isimsiz ve boş olmayan kutulara ayırmak, bir kümenin $m$ gruba bölünmesidir. Bu nedenle cevap $S(n,m)$ olur. Stirling sayıları şu bağıntıyla hesaplanabilir:

$$S(n,m)=mS(n-1,m)+S(n-1,m-1)$$

İlk terim yeni nesnenin mevcut gruplardan birine girmesini, ikinci terim tek başına yeni bir grup oluşturmasını temsil eder.

Hem nesneler hem kutular özdeşse artık sıradan kombinasyon formülleri yetmez. Örneğin dört bilyeyi en fazla iki kutuya dağıtmak, $4$ ve $3+1$ ile $2+2$ bölüşümlerini verir. Kutuların yerini değiştirmek yeni sonuç üretmez. Bu alan, tamsayı bölüşümleriyle ilgilidir.

## Python ile Stirling hesabı

Aşağıdaki dinamik programlama kodu, farklı nesnelerin isimsiz ve boş olmayan kutulara dağılımını hesaplar:

```python
def stirling(n, m):
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 1

    for objects in range(1, n + 1):
        for boxes in range(1, min(objects, m) + 1):
            dp[objects][boxes] = (
                boxes * dp[objects - 1][boxes]
                + dp[objects - 1][boxes - 1]
            )
    return dp[n][m]

print(stirling(5, 3))  # 25
```

Dağıtım sorularında altın kural formül ezberlemek değil, önce “Kimlerin etiketi var?” ve “Boş kutu mümkün mü?” sorularını sormaktır. Doğru model seçildiğinde kutuların içindeki kombinatorik karmaşa hızla düzene girer.

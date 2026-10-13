---
layout: post
title: "Sayıların Parçalanması: Bir Doğal Sayı Kaç Farklı Toplamla Yazılır?"
math: true
categories: 
  - Program
tags: 
  - matematik
  - dinamik programlama
  - python
  - algoritma
  - sayı teorisi
toc: true
image: /img/sayilarin-parcalanmasi-bir-83.png
---

![sayilarin-parcalanmasi-bir-83](/img/sayilarin-parcalanmasi-bir-83.svg)


Bir doğal sayıyı pozitif tam sayıların toplamı olarak kaç farklı biçimde yazabiliriz? İlk bakışta basit görünen bu soru, sayı teorisinin ünlü **tam sayı parçalanması** problemidir. Örneğin 4 sayısı; $4$, $3+1$, $2+2$, $2+1+1$ ve $1+1+1+1$ biçimlerinde yazılabilir. Dolayısıyla sonuç 5’tir. Ancak sayı büyüdükçe olasılıklar roket gibi artar ve elle listeleme yöntemi hızla kullanışsız hâle gelir.

``

## Önce kuralları netleştirelim

Bu problemde sayıların sırası önemli değildir. Yani $3+1$ ile $1+3$ aynı parçalanmayı temsil eder. Ayrıca yalnızca pozitif tam sayılar kullanılır; sıfır veya negatif sayılar partiye davetli değildir.

| İfade | Ayrı çözüm mü? | Açıklama |
|---|---:|---|
| $3+1$ ve $1+3$ | Hayır | Toplananların sırası önemsizdir |
| $2+2$ | Evet | Aynı sayı birden fazla kullanılabilir |
| $4$ | Evet | Sayının kendisi de bir parçalanmadır |
| $5+(-1)$ | Hayır | Negatif parçalar kullanılamaz |

$n$ sayısının parçalanma sayısı geleneksel olarak $p(n)$ ile gösterilir. Başlangıç değeri biraz şaşırtıcıdır:

$$p(0)=1$$

Sıfırı yazmanın bir yolu olduğu kabul edilir: hiçbir sayı seçmemek. Bu tanım, dinamik programlama geçişlerini oldukça temiz hâle getirir.

## Dinamik programlama fikri

Bir `dp` dizisi oluşturalım. `dp[t]`, işlediğimiz parçaları kullanarak $t$ toplamına kaç farklı yolla ulaşabildiğimizi tutsun. Başlangıçta yalnızca `dp[0] = 1` olur.

Daha sonra kullanılabilecek her $k$ parçası için toplamları $k$ değerinden $n$ değerine kadar ilerletiriz:

$$dp[t] = dp[t] + dp[t-k]$$

Buradaki $dp[t-k]$, toplamı $t-k$ yapan mevcut çözümleri gösterir. Bu çözümlerin her birine bir adet $k$ eklediğimizde toplam $t$ olur.

Döngü sırası kritik bir ayrıntıdır. Önce parçaları, sonra toplamları dolaşırsak $1+3$ ile $3+1$ iki kez sayılmaz. Döngüleri ters çevirseydik parçalanmaları değil, sıralı toplamları hesaplamış olurduk.

| Yaklaşım | Zaman karmaşıklığı | Bellek | Özellik |
|---|---:|---:|---|
| Tüm toplamları üretme | Üstel | Yüksek | Küçük sayılarda kullanılabilir |
| İki boyutlu DP | $O(n^2)$ | $O(n^2)$ | Mantığı görselleştirmek kolaydır |
| Tek boyutlu DP | $O(n^2)$ | $O(n)$ | Pratik ve verimlidir |

## Python ile çözüm

Aşağıdaki fonksiyon, tek boyutlu dinamik programlama kullanarak sonucu hesaplar:

```python
def partition_count(n: int) -> int:
    if n < 0:
        raise ValueError("n doğal sayı olmalıdır")

    dp = [0] * (n + 1)
    dp[0] = 1

    # Kullanılabilecek her pozitif parçayı sırayla işliyoruz.
    for part in range(1, n + 1):
        for total in range(part, n + 1):
            dp[total] += dp[total - part]

    return dp[n]

for number in range(1, 8):
    print(number, partition_count(number))
```

Program sırasıyla $1, 2, 3, 5, 7, 11, 15$ sonuçlarını üretir. Örneğin `partition_count(5)` değeri 7’dir. `dp` dizisinin her güncellemesi, yeni bir parçanın mevcut kombinasyonlara eklenmesini temsil eder.

## Parçalanmaları gerçekten listelemek

Yalnızca sayıyı bulmak yerine toplamları görmek istersek geri izlemeli bir fonksiyon kullanabiliriz:

```python
def generate_partitions(n, maximum=None):
    if n == 0:
        yield []
        return

    maximum = n if maximum is None else min(maximum, n)
    for part in range(maximum, 0, -1):
        for rest in generate_partitions(n - part, part):
            yield [part] + rest

print(list(generate_partitions(5)))
```

`maximum` parametresi, sonraki parçanın önceki parçadan büyük olmasını engeller. Böylece sonuçlar azalan sırada üretilir ve aynı toplamın farklı permütasyonları tekrarlanmaz. Bu yöntem öğreticidir; fakat bütün sonuçları oluşturduğu için büyük $n$ değerlerinde pahalıdır.

Tam sayı parçalanması; para üstü hesaplama, kombinatorik, üretici fonksiyonlar ve dinamik programlama arasında güçlü bir köprü kurar. Küçük bir toplama sorusu gibi başlayan macera, algoritmaların neden doğru döngü sırasına ihtiyaç duyduğunu gösteren şahane bir örneğe dönüşür.

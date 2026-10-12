---
layout: post
title: "Collatz Problemi: 3n+1 ile Sonsuzluğa Açılan Matematik Bilmecesi"
math: true
categories: 
  - Bilgi
tags: 
  - collatz
  - matematik
  - algoritma
  - python
  - sayı teorisi
  - varsayım
toc: true
image: /img/collatz-problemi-3n1-78.png
---

Bir pozitif tam sayı seçin. Çiftse ikiye bölün, tekse üçle çarpıp bir ekleyin ve aynı işlemi tekrarlayın. Çocuk oyuncağı kadar basit görünen bu tarif, matematikçilerin onlarca yıldır çözemediği Collatz varsayımını oluşturur. Bilgisayarlar akıl almaz büyüklükte sayıları sınamış olsa da her başlangıç değerinin sonunda 1'e ulaşacağını kanıtlayan genel bir ispat hâlâ bulunamamıştır.

``

## Kural tam olarak nedir?

1937 yılında Alman matematikçi Lothar Collatz tarafından ortaya atılan problem, pozitif tam sayılar üzerinde çalışan bir fonksiyonla tanımlanır:

$$
C(n)=
\begin{cases}
n/2, & n \text{ çiftse} \\
3n+1, & n \text{ tekse}
\end{cases}
$$

Elde edilen sonuç tekrar aynı fonksiyona verilir. Varsayım, hangi pozitif $n$ değeriyle başlanırsa başlansın dizinin sonunda $1$ sayısına ulaşacağını söyler. Bir kez 1'e gelindiğinde $1 \rightarrow 4 \rightarrow 2 \rightarrow 1$ döngüsü oluşur.

| Başlangıç türü | Uygulanan işlem | İlk sonucun özelliği |
|---|---:|---|
| Çift $n$ | $n/2$ | Sayı kesinlikle küçülür |
| Tek $n$ | $3n+1$ | Sonuç çift ve genellikle daha büyüktür |
| $n=1$ | $3(1)+1=4$ | Ana döngü başlar |

![collatz-problemi-3n1-78](/img/collatz-problemi-3n1-78.svg)


Tek sayıdan sonra sonucun çift olması önemlidir. Çünkü $3n+1$ ifadesinde hem $3n$ hem de $n$ tek olduğundan sonuç çifttir; böylece sonraki adımda bölme işlemi garanti edilir.

## Küçük sayı, uzun macera

Örneğin $n=6$ ile başlayalım:

$$6 \rightarrow 3 \rightarrow 10 \rightarrow 5 \rightarrow 16 \rightarrow 8 \rightarrow 4 \rightarrow 2 \rightarrow 1$$

Daha şaşırtıcı bir örnek 27'dir. Dizi hızla küçülmek yerine 9232'ye kadar yükselir ve 1'e ulaşması 111 adım sürer. Yani başlangıç sayısının küçük olması, yolculuğun kısa olacağı anlamına gelmez.

| Başlangıç | 1'e ulaşma adımı | Yolculuktaki en büyük değer |
|---:|---:|---:|
| 6 | 8 | 16 |
| 12 | 9 | 16 |
| 27 | 111 | 9232 |

Bu düzensiz davranış, problemi kaotik bir labirente dönüştürür. Bazı adımlar sayıyı küçültürken bazıları aniden büyütür; yerel hareketlere bakarak uzun vadeli sonucu kestirmek kolay değildir.

## Neden ispatlamak bu kadar zor?

Deneysel doğrulama ile matematiksel ispat aynı şey değildir. Bir bilgisayar ilk trilyonlarca başlangıç değerini kontrol edebilir; ancak pozitif tam sayılar sonsuzdur. Kontrol edilmeyen tek bir sayı bile sonsuza kaçabilir veya 1'i içermeyen farklı bir döngüye girebilir.

Sezgisel olarak tek bir adımdan ziyade, tek sayıdan sonraki bölmeleri birlikte düşünebiliriz. $3n+1$ sonucu bazen 2'ye, bazen $4$, $8$ veya daha büyük bir iki kuvvetine bölünür. Kabaca rastgelelik varsayılırsa bölmelerin uzun vadede büyümeyi dengelemesi beklenir. Fakat “beklenir” sözcüğü ispat değildir; adımlar birbirinden bağımsız rastgele olaylar değildir.

## Python ile Collatz yolculuğu

Aşağıdaki fonksiyon diziyi üretir, tekrar eden bir değer görürse durur. Böylece hem 1 döngüsü hem de varsayımsal başka döngüler yakalanabilir:

```python
def collatz_sequence(start, limit=10_000):
    if start <= 0:
        raise ValueError('Pozitif bir tam sayı girilmeli.')

    sequence = []
    seen = set()
    n = start

    while n not in seen and len(sequence) < limit:
        sequence.append(n)
        seen.add(n)

        if n == 1:
            break
        n = n // 2 if n % 2 == 0 else 3 * n + 1

    return sequence

path = collatz_sequence(27)
print('Adım sayısı:', len(path) - 1)
print('En büyük değer:', max(path))
```

`seen` kümesi daha önce ziyaret edilen değerleri hızlıca denetler. `limit` ise beklenmedik derecede uzun bir yürüyüşün programı süresiz çalıştırmasını engeller. Bu kod örnekleri test eder, fakat genel bir kanıt üretmez.

## Basitlik neden yanıltıcıdır?

Collatz problemi, kolay ifade edilmenin kolay çözülmek anlamına gelmediğini gösterir. Ortada yalnızca çarpma, toplama ve bölme vardır; buna rağmen işlemlerin birleşimi öngörülmesi güç küresel bir davranış doğurur. Belki bütün diziler 1'e iner, belki erişilmesi inanılmaz zor bir karşı örnek vardır. İşte bu belirsizlik, $3n+1$ bilmecesini sayı teorisinin en eğlenceli ve inatçı problemlerinden biri yapar.

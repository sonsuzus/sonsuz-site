---
layout: post
title: "Regex Motorunun Perde Arkası: Düzenli İfadeden NFA Simülasyonuna"
math: true
categories: 
  - Bilgi
tags: 
  - regex
  - nfa
  - sonlu-durum-otomatı
  - algoritma
  - biçimsel-diller
  - python
toc: true
image: /img/regex-motorunun-perde-56.png
---

Bir düzenli ifade yazıp eşleşme arattığımızda küçük bir sihir gerçekleşir: Metinsel desen, durumlar ve geçişlerden oluşan matematiksel bir makineye dönüştürülür. Özellikle klasik regex motorlarında bu makine çoğunlukla bir **belirsiz sonlu durum otomatıdır**, yani NFA'dır. Gelin `(a|b)*abb` ifadesinin bir metni nasıl adım adım tükettiğini ve motorun arka planda hangi durumları takip ettiğini keşfedelim.

![regex-motorunun-perde-56](/img/regex-motorunun-perde-56.svg)


``

## Regex ile otomat arasındaki köprü

Düzenli ifadeler ve sonlu durum otomatları aynı dil sınıfını, yani **düzenli dilleri** tanımlar. Başka bir deyişle her regex için eşdeğer bir sonlu durum otomatı, her sonlu durum otomatı için de eşdeğer bir regex oluşturulabilir.

Bir NFA matematiksel olarak şu beşliyle gösterilir:

$$N = (Q, \Sigma, \delta, q_0, F)$$

Burada $Q$ durum kümesi, $\Sigma$ alfabe, $\delta$ geçiş fonksiyonu, $q_0$ başlangıç durumu ve $F$ kabul durumlarıdır. NFA'nın ayırt edici özelliği, aynı karakter için birden fazla geçiş yapabilmesi ve hiçbir karakter tüketmeden ilerleyen $\varepsilon$ geçişlerine izin vermesidir.

| Özellik | NFA | DFA |
|---|---|---|
| Bir sembolde olası geçiş | Bir veya daha fazla | Tam olarak bir |
| $\varepsilon$ geçişi | Var olabilir | Yoktur |
| Oluşturma maliyeti | Genellikle kolay | Durum sayısı büyüyebilir |
| Çalıştırma yaklaşımı | Durum kümesi izlenir | Tek durum izlenir |

## Regex nasıl NFA'ya çevrilir?

Yaygın yöntemlerden biri **Thompson yapımıdır**. Önce regex ayrıştırılır ve bir sözdizimi ağacı oluşturulur. Ardından her parça küçük bir NFA üretir:

- `a` gibi bir sembol, iki durum arasında `a` geçişi oluşturur.
- `A|B`, iki seçeneğe $\varepsilon$ geçişleriyle dallanır.
- `AB`, A'nın kabul durumunu B'nin başlangıcına bağlar.
- `A*`, sıfır veya daha fazla tekrar için ileri ve geri $\varepsilon$ geçişleri ekler.

Örneğin `(a|b)*abb`, önce `a|b` seçimini kurar, yıldız sayesinde bu seçimi döngüye alır ve sonuna sırasıyla `a`, `b`, `b` geçişlerini bağlar. Ortaya çıkan grafik ilk bakışta kablo yumağına benzese de her parça tek bir regex operatörünün mekanik karşılığıdır.

## NFA nasıl çalıştırılır?

Motor yalnızca tek bir durumu değil, o anda erişilebilir **durumlar kümesini** saklar. Başlangıçta $q_0$ durumunun epsilon kapanışı hesaplanır. Epsilon kapanışı, karakter tüketmeden ulaşılabilen bütün durumlardır:

$$E(S)=\{q \mid q,\ S\text{'deki bir durumdan yalnızca }\varepsilon\text{ geçişleriyle erişilebilir}\}$$

Her giriş karakteri için önce o karakterle gidilebilen durumlar bulunur, sonra yeniden epsilon kapanışı alınır. Girdi bittiğinde kümede bir kabul durumu varsa eşleşme başarılıdır.

Aşağıdaki Python kodu, geçişleri önceden hazırlanmış bir NFA'yı simüle eder:

```python
def epsilon_closure(states, transitions):
    closure = set(states)
    stack = list(states)

    while stack:
        state = stack.pop()
        for target in transitions.get((state, None), []):
            if target not in closure:
                closure.add(target)
                stack.append(target)
    return closure


def matches(text, start, accepting, transitions):
    current = epsilon_closure({start}, transitions)

    for char in text:
        next_states = set()
        for state in current:
            next_states.update(transitions.get((state, char), []))
        current = epsilon_closure(next_states, transitions)

        if not current:
            return False

    return bool(current & accepting)
```

Burada `None`, $\varepsilon$ geçişini temsil eder. `epsilon_closure` görünmez geçişleri dolaşırken `matches`, her karakterden sonra mümkün durumları günceller. Hiç durum kalmazsa motor erken çıkar; kabul kümesiyle kesişim varsa desen eşleşmiştir.

## Neden bu yaklaşım önemli?

Thompson NFA simülasyonu, giriş uzunluğu $n$ ve otomat durum sayısı $m$ olduğunda kabaca $O(nm)$ zamanda çalışır. Klasik geri izlemeli motorlarda görülebilen felaket düzeyindeki üstel davranıştan kaçınır. Ancak geri referanslar gibi bazı modern regex özellikleri düzenli dil sınırlarını aştığından saf NFA ile modellenemez.

Kısacası regex motoru desen üzerinde rastgele tahmin yürütmez; olası yolları kümeler halinde taşıyan disiplinli bir otomat çalıştırır. Ekranda birkaç karakter görürüz, arka planda ise matematik, grafikler ve oldukça hareketli bir durum partisi vardır.

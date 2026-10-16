---
layout: post
title: "C++ Yapıcılarında Sessiz Tuzak: Üyeler Hangi Sırayla İlklendirilir?"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - oop
  - constructor
  - başlatma-sırası
  - hata-ayıklama
toc: true
image: /img/c-yapicilarinda-sessiz-29.png
---

Bir C++ yapıcısındaki üye ilklendirme listesi soldan sağa okunur. Bu nedenle üyelerin de aynı sırayla hazırlandığını düşünmek oldukça doğaldır. Ne var ki C++, görünüşe değil sınıftaki **bildirim sırasına** bakar. Listeyi istediğiniz kadar yeniden düzenleyin; gerçek ilklendirme sırası değişmez. Bu küçük kural, tanımsız davranıştan zor fark edilen mantık hatalarına kadar uzanan sürprizler yaratabilir.


![c-yapicilarinda-sessiz-29](/img/c-yapicilarinda-sessiz-29.svg)

``

## Temel kural

Bir nesne oluşturulurken sıra genel olarak şöyledir:

1. Sanal taban sınıflar,
2. Doğrudan taban sınıflar,
3. Üye değişkenler — sınıf gövdesindeki bildirim sırasıyla,
4. Yapıcı gövdesi.

Üye ilklendirme listesindeki yazım sırası yalnızca görseldir. Örneğin aşağıdaki sınıfta `value`, listede önce görünmesine rağmen ilk hazırlanan üye değildir:

```cpp
class Measurement {
    int doubled;
    int value;

public:
    Measurement(int input)
        : value(input), doubled(value * 2) {}
};
```

Derleyicinin izlediği mantık, kabaca şuna denktir:

```cpp
Measurement(int input)
    : doubled(value * 2), // value henüz ilklendirilmedi!
      value(input) {}
```

`doubled`, sınıf içinde önce bildirildiği için önce ilklendirilir. Bu sırada `value` henüz geçerli bir değere sahip değildir. İlklendirilmemiş değerin okunması programı tanımsız davranış bölgesine taşır. Sonucun bazen `42` çıkması kodu doğru yapmaz; yalnızca hatayı daha sinsi hâle getirir.

## Beklenti ve gerçeklik

| Durum | Geliştiricinin beklentisi | C++ davranışı |
|---|---|---|
| Listede `a` önce yazılmış | `a` önce hazırlanır | Bildirim sırasına bakılır |
| `b`, `a` değerini kullanıyor | Liste doğruysa güvenlidir | `a` önce bildirilmiş olmalıdır |
| Yapıcı gövdesinde atama | İlklendirme ile aynıdır | Önce varsayılan ilklendirme, sonra atama olur |
| Liste sırası değiştirildi | Çalışma sırası değişir | Yalnızca kodun görünümü değişir |

Bağımlılığı matematiksel olarak şöyle ifade edebiliriz:

$$b = f(a)$$

Eğer `b` ilklendirilirken `a` kullanılacaksa gerekli koşul şudur:

$$order(a) < order(b)$$

Buradaki `order`, ilklendirme listesindeki konumu değil, **sınıftaki bildirim konumunu** temsil eder.

## Doğru çözüm

Bağımlılıkları bildirim sırasına yansıtın ve ilklendirme listesini de aynı sırada yazın:

```cpp
class Measurement {
    int value;
    int doubled;

public:
    explicit Measurement(int input)
        : value(input), doubled(value * 2) {}
};
```

Artık önce `value`, ardından ona bağımlı olan `doubled` hazırlanır. Listeyi bildirim sırasıyla eşleştirmek dil tarafından zorunlu tutulmasa da insan okuyucular ve kod incelemeleri açısından güçlü bir alışkanlıktır.

## Daha gerçekçi bir tuzak

Aynı sorun kaynak yöneten sınıflarda da görülebilir:

```cpp
class BufferView {
    const char* data;
    std::string storage;

public:
    explicit BufferView(std::string text)
        : storage(std::move(text)), data(storage.data()) {}
};
```

`data`, `storage` nesnesinden önce bildirildiği için `storage` oluşturulmadan önce onun `data()` fonksiyonu çağrılmaya çalışılır. Çözüm, `storage` üyesini yukarı taşımaktır. Bağımlı üye her zaman bağımlılık duyduğu üyeden sonra bildirilmelidir.

## Derleyiciyi yanınıza alın

GCC ve Clang, `-Wall -Wextra -Wreorder` seçenekleriyle liste ve bildirim sırası uyuşmazlıklarını yakalayabilir:

```bash
g++ -std=c++20 -Wall -Wextra -Wreorder main.cpp
```

Bu uyarıları susturmak yerine tasarımı gözden geçirin. Kısa kontrol listesi şudur:

- Üyeleri bağımlılık sırasıyla bildirin.
- İlklendirme listesini aynı sırada yazın.
- Bir üyeyi, daha sonra bildirilen başka bir üyeden üretmeyin.
- Uyarıları CI sürecinde mümkünse hata kabul edin.

Özetle C++, yapıcı listesini bir yürütme planı olarak değil, her üye için ilklendirici kataloğu olarak görür. Gerçek plan sınıf bildiriminin içinde çoktan yazılmıştır.

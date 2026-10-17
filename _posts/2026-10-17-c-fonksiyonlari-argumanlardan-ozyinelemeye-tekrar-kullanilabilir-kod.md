---
layout: post
title: "C Fonksiyonları: Argümanlardan Özyinelemeye Tekrar Kullanılabilir Kod"
math: true
categories: 
  - Bilgi
tags: 
  - c
  - fonksiyonlar
  - programlama
  - özyineleme
  - algoritma
  - parametreler
toc: true
image: /img/c-fonksiyonlari-argumanlardan-91.png
---

C programlarında her işi `main` fonksiyonuna yüklemek, bütün eşyaları tek çekmeceye doldurmaya benzer: Başlangıçta kolay görünür, fakat aradığını bulmak kısa sürede işkenceye dönüşür. Fonksiyonlar, büyük problemleri adlandırılmış ve tekrar kullanılabilir küçük parçalara ayırır. Böylece kod daha okunabilir, test edilebilir ve değiştirilebilir hâle gelir.


![c-fonksiyonlari-argumanlardan-91](/img/c-fonksiyonlari-argumanlardan-91.svg)

``

## Fonksiyonun anatomisi

Bir C fonksiyonu dönüş türü, ad, parametre listesi ve gövdeden oluşur. Fonksiyon kullanılmadan önce derleyicinin onun imzasını bilmesi gerekir. Bu nedenle prototipler çoğunlukla dosyanın üst bölümünde veya bir başlık dosyasında bulunur.

```c
#include <stdio.h>

int maksimum(int a, int b);  // Fonksiyon prototipi

int main(void) {
    int sonuc = maksimum(12, 7);
    printf("Büyük değer: %d\n", sonuc);
    return 0;
}

int maksimum(int a, int b) {
    return (a > b) ? a : b;
}
```

Burada `a` ve `b` birer **parametre**, çağrıdaki `12` ve `7` ise **argümandır**. `int` dönüş türü, fonksiyonun çağırana bir tam sayı göndereceğini belirtir. Değer döndürmeyen fonksiyonlarda `void` kullanılır.

| Kavram | Görevi | Örnek |
|---|---|---|
| Prototip | Fonksiyonun imzasını bildirir | `int maksimum(int, int);` |
| Parametre | Fonksiyonun aldığı yerel değişkendir | `int a` |
| Argüman | Çağrı sırasında gönderilen değerdir | `maksimum(12, 7)` |
| Dönüş değeri | Sonucu çağırana iletir | `return a;` |

## C'de argüman aktarımı

C, argümanları varsayılan olarak **değer ile** aktarır. Yani fonksiyon, özgün değişkenin kendisini değil kopyasını alır. Matematiksel olarak bunu $p = x$ biçiminde düşünebiliriz: `p` başlangıçta `x` ile aynı değere sahiptir, ancak ayrı bir saklama alanıdır.

```c
void arttir(int sayi) {
    sayi++;
}
```

Bu fonksiyon çağıranın değişkenini değiştirmez. Kalıcı değişiklik için değişkenin adresi, yani bir işaretçi aktarılır:

```c
void arttir(int *sayi) {
    (*sayi)++;
}

int main(void) {
    int puan = 10;
    arttir(&puan);  // puan artık 11
    return 0;
}
```

`&puan` değişkenin adresini verir; `*sayi` ise o adresteki değere erişir. Diziler fonksiyonlara gönderildiğinde ilk elemanlarının adresine dönüştükleri için yapılan değişiklikler özgün dizi üzerinde görülebilir.

| Yaklaşım | Fonksiyona giden | Özgün veri değişir mi? | Kullanım |
|---|---|---:|---|
| Değer aktarımı | Verinin kopyası | Hayır | Küçük ve salt okunur veriler |
| İşaretçi aktarımı | Bellek adresi | Evet | Çıktı üretme, dizi veya yapı güncelleme |

İşaretçiler güçlüdür; fakat `NULL` adresler ve geçersiz bellek erişimleri kontrol edilmezse programı beklenmedik bir maceraya çıkarabilir.

## Özyineleme: Fonksiyonun kendisini çağırması

Özyinelemeli bir fonksiyon problemi daha küçük bir örneğine dönüştürerek kendisini çağırır. Her özyinelemede iki parça zorunludur: çağrıları durduran **taban durum** ve problemi küçülten **özyinelemeli adım**.

Faktöriyel matematiksel olarak şöyle tanımlanır:

$$n! = n \times (n-1)!, \quad 0! = 1$$

```c
unsigned long long faktoriyel(unsigned int n) {
    if (n == 0) {              // Taban durum
        return 1;
    }
    return n * faktoriyel(n - 1); // Daha küçük problem
}
```

`faktoriyel(4)` çağrısı, $4 \times 3 \times 2 \times 1$ sonucunu üretir. Her çağrı dönüş adresi ve yerel değişkenleriyle çağrı yığınına eklenir. Taban durum unutulursa çağrılar sürer ve sonunda **stack overflow** oluşabilir.

Bu örneğin zaman karmaşıklığı $T(n)=T(n-1)+O(1)$ olduğundan $O(n)$, çağrı yığını kullanımı da $O(n)$ olur. Döngülü sürüm aynı zaman karmaşıklığıyla genellikle $O(1)$ ek bellek tüketir. Buna karşılık ağaç dolaşma, böl-ve-yönet ve iç içe geçmiş yapılar özyineleme ile daha doğal ifade edilebilir.

Fonksiyon tasarlarken tek sorumluluk ilkesini benimsemek, açıklayıcı adlar seçmek ve gereksiz küresel değişkenlerden kaçınmak önemlidir. Kısacası fonksiyonlar yalnızca kod tekrarını azaltmaz; programın düşünce haritasını da oluşturur. İyi bölünmüş bir C programı, hem derleyicinin hem de gelecekteki sizin teşekkür edeceği bir programdır.

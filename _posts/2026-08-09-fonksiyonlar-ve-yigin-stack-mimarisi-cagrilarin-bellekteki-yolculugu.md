---
layout: post
title: "Fonksiyonlar ve Yığın (Stack) Mimarisi: Çağrıların Bellekteki Yolculuğu"
math: true
categories: 
  - Bilgi
tags: 
  - fonksiyonlar
  - stack
  - bellek yönetimi
toc: true
image: /img/fonksiyonlar-ve-yigin-81.png
---

Fonksiyonlar, büyük bir programı yönetilebilir görevlere ayırır; yığın (stack) ise bu görevlerin kim tarafından, hangi parametrelerle ve nereye dönmek üzere çağrıldığını düzenler. Bir fonksiyon çağrısı yalnızca kodun başka bir satıra atlaması değildir: İşletim sistemi, derleyici ve işlemci birlikte çalışarak geçici veriler için düzenli bir bellek kaydı oluşturur. Bu mekanizma sayesinde iç içe çağrılar, özyineleme ve yerel değişkenler güvenle yönetilir.

``

## Yığın neden gereklidir?

Programın belleği kavramsal olarak kod, global veri, heap ve stack gibi bölümlere ayrılır. Heap dinamik olarak oluşturulan ve ömrü programcının ya da çöp toplayıcının kontrolündeki nesneler içindir. Stack ise fonksiyon çağrılarının doğal **LIFO** (Last In, First Out — son giren ilk çıkar) düzenini izler. `main()` içinden `A()`, onun içinden de `B()` çağrılırsa, önce `B()` bitmek zorundadır.

Her çağrıda stack üzerinde bir **stack frame** (çağrı çerçevesi) oluşturulur. Bu çerçeve tipik olarak dönüş adresini, parametreleri, yerel değişkenleri, kaydedilmiş kayıtçıları ve hizalama için ayrılan alanı içerir. Stack işaretçisi `$SP`, yığının güncel tepesini; frame pointer ise çoğu mimaride mevcut çerçevenin sabit bir referans noktasını gösterir.

\vert  Bellek bölgesi \vert  Temel kullanım \vert  Ömür \vert  Yönetim \vert 
\vert ---\vert ---\vert ---\vert ---\vert 
\vert  Kod bölgesi \vert  Derlenmiş komutlar \vert  Program boyunca \vert  İşletim sistemi / yükleyici \vert 
\vert  Global veri \vert  Global ve statik değişkenler \vert  Program boyunca \vert  Çalışma zamanı \vert 
\vert  Heap \vert  Dinamik nesneler \vert  İhtiyaca bağlı \vert  `malloc/free` veya GC \vert 
\vert  Stack \vert  Çağrılar ve yerel veriler \vert  Fonksiyon bitene kadar \vert  Otomatik \vert 

## Bir çağrının anatomisi

Örneğin aşağıdaki C kodunda `topla`, iki parametre alır ve sonucu çağırana döndürür:

```c
int topla(int a, int b) {
    int araSonuc = a + b;
    return araSonuc;
}

int main(void) {
    int sonuc = topla(7, 5);
    return sonuc;
}
```

`main`, `topla(7, 5)` çağrısını hazırlarken parametreleri ilgili kayıtçılara veya mimarinin çağrı sözleşmesine göre stack'e yerleştirir. Ardından dönüş adresini saklayarak `topla` koduna dallanır. Fonksiyon kendi yerel alanını ayırır, toplamayı yapar ve dönüş değerini genellikle belirlenmiş bir kayıtçıyla iletir. Son olarak frame temizlenir; işlemci dönüş adresine gider.

Basitleştirilmiş yığın görünümü şöyledir:

```text
Yüksek adresler
+-------------------+
\vert  main'in frame'i   \vert 
+-------------------+
\vert  dönüş adresi      \vert 
\vert  kaydedilmiş kayıt \vert 
\vert  yerel: araSonuc   \vert  <- topla'nın frame'i
+-------------------+
Düşük adresler
```

Çoğu modern sistemde stack düşük adreslere doğru büyür. Bu evrensel bir zorunluluk değildir; önemli olan derleyici, ABI (Application Binary Interface) ve işlemcinin aynı sözleşmeyi izlemesidir. Bir frame için kabaca şu ilişki düşünülebilir:

$$S_{yeni} = S_{eski} - (P + L + R + A)$$

Burada $P$ parametre alanı, $L$ yerel değişkenler, $R$ saklanan kayıtçılar ve $A$ hizalama boşluğudur.

## Parametreler nasıl aktarılır?

Çağrı sözleşmesi, parametrelerin nerede duracağını ve kimin temizleme yapacağını belirler. Güncel 64-bit mimariler ilk birkaç parametreyi kayıtçılarla aktararak bellek erişimini azaltır; fazlası stack'e taşar. Kayıtçıların sınırlı olması, büyük yapıların veya çok sayıda argümanın stack kullanımını hâlâ gerekli kılar.

\vert  Yaklaşım \vert  Avantaj \vert  Dikkat edilmesi gereken \vert 
\vert ---\vert ---\vert ---\vert 
\vert  Kayıtçı ile aktarım \vert  Hızlı, az bellek erişimi \vert  Kayıtçı sayısı sınırlıdır \vert 
\vert  Stack ile aktarım \vert  Çok sayıda argümanı destekler \vert  Daha fazla bellek trafiği \vert 
\vert  Değer ile aktarım \vert  Çağıranın verisi korunur \vert  Büyük veriler kopyalanabilir \vert 
\vert  Referans/işaretçi ile aktarım \vert  Kopyalama maliyeti düşer \vert  Yan etkiler oluşabilir \vert 

Özyinelemeli fonksiyonlar stack'in önemini dramatik biçimde gösterir. Her `faktoriyel(n)` çağrısı ayrı bir frame açar; dolayısıyla bellek tüketimi yaklaşık olarak $O(n)$ olur. Kontrolsüz derinlik, **stack overflow** üretir. Ayrıca bir fonksiyondan yerel dizinin adresini döndürmek tehlikelidir: Fonksiyon bittiğinde frame geçersizdir.

Özetle stack, modüler programlamanın görünmez sahne amiridir. Fonksiyonlar arası geçişi, dönüşü ve geçici verileri disiplinli biçimde düzenler. Bu yapıyı anlamak; performans analizi, hata ayıklama, güvenli kod yazımı ve assembly seviyesindeki davranışı yorumlama için güçlü bir temel sağlar.

![fonksiyonlar-ve-yigin-81](/img/fonksiyonlar-ve-yigin-81.svg)


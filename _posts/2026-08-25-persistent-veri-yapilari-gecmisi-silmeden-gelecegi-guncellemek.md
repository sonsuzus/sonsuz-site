---
layout: post
title: "Persistent Veri Yapıları: Geçmişi Silmeden Geleceği Güncellemek"
math: true
categories: 
  - Bilgi
tags: 
  - veri yapıları
  - algoritmalar
  - fonksiyonel programlama
---

Bir diziyi güncellediğinizde eski hâlinin de erişilebilir kaldığını hayal edin: hata ayıklamada zaman yolculuğu, sürüm kontrolünde anlık geri alma ve eşzamanlı işlemlerde daha güvenli okuma mümkün olur. Persistent (kalıcı) veri yapıları tam olarak bunu sağlar. Buradaki “kalıcı” ifadesi diske yazılmayı değil, bir güncelleme sonrasında önceki mantıksal sürümlerin yaşamaya devam etmesini anlatır.
``

Klasik, yani **ephemeral** veri yapısında `push`, `insert` veya `update` işlemi nesneyi yerinde değiştirir. Eski değerler kaybolur. Persistent yaklaşımda ise her güncelleme yeni bir sürüm üretir. Kritik fikir, tüm yapıyı kopyalamak değildir; değişmeyen bölümler sürümler arasında **paylaşılır**. Buna yapısal paylaşım (*structural sharing*) denir.

| Özellik | Geçici yapı | Persistent yapı |
|---|---|---|
| Güncelleme | Mevcut nesneyi değiştirir | Yeni sürüm döndürür |
| Eski sürüm | Kaybolabilir | Erişilebilir kalır |
| Bellek | Tek anlık durum için düşük | Paylaşımla kontrollü ek maliyet |
| Hata ayıklama | Geçmişi yeniden üretmek gerekir | Eski sürüm doğrudan incelenir |

En basit örnek bağlı listedir. Listenin başına eleman eklemek için eski listeyi değiştirmeye gerek yoktur: yeni düğümün `next` alanı eski başı gösterir. Dolayısıyla `O(1)` zamanda yeni bir sürüm oluşur ve iki sürümün kuyruğu ortaktır.

```javascript
class Node {
  constructor(value, next = null) {
    this.value = value;
    this.next = next;
    Object.freeze(this); // Kazara yerinde değişikliği engeller
  }
}

function push(stack, value) {
  return new Node(value, stack);
}

function pop(stack) {
  if (!stack) throw new Error("Boş yığın");
  return { value: stack.value, rest: stack.next };
}

const v1 = push(null, "A");
const v2 = push(v1, "B");
// v1 hâlâ yalnızca A'yı, v2 ise B -> A zincirini temsil eder.
```

Bu kodda `push`, eski `stack`i mutasyona uğratmaz. Yalnızca bir düğüm ayırır. Ancak dizideki `i` indisli elemanı değiştirmek daha ilginçtir. Basitçe tüm diziyi kopyalamak `O(n)` maliyetlidir. Persistent segment tree gibi ağaç tabanlı yapılarda yalnızca kökten değişen yaprağa giden yol kopyalanır. Ağacın yüksekliği $h = O(\log n)$ olduğundan, hem güncelleme hem de sürüm başına ek düğüm maliyeti yaklaşık $O(\log n)$ olur.

Bir tam ikili ağaçta $n$ yaprak bulunduğunu düşünelim. Bir güncelleme yalnızca $\log_2 n$ düğümün yeniden kurulmasını gerektirir; diğer alt ağaçlar önceki sürümle paylaşılır. $k$ güncelleme sonrasında kaba bellek maliyeti şu şekilde ifade edilebilir:

$$M \approx M_0 + k \cdot O(\log n)$$

Bu sonuç, her sürüm için $O(n)$ kopya tutmaktan çok daha verimlidir.

| Kalıcılık türü | Eski sürümde okuma | Eski sürümde güncelleme | Tipik kullanım |
|---|---|---|---|
| Partial persistence | Evet | Hayır | Sürüm geçmişi, undo |
| Full persistence | Evet | Evet | Dallanabilen geçmişler |
| Confluent persistence | Evet | Evet, sürümler birleştirilebilir | İleri seviye sürüm sistemleri |

Tasarımda iki tuzak vardır. İlk olarak, paylaşılan düğümlerin gerçekten değişmez olması gerekir; aksi hâlde bir sürümü düzenlemek diğerlerini gizlice bozar. İkinci olarak, küçük nesnelerin çok sayıda oluşturulması çöp toplayıcı üzerinde baskı yaratabilir. Bu nedenle vektör trie, HAMT ve persistent red-black tree gibi dengeli yapılar pratikte önem kazanır.

Persistent veri yapıları özellikle fonksiyonel programlamada doğal görünür; çünkü fonksiyonlar yan etkisiz değerler döndürmeye yatkındır. Yine de yalnızca akademik bir fikir değildir: editörlerin undo geçmişi, zaman bazlı sorgular, durum yönetim kütüphaneleri ve blokzincir benzeri kayıt sistemleri bu yaklaşımın farklı yüzleridir. Özetle hedef, geçmişi saklamak uğruna her şeyi çoğaltmak değil; değişen küçük yolu kopyalayıp değişmeyen büyük kısmı akıllıca paylaşmaktır.

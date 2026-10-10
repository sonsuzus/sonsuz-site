---
layout: post
title: "Yığın ve Kuyruk Veri Yapılarının Temelleri: LIFO ve FIFO’yu Kodlamak"
math: true
categories: 
  - Bilgi
tags: 
  - veri yapıları
  - yığın
  - kuyruk
  - lifo
  - fifo
  - python
  - algoritmalar
toc: true
image: /img/yigin-ve-kuyruk-54.png
---

Bir kafede sıraya giren müşterileri ve masanın üzerinde üst üste duran tabakları düşünün. Müşteriler geliş sırasına göre hizmet alırken tabaklardan önce en üstteki kaldırılır. Bilgisayar biliminde bu iki gündelik düzen, **kuyruk (queue)** ve **yığın (stack)** veri yapılarıyla modellenir. Basit görünmelerine rağmen işletim sistemlerinden tarayıcılara, oyunlardan mesajlaşma servislerine kadar pek çok yazılımın arkasında bu yapılar çalışır.
``
## Temel mantık: LIFO ve FIFO

Yığın, **LIFO** (*Last In, First Out — Son Giren, İlk Çıkar*) prensibini kullanır. Yığına son eklenen eleman, çıkarılacak ilk elemandır. Matematiksel olarak ekleme işlemini $push(S, x)$, çıkarma işlemini $pop(S)$ ile gösterirsek:

$$pop(push(S, x)) = x$$

Bu davranış, üst üste konmuş tabaklara benzer. Aradaki tabağı doğrudan almak yerine önce üstündekileri kaldırmanız gerekir.

Kuyruk ise **FIFO** (*First In, First Out — İlk Giren, İlk Çıkar*) prensibiyle çalışır. Kuyruğa önce eklenen eleman önce çıkar:

$$dequeue(enqueue(Q, x)) = x$$

Elbette bu eşitlik, işlem sırasında kuyrukta daha eski bir eleman bulunmadığı durumda geçerlidir. Gerçek hayattaki bilet sırası bunun en anlaşılır örneğidir.

| Özellik | Yığın (Stack) | Kuyruk (Queue) |
|---|---|---|
| Temel ilke | LIFO | FIFO |
| Ekleme | `push` | `enqueue` |
| Çıkarma | `pop` | `dequeue` |
| Erişim noktası | Aynı uç | Ön ve arka uçlar |
| Gerçek dünya örneği | Tabak yığını | Müşteri sırası |
| Yazılım örneği | Geri alma sistemi | Yazdırma görevleri |

## Python ile yığın oluşturmak

Python listeleri, sona eleman ekleme ve sondan eleman çıkarma işlemlerini verimli biçimde destekler. Her iki işlemin ortalama zaman karmaşıklığı $O(1)$ olur.

```python
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError('Yığın boş!')
        return self.items.pop()

    def peek(self):
        return None if self.is_empty() else self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

stack = Stack()
stack.push('Ana sayfa')
stack.push('Ürünler')
stack.push('Sepet')
print(stack.pop())  # Sepet
```

Burada `push`, ziyaret edilen sayfayı yığının üstüne ekler. `pop` ise son ziyaret edilen sayfayı çıkarır. Tarayıcıların geri düğmesi benzer bir mantıktan yararlanır. `peek`, elemanı silmeden sıradaki değeri görmemizi sağlar.

## Python ile kuyruk oluşturmak

Kuyruk için listenin başından sürekli eleman çıkarmak uygun değildir; çünkü kalan elemanların kaydırılması $O(n)$ maliyet oluşturabilir. Python’daki `deque`, iki uçta da yaklaşık $O(1)$ işlem sunar.

```python
from collections import deque

class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError('Kuyruk boş!')
        return self.items.popleft()

    def is_empty(self):
        return len(self.items) == 0

queue = Queue()
queue.enqueue('rapor.pdf')
queue.enqueue('fatura.pdf')
queue.enqueue('sunum.pdf')
print(queue.dequeue())  # rapor.pdf
```

Bu örnekte yazıcı, ilk gönderilen belgeyi önce işler. Yeni belgeler kuyruğun arkasına eklenirken işlenecek belgeler ön taraftan alınır.

## Gerçek projelerde hangisi seçilmeli?

Bir işlemi ters sırada geri almak istiyorsanız yığın uygundur. Metin editörlerindeki **geri al**, fonksiyon çağrılarını yöneten **çağrı yığını**, parantez denetimi ve derinlik öncelikli arama bunun örnekleridir.

Geliş sırasını korumak istiyorsanız kuyruk tercih edilir. Müşteri talepleri, e-posta gönderimleri, arka plan işleri ve genişlik öncelikli arama kuyrukla modellenebilir. Ancak acil işlerin önce yürütülmesi gerekiyorsa klasik FIFO yerine **öncelik kuyruğu** kullanılmalıdır.

Özetle seçim sorusu oldukça pratiktir: “En son gelen mi, yoksa en uzun süredir bekleyen mi önce işlenmeli?” İlk yanıt yığını, ikinci yanıt kuyruğu işaret eder. Bu küçük soru, büyük sistemlerin düzenli ve öngörülebilir çalışmasını sağlayabilir.

![yigin-ve-kuyruk-54](/img/yigin-ve-kuyruk-54.svg)


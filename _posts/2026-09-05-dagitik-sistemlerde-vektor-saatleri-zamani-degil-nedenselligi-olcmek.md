---
layout: post
title: "Dağıtık Sistemlerde Vektör Saatleri: Zamanı Değil Nedenselliği Ölçmek"
math: true
categories: 
  - Bilgi
tags: 
  - dağıtık sistemler
  - vektör saatleri
  - nedensellik
toc: true
---

Dağıtık bir sistemde herkesin baktığı kusursuz bir duvar saati yoktur. Düğümlerin fiziksel saatleri farklı hızlarda ilerleyebilir, ağ paketleri gecikebilir ve mesajlar gönderildikleri sıradan farklı bir sırada ulaşabilir. Vektör saatleri, “Saat kaç?” sorusunu cevaplamak yerine daha yararlı bir soruya odaklanır: “Bu olay, diğer olaydan önce mi gerçekleşti; yoksa ikisi birbirinden bağımsız mıydı?”
``

## Fiziksel zaman neden yeterli değildir?

A ve B adlı iki sunucu düşünelim. A bir kullanıcı kaydını güncellerken B aynı kaydı başka bir bölgede değiştirebilir. Zaman damgalarına göre A'nın işlemi daha yeni görünebilir; ancak A'nın saati birkaç saniye ilerideyse bu sonuç yanıltıcıdır.

Lamport saatleri olaylara artan sayılar vererek nedensel sıralamayı kısmen temsil eder. Fakat iki olayın gerçekten birbirinden bağımsız, yani **eşzamanlı** olup olmadığını söyleyemez. Vektör saatleri ise her düğüm için ayrı bir sayaç tutarak bu eksikliği giderir.

| Yaklaşım | Saklanan değer | Nedenselliği gösterir mi? | Eşzamanlı olayları ayırır mı? |
|---|---:|---|---|
| Fiziksel saat | Tarih ve saat | Güvenilir biçimde hayır | Hayır |
| Lamport saati | Tek tamsayı | Önceliği korur | Hayır |
| Vektör saati | Sayaç dizisi | Evet | Evet |

## Vektör nasıl ilerler?

Üç düğümlü bir sistemde sayaçlar $[A, B, C]$ biçiminde tutulsun. Başlangıçta tüm düğümlerin vektörü $[0,0,0]$ olur. Kurallar oldukça mekaniktir:

1. Bir düğüm yerel olay gerçekleştirdiğinde kendi bileşenini bir artırır.
2. Mesaj gönderirken güncel vektörünü mesaja ekler.
3. Mesaj alan düğüm, her bileşen için yerel ve gelen değerlerin maksimumunu alır.
4. Alıcı daha sonra kendi bileşenini bir artırır.

Birleştirme işlemi matematiksel olarak şöyle yazılır:

$$V_{yeni}[i] = \max(V_{yerel}[i], V_{mesaj}[i])$$

Örneğin A'nın saati $[2,0,0]$ iken B'ye mesaj gönderdiğini düşünelim. B'nin mevcut değeri $[0,1,0]$ olsun. B mesajı alınca önce maksimumları hesaplar, ardından kendi sayacını artırır ve $[2,2,0]$ sonucuna ulaşır. Böylece B'nin durumu, A'daki ilk iki olaydan haberdar olduğunu taşır.

## Olaylar nasıl karşılaştırılır?

$X$ olayı $Y$ olayından önce geliyorsa, tüm bileşenlerde $V_X[i] <= V_Y[i]$ olmalı ve en az bir bileşende kesin küçüklük bulunmalıdır. Bu ilişki $X \rightarrow Y$ şeklinde gösterilir.

Eğer vektörlerin bazı bileşenleri büyük, bazıları küçükse olaylar karşılaştırılamaz. Örneğin $[2,1,0]$ ile $[1,2,0]$ eşzamanlıdır. Buradaki “eşzamanlı”, aynı milisaniyede gerçekleşmek değil, aralarında bilinen bir neden-sonuç bağlantısı bulunmaması demektir.

## Python ile küçük bir uygulama

Aşağıdaki sınıf yerel olayları, mesaj göndermeyi ve alınan vektörü birleştirmeyi gösterir:

```python
class VectorClock:
    def __init__(self, node_id, size):
        self.node_id = node_id
        self.clock = [0] * size

    def local_event(self):
        self.clock[self.node_id] += 1

    def send(self):
        self.local_event()
        return self.clock.copy()

    def receive(self, incoming):
        self.clock = [
            max(local, remote)
            for local, remote in zip(self.clock, incoming)
        ]
        self.clock[self.node_id] += 1

    def snapshot(self):
        return self.clock.copy()

alice = VectorClock(0, 3)
bob = VectorClock(1, 3)

message_clock = alice.send()
bob.receive(message_clock)

print(alice.snapshot())  # [1, 0, 0]
print(bob.snapshot())    # [1, 1, 0]
```

`copy()` kullanılması önemlidir; aksi halde mesaj, gönderen düğümün daha sonra değiştirdiği aynı listeyi paylaşabilir. Gerçek bir ağda bu vektör serileştirilerek mesajın üst verisine eklenir.

## Güçlü ama bedelsiz değil

Vektör saatinin boyutu düğüm sayısıyla birlikte büyür. Dinamik üyeliğe sahip binlerce düğümlü sistemlerde depolama, aktarım ve düğüm kimliklerini temizleme maliyeti oluşur. Buna rağmen sürüm çatışmalarını bulmak, çoğaltılmış verileri uzlaştırmak ve olayların nedensel geçmişini izlemek için son derece değerlidir. Kısacası vektör saatleri zamanı ölçmez; dağıtık sistemin hafızasını düzenler.

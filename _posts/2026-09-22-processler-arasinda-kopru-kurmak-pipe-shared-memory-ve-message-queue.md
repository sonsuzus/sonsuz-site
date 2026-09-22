---
layout: post
title: "Process’ler Arasında Köprü Kurmak: Pipe, Shared Memory ve Message Queue"
math: true
categories: 
  - Bilgi
tags: 
  - ipc
  - işletim-sistemleri
  - pipe
  - shared-memory
  - message-queue
  - python
toc: true
image: /img/processler-arasinda-kopru-13.png
---

Bir process kendi sanal adres alanında yaşayan, komşusunun değişkenlerine doğrudan dokunamayan küçük bir ada gibidir. Ancak gerçek uygulamalarda bu adaların veri paylaşması gerekir. İşte **Inter-Process Communication (IPC)** mekanizmaları, process’ler arasında köprü kurar. Pipe akış sunar, shared memory ortak bir çalışma masası sağlar, message queue ise düzenli bir posta kutusu gibi davranır.

``

## IPC neden gereklidir?

İşletim sistemi process’leri güvenlik ve kararlılık için birbirinden yalıtır. Process A içindeki `sayac` değişkeninin adresi, Process B için anlamlı değildir. Bu izolasyon güzel olsa da paralel hesaplama, istemci-sunucu mimarileri ve arka plan görevleri veri alışverişi ister.

Bir IPC yönteminin yaklaşık toplam maliyetini şöyle düşünebiliriz:

$$T_{toplam} = T_{kopyalama} + T_{senkronizasyon} + T_{sistem\ çağrısı}$$

Shared memory, veri kopyalama maliyetini azaltırken senkronizasyon sorumluluğunu uygulamaya bırakır. Pipe ve message queue ise daha kontrollü iletişim karşılığında kernel müdahalesini artırır.

| Mekanizma | Veri modeli | Hız | Senkronizasyon | İdeal kullanım |
|---|---|---:|---|---|
| Pipe | Sıralı byte akışı | Orta | Okuma/yazma düzeniyle | Ebeveyn-çocuk iletişimi |
| Shared memory | Ortak bellek bölgesi | Çok yüksek | Mutex/semaphore gerekir | Büyük veri ve yoğun işlem |
| Message queue | Ayrı mesajlar | Orta | Kuyruk tarafından desteklenir | Görev dağıtımı ve olaylar |

![processler-arasinda-kopru-13](/img/processler-arasinda-kopru-13.svg)


## Pipe: Tek yönlü veri tüneli

Pipe, bir process’in yazdığı byte’ları diğer process’in aynı sırayla okuduğu FIFO yapısıdır. Geleneksel anonim pipe çoğunlukla akraba process’ler arasında kullanılır. Çift yönlü iletişim için iki pipe açmak gerekebilir.

```python
import os

okuma, yazma = os.pipe()
pid = os.fork()

if pid == 0:
    os.close(yazma)
    mesaj = os.read(okuma, 1024)
    print("Çocuk aldı:", mesaj.decode())
else:
    os.close(okuma)
    os.write(yazma, b"Merhaba cocuk process!")
    os.close(yazma)
```

Burada `fork()` sonrasında dosya tanımlayıcıları iki process’e de miras kalır. Kullanılmayan uçların kapatılması önemlidir; aksi durumda okuyucu EOF beklerken sonsuza kadar bloklanabilir. Pipe mesaj sınırlarını korumaz: iki yazma işlemi okuyucuya tek byte akışı olarak gelebilir.

## Shared memory: Aynı masada çalışmak

Shared memory, bir bellek bölgesini birden fazla process’in adres alanına eşler. Veri kernel üzerinden sürekli taşınmadığı için özellikle büyük dizilerde hızlıdır. Teorik olarak $n$ byte verinin kopyalanması $O(n)$ iken, ortak bölgeye erişim ek kopyayı ortadan kaldırabilir.

```python
from multiprocessing import Process, shared_memory

shm = shared_memory.SharedMemory(create=True, size=4)
shm.buf[:4] = (42).to_bytes(4, "little")

def oku(ad):
    ortak = shared_memory.SharedMemory(name=ad)
    print(int.from_bytes(ortak.buf[:4], "little"))
    ortak.close()

p = Process(target=oku, args=(shm.name,))
p.start()
p.join()
shm.close()
shm.unlink()
```

Örnekte çocuk process ortak bölgeyi adıyla açar. Fakat iki process aynı değeri eşzamanlı değiştirirse **race condition** oluşabilir. Bu nedenle lock, semaphore veya atomik işlemler kullanılmalıdır. Ayrıca iş bitince belleği kaldırmamak kaynak sızıntısına yol açar.

## Message queue: Process’lerin posta kutusu

Message queue, byte akışı yerine sınırları belli mesajlar taşır. Üretici kuyruğa görev bırakır, tüketici uygun olduğunda alır. Böylece iki tarafın aynı anda çalışması gerekmez.

```python
from multiprocessing import Process, Queue

kuyruk = Queue()

def tuket(q):
    while True:
        mesaj = q.get()
        if mesaj is None:
            break
        print("İşleniyor:", mesaj)

p = Process(target=tuket, args=(kuyruk,))
p.start()
kuyruk.put({"is": "rapor", "id": 7})
kuyruk.put(None)
p.join()
```

Python’ın `Queue` sınıfı serileştirme ve senkronizasyon ayrıntılarını gizler. Bunun bedeli, nesnelerin dönüştürülmesi ve kopyalanmasıdır. Mesajların çok büyük olması performansı düşürebilir.

## Hangisini seçmeliyiz?

Basit, sıralı ve kısa ömürlü iletişimde pipe; devasa veri bloklarında shared memory; bağımsız görevleri güvenilir biçimde dağıtırken message queue tercih edilir. Kısacası en hızlı seçenek her zaman en kolay veya en güvenli seçenek değildir. IPC tasarımında veri hacmi, process ilişkisi, hata toleransı ve senkronizasyon maliyeti birlikte değerlendirilmelidir.

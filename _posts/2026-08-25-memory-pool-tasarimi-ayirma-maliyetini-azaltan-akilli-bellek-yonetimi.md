---
layout: post
title: "Memory Pool Tasarımı: Ayırma Maliyetini Azaltan Akıllı Bellek Yönetimi"
math: true
categories: 
  - Bilgi
tags: 
  - memory pool
  - bellek yönetimi
  - performans
  - c++
---

Bir uygulama saniyede binlerce küçük nesne oluşturup yok ediyorsa, asıl darboğaz her zaman algoritmanız olmayabilir. `malloc`, `free`, `new` ve `delete` çağrıları; uygun blok arama, meta veri güncelleme, kilit alma ve parçalanma yönetimi gibi görünmeyen maliyetler taşır. Memory pool, sık kullanılan benzer boyutlu nesneleri önceden ayrılmış bir bellek alanından dağıtarak bu maliyeti daha öngörülebilir hale getiren özel bir bellek yöneticisidir.
``

Standart dinamik bellek ayırıcıları genel amaçlıdır: 16 baytlık bir nesne de, 16 MB'lık bir tampon da aynı arayüzden talep edilir. Bu esneklik değerlidir; ancak küçük ve kısa ömürlü nesnelerin yoğun olduğu oyun motorları, ağ sunucuları, derleyiciler ve gerçek zamanlı sistemler için fazladan iş anlamına gelebilir. Pool yaklaşımı, problem alanının kurallarını kullanır: “Nesnelerim çoğunlukla aynı boyutta ve çok sık oluşturuluyor.”

Temel fikir basittir. Program başlarken ya da ihtiyaç duyuldukça büyük bir blok, yani **arena**, ayrılır. Bu alan sabit boyutlu slotlara bölünür. Yeni nesne gerektiğinde yöneticinin işletim sisteminden bellek istemesi yerine boş slot listesinden bir adres vermesi yeterlidir. Nesne serbest bırakıldığında slot tekrar boş listeye eklenir.

| Özellik | Genel amaçlı ayırıcı | Sabit boyutlu memory pool |
|---|---|---|
| Ayırma maliyeti | Değişken, arama içerebilir | Genellikle $O(1)$ |
| Parçalanma | Zamanla artabilir | Slotlar eşit olduğu için düşüktür |
| Esneklik | Her boyutta veri | Belirlenmiş nesne boyutu |
| Serbest bırakma | Blok birleştirme gerekebilir | Boş listeye geri ekleme |

Bir pool'un kapasitesi $N$, her slotun boyutu $S$ ise yalnızca kullanıcı verisi için gereken alan yaklaşık olarak $N \times S$ olur. Boş liste işaretçisi, hizalama ve hata ayıklama bilgileri eklendiğinde gerçek maliyet şuna yaklaşır:

$$M = N \times (S + H + P)$$

Burada $H$ slot başına yönetim verisini, $P$ ise hizalama nedeniyle oluşabilecek dolguyu temsil eder. Örneğin 64 baytlık nesneleri 16 bayt hizalamayla saklamak, işlemci önbelleği ve SIMD erişimleri açısından faydalı olabilir; fakat kapasite planlamasında bu ek alan unutulmamalıdır.

Aşağıdaki C++ örneği, serbest slotları kendi içlerinde bağlayan minimal bir free-list pool gösterir. Gerçek projelerde sınır kontrolleri, thread safety ve hata ayıklama etiketleri eklenmelidir.

```cpp
#include <cstddef>
#include <new>

class ParticlePool {
    struct Slot { Slot* next; };
    Slot* freeList;

public:
    ParticlePool(void* memory, std::size_t count) : freeList(nullptr) {
        auto* slots = static_cast<Slot*>(memory);
        for (std::size_t i = 0; i < count; ++i) {
            slots[i].next = freeList;
            freeList = &slots[i];
        }
    }

    void* allocate() {
        if (!freeList) return nullptr; // Pool dolu
        Slot* slot = freeList;
        freeList = freeList->next;
        return slot;
    }

    void deallocate(void* ptr) {
        auto* slot = static_cast<Slot*>(ptr);
        slot->next = freeList;
        freeList = slot;
    }
};
```

Bu tasarımda `allocate`, listenin başındaki slotu alır; `deallocate` ise aynı slotu başa koyar. Her iki işlem de liste uzunluğundan bağımsızdır: $T_{allocate} \approx T_{deallocate} \approx O(1)$. Ancak önemli bir ayrıntı vardır: `Slot` yapısı, yönetilen nesneden büyük olmalıdır. Küçük nesnelerde slotun başındaki işaretçi alanı israf yaratabilir. Bu nedenle çok küçük nesneler için bitmap tabanlı takip veya farklı boyut sınıfları tercih edilebilir.

| Pool türü | En uygun kullanım | Dikkat edilmesi gereken |
|---|---|---|
| Fixed-size pool | Mermi, parçacık, bağlantı nesnesi | Nesne boyutu sabittir |
| Arena / linear allocator | Birlikte ölen geçici veriler | Tek tek serbest bırakma yoktur |
| Object pool | Yeniden kullanılabilen pahalı nesneler | Eski durumun sıfırlanması gerekir |

Pool tasarlarken “belleği geri vermek” ile “nesneyi yeniden kullanıma hazırlamak” arasındaki farkı ayırın. Bir nesnenin yıkıcısı, dosya tanıtıcısı veya GPU kaynağı gibi harici kaynakları temizlemelidir; slotu havuza iade etmek ise yalnızca RAM'in tekrar kullanılabilir olduğunu belirtir. Çok iş parçacıklı kodda serbest listeyi mutex ile korumak kolaydır, fakat yüksek yükte thread-local pool'lar veya kilitsiz yapılar daha iyi ölçeklenebilir.

Sonuç olarak memory pool sihirli bir hız düğmesi değildir; değişken boyutlu, seyrek oluşturulan nesnelerde standart ayırıcı çoğu zaman yeterlidir. Ancak yaşam döngüsü ve boyutu öngörülebilen yoğun nesne akışlarında pool, gecikme dalgalanmasını azaltır, önbellek yerelliğini iyileştirir ve bellek yönetimini uygulamanın kurallarına göre şekillendirir.

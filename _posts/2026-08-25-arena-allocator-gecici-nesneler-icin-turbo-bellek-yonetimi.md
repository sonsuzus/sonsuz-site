---
layout: post
title: "Arena Allocator: Geçici Nesneler İçin Turbo Bellek Yönetimi"
math: true
categories: 
  - Bilgi
tags: 
  - arena allocator
  - bellek yönetimi
  - c++
  - performans
toc: true
---

Modern yazılımlarda performans sorunlarının önemli bir bölümü işlemciden değil, bellek tahsisinden doğar. Her geçici nesne için `malloc`, `new` ya da benzeri bir çağrı yapmak; ayırıcıyı kilitleme, uygun boş blok bulma ve parçalanmayı yönetme gibi ek maliyetler yaratır. Arena allocator yaklaşımı bu maliyeti dramatik biçimde azaltır: Büyük bir bellek bölgesi ayırır, küçük nesneleri bu bölge içinde sırayla yerleştirir ve iş bittiğinde hepsini tek hamlede temizler.
``
## Temel fikir: Tek tek silmek yerine topluca unutmak

Arena, genellikle önceden ayrılmış bir byte dizisi ve bu dizideki güncel konumu gösteren bir `offset` değerinden oluşur. Yeni bir nesne istendiğinde allocator uygun hizalamayı hesaplar, `offset` değerini ileri taşır ve ilgili adresi döndürür. Serbest liste aramak, blokları birleştirmek veya her nesne için ayrı `free` çağrısı yapmak yoktur.

Bu davranışın maliyetini kabaca şöyle düşünebiliriz:

$$T_{arena}(n) \approx T_{rezervasyon} + n \cdot T_{bump}$$

Buradaki `bump`, yalnızca bir işaretçiyi ileri alma işlemidir. Geleneksel dinamik tahsiste ise ek meta veri, uygun blok arama ve serbest bırakma maliyetleri bulunur:

$$T_{klasik}(n) \approx n \cdot (T_{allocate} + T_{free})$$

Arena'nın en güçlü yanı, nesnelerin yaşam sürelerinin benzer olduğu durumlarda ortaya çıkar. Örneğin bir HTTP isteği işlenirken oluşturulan ayrıştırma düğümleri, bir oyun karesindeki parçacık verileri veya bir derleyicinin tek dosya için ürettiği AST düğümleri aynı anda ölebilir.

| Özellik | Geleneksel heap | Arena allocator |
|---|---|---|
| Tahsis hızı | Değişken, daha karmaşık | Genellikle sabit zamana yakın |
| Tekil nesne silme | Desteklenir | Genellikle desteklenmez |
| Parçalanma riski | Zamanla artabilir | Arena içinde çok düşüktür |
| Uygun kullanım | Farklı ömürlü nesneler | Birlikte ölen geçici nesneler |

## Bump-pointer mantığını C++ ile kurmak

Aşağıdaki örnek, eğitim amaçlı küçük bir arena uygular. Gerçek projelerde taşma kontrolü, büyüyen bloklar ve thread-safety gereksinimleri ayrıca değerlendirilmelidir.

```cpp
#include <cstddef>
#include <cstdint>
#include <stdexcept>
#include <vector>

class Arena {
    std::vector<std::byte> buffer;
    std::size_t offset = 0;

public:
    explicit Arena(std::size_t capacity) : buffer(capacity) {}

    void* allocate(std::size_t size, std::size_t alignment) {
        std::size_t aligned = (offset + alignment - 1) & ~(alignment - 1);
        if (aligned + size > buffer.size())
            throw std::bad_alloc();

        void* result = buffer.data() + aligned;
        offset = aligned + size;
        return result;
    }

    void reset() { offset = 0; }
};
```

`allocate` metodundaki hizalama işlemi kritiktir. Bazı türler bellekte belirli adres sınırlarında başlamalıdır; aksi hâlde performans düşebilir, hatta bazı mimarilerde hatalı erişim oluşabilir. `reset()` ise arena'nın sihirli düğmesidir: Eski nesneleri tek tek dolaşmadan `offset` sıfırlanır ve tüm alan yeniden kullanılabilir olur.

## Güçlü ama her derde deva değil

Arena allocator, nesnelerin farklı zamanlarda silinmesi gereken senaryolarda kötü bir seçim olabilir. Bir nesneyi yaşatırken diğerlerini silmek istiyorsanız, arena belleği gereksiz yere tutabilir. Ayrıca C++'ta destructor çalıştırılması gereken nesneler için yalnızca belleği geri almak yeterli değildir; kaynak kapatma mantığı ayrıca yönetilmelidir.

| Senaryo | Arena kararı | Neden |
|---|---|---|
| İstek bazlı web parser'ı | Çok uygun | İstek sonunda toplu reset yapılır |
| Oyun frame verisi | Çok uygun | Her frame geçici veriler yenilenir |
| Uzun ömürlü kullanıcı oturumları | Dikkatli kullanılmalı | Yaşam süreleri farklılaşabilir |
| Dosya, socket, mutex saran nesneler | Ek yönetim gerekli | Destructor ve kaynak kapatma gerekir |

Özetle arena allocator, bellek yönetiminde “her nesneyi ayrı ayrı düzenlemek” yerine yaşam döngüsünü tasarlamayı öğretir. Geçici verinin sınırları netse, bu küçük mimari karar hem kodu sadeleştirir hem de kritik döngülerde gözle görülür hız kazandırır.

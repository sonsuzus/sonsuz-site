---
layout: post
title: "C++ Atama Operatöründe Copy-and-Swap ile Güçlü İstisna Güvenliği"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - copy-and-swap
  - istisna-güvenliği
  - operator-overloading
  - raii
  - modern-c++
toc: true
image: /img/c-atama-operatorunde-36.png
---

C++’ta kaynak yöneten bir sınıfa atama operatörü yazmak, ilk bakışta birkaç alanı kopyalamaktan ibaret görünür. Fakat bellek ayırma işlemi yarıda başarısız olursa nesne hangi durumda kalacaktır? **Copy-and-swap**, yeni durumu önce güvenli bir geçici nesnede hazırlayıp yalnızca başarı kesinleştiğinde devreye alarak bu sorunu zarifçe çözer.

![c-atama-operatorunde-36](/img/c-atama-operatorunde-36.svg)

``
## Önce problem: Sil, sonra kopyala

Dinamik dizi yöneten basit bir sınıf düşünelim. Tehlikeli bir atama operatörü eski belleği önce silebilir, ardından yeni bellek ayırmaya çalışabilir:

```cpp
Buffer& operator=(const Buffer& other) {
    delete[] data_;
    size_ = other.size_;
    data_ = new int[size_]; // std::bad_alloc fırlatabilir
    std::copy(other.data_, other.data_ + size_, data_);
    return *this;
}
```

`new` başarısız olduğunda eski veri çoktan kaybedilmiştir. Üstelik `data_`, silinmiş belleği gösterebilir. Nesne artık yalnızca yanlış değil, yıkıcısı çalıştığında ikinci kez silme yapabilecek kadar tehlikelidir.

İstisna güvenliği genellikle üç seviyede değerlendirilir:

| Garanti | İstisna sonrası durum | Copy-and-swap |
|---|---|---|
| Garanti yok | Nesne bozulabilir | Önler |
| Temel garanti | Nesne geçerlidir, değeri değişebilir | Aşar |
| Güçlü garanti | İşlem ya tamamen olur ya hiç olmamış sayılır | Sağlar |
| Fırlatmama garantisi | İşlem istisna üretmez | Yalnızca `swap` için beklenir |

Güçlü garantiyi matematiksel olarak bir durum geçişi gibi ifade edebiliriz. Eski durum $S$, hedef durum $T$ ise:

$$
\operatorname{assign}(S,T)=
\begin{cases}
T, & \text{işlem başarılıysa} \\
S, & \text{istisna oluşursa}
\end{cases}
$$

Yani yarım kalmış, garip bir $S'$ durumuna izin verilmez.

## Copy-and-swap nasıl çalışır?

Teknik üç adımdan oluşur:

1. Sağ taraftaki nesnenin geçici bir kopyasını oluştur.
2. Geçici nesne ile mevcut nesnenin kaynaklarını değiştir.
3. Geçici nesne kapsam dışına çıkınca eski kaynakları otomatik olarak yok etsin.

```cpp
#include <algorithm>
#include <cstddef>
#include <utility>

class Buffer {
public:
    explicit Buffer(std::size_t size = 0)
        : size_(size), data_(size ? new int[size]{} : nullptr) {}

    Buffer(const Buffer& other)
        : size_(other.size_),
          data_(size_ ? new int[size_] : nullptr) {
        std::copy(other.data_, other.data_ + size_, data_);
    }

    Buffer(Buffer&& other) noexcept
        : size_(std::exchange(other.size_, 0)),
          data_(std::exchange(other.data_, nullptr)) {}

    ~Buffer() {
        delete[] data_;
    }

    friend void swap(Buffer& a, Buffer& b) noexcept {
        using std::swap;
        swap(a.size_, b.size_);
        swap(a.data_, b.data_);
    }

    Buffer& operator=(Buffer other) {
        swap(*this, other);
        return *this;
    }

private:
    std::size_t size_{};
    int* data_{};
};
```

Buradaki kritik ayrıntı, parametrenin `const Buffer&` yerine **değerle** alınmasıdır. Bir lvalue gönderildiğinde kopya kurucu, rvalue gönderildiğinde ise taşıma kurucu geçici `other` nesnesini hazırlar. Böylece tek operatör hem kopyalama hem taşıma atamasını karşılayabilir.

Kopyalama sırasında `new` istisna fırlatırsa fonksiyon gövdesine henüz girilmez; `*this` değişmeden kalır. Kopya başarıyla oluşursa `swap` yalnızca boyut ve işaretçi gibi ucuz üyeleri değiştirir. Bu nedenle `swap` fonksiyonunun `noexcept` olması güçlü garantinin merkezidir. Değişimden sonra `other`, hedef nesnenin eski belleğini taşır ve yıkıcısı bu belleği temizler. RAII burada temizlik ekibidir; hem de fazla mesai ücreti istemez.

## Geleneksel atama ile karşılaştırma

| Özellik | Elle yazılmış atama | Copy-and-swap |
|---|---|---|
| Kendine atama kontrolü | Genellikle `this != &other` gerekir | Doğal olarak güvenlidir |
| Hata yönetimi | Karmaşık geri alma kodu gerekir | Geçici nesne geri almayı sağlar |
| Kod tekrarı | Yüksek olabilir | Kopya kurucu ve `swap` yeniden kullanılır |
| Performans | Bellek yeniden kullanılabilir | Her kopyada yeni kaynak ayırabilir |

Copy-and-swap temiz ve güvenlidir; ancak her zaman en hızlı çözüm değildir. Büyük tamponlarda mevcut kapasiteyi yeniden kullanmak önemliyse özel bir atama operatörü daha verimli olabilir. Ayrıca sınıf yalnızca `std::vector`, `std::string` ve akıllı işaretçiler gibi RAII türlerinden oluşuyorsa en iyi seçenek çoğu zaman **Rule of Zero**, yani özel atama operatörü yazmamaktır.

Özetle copy-and-swap, işlemi önce hazırla, sonra tek ve güvenli adımla yayımla yaklaşımıdır. `swap` gerçekten `noexcept` olduğu sürece atama işlemini bir veritabanı işlemi gibi davranmaya yaklaştırır: ya commit gerçekleşir ya da nesne eski hâlinde kalır.

---
layout: post
title: "C++ Pimpl Deyimi: Derleme Bağımlılıklarını Perde Arkasına Taşımak"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - pimpl
  - derleme
  - bağımlılık
  - tasarım desenleri
  - cpp
toc: true
image: /img/c-pimpl-deyimi-28.png
---

C++ projeleri büyüdükçe küçük bir başlık dosyası değişikliği, ilgisiz görünen onlarca kaynak dosyanın yeniden derlenmesine yol açabilir. Pimpl, yani *Pointer to Implementation*, sınıfın kullanıcıya açık arayüzünü gerçek uygulama ayrıntılarından ayırarak bu zincirleme etkiyi azaltan köklü bir C++ deyimidir. Kısacası sınıfımız sahne önünde sade görünürken bütün dekor, kablolar ve karmaşa perdenin arkasında kalır.

``

## Derleme bağımlılığı neden oluşur?

Bir başlık dosyasında başka sınıfları doğrudan üye olarak kullandığımızı düşünelim:

```cpp
#include <string>
#include <vector>
#include "DatabaseConnection.hpp"
#include "Logger.hpp"

class UserService {
public:
    void createUser(const std::string& name);

private:
    DatabaseConnection database;
    Logger logger;
    std::vector<std::string> cache;
};
```

Derleyici, `UserService` nesnesinin boyutunu hesaplayabilmek için bütün veri üyelerinin tanımlarını bilmelidir. Bu nedenle başlıklar içeri alınır. `Logger.hpp` değiştiğinde `UserService.hpp` dosyasını kullanan kaynaklar da yeniden derlenebilir.

Basitleştirilmiş biçimde toplam derleme maliyetini şöyle düşünebiliriz:

$$
T \approx \sum_{i=1}^{n} D_i \times C_i
$$

Burada $D_i$, bir başlığa bağımlı çeviri birimi sayısını; $C_i$ ise ilgili birimin derleme maliyetini temsil eder. Pimpl özellikle $D_i$ değerinin oluşturduğu zincirleme etkiyi küçültür.

## Pimpl yapısı

Başlık dosyasında uygulama sınıfı yalnızca ileri bildirilir ve ona bir akıllı işaretçi tutulur:

```cpp
// UserService.hpp
#pragma once

#include <memory>
#include <string>

class UserService {
public:
    UserService();
    ~UserService();

    UserService(UserService&&) noexcept;
    UserService& operator=(UserService&&) noexcept;

    void createUser(const std::string& name);

private:
    class Impl;
    std::unique_ptr<Impl> impl;
};
```

Gerçek üyeler `.cpp` dosyasına taşınır:

```cpp
// UserService.cpp
#include "UserService.hpp"
#include "DatabaseConnection.hpp"
#include "Logger.hpp"

#include <vector>

class UserService::Impl {
public:
    void createUser(const std::string& name) {
        logger.info("Kullanıcı oluşturuluyor: " + name);
        database.insert(name);
        cache.push_back(name);
    }

private:
    DatabaseConnection database;
    Logger logger;
    std::vector<std::string> cache;
};

UserService::UserService()
    : impl(std::make_unique<Impl>()) {}

UserService::~UserService() = default;
UserService::UserService(UserService&&) noexcept = default;
UserService& UserService::operator=(UserService&&) noexcept = default;

void UserService::createUser(const std::string& name) {
    impl->createUser(name);
}
```

Yıkıcının `.cpp` içinde tanımlanması önemlidir. `std::unique_ptr`, işaret ettiği nesneyi yok ederken `Impl` türünün tamamlanmış olmasına ihtiyaç duyar. Başlık içinde otomatik üretilen bir yıkıcı bazı derleyici bağlamlarında eksik tür hatasına neden olabilir.

## Pimpl öncesi ve sonrası

| Özellik | Doğrudan üyeler | Pimpl yaklaşımı |
|---|---|---|
| Başlık bağımlılığı | Yüksek | Düşük |
| Uygulama ayrıntılarının görünürlüğü | Açık | Gizli |
| ABI kararlılığı | Daha kırılgan | Daha güçlü |
| Nesne oluşturma maliyeti | Genellikle daha düşük | Ek bellek tahsisi olabilir |
| Üyelere erişim | Doğrudan | İşaretçi üzerinden |
| Kod karmaşıklığı | Daha az | Ek sınıf ve yönlendirme gerekir |

![c-pimpl-deyimi-28](/img/c-pimpl-deyimi-28.svg)


## ABI avantajı

Pimpl yalnızca derleme süresini değil, ikili uyumluluğu da destekler. Doğrudan üye eklemek sınıfın `sizeof` değerini değiştirir. Pimpl kullanılan sınıfta ise dışarıdan görünen veri çoğunlukla tek bir işaretçidir:

$$
\text{sizeof(UserService)} \approx \text{sizeof(void*)}
$$

`Impl` içine yeni alanlar eklense bile açık sınıfın yerleşimi değişmez. Bu durum özellikle paylaşımlı kütüphanelerde değerlidir.

## Bedelsiz bir sihir değil

Pimpl; ek dinamik bellek tahsisi, işaretçi dolayımı ve daha fazla yardımcı kod getirir. Küçük, yalnızca dahili kullanılan veya şablon ağırlıklı sınıflarda kazancı maliyetinden düşük olabilir. Buna karşılık sık değişen özel üyeleri bulunan, geniş kitlelere sunulan ya da kararlı ABI gerektiren sınıflarda oldukça etkilidir.

Özetle Pimpl, her sınıfa serpilecek bir performans baharatı değil; derleme sınırlarını bilinçli biçimde yönetme aracıdır. Doğru yerde kullanıldığında başlık dosyalarını hafifletir, değişikliklerin yayılmasını sınırlar ve kütüphanenin perde arkasını özgürce yenilemenize imkân verir.

---
layout: post
title: "C++ RAII: İstisna Güvenliğinin Görünmez Süper Kahramanı"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - raii
  - istisna güvenliği
  - akıllı işaretçiler
  - kaynak yönetimi
toc: true
image: /img/c-raii-istisna-26.png
---

![c-raii-istisna-26](/img/c-raii-istisna-26.svg)


C++ programında dosya açmak, bellek ayırmak veya kilit edinmek kolaydır; asıl macera, işler ters gittiğinde bunları güvenle bırakabilmektir. Bir istisna normal kontrol akışını aniden kesebilir. RAII (Resource Acquisition Is Initialization), kaynakların ömrünü nesnelerin ömrüne bağlayarak bu sorunu dil seviyesindeki otomatik ömür yönetimine teslim eder.

``

## RAII tam olarak ne söyler?

RAII prensibinde kaynak, bir nesnenin kurucusunda edinilir ve yıkıcısında serbest bırakılır. Nesne kapsamdan normal biçimde çıksa da bir istisna nedeniyle ayrılsa da yıkıcı otomatik olarak çağrılır. Böylece `delete`, `close` veya `unlock` çağrılarını her çıkış yoluna elle yerleştirmek gerekmez.

Bir fonksiyonda $n$ farklı erken çıkış ve hata yolu bulunduğunu düşünelim. Elle yönetimde denetlenmesi gereken temizlik senaryoları kabaca $O(n)$ büyür; birden fazla bağımsız kaynak etkileşime girdiğinde olası durumlar $2^k$ seviyesine yaklaşabilir. RAII ise her kaynağın sorumluluğunu kendi nesnesine dağıtır: kapsam çözülürken nesneler edinilme sırasının tersine yok edilir.

| Yaklaşım | Kaynak edinme | Temizleme | İstisna durumunda risk |
|---|---|---|---|
| Elle yönetim | Fonksiyon içinde | Her çıkışta açıkça | Sızıntı ve kilitli kalma |
| RAII | Kurucuda | Yıkıcıda otomatik | Çok düşük |
| Çöp toplama | Çalışma zamanı yönetir | Zamanı belirsiz | Bellek güvenli, diğer kaynaklar belirsiz |

## Yığın çözme ve istisna güvenliği

Bir istisna fırlatıldığında C++, uygun `catch` bloğunu ararken aradaki kapsamları terk eder. Bu sürece **stack unwinding**, yani yığın çözme denir. Her terk edilen kapsamın otomatik nesneleri yok edilir. RAII’nin merkezi rolü tam burada ortaya çıkar: yıkıcı, hem başarı hem başarısızlık yolunun ortak temizlik kapısıdır.

```cpp
#include <fstream>
#include <stdexcept>
#include <string>

void kaydet(const std::string& veri) {
    std::ofstream dosya("sonuc.txt");
    if (!dosya) {
        throw std::runtime_error("Dosya açılamadı");
    }

    dosya << veri;
    if (!dosya) {
        throw std::runtime_error("Yazma başarısız");
    }
} // ofstream yıkıcısı dosyayı kapatır
```

İkinci hata oluşursa fonksiyon sonundaki açıklama satırına normal akışla ulaşılamaz. Buna rağmen `dosya` nesnesinin yıkıcısı çalışır ve işletim sistemi tanıtıcısı serbest bırakılır. RAII, unutkan programcıya karşı oldukça sabırlı bir güvenlik görevlisidir.

## İstisna güvenliği garantileri

C++ kodunda genellikle üç güvence seviyesi konuşulur:

| Garanti | Hata sonrası durum | RAII’nin katkısı |
|---|---|---|
| Temel garanti | Nesne geçerli, kaynak sızıntısı yok | Otomatik temizlik sağlar |
| Güçlü garanti | İşlem hiç yapılmamış gibi görünür | Geçici nesne ve takas desenini destekler |
| Fırlatmama garantisi | İşlem istisna üretmez | Güvenli yıkıcılar için kritiktir |

RAII tek başına güçlü garantiyi sihirli biçimde sağlamaz; fakat onun temelini oluşturur. Örneğin önce geçici bir sonuç hazırlanıp yalnızca başarıdan sonra mevcut değerle değiştirilebilir:

```cpp
void guncelle(std::vector<int>& hedef,
              const std::vector<int>& yeniVeri) {
    std::vector<int> gecici = yeniVeri; // Kopyalama hata verebilir
    hedef.swap(gecici);                 // Başarılıysa değiştir
} // Eski veri gecici ile birlikte temizlenir
```

Kopyalama başarısız olursa `hedef` değişmez. Başarılı olursa eski içerik `gecici` nesnesinin yıkımıyla temizlenir. Bu, güçlü garantinin “ya tamamen uygula ya hiç uygulama” mantığıdır.

## Modern C++ araçları

Ham `new` ve `delete` yerine `std::unique_ptr` tek sahipliği, `std::shared_ptr` paylaşımlı sahipliği temsil eder. `std::lock_guard` ve `std::scoped_lock` kilitleri kapsam sonunda bırakır. Dosya akışları da aynı prensibi uygular.

Yıkıcıların mümkün olduğunca istisna fırlatmaması gerekir. Yığın çözülürken çalışan bir yıkıcı ikinci bir istisna üretirse program `std::terminate` ile sonlanabilir. Bu nedenle pratik formül şudur: kaynağı kurucuda edin, sahipliği açıkça modelle, yıkıcıda güvenle bırak ve ham kaynağı mümkün olduğunca kısa süre çıplak tut. RAII yalnızca temizlik tekniği değil, C++’ta güvenilir tasarımın omurgasıdır.

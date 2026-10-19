---
layout: post
title: "C++ İstisna Garantileri: Güçlü, Temel ve Zayıf Güvencenin Gerçek Etkisi"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - istisna yönetimi
  - exception safety
  - raii
  - yazılım tasarımı
toc: true
image: /img/c-istisna-garantileri-83.png
---

![c-istisna-garantileri-83](/img/c-istisna-garantileri-83.svg)


Bir C++ fonksiyonunun istisna fırlatabilmesi tek başına korkutucu değildir; asıl mesele, istisna sonrasında programın hangi durumda kaldığıdır. Sepete ürün eklerken bellek tahsisi başarısız olursa eski sepet hâlâ kullanılabilir mi, yoksa nesne yarı güncellenmiş bir zombiye mi dönüşür? İstisna garantileri tam olarak bu soruya cevap verir.

``

## Önce terminolojiyi netleştirelim

C++ literatüründe yaygın olarak **no-throw**, **güçlü**, **temel** ve **garantisiz** olmak üzere dört seviye bulunur. “Zayıf garanti” standartlaşmış ayrı bir seviye değildir. Bazı kaynaklar bu ifadeyi temel garantinin eş anlamlısı olarak, bazılarıysa hiçbir durum garantisi vermeyen kod için kullanır. Bu yazıda karışıklığı önlemek amacıyla **zayıf/garantisiz** ifadesini son anlamda kullanacağız.

| Seviye | İstisna sonrasında durum | Veri kaybı | Kullanılabilirlik |
|---|---|---:|---|
| Güçlü garanti | İşlem hiç başlamamış gibi | Yok | Tam |
| Temel garanti | Durum değişebilir fakat geçerlidir | Olabilir | Nesne kullanılabilir |
| Zayıf/garantisiz | Durum hakkında söz verilmez | Muhtemel | Belirsiz |

Güçlü garantiyi bir işlem dönüşümüyle ifade edebiliriz. Başlangıç durumu $S$, işlem $f$ ise:

$$f(S) = S' \quad \text{veya istisna durumunda} \quad S$$

Yani sonuç ya tamamen yeni durumdur ya da tamamen eski durumdur. Bu yaklaşım veritabanlarındaki atomik işlemlere benzer.

## Güçlü garanti: Ya hep ya hiç

Aşağıdaki sınıf, yeni değeri önce geçici nesnede hazırlar. Riskli işlemler tamamlanmadan mevcut veriye dokunulmaz:

```cpp
#include <string>
#include <utility>

class Profile {
    std::string name;

public:
    void rename(const std::string& newName) {
        std::string temporary = newName; // Bellek ayırırken fırlatabilir
        name.swap(temporary);            // noexcept
    }
};
```

Kopyalama sırasında `std::bad_alloc` oluşursa `name` değişmez. Başarılı olursa `swap` ile yeni değer devreye alınır. Bu desen **copy-and-swap** veya daha genel anlamıyla “önce hazırla, sonra taahhüt et” yaklaşımıdır.

Güçlü garanti; finansal işlemler, yapılandırma güncellemeleri ve birden fazla adımın tek işlem gibi görünmesi gereken yerlerde değerlidir. Bedeli ise geçici kopyalar, ek bellek ve bazen daha karmaşık tasarımdır.

## Temel garanti: Dağınık ama hayatta

Temel garanti, istisna sonrasında nesnenin kurallarını koruduğunu ve kaynak sızdırmadığını söyler. Ancak eski değerlerin korunacağını söylemez:

```cpp
void normalize(std::vector<int>& values) {
    values.clear();
    values.push_back(0); // Bellek tahsisi başarısız olabilir
}
```

`push_back` başarısız olursa vektör boş kalabilir. Eski elemanlar kaybedilmiştir fakat `values` hâlâ geçerli bir vektördür; yeniden doldurulabilir, taşınabilir veya yok edilebilir. Bu, temel garantinin pratik özüdür.

RAII burada kritik rol oynar. `std::vector`, `std::string`, akıllı işaretçiler ve kilit sınıfları kaynaklarını yıkıcılarında bıraktığı için istisna sırasında bellek ve kilit sızıntılarını önler.

## Zayıf veya garantisiz kod: Sürpriz kutusu

Ham kaynaklar ve sıralı güncellemeler tehlikeli bir kombinasyondur:

```cpp
account.balance -= amount;
ledger.add(account.id, amount); // Fırlatabilir
account.lastTransfer = now();
```

`ledger.add` fırlatırsa bakiye azalmış, kayıt eklenmemiş ve zaman damgası değişmemiş olabilir. Nesneler tek tek geçerli görünse bile sistemin iş kuralı bozulmuştur. Böyle bir fonksiyon tekrar çağrılırsa para ikinci kez düşülebilir.

Çözüm; değişiklikleri geçici bir yapıda toplamak, geri alma işlemi tasarlamak veya fırlatabilen adımları mutasyondan önce tamamlamaktır.

## Hangi seviyeyi seçmeliyiz?

Her fonksiyona güçlü garanti vermek gereksiz olabilir. Salt hesaplamalarda ve kritik güncellemelerde güçlü garanti hedeflenebilir; büyük koleksiyonları dönüştüren performans odaklı işlemlerde temel garanti yeterli olabilir. Yıkıcılar, kaynak bırakma fonksiyonları ve `swap` gibi altyapı işlemleri ise mümkünse `noexcept` olmalıdır.

Pratik kontrol sorusu şudur: “Bu satır fırlatırsa hangi değişiklikler yapılmış olacak?” Cevap belirsizse yalnızca bir istisna probleminiz değil, aynı zamanda bir tasarım probleminiz vardır.

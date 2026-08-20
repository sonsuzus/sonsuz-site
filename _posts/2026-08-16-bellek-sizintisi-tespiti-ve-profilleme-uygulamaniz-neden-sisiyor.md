---
layout: post
title: "Bellek Sızıntısı Tespiti ve Profilleme: Uygulamanız Neden Şişiyor?"
math: true
categories: 
  - Bilgi
tags: 
  - bellek yönetimi
  - profilleme
  - debugging
  - performans
  - memory leak
toc: true
---

Uzun süre çalışan bir servis ilk gün kusursuz, üçüncü gün ise ağır davranıyorsa şüpheli genellikle CPU değil bellektir. Bellek sızıntısı, artık ihtiyaç duyulmayan nesnelerin hâlâ erişilebilir kalması veya işletim sistemi kaynaklarının serbest bırakılmaması durumudur. Bu sorun, yalnızca uygulamayı yavaşlatmaz; konteynerin OOM Killer tarafından sonlandırılmasına, gecikmelerin artmasına ve maliyetlerin yükselmesine de yol açabilir.
``
Bellek tüketimini anlamak için önce iki kavramı ayırmak gerekir: **anlık kullanım** ve **büyüme eğilimi**. Bir uygulamanın 800 MB RAM kullanması tek başına hata değildir; trafik yükü, önbellek ve çalışma veri seti bunu gerektirebilir. Asıl kritik soru şudur: İş yükü sabitken bellek taban çizgisi zamanla yükseliyor mu?

Kabaca, süreç belleğini şu şekilde modelleyebiliriz:

$$M(t) = M_0 + C(t) + L(t)$$

Burada $M_0$ başlangıç maliyeti, $C(t)$ meşru önbellek veya geçici veri kullanımı, $L(t)$ ise sızıntı bileşenidir. Sağlıklı bir sistemde geçici işlemler bittiğinde $C(t)$ azalır. Sızıntı varsa $L(t)$ sürekli büyür ve uzun vadeli eğim $\frac{dM}{dt} > 0$ kalır.

| Durum | Gözlenen davranış | Olası yorum |
|---|---|---|
| Sağlıklı dalgalanma | Yük altında yükselir, GC sonrası düşer | Geçici nesneler normal temizleniyor |
| Önbellek ısınması | Başta artar, sonra plato yapar | Sınırlandırılmış cache davranışı |
| Gerçek sızıntı | Trafik sabitken düzenli yükseliş | Referans veya kaynak tutuluyor |
| Parçalanma | Nesneler temizlense de RSS düşmez | Ayırıcı/işletim sistemi davranışı olabilir |

## Sızıntının Kaynağını Sınıflandırın

Yönetilen dillerde çöp toplayıcı, **erişilebilen** nesneleri silmez. Dolayısıyla sızıntı; global koleksiyonlar, büyüyen event listener listeleri, kapanmayan coroutine görevleri ya da sınırsız cache'ler yüzünden oluşabilir. Buna karşılık dosya tanıtıcıları, socket'ler ve native buffer'lar çoğu zaman GC'nin doğrudan çözemediği kaynaklardır.

| Kaynak türü | Tipik belirti | İnceleme yaklaşımı |
|---|---|---|
| Heap nesneleri | Heap snapshot boyutu büyür | Retaining path ve nesne sayısı |
| Native bellek | RSS artar, heap sabit kalır | Allocator ve sistem metrikleri |
| Dosya tanıtıcısı | `too many open files` hatası | FD sayısı, kapatma akışı |
| Cache | Anahtar sayısı büyür | TTL, LRU ve üst sınır kontrolü |

## Ölç, Karşılaştır, Doğrula

En güvenilir yöntem, aynı senaryonun farklı anlarında alınmış iki veya daha fazla profili karşılaştırmaktır. Önce uygulamayı kontrollü bir yük altında çalıştırın. Ardından bir "başlangıç" snapshot'ı, birkaç istek döngüsünden sonra ikinci snapshot'ı ve mümkünse zorlanmış bir GC sonrası üçüncü snapshot'ı alın. GC sonrasında yaşayan nesneler özellikle değerlidir; bunlar hâlâ bir referans zinciri tarafından tutuluyordur.

Python'da `tracemalloc`, tahsisatların hangi satırlardan geldiğini izlemek için pratik bir başlangıç aracıdır:

```python
import tracemalloc

tracemalloc.start(25)  # Çağrı zincirinin 25 karesini saklar.
baslangic = tracemalloc.take_snapshot()

for _ in range(10_000):
    istek_isle()  # Şüpheli iş yükü burada tekrar edilir.

son = tracemalloc.take_snapshot()
for fark in son.compare_to(baslangic, "lineno")[:5]:
    print(fark)
```

Bu kod, en çok bellek artışı üreten satırları listeler. Ancak bir satırın tahsisat yapması onu otomatik olarak suçlu yapmaz. Asıl soru, o nesnelerin **neden yaşamaya devam ettiği**dir. Heap snapshot araçlarındaki `retainers`, `dominators` veya `retaining path` görünümleri bu nedenle önemlidir: Nesneyi hayatta tutan global değişkeni, closure'ı ya da cache girdisini gösterir.

Üretimde yalnızca profil almak yerine gözlemlenebilirlik kurun. RSS, heap used, GC pause süresi, açık dosya tanıtıcısı sayısı ve cache boyutunu zaman serisi olarak izleyin. Alarm koşulu mutlak bir sayıdan çok eğim olabilir: örneğin sabit trafikte bir saat boyunca sürekli pozitif bellek artışı inceleme gerektirir.

Son olarak, her artışı sızıntı diye etiketlemeyin. JIT derleyici, bellek havuzları ve allocator parçalanması RSS'i yüksek tutabilir. Teşhis tamamlandığında çözüm; referansı kaldırmak, listener'ı unsubscribe etmek, `close` çağrısını garantiye almak, cache'e TTL/kapasite koymak ve aynı yük testiyle eğrinin yeniden plato yaptığını doğrulamak olmalıdır. Bellek avcılığında kanıt, tek bir grafik değil; tekrar edilebilir deneydir.

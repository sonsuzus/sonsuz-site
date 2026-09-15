---
layout: post
title: "Çöp Toplama Arenası: Mark-Sweep ve Nesil Bazlı GC"
math: true
categories: 
  - Bilgi
tags: 
  - çöp toplama
  - garbage collection
  - mark-sweep
  - nesil bazlı gc
  - bellek yönetimi
  - programlama
toc: true
---

Program çalışırken oluşturulan her nesne sonsuza kadar yaşamaz. Bir kullanıcı oturumu kapanır, geçici liste işini bitirir veya fonksiyon yerel değişkenleriyle vedalaşır. Bu nesnelerin kapladığı belleği otomatik olarak geri kazanan mekanizmaya **çöp toplayıcı** ya da GC (Garbage Collector) denir. Ancak bellekteki çöpleri bulmak, mutfaktaki çöp kutusunu boşaltmak kadar basit değildir: Önce hangi nesnenin gerçekten sahipsiz kaldığını anlamak gerekir.

``

## Erişilebilirlik: Çöpün matematiksel tanımı

Belleği yönlü bir grafik olarak düşünelim. Her nesne bir düğüm, nesneler arasındaki referanslar ise kenardır. Programın doğrudan erişebildiği global değişkenler, aktif çağrı yığınları ve CPU kayıtları **kök kümesini** oluşturur.

Kök kümesi $R$, tüm nesneler kümesi $V$ ve erişilebilir nesneler kümesi $L$ olsun:

$$L = \{v \in V \mid R'den\ v'ye\ bir\ yol\ vardır\}$$

Dolayısıyla çöp kümesi şöyledir:

$$G = V - L$$

Bir nesnenin başka bir nesne tarafından işaret edilmesi tek başına yeterli değildir. Birbirini gösteren iki sahipsiz nesne de çöptür; çünkü köklerden ikisine de ulaşılamaz. Bu ayrıntı, yalnızca referans saymaya dayalı yöntemlerin döngüler karşısında neden zorlandığını açıklar.

## Mark-sweep nasıl çalışır?

Mark-sweep, adını iki temel aşamasından alır:

1. **Mark:** Köklerden başlanır ve erişilebilen bütün nesneler işaretlenir.
2. **Sweep:** Bellek taranır; işaretlenmemiş nesneler serbest bırakılır.

Basitleştirilmiş sözde kod şöyledir:

```text
function collect(roots, heap):
    for root in roots:
        markRecursively(root)

    for object in heap:
        if object.marked:
            object.marked = false
        else:
            free(object)
```

`markRecursively`, nesnenin referans verdiği komşuları dolaşır. İşaretlerin temizlenmesi ise bir sonraki toplama turuna hazırlıktır. Mark-sweep döngüsel yapıları başarıyla toplar ve nesneleri taşımadığı için adreslerin sabit kalmasını sağlar. Buna karşılık tüm yığını taramak gecikmeye neden olabilir. Ayrıca boşalan alanlar dağınık kalır ve **bellek parçalanması** oluşabilir.

## Nesil bazlı GC: Gençler hızlı yaşar

Nesil bazlı GC, deneysel bir gözleme dayanır: Yeni oluşturulan nesnelerin büyük bölümü kısa sürede ölür. Buna **zayıf nesil hipotezi** denir. Bellek genellikle genç, yaşlı ve bazen kalıcı bölgeler şeklinde ayrılır.

Bir nesnenin hayatta kalma olasılığı $p$ ise, art arda $k$ toplama turundan sağ çıkma olasılığı kabaca:

$$P(yaşam) = p^k$$

Genç bölgede sık fakat küçük çaplı **minor GC** çalışır. Birkaç tur hayatta kalan nesneler yaşlı bölgeye terfi ettirilir. Yaşlı bölge daha seyrek taranır; kapsamlı işlem çoğunlukla **major** veya **full GC** olarak adlandırılır.

Genç nesneleri tararken yaşlı bir nesnenin genç bir nesneye verdiği referans kaybolmamalıdır. Bu nedenle çalışma zamanı, referans güncellemelerini izleyen **write barrier** ve hatırlanan kümeler kullanır. Böylece her minor GC sırasında bütün yaşlı bölgeyi taramak gerekmez.

## Yan yana karşılaştırma

| Özellik | Mark-sweep | Nesil bazlı GC |
|---|---|---|
| Temel fikir | Erişilebilirleri işaretle, kalanları temizle | Nesneleri yaşlarına göre ayır |
| Tarama alanı | Genellikle tüm yığın | Çoğunlukla genç nesil |
| Kısa ömürlü nesneler | Özel optimizasyon yok | Çok verimli |
| Uygulama karmaşıklığı | Görece düşük | Write barrier nedeniyle yüksek |
| Duraklama | Büyük yığında uzayabilir | Minor GC kısa; full GC uzun olabilir |
| Parçalanma | Oluşabilir | Kopyalama veya sıkıştırmayla azaltılabilir |

Burada önemli bir nüans vardır: Nesil bazlı GC, mark-sweep’in mutlaka rakibi değildir. Modern çalışma zamanları genç bölgede kopyalamalı toplama, yaşlı bölgede ise mark-sweep veya mark-compact kullanabilir. Yani nesil yaklaşımı, nesnelerin **nerede ve ne sıklıkta** toplanacağını; mark-sweep ise **nasıl** tespit edilip temizleneceğini anlatır.

## Hangisi ne zaman mantıklı?

Basitlik, sabit nesne adresleri veya sınırlı çalışma zamanı altyapısı önemliyse mark-sweep iyi bir başlangıçtır. Web sunucuları, sanal makineler ve yoğun şekilde geçici nesne oluşturan uygulamalar ise nesil bazlı GC’den ciddi fayda görür. Yine de gecikmeye duyarlı sistemlerde ortalama hız kadar en uzun duraklama da ölçülmelidir. Kısacası en iyi GC, yalnızca çöpleri bulan değil, programın çalışma karakterine en az sürprizle uyum sağlayandır.

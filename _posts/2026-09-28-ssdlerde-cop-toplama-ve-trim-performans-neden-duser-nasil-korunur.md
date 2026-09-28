---
layout: post
title: "SSD’lerde Çöp Toplama ve TRIM: Performans Neden Düşer, Nasıl Korunur?"
math: true
categories: 
  - Bilgi
tags: 
  - ssd
  - trim
  - depolama
  - donanım
  - performans
  - işletim-sistemi
toc: true
image: /img/ssdlerde-cop-toplama-35.png
---

Yeni alınmış bir SSD genellikle ışık hızındaymış gibi hissettirir; fakat sürücü dolup boşaldıkça yazma performansı gerileyebilir. Bunun nedeni hücrelerin eskimesinden ibaret değildir. NAND flash bellek, mevcut verinin üzerine doğrudan yazamaz. Önce ilgili alanın silinmesi gerekir. TRIM komutu ve SSD’nin çöp toplama mekanizması, bu zorunlu temizliği kullanıcıyı mümkün olduğunca bekletmeden gerçekleştiren iki takım arkadaşıdır.

``

## NAND belleğin temel kuralı

SSD verileri **sayfalara**, sayfaları ise daha büyük **bloklara** yerleştirir. Okuma ve yazma sayfa düzeyinde yapılabilirken silme işlemi blok düzeyinde gerçekleştirilir. Örneğin 16 KB büyüklüğündeki bir sayfayı değiştirmek için onu içeren birkaç MB’lık bloğun ele alınması gerekebilir.

| İşlem | Çalıştığı birim | Ön koşul | Göreli maliyet |
|---|---|---|---|
| Okuma | Sayfa | Yok | Düşük |
| Yazma | Boş sayfa | Sayfanın temiz olması | Orta |
| Silme | Blok | Geçerli verilerin taşınması gerekebilir | Yüksek |

İşletim sisteminde bir dosyayı sildiğimizde çoğunlukla yalnızca dosya sistemi kaydı kaldırılır. Klasik bir sabit disk için sektörlerin hemen temizlenmesi gerekmez; yeni veri geldiğinde üzerlerine yazılabilir. SSD ise hangi sayfaların artık gereksiz olduğunu kendi başına anlayamaz. Denetleyici, bildirilmediği sürece silinen dosyanın sayfalarını hâlâ geçerli sanır.

## TRIM ne yapar?

TRIM, işletim sisteminin SSD’ye “bu mantıksal adreslerdeki veriye artık ihtiyacım yok” demesidir. Komut veriyi anında fiziksel olarak silmek zorunda değildir. Yalnızca sayfaların **geçersiz** olarak işaretlenmesini sağlar. Böylece sürücünün denetleyicisi uygun bir zamanda temizlik yapabilir.

TRIM ile çöp toplama aynı şey değildir:

| Mekanizma | Kararı veren | Temel görevi |
|---|---|---|
| TRIM | İşletim sistemi | Kullanılmayan mantıksal blokları bildirmek |
| Çöp toplama | SSD denetleyicisi | Geçerli sayfaları taşıyıp blokları silmek |
| Aşınma dengeleme | SSD denetleyicisi | Yazma ve silme yükünü hücrelere dağıtmak |

Çöp toplama sırasında bir bloktaki geçerli sayfalar başka bir boş bloğa kopyalanır. Ardından eski blok tamamen silinerek yeni yazmalara hazırlanır. TRIM yoksa denetleyici gereksiz sayfaları da taşır; yani fazladan veri yazar.

Bu yük **yazma büyütmesi** ile ifade edilir:

$$WA = \frac{\text{NAND üzerine fiziksel yazılan veri}}{\text{İşletim sisteminin yazdığı veri}}$$

İşletim sistemi 1 GB yazarken NAND’a toplam 2 GB yazılmışsa $WA=2$ olur. Yüksek değer performansı düşürür ve hücrelerin silme-yazma döngülerini daha hızlı tüketir.

## TRIM durumunu kontrol etmek

Windows’ta yönetici yetkili terminalde şu komut kullanılabilir:

```powershell
fsutil behavior query DisableDeleteNotify
```

Sonuç `0` ise ilgili dosya sistemi için silme bildirimleri, yani TRIM etkindir. `1` görülmesi devre dışı olduğunu belirtir.

Linux’ta zamanlanmış TRIM servisinin durumu şöyle incelenebilir:

```bash
systemctl status fstrim.timer
```

Desteklenen bağlı dosya sistemlerine elle TRIM göndermek için ise aşağıdaki komut çalıştırılabilir:

```bash
sudo fstrim -av
```

Bu komutu sürekli çalıştırmak gerekmez. Çoğu modern dağıtım periyodik TRIM kullanır; Windows ve macOS da desteklenen SSD’lerde süreci otomatik yönetir.

## Boş alan neden önemlidir?

SSD doluluğu arttıkça denetleyicinin sayfaları taşıyabileceği boş blok sayısı azalır. Bu nedenle özellikle yoğun yazma yapılan sistemlerde sürücünün bir bölümünü boş bırakmak yararlıdır. Üreticinin ayırdığı **over-provisioning** alanı da aynı amaçla denetleyiciye çalışma sahası sağlar.

TRIM bir sihirli hızlandırma düğmesi değil, işletim sistemi ile SSD arasındaki gerekli iletişim protokolüdür. Çöp toplama, aşınma dengeleme ve yeterli boş alanla birlikte çalıştığında yazma büyütmesini azaltır; böylece SSD hem daha tutarlı performans gösterir hem de gereksiz hücre yıpranmasından korunur.

![ssdlerde-cop-toplama-35](/img/ssdlerde-cop-toplama-35.svg)


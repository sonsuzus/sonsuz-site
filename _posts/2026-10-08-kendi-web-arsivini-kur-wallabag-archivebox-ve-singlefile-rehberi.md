---
layout: post
title: "Kendi Web Arşivini Kur: Wallabag, ArchiveBox ve SingleFile Rehberi"
math: true
categories: 
  - Program
tags: 
  - web-clipping
  - wallabag
  - archivebox
  - singlefile
  - self-hosted
  - dijital-arşiv
toc: true
image: /img/kendi-web-arsivini-58.png
---

İnternette gördüğünüz harika bir makaleyi “sonra okurum” diye kaydedip birkaç ay sonra kırık bağlantıyla karşılaşmak, dijital dünyanın küçük ama can sıkıcı trajedilerindendir. Web clipping sistemleri; yazıları, görselleri ve bazen sayfanın çalışan bir kopyasını saklayarak bu sorunu çözer. Bu rehberde Wallabag, ArchiveBox ve SingleFile araçlarının farklı arşivleme yaklaşımlarını inceleyip kişisel bir web arşivinin nasıl kurulabileceğini göreceğiz.

``

## Web clipping tam olarak nedir?

Yer imi, yalnızca bir URL saklar. Web clipping ise bağlantının işaret ettiği içeriği de korumaya çalışır. Aradaki farkı kütüphane benzetmesiyle düşünelim: Yer imi, kitabın raftaki konumunu not etmektir; clipping ise kitabın fotokopisini almaktır.

Bir arşivleme sisteminin başarısını kabaca şu modelle değerlendirebiliriz:

$$Q = C \times F \times A$$

Burada $C$ içerik bütünlüğünü, $F$ gelecekte görüntülenebilme olasılığını, $A$ ise arşive erişim kolaylığını temsil eder. Sayfayı kusursuz saklayan ama arama yapılamayan bir sistem de yalnızca metni tutup görselleri kaybeden bir sistem de ideal değildir.

## Üç araç, üç farklı yaklaşım

| Araç | Temel amaç | Saklama biçimi | En güçlü yanı | Uygun kullanıcı |
|---|---|---|---|---|
| Wallabag | Sonra okuma | Temizlenmiş makale | Okuma deneyimi ve etiketleme | Makale koleksiyoncusu |
| ArchiveBox | Kapsamlı arşivleme | HTML, PDF, ekran görüntüsü, WARC | Çok formatlı ve aranabilir arşiv | Araştırmacı ve ekipler |
| SingleFile | Tek sayfalık kayıt | Bağımsız `.html` dosyası | Taşınabilirlik ve kolaylık | Hızlı, yerel arşiv isteyenler |

![kendi-web-arsivini-58](/img/kendi-web-arsivini-58.svg)


### Wallabag: Gürültüyü temizle, yazıyı sakla

Wallabag, reklamları ve gereksiz menüleri ayıklayarak sayfanın okunabilir bölümünü çıkarır. Etiketler, favoriler, tam metin araması ve mobil uygulamalar sayesinde açık kaynaklı bir “sonra oku” merkezi gibi davranır.

Docker ile hızlı bir deneme kurulumu yapılabilir:

```bash
docker run -d --name wallabag \
  -p 8080:80 \
  wallabag/wallabag
```

Bu komut Wallabag konteynerini başlatır ve arayüzü `http://localhost:8080` adresinde yayınlar. Kalıcı kullanımda veritabanı, volume, HTTPS ve düzenli yedekleme ayrıca yapılandırılmalıdır.

### ArchiveBox: Sayfanın dijital fosilini çıkar

ArchiveBox, URL listesini alıp her bağlantı için birden fazla çıktı üretebilir. Orijinal HTML, okunabilir metin, PDF, ekran görüntüsü ve WARC kaydı saklanabilir. Böylece bir yöntem başarısız olduğunda diğer kopya devreye girer.

```bash
mkdir web-arsivi && cd web-arsivi
archivebox init
archivebox add https://example.com/makale
archivebox server 0.0.0.0:8000
```

`init` arşiv dizinini hazırlar, `add` bağlantıyı işler, `server` ise arama yapılabilen web arayüzünü açar. Çok sayıda sayfa ve medya dosyası depolanacağı için disk tüketimi Wallabag’e göre daha yüksektir.

### SingleFile: Bir dosya, bütün sayfa

SingleFile bir tarayıcı eklentisidir. CSS, görseller ve gerekli kaynakları tek bir HTML belgesinin içine gömer. Sunucu kurmadan çalışan bu yaklaşım, dosyayı USB belleğe koymak veya bulut klasöründe saklamak için idealdir. Ancak koleksiyon büyüdükçe etiketleme, merkezi arama ve otomatik yedekleme işlerini sizin düzenlemeniz gerekir.

## Hangisini seçmelisiniz?

Sadece uzun yazıları rahat okumak istiyorsanız **Wallabag**, kanıt niteliğinde ve çok formatlı kayıtlar arıyorsanız **ArchiveBox**, birkaç önemli sayfayı taşınabilir biçimde korumak istiyorsanız **SingleFile** seçin. En sağlam çözüm ise araçları yarıştırmak değil, birleştirmektir: Wallabag günlük okuma kuyruğunu yönetebilir, değerli kaynaklar ArchiveBox’a aktarılabilir, kritik sayfalar da SingleFile ile çevrimdışı tutulabilir.

Son olarak 3-2-1 yedekleme kuralını unutmayın: verinin üç kopyası, iki farklı ortamı ve bir uzak kopyası bulunmalıdır. Çünkü iyi bir web arşivi yalnızca sayfayı yakalayan değil, yıllar sonra da geri getirebilen arşivdir.

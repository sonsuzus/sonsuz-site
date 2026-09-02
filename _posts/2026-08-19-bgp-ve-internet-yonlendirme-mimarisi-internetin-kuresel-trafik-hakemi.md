---
layout: post
title: "BGP ve İnternet Yönlendirme Mimarisi: İnternetin Küresel Trafik Hakemi"
math: true
categories: 
  - Bilgi
tags: 
  - bgp
  - ağ
  - yönlendirme
  - otonom sistem
  - siber güvenlik
toc: true
image: /img/bgp-ve-internet-40.png
---

İnternet, tek bir kurumun yönettiği dev bir ağ değildir; binlerce bağımsız ağın uzlaşarak oluşturduğu küresel bir ekosistemdir. Bir kullanıcının tarayıcısından çıkan paket, hedefe ulaşana kadar operatörler, bulut sağlayıcıları, üniversiteler ve içerik dağıtım ağları arasında dolaşabilir. Bu ağlar arası yol seçiminin temel dili ise **Border Gateway Protocol (BGP)**'dir. BGP, en kısa fiziksel yolu bulmaktan çok, ağların ticari ilişkilerini ve yönetim politikalarını dikkate alan bir rota müzakere sistemidir.

![bgp-ve-internet-40](/img/bgp-ve-internet-40.svg)

``

## Otonom Sistem: İnternetin Yönetim Birimi

Bir **Otonom Sistem (AS)**, tek bir yönetim altında bulunan ve dış dünyaya tutarlı bir yönlendirme politikası sunan IP ağları topluluğudur. Her AS, Internet Assigned Numbers Authority ekosistemindeki kayıt kuruluşlarından aldığı benzersiz bir **ASN** ile tanınır. Örneğin bir internet servis sağlayıcısı, büyük bir şirket veya bulut platformu ayrı bir AS işletebilir.

BGP'nin temel görevi, bir AS'in hangi IP ön eklerine (*prefix*) erişebildiğini komşularına duyurmasıdır. Örneğin `203.0.113.0/24` ağı için yapılan bir duyuru, kabaca “Bu hedefe bana uğrayarak erişebilirsin” anlamına gelir. Duyurunun içindeki `AS_PATH` özniteliği ise paketin geçeceği AS zincirini taşır:

$$AS\_PATH = [AS64500, AS64496, AS64497]$$

Bu zincir hem yol seçimine yardım eder hem de bir AS'in kendi numarasını tekrar görmesi durumunda döngü oluşmasını engeller. Yani BGP, klasik bağlantı durumu protokollerinden farklı olarak internete ait tam topolojiyi hesaplamaz; erişilebilirlik bilgisi ve politika öznitelikleri üzerinden karar verir.

| Özellik | OSPF / IS-IS | BGP |
|---|---|---|
| Çalışma alanı | Tek bir kurum veya AS içi | AS'ler arası |
| Ana hedef | En iyi teknik yolu bulmak | Politika tabanlı erişilebilirlik |
| Yakınsama | Görece hızlı | Daha temkinli, daha yavaş olabilir |
| Döngü önleme | Topoloji veritabanı | `AS_PATH` kontrolü |

## “En İyi Yol” Her Zaman En Kısa Yol Değildir

BGP karar süreci çok sayıda öznitelik kullanır. Uygulama ayrıntıları üreticiye göre değişse de, yaygın mantık önce yerel politikalara, sonra yol uzunluğuna bakmaktır. Basitleştirilmiş bir tercih sırası şöyledir:

1. En yüksek `LOCAL_PREF` değeri,
2. Yerel olarak üretilmiş rota,
3. En kısa `AS_PATH`,
4. Daha uygun `MED` değeri,
5. Sonraki atlama ve yönlendirici kimliği gibi bağ bozucu ölçütler.

Örneğin bir operatör, müşterisinden gelen trafiği ücretsiz veya gelir getiren kabul ettiği için müşteri rotalarına yüksek `LOCAL_PREF` verebilir. Transit sağlayıcı üzerinden gelen rota teknik olarak kısa olsa bile daha düşük öncelik alabilir. Bu yaklaşımın ekonomik özeti şu şekilde düşünülebilir:

$$Tercih = Politika + Güven + Maliyet - Gecikme$$

Bu bir BGP formülü değildir; yönlendirme kararlarının neden yalnızca kilometre hesabıyla açıklanamayacağını anlatan sezgisel bir modeldir.

## Peering, Transit ve Küresel Trafik Akışı

AS'ler genellikle üç ilişki biçiminde çalışır: müşteri-sağlayıcı, eşler arası bağlantı (*peering*) ve kurum içi bağlantılar. Bir transit sağlayıcı, müşterisinin trafiğini internete taşır. Peering yapan iki ağ ise çoğunlukla kendi müşterilerine ait trafiği doğrudan değiş tokuş eder.

| İlişki | Trafiği taşıma motivasyonu | Tipik politika |
|---|---|---|
| Müşteri → Sağlayıcı | Ücretli transit hizmeti | Müşteri rotaları genişçe duyurulur |
| Peering | Karşılıklı maliyet azaltma | Genellikle sadece müşteri rotaları paylaşılır |
| Sağlayıcı → Müşteri | Küresel erişim sağlama | Varsayılan veya tam rota verilebilir |

Bu politikalar hatalı yapılandırılırsa **yönlendirme sızıntısı (route leak)** oluşabilir. Örneğin bir AS, bir transit sağlayıcıdan öğrendiği rotaları başka bir transit sağlayıcıya yanlışlıkla duyurursa, normalde geçmemesi gereken trafik kendi üzerinden akmaya başlayabilir. Sonuç; gecikme artışı, kapasite taşması, hizmet kesintisi ve hatta küresel erişim sorunları olabilir.

## Sızıntı ve Kaçırma Arasındaki Kritik Fark

Route leak çoğunlukla yanlış politika sonucu oluşur; **BGP hijacking** ise bir AS'in kendisine ait olmayan bir IP ön ekini duyurmasıdır. Kötü niyetli ya da hatalı bir duyuru, daha spesifik ön ek kullanırsa özellikle etkili olur. Çünkü `203.0.113.0/24`, `203.0.113.0/23` rotasına göre daha spesifiktir ve yönlendiriciler genellikle **en uzun ön ek eşleşmesini** seçer.

Koruma için ağ operatörleri prefix filtreleri, maksimum önek sınırları, IRR kayıtları ve **RPKI Route Origin Validation** kullanır. RPKI, “Bu ASN bu prefix'i duyurmaya yetkili mi?” sorusuna kriptografik kayıtlarla yanıt verir. Ancak RPKI tek başına yolun tamamının güvenli olduğunu kanıtlamaz; doğru politika, sürekli izleme ve komşu doğrulaması hâlâ vazgeçilmezdir.

BGP'yi anlamak, internetin neden hem dayanıklı hem de dikkat gerektiren bir ortak altyapı olduğunu görmektir: Her rota duyurusu, teknik bir paketten çok küresel ölçekte verilmiş bir güven ve politika beyanıdır.

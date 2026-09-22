---
layout: post
title: "Anycast: Aynı IP Adresi Dünyanın Farklı Noktalarında Nasıl Bulunur?"
math: true
categories: 
  - Bilgi
tags: 
  - anycast
  - ağ
  - bgp
  - dns
  - internet
  - yönlendirme
toc: true
---

Bir IP adresini genellikle tek bir sunucunun internet üzerindeki ev adresi gibi düşünürüz. Oysa Anycast dünyasında aynı IP adresi İstanbul, Frankfurt, Singapur ve New York’taki sunucularda eş zamanlı olarak bulunabilir. Kullanıcı bu adresle bağlantı kurduğunda paketler sihirle çoğalmaz; internetin yönlendirme sistemi, kullanıcıyı ağ açısından en uygun noktaya götürür.

``

## Anycast tam olarak nedir?

Anycast, aynı IP adresinin birden fazla fiziksel konumdan ilan edilmesi tekniğidir. Farklı veri merkezlerindeki yönlendiriciler, Border Gateway Protocol yani **BGP** aracılığıyla aynı IP önekine ulaşabildiklerini internete duyurur.

Örneğin üç veri merkezinin de `203.0.113.10` adresine hizmet verdiğini düşünelim. Bu merkezler aynı IP bloğunu kendi ağlarından ilan eder. İnternet servis sağlayıcısının yönlendiricileri de BGP politikalarına göre en uygun rotayı seçer. Buradaki “en yakın” ifadesi kuş uçuşu mesafe anlamına gelmez; çoğunlukla ağ topolojisi, otonom sistem geçişleri ve operatör politikaları belirleyicidir.

Basitleştirilmiş bir rota maliyetini şöyle gösterebiliriz:

$$
R = \alpha H + \beta L + \gamma P
$$

Burada $H$ AS geçiş sayısını, $L$ gecikmeyi, $P$ ise operatör politikasından doğan maliyeti temsil eder. BGP gerçekte bu formülü doğrudan hesaplamaz; ancak denklem, “en iyi rota” kararının yalnızca fiziksel uzaklığa bağlı olmadığını anlamayı kolaylaştırır.

## Unicast ile arasındaki fark

| Özellik | Unicast | Anycast |
|---|---|---|
| IP adresini sunan konum | Genellikle tek nokta | Birden fazla nokta |
| Trafiğin hedefi | Belirli sunucu veya ağ | BGP’nin seçtiği uygun merkez |
| Gecikme | Uzak kullanıcılar için artabilir | Genellikle daha düşüktür |
| Arıza dayanıklılığı | Ek mekanizma gerektirir | Rota geri çekilerek sağlanabilir |
| Yaygın kullanım | Web sunucuları, istemciler | DNS, CDN, DDoS koruması |

Anycast bir yük dengeleyiciyle aynı şey değildir. Klasik yük dengeleyici kendisine ulaşan bağlantıları arka uç sunucularına dağıtır. Anycast ise trafik henüz hedef ağa ulaşmadan, internetin yönlendirme katmanında hangi veri merkezine gideceğini etkiler. İkisi birlikte de kullanılabilir: Anycast doğru şehri, yük dengeleyici ise o şehirdeki doğru sunucuyu seçer.

## Paketler doğru noktayı nasıl bulur?

Diyelim ki İstanbul’daki kullanıcı bir DNS hizmetinin Anycast IP adresine sorgu gönderdi. Kullanıcının servis sağlayıcısı, bu IP öneki için aldığı BGP ilanlarını karşılaştırır. Frankfurt rotası daha uygun görünüyorsa paketler oraya gider. Aynı IP’yi kullanan Tokyo’daki bir kullanıcı ise Singapur noktasına yönlendirilebilir.

Bir merkez arızalandığında ilgili BGP ilanı geri çekilir. Yönlendiriciler kalan rotalardan birini seçer ve trafik başka bir merkeze kayar. Buna **yakınsama** denir. Yakınsama anlık olmak zorunda değildir; rota bilgilerinin yayılması birkaç saniye veya daha uzun sürebilir.

Anycast davranışını incelemek için farklı ağlardan şu komutlar çalıştırılabilir:

```bash
# IP adresinin DNS kaydını öğrenir
dig +short example.com

# Paketlerin geçtiği yönlendiricileri gösterir
traceroute 203.0.113.10

# Windows üzerindeki karşılığı
tracert 203.0.113.10
```

Aynı hedef IP için farklı ülkelerde çalıştırılan `traceroute` sonuçlarının farklı veri merkezlerine ulaşması, Anycast kullanımına güçlü bir işarettir. Yine de rota isimleri yanıltıcı olabileceğinden kesin doğrulama için servis sağlayıcının ağ dokümantasyonu incelenmelidir.

## Neden özellikle DNS ve CDN sistemlerinde kullanılır?

DNS sorguları kısa ve çoğunlukla durumsuzdur; bu nedenle rota değişikliklerinden uzun ömürlü bağlantılara göre daha az etkilenir. CDN’lerde ise kullanıcıyı yakındaki bir uç noktaya taşımak gecikmeyi azaltır. Yaklaşık toplam süreyi

$$
T_{toplam} = T_{iletim} + T_{işleme} + T_{kuyruk}
$$

şeklinde düşünürsek, Anycast özellikle $T_{iletim}$ bileşenini küçültmeye yardımcı olur.

Elbette dikkat edilmesi gereken noktalar vardır. BGP rota değiştirirse uzun süreli TCP bağlantısı başka merkeze kayabilir ve kopabilir. Veri merkezlerinin aynı yapılandırmayı sunması, durum bilgisinin paylaşılması ve sağlık kontrollerinin rota ilanlarıyla ilişkilendirilmesi gerekir. Doğru tasarlandığında Anycast, tek bir IP adresini küresel ölçekte hızlı, dayanıklı ve şaşırtıcı derecede esnek bir giriş kapısına dönüştürür.

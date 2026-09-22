---
layout: post
title: "NAT ve Port Yönlendirme: Yerel Ağdaki Bilgisayar İnternete Nasıl Çıkıyor?"
math: true
categories: 
  - Bilgi
tags: 
  - nat
  - port yönlendirme
  - ağ
  - tcp-ip
  - router
  - güvenlik
toc: true
---

Evdeki bilgisayarınızın IP adresi `192.168.1.42`, ziyaret ettiğiniz web sitesinin gördüğü adres ise bambaşka olabilir. Bu küçük ağ sihrinin arkasında NAT bulunur. NAT, aynı yerel ağdaki telefon, bilgisayar ve hatta akıllı buzdolabının tek bir genel IP adresini paylaşarak internete çıkmasını sağlar.

``

## Özel ve genel IP adresleri

Yerel ağlarda çoğunlukla internette doğrudan yönlendirilemeyen **özel IP adresleri** kullanılır. Yaygın özel IPv4 aralıkları `10.0.0.0/8`, `172.16.0.0/12` ve `192.168.0.0/16` bloklarıdır. İnternet servis sağlayıcısının yönlendiricinize verdiği adres ise genellikle **genel IP adresidir**.

| Özellik | Özel IP | Genel IP |
|---|---|---|
| Kullanıldığı alan | Yerel ağ | İnternet |
| İnternette yönlendirilebilir mi? | Hayır | Evet |
| Örnek | `192.168.1.42` | `203.0.113.25` |
| Benzetme | Apartman daire numarası | Binanın sokak adresi |

IPv4 adresi 32 bitten oluştuğu için teorik adres sayısı şöyledir:

$$2^{32} = 4.294.967.296$$

Bu sayı günümüzdeki cihaz miktarı için yetersizdir. NAT, birçok cihazın tek genel adresi paylaşmasını sağlayarak IPv4 kıtlığını hafifletmiştir.

## NAT paketi nasıl dönüştürür?

Bilgisayarınız `93.184.216.34:443` adresine bağlanırken örneğin `192.168.1.42:51500` kaynak bilgisini kullanır. Yönlendirici paketin kaynak adresini ve çoğunlukla portunu değiştirir:

```text
192.168.1.42:51500  ->  203.0.113.25:62001
```

Bu yönteme günlük kullanımda NAT dense de portların da çevrildiği biçimi **PAT** veya **NAT Overload** olarak adlandırılır. Yönlendirici bir eşleştirme tablosu tutar:

| Yerel uç | Genel uç | Hedef |
|---|---|---|
| `192.168.1.42:51500` | `203.0.113.25:62001` | `93.184.216.34:443` |
| `192.168.1.18:53020` | `203.0.113.25:62002` | `93.184.216.34:443` |

Kabaca aynı genel IP üzerinden kurulabilecek bağlantıların port uzayı $2^{16}=65.536$ değerine dayanır. Ancak ayrılmış portlar, protokoller ve zaman aşımı kuralları nedeniyle pratik kapasite farklıdır.

Yanıt `203.0.113.25:62001` adresine geldiğinde yönlendirici tablosuna bakar ve paketi `192.168.1.42:51500` adresine yollar. Böylece doğru cihaz yanıtı alır. Dışarıdan rastgele gelen ve tabloda karşılığı olmayan trafik ise genellikle içeri geçirilmez.

## Port yönlendirme neden gerekir?

Yerel ağınızdaki bir web sunucusuna internetten erişmek istediğinizi düşünün. Dışarıdan gelen bağlantıyı başlatan taraf siz olmadığınız için NAT tablosunda hazır bir kayıt bulunmaz. **Port yönlendirme**, yönlendiriciye kalıcı bir teslimat kuralı verir:

```text
Genel IP:8080  ->  192.168.1.50:80
```

Böylece ziyaretçi genel adresinizin `8080` numaralı portuna bağlandığında istek içerideki web sunucusunun `80` numaralı portuna gönderilir. Linux üzerinde yönlendirme davranışını kavramsal olarak gösteren bir `iptables` kuralı şöyledir:

```bash
sudo iptables -t nat -A PREROUTING -p tcp \
  --dport 8080 -j DNAT --to-destination 192.168.1.50:80
```

Bu komut, TCP `8080` trafiğinin hedefini değiştirir. Gerçek kurulumda IP yönlendirme, güvenlik duvarı izinleri ve dönüş rotası da doğru yapılandırılmalıdır.

## Güvenlik ve CGNAT sürprizi

Port yönlendirme, cihazı internete açtığı için yalnızca gerekli portlar kullanılmalı; yazılımlar güncel tutulmalı, güçlü kimlik doğrulama ve mümkünse VPN tercih edilmelidir. NAT tek başına güvenlik duvarı değildir; yalnızca adres çevirir.

Servis sağlayıcınız **CGNAT** kullanıyorsa yönlendiriciniz bile gerçek bir genel IPv4 adresine sahip olmayabilir. Bu durumda kendi yönlendiricinizde açtığınız port internete ulaşmaz. Genel IP talep etmek, IPv6 kullanmak, VPN tüneli veya ters proxy kurmak çözüm olabilir.

Özetle NAT, içeriden başlatılan bağlantıları kaydedip yanıtları doğru cihaza teslim eden bir resepsiyonisttir. Port yönlendirme ise resepsiyona bırakılan kalıcı talimattır: “Bu porta gelenleri doğrudan şu odaya gönder!”

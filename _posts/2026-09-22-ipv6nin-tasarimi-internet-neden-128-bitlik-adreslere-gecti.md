---
layout: post
title: "IPv6’nın Tasarımı: İnternet Neden 128 Bitlik Adreslere Geçti?"
math: true
categories: 
  - Bilgi
tags: 
  - ipv6
  - ağ
  - internet
  - ip-adresleme
  - network
  - siber-güvenlik
toc: true
image: /img/ipv6nin-tasarimi-internet-98.png
---

![ipv6nin-tasarimi-internet-98](/img/ipv6nin-tasarimi-internet-98.svg)


İnternete bağlanan her cihazın bir adrese ihtiyacı vardır. Bilgisayarlar, telefonlar, sunucular ve hatta akıllı ampuller, veri paketlerinin nereye gideceğini IP adresleri sayesinde bilir. IPv4 uzun yıllar bu görevi başarıyla yürüttü; ancak internet büyüdükçe 32 bitlik adres alanının sınırları görünür hâle geldi. IPv6’nın 128 bitlik adresleri, yalnızca “daha fazla cihaz bağlayalım” düşüncesinin değil, ölçeklenebilir ve daha düzenli bir internet tasarlama hedefinin sonucudur.
``

## IPv4 neden yetersiz kaldı?

IPv4 adresleri 32 bitten oluşur. Teorik adres sayısı:

$$2^{32} = 4.294.967.296$$

Yaklaşık 4,3 milyar adres, IPv4 tasarlanırken devasa görünüyordu. Ne var ki bazı adres blokları özel ağlara, çoklu yayına, testlere ve başka amaçlara ayrıldı. Ayrıca adreslerin kurumlara bloklar hâlinde tahsis edilmesi, kullanılmayan adreslerin de fiilen rezerve edilmesine yol açtı.

İnternetin küreselleşmesi, mobil cihazlar, bulut sistemleri ve Nesnelerin İnterneti bu alanı hızla tüketti. Geçici çözüm olarak geliştirilen NAT, birden fazla cihazın tek genel IPv4 adresini paylaşmasını sağladı. Fakat NAT, internetin başlangıçtaki “uçtan uca bağlantı” modelini karmaşıklaştırdı.

| Özellik | IPv4 | IPv6 |
|---|---:|---:|
| Adres uzunluğu | 32 bit | 128 bit |
| Teorik adres sayısı | $2^{32}$ | $2^{128}$ |
| Yazım biçimi | Ondalık | Onaltılık |
| NAT ihtiyacı | Genellikle yüksek | Temel tasarımda düşük |
| Otomatik yapılandırma | Sınırlı | Yerleşik destek |

## Neden 64 değil de 128 bit?

64 bitlik bir adres alanı bile yaklaşık $2^{64}$, yani 18 kentilyon adres sağlayabilirdi. Ancak IPv6 tasarımcıları yalnızca bugünkü cihaz sayısını karşılamayı hedeflemedi. Adreslerin coğrafi bölgelere, servis sağlayıcılara, kurumlara, alt ağlara ve cihazlara hiyerarşik biçimde dağıtılabilmesi için geniş bir alan gerekliydi.

IPv6 adresleri çoğunlukla iki mantıksal parçayla düşünülür:

$$128 = 64\text{ bit ağ öneki} + 64\text{ bit arayüz kimliği}$$

İlk 64 bit ağın nerede olduğunu, kalan 64 bit ise ağ içindeki arayüzü tanımlayabilir. Bu ayrım, yönlendirme tablolarının daha düzenli tutulmasına ve cihazların SLAAC ile kendi adreslerini otomatik oluşturmasına yardımcı olur. Başka bir deyişle 128 bit, yalnızca kapasite değil, adresleme mimarisi için seçilmiştir.

Teorik IPv6 adres sayısı şöyledir:

$$2^{128} = 340.282.366.920.938.463.463.374.607.431.768.211.456$$

Bu sayı, Dünya üzerindeki her metrekareye inanılmaz miktarda adres düşmesi demektir. Amaç bütün adresleri kullanmak değil; adresleri cimrilik yapmadan, hiyerarşik ve yönetilebilir şekilde tahsis edebilmektir.

## IPv6 adresleri nasıl okunur?

IPv6, sekiz adet 16 bitlik grubun iki nokta ile ayrıldığı onaltılık gösterimi kullanır:

```text
2001:0db8:0000:0000:0212:34ff:fe56:789a
```

Baştaki sıfırlar atılabilir, art arda gelen sıfır grupları ise bir kez `::` ile kısaltılabilir:

```text
2001:db8::212:34ff:fe56:789a
```

Bir sistemde IPv6 adreslerini görüntülemek için Linux üzerinde şu komut kullanılabilir:

```bash
ip -6 address show
```

Komut, ağ arayüzlerine atanmış IPv6 adreslerini ve önek uzunluklarını gösterir. Örneğin `/64`, ilk 64 bitin ağ öneki olduğunu belirtir.

## Daha çok adresten fazlası

IPv6; yönlendiriciler tarafından parçalama yapılmaması, daha sade bir temel başlık, otomatik adres yapılandırması ve çoklu yayın kullanımının geliştirilmesi gibi tasarım yenilikleri de getirir. Güvenlik tarafında IPsec desteği standartlaştırılmıştır; ancak bu, her IPv6 bağlantısının kendiliğinden güvenli olduğu anlamına gelmez. Güvenlik duvarı kuralları hâlâ gereklidir.

128 bitlik seçim biraz “geleceğe fazla hazırlıklı olmak” gibi görünebilir. Aslında internet altyapısını tekrar adres kıtlığı nedeniyle değiştirmemek için bilinçli bir mühendislik kararıdır. IPv6, adresleri bolca dağıtırken ağların daha düzenli büyümesine izin verir; yani mesele yalnızca daha büyük bir sayı değil, daha sürdürülebilir bir internettir.

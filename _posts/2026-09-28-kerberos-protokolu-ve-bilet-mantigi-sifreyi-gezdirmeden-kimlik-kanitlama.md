---
layout: post
title: "Kerberos Protokolü ve Bilet Mantığı: Şifreyi Gezdirmeden Kimlik Kanıtlama"
math: true
categories: 
  - Bilgi
tags: 
  - kerberos
  - siber güvenlik
  - kimlik doğrulama
  - ağ protokolleri
  - şifreleme
  - dağıtık sistemler
toc: true
image: /img/kerberos-protokolu-ve-38.png
---

Bir şirket ağında dosya sunucusuna, e-posta sistemine ve veritabanına bağlandığınızı düşünün. Her servise parolanızı ayrı ayrı göndermek hem riskli hem de yorucu olurdu. Kerberos, parolayı ağda dolaştırmak yerine güvenilir bir merkezden alınan, kısa ömürlü ve şifreli **biletlerle** kimlik kanıtlar. Adını mitolojide yeraltı kapısını koruyan üç başlı köpekten alması da tesadüf değildir: protokolün dünyasında kapılar sıkı korunur.

``

## Temel fikir: Parola değil, kanıt gönder

Kerberos mimarisinin merkezinde **Key Distribution Center (KDC)** bulunur. KDC genellikle iki mantıksal parçadan oluşur:

- **Authentication Server (AS):** Kullanıcıyı ilk kez doğrular.
- **Ticket Granting Server (TGS):** Belirli servisler için bilet üretir.

Kullanıcı, servis ve KDC önceden kendilerine ait uzun süreli gizli anahtarlara sahiptir. Kullanıcının anahtarı çoğunlukla parolasından türetilir. Parolanın kendisi sunucuya gönderilmez; istemci, bu anahtarla şifrelenmiş bir zaman damgası gibi **ön kimlik doğrulama** verileri sunar.

| Kavram | Ne işe yarar? | Kim okuyabilir? |
|---|---|---|
| TGT | Yeni servis biletleri istemeyi sağlar | TGS |
| Servis bileti | Belirli bir servise erişim sağlar | Hedef servis |
| Authenticator | İsteğin güncel olduğunu kanıtlar | İlgili oturum anahtarına sahip taraf |
| Oturum anahtarı | Tarafların geçici ve güvenli konuşmasını sağlar | İstemci ve ilgili sunucu |

## Bilet yolculuğu

İlk aşamada istemci, AS'ye kullanıcı adını ve gerekli ön doğrulama verisini yollar. Doğrulama başarılıysa AS, istemciye bir **Ticket Granting Ticket (TGT)** verir. TGT; kullanıcının kimliğini, geçerlilik süresini ve istemci-TGS oturum anahtarını içerir. Bu paket TGS'nin uzun süreli anahtarıyla şifrelendiği için istemci içeriğini değiştiremez.

İstemci daha sonra örneğin `fileserver` servisine ulaşmak istediğinde TGT'yi, servis adını ve güncel bir authenticator'ı TGS'ye gönderir. TGS geçerlilik kontrollerini yapar ve hedef servisin anahtarıyla şifrelenmiş bir **servis bileti** üretir.

Son aşamada istemci, servis biletini hedef sunucuya sunar. Sunucu kendi anahtarıyla bileti açar, authenticator'ı kontrol eder ve erişim kararını verir. İstenirse sunucu da yanıt üreterek kimliğini istemciye kanıtlar; buna **karşılıklı kimlik doğrulama** denir.

Akış kısaca şöyledir:

```text
İstemci → AS     : Ön doğrulama isteği
AS → İstemci     : TGT + istemci/TGS oturum anahtarı
İstemci → TGS    : TGT + authenticator + servis adı
TGS → İstemci    : Servis bileti + yeni oturum anahtarı
İstemci → Servis : Servis bileti + authenticator
Servis → İstemci : İsteğe bağlı karşılıklı doğrulama yanıtı
```

## Zaman neden bu kadar önemli?

Bir saldırgan ağ trafiğinden geçerli bir paketi kopyalayıp yeniden gönderirse **replay saldırısı** yapabilir. Kerberos bunu zaman damgaları, kısa bilet ömürleri ve daha önce görülen authenticator kayıtlarıyla sınırlar. Kabul koşulu basitçe şöyle gösterilebilir:

$$\vert t_{sunucu} - t_{istemci}\vert  \leq \Delta$$

Buradaki $\Delta$, izin verilen saat sapmasıdır. Bu nedenle Kerberos ortamında NTP gibi saat eşitleme mekanizmaları kritik öneme sahiptir. Saatler ciddi biçimde ayrılırsa doğru parola bile sizi kurtaramaz; protokol bileti bayat sanabilir.

Aşağıdaki sözde kod, servis tarafındaki kontrol mantığını özetler:

```python
def bileti_dogrula(ticket, authenticator, simdi):
    veri = servis_anahtariyla_ac(ticket)
    kanit = veri.oturum_anahtariyla_ac(authenticator)

    if simdi > veri.son_kullanma:
        return False
    if abs(simdi - kanit.zaman) > IZIN_VERILEN_SAPMA:
        return False
    if replay_cache.icinde(kanit):
        return False

    replay_cache.ekle(kanit)
    return veri.kullanici == kanit.kullanici
```

Bu kod gerçek şifreleme ayrıntılarını soyutlar; ancak üç temel denetimi gösterir: bilet süresi, saat yakınlığı ve tekrar kullanım kontrolü.

## Güçlü ama sihirli değil

Kerberos merkezi güven, hızlı tek oturum açma ve parolanın servislere açıklanmaması gibi önemli avantajlar sunar. Buna karşılık KDC kritik altyapıdır; erişilebilirliği ve anahtarları dikkatle korunmalıdır. Zayıf parolalar çevrimdışı tahmin saldırılarına kapı aralayabilir, ele geçirilmiş servis anahtarları da sahte bilet riskini artırabilir. Doğru yapılandırıldığında Kerberos'un özeti nettir: **Parolanı her kapıya söyleme; güvenilir gişeden süreli bir bilet al.**

![kerberos-protokolu-ve-38](/img/kerberos-protokolu-ve-38.svg)


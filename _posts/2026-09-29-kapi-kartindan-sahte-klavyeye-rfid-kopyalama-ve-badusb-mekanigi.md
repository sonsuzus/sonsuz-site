---
layout: post
title: "Kapı Kartından Sahte Klavyeye: RFID Kopyalama ve BadUSB Mekaniği"
math: true
categories: 
  - Bilgi
tags: 
  - siber güvenlik
  - rfid
  - badusb
  - fiziksel güvenlik
  - usb
  - hid
toc: true
image: /img/kapi-kartindan-sahte-88.png
---

Bir binanın kapısı kartla açılıyor, bilgisayarlar parola ile korunuyor ve ağ güvenlik duvarının arkasında duruyor olabilir. Ancak saldırgan birkaç saniyeliğine masaya ya da karta erişebiliyorsa bütün bu önlemler beklenmedik biçimde aşılabilir. RFID kopyalama ve klavye gibi davranan BadUSB cihazları, siber güvenliğin yalnızca ağ paketlerinden ibaret olmadığını gösteren iki çarpıcı örnektir.

![kapi-kartindan-sahte-88](/img/kapi-kartindan-sahte-88.svg)

``

## RFID sistemleri aslında ne yapar?

RFID, radyo dalgalarıyla kimlik bilgisinin okuyucuya aktarılması prensibine dayanır. Pasif kartlarda pil bulunmaz; okuyucunun oluşturduğu elektromanyetik alan karta enerji sağlar. Kart daha sonra taşıdığı bilgiyi geri iletir. Buradaki kritik soru şudur: Kart yalnızca sabit bir numara mı gönderiyor, yoksa kriptografik olarak doğrulanıyor mu?

Basit sistemlerde kartın kimliği değişmeyen bir seri numarası olabilir. Bu numaranın okunup başka bir uyumlu etikette taklit edilmesi, teknik olarak kartın fiziksel biçimini değil, verdiği cevabı kopyalamaktır. Güvenli sistemler ise rastgele meydan okuma ve kriptografik cevap mekanizmaları kullanır.

Bir kimlik alanı $n$ bit ise teorik olası değer sayısı:

$$N = 2^n$$

olur. Fakat büyük bir kimlik alanı tek başına güvenlik sağlamaz. Seri numarası kablosuz olarak açık biçimde okunabiliyorsa saldırganın tüm alanı taramasına gerek kalmaz; doğrudan gözlemlediği değeri tekrar kullanabilir.

| Özellik | Basit RFID sistemi | Güvenli akıllı kart sistemi |
|---|---|---|
| Kimlik doğrulama | Sabit UID | Kriptografik meydan okuma-cevap |
| Tekrar saldırısı | Daha olası | Sayaç veya oturum verisiyle zorlaştırılır |
| Anahtar yönetimi | Yok ya da zayıf | Kart başına çeşitlendirilmiş anahtarlar |
| Kayıp kart riski | Yüksek | Hızlı iptal ve merkezi politika |

Bu nedenle kartı metal bir kılıfa koymak faydalı olsa da tek çözüm değildir. Asıl savunma; modern kart teknolojisi, kart başına anahtar, geçiş kayıtlarının izlenmesi ve hassas alanlarda ikinci faktördür.

## BadUSB neden sıradan bellek değildir?

USB bağlantısında cihaz, bilgisayara hangi sınıfa ait olduğunu bildirir. İşletim sistemi bir klavye gördüğünde genellikle kullanıcı onayı istemeden HID sürücüsünü yükler. BadUSB yaklaşımı, cihazın depolama belleği yerine ya da onun yanında klavye olarak tanıtılmasını kullanır.

Cihazın mikrodenetleyicisi önceden tanımlanmış tuş dizilerini çok hızlı gönderebilir. Mekanik süreç kabaca şöyledir:

```text
USB bağlantısını algıla
Kendini HID klavye olarak tanıt
İşletim sisteminin hazır olmasını bekle
Zararsız test metnini yaz
İşlemi durdur ve kayıt oluştur
```

Bu akış yalnızca mekaniği açıklar; gerçek sistemlerde komut çalıştıran örnekler kullanmak güvenli değildir. Temel tehlike, bilgisayarın tuşları yetkili kullanıcının yazdığını varsaymasıdır. Yaklaşık $k$ tuşluk bir dizinin saniyede $r$ tuş hızında gönderilme süresi:

$$t \approx \frac{k}{r}$$

şeklindedir. Örneğin 300 tuş, saniyede 50 tuşla yaklaşık 6 saniyede iletilebilir.

## Savunma görünürlükle başlar

Windows ortamında bağlı klavye sınıfı cihazları envanterlemek için aşağıdaki savunmacı PowerShell sorgusu kullanılabilir:

```powershell
Get-PnpDevice -PresentOnly |
  Where-Object { $_.Class -eq 'Keyboard' } |
  Select-Object Status, FriendlyName, InstanceId
```

Kod yalnızca mevcut klavye aygıtlarını listeler; bilinmeyen üretici veya beklenmedik cihaz kimliklerinin araştırılmasına yardımcı olur. Kurumsal ölçekte sonuçlar merkezi cihaz yönetimi ve olay kayıtlarıyla ilişkilendirilmelidir.

| Risk | Etkili kontrol |
|---|---|
| Yetkisiz USB klavye | USB cihaz izin listesi |
| Kilitsiz bilgisayar | Kısa otomatik ekran kilidi |
| RFID kart kopyalama | Kriptografik kart ve ikinci faktör |
| Sahipsiz cihaz | Güvenlik farkındalığı ve teslim prosedürü |
| Fiziksel erişim | Kamera, turnike ve ziyaretçi kaydı |

Sonuç basit: Tanımadığınız USB cihazını bağlamayın, erişim kartınızı ödünç vermeyin ve fiziksel erişimi güven sınırının dışında bırakmayın. En iyi güvenlik duvarı bile saldırgan zaten klavyenizin başındaysa tek başına yeterli değildir.

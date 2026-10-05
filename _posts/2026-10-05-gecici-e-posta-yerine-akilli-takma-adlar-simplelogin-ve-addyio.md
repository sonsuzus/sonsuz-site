---
layout: post
title: "Geçici E-Posta Yerine Akıllı Takma Adlar: SimpleLogin ve Addy.io"
math: true
categories: 
  - Bilgi
tags: 
  - geçici e-posta
  - simplelogin
  - addy.io
  - gizlilik
  - e-posta güvenliği
  - alias
toc: true
image: /img/gecici-e-posta-45.png
---

Bir siteye üye olduktan birkaç gün sonra gelen “kaçırılmayacak fırsatlar” yüzünden ana gelen kutunuz dijital bir pazara döndüyse yalnız değilsiniz. SimpleLogin ve Addy.io, gerçek adresinizi paylaşmadan her hizmet için farklı e-posta takma adları oluşturmanızı sağlar. Böylece hangi sitenin adresinizi sızdırdığını görebilir, sorunlu adresi tek hareketle kapatabilirsiniz.

``

## Geçici posta kutusu mu, e-posta takma adı mı?

SimpleLogin ve Addy.io klasik anlamda birkaç dakika sonra yok olan geçici posta kutuları değildir. Bunlar birer **e-posta yönlendirme ve kimlik maskeleme sistemi**dir. Oluşturduğunuz takma adlara gelen mesajlar, aracı sunucu üzerinden gerçek posta kutunuza iletilir.

Akış basitçe şöyledir:

$$Gönderen \rightarrow Takma\ Ad \rightarrow Yönlendirme\ Sunucusu \rightarrow Gerçek\ Adres$$

Yanıt verdiğinizde sistem ters yönlü bir maskeleme uygular. Karşı taraf gerçek adresinizi değil, kullandığınız takma adı görür. Bu özellik, yalnızca mesaj almak için tasarlanan birçok tek kullanımlık posta servisinden önemli ölçüde daha kullanışlıdır.

| Yöntem | Kalıcılık | Yanıt gönderme | Gizlilik | Uygun kullanım |
|---|---:|---:|---:|---|
| Geçici posta kutusu | Dakika veya saat | Genellikle yok | Orta | Tek seferlik doğrulama |
| `+` adresleme | Kalıcı | Var | Düşük | Basit filtreleme |
| SimpleLogin | Kullanıcı kapatana kadar | Var | Yüksek | Günlük üyelikler |
| Addy.io | Kullanıcı kapatana kadar | Var | Yüksek | Çok sayıda otomatik alias |

![gecici-e-posta-45](/img/gecici-e-posta-45.svg)


`adiniz+magaza@example.com` biçimindeki artı adresleme pratik olsa da gerçek adresinizi tahmin etmeyi kolaylaştırır. Takma ad servislerinde ise `rastgele-kelime@alan.com` gibi bağımsız bir adres görünür.

## Gizlilik mantığı ve tehdit modeli

Her hizmet için ayrı alias kullanıldığını varsayalım. Toplam $T$ üyeliğinizden $L$ tanesi adresinizi istenmeyen listelere aktardıysa kontrol oranını yaklaşık olarak

$$R = 1 - \frac{L}{T}$$

şeklinde düşünebiliriz. Aynı gerçek adres her yerde kullanılırsa hangi hizmetin sızıntıya yol açtığını belirlemek zordur. Ayrı alias modelinde spam gelen adres doğrudan kaynağı işaret eder; onu devre dışı bırakmak diğer hesapları etkilemez.

Yine de servis sağlayıcı yönlendirme için mesajları işler. Bu nedenle güçlü parola, iki faktörlü doğrulama ve mümkünse PGP şifreleme kullanılmalıdır. Çok kritik hesaplarda kurtarma adresinin kaybedilmesi ciddi sonuçlar doğurabileceğinden alan adı ve yedekleme planı ayrıca düşünülmelidir.

## SimpleLogin ve Addy.io karşılaştırması

| Özellik | SimpleLogin | Addy.io |
|---|---|---|
| Yaklaşım | Kontrollü alias oluşturma | Hızlı ve otomatik alias üretimi |
| Açık kaynak | Evet | Evet |
| Kendi sunucuna kurma | Desteklenir | Desteklenir |
| Özel alan adı | Ücretli planlarda güçlü | Ücretli planlarda güçlü |
| Ekosistem | Proton ile bütünleşik | Bağımsız ve esnek |

SimpleLogin, düzenli bir kontrol paneli ve Proton ekosistemiyle yakın entegrasyon isteyenler için çekicidir. Addy.io ise alan adını yazarak anında yeni takma ad kullanma yaklaşımıyla öne çıkar. Plan limitleri zamanla değişebileceğinden seçimden önce güncel fiyat ve bant genişliği koşulları incelenmelidir.

## Yönlendirme mantığını kodla anlamak

Aşağıdaki Python örneği gerçek e-posta göndermez; gelen alıcı adresinin kayıtlı bir alias olup olmadığını denetleyen temel yönlendirme kararını gösterir:

```python
aliases = {
    "oyun@alias.example": "ana@posta.example",
    "magaza@alias.example": "ana@posta.example"
}

def route_mail(recipient: str) -> str:
    normalized = recipient.strip().lower()

    if normalized not in aliases:
        raise ValueError("Alias kapalı veya tanımsız")

    return aliases[normalized]

try:
    destination = route_mail("magaza@alias.example")
    print(f"Mesaj güvenli biçimde {destination} adresine yönlendirilecek.")
except ValueError as error:
    print(error)
```

Gerçek sistemlerde bu kontrolün ardından spam filtreleme, DKIM/SPF doğrulaması, ters alias üretimi ve SMTP iletimi gelir. Ayrıca günlüklerin ne kadar süre tutulduğu da gizlilik açısından önemlidir.

## Hangisini seçmeli?

Proton Mail kullanıyor ve sade bir deneyim istiyorsanız SimpleLogin güçlü bir adaydır. Sınırsıza yakın, hızlı alias üretme alışkanlığı arıyorsanız Addy.io daha doğal gelebilir. En iyi strateji ise banka gibi kritik hesaplarda kalıcı ve özel alias, deneme üyeliklerinde kolayca kapatılabilen alias kullanmaktır. Böylece gelen kutunuz sakin, dijital kimliğiniz ise parçalanmış ve izlenmesi daha zor kalır.

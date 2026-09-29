---
layout: post
title: "Sosyal Mühendisliğin Bilişsel Sınırları: Phishing Neden Hâlâ İşe Yarıyor?"
math: true
categories: 
  - Bilgi
tags: 
  - siber güvenlik
  - phishing
  - sosyal mühendislik
  - bilişsel önyargılar
  - psikoloji
  - farkındalık
toc: true
image: /img/sosyal-muhendisligin-bilissel-95.png
---

Oltalama saldırıları, en güçlü güvenlik duvarının bile her zaman koruyamadığı bir hedefe yönelir: insan zihnine. Sahte bir “hesabınız kapatılacak” mesajı geldiğinde teknik bilgimiz kaybolmaz; fakat korku, acelecilik ve otorite algısı düşünme biçimimizi geçici olarak değiştirebilir. Phishing’in başarısı çoğu zaman yazılımdaki açıktan değil, beynimizin hızlı karar vermek için kullandığı kestirme yollardan doğar.
``

## Sorun bilgisizlikten ibaret değil

İnsan beyni her kararı uzun uzun analiz etmez. Daniel Kahneman’ın popülerleştirdiği yaklaşımla düşünürsek iki temel işleyişten söz edebiliriz: hızlı, sezgisel ve otomatik **Sistem 1** ile yavaş, sorgulayıcı ve çaba gerektiren **Sistem 2**. Oltalama mesajları, Sistem 2 devreye girmeden kullanıcıyı tıklamaya yöneltmeye çalışır.

Bir kullanıcının mesajı tehlikeli bulma olasılığını basitleştirilmiş biçimde şöyle düşünebiliriz:

$$
P(\text{şüphe}) = \sigma(B + E - K - A - O)
$$

Burada $B$ güvenlik bilgisini, $E$ mesajı incelemek için ayrılan zamanı, $K$ korkuyu, $A$ aceleciliği ve $O$ otorite baskısını temsil eder. $\sigma$ ise sonucu 0 ile 1 arasına taşıyan lojistik fonksiyondur. Bu bilimsel bir saldırı formülü değil; duygusal baskı arttıkça şüphe üretme kapasitesinin nasıl zayıflayabildiğini anlatan kavramsal bir modeldir.

## Saldırganların hedeflediği bilişsel düğmeler

| Psikolojik etken | Tipik mesaj yaklaşımı | Oluşturduğu kısa yol | Savunma davranışı |
|---|---|---|---|
| Korku | “Hesabınız askıya alındı” | Tehdidi hemen durdurma | Ayrı kanaldan doğrulama |
| Acelecilik | “10 dakika içinde işlem yapın” | Ayrıntıları atlama | Bilinçli bekleme süresi |
| Otorite | “Genel müdürün acil talebi” | Emri sorgulamama | Yetki ve kimlik kontrolü |
| Merak | “Gizli maaş listesi” | Sonucu görme arzusu | Ek ve bağlantıyı açmama |
| Sosyal kanıt | “Tüm ekip tamamladı” | Çoğunluğa uyma | Resmî duyuruyu kontrol etme |

Bu yöntemlerin etkili olması, mağdurun “saf” olduğu anlamına gelmez. Yoğun iş yükü, mobil ekranların alan adını gizlemesi, bildirim yorgunluğu ve gerçek kurumların da acil dil kullanması saldırganın oluşturduğu bağlamı güçlendirir. Üstelik üretken yapay zekâ sayesinde yazım hatalarıyla dolu klasik mesajların yerini daha akıcı ve kişiselleştirilmiş metinler alabilir.

## Küçük bir savunma aracı

Aşağıdaki Python örneği, bir mesajdaki baskı ifadelerini sayarak basit bir risk puanı üretir. Gerçek bir e-posta güvenlik ürününün yerini tutmaz; eğitimlerde mesaj dilinin neden şüpheli olduğunu görünür kılmak için kullanılabilir.

```python
riskli_ifadeler = {
    "acil": 2,
    "hemen": 2,
    "askıya alınacak": 3,
    "şifrenizi doğrulayın": 4,
    "gizli": 1
}

def risk_puani(mesaj):
    metin = mesaj.casefold()
    bulunanlar = {
        ifade: agirlik
        for ifade, agirlik in riskli_ifadeler.items()
        if ifade in metin
    }
    return sum(bulunanlar.values()), bulunanlar

puan, nedenler = risk_puani(
    "Acil: Hesabınız askıya alınacak, şifrenizi doğrulayın."
)
print(puan, nedenler)
```

Kod, eşleşen ifadelerin ağırlıklarını toplar ve puanın neden yükseldiğini gösterir. Ancak yalnızca kelime aramak yanlış pozitifler üretir; bağlam, gönderen alan adı, bağlantı hedefi ve kimlik doğrulama sonuçları da değerlendirilmelidir.

## Eğitim yerine davranış tasarımı

Yılda bir kez gösterilen “şüpheli bağlantıya tıklamayın” sunumu yeterli değildir. Kurumlar, çalışanların tereddüt ettiğinde cezalandırılmadan soru sorabildiği bir kültür kurmalıdır. E-posta istemcisine kolay bir bildirim düğmesi eklemek, kritik ödeme taleplerinde ikinci kişi onayı istemek ve çok faktörlü kimlik doğrulama kullanmak bilişsel yükü azaltır.

En etkili kişisel yöntem ise kısa bir duraklama protokolüdür: **Dur, kaynağı kontrol et, başka kanaldan doğrula, sonra işlem yap.** Phishing hız ister; savunma birkaç saniyelik bilinçli yavaşlamayla başlar. İnsan zihnini kusur olarak görmek yerine sınırlarını kabul eden sistemler tasarladığımızda sosyal mühendisliğin hareket alanı belirgin biçimde daralır.

![sosyal-muhendisligin-bilissel-95](/img/sosyal-muhendisligin-bilissel-95.svg)


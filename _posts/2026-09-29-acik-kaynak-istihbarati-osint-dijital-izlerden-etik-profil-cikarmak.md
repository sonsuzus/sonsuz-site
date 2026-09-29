---
layout: post
title: "Açık Kaynak İstihbaratı (OSINT): Dijital İzlerden Etik Profil Çıkarmak"
math: true
categories: 
  - Bilgi
tags: 
  - osint
  - siber güvenlik
  - dijital iz
  - istihbarat
  - sosyal ağlar
  - veri analizi
toc: true
image: /img/acik-kaynak-istihbarati-20.png
---

İnternette attığımız her adım; kullanıcı adları, alan adı kayıtları, fotoğraf metadataları ve herkese açık belgeler biçiminde küçük kırıntılar bırakır. Açık Kaynak İstihbaratı, yani OSINT, bu dağınık kırıntıları yasal ve etik sınırlar içinde toplayarak doğrulanabilir bilgiye dönüştürme disiplinidir. Amaç birkaç arama sonucunu yan yana koymak değil, dijital izler arasındaki ilişkileri sistematik biçimde analiz etmektir.
``

## OSINT tam olarak nedir?

OSINT, erişimi herkese açık kaynaklardan bilgi toplama, doğrulama ve anlamlandırma sürecidir. Arama motorları, sosyal ağlar, şirket sicilleri, resmi gazeteler, sertifika kayıtları, haber arşivleri ve internet arşivleri bu kapsama girebilir.

Buradaki kritik ayrım **veri** ile **istihbarat** arasındadır. Bir sosyal medya gönderisi ham veridir. Gönderinin zamanı, konumu ve diğer güvenilir kaynaklarla ilişkisi incelendiğinde ise karar vermeyi destekleyen istihbarata dönüşebilir:

$$\text{İstihbarat} = \text{Veri} + \text{Bağlam} + \text{Doğrulama}$$

Bir bilginin internette bulunması onun doğru, güncel veya kullanılmasının etik olduğu anlamına gelmez. Özellikle sızdırılmış veritabanları kişisel veri, telif ve bilişim hukuku bakımından ciddi risk taşır. Yetkisiz veri kümelerini indirmek, sorgulamak veya yaymak yerine ihlalin varlığını güvenilir güvenlik bildirimleri ve resmi açıklamalar üzerinden doğrulamak gerekir.

## Kaynakların karşılaştırılması

| Kaynak | Sağlayabileceği bilgi | Temel risk | Doğrulama yöntemi |
|---|---|---|---|
| Sosyal ağlar | İlgi alanları, bağlantılar, zaman çizelgesi | Sahte hesap ve eski içerik | Hesap geçmişi ve çapraz kaynak |
| Kamu kayıtları | Şirket, ihale veya ruhsat bilgileri | Güncelliğini yitirmiş kayıt | Resmî kurum ve tarih kontrolü |
| Alan adı kayıtları | Kayıt tarihleri, DNS ilişkileri | Gizlilik servisleri | DNS ve sertifika kayıtları |
| Haber arşivleri | Olay geçmişi ve açıklamalar | Editoryal hata veya taraflılık | Birden fazla bağımsız yayın |
| İhlal bildirimleri | Hesap bilgilerinin etkilenme ihtimali | Hukuka aykırı veri kullanımı | Resmî bildirim ve güvenilir servis |

## Hipotez kur, sonra kanıt ara

Sağlıklı bir araştırma, peşinen verilmiş bir hükmü kanıtlamaya çalışmaz. Önce araştırma sorusu belirlenir, ardından alternatif hipotezler oluşturulur. Örneğin aynı kullanıcı adını taşıyan iki hesabın aynı kişiye ait olduğu yalnızca bir varsayımdır. Profil fotoğrafı, paylaşım saatleri veya benzer biyografi metni destekleyici olabilir; ancak tek başına kesin kimlik kanıtı değildir.

Kanıtların güven düzeyi basit bir ağırlıklı modelle ifade edilebilir:

$$C = \frac{\sum_{i=1}^{n} w_i r_i}{\sum_{i=1}^{n} w_i}$$

Burada $r_i$ kaynağın güvenilirlik puanını, $w_i$ ise araştırma açısından önemini temsil eder. Bu puan matematiksel kesinlik sağlamaz; analistin neden bir sonuca ulaştığını görünür kılar.

## Küçük bir veri normalleştirme örneği

Aşağıdaki Python kodu, yalnızca izinli veya örnek bir veri kümesindeki kullanıcı adlarını standartlaştırır ve tekrar sayılarını çıkarır. Böylece büyük-küçük harf ya da gereksiz boşluklar yüzünden aynı takma adın farklı görünmesi engellenir.

```python
from collections import Counter

aliases = [
    'KodGezgini ',
    'kodgezgini',
    'SiberMarti',
    ' sibermarti '
]

def normalize_alias(value):
    return value.strip().lower()

normalized = [normalize_alias(item) for item in aliases]
counts = Counter(normalized)

for alias, total in counts.items():
    print(f'{alias}: {total} kayıt')
```

Bu işlem yalnızca aday eşleşmeler üretir. Aynı kullanıcı adını kullanan kişilerin otomatik olarak aynı kişi kabul edilmesi, OSINT çalışmalarındaki en yaygın hatalardan biridir.

## Etik kontrol listesi

- Araştırmanın meşru ve belgelenebilir bir amacı olmalı.
- Yalnızca gerekli veriler toplanmalı; özel hayata müdahale edilmemeli.
- Kimlik bilgileri, parolalar veya sızdırılmış kişisel kayıtlar saklanmamalı ve paylaşılmamalı.
- Bulgular en az iki bağımsız kaynakla doğrulanmalı.
- Raporlarda kesinlik derecesi, tarih ve kaynak açıkça belirtilmeli.

OSINT, dijital dedektiflik kadar metodoloji ve sorumluluk işidir. En değerli analist en fazla veriyi toplayan değil, hangi verinin güvenilir olduğunu açıklayabilen ve nerede durması gerektiğini bilen kişidir.

![acik-kaynak-istihbarati-20](/img/acik-kaynak-istihbarati-20.svg)


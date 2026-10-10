---
layout: post
title: "Dijital Sözlük Kurmak: WordPress Glossary, MediaWiki ve DictPress Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - sözlük
  - wordpress
  - mediawiki
  - dictpress
  - veri-modelleme
  - arama
toc: true
image: /img/dijital-sozluk-kurmak-46.png
---

Bir sözlük sistemi dışarıdan yalnızca “kelime ve açıklama” ikilisi gibi görünür. Oysa eş anlamlılar, yönlendirmeler, kategoriler, kaynaklar, sürümler ve güçlü arama özellikleri devreye girdiğinde küçük çaplı bir bilgi mimarisine dönüşür. WordPress Glossary, MediaWiki ve DictPress bu probleme farklı yönlerden yaklaşır: biri içerik yönetimini, biri ortak üretimi, diğeri ise sözlük odaklı veri organizasyonunu öne çıkarır.


![dijital-sozluk-kurmak-46](/img/dijital-sozluk-kurmak-46.svg)

``

## Önce veri modelini anlayalım

En basit sözlük girdisini matematiksel olarak şöyle gösterebiliriz:

$$G = (T, D, C, R, M)$$

Burada $T$ terimi, $D$ tanımı, $C$ kategorileri, $R$ ilişkili girdileri ve $M$ kaynak, yazar, tarih gibi meta verileri temsil eder. Gerçek projelerde bir terimin birden fazla anlamı bulunabileceğinden ilişki çoğu zaman $T \rightarrow \{D_1, D_2, \ldots, D_n\}$ biçimindedir.

Arama başarısını ölçmek için de iki temel kavram kullanılır:

$$Precision = \frac{İlgili\ bulunan\ sonuçlar}{Bulunan\ tüm\ sonuçlar}$$

$$Recall = \frac{İlgili\ bulunan\ sonuçlar}{Sistemdeki\ tüm\ ilgili\ sonuçlar}$$

Yani kullanıcı doğru yazdığında sonuç göstermek yetmez; yazım hataları, çekim ekleri ve eş anlamlılar da düşünülmelidir.

## Üç yaklaşımın karşılaştırması

| Özellik | WordPress Glossary | MediaWiki | DictPress |
|---|---|---|---|
| Temel yaklaşım | CMS ve eklenti tabanlı | İş birliğine açık wiki | Sözlük odaklı yayınlama |
| Kurulum kolaylığı | Yüksek | Orta | Orta |
| Editör deneyimi | Blog yönetimine benzer | Wiki sözdizimi ağırlıklı | Girdi ve alan odaklı |
| Sürüm geçmişi | WordPress revizyonları | Çok güçlü ve ayrıntılı | Uygulamaya göre değişir |
| Tema esnekliği | Çok yüksek | Görünüm sistemiyle esnek | Daha sınırlı olabilir |
| Büyük topluluk katkısı | Ek geliştirme gerekir | Doğal kullanım senaryosu | Genellikle kontrollü editörlük |
| En uygun senaryo | Kurumsal terimler, SEO | Topluluk ansiklopedisi | Yapılandırılmış sözlük |

### WordPress Glossary

WordPress tabanlı çözümde terimler genellikle özel yazı türü, yani `custom post type`, olarak tutulur. Kategoriler için taxonomy, ek bilgiler için özel alanlar kullanılabilir. En büyük avantaj, yönetim panelinin tanıdık olması ve SEO, önbellek, kullanıcı rolü gibi ihtiyaçların eklentilerle çözülebilmesidir.

Aşağıdaki kod basit bir `terim` içerik türü oluşturur:

```php
add_action('init', function () {
    register_post_type('terim', [
        'label' => 'Terimler',
        'public' => true,
        'has_archive' => true,
        'rewrite' => ['slug' => 'sozluk'],
        'supports' => ['title', 'editor', 'revisions']
    ]);
});
```

Bu yapı her sözlük maddesine ayrı URL verir ve WordPress revizyon sistemini etkinleştirir. Ancak binlerce özel alanla karmaşık dilbilimsel ilişkiler kurulacaksa veri tabanı sorguları dikkatle tasarlanmalıdır.

### MediaWiki

MediaWiki, çok sayıda kullanıcının içerik üretmesi ve değişikliklerin şeffaf biçimde izlenmesi gereken projelerde parlar. Şablonlar sayesinde girdiler standartlaştırılabilir:

{% raw %}
```text
{{Terim
|ad=Özyineleme
|tanım=Bir işlevin kendisini çağırmasıdır.
|kategori=Programlama
|eşanlamlı=Rekürsiyon
}}
```
{% endraw %}

Bu şablon, editörlerin aynı alanları tutarlı biçimde doldurmasını sağlar. Tartışma sayfaları, değişiklik karşılaştırmaları ve geri alma mekanizması büyük avantajdır. Buna karşılık ziyaretçiye sade bir sözlük deneyimi sunmak için tema, şablon ve arama yapılandırması gerekebilir.

### DictPress

DictPress yaklaşımı, genel amaçlı sayfalardan çok madde, anlam, örnek ve çapraz başvuru ilişkilerine odaklanır. Bu nedenle iki dilli sözlükler veya dilbilimsel projeler için daha doğal bir model sunabilir. Dezavantajı, WordPress ve MediaWiki kadar geniş eklenti ekosistemine sahip olmayabilmesi ve seçilen sürüme göre bakım durumunun mutlaka incelenmesidir.

## Hangisini seçmeli?

Hızlı yayın, modern tema ve SEO istiyorsanız **WordPress Glossary**; açık katkı, güçlü geçmiş takibi ve topluluk yönetimi istiyorsanız **MediaWiki** daha uygundur. Anlam, köken, telaffuz ve çeviri gibi alanların birinci sınıf veri olarak saklanması gerekiyorsa **DictPress** değerlendirilebilir.

Son kararı yalnız özellik listesine göre vermeyin. Önce 50 örnek terim girin, arama senaryolarını deneyin ve dışa aktarma imkânını kontrol edin. Çünkü iyi bir sözlük yalnız kelimeleri saklamaz; kelimeler arasındaki görünmez köprüleri de korur.

---
layout: post
title: "Docusaurus, MkDocs ve GitBook Yerine Kullanabileceğiniz Dokümantasyon Araçları"
math: true
categories: 
  - Bilgi
tags: 
  - dokümantasyon
  - docusaurus
  - mkdocs
  - gitbook
  - vitepress
  - starlight
  - sphinx
toc: true
image: /img/docusaurus-mkdocs-ve-89.png
---

İyi bir dokümantasyon sitesi, kodun yanında verilen sıkıcı bir kullanım kılavuzu değil; geliştiricinin ürünle tanıştığı, hata çözdüğü ve bazen hayatı sorgulamadan önce son kez baktığı yerdir. Docusaurus, MkDocs ve GitBook popüler seçenekler olsa da her projenin teknoloji yığını, içerik modeli ve dağıtım beklentisi farklıdır. Neyse ki dokümantasyon dünyasında alternatif bol.

``

## Araç seçimindeki temel mantık

Dokümantasyon araçları genellikle Markdown dosyalarını alır, bir tema ve gezinme yapısıyla işleyerek statik HTML çıktısına dönüştürür. Böylece ortaya hızlı, sürümlenebilir ve CDN üzerinden kolayca yayımlanabilen bir site çıkar.

Doğru aracı seçerken yalnızca tasarıma bakmak yerine karar faktörlerine ağırlık vermek gerekir. Basit bir değerlendirme modeli şöyle kurulabilir:

$$
P = \sum_{i=1}^{n} w_i s_i
$$

Burada $P$ toplam puanı, $w_i$ kriterin önem ağırlığını, $s_i$ ise aracın o kriterde aldığı puanı temsil eder. Örneğin çok dilli içerik kritikse i18n kriterinin ağırlığı artırılmalıdır. Ekip yalnızca Python biliyorsa React tabanlı bir aracın puanı doğal olarak düşebilir.

| Araç | Altyapı | Güçlü yanı | Uygun senaryo |
|---|---|---|---|
| VitePress | Vue ve Vite | Hızlı geliştirme, sade yapı | Vue ekosistemi ve teknik bloglar |
| Starlight | Astro | Hazır dokümantasyon özellikleri | Modern ve performanslı siteler |
| Nextra | Next.js ve React | Uygulamayla güçlü entegrasyon | React tabanlı ürün ekipleri |
| Sphinx | Python | Gelişmiş referans üretimi | Python kütüphaneleri ve akademik projeler |
| Hugo | Go | Çok hızlı derleme | Binlerce sayfalık büyük siteler |
| Docsify | JavaScript | Derleme gerektirmeyen kurulum | Küçük ve hızlı prototipler |

![docusaurus-mkdocs-ve-89](/img/docusaurus-mkdocs-ve-89.svg)


## Öne çıkan alternatifler

### VitePress

VitePress, Vue ekibi tarafından geliştirilen hızlı ve minimal bir statik site üreticisidir. Markdown içinde Vue bileşenleri kullanılabilir. Yapılandırması Docusaurus’a göre daha hafiftir; ancak gelişmiş sürümleme veya kapsamlı eklenti ihtiyaçlarında ek geliştirme gerekebilir.

### Astro Starlight

Starlight, dokümantasyon için özel hazırlanmış bir Astro temasıdır. Arama, karanlık mod, erişilebilirlik, çoklu dil ve otomatik kenar çubuğu gibi özellikleri kutudan çıktığı anda sunar. React, Vue veya Svelte bileşenlerini aynı projede kullanabilmesi onu teknoloji bağımsız ekipler için çekici kılar.

Aşağıdaki yapılandırma site başlığını ve sosyal bağlantıyı tanımlar:

```javascript
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: 'Uzay Üssü Dokümantasyonu',
      social: { github: 'https://github.com/ornek/proje' }
    })
  ]
});
```

Bu dosya, Astro’nun derleme sürecine Starlight entegrasyonunu ekler. İçerikler daha sonra `src/content/docs` altında Markdown veya MDX olarak tutulur.

### Sphinx

Sphinx özellikle Python dünyasının ağır topudur. Kaynak koddan API referansı üretebilir, çapraz bağlantıları yönetebilir ve PDF gibi farklı çıktılar oluşturabilir. ReStructuredText geleneksel biçimidir; MyST eklentisi sayesinde Markdown da kullanılabilir. Görsel özelleştirme tarafı modern JavaScript araçları kadar eğlenceli olmayabilir, fakat teknik doğruluk konusunda oldukça güçlüdür.

### Nextra, Hugo ve Docsify

Nextra, mevcut bir Next.js uygulamasıyla dokümantasyonu aynı depoda yaşatmak isteyen ekipler için idealdir. Hugo, büyük içerik koleksiyonlarını şaşırtıcı hızda derler. Docsify ise Markdown dosyalarını tarayıcıda yorumlar; yani ayrı bir derleme adımı istemez. Bunun karşılığında SEO ve ilk yükleme performansı statik üretilmiş alternatiflerden daha zayıf olabilir.

## Hangisini seçmelisiniz?

React ekibiyseniz Nextra, Vue kullanıyorsanız VitePress, Python paketi geliştiriyorsanız Sphinx güçlü adaylardır. Teknoloji bağımsız ve kullanıma hazır bir deneyim için Starlight öne çıkar. Çok büyük içerik arşivlerinde Hugo, birkaç saatte çalışan bir iç dokümantasyon gerektiğinde ise Docsify değerlendirilebilir.

Son karardan önce arama, sürümleme, i18n, erişilebilirlik, eklenti desteği ve dağıtım maliyetini küçük bir prototiple test edin. Çünkü en iyi dokümantasyon aracı, en fazla özelliğe sahip olan değil; ekibin gerçekten güncel tutacağı araçtır.

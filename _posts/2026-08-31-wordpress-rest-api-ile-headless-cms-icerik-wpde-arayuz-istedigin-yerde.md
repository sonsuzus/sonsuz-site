---
layout: post
title: "WordPress REST API ile Headless CMS: İçerik WP’de, Arayüz İstediğin Yerde"
math: true
categories: 
  - Bilgi
tags: 
  - wordpress rest apı
  - headless cms
  - javascript
toc: true
---

WordPress denince akla çoğunlukla tema, eklenti ve klasik blog sayfaları gelir. Oysa WordPress’i yalnızca içerik üretim paneli olarak kullanıp ziyaretçiye görünen arayüzü React, Vue, Next.js, Nuxt, Flutter veya başka bir teknolojiyle geliştirmek mümkündür. Bu yaklaşımda WordPress mutfakta yemekleri hazırlar, REST API garsonluk yapar, seçtiğin arayüz ise sunumu üstlenir.

``

## Headless WordPress nedir?

Klasik WordPress mimarisinde içerik yönetimi ve kullanıcı arayüzü aynı sistemin parçalarıdır. PHP tabanlı tema; veritabanından yazıları alır, HTML üretir ve tarayıcıya gönderir. Headless mimaride ise WordPress’in “baş”, yani görünüm katmanı ayrılır. Yönetim paneli, veritabanı ve içerik araçları korunurken ön yüz bağımsız bir uygulama olur.

WordPress REST API, kaynaklara HTTP üzerinden erişilmesini sağlar. Temel yazı adresi şöyledir:

```text
https://site.com/wp-json/wp/v2/posts
```

Bu uç nokta JSON biçiminde yazıları döndürür. Sayfalar için `/pages`, kategoriler için `/categories`, kullanıcılar için `/users` kullanılır. Belirli bir yazıya erişmek için sona kimlik numarası eklenebilir: `/posts/42`.

| Özellik | Klasik WordPress | Headless WordPress |
|---|---|---|
| Arayüz | PHP teması | React, Vue, mobil uygulama vb. |
| Veri aktarımı | Sunucuda HTML | JSON tabanlı API |
| Dağıtım | Genellikle tek sunucu | Ön yüz ve WP ayrı olabilir |
| Esneklik | Tema yapısıyla sınırlı | Çoklu platform desteği |
| Bakım | Daha basit | Daha fazla mimari sorumluluk |

## React ile yazıları çekmek

Aşağıdaki bileşen WordPress API’sinden son yazıları getirir. `fetch`, HTTP isteğini gerçekleştirir; `useEffect` bileşen açıldığında isteği başlatır; `useState` ise gelen veriyi arayüzde saklar.

```jsx
import { useEffect, useState } from "react";

export default function Posts() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch("https://site.com/wp-json/wp/v2/posts?per_page=5")
      .then((response) => {
        if (!response.ok) throw new Error("Yazılar alınamadı");
        return response.json();
      })
      .then(setPosts)
      .catch(console.error);
  }, []);

  return (
    <section>
      {posts.map((post) => (
        <article key={post.id}>
          <h2 dangerouslySetInnerHTML={{ __html: post.title.rendered }} />
        </article>
      ))}
    </section>
  );
}
```

WordPress başlık ve içerikleri işlenmiş HTML olarak döndürebilir. `dangerouslySetInnerHTML` bu HTML’yi görüntüler; ancak güvenilmeyen kaynaklardan gelen içeriklerde XSS riski oluşturur. İçeriği temizlemek için DOMPurify gibi bir araç kullanmak iyi fikirdir.

## Performansın küçük matematiği

Bir sayfanın yaklaşık yanıt süresini şöyle düşünebiliriz:

$$T_{toplam} = T_{arayüz} + T_{API} + T_{veritabanı} + T_{ağ}$$

Headless olmak sistemi otomatik olarak hızlandırmaz. API her ziyarette WordPress’e giderse gecikme artabilir. Next.js gibi araçlarla statik üretim, artımlı yenileme ve önbellekleme uygulanabilir. Örneğin önbellek isabet oranı $h$ ise ortalama erişim maliyeti yaklaşık olarak şöyledir:

$$T_{ortalama} = hT_{cache} + (1-h)T_{API}$$

$h$ yükseldikçe WordPress’in omuzlarındaki yük azalır; sunucu da kahvesini daha sakin içer.

## Kimlik doğrulama ve güvenlik

Herkese açık yazıları okumak için çoğunlukla kimlik doğrulama gerekmez. Taslak görüntüleme, içerik oluşturma veya güncelleme işlemlerinde ise Application Passwords, JWT ya da OAuth kullanılabilir. API anahtarları tarayıcı koduna gömülmemeli; hassas işlemler güvenilir bir sunucu katmanından geçirilmelidir.

Ayrıca CORS ayarları yalnızca izin verilen alanları kapsamalı, kullanılmayan API uçları sınırlandırılmalı ve WordPress düzenli güncellenmelidir. Headless yapı, güvenliği ortadan kaldırmaz; yalnızca saldırı yüzeyinin şeklini değiştirir.

## Ne zaman tercih edilmeli?

Aynı içeriği web sitesi, mobil uygulama, akıllı ekran ve kurumsal portal gibi birçok kanala dağıtacaksan headless WordPress güçlü bir seçenektir. Özel kullanıcı deneyimleri ve modern ön yüz araçları için de özgürlük sağlar. Ancak basit bir tanıtım sitesi için ek dağıtım, önizleme, SEO ve önbellek süreçleri gereksiz karmaşıklık yaratabilir.

Kısacası WordPress’i tema motorundan ibaret görmemek gerekir. REST API sayesinde o, içerik ekibinin tanıdığı paneli koruyan ve farklı uygulamalara düzenli JSON servis eden yetenekli bir veri merkezine dönüşebilir.

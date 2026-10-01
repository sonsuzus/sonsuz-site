---
layout: post
title: "Web Components ile Çerçevesiz Geliştirme Dönemi"
math: true
categories: 
  - Bilgi
tags: 
  - web-components
  - custom-elements
  - shadow-dom
  - javascript
  - frontend
  - framework-agnostic
toc: true
image: /img/web-components-ile-85.png
---

Modern web geliştirme denince akla hemen React, Angular veya Vue geliyor. Oysa tarayıcılarımız uzun süredir kendi bileşen sistemini taşıyor: **Web Components**. Custom Elements, Shadow DOM ve HTML Templates standartlarını bir araya getirerek herhangi bir çerçeveye bağlanmadan yeniden kullanılabilir arayüzler oluşturabiliriz. Üstelik ortaya çıkan bileşenler düz HTML’de, React projesinde veya yıllar sonra çıkacak başka bir teknolojide çalışabilir.

![web-components-ile-85](/img/web-components-ile-85.svg)

``

## Web Components aslında nedir?

Web Components tek bir teknoloji değil, birlikte çalışan tarayıcı standartları ailesidir:

- **Custom Elements:** Kendimize ait HTML etiketleri tanımlamamızı sağlar.
- **Shadow DOM:** Bileşenin HTML ve CSS yapısını dış dünyadan izole eder.
- **HTML Templates:** Hemen ekrana basılmayan, gerektiğinde çoğaltılabilen şablonlar sunar.
- **ES Modules:** Bileşenleri dosyalara ayırıp içe aktarmayı kolaylaştırır.

Bir bileşeni kabaca şu fonksiyonla düşünebiliriz:

$$B = f(A, S, E)$$

Burada $A$ özellikleri (attributes), $S$ iç durumu (state), $E$ olayları (events), $B$ ise üretilen kullanıcı arayüzünü temsil eder. Framework’ler bu ilişkiyi kendi kurallarıyla yönetirken Web Components doğrudan platformun araçlarını kullanır.

| Özellik | Web Components | React/Angular yaklaşımı |
|---|---|---|
| Çalışma ortamı | Doğrudan tarayıcı | Kütüphane veya framework |
| Stil izolasyonu | Shadow DOM ile yerleşik | Ek araçlara ihtiyaç duyabilir |
| Yeniden kullanım | Teknolojiden bağımsız | Ekosisteme bağlı olabilir |
| Başlangıç maliyeti | Düşük | Paket ve yapılandırma gerekebilir |
| Durum yönetimi | Geliştirici tasarlar | Hazır desenler sunulur |

## İlk özel elementimizi oluşturalım

Aşağıdaki bileşen, `user-card` isimli yeni bir HTML etiketi tanımlar. `name` özelliğini okuyarak kartın içeriğini üretir ve Shadow DOM sayesinde stillerini sayfanın geri kalanından korur.

```javascript
class UserCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  connectedCallback() {
    const name = this.getAttribute("name") ?? "Misafir";

    this.shadowRoot.innerHTML = `
      <style>
        article {
          padding: 1rem;
          border: 2px solid #6750a4;
          border-radius: 12px;
          font-family: system-ui;
        }
        strong { color: #6750a4; }
      </style>
      <article>
        Merhaba, <strong>${name}</strong>!
        <button>Selam ver</button>
      </article>
    `;

    this.shadowRoot.querySelector("button").addEventListener("click", () => {
      this.dispatchEvent(new CustomEvent("greet", {
        detail: { name },
        bubbles: true
      }));
    });
  }
}

customElements.define("user-card", UserCard);
```

Tanımlanan bileşen artık normal bir HTML etiketi gibi kullanılabilir:

```html
<user-card name="Ada"></user-card>

<script type="module" src="./user-card.js"></script>
```

Özel element adında kısa çizgi bulunması zorunludur. Bu kural, gelecekte eklenecek yerleşik HTML etiketleriyle isim çakışmasını önler. `connectedCallback`, element belgeye eklendiğinde çalışır; olay dinleyicileri kurmak veya ilk görünümü oluşturmak için uygundur.

## Shadow DOM neden önemli?

Büyük projelerde `.button` gibi genel CSS sınıfları kolayca birbirini bozar. Shadow DOM, bileşene ayrı bir DOM sınırı verir. Dışarıdaki `button { color: red; }` kuralı içerideki düğmeye sızmaz; içerideki stiller de sayfayı etkilemez.

Bu izolasyon mutlak bir duvar değildir. CSS özel özellikleri kullanılarak kontrollü kişiselleştirme yapılabilir:

```css
/* Sayfayı kullanan uygulama */
user-card {
  --card-accent: #e91e63;
}
```

Bileşen içinde `color: var(--card-accent, #6750a4);` kullanılması, güvenli fakat özelleştirilebilir bir API oluşturur.

## Her projede framework’ü bırakmalı mıyız?

Hayır; Web Components bir “framework katili” değil, sağlam bir paylaşım standardıdır. Karmaşık yönlendirme, merkezi durum yönetimi ve sunucu tarafı render gibi ihtiyaçlarda framework’ler ciddi hız kazandırır. Buna karşılık tasarım sistemleri, kurumlar arası paylaşılan widget’lar, mikro frontend’ler ve uzun ömürlü bileşen kütüphaneleri için Web Components son derece güçlüdür.

En iyi yaklaşım araç fanatikliği değil, doğru soyutlamadır. Küçük ve bağımsız bir bileşen için tarayıcı zaten ihtiyacımız olan sahneyi, oyuncuları ve ışıkları sağlıyorsa bütün tiyatro binasını yeniden kurmaya gerek yoktur.

---
layout: post
title: "Tarayıcıda Görsel Düzenleme: Photopea, Pintura ve TUI Image Editor Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - photopea
  - pintura
  - tui-image-editor
  - görsel-düzenleme
  - javascript
  - web-geliştirme
toc: true
image: /img/tarayicida-gorsel-duzenleme-74.png
---

![tarayicida-gorsel-duzenleme-74](/img/tarayicida-gorsel-duzenleme-74.svg)


Bir görseli kırpmak, yeniden boyutlandırmak veya üzerine yazı eklemek için kullanıcıya masaüstü programı kurdurmak artık şart değil. Photopea doğrudan kullanılabilen kapsamlı bir editör sunarken Pintura ve TUI Image Editor, geliştiricilerin kendi uygulamalarına düzenleme yetenekleri eklemesini sağlar. Üçü de tarayıcıda çalışır; ancak hedefleri, lisansları ve entegrasyon biçimleri oldukça farklıdır.

``

## Önce temel mantık: Tarayıcı görseli nasıl işler?

Web tabanlı editörler, kullanıcının seçtiği resmi çoğunlukla `Canvas`, WebGL veya bunları soyutlayan JavaScript kütüphaneleri aracılığıyla işler. Bir pikselin rengi genellikle kırmızı, yeşil, mavi ve alfa bileşenleriyle temsil edilir:

$$P = (R, G, B, A)$$

Burada her renk kanalı çoğunlukla $0$ ile $255$ arasındadır. Örneğin parlaklık artırılırken basitleştirilmiş biçimde $R' = R + k$, $G' = G + k$ ve $B' = B + k$ işlemleri uygulanabilir. Kırpma ise pikselleri değiştirmekten çok, görüntünün belirli koordinatlar arasındaki bölümünü seçmektir.

Tarayıcı tabanlı çalışmanın önemli avantajı, görselin her zaman sunucuya gönderilmek zorunda olmamasıdır. İşlem istemci tarafında gerçekleşirse daha hızlı geri bildirim alınır ve hassas dosyalar cihazdan çıkmaz. Yine de kullanılan servisin yükleme ve gizlilik politikasını ayrıca incelemek gerekir.

## Üç aracın kısa karşılaştırması

| Araç | Temel hedef | En güçlü yanı | Dikkat edilmesi gereken |
|---|---|---|---|
| Photopea | Son kullanıcılar | PSD desteği ve katmanlı düzenleme | Uygulamaya yerel bileşen gibi eklenmez |
| Pintura | Web ve mobil geliştiriciler | Modern arayüz, güçlü kırpma ve açıklama araçları | Ticari lisans gerektirir |
| TUI Image Editor | JavaScript projeleri | Açık kaynaklı ve özelleştirilebilir yapı | Proje bakımı ve modern entegrasyon ihtiyaçları kontrol edilmelidir |

## Photopea: Tarayıcıdaki dijital stüdyo

Photopea, Photoshop benzeri arayüzüyle PSD, XCF, Sketch, SVG ve yaygın resim biçimlerini açabilir. Katmanlar, maskeler, seçim araçları ve filtreler sunduğundan hızlı tasarım işleri için oldukça pratiktir. Kurulum gerektirmemesi, ortak veya düşük yetkili bilgisayarlarda büyük avantajdır.

Bununla birlikte Photopea daha çok hazır bir uygulamadır. Kendi e-ticaret sitenizde kullanıcıların yalnızca ürün fotoğrafını kırpmasını istiyorsanız tam teşekküllü editör, çay kaşığı ararken mutfak robotu çıkarmaya benzeyebilir.

## Pintura: Ürüne gömülen modern editör

Pintura; kırpma, döndürme, filtre, açıklama, yeniden boyutlandırma ve dosya çıktısı özelliklerini uygulamanıza eklemek için tasarlanmıştır. React, Vue ve Angular gibi ekosistemlerle kullanılabilir. Aşağıdaki örnek, bir dosya alanını editöre bağlayan temel yaklaşımı gösterir:

```javascript
import { openDefaultEditor } from '@pqina/pintura';

const input = document.querySelector('#image');

input.addEventListener('change', () => {
  const editor = openDefaultEditor({
    src: input.files[0]
  });

  editor.on('process', ({ dest }) => {
    document.querySelector('#preview').src = URL.createObjectURL(dest);
  });
});
```

Kod, seçilen dosyayı Pintura içinde açar ve düzenlenen çıktıyı önizleme alanına yerleştirir. Üretimde dosya türü, maksimum boyut ve yükleme hataları da doğrulanmalıdır.

## TUI Image Editor: Açık kaynaklı alternatif

TUI Image Editor; kırpma, çevirme, döndürme, çizim, şekil ve metin ekleme gibi temel özellikler sunar. Hazır arayüzü kullanılabilir veya API üzerinden özel kontroller geliştirilebilir:

```javascript
const editor = new tui.ImageEditor('#editor', {
  cssMaxWidth: 900,
  cssMaxHeight: 600,
  usageStatistics: false
});

editor.loadImageFromURL('/images/sample.jpg', 'Sample');
```

Bu kod editörü belirtilen kapsayıcıda oluşturur ve örnek resmi yükler. Açık kaynak avantajlıdır; fakat bağımlılık uyumluluğunu, güvenlik durumunu ve güncel bakım seviyesini proje başlamadan değerlendirmek akıllıca olur.

## Hangisini seçmelisiniz?

Tek seferlik veya profesyonel katmanlı düzenleme için **Photopea**, şık ve desteklenen bir ürün bileşeni için **Pintura**, kaynak koduna erişmek ve özelleştirme yapmak için **TUI Image Editor** öne çıkar. Kısacası seçim yalnızca özellik sayısına değil; lisans maliyeti, entegrasyon süresi, gizlilik ve bakım yüküne dayanmalıdır. En iyi editör, en çok düğmesi olan değil, kullanıcının işini en az sürtünmeyle bitirendir.

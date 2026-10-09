---
layout: post
title: "Online Beyaz Tahta Seçimi: Excalidraw, tldraw ve WBO Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - excalidraw
  - tldraw
  - wbo
  - beyaz tahta
  - iş birliği
  - açık kaynak
toc: true
image: /img/online-beyaz-tahta-58.png
---

Uzaktan toplantıda biri “Şunu bir çizerek anlatsak?” dediği anda çevrim içi beyaz tahtalar sahneye çıkar. Excalidraw, tldraw ve WBO; fikirleri kutulara, oklara ve bol miktarda dijital karalamaya dönüştüren üç güçlü seçenek. Benzer görünseler de çizim tarzı, geliştirilebilirlik ve kendi sunucunda çalıştırma bakımından farklı ihtiyaçlara hitap ederler.
``

## Dijital beyaz tahtanın arkasındaki mantık

Bir çevrim içi beyaz tahta, yalnızca tarayıcı üzerinde çalışan bir çizim uygulaması değildir. Her şekil; tür, konum, boyut, renk ve oluşturucu gibi özelliklerden meydana gelen bir veri nesnesidir. Örneğin bir dikdörtgen kabaca şöyle temsil edilebilir:

```json
{
  "type": "rectangle",
  "x": 120,
  "y": 80,
  "width": 240,
  "height": 100,
  "color": "#4f46e5"
}
```

Sonsuz tuvalde gördüğümüz ekran, dünya koordinatlarının kamera dönüşümüyle görüntülenmesidir. Yakınlaştırma oranı $s$, kamera konumu $(c_x,c_y)$ ve nesne konumu $(x,y)$ ise ekrandaki konum basitçe

$$X = (x-c_x)s, \quad Y = (y-c_y)s$$

şeklinde hesaplanabilir. Bu sayede kullanıcı yakınlaştırdığında nesneler gerçekten büyütülmez; yalnızca farklı ölçekte çizilir.

Eş zamanlı çalışmada asıl mesele, birden fazla kullanıcının değişikliklerini uzlaştırmaktır. Basit sistemler olayları WebSocket üzerinden sırayla dağıtır. Daha gelişmiş uygulamalar ise çakışmaları azaltmak için CRDT benzeri veri yapılarını kullanabilir. Amaç, ağ gecikmesi yaşansa bile tüm katılımcıların sonunda aynı tahta durumuna ulaşmasıdır.

## Üç araç, üç farklı karakter

| Özellik | Excalidraw | tldraw | WBO |
|---|---|---|---|
| Görsel tarz | El çizimi, samimi | Temiz ve modern | Sade, klasik tahta |
| Temel güç | Hızlı diyagram | Uygulama geliştirme ve SDK | Kolay ortak çizim |
| Açık kaynak | Evet | Evet | Evet |
| Kendi sunucunda kullanım | Mümkün | Geliştirici kurulumu odaklı | Güçlü seçenek |
| İdeal kullanıcı | Ekipler, öğrenciler | Ürün geliştiricileri | Topluluklar, sınıflar |

### Excalidraw: Diyagramların eskiz defteri

Excalidraw’ın elde çizilmiş görünümü, kusursuz tasarım baskısını ortadan kaldırır. Akış şemaları, sistem mimarileri ve ders notları birkaç dakika içinde hazırlanabilir. Sahne dosyalarının dışa aktarılması, bağlantıyla paylaşım ve ortak çalışma özellikleri günlük kullanımda oldukça pratiktir.

Bu araç özellikle “önce fikri anlatalım, pikselleri sonra düzeltiriz” yaklaşımına uygundur. Resmî uygulamadaki özelliklerle açık kaynak kodunu kendi sunucunda çalıştırdığında elde edeceğin özelliklerin birebir aynı olmayabileceğini ise hesaba katmalısın.

### tldraw: Beyaz tahtadan uygulama platformuna

tldraw, başarılı bir çizim aracının yanında geliştiricilere sunulan SDK ile öne çıkar. Özel şekiller, araçlar ve etkileşimler tanımlayarak kendi görsel düzenleyicini geliştirebilirsin. Örneğin bir proje yönetim uygulamasında kartları serbest bir tuval üzerinde göstermek için güçlü bir temel sağlar.

Bu esneklik beraberinde daha fazla geliştirme kararı getirir. Yalnızca toplantı sırasında ok çizmek isteyen biri için bazı avantajları görünmez kalabilir; özel ürün geliştiren ekip içinse tam tersine belirleyici olabilir.

### WBO: Sadelik ve kendi sunucunun kontrolü

WBO, hızlıca bir tahta açıp bağlantıyı paylaşma fikrine odaklanır. Arayüzü diğer ikisi kadar gösterişli değildir; ancak açık kaynaklı ve kendi sunucunda barındırılabilir olması eğitim kurumları, küçük ekipler ve veri kontrolünü önemseyen topluluklar için değerlidir.

Örneğin bir istemcinin çizim olayını göndermesi kavramsal olarak şöyledir:

```javascript
const socket = new WebSocket("wss://ornek.com/board");

socket.addEventListener("open", () => {
  socket.send(JSON.stringify({
    action: "draw",
    from: { x: 20, y: 30 },
    to: { x: 80, y: 95 }
  }));
});
```

Kod, çizginin başlangıç ve bitiş koordinatlarını sunucuya yollar. Sunucu da bu olayı diğer kullanıcılara dağıtarak ortak görünümü günceller.

## Hangisini seçmeli?

Hızlı ve hoş diyagramlar için **Excalidraw**, özel bir tuval tabanlı ürün geliştirmek için **tldraw**, sade kullanım ve sunucu kontrolü için **WBO** daha uygun başlangıç noktalarıdır. Kararı yalnızca araç sayısına göre değil; veri sahipliği, entegrasyon, eş zamanlı kullanıcı sayısı ve bakım maliyetine göre vermelisin. Sonuçta en iyi beyaz tahta, toplantıyı uzatan değil fikri görünür kılan tahtadır.

![online-beyaz-tahta-58](/img/online-beyaz-tahta-58.svg)


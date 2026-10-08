---
layout: post
title: "Tarayıcıda Kod Yazmak: code-server, Eclipse Che ve Theia Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - online ide
  - code-server
  - eclipse che
  - theia
  - bulut geliştirme
  - devops
toc: true
image: /img/tarayicida-kod-yazmak-75.png
---

![tarayicida-kod-yazmak-75](/img/tarayicida-kod-yazmak-75.svg)


Bir projeyi çalıştırmak için bilgisayara onlarca araç kurduğunuz, sürüm uyuşmazlıklarıyla boğuştuğunuz ve sonunda “Bende çalışıyor!” cümlesine sığındığınız günleri düşünün. Online kod editörleri, geliştirme ortamını uzak bir sunucuda çalıştırıp tarayıcı üzerinden erişilebilir hâle getirerek bu macerayı sakinleştirir. Bu dünyanın öne çıkan üç oyuncusu code-server, Eclipse Che ve Theia olsa da aynı ihtiyaca oldukça farklı açılardan yaklaşırlar.
``

## Online geliştirme ortamının mantığı

Geleneksel modelde editör, derleyici, bağımlılıklar ve kaynak kod geliştiricinin bilgisayarındadır. Tarayıcı tabanlı modelde ise kullanıcı arayüzü istemcide görüntülenirken terminal, dil sunucusu, dosya sistemi ve uygulama süreçleri uzak makinede çalışır.

Bir tuşa basılması ile sonucun görünmesi arasındaki gecikmeyi kabaca şöyle modelleyebiliriz:

$$T_{toplam} = T_{ağ} + T_{işleme} + T_{çizim}$$

Burada ağ gecikmesi yükseldikçe editörün akıcılığı azalabilir. Buna karşılık güçlü bir sunucu; derleme, indeksleme ve test işlemlerini zayıf bir dizüstü bilgisayardan çok daha hızlı tamamlayabilir. Yani hesaplama gücü kazanılırken ağ bağlantısına bağımlılık artar.

## Üç aracın karakteri

**code-server**, Visual Studio Code deneyimini uzak bir makinede çalıştırıp tarayıcıya taşır. Tek geliştirici, kişisel sunucu veya hızlı ekip kurulumu için pratiktir. Mevcut VS Code alışkanlıklarını büyük ölçüde koruması, öğrenme eşiğini düşürür.

**Eclipse Che**, Kubernetes üzerinde standartlaştırılmış çalışma alanları sağlamaya odaklanan daha kapsamlı bir platformdur. Her geliştirici için izole ortamlar üretir; ekip politikaları, merkezi yapılandırma ve kurumsal ölçek burada başrole çıkar.

**Eclipse Theia** ise yalnızca hazır bir editör değil, özelleştirilebilir bulut ve masaüstü IDE’leri geliştirmek için kullanılan bir platformdur. Ürününüze kendi markanızla özel bir IDE gömmek istiyorsanız Theia güçlü bir temel sunar.

| Özellik | code-server | Eclipse Che | Theia |
|---|---|---|---|
| Temel yaklaşım | Tarayıcıda VS Code deneyimi | Kubernetes tabanlı çalışma alanı platformu | Özelleştirilebilir IDE platformu |
| Kurulum zorluğu | Düşük | Yüksek | Orta |
| Hedef kullanıcı | Bireysel geliştirici ve küçük ekip | Büyük ekip ve kurum | IDE ürünü geliştiren ekip |
| Özelleştirme | Eklentiler ve ayarlar | Ortam şablonları ve politikalar | Kaynak kod seviyesinde kapsamlı |
| Altyapı ihtiyacı | Tek sunucu yeterli olabilir | Genellikle Kubernetes gerekir | Kullanım senaryosuna bağlıdır |

## code-server ile hızlı başlangıç

Docker kullanarak birkaç komutla kişisel bir geliştirme ortamı oluşturabiliriz:

```bash
mkdir -p "$HOME/code-server/config" "$HOME/projects"

docker run -d \
  --name web-ide \
  -p 127.0.0.1:8080:8080 \
  -v "$HOME/code-server/config:/home/coder/.config" \
  -v "$HOME/projects:/home/coder/project" \
  codercom/code-server:latest
```

Bu komut, yapılandırma ve proje klasörlerini kalıcı depolamaya bağlar. Portun yalnızca `127.0.0.1` adresinde açılması bilinçli bir güvenlik önlemidir. Dış erişim için doğrudan portu internete saçmak yerine HTTPS sağlayan Nginx, Caddy veya güvenli bir VPN kullanılmalıdır.

## Hangisini seçmelisiniz?

Kararı sezgilere bırakmak yerine basit bir ağırlıklı puan modeli kullanılabilir:

$$P = 0.35K + 0.25Ö + 0.20Y + 0.20B$$

Burada $K$ kurulum kolaylığını, $Ö$ ölçeklenebilirliği, $Y$ özelleştirme yeteneğini ve $B$ bakım kolaylığını temsil eder. Katsayıları kendi önceliklerinize göre değiştirebilirsiniz. Kişisel kullanımda kurulum kolaylığına, yüzlerce geliştiricili bir şirkette ise ölçeklenebilirliğe daha yüksek ağırlık vermek mantıklıdır.

Hızlıca tarayıcıdan VS Code kullanmak istiyorsanız **code-server**, Kubernetes üzerinde tutarlı ve yönetilebilir ortamlar arıyorsanız **Eclipse Che**, kendi IDE ürününüzü şekillendirmek istiyorsanız **Theia** daha uygun seçimdir. Üçü de “bilgisayarımda çalışıyor” sorununu azaltır; fakat biri pratik bir araç kutusu, biri geliştirme fabrikası, diğeri ise kendi araç kutunuzu üretmenizi sağlayan atölyedir.

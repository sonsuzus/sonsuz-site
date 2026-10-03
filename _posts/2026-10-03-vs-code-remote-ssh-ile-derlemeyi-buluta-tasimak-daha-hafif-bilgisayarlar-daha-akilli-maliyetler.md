---
layout: post
title: "VS Code Remote-SSH ile Derlemeyi Buluta Taşımak: Daha Hafif Bilgisayarlar, Daha Akıllı Maliyetler"
math: true
categories: 
  - Bilgi
tags: 
  - vscode
  - remote-ssh
  - bulut
  - devops
  - uzak geliştirme
  - sunucu maliyeti
toc: true
image: /img/vs-code-remote-78.png
---

Modern bir projeyi ince ve sessiz bir dizüstü bilgisayarda geliştirirken yüzlerce paketi derlemek, Docker imajı oluşturmak veya devasa bir test paketini çalıştırmak bilgisayarı küçük bir jet motoruna çevirebilir. VS Code Remote-SSH, kod düzenleme deneyimini yerelde tutarken ağır hesaplama yükünü uzak bir Linux sunucusuna taşıyarak bu tabloyu değiştiriyor. Ancak bu yaklaşım yalnızca performans değil; donanım yatırımı, bulut faturası ve ekip verimliliği arasında yeni bir maliyet dengesi de oluşturuyor.
``
## Remote-SSH gerçekte nasıl çalışır?

Remote-SSH, klasik uzak masaüstünden farklıdır. Ekran görüntüsünü ağ üzerinden taşımak yerine VS Code arayüzü yerel bilgisayarda çalışır. SSH bağlantısı kurulduğunda uzak makineye küçük bir **VS Code Server** bileşeni yüklenir. Dosya sistemi işlemleri, terminal komutları, dil sunucuları, hata ayıklayıcılar ve çoğu eklenti bu sunucuda çalışır.

Başka bir deyişle klavye ve ekran yerelde, kas gücü uzaktadır. Rust derleyicisi, C++ araç zinciri veya Node.js bağımlılıkları geliştiricinin bilgisayarına kurulmak zorunda değildir.

| İşlem | Yerel geliştirme | Remote-SSH |
|---|---|---|
| Kod düzenleme arayüzü | Yerel | Yerel |
| Derleme ve test | Yerel CPU/RAM | Uzak CPU/RAM |
| Proje dosyaları | Yerel disk | Sunucu diski |
| Araç zinciri kurulumu | Her bilgisayarda | Merkezi ortamda |
| Ağ bağımlılığı | Düşük | Orta veya yüksek |

## Maliyet denklemi

Güçlü geliştirici bilgisayarları satın almak tek seferlik görünse de yükseltme, bakım ve kullanılmayan kapasite maliyetleri vardır. Basitleştirilmiş toplam sahip olma maliyetini şöyle düşünebiliriz:

$$TCO = D + B + E + K$$

Burada $D$ donanım, $B$ bakım, $E$ enerji ve $K$ geliştiricinin bekleme maliyetidir. Uzak geliştirmede ise yaklaşık maliyet şöyledir:

$$C_{bulut} = s \times t + depolama + trafik$$

$s$ saatlik sunucu fiyatını, $t$ açık kalma süresini temsil eder. Kritik nokta, sunucunun yalnızca ihtiyaç olduğunda çalıştırılmasıdır. Sekiz çekirdekli bir makineyi ay boyunca açık unutmak, güçlü bir dizüstü bilgisayardan daha pahalı olabilir. Otomatik kapatma ve zamanlanmış ölçeklendirme bu nedenle lüks değil, bütçe emniyet kemeridir.

| Senaryo | Ekonomik yaklaşım |
|---|---|
| Sürekli yoğun derleme | Ayrılmış veya rezerve sunucu |
| Günde birkaç kısa derleme | İstek üzerine bulut örneği |
| Küçük proje | Yerel geliştirme |
| Geçici yüksek kaynak ihtiyacı | Otomatik kapanan güçlü örnek |

## VS Code ile bağlantı

Önce SSH anahtarı oluşturulur ve açık anahtar sunucuya eklenir:

```bash
ssh-keygen -t ed25519 -C "developer@example.com"
ssh-copy-id developer@build.example.com
```

Ardından `~/.ssh/config` dosyasında okunabilir bir bağlantı tanımlanabilir:

```sshconfig
Host build-server
    HostName build.example.com
    User developer
    IdentityFile ~/.ssh/id_ed25519
```

VS Code içindeki **Remote-SSH: Connect to Host** komutuyla `build-server` seçildiğinde uzak klasör doğrudan IDE içinde açılır. Entegre terminalde çalıştırılan aşağıdaki komut artık yerel işlemciyi değil, sunucuyu terletir:

```bash
npm ci
npm run build
npm test
```

## Dev bulut ortamlarıyla doğal entegrasyon

Remote-SSH yalnızca elle hazırlanmış sanal makinelerle sınırlı değildir. AWS EC2, Azure VM, Google Compute Engine veya şirket içi Kubernetes tabanlı geliştirme ortamları aynı modele bağlanabilir. Dev Containers kullanıldığında derleyici sürümleri ve bağımlılıklar bir container tanımında sabitlenir. Böylece “bende çalışıyor” cümlesi doğal yaşam alanını kaybeder.

Her geliştirici için izole ortam oluşturmak güvenliği ve tekrarlanabilirliği artırır. Buna karşılık SSH anahtar yönetimi, güvenlik duvarı kuralları, yedekleme ve boşta kalan sunucuların kapatılması gerekir. Gecikmesi yüksek bağlantılarda dosya arama ve eklenti davranışları da yavaşlayabilir.

Sonuç olarak Remote-SSH, pahalı bilgisayarları sihirli biçimde bedavaya dönüştürmez; hesaplama kapasitesini doğru yerde ve doğru zamanda satın almayı sağlar. İyi otomasyonla geliştirici makinesi hafifler, ortamlar standartlaşır ve derleme süreleri kısalır. Kötü yönetimdeyse bulut faturası sessizce derlenir—üstelik bu derleme hiçbir zaman hata vermez.

![vs-code-remote-78](/img/vs-code-remote-78.svg)


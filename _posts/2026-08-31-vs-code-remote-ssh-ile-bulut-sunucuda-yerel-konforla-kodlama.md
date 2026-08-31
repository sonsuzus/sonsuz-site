---
layout: post
title: "VS Code Remote-SSH ile Bulut Sunucuda Yerel Konforla Kodlama"
math: true
categories: 
  - Program
tags: 
  - vs code
  - remote ssh
  - bulut geliştirme
toc: true
---

Kod bulut sunucuda, editör dizüstü bilgisayarında olabilir mi? VS Code Remote-SSH tam olarak bu sihri gerçekleştirir. Proje dosyalarını indirip yeniden yüklemek yerine SSH üzerinden sunucuya bağlanır; dosya gezgininden terminale, Git işlemlerinden hata ayıklamaya kadar geliştirme ortamını yerel VS Code penceresinden yönetmeni sağlar. Böylece “Sunucuda çalışan kod neden bilgisayarımda çalışmıyor?” bilmecesi de büyük ölçüde tarihe karışır.

``

## Remote-SSH nasıl çalışır?

Klasik yöntemde dosyalar SFTP ile bilgisayara indirilir, düzenlenir ve tekrar sunucuya gönderilir. Remote-SSH ise uzak makineye küçük bir **VS Code Server** bileşeni kurar. Kullanıcı arayüzü yerelde çalışırken dosya sistemi, terminal, eklentiler ve dil servisleri sunucuda çalışabilir.

Bağlantının algılanan gecikmesini kabaca şöyle düşünebiliriz:

$$T_{toplam} = T_{ağ} + T_{işlem} + T_{arayüz}$$

Arayüz yerel olduğu için $T_{arayüz}$ oldukça küçüktür. Ancak “gecikmesiz” deneyim, fiziksel olarak sıfır gecikme anlamına gelmez. Sunucu yakın bir bölgede bulunuyorsa, kararlı bir bağlantı ve düşük ping sayesinde düzenleme son derece akıcı hissedilir.

| Yöntem | Dosyaların konumu | Çalıştırma ortamı | Senkronizasyon |
|---|---|---|---|
| SFTP ile düzenleme | Yerel ve uzak | Genellikle uzak | Manuel |
| Ağ diski bağlama | Uzak | Değişken | Anlık, fakat kırılgan |
| Remote-SSH | Uzak | Uzak | Ek kopyalama gerekmez |
| Yerel geliştirme | Yerel | Yerel | Dağıtım sırasında gerekir |

## Kurulum ve ilk bağlantı

Öncelikle VS Code içindeki Extensions bölümünden **Remote - SSH** eklentisini kur. Ardından yerel terminalde bir SSH anahtarı oluştur:

```bash
ssh-keygen -t ed25519 -C "developer@example.com"
ssh-copy-id kullanici@sunucu-adresi
```

İlk komut güvenli bir anahtar çifti üretir. İkinci komut açık anahtarı sunucuya ekler; böylece her bağlantıda parola yazmak yerine anahtar tabanlı kimlik doğrulama kullanılabilir.

Bağlantıyı kolaylaştırmak için `~/.ssh/config` dosyasına bir sunucu tanımı ekle:

```sshconfig
Host proje-sunucum
    HostName 203.0.113.10
    User developer
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
```

Buradaki `Host`, VS Code içinde göreceğin kısa addır. `ServerAliveInterval`, uzun süre işlem yapılmadığında bağlantının sessizce kopmasını önlemeye yardımcı olur.

Şimdi Komut Paleti’ni `Ctrl+Shift+P` ile aç, **Remote-SSH: Connect to Host** komutunu seç ve `proje-sunucum` bağlantısına tıkla. Yeni pencerenin sol alt köşesinde SSH göstergesi belirdiğinde artık uzak sunucudasın. **Open Folder** ile örneğin `/var/www/uygulama` dizinini açabilirsin.

## Eklentiler ve terminal nerede çalışır?

Remote-SSH kullanırken bazı eklentiler yerelde, bazıları uzak sunucuda çalışır. Tema gibi görsel eklentiler yerelde kalırken Python, ESLint veya Docker gibi çalışma ortamına ihtiyaç duyan eklentiler sunucu tarafına kurulmalıdır.

```bash
cd /var/www/uygulama
npm install
npm run dev
```

Bu komutlar VS Code’un bütünleşik terminalinde görünse de gerçekte bulut sunucuda yürütülür. Dolayısıyla sunucunun Node.js sürümü, işletim sistemi ve çevre değişkenleri kullanılır. Uygulama `localhost:3000` üzerinde açılırsa VS Code’un **Ports** panelinden port yönlendirme yaparak tarayıcıdan erişebilirsin.

## Güvenlik ve performans ipuçları

Root kullanıcısıyla bağlanmak yerine sınırlı yetkili bir kullanıcı oluştur. SSH anahtarını parola ile koru, güvenlik duvarını etkinleştir ve mümkünse sunucu erişimini belirli IP adresleriyle sınırla. Özel anahtarını asla Git deposuna ekleme; o dosya dijital ev anahtarındır.

Daha akıcı kullanım için sunucuyu sana yakın bir bölgede seç, büyük klasörleri dosya izleme kapsamından çıkar ve gereksiz eklentileri uzak tarafa kurma. Ağ gecikmesi $20$–$50\,ms$ civarındaysa deneyim çoğu projede yerel geliştirmeye oldukça yaklaşır.

Remote-SSH özellikle güçlü işlemci, Linux bağımlılıkları, GPU veya merkezi geliştirme ortamı gereken projelerde harikadır. Kod sunucudan ayrılmaz; sen ise sevdiğin kısayollar, tema ve VS Code arayüzüyle çalışmaya devam edersin. Kısacası sunucunun kası ile bilgisayarının konforu aynı takımda oynar.

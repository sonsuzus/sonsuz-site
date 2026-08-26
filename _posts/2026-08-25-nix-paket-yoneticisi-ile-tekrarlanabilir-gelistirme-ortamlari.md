---
layout: post
title: "Nix Paket Yöneticisi ile Tekrarlanabilir Geliştirme Ortamları"
math: true
categories: 
  - Bilgi
tags: 
  - nix
  - paket yönetimi
  - devops
toc: true
---

Bir projeyi yeni bir bilgisayarda çalıştırırken yaşanan “bende çalışıyordu” sendromu, çoğu zaman koddan değil ortamdan kaynaklanır. Farklı derleyici sürümleri, eksik kütüphaneler ve işletim sistemi farkları geliştirme sürecini tahmin edilmez hâle getirir. Nix, paketleri ve geliştirme ortamlarını deklaratif biçimde tanımlayarak bu kaosu kontrol altına alan güçlü bir paket yöneticisidir.
``
## Nix'in temel fikri: bağımlılık grafiği

Geleneksel paket yöneticileri çoğunlukla sistemi yerinde değiştirir: bugün kurduğunuz bir paket, yarın başka bir paketin sürümünü etkileyebilir. Nix ise her paketi, bağımlılıklarıyla birlikte benzersiz bir yolda saklar. Bu yolun adı **Nix store**'dur ve genellikle `/nix/store` altında bulunur.

Bir paketin kimliği; kaynak kodu, derleme seçenekleri, bağımlılıkları ve ilgili sistem bilgileri üzerinden hesaplanır. Basitleştirilmiş hâliyle bunu şöyle düşünebilirsiniz:

$$
PaketKimliği = H(kaynak + bağımlılıklar + yapılandırma)
$$

Buradaki $H$, kriptografik bir özet fonksiyonudur. Girdi değişirse çıktı da değişir; dolayısıyla aynı tanım aynı ortamı, farklı tanım ise ayrı bir ortamı üretir. Nix'in tekrarlanabilirlik iddiasının kalbinde bu yaklaşım vardır.

| Özellik | Klasik paket yönetimi | Nix yaklaşımı |
|---|---|---|
| Paket kurulumu | Sistem genelini değiştirir | İzole store yoluna yazılır |
| Sürüm çakışması | Sık görülür | Birden fazla sürüm birlikte yaşayabilir |
| Geri alma | Zor veya sınırlı | Nesiller üzerinden kolay |
| Ortam tanımı | Çoğunlukla dokümantasyonda | Kod olarak depoda |

## Geliştirme kabuğu oluşturmak

Nix ile bir proje için gereken araçları `flake.nix` dosyasında tanımlayabilirsiniz. Örneğin Node.js, Python ve Git içeren küçük bir geliştirme kabuğu şöyle hazırlanabilir:

```nix
{
  description = "Tekrarlanabilir web projesi ortami";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          nodejs_22
          python312
          git
        ];

        shellHook = ''
          echo "Gelisim ortami hazir!"
          node --version
        '';
      };
    };
}
```

Bu dosya, ortamın tarifidir; ekip arkadaşınızın makinesine tek tek “Node 22 kur, Python 3.12 yükle” demenize gerek kalmaz. Proje dizininde `nix develop` komutunu çalıştırmak yeterlidir. `shellHook` bölümü ise kabuk açıldığında çalışan karşılama mesajı veya çevre değişkeni tanımları için kullanılır.

## Flake lock dosyası neden önemlidir?

`flake.nix`, kullanılacak kaynakları tanımlar; `flake.lock` ise bu kaynakların tam hangi revizyonlarda olduğunu kilitler. Böylece ekipteki herkes yalnızca aynı paket adını değil, aynı paket koleksiyonunu kullanır. Bu fark özellikle CI/CD sistemlerinde kritiktir.

| Dosya | Görevi | Git'e eklenmeli mi? |
|---|---|---|
| `flake.nix` | Ortamın deklaratif tarifi | Evet |
| `flake.lock` | Kesin bağımlılık revizyonları | Evet |
| `result` | Yerel derleme bağlantısı | Hayır |

Nix'in güzel yanı, yerel makine ile sürekli entegrasyon sunucusunu aynı reçeteye bağlamasıdır. CI tarafında `nix develop --command npm test` benzeri bir komut çalıştırdığınızda, testler geliştiricinin kullandığı araç zinciriyle uyumlu bir ortamda yürür.

## Pratik başlangıç önerileri

İlk aşamada her şeyi Nix'e taşımaya çalışmayın. Önce derleyici, çalışma zamanı ve formatlayıcı gibi kritik araçları `devShell` içine alın. Ardından veritabanı istemcileri, test araçları ve özel betiklerle ortamı genişletin. `nix flake update` komutunu bilinçli aralıklarla çalıştırarak güncellemeleri küçük ve denetlenebilir adımlara bölün.

Sonuçta Nix, yalnızca “paket kuran farklı bir araç” değildir. Geliştirme ortamını sürümlenebilir, paylaşılabilir ve yeniden üretilebilir bir yazılım çıktısına dönüştürür. Kurulum rehberleri yerine çalışan bir tanım bırakırsınız; gelecek zamandaki kendiniz ve takımınız bunun için size teşekkür eder.

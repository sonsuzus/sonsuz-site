---
layout: post
title: "sudo Ortam Değişkenlerini Neden Kaybeder?"
math: true
categories: 
  - Bilgi
tags: 
  - linux
  - sudo
  - ortam-değişkenleri
  - shell
  - güvenlik
  - devops
toc: true
image: /img/sudo-ortam-degiskenlerini-61.png
---

Terminalde çalışan bir komutun başına `sudo` eklediğinizde aniden API anahtarını, özel `PATH` ayarını veya uygulama yapılandırmasını görememesi oldukça şaşırtıcıdır. Fakat bu davranış bir hata değil, `sudo` tarafından bilinçli şekilde uygulanan bir güvenlik önlemidir. Gelin değişkenlerin nereye kaybolduğunu ve onları güvenli biçimde nasıl geri getirebileceğimizi inceleyelim.

``

## Ortam değişkeni nedir?

Shell, başlattığı süreçlere anahtar-değer çiftlerinden oluşan bir ortam aktarır. Örneğin aşağıdaki komut, `APP_MODE` değişkenini mevcut shell ve onun alt süreçleri için erişilebilir yapar:

```bash
export APP_MODE=development
node app.js
```

Normal koşullarda çocuk süreç, ebeveyn sürecin dışa aktarılmış değişkenlerinin bir kopyasını alır. Bunu basitleştirerek şu şekilde ifade edebiliriz:

$$E_{child} = E_{parent} \cup E_{command}$$

Burada $E$, sürece aktarılan ortam değişkenleri kümesidir. Ancak araya `sudo` girdiğinde yeni süreç yalnızca shell tarafından değil, ayrıca `sudo` güvenlik politikası tarafından hazırlanır:

$$E_{sudo} = (E_{parent} \cap E_{allowed}) \cup E_{sudo\_defaults}$$

Yani yalnızca izin verilen değişkenler korunur; geri kalanı temizlenir veya güvenli varsayılanlarla değiştirilir.

## Neden temizleniyor?

Bir ortam değişkeni masum görünse de çalıştırılacak kodu etkileyebilir. `PATH`, `LD_PRELOAD`, `PYTHONPATH` ve benzeri değişkenler yanlış programın ya da kütüphanenin root yetkisiyle yüklenmesine yol açabilir. Kullanıcının bütün ortamını doğrudan yönetici sürecine taşımak, yetki yükseltme açığı oluşturabilir.

Birçok sistemde `/etc/sudoers` içindeki `env_reset` seçeneği bu filtrelemeyi etkinleştirir. Ayrıca `secure_path`, `sudo` ile çalıştırılan komutlarda kullanılacak güvenilir bir `PATH` tanımlar.

| Yöntem | Değişken davranışı | Güvenlik durumu | Kullanım amacı |
|---|---|---|---|
| `sudo komut` | Çoğu özel değişken silinir | En güvenli varsayılan | Genel yönetim işleri |
| `sudo -E komut` | İzin verilen kullanıcı ortamı korunur | Daha dikkatli kullanılmalı | Geçici geliştirme işlemleri |
| `sudo VAR=değer komut` | Belirli değişken aktarılır | Kontrollü | Tek değişken gereken işler |
| `sudoers env_keep` | Seçilen değişkenler kalıcı korunur | Doğru yapılandırılmalı | Sistem çapında politika |

![sudo-ortam-degiskenlerini-61](/img/sudo-ortam-degiskenlerini-61.svg)


## Önce problemi doğrulayın

Aynı değişkeni normal kullanıcı ve `sudo` ortamında karşılaştırabilirsiniz:

```bash
export APP_MODE=development
printenv APP_MODE
sudo printenv APP_MODE
```

İlk komut `development` yazarken ikinci komut boş sonuç verebilir. Ortamların tamamını karşılaştırmak için çıktıları sıralayıp `diff` kullanmak daha açıklayıcıdır:

```bash
env | sort > /tmp/user-env.txt
sudo env | sort > /tmp/sudo-env.txt
diff -u /tmp/user-env.txt /tmp/sudo-env.txt
```

Bu kod, iki ortam arasındaki eklenen, kaldırılan veya değiştirilen değerleri gösterir.

## Güvenli çözüm seçenekleri

Yalnızca gerekli değişkeni komut satırında geçirmek genellikle en açık çözümdür:

```bash
sudo APP_MODE=production /opt/myapp/start.sh
```

Değişken mevcut shell değerinden alınacaksa şu biçim kullanılabilir:

```bash
sudo APP_MODE="$APP_MODE" /opt/myapp/start.sh
```

Tüm ortamı korumayı denemek için `sudo -E` kullanılabilir:

```bash
sudo -E ./deploy.sh
```

Ancak `-E`, sistemdeki `sudoers` politikası izin vermiyorsa etkisiz olabilir. Ayrıca hassas veya davranış değiştirici değişkenleri root sürecine taşımak risklidir.

Kalıcı ve kontrollü izin için `sudo visudo` ile yapılandırma düzenlenebilir:

```sudoers
Defaults env_keep += "APP_MODE API_ENDPOINT"
```

`visudo`, sözdizimini doğrulayarak hatalı bir dosya yüzünden `sudo` erişiminin bozulmasını önler. API anahtarlarını bu listeye gelişigüzel eklemek yerine secret manager, korumalı yapılandırma dosyası veya systemd kimlik bilgileri kullanmak daha doğrudur.

Sonuç olarak `sudo`, değişkenlerinizi unutmaz; onları güvenlik kontrolünden geçirir. En iyi yaklaşım, bütün ortamı taşımak yerine ihtiyaç duyulan değişkenleri açıkça ve mümkün olan en dar kapsamda aktarmaktır.

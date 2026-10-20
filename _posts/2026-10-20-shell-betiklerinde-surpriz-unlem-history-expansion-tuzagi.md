---
layout: post
title: "Shell Betiklerinde Sürpriz Ünlem: History Expansion Tuzağı"
math: true
categories: 
  - Bilgi
tags: 
  - shell
  - bash
  - history-expansion
  - betik
  - linux
  - hata-ayiklama
toc: true
image: /img/shell-betiklerinde-surpriz-33.png
---

Bir betik çalıştırıyorsunuz; parola, URL veya mesaj içinde sıradan bir `!` karakteri var. Birden terminal `event not found` diye bağırıyor ya da komutunuz beklenmedik biçimde değişiyor. Suçlu çoğu zaman Bash’in **history expansion** özelliğidir. Ünlem işareti kabuk için yalnızca heyecan belirtmez; geçmiş komutlara açılan gizli bir kapı da olabilir.


![shell-betiklerinde-surpriz-33](/img/shell-betiklerinde-surpriz-33.svg)

``

## History expansion nedir?

Bash, etkileşimli kullanımda önceki komutları hızlıca çağırmak için `!` ile başlayan ifadeleri yorumlayabilir. Örneğin `!!` son komutu, `!42` geçmişteki 42 numaralı komutu, `!git` ise `git` ile başlayan son komutu temsil eder.

Bunu basitçe şu dönüşümle düşünebiliriz:

$$
\text{çalıştırılan komut} = H(\text{yazılan metin})
$$

Buradaki $H$, history expansion etkinse ünlem ifadelerini geçmişteki komutlarla değiştiren fonksiyondur. Özellik kapalıysa $H(x)=x$ olur; yani metin değişmeden kalır.

| Yazılan ifade | Özellik açıkken olası anlamı | Özellik kapalıyken |
|---|---|---|
| `!!` | Son komut | İki ünlem karakteri |
| `!42` | 42 numaralı geçmiş girdisi | Değişmeden kalır |
| `!echo` | Son `echo` komutu | Değişmeden kalır |
| `merhaba!` | Genellikle aynı kalır | Aynı kalır |

Bash’in **etkileşimli olmayan** betiklerinde history expansion normalde kapalıdır. Ancak betik `source` ile etkileşimli bir kabuğa yüklenirse, `bash -H` ile başlatılırsa veya kod içinde `set -H` çalıştırılırsa özellik devreye girebilir. Bu yüzden “Betikte asla olmaz” varsayımı güvenli değildir.

## Çifte tırnak her zaman korumaz

Shell programlamasında çifte tırnağın özel karakterleri tamamen etkisizleştirdiği sanılır. Oysa history expansion etkin olduğunda `!`, çifte tırnak içinde de yorumlanabilir:

```bash
#!/usr/bin/env bash
set -H

password="Guclu!Parola"
echo "$password"
```

Bash, `!Parola` için uygun bir geçmiş olayı arayabilir ve `event not found` hatası üretebilir. Üstelik expansion, değişkenin değerinden çok kaynak satırı okunurken önem kazanır. Bu nedenle davranış kabuk sürümüne, çalışma biçimine ve bağlama göre şaşırtıcı görünebilir.

## En güvenli çözüm: Özelliği kapatmak

History expansion gerekmeyen bir betiğin başında özelliği açıkça kapatabilirsiniz:

```bash
#!/usr/bin/env bash
set +H
# Aynı işlemin daha açıklayıcı karşılığı:
set +o histexpand

message="Dağıtım tamamlandı!"
printf '%s\n' "$message"
```

`set +H`, `histexpand` seçeneğini kapatır. Buradaki artı işaretinin seçeneği kapatması ilk bakışta ters gelebilir: Bash’te `set -H` açar, `set +H` kapatır.

| Yaklaşım | Güvenilirlik | Kullanım amacı |
|---|---:|---|
| `set +H` | Yüksek | Betik genelinde expansion’ı kapatır |
| Tek tırnak kullanmak | Yüksek | Sabit metni korur |
| `\!` ile kaçırmak | Orta | Belirli bir ünlemi korur |
| Çifte tırnağa güvenmek | Düşük | History expansion için yeterli olmayabilir |

Sabit bir değer söz konusuysa tek tırnak da kullanılabilir:

```bash
printf '%s\n' 'İşlem başarılı!'
printf '%s\n' 'api-token: abc!123'
```

Ancak tek tırnak içinde değişken genişletmesi yapılmaz. Örneğin `'Merhaba $USER!'`, kullanıcı adını değil, doğrudan `$USER` metnini yazdırır.

## Durumu teşhis etmek

Seçeneğin mevcut durumunu aşağıdaki komutla görebilirsiniz:

```bash
set -o | grep histexpand
```

Çıktıda `histexpand on` görülüyorsa ünlem genişletmesi açıktır. Betik `source script.sh` biçiminde çalıştırılıyorsa aynı kabuğun seçeneklerini miras alabileceğini unutmayın. Bağımsız çalıştırma için yürütme izni verip `./script.sh` kullanmak daha öngörülebilir olabilir.

Özetle ünlem kaynaklı hatalarda yalnızca kaçış karakterleriyle boğuşmayın. Önce kabuğun türünü, betiğin nasıl çalıştırıldığını ve `histexpand` durumunu kontrol edin. Otomasyon kodunda geçmiş komut sihrine ihtiyaç yoksa `set +H` diyerek sürprizi daha perde açılmadan bitirin.

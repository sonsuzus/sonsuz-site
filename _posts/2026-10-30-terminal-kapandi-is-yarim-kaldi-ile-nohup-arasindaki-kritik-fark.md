---
layout: post
title: "Terminal Kapandı, İş Yarım Kaldı: & ile nohup Arasındaki Kritik Fark"
math: true
categories: 
  - Bilgi
tags: 
  - shell
  - bash
  - linux
  - sighup
  - nohup
  - süreç-yönetimi
toc: true
image: /img/terminal-kapandi-is-30.png
---

Uzun süren bir betiği başlatıp sonuna `&` koydunuz. Komut satırı geri geldi, siz de terminali kapattınız. Biraz sonra baktınız ki işlem ortadan kaybolmuş! Peki arka planda çalışması gerekmiyor muydu? Gerekiyordu; fakat **arka planda çalışmak, terminalden bağımsız yaşamak değildir**. İşte bu küçük farkın başrollerinde kabuk, SIGHUP ve `nohup` bulunuyor.


![terminal-kapandi-is-30](/img/terminal-kapandi-is-30.svg)

``

## `&` Aslında Ne Yapar?

Kabuk, normalde ön plandaki komutun tamamlanmasını bekler. Komutun sonuna `&` eklemek, onu asenkron başlatır: kabuk beklemeden yeni komut kabul eder. İş kontrolü etkin etkileşimli Bash oturumunda bu işlem ayrı bir arka plan süreç grubunda yönetilir.

```bash
bash -c 'while true; do date; sleep 5; done' > nabiz.log 2>&1 &
echo "Arka plan PID: $!"
```

Bu örnek beş saniyede bir tarih yazar. `$!`, en son başlatılan arka plan işinin süreç kimliğini verir. Çıktıyı dosyaya göndermek ekran karmaşasını önler; ancak **SIGHUP koruması sağlamaz**.

Mantıksal ayrımı şöyle özetleyebiliriz:

$$\text{Arka plan yürütme} \neq \text{Oturumdan bağımsızlık}$$

| Özellik | Normal komut | `komut &` |
|---|---|---|
| Kabuk tamamlanmasını bekler mi? | Evet | Hayır |
| Terminalle ilişkisi otomatik kesilir mi? | Hayır | Hayır |
| SIGHUP otomatik yok sayılır mı? | Hayır | Hayır |

Kısacası `&`, çalışana “masana dön” der; “binanın elektriği kesilse de çalış” demez.

## Terminal Kapanınca SIGHUP Nereden Gelir?

SIGHUP, tarihsel olarak modem bağlantısının kopmasını bildiren “hangup” sinyalidir. Günümüzde terminal bağlantısının kaybolmasıyla da ilişkilidir. Varsayılan davranışı, sinyali alan süreci sonlandırmaktır.

Terminal kapandığında terminal sürücüsü ilgili oturumdaki süreçlere SIGHUP gönderebilir. Etkileşimli Bash de SIGHUP aldığında, çıkmadan önce iş listesindeki süreçlere bu sinyali iletebilir. Böylece arka plandaki iş, doğrudan veya kabuk üzerinden etkilenebilir.

Burada önemli bir nüans var: **Terminali kapatmak ile kabuktan normal `exit` komutuyla çıkmak aynı olay değildir.** Sonuç; kabuğa, iş kontrolüne, oturum yapısına ve ayarlara bağlıdır. Örneğin Bash’in `huponexit` seçeneği, etkileşimli giriş kabuğunun normal çıkışında işlere SIGHUP gönderilmesini sağlayabilir. Dolayısıyla “her `&` işlemi kesin ölür” ifadesi fazla iddialıdır.

## `nohup`: SIGHUP İçin Kulak Tıkacı

`nohup`, çalıştıracağı komutun SIGHUP sinyalini yok saymasını sağlar. Ancak komutu kendi başına arka plana taşımaz. Bunun için yine `&` gerekir.

Aşağıdaki örnek, hem sinyal davranışını hem de standart giriş ve çıkışları açıkça düzenler:

```bash
nohup bash -c 'while true; do date; sleep 5; done' \
  > nabiz.log 2>&1 < /dev/null &

pid=$!
printf '%s\n' "$pid" > nabiz.pid
ps -p "$pid" -o pid,ppid,sid,stat,args
```

Burada `nohup`, SIGHUP sinyalinin yok sayılmasını ayarlar. `> nabiz.log` standart çıktıyı dosyaya gönderir; `2>&1` standart hatayı aynı hedefe bağlar. `< /dev/null` ise terminalden veri okunmasını engeller. Son satır süreç kimliğini, ebeveynini, oturum kimliğini ve durumunu gösterir.

Yönlendirme sırası önemlidir: `> nabiz.log 2>&1`, önce çıktıyı dosyaya bağlar, ardından hatayı bu yeni hedefe yönlendirir. Sıralamayı ters çevirmek aynı sonucu vermeyebilir.

Çıktı hâlâ terminale bağlıysa `nohup`, genellikle `nohup.out` dosyasını kullanır. Açık yönlendirme yapmak, kayıtların nerede olduğunu tahmin etme oyununu ortadan kaldırır.

## Hangi Araç, Hangi İhtiyaç?

\vert  Yöntem \vert  Temel amaç \vert  Sınır veya not \vert 
\vert ---\vert ---\vert ---\vert 
\vert  `komut &` \vert  Kabukta beklemeden çalıştırmak \vert  SIGHUP koruması yok \vert 
\vert  `nohup komut &` \vert  SIGHUP yok sayılarak arka planda çalıştırmak \vert  Yeni oturum oluşturmaz \vert 
\vert  `disown -h %1` \vert  Bash’in ilgili işe SIGHUP iletmesini engellemek \vert  Terminal giriş/çıkışını düzeltmez \vert 
\vert  `tmux` veya `screen` \vert  Yeniden bağlanılabilir terminal sunmak \vert  Etkileşimli işler için uygundur \vert 

`disown`, zaten başlatılmış işler için kullanışlıdır. Fakat kabuğun sinyal iletmesini engellemek, başka kaynaklardan gelebilecek SIGHUP sinyallerine karşı genel koruma değildir.

## Ölümsüzlük Değil, Belirli Bir Koruma

Hedefimiz $T_{\text{iş}} > T_{\text{terminal}}$ olabilir; yani iş, terminalden uzun yaşasın. `nohup` bunu birçok sıradan senaryoda mümkün kılar, fakat SIGTERM, SIGKILL, bellek yetersizliği veya makinenin kapanmasına karşı kalkan değildir. Oturum yöneticisinin süreçleri ayrıca temizlemesi de sonucu değiştirebilir.

Terminal kapandıktan sonra `ps -p PID` ile sürecin varlığını, günlük dosyasıyla da gerçekten ilerlediğini kontrol edin. **Çalışıyor görünmek ile iş üretmek farklıdır.**

Kalıcı uygulamalarda bir servis yöneticisi kullanın. Tek seferlik uzun görevlerde ise reçete nettir: **`nohup` sinyali yönetir, yönlendirmeler terminal bağımlılığını azaltır, `&` kabuğu serbest bırakır.**

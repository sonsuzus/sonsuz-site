---
layout: post
title: "SIGTERM Yetmediğinde: kill, SIGKILL ve Güvenli Süreç Sonlandırma"
math: true
categories: 
  - Bilgi
tags: 
  - linux
  - shell
  - sigterm
  - sigkill
  - süreç-yönetimi
  - unix
toc: true
image: /img/sigterm-yetmediginde-kill-34.png
---

![sigterm-yetmediginde-kill-34](/img/sigterm-yetmediginde-kill-34.svg)


Linux veya Unix benzeri bir sistemde donmuş görünen bir programı kapatmak için çoğu kişinin ilk refleksi `kill` komutudur. Ancak ismine rağmen `kill`, bir süreci doğrudan ortadan kaldırmaz; ona bir **sinyal** gönderir. Varsayılan sinyal olan SIGTERM sürece düzenli biçimde kapanma fırsatı verirken, SIGKILL işletim sisteminin devreye girip süreci koşulsuz sonlandırmasını sağlar.

``

## `kill` gerçekte ne yapar?

Aşağıdaki komut, PID değeri 4242 olan sürece varsayılan olarak SIGTERM gönderir:

```bash
kill 4242
```

Bu işlem şu komutla eşdeğerdir:

```bash
kill -TERM 4242
# Sayısal gösterimi:
kill -15 4242
```

Bir sinyal, çekirdeğin sürece ilettiği küçük bir bildirim olarak düşünülebilir. Basitleştirilmiş şekilde sinyal kümesini $S$ ile gösterirsek, `kill` işlemi şu biçimde modellenebilir:

$$
\operatorname{kill}(pid, s), \quad s \in S
$$

Burada `pid` hedef süreci, $s$ ise gönderilecek sinyali belirtir. Komutun adı yanıltıcıdır çünkü gönderilen her sinyal süreci öldürmez. Bazıları süreci durdurur, devam ettirir veya yalnızca belirli bir olaydan haberdar eder.

## SIGTERM neden tercih edilir?

SIGTERM, yani sinyal 15, sürece kibarca “Artık kapanmalısın” der. Süreç bu sinyali yakalayan bir işleyici çalıştırabilir. Böylece:

- Açık dosyalarını kapatabilir.
- Bellekteki verileri diske yazabilir.
- Geçici dosyaları silebilir.
- Ağ bağlantılarını düzgün biçimde sonlandırabilir.
- Alt süreçlerine kapanmaları gerektiğini bildirebilir.

Örneğin bir uygulama SIGTERM aldığında kontrollü temizlik yapabilir:

```python
import signal
import sys
import time

def shutdown(signum, frame):
    print("SIGTERM alındı, kaynaklar temizleniyor...")
    # Dosya, bağlantı ve geçici kaynaklar burada kapatılır.
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown)

while True:
    time.sleep(1)
```

Ne var ki bir süreç SIGTERM için özel bir işleyici tanımlayabilir, sinyali erteleyebilir veya tamamen yok sayabilir. Ayrıca süreç sonsuz döngüde, kesilemeyen bir çekirdek bekleyişinde ya da hatalı bir kapanma rutininde takılı kalabilir. Bu durumda `kill PID` komutu beklenen sonucu vermez.

## SIGTERM ve SIGKILL karşılaştırması

| Özellik | SIGTERM | SIGKILL |
|---|---|---|
| Sinyal numarası | 15 | 9 |
| Süreç tarafından yakalanabilir mi? | Evet | Hayır |
| Yok sayılabilir mi? | Evet | Hayır |
| Temizlik fırsatı verir mi? | Evet | Hayır |
| Veri kaybı riski | Daha düşük | Daha yüksek |
| Önerilen kullanım | İlk seçenek | Son çare |

SIGKILL doğrudan çekirdek tarafından uygulanır. Sürecin bu sinyal için işleyici oluşturması, sinyali engellemesi veya “Bir dakika, dosyamı kaydedeyim” demesi mümkün değildir:

```bash
kill -KILL 4242
# Kısa ve yaygın biçimi:
kill -9 4242
```

## `kill -9` ne zaman gereklidir?

Önce SIGTERM gönderilmeli ve sürece makul bir kapanma süresi tanınmalıdır. Hâlâ çalışıyorsa SIGKILL değerlendirilebilir:

```bash
kill -TERM 4242
sleep 5

if kill -0 4242 2>/dev/null; then
    echo "Süreç kapanmadı; SIGKILL gönderiliyor."
    kill -KILL 4242
fi
```

Buradaki `kill -0`, gerçek bir sonlandırma sinyali göndermeden sürecin varlığını ve erişim iznini kontrol eder. Bu yaklaşım servis yönetim betiklerinde kullanışlıdır.

SIGKILL; yanıt vermeyen, CPU’yu kontrolsüz tüketen, kapanma isteğini sürekli reddeden veya sistemi tehlikeye atan süreçlerde gerekli olabilir. Ancak veritabanı, dosya yazan uygulama ya da işlem yürüten sunucu aniden öldürülürse veri bozulması oluşabilir. Ayrıca `D` durumundaki kesilemeyen çekirdek bekleyişinde bulunan bir süreç, SIGKILL gönderilse bile kaynak işlemi tamamlanana kadar kaybolmayabilir.

Kısacası doğru sıra şudur: önce SIGTERM ile kapıyı çal, biraz bekle, yalnızca cevap gelmiyorsa SIGKILL ile kapıyı kır. `kill -9` güçlüdür; fakat güç, özellikle üretim sistemlerinde, dikkatle kullanılmalıdır.

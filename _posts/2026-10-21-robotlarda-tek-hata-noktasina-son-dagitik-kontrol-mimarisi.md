---
layout: post
title: "Robotlarda Tek Hata Noktasına Son: Dağıtık Kontrol Mimarisi"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - dağıtık-sistemler
  - kontrol-mimarisi
  - hata-toleransı
  - çoklu-robot-sistemleri
toc: true
image: /img/robotlarda-tek-hata-80.png
---

![robotlarda-tek-hata-80](/img/robotlarda-tek-hata-80.svg)


Bir robot filosunun bütün kararlarını tek bir merkezi bilgisayara emanet etmek, orkestrayı yalnızca şefin duyabildiği bir kulaklıkla yönetmeye benzer: Şef görevini yaptığı sürece sonuç harikadır; fakat kulaklık bozulursa herkes farklı telden çalmaya başlar. Dağıtık kontrol mimarisi, algılama, karar verme ve eylem üretme sorumluluklarını birden fazla robot veya kontrol düğümü arasında paylaşarak bu kırılganlığı azaltır. Böylece tek bir bileşenin arızalanması, sistemin tamamını zorunlu olarak durdurmaz.

``

## Merkezi mimarinin kırılgan noktası

Merkezi kontrol sisteminde sensör verileri bir ana denetleyiciye gönderilir. Denetleyici dünyayı yorumlar, görevleri planlar ve robotlara komut yollar. Yönetimi kolaylaştıran bu yaklaşımda merkezi denetleyici bir **single point of failure**, yani tek hata noktası olabilir.

Merkezi düğümün çalışma olasılığı $p$ ise ona tamamen bağımlı sistemin erişilebilirliği kabaca

$$A_{sistem} = p$$

olarak düşünülebilir. Düğüm çöktüğünde iletişim ağı ve robotlar sağlam olsa bile karar üretilemez. Kısacası kaslar yerindedir, fakat beyin tatile çıkmıştır.

Dağıtık mimaride ise her düğüm yerel sensörlerini değerlendirir, komşularıyla bilgi paylaşır ve belirli kararları bağımsız biçimde verebilir. Kritik görev $n$ bağımsız düğüm tarafından yedekleniyorsa ve her düğümün arıza olasılığı $q$ ise tüm düğümlerin aynı anda kaybedilme olasılığı ideal koşullarda

$$P_{kayıp} = q^n$$

olur. Örneğin $q=0.1$ ve $n=3$ için sonuç $0.001$’dir. Ancak bağımsızlık varsayımı önemlidir: Bütün düğümler aynı güç kaynağına bağlıysa dağıtık yazılım, ortak sigortayı sihirli biçimde kurtaramaz.

## Merkezi ve dağıtık yaklaşım

| Özellik | Merkezi kontrol | Dağıtık kontrol |
|---|---|---|
| Karar noktası | Tek ana denetleyici | Birden fazla düğüm |
| Hata etkisi | Sistemin tamamına yayılabilir | Çoğunlukla yerel kalır |
| Ölçeklenebilirlik | Merkez darboğaz olabilir | Yeni düğümlerle artabilir |
| Tutarlılık | Yönetilmesi daha kolay | Uzlaşma mekanizması gerekir |
| İletişim | Merkezle bağlantı kritiktir | Komşular arası bağlantılar kritiktir |
| Tasarım karmaşıklığı | Görece düşük | Görece yüksek |

## Tek hata noktası nasıl kaldırılır?

Yalnızca kontrol kodunu üç bilgisayara kopyalamak yeterli değildir. Gerçek hata toleransı için şu katmanlar birlikte tasarlanmalıdır:

1. **Yedekli karar üretimi:** Bir lider kaybolduğunda başka bir düğüm liderliği devralmalıdır.
2. **Yerel otonomi:** Robot, bağlantı kesildiğinde güvenli biçimde durabilmeli veya görevini sınırlı olarak sürdürebilmelidir.
3. **Dağıtık durum paylaşımı:** Konum, görev ve sağlık bilgileri düğümler arasında güncellenmelidir.
4. **Çoğunluk kararı:** Çelişkili sonuçlarda oylama ya da Raft benzeri uzlaşma yöntemleri kullanılmalıdır.
5. **Fiziksel yedeklilik:** Ağ anahtarı, batarya ve saat kaynağı gibi donanımlar da hesaba katılmalıdır.

Aşağıdaki basitleştirilmiş Python örneği, liderden belirli süre mesaj alınamazsa düğümün seçim başlatmasını gösterir:

```python
import time

class ControlNode:
    def __init__(self, node_id, timeout=2.0):
        self.node_id = node_id
        self.timeout = timeout
        self.last_heartbeat = time.monotonic()
        self.role = "follower"

    def receive_heartbeat(self):
        # Liderin hâlâ çalıştığını kaydeder.
        self.last_heartbeat = time.monotonic()

    def update(self):
        elapsed = time.monotonic() - self.last_heartbeat
        if elapsed > self.timeout:
            self.start_election()

    def start_election(self):
        # Gerçek sistemde diğer düğümlere oy isteği gönderilir.
        self.role = "candidate"
        print(f"Düğüm {self.node_id}: lider seçimi başlatıldı")
```

Bu kod tek başına eksiksiz bir uzlaşma algoritması değildir; temel fikri görünür kılar: Bir düğümün sessizliği bütün sistemi dondurmak yerine yeniden yapılanmayı tetikler.

## Bedelsiz dayanıklılık yoktur

Dağıtık kontrol; ağ gecikmesi, paket kaybı, saat uyuşmazlığı ve bölünmüş ağ gibi yeni problemler getirir. İki robot kendisini aynı anda lider sanırsa **split-brain** oluşabilir. Bu nedenle kalp atışı mesajları, dönem numaraları, çoğunluk kuralları ve güvenli durum makineleri kullanılmalıdır.

Sonuç olarak dağıtık mimari, tek hata noktasını otomatik değil, doğru yedeklilik ve uzlaşma tasarımı sayesinde ortadan kaldırır. Başarılı bir sistem, yalnızca “kim karar veriyor?” sorusunu değil, “karar verici kaybolursa kim, ne kadar sürede ve hangi güvenlik sınırlarıyla devralacak?” sorusunu da cevaplar.

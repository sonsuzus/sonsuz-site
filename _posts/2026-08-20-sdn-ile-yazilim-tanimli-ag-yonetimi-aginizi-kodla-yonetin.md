---
layout: post
title: "SDN ile Yazılım Tanımlı Ağ Yönetimi: Ağınızı Kodla Yönetin"
math: true
categories: 
  - Bilgi
tags: 
  - sdn
  - ağ yönetimi
  - openflow
image: /img/sdn-ile-yazilim-47.png
---

Geleneksel ağlarda her yönlendirici ve anahtar kendi kararlarını verir; bu durum büyüyen altyapılarda yapılandırma karmaşası, tutarsız kurallar ve yavaş değişiklikler doğurur. Yazılım Tanımlı Ağlar (Software-Defined Networking, SDN), kontrol kararlarını merkezi bir yazılıma taşıyarak ağın davranışını programlanabilir hâle getirir. Böylece yönlendirme tabloları, güvenlik politikaları ve trafik öncelikleri tek tek cihazlara bağlanmadan dinamik biçimde yönetilebilir.
``

SDN'nin temel fikri, ağın **kontrol düzlemi** ile **veri düzlemini** ayırmaktır. Veri düzlemi, paketi belirlenmiş kurala göre ileten switch ve router'lardan oluşur. Kontrol düzlemi ise ağın genel görünümünü değerlendiren, politika üreten ve cihazlara akış kuralları gönderen SDN denetleyicisidir. Denetleyiciyi ağın orkestra şefi, cihazları ise notaları uygulayan müzisyenler gibi düşünebilirsiniz.

| Özellik | Geleneksel Ağ | SDN Yaklaşımı |
|---|---|---|
| Karar verme | Her cihazda dağınık | Merkezi veya mantıksal olarak merkezi |
| Yapılandırma | CLI ile cihaz bazlı | API ve otomasyon ile politika bazlı |
| Görünürlük | Parçalı ağ bilgisi | Ağın uçtan uca görünümü |
| Değişiklik hızı | Manuel, hata riski yüksek | Yazılımla hızlı ve tekrarlanabilir |

![sdn-ile-yazilim-47](/img/sdn-ile-yazilim-47.svg)


Bir SDN denetleyicisi, anahtarlardan bağlantı ve istatistik bilgisi toplar; ardından hedefe en uygun yolu hesaplar. Basit bir maliyet modelinde yol maliyeti şu şekilde ifade edilebilir:

$$C(P) = \sum_{e \in P} (\alpha \cdot gecikme_e + \beta \cdot kayip_e + \gamma \cdot yuk_e)$$

Burada $P$ seçilen yol, $e$ yol üzerindeki bağlantı ve $\alpha$, $\beta$, $\gamma$ ise işletmenin önceliklerini temsil eden ağırlıklardır. Örneğin görüntülü görüşme için gecikmenin ağırlığı artırılabilir; yedekleme trafiğinde ise bant genişliği maliyeti daha önemli olabilir. Denetleyici, bu hesabı periyodik olarak yeniden çalıştırıp trafik koşulları değiştiğinde akışları farklı bir yola taşıyabilir.

SDN dünyasında sık duyulan protokollerden biri **OpenFlow**'dur. OpenFlow, denetleyicinin switch akış tablolarına kural eklemesini, değiştirmesini veya silmesini sağlar. Bir akış kuralı genellikle paket eşleştirme alanları, uygulanacak eylemler ve öncelik bilgisinden oluşur. Mantıksal bir kural şu anlama gelebilir: “10.10.0.0/24 ağından gelen HTTP trafiğini ikinci porta ilet.”

```python
# Denetleyicinin üretebileceği örnek akış kuralı
flow_rule = {
    "priority": 200,
    "match": {
        "ipv4_src": "10.10.0.0/24",
        "tcp_dst": 80
    },
    "actions": [
        {"type": "OUTPUT", "port": 2}
    ],
    "idle_timeout": 60
}

controller.install_flow(switch_id="sw-01", rule=flow_rule)
```

Bu örnekte denetleyici, `sw-01` adlı anahtara belirli kaynak ağdan gelen HTTP paketlerini 2 numaralı porttan göndermesini söyler. `idle_timeout` değeri sayesinde kullanılmayan kural 60 saniye sonra temizlenir. Gerçek projelerde bu kurallar REST API'leri, OpenFlow mesajları veya üreticiye özgü otomasyon arabirimleri üzerinden iletilebilir.

| Senaryo | SDN ile çözüm |
|---|---|
| Link arızası | Denetleyici alternatif yolu hesaplayıp akışları günceller |
| DDoS şüphesi | Şüpheli IP veya port için merkezi engelleme kuralı dağıtır |
| Yoğun trafik | Akışları az kullanılan bağlantılara yönlendirir |
| Yeni şube | Şablon politikaları API üzerinden hızla uygular |

Merkezî yönetim, denetleyicinin kritik bir bileşen olduğu anlamına gelir. Bu nedenle yüksek erişilebilirlik için denetleyici kümesi, kimlik doğrulama, rol tabanlı yetkilendirme ve kayıt mekanizmaları kullanılmalıdır. Ayrıca her kararı anında değiştirmek yerine ölçüm, eşik değerleri ve geri dönüş planlarıyla çalışmak gerekir. Doğru tasarlandığında SDN, ağı sadece “çalışan kablolar” olmaktan çıkarır; ihtiyaçlara tepki veren, ölçülebilen ve kodla yönetilebilen canlı bir platforma dönüştürür.

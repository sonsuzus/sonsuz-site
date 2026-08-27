---
layout: post
title: "Canary Release: Yeni Sürümleri Güvenle Uçurmanın Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - canary release
  - devops
  - ci/cd
---

Yeni bir sürümü herkesin önüne aynı anda koymak, yazılım dünyasındaki en heyecanlı ama en riskli düğmelerdendir. Canary Release yaklaşımı bu riski küçültür: Yeni sürüm önce trafiğin küçük bir bölümüne sunulur, metrikler izlenir ve her şey yolundaysa erişim kademeli biçimde genişletilir. Adını, zehirli gazları erkenden fark etmek için madenlerde kullanılan kanaryalardan alır. Buradaki kanarya ise cesur birkaç kullanıcı değil; kontrollü bir trafik dilimidir.

``

Canary dağıtımının temel fikri, değişimin etkisini izole etmektir. Örneğin uygulamanın iki sürümü aynı anda çalışır: kararlı sürüm `v1` trafiğin çoğunu alırken, yeni `v2` başlangıçta yalnızca %1 veya %5 trafiği karşılar. Kullanıcı yönlendirme işlemi yük dengeleyici, API gateway, service mesh ya da özellik bayrağı (feature flag) üzerinden yapılabilir. Amaç yalnızca "uygulama ayakta mı?" sorusunu değil, "uygulama gerçek kullanıcı davranışında beklenen değeri üretiyor mu?" sorusunu da yanıtlamaktır.

Başarıyı ölçmek için bir karar fonksiyonu tanımlamak faydalıdır. Basit bir hata oranı şöyle hesaplanabilir:

$$ErrorRate = \frac{5xx\_istekleri}{toplam\_istekler} \times 100$$

Canary sürümünün hata oranı kararlı sürümden anlamlı derecede yüksekse dağıtım durdurulur. Örneğin kabul eşiği $ErrorRate_{v2} \leq ErrorRate_{v1} + 0.2\%$ olabilir. Ancak yalnızca hata oranına bakmak yeterli değildir; gecikme, kaynak tüketimi, dönüşüm oranı ve iş metrikleri de izlenmelidir. Bir ödeme servisinde başarılı ödeme oranı, teknik metriklerden bile daha kritik bir sinyal olabilir.

| Yaklaşım | Risk Seviyesi | Geri Alma Hızı | Uygun Senaryo |
|---|---:|---:|---|
| Big Bang dağıtımı | Yüksek | Değişken | Küçük, düşük etkili sistemler |
| Blue-Green | Orta | Çok hızlı | Altyapı maliyeti kabul edilebiliyorsa |
| Canary Release | Düşük-Orta | Çok hızlı | Sürekli trafik alan kritik servisler |

Canary stratejisi, rastgele kullanıcı seçmek zorunda değildir. İlk grup; şirket çalışanları, beta kullanıcıları, belirli bir bölge veya yalnızca yeni oturumlar olabilir. Bu seçimin dikkatli yapılması gerekir: Sadece düşük trafikli müşteriler kanaryaya girerse, yüksek yük altındaki performans sorunu görünmeyebilir. Temsil gücü olan bir örneklem seçmek, istatistiksel güvenin temelidir.

Aşağıdaki NGINX örneği, isteklerin yaklaşık %5'ini yeni sürüme yönlendiren basit bir yapı gösterir:

```nginx
split_clients "${remote_addr}${http_user_agent}" $backend_pool {
    5%      canary_backend;
    *       stable_backend;
}

upstream stable_backend {
    server app-v1:8080;
}

upstream canary_backend {
    server app-v2:8080;
}

server {
    location / {
        proxy_pass http://$backend_pool;
    }
}
```

Burada `split_clients`, istemci IP'si ve kullanıcı aracısını kullanarak tutarlı bir yönlendirme üretir. Böylece aynı kullanıcı her istekte farklı sürüme sıçramaz; hata ayıklama ve kullanıcı deneyimi daha tutarlı kalır. Gerçek sistemlerde oturum çerezi, kullanıcı kimliği veya servis mesh kuralları daha güvenilir alternatifler sunabilir.

İyi bir canary süreci üç aşamada düşünülmelidir: gözlem, karar ve genişletme. Önce sürüm %1 trafikle yayınlanır; loglar, dağıtık izler ve dashboard'lar incelenir. Ardından otomatik ya da insan onaylı bir karar verilir. Son olarak trafik %5, %25, %50 ve %100 gibi basamaklarla artırılır. Alarm tetiklenirse trafik anında `v1` sürümüne döndürülür. Bu geri alma işlemi veritabanı şeması değişiklikleriyle uyumlu olmalıdır; geriye dönük uyumsuz migrasyonlar canary'nin güvenlik ağını zayıflatır.

Canary Release sihirli bir değnek değildir; güçlü gözlemlenebilirlik, otomasyon ve net eşikler ister. Buna karşılık ekiplerin daha küçük riskler alarak daha sık teslimat yapmasını sağlar. Küçük bir kanaryanın uçuşunu dikkatle izlemek, tüm filoyu fırtınaya göndermekten çok daha akıllıcadır.

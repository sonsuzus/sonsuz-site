---
layout: post
title: "Oracle Cloud’da Ampere Sunucularını Yük Dengeleyiciyle Ölçeklendirme"
math: true
categories: 
  - Proje
tags: 
  - oracle cloud
  - ampere
  - yük dengeleme
toc: true
---

Tek bir Ampere sunucusu hızlı ve ekonomik olabilir; ancak bütün web trafiğini ona yönlendirmek, uygulamanın kaderini tek bir makineye bağlar. Oracle Cloud Infrastructure üzerinde bir yük dengeleyici kullanarak istekleri birden fazla Ampere A1 sunucusuna dağıtabilir, bakım sırasında kesintiyi azaltabilir ve trafik yükseldiğinde sisteminizi daha rahat ölçeklendirebilirsiniz.
``

## Mimarinin Temel Mantığı

Örnek mimarimizde internetten gelen HTTPS trafiği önce OCI Load Balancer’a ulaşır. Yük dengeleyici, sağlıklı durumdaki Ampere sunucularını içeren **backend set** üzerinden uygun hedefi seçer. Sunucular özel alt ağda tutulurken yalnızca yük dengeleyici genel IP adresine sahip olabilir.

Basitçe toplam istek oranı $λ$ ve sağlıklı sunucu sayısı $N$ ise ideal durumda her sunucu yaklaşık $λ_i ≈ λ/N$ istek işler. Fakat gerçek dağılım; bağlantı süreleri, oturum kalıcılığı ve seçilen algoritma nedeniyle tamamen eşit olmayabilir. Kararlı bir sistem için sunucuların toplam işleme kapasitesi talebi aşmalıdır:

$$ρ = \frac{λ}{Nμ} < 1$$

Burada $μ$, tek bir sunucunun saniyede işleyebildiği ortalama istek sayısıdır. $ρ$ değeri 1’e yaklaştıkça gecikme kuyruğu büyür; yani “CPU hâlâ çalışıyor” demek, kullanıcıların mutlu olduğu anlamına gelmez.

## Hangi Yük Dengeleyici?

| Özellik | OCI Load Balancer | OCI Network Load Balancer |
|---|---|---|
| Çalışma katmanı | Katman 7 ve Katman 4 | Katman 4 |
| TLS sonlandırma | Desteklenir | Genellikle sunucuda yapılır |
| HTTP yönlendirme | Gelişmiş | Sınırlı |
| İstemci IP koruma | Yapılandırmaya bağlı | Doğal olarak uygundur |
| Kullanım örneği | Web uygulaması, API | Çok yüksek hacimli TCP/UDP |

Web sitesi veya REST API için TLS sertifikası yönetimi, HTTP sağlık kontrolü ve yönlendirme kuralları gerektiğinden klasik OCI Load Balancer çoğu projede daha pratiktir.

## Ağ ve Güvenlik Tasarımı

Yük dengeleyiciyi genel alt ağa, Ampere instance’larını ise özel alt ağa yerleştirin. Network Security Group kurallarıyla internete yalnızca `443` portunu açın. Backend sunucularında `80` veya `8080` portuna sadece yük dengeleyicinin NSG’sinden erişim verin. SSH erişimini tüm internete açmak yerine Bastion servisi kullanın.

TLS sertifikasını yük dengeleyicide sonlandırmak sunucuların şifreleme yükünü azaltır. Daha yüksek güvenlik gerekiyorsa yük dengeleyici ile backend arasında da HTTPS kullanarak uçtan uca şifreleme sağlayabilirsiniz.

## Terraform ile Temel Backend Set

Aşağıdaki örnek, round-robin algoritmalı bir backend set ve HTTP sağlık kontrolü oluşturur:

```hcl
resource "oci_load_balancer_backend_set" "ampere_pool" {
  load_balancer_id = oci_load_balancer_load_balancer.web_lb.id
  name             = "ampere-web-pool"
  policy           = "ROUND_ROBIN"

  health_checker {
    protocol          = "HTTP"
    port              = 8080
    url_path          = "/health"
    return_code       = 200
    interval_ms       = 10000
    timeout_in_millis = 3000
    retries           = 3
  }
}

resource "oci_load_balancer_backend" "ampere_1" {
  load_balancer_id = oci_load_balancer_load_balancer.web_lb.id
  backendset_name  = oci_load_balancer_backend_set.ampere_pool.name
  ip_address       = "10.0.2.10"
  port             = 8080
}
```

`ROUND_ROBIN`, yeni istekleri sırayla sunuculara gönderir. `/health` uç noktası ise uygulamanın gerçekten çalışıp çalışmadığını denetler. Yalnızca işletim sisteminin açık olduğunu gösteren yüzeysel bir kontrol yerine veritabanı veya kritik bağımlılıkları hafifçe sınayan bir endpoint hazırlamak daha güvenlidir.

İkinci ve üçüncü Ampere sunucuları aynı backend set’e eklenebilir. Uygulama oturum bilgilerini yerel diskte saklıyorsa kullanıcı farklı sunucuya geçtiğinde oturumunu kaybedebilir. Bu nedenle oturumları Redis, veritabanı veya imzalı çerezlerde tutarak sunucuları **stateless** tasarlayın.

Son aşamada OCI Monitoring üzerinden sağlıksız backend sayısı, yanıt süresi ve HTTP 5xx oranı için alarm kurun. Böylece mimariniz yalnızca trafiği dağıtan değil, arızayı fark eden ve büyümeye hazır bir yapıya dönüşür.

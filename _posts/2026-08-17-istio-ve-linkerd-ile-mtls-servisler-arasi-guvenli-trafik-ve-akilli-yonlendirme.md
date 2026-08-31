---
layout: post
title: "Istio ve Linkerd ile mTLS: Servisler Arası Güvenli Trafik ve Akıllı Yönlendirme"
math: true
categories: 
  - Bilgi
tags: 
  - ıstio
  - linkerd
  - mtls
toc: true
image: /img/istio-ve-linkerd-98.png
---

Mikroservis mimarisinde bir isteğin kaç farklı servisten geçtiğini takip etmek bile bazen dedektiflik gerektirir. Güvenlik açısından daha kritik soru ise şudur: Bu servisler gerçekten birbirleriyle konuştuğunu sandıkları servisler mi? Servis ağı (service mesh), uygulama kodunu güvenlik ve ağ politikalarıyla şişirmeden bu sorunu çözmek için tasarlanır. Istio ve Linkerd; şifreleme, kimlik doğrulama, yetkilendirme, gözlemlenebilirlik ve trafik yönetimini altyapı katmanına taşır.
``
## mTLS neden gereklidir?

Klasik TLS, istemcinin bağlandığı sunucunun kimliğini doğrular ve iletişimi şifreler. Karşılıklı TLS yani **mTLS** ise iki ucu da doğrular: İstemci sunucuya, sunucu da istemciye sertifika sunar. Böylece ağ içinde "aynı kümeye erişebilen herkes güvenilirdir" varsayımı ortadan kalkar.

Bir mTLS oturumunda taraflar sertifikalarını doğrular, ortak bir oturum anahtarı üretir ve veri bu anahtarla şifrelenir. Kavramsal olarak mesaj gizliliği şöyle ifade edilebilir:

$$C = E_{K_s}(M)$$

Burada $M$ mesajı, $K_s$ oturum anahtarını, $E$ şifreleme işlemini ve $C$ şifreli veriyi temsil eder. mTLS yalnızca gizlilik sağlamaz; sertifika kimliği sayesinde çağrıyı yapan iş yükünün kimliği de bilinir. Bu yaklaşım zero-trust mimarisinin temelidir.

| Özellik | TLS | mTLS |
|---|---|---|
| Sunucu kimliği doğrulama | Var | Var |
| İstemci kimliği doğrulama | Genellikle yok | Var |
| Servis-servis iletişimi | Sınırlı güvence | Güçlü kimlik güvencesi |
| Yetkilendirme politikası | IP/başlık odaklı olabilir | İş yükü kimliği odaklıdır |

![istio-ve-linkerd-98](/img/istio-ve-linkerd-98.svg)


## Istio: Ayrıntılı kontrol paneli

Istio, Envoy tabanlı sidecar proxy'ler veya ambient mesh bileşenleri üzerinden trafiği yönetir. Sertifika üretimi, dağıtımı ve yenilenmesi çoğunlukla Istio'nun kontrol düzlemi tarafından otomatik yapılır. Strict mod etkinleştirildiğinde, mesh içindeki bir iş yükü yalnızca mTLS kullanan istemcilerden trafik kabul eder.

Aşağıdaki politika, `default` ad alanındaki servisler için mTLS'i zorunlu tutar:

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: strict-mtls
  namespace: default
spec:
  mtls:
    mode: STRICT
```

Bu yapılandırma uygulama koduna dokunmaz; proxy, gelen bağlantının sertifikalı ve şifreli olmasını denetler. Geçiş dönemlerinde `PERMISSIVE` modu hem düz metin hem mTLS trafiğini kabul eder. Ancak bu mod, uyumluluk için faydalı olsa da kalıcı güvenlik hedefi olmamalıdır.

Istio'nun güçlü tarafı, sürüm bazlı trafik yönetimidir. Örneğin yeni sürümü önce trafiğin %10'u ile sınamak için `VirtualService` kullanılabilir:

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: catalog
spec:
  hosts: [catalog]
  http:
  - route:
    - destination: { host: catalog, subset: v1 }
      weight: 90
    - destination: { host: catalog, subset: v2 }
      weight: 10
```

Bu canary yaklaşımı, hata oranı veya gecikme yükselirse geri dönüş kararını çok daha az riskli hale getirir.

## Linkerd: Daha sade, daha hafif yaklaşım

Linkerd de proxy tabanlıdır ancak kurulumu ve varsayılanları daha yalın tutmayı hedefler. Mesh'e eklenen iş yükleri arasında mTLS çoğunlukla otomatik olarak devreye girer. Linkerd kimliklerini Kubernetes servis hesabına bağlayarak sertifika operasyonunu geliştirici açısından görünmez kılar.

| Başlık | Istio | Linkerd |
|---|---|---|
| Trafik politikası derinliği | Çok kapsamlı | Temel ve pratik |
| Öğrenme eğrisi | Daha yüksek | Daha düşük |
| Proxy yaklaşımı | Envoy / ambient seçenekleri | Hafif Rust tabanlı proxy |
| Uygun senaryo | Karmaşık kurumsal kurallar | Hızlı, sade Kubernetes mesh'i |

Trafik yönlendirme sadece dağıtım stratejisi değildir; timeout, yeniden deneme, circuit breaking ve hata enjeksiyonu gibi dayanıklılık kurallarını da kapsar. Örneğin sınırsız retry, geçici bir hatayı zincirleme kaynak tüketimine dönüştürebilir. Bu nedenle politika tasarımı yapılırken gecikme bütçesi, idempotency ve servis kapasitesi birlikte değerlendirilmelidir.

Sonuç olarak Istio ayrıntılı kontrol isteyen ekipler için güçlü bir araç kutusu, Linkerd ise güvenli varsayılanlarla hızlı ilerlemek isteyenler için zarif bir seçenektir. Hangisi seçilirse seçilsin, mTLS'i `STRICT` hedefiyle devreye almak ve yönlendirme kurallarını ölçümlerle doğrulamak, servis ağını görünmez bir karmaşıklık yerine somut bir güvenlik katmanına dönüştürür.

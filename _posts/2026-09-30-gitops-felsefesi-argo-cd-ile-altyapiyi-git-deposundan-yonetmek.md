---
layout: post
title: "GitOps Felsefesi: Argo CD ile Altyapıyı Git Deposundan Yönetmek"
math: true
categories: 
  - Bilgi
tags: 
  - gitops
  - argocd
  - kubernetes
  - devops
  - continuous-delivery
  - bulut
toc: true
image: /img/gitops-felsefesi-argo-89.png
---

![gitops-felsefesi-argo-89](/img/gitops-felsefesi-argo-89.svg)


Bir Kubernetes kümesinde çalışan uygulamayı güncellemek için gece yarısı sunucuya bağlanıp gizemli komutlar çalıştırdığınızı düşünün. Sabah olduğunda kimse neyin, neden değiştiğini bilmiyor! GitOps bu maceraya son verir: Sistemin istenen durumu Git deposunda tanımlanır, Argo CD ise kümeyi sürekli izleyerek gerçek durumu bu tanıma yaklaştırır. Böylece Git yalnızca kaynak kodun değil, altyapının da güvenilir kayıt defteri olur.

``

## GitOps nedir?

GitOps, altyapı ve uygulama konfigürasyonlarının bildirimsel dosyalarla yönetildiği bir operasyon modelidir. Kubernetes manifestleri, Helm chart değerleri veya Kustomize katmanları Git üzerinde tutulur. Değişiklik yapmak isteyen geliştirici doğrudan kümeye müdahale etmek yerine pull request açar.

Bu modelde iki temel durum vardır:

- **İstenen durum:** Git deposunda tanımlanan konfigürasyon.
- **Gerçek durum:** Kubernetes kümesinde o anda çalışan kaynaklar.

Argo CD düzenli olarak bu durumları karşılaştırır. Basitçe sapmayı şöyle düşünebiliriz:

$$
D = \lvert S_{git} - S_{cluster} \rvert
$$

Burada $D$ konfigürasyon sapmasını temsil eder. Amaç, senkronizasyon işlemleriyle $D \to 0$ olmasını sağlamaktır. Elbette YAML dosyaları matematiksel olarak çıkarılmaz; formül, iki durum arasındaki farkın sürekli azaltılması fikrini anlatır.

| Yaklaşım | Manuel operasyon | GitOps |
|---|---|---|
| Değişiklik kaynağı | Terminal komutları | Git commitleri |
| Denetlenebilirlik | Sınırlı | Commit geçmişiyle güçlü |
| Geri alma | Komutlara ve hafızaya bağlı | Önceki commit'e dönüş |
| Sapma tespiti | Genellikle manuel | Otomatik |
| Yetkilendirme | Küme erişimi gerekir | Git ve PR politikaları kullanılabilir |

## Argo CD nasıl çalışır?

Argo CD, Kubernetes için geliştirilmiş bir sürekli teslimat aracıdır. Git deposunu kaynak, Kubernetes kümesini hedef kabul eder. Depodaki manifest değiştiğinde uygulamayı **OutOfSync** olarak işaretler. Senkronizasyon manuel başlatılabilir veya otomatik politika ile gerçekleştirilebilir.

Örnek bir depo yapısı şöyle olabilir:

```text
infrastructure/
├── base/
│   ├── deployment.yaml
│   └── service.yaml
└── overlays/
    ├── staging/
    └── production/
```

Bu yapı, ortak kaynakların `base` altında tutulmasını; ortama özgü replica, alan adı veya kaynak limiti gibi değerlerin `overlays` içinde değiştirilmesini sağlar.

Argo CD'ye bu depoyu tanıtan örnek bir `Application` kaynağı şöyledir:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: kahve-api
  namespace: argocd
spec:
  source:
    repoURL: https://github.com/ornek/infrastructure.git
    targetRevision: main
    path: overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: kahve-api
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

`path`, uygulanacak manifestlerin konumunu belirtir. `selfHeal`, kümede elle yapılan değişiklikleri Git'teki tanıma geri döndürür. `prune` ise Git'ten silinen kaynakların kümeden de kaldırılmasını sağlar. Bu seçenekler güçlüdür; yanlış bir commit'i de büyük bir disiplinle uygulayabilecekleri unutulmamalıdır.

## Tipik değişiklik akışı

Bir sürümü dağıtmak için `deployment.yaml` içindeki imaj etiketi değiştirilir:

```yaml
spec:
  template:
    spec:
      containers:
        - name: api
          image: registry.example.com/kahve-api:2.4.0
```

Ardından commit gönderilir, pull request incelemeden geçer ve ana dala birleştirilir. Argo CD farkı algılar, manifestleri uygular ve kaynakların sağlıklı duruma gelmesini takip eder. Sorun çıkarsa hatalı commit geri alınabilir. Böylece geri dönüş işlemi de kayıtlı ve tekrarlanabilir olur.

## Güvenli kullanım için öneriler

GitOps, “her şeyi otomatikleştir ve unut” yaklaşımı değildir. Üretim değişikliklerinde branch koruması, zorunlu inceleme, YAML doğrulaması ve politika kontrolleri kullanılmalıdır. Parolalar düz metin olarak Git'e yazılmamalı; Sealed Secrets, External Secrets veya bir gizli bilgi kasası tercih edilmelidir.

Argo CD ayrıca rol tabanlı erişim, sağlık kontrolleri ve senkronizasyon pencereleri sunar. Küme üzerinde yapılan acil bir manuel değişikliğin `selfHeal` tarafından geri alınabileceğini ekibin bilmesi gerekir.

Sonuç olarak GitOps; görünürlük, denetlenebilirlik ve tutarlılık kazandırır. Git karar defteri, Argo CD ise yorulmadan çalışan uygulayıcıdır. Doğru güvenlik politikalarıyla birleştiğinde “sunucuda kim ne değiştirdi?” sorusu yerini çok daha huzurlu bir soruya bırakır: “Hangi pull request'i incelemeliyiz?”

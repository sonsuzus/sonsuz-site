---
layout: post
title: "Helm ile Kubernetes Paket Yönetimi: YAML Karmaşasını Düzenleme Sanatı"
math: true
categories: 
  - Program
tags: 
  - kubernetes
  - helm
  - devops
---

Kubernetes üzerinde küçük bir uygulamayı dağıtmak çoğu zaman birkaç YAML dosyasıyla başlar; fakat uygulama büyüdükçe Deployment, Service, Ingress, ConfigMap, Secret, HPA ve RBAC tanımları hızla çoğalır. Helm, bu karmaşayı sürümlenebilir ve yeniden kullanılabilir paketlere dönüştüren Kubernetes paket yöneticisidir. Amaç yalnızca YAML üretmek değil; farklı ortamlar için aynı uygulamayı güvenilir, tutarlı ve tekrarlanabilir biçimde yayınlamaktır.
``

Helm'in temel birimi **chart** olarak adlandırılır. Bir chart, Kubernetes kaynak şablonlarını, varsayılan yapılandırmaları ve paket hakkındaki metaveriyi içerir. Uygulama kümeye kurulduğunda ise bu chart'ın çalışan örneği bir **release** olur. Aynı chart, örneğin `development`, `staging` ve `production` ortamlarında farklı değerlerle birden fazla release olarak kullanılabilir.

Helm'in arkasındaki ana fikir şablonlamadır. Statik YAML'da image etiketi veya replika sayısı değiştiğinde her dosyayı elle düzenlemek gerekir. Helm ise Go template sözdizimiyle değişkenleri `values.yaml` dosyasından alır. Örneğin teorik olarak bir Deployment içindeki replika sayısı şöyle modellenebilir:

$$Replicas_{ortam} = Values[replicaCount]$$

Bu basit denklem, ortam bazlı farkların şablonun kendisinden değil, dışarıdan verilen değerlerden gelmesini sağlar. Böylece altyapı tanımı tekrar eden kopyalar yerine parametrik bir yapıya kavuşur.

| Kavram | Görevi | Örnek |
|---|---|---|
| Chart | Uygulama paketinin tarifi | `web-api` chart'ı |
| Template | Değişken içeren YAML şablonu | `templates/deployment.yaml` |
| Values | Şablona verilen yapılandırma | `replicaCount: 3` |
| Release | Kümeye kurulmuş chart örneği | `web-api-prod` |
| Repository | Chart paketlerinin kaynağı | Bitnami deposu |

Yeni bir chart oluşturmak için `helm create` komutu kullanılabilir:

```bash
helm create web-api
cd web-api
```

Bu komut; `Chart.yaml`, `values.yaml` ve `templates/` dizinini içeren başlangıç iskeletini üretir. `Chart.yaml` paketin adı ve sürümü gibi bilgileri saklarken, `values.yaml` varsayılan değerlerin evidir. Aşağıdaki parça, Deployment şablonunda kullanıcı tanımlı değerlerin nasıl kullanıldığını gösterir:

{% raw %}

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "web-api.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
        - name: web-api
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: {{ .Values.service.port }}
```

{% endraw %}

Burada `{{ .Values.image.tag }}` ifadesi, gerçek bir YAML değeri değil, Helm'in kurulum sırasında çözeceği bir yer tutucudur. Ortama özel bir dosya hazırlamak oldukça pratiktir:

```yaml
# values-production.yaml
replicaCount: 4
image:
  repository: registry.example.com/web-api
  tag: "2.4.0"
service:
  port: 8080
```

Kurulum komutu bu değerleri şablonla birleştirir:

```bash
helm upgrade --install web-api-prod ./web-api \
  --namespace production --create-namespace \
  -f values-production.yaml
```

`upgrade --install` yaklaşımı özellikle CI/CD boru hatlarında değerlidir: Release yoksa kurar, varsa günceller. Ancak Helm'in güçlü olması, kontrolsüz kullanılabileceği anlamına gelmez. Yayın öncesinde oluşturulacak manifestleri görmek için `helm template`, şablon sorunlarını bulmak için de `helm lint` çalıştırılmalıdır.

| İşlem | Düz YAML | Helm |
|---|---|---|
| Ortam farkı | Dosya kopyalama eğilimi | Ayrı values dosyaları |
| Sürümleme | Git disipliniyle manuel takip | Release geçmişiyle takip |
| Geri alma | Manifestleri yeniden uygulama | `helm rollback` |
| Paylaşım | Dosya klasörü paylaşımı | Chart repository |

Son olarak Secret verilerini doğrudan `values.yaml` içine koymak risklidir; bu dosyalar çoğunlukla Git'e girer. SOPS, External Secrets veya CI/CD gizli değişkenleriyle entegrasyon tercih edilmelidir. Helm, Kubernetes'i sihirli biçimde basitleştirmez; fakat tekrar eden dağıtım bilgisini paketleyerek YAML ormanını yönetilebilir bir bahçeye dönüştürür.

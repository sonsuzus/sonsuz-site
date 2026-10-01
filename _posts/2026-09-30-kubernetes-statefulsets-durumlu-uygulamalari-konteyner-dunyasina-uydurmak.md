---
layout: post
title: "Kubernetes StatefulSets: Durumlu Uygulamaları Konteyner Dünyasına Uydurmak"
math: true
categories: 
  - Bilgi
tags: 
  - kubernetes
  - statefulset
  - veritabanı
  - devops
  - kalıcı-depolama
  - konteyner
toc: true
image: /img/kubernetes-statefulsets-durumlu-18.png
---

Konteynerler geçici doğalarıyla ünlüdür: kapanır, yeniden oluşturulur ve hiçbir şey olmamış gibi hayatlarına devam ederler. Ancak PostgreSQL, MongoDB veya Kafka gibi sistemler için “hiçbir şey olmamış gibi” davranmak, verilerin gerçekten kaybolduğu anlamına gelebilir. Kubernetes StatefulSet, bu çelişkiyi kararlı ağ kimlikleri, sıralı yönetim ve kalıcı disklerle çözerek durumlu uygulamaları konteyner dünyasına uydurur.

``

## Deployment Neden Her Zaman Yeterli Değildir?

Bir Deployment tarafından yönetilen pod’lar birbirinin yerine geçebilir. `web-7d8f` silindiğinde yerine farklı isim ve IP adresine sahip başka bir pod gelebilir. Trafiği dağıtan stateless bir web sunucusu için bu davranış idealdir; fakat bir veritabanı kümesinde her üyenin rolü, diski ve ağ kimliği önemlidir.

StatefulSet ise pod’lara sıralı ve kararlı kimlikler verir:

- `postgres-0`
- `postgres-1`
- `postgres-2`

Pod yeniden oluşturulsa bile adı değişmez. Headless Service kullanıldığında `postgres-0.db.default.svc.cluster.local` gibi tahmin edilebilir DNS kayıtları elde edilir.

| Özellik | Deployment | StatefulSet |
|---|---|---|
| Pod kimliği | Geçici | Kararlı ve sıralı |
| Başlatma/silme | Paralel olabilir | Varsayılan olarak sıralı |
| Disk ilişkisi | Ortak veya bağımsız | Her pod’a özel PVC |
| Uygun senaryo | Web API, worker | Veritabanı, Kafka, ZooKeeper |

## Kalıcılığın Matematiği

Bir sistemin gözlenen toplam durumu kabaca şöyle düşünülebilir:

$$S_{toplam} = S_{disk} + S_{kimlik} + S_{küme}$$

Yalnızca diski korumak yeterli değildir. Bir veritabanı düğümü kendi verisini bulsa bile kümedeki eski rolünü veya ağ kimliğini bulamıyorsa güvenli biçimde çalışamayabilir. StatefulSet, $S_{kimlik}$ bileşenini; PersistentVolume ise $S_{disk}$ bileşenini korur. Uygulamanın replikasyon protokolü de $S_{küme}$ kısmından sorumludur.

## Temel Bir StatefulSet Örneği

Aşağıdaki yapılandırma, üç adet Nginx pod’u oluşturur. Nginx burada kavramı sade göstermek için kullanılıyor; aynı model uygun ayarlarla veritabanlarına uygulanabilir.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  clusterIP: None
  selector:
    app: web
  ports:
    - port: 80
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: web
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
          volumeMounts:
            - name: data
              mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 2Gi
```

`clusterIP: None`, servisi headless hâle getirir ve pod’ların ayrı DNS kimlikleriyle keşfedilmesini sağlar. `volumeClaimTemplates` ise her pod için farklı bir PersistentVolumeClaim üretir: `data-web-0`, `data-web-1` ve `data-web-2`. Pod silinse bile PVC varsayılan olarak korunur; geri gelen pod kendi diskine yeniden bağlanır.

## Sıralama, Ölçekleme ve Güvenlik

StatefulSet pod’ları varsayılan `OrderedReady` politikasıyla küçük numaradan büyüğe doğru başlatır; silerken ters sırayı izler. Bu yaklaşım lider ve takipçi ilişkisi bulunan kümelerde önemlidir. Bağımsız çalışan durumlu işler için `podManagementPolicy: Parallel` seçilebilir, ancak hız uğruna uygulamanın başlangıç varsayımları bozulmamalıdır.

Kalıcı depolama tek başına yedekleme değildir. Disk bozulabilir, bölge erişilemez olabilir veya hatalı bir sorgu tüm kayıtları silebilir. Üretimde şu önlemler birlikte düşünülmelidir:

1. StorageClass ve genişletme desteğini doğrulayın.
2. Düzenli snapshot ve uygulama seviyesinde yedek alın.
3. Pod anti-affinity ile replikaları farklı düğümlere dağıtın.
4. PodDisruptionBudget ile aynı anda fazla üyenin kapanmasını engelleyin.
5. Güncelleme ve geri dönüş senaryolarını test edin.

StatefulSet sihirli bir “veritabanını güvenli yap” düğmesi değildir; Kubernetes ile durumlu yazılım arasında yapılan sağlam bir kimlik ve depolama sözleşmesidir. Uygulamanın replikasyon mantığı, doğru disk sınıfı ve gerçek bir felaket kurtarma planıyla birleştiğinde konteynerlerin geçiciliği artık korkutucu değil, yönetilebilir olur.

![kubernetes-statefulsets-durumlu-18](/img/kubernetes-statefulsets-durumlu-18.svg)


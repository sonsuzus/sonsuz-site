---
layout: post
title: "Kubernetes'te CRD ve Operator: Kendi K8s Nesnenizi Yaratın"
math: true
categories: 
  - Bilgi
tags: 
  - kubernetes
  - crd
  - operator
  - devops
  - cloud-native
  - go
toc: true
image: /img/kuberneteste-crd-ve-33.png
---

![kuberneteste-crd-ve-33](/img/kuberneteste-crd-ve-33.svg)


Kubernetes yalnızca Pod, Service veya Deployment yönetmek zorunda değildir. API sunucusuna yeni bir nesne türü tanıtarak veritabanını, mesaj kuyruğunu hatta şirketinize özgü iş yükünü standart bir Kubernetes kaynağı gibi yönetebilirsiniz. Bunun anahtarı **Custom Resource Definition (CRD)**, otomasyon tarafındaki yardımcısı ise **Operator** desenidir.

``

## CRD tam olarak nedir?

Kubernetes API'sindeki her kaynak, istenen durumu bildiren bir belgedir. Örneğin Deployment için “üç kopya çalışsın” deriz; ilgili controller mevcut durum ile istenen durum arasındaki farkı kapatır. CRD ise API'ye yeni bir kaynak şeması ekler.

Temel kontrol döngüsünü şöyle düşünebiliriz:

$$
Hata = İstenen\ Durum - Mevcut\ Durum
$$

Controller bu hatayı mümkün olduğunca sıfıra yaklaştırmaya çalışır. CRD yalnızca yeni nesnenin dilbilgisini tanımlar; nesneyi gerçekten yöneten kod ise Operator veya özel controller'dır.

| Kavram | Görevi | Örnek |
|---|---|---|
| CRD | Yeni API türünü ve şemasını tanımlar | `Database` |
| Custom Resource | CRD'ye göre oluşturulan gerçek nesnedir | `customer-db` |
| Controller | Kaynakları izleyip uzlaştırma yapar | Pod oluşturur |
| Operator | Controller'a alan bilgisi ekler | Yedekleme ve yükseltme yapar |

## İlk özel kaynağımızı tanımlayalım

Aşağıdaki CRD, `example.com/v1` altında `Database` isimli yeni bir kaynak oluşturur. Kullanıcılar motoru, sürümü ve replika sayısını `spec` bölümünde belirtebilir:

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.example.com
spec:
  group: example.com
  scope: Namespaced
  names:
    plural: databases
    singular: database
    kind: Database
    shortNames: [db]
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              required: [engine, replicas]
              properties:
                engine:
                  type: string
                  enum: [postgres, mysql]
                version:
                  type: string
                replicas:
                  type: integer
                  minimum: 1
            status:
              type: object
              properties:
                readyReplicas:
                  type: integer
      subresources:
        status: {}
```

Dosyayı `kubectl apply -f database-crd.yaml` ile yükledikten sonra Kubernetes artık `kubectl get databases` komutunu anlayacaktır. Ardından özel kaynağımızı oluşturabiliriz:

```yaml
apiVersion: example.com/v1
kind: Database
metadata:
  name: customer-db
spec:
  engine: postgres
  version: "16"
  replicas: 3
```

Bu belge tek başına PostgreSQL başlatmaz. Kubernetes nesneyi saklar ve doğrular; fakat talimatları uygulayacak bir controller henüz yoktur. Aşçı olmadan sipariş fişinin mutfağa düşmesi gibi!

## Operator nasıl çalışır?

Operator, `Database` nesnelerini izleyen sürekli bir **reconciliation** döngüsü çalıştırır. Go ekosisteminde Kubebuilder veya Operator SDK bu yapıyı üretmeyi kolaylaştırır. Basitleştirilmiş bir uzlaştırma akışı şöyledir:

```go
func (r *DatabaseReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var db Database
    if err := r.Get(ctx, req.NamespacedName, &db); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    desired := buildStatefulSet(db)
    if err := controllerutil.SetControllerReference(&db, desired, r.Scheme); err != nil {
        return ctrl.Result{}, err
    }

    err := upsertStatefulSet(ctx, r.Client, desired)
    return ctrl.Result{RequeueAfter: time.Minute}, err
}
```

Kod, özel kaynağı okur, beklenen StatefulSet'i üretir ve sahiplik ilişkisini kurar. `SetControllerReference` sayesinde Database silindiğinde bağlı kaynaklar çöp toplama mekanizmasıyla kaldırılabilir.

## Sağlam bir Operator için püf noktaları

Reconciliation işlemi **idempotent** olmalıdır: aynı işlem defalarca çalıştığında sonuç değişmemelidir. `status` alanı gerçek durumu kullanıcıya göstermeli, `spec` ise kullanıcının niyetini korumalıdır. Silme öncesinde harici yedekleri veya bulut kaynaklarını temizlemek gerekiyorsa **finalizer** kullanılmalıdır.

Ayrıca Operator'a yalnızca gerekli kaynaklar için RBAC izinleri verin. Sürüm geçişlerinde `v1alpha1`, `v1beta1` ve `v1` aşamalarını planlayın; şema değişiklikleri için conversion webhook değerlendirin. Böylece CRD basit bir API eklentisinden çıkar, veritabanı operasyon bilgisini kodlayan güvenilir bir otomasyon ürününe dönüşür.

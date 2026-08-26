---
layout: post
title: "Kubernetes Operatörleriyle Karmaşık Uygulamaları Otomatik Yönetmek"
math: true
categories: 
  - Program
tags: 
  - kubernetes
  - operatör
  - go
  - otomasyon
  - devops
---

Kubernetes, konteynerleri çalıştırma işini oldukça iyi yapar; ancak veritabanı kümesi kurmak, yedek almak, sürüm yükseltmek veya arızalı bir düğümü güvenle değiştirmek gibi uygulamaya özgü işler daha fazla bilgi ister. Kubernetes Operatörü tam burada devreye girer: Bir uzmanın operasyonel bilgisini kodlayarak uygulamanın yaşam döngüsünü sürekli yöneten özel bir denetleyici oluşturur. Kısacası Operatör, YAML dosyalarınızın yanında nöbet tutan, yorulmayan bir SRE yardımcısıdır.
``

Operatör deseninin temelinde **bildirimsel durum yönetimi** bulunur. Kullanıcı bir kaynağın ulaşmasını istediği durumu `spec` alanında tanımlar; Operatör ise kümenin gerçek durumunu gözler ve hedefe yaklaşmak için işlemler yapar. Bu mantık, Kubernetes'in yerleşik Deployment denetleyicisinden tanıdıktır. Fark şudur: Deployment pod sayısını yönetirken, sizin Operatörünüz örneğin PostgreSQL replikasyonu, sertifika yenileme ya da özel bir iş kuyruğu topolojisini yönetebilir.

Teorik olarak denetleyicinin hedefi, arzu edilen durum ($D$) ile mevcut durum ($A$) arasındaki farkı azaltmaktır:

$$e = D - A$$

Her **reconcile** döngüsünde denetleyici bu hatayı gözlemler ve uygun eylemi seçer. İyi tasarlanmış bir reconcile fonksiyonu **idempotent** olmalıdır: Aynı istek tekrar işlense bile sistem gereksiz veya zararlı yeni bir değişiklik üretmemelidir. Ağ hataları, yeniden başlatmalar ve olayların birden fazla kez gelmesi Kubernetes dünyasında istisna değil, günlük rutindir.

| Kavram | Ne tanımlar? | Örnek |
|---|---|---|
| CRD (CustomResourceDefinition) | Kubernetes API'sine eklenen yeni kaynak türü | `DatabaseCluster` |
| CR (Custom Resource) | Bu türün kullanıcının oluşturduğu örneği | `production-db` |
| Controller | Kaynağı izleyip durumu uzlaştıran yazılım | Go ile yazılmış reconciler |
| Operator | Uygulama operasyon bilgisini taşıyan controller paketi | Yedekleme ve failover yöneticisi |

Örneğin kullanıcı, üç replikalı bir veritabanı kümesini şöyle isteyebilir:

```yaml
apiVersion: data.example.io/v1alpha1
kind: DatabaseCluster
metadata:
  name: production-db
spec:
  replicas: 3
  version: "16"
  backupSchedule: "0 2 * * *"
```

Bu YAML yalnızca niyeti açıklar. Operatör bunun karşılığında StatefulSet, Service, Secret, PVC ve gerekirse CronJob kaynaklarını oluşturur. Ayrıca `status` alanına hazır replikaları, gözlenen sürümü ve son yedekleme zamanını yazar. Böylece kullanıcı, altyapı ayrıntılarını takip etmek yerine ürün ihtiyacına odaklanır.

Go ve `controller-runtime` ile bir reconcile iskeleti kabaca şöyledir:

```go
func (r *DatabaseClusterReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var db DatabaseCluster
    if err := r.Get(ctx, req.NamespacedName, &db); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    sts := desiredStatefulSet(&db)
    if err := controllerutil.SetControllerReference(&db, sts, r.Scheme); err != nil {
        return ctrl.Result{}, err
    }

    if err := r.Client.Patch(ctx, sts, client.Apply, client.FieldOwner("db-operator")); err != nil {
        return ctrl.Result{}, err
    }
    return ctrl.Result{}, r.updateStatus(ctx, &db)
}
```

Bu kod, önce özel kaynağı okur, sonra hedef StatefulSet'i üretir ve **server-side apply** ile kümeye uygular. `SetControllerReference`, sahiplik ilişkisini kurar; özel kaynak silindiğinde Kubernetes'in garbage collector mekanizması bağlı kaynakları da temizleyebilir. Gerçek bir Operatörde buna sürüm geçişleri, health check'ler, olay kayıtları ve hata durumunda kontrollü yeniden deneme eklenir.

| Yaklaşım | Güçlü yönü | Sınırı |
|---|---|---|
| Helm chart | Hızlı kurulum ve paketleme | Çalışma zamanında karar verme sınırlıdır |
| Script/CI işi | Basit tek seferlik otomasyon | Sürekli durum gözlemi yapmaz |
| Operatör | Güncel duruma göre sürekli otomasyon | Geliştirme ve test maliyeti yüksektir |

Başlangıçta küçük kalın: Tek bir CRD, net bir `spec`, anlamlı bir `status` ve güvenilir bir reconcile döngüsü tasarlayın. RBAC izinlerini minimumda tutun, silme işlemleri için finalizer kullanın ve metriklerle gözlemlenebilirlik ekleyin. Operatör yazmak sadece kaynak oluşturmak değildir; başarısızlıkları, kısmi durumları ve gelecekteki yükseltmeleri de tasarlamaktır. Bu disiplin oturduğunda, karmaşık uygulamalarınız Kubernetes üzerinde gerçekten kendi kendini yöneten sistemlere dönüşür.

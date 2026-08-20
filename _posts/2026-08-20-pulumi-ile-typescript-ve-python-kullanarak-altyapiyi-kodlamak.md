---
layout: post
title: "Pulumi ile TypeScript ve Python Kullanarak Altyapıyı Kodlamak"
math: true
categories: 
  - Program
tags: 
  - Pulumi
  - Infrastructure as Code
  - TypeScript
  - Python
  - Bulut
---

Bulut altyapısı artık yalnızca kontrol panelinde tıklanarak yönetilen kaynaklar bütünü değildir. Sunucular, depolama alanları, ağ kuralları ve veritabanları; yazılımın kendisi kadar tekrar üretilebilir, gözden geçirilebilir ve test edilebilir olmalıdır. Pulumi, bu yaklaşımı genel amaçlı dillerle birleştiren bir Infrastructure as Code (IaC) aracıdır. TypeScript veya Python ile AWS, Azure, Google Cloud ya da Kubernetes kaynaklarını bildirimsel biçimde tanımlayabilir; bu tanımları Git deposunda uygulama kodunuzla birlikte sürümlendirebilirsiniz.

``

Klasik IaC araçlarında genellikle araca özgü bir yapılandırma dili kullanılır. Pulumi ise kaynakların **istenen son durumunu** tanımlarken JavaScript/TypeScript, Python, Go, C# veya Java gibi dillerin koşul, döngü, fonksiyon, sınıf ve paket yönetimi özelliklerini kullanır. Buradaki önemli fikir şudur: Kodunuz kaynakları sırayla oluşturan basit bir betik gibi görünse de Pulumi, çalıştırma sırasında bağımlılık grafiği üretir ve sağlayıcı API'lerine uygulanacak değişiklikleri hesaplar.

Bu süreci basitleştirerek şöyle ifade edebiliriz:

$$\text{Yeni Durum} = \text{İstenen Tanım} - \text{Mevcut Durum}$$

Pulumi bu farkı bir **plan** olarak gösterir. `pulumi preview` ile gerçek ortamı değiştirmeden önce nelerin ekleneceğini, güncelleneceğini veya silineceğini denetlersiniz. `pulumi up` komutu ise onaylanan planı uygular. Böylece "konsolda kim neyi değiştirdi?" gizemi yerini kayıtlı ve tekrarlanabilir bir sürece bırakır.

| Yaklaşım | Güçlü yönü | Dikkat edilmesi gereken |
|---|---|---|
| Bulut konsolu | Hızlı deneme ve görsel kullanım | Manuel değişiklikler izlenmesi zor olabilir |
| Şablon tabanlı IaC | Sade ve deklaratif yapı | Karmaşık mantıkta ifade gücü sınırlanabilir |
| Pulumi | Genel amaçlı dil, modülerlik, test edilebilirlik | Dil bağımlılıkları ve state yönetimi öğrenilmelidir |

Örneğin aşağıdaki TypeScript kodu AWS üzerinde bir S3 bucket tanımlar. Kodun kısa olması, arka planda yalnızca bir API çağrısı yapıldığı anlamına gelmez: Pulumi kaynak kimliğini, özelliklerini ve bağımlılıklarını state dosyasında izler.

```typescript
import * as aws from "@pulumi/aws";

const assets = new aws.s3.Bucket("uygulama-varliklari", {
  tags: {
    Environment: "dev",
    ManagedBy: "pulumi"
  }
});

export const bucketName = assets.id;
```

`Bucket` nesnesi istenen kaynağı temsil eder; `export` edilen değer ise deployment sonunda başka sistemlerde kullanılabilecek bir çıktıdır. Örneğin bir CI/CD işi bu bucket adını alıp derlenmiş ön yüz dosyalarını yükleyebilir. Pulumi'nin `Output<T>` modeli de burada önemlidir: Bulutta oluşturulacak bir kaynağın değeri henüz bilinmiyorsa, bu değer normal bir string değil, gelecekte çözümlenecek bağımlı bir çıktı olarak ele alınır.

Python tarafında aynı fikir, dilin sade sözdizimiyle uygulanabilir. Aşağıdaki örnek bir güvenlik grubu oluşturur ve yalnızca HTTPS trafiğine izin verir:

```python
import pulumi
import pulumi_aws as aws

web_sg = aws.ec2.SecurityGroup(
    "web-security-group",
    description="HTTPS erişimi için güvenlik grubu",
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        protocol="tcp",
        from_port=443,
        to_port=443,
        cidr_blocks=["0.0.0.0/0"],
    )],
)

pulumi.export("security_group_id", web_sg.id)
```

Bu tanımda bildirimsel kısım, 443 portuna izin veren bir güvenlik grubu **istediğinizi** söylemenizdir. Pulumi'nin görevi, mevcut ortamda bu sonuca ulaşmak için gerekli oluşturma veya güncelleme işlemlerini belirlemektir. İdempotentlik hedefi kabaca şöyle düşünülebilir: $apply(desired, desired) \approx no\ change$. Aynı tanımı tekrar uyguladığınızda gereksiz kaynak üretimi beklenmez.

Versiyon kontrolü Pulumi kullanımının en değerli parçalarından biridir. Her altyapı değişikliği pull request ile incelenebilir; ekip arkadaşları `preview` çıktısını değerlendirebilir ve geri alma işlemi Git geçmişi üzerinden daha güvenli planlanabilir. Ancak gizli anahtarları doğrudan kaynak koduna koymamalısınız. Pulumi Secrets, şifrelenmiş yapılandırma değerleri ve CI/CD ortam değişkenleri bu iş için kullanılmalıdır.

| Pratik | Neden önemlidir? |
|---|---|
| Küçük ve modüler stack'ler | Geliştirme, test ve üretim ortamlarını ayırır |
| `pulumi preview` zorunluluğu | Yıkıcı değişiklikleri uygulamadan yakalar |
| Kaynak etiketleri | Maliyet, sahiplik ve ortam takibini kolaylaştırır |
| Secret yönetimi | Parola ve token sızıntısı riskini azaltır |

Sonuç olarak Pulumi, altyapıyı uygulama geliştirme alışkanlıklarına yaklaştırır. TypeScript'in tip sistemi veya Python'ın okunabilirliği sayesinde bulut kaynakları; test edilebilir fonksiyonlara, tekrar kullanılabilir bileşenlere ve denetlenebilir Git değişikliklerine dönüşür. Tıklamalarla büyüyen altyapı yerine, kodla açıklanabilen bir sistem kurmanın oldukça güçlü bir yoludur.

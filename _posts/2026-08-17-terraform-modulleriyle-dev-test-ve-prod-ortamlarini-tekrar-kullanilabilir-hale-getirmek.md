---
layout: post
title: "Terraform Modülleriyle Dev, Test ve Prod Ortamlarını Tekrar Kullanılabilir Hale Getirmek"
math: true
categories: 
  - Bilgi
tags: 
  - terraform
  - ınfrastructure as code
  - devops
---

Bulut altyapısını elle yönetmek, ilk birkaç sunucuda masum görünür; fakat dev, test ve prod ortamları çoğaldıkça aynı güvenlik grubu, ağ ve veritabanı ayarlarını kopyalamak hızla bir bakım kabusuna dönüşür. Terraform modülleri bu sorunu, altyapı bileşenlerini parametre alan küçük ve tekrar kullanılabilir paketlere dönüştürerek çözer. Böylece ekipler aynı mimari standardı her ortamda korurken, yalnızca ortama özgü değerleri değiştirir.

``

## Modül düşüncesinin teorik temeli

Terraform'da **root module**, komutları çalıştırdığınız ana dizindir. Bir klasör içindeki her Terraform yapılandırması teknik olarak modüldür; ancak yaygın kullanımda modül denince root module tarafından çağrılan, belirli bir sorumluluğa sahip alt klasörler anlaşılır. Örneğin bir `network` modülü VPC, subnet ve route table oluştururken; `application` modülü uygulama sunucularını oluşturabilir.

Bu yaklaşım yazılımdaki **soyutlama** ve **DRY (Don't Repeat Yourself)** ilkelerinin altyapıdaki karşılığıdır. Ortam başına kopyalanan kaynak sayısı $n$, aynı yapının güncellenme maliyeti ise $c$ olsun. Kopyala-yapıştır modelinde değişiklik maliyeti kabaca $n \times c$ olur. Ortak modül kullanıldığında bu maliyet çoğu zaman $c + n \times v$ seviyesine iner; burada $v$, yalnızca ortam değişkenlerini yönetmenin düşük maliyetidir.

| Yaklaşım | Avantaj | Risk |
|---|---|---|
| Ortam başına kopya `.tf` dosyaları | Başlangıçta hızlı görünür | Konfigürasyon sapması ve zor bakım |
| Tek, devasa yapılandırma | Tüm kaynaklar görünür | Ortam ayrımı ve yetkilendirme zorlaşır |
| Modül + ortam kök dizinleri | Standart, tekrar kullanım ve net sınırlar | Modül arayüzü tasarımı gerektirir |

## Önerilen klasör yapısı

Yaygın ve anlaşılır bir düzen, ortak modülleri `modules` altında; her ortamın çağırıcı yapılandırmasını ise `environments` altında tutmaktır:

```text
terraform/
├── modules/
│   ├── network/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── application/
└── environments/
    ├── dev/
    ├── test/
    └── prod/
```

`network` modülü, değişkenlerle esnek fakat davranış olarak öngörülebilir olmalıdır. Aşağıdaki örnekte CIDR bloğu, ortam etiketi ve subnet sayısı dışarıdan alınır. Kodun görevi, ağ bileşenlerini aynı şablona göre üretmektir.

```hcl
# modules/network/main.tf
resource "aws_vpc" "this" {
  cidr_block = var.vpc_cidr

  tags = {
    Name        = "${var.project}-${var.environment}-vpc"
    Environment = var.environment
  }
}

resource "aws_subnet" "private" {
  count             = var.subnet_count
  vpc_id            = aws_vpc.this.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
}
```

`cidrsubnet` kullanımı, ana ağ bloğunu daha küçük bloklara ayırır. Örneğin `/16` bir VPC için eklenen $8$ bit, teorik olarak $2^8 = 256$ adet `/24` alt ağ üretme kapasitesi sağlar. Elbette gerçek tasarımda IP planı, kullanılabilir zone sayısı ve büyüme beklentisi birlikte değerlendirilmelidir.

## Ortamlar yalnızca değer sağlamalı

Dev ortamı modülün nasıl çalıştığını yeniden tanımlamamalı; ona hangi değerlerle çalışacağını söylemelidir. Bu ayrım, prod'a geçerken mimariyi yanlışlıkla değiştirme olasılığını azaltır.

```hcl
# environments/dev/main.tf
module "network" {
  source       = "../../modules/network"
  project      = "shop"
  environment  = "dev"
  vpc_cidr     = "10.10.0.0/16"
  subnet_count = 2
}
```

| Özellik | Dev | Test | Prod |
|---|---:|---:|---:|
| Subnet sayısı | 2 | 2 | 3 |
| Kaynak boyutu | Küçük | Orta | Yüksek |
| Silme koruması | Genellikle kapalı | Tercihe bağlı | Açık |
| State erişimi | Geliştirici ekibi | QA/DevOps | Sınırlı DevOps |

Her ortam için ayrı bir remote state kullanmak kritik bir güvenlik ve eşzamanlılık önlemidir. Örneğin farklı S3 anahtarları veya Terraform Cloud workspace'leri seçilebilir. `prod` state dosyasını `dev` ile paylaşmak, yanlış `apply` komutunun üretim kaynaklarını değiştirmesine davetiye çıkarır.

Son olarak modülleri sürümlendirin: Git etiketi, private registry veya güvenilir bir modül kaynağı kullanın. `terraform fmt`, `validate`, `plan` ve onaylı `apply` adımlarını CI/CD hattına ekleyin. Böylece modüler Terraform yalnızca daha az kod değil; denetlenebilir, tutarlı ve büyümeye hazır bir altyapı sözleşmesi haline gelir.

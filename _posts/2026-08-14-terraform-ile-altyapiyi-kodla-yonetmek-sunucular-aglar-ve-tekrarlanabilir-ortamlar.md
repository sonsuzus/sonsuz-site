---
layout: post
title: "Terraform ile Altyapıyı Kodla Yönetmek: Sunucular, Ağlar ve Tekrarlanabilir Ortamlar"
math: true
categories: 
  - Bilgi
tags: 
  - terraform
  - ınfrastructure as code
  - devops
image: /img/terraform-ile-altyapiyi-88.png
---

Bir sunucuyu panelden tek tek oluşturmak, ağ kurallarını elle yazmak ve hangi ayarın nerede değiştiğini hatırlamaya çalışmak; küçük projelerde bile hızla yorucu hâle gelir. **Infrastructure as Code (IaC)** yaklaşımı, altyapıyı Terraform dosyalarında tanımlayarak bu süreci yazılım geliştirmeye benzetir: değişiklikler sürüm kontrolüne girer, gözden geçirilir ve aynı ortam tekrar tekrar üretilebilir.
``
Terraform, HashiCorp tarafından geliştirilen bildirimsel bir IaC aracıdır. Bildirimsel yaklaşımda “önce şu API çağrısını yap, sonra bunu çalıştır” demezsiniz; ulaşmak istediğiniz **nihai durumu** tarif edersiniz. Terraform ise mevcut altyapıyı okuyup hedef durumla karşılaştırır ve aradaki farkı kapatacak işlemleri planlar.

Bu mantığı basitçe şöyle düşünebiliriz:

$$\text{Değişiklik Kümesi} = \text{İstenen Durum} - \text{Mevcut Durum}$$

Örneğin yapılandırmada bir sanal ağ, bir alt ağ ve bir sunucu tanımlıysa; Terraform bunların yokluğunu algılar ve oluşturulacak kaynakları planına ekler. Sunucu zaten varsa, gereksiz yere yeniden yaratmak yerine yalnızca değişen alanlara odaklanır. Bu davranış, **idempotency** olarak bilinir: aynı tanımı tekrar uygulamak, altyapıyı her seferinde beklenmedik biçimde değiştirmez.

## Terraform'ın Temel Parçaları

Terraform projeleri çoğunlukla `.tf` uzantılı HCL (HashiCorp Configuration Language) dosyalarından oluşur. Kaynak sağlayıcıları AWS, Azure, Google Cloud veya Kubernetes gibi platformların API'leriyle iletişim kurar. Terraform'un yerel belleği ise oluşturduğu kaynakların kimliklerini ve ilişkilerini `terraform.tfstate` dosyasında tutar.

| Kavram | Görevi | Günlük Hayattan Benzetme |
|---|---|---|
| Provider | Bulut platformunun API'sine bağlanır | Tedarikçi firma |
| Resource | Oluşturulacak somut nesnedir | Sipariş edilen ürün |
| Variable | Tekrar kullanılabilir girdi sağlar | Sipariş formundaki seçenek |
| State | Bilinen altyapı durumunu saklar | Envanter defteri |
| Output | Oluşan önemli bilgileri gösterir | Teslimat makbuzu |

Aşağıdaki örnek, AWS üzerinde bir ağ ve bu ağ içinde bir EC2 sunucusu tanımlar. Gerçek kullanımda erişim anahtarları dosyaya yazılmamalı; ortam değişkenleri, IAM roller veya güvenli gizli bilgi servisleri tercih edilmelidir.

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}

resource "aws_vpc" "uygulama" {
  cidr_block = "10.20.0.0/16"

  tags = {
    Name = "uygulama-vpc"
  }
}

resource "aws_subnet" "web" {
  vpc_id            = aws_vpc.uygulama.id
  cidr_block        = "10.20.1.0/24"
  availability_zone = "eu-central-1a"
}

resource "aws_instance" "web" {
  ami           = "ami-1234567890abcdef0"
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.web.id

  tags = {
    Name = "web-sunucusu"
  }
}
```

Burada `aws_instance.web`, `aws_subnet.web.id` değerini kullandığı için Terraform bağımlılığı otomatik algılar. Yani önce VPC, ardından alt ağ, en son sunucu oluşturulur. Bu özellik, karmaşık altyapılarda işlem sırasını elle takip etme ihtiyacını azaltır.

## Güvenli Uygulama Döngüsü

Terraform ile çalışmanın klasik akışı üç komuttan oluşur:

```bash
terraform init      # Provider eklentilerini indirir
terraform plan      # Yapılacak değişiklikleri önizler
terraform apply     # Onay sonrası planı uygular
```

| Komut | Etki | Ne zaman kullanılmalı? |
|---|---|---|
| `init` | Çalışma dizinini hazırlar | Yeni proje veya provider değişikliği |
| `plan` | Değişiklikleri sadece gösterir | Her uygulamadan önce |
| `apply` | Kaynakları oluşturur/değiştirir | Plan incelendikten sonra |
| `destroy` | Yönetilen kaynakları siler | Test ortamını kapatırken |

`plan` çıktısı özellikle önemlidir: yanlış bölge, beklenmeyen silme işlemi veya maliyetli bir kaynak hemen fark edilebilir. Ekip çalışmalarında state dosyasını yerel bilgisayarda bırakmak yerine S3 gibi uzak bir backend'de, kilitleme mekanizmasıyla saklamak gerekir. Böylece iki kişinin aynı anda altyapıyı değiştirmesiyle oluşabilecek çakışmalar önlenir.

Terraform, altyapıyı sihirli biçimde hatasız yapmaz; fakat altyapı kararlarını görünür, denetlenebilir ve tekrarlanabilir kılar. Küçük bir VPC ile başlayıp modüller, uzak state ve CI/CD doğrulamaları ekledikçe, sunucu kurma süreci kişisel bir bilgi olmaktan çıkar; ekibin güvenle çalıştırabildiği bir yazılım sürecine dönüşür.

![terraform-ile-altyapiyi-88](/img/terraform-ile-altyapiyi-88.svg)


---
layout: post
title: "Terraform State Yönetimi: Çakışmaları ve Gizli Bilgi Sızıntılarını Önlemek"
math: true
categories: 
  - Bilgi
tags: 
  - terraform
  - iac
  - devops
  - bulut
  - güvenlik
  - state-yönetimi
toc: true
image: /img/terraform-state-yonetimi-38.png
---

Terraform ile birkaç kaynak oluşturmak kolaydır; asıl macera aynı altyapıyı bir ekip yönetmeye başladığında ortaya çıkar. Terraform State dosyası, tanımladığımız kod ile bulutta gerçekten bulunan kaynaklar arasındaki köprüdür. Ancak yanlış saklanan veya eş zamanlı güncellenen bir State, altyapıyı otomatikleştiren dostumuzun kısa sürede kaos makinesine dönüşmesine neden olabilir.
``

## State dosyası neden vardır?

Terraform, `main.tf` içindeki yapılandırmayı doğrudan bulut ortamıyla karşılaştırmak yerine kaynakların bilinen son durumunu State içerisinde tutar. Böylece bir kaynağın kimliğini, özelliklerini ve bağımlılıklarını izleyebilir.

Bu ilişkiyi basitleştirirsek:

$$
Değişiklik = İstenen\ Durum - Bilinen\ Durum
$$

Buradaki “bilinen durum” State dosyasından gelir. State kaybolur veya gerçeği yansıtmazsa Terraform mevcut bir kaynağı yeni sanabilir, gereksiz yere değiştirebilir ya da yeniden oluşturmaya çalışabilir.

Yerel kullanımda dosya genellikle `terraform.tfstate` adıyla çalışma dizininde bulunur. Tek geliştiricili denemelerde bu yöntem kabul edilebilir; ekip çalışmalarında ise ciddi risk taşır.

| Risk | Yerel State | Uzak State |
|---|---|---|
| Takım erişimi | Dosya paylaşımı gerekir | Merkezi erişim sağlanır |
| Eş zamanlı işlem | Çakışma olasılığı yüksek | Kilitleme uygulanabilir |
| Yedekleme | Kullanıcıya bağlıdır | Sürümleme kullanılabilir |
| Yetkilendirme | Dosya sistemiyle sınırlıdır | IAM politikaları uygulanır |
| Denetim | Zordur | Erişim kayıtları tutulabilir |

## Birinci tehlike: Eş zamanlı değişiklikler

İki geliştirici aynı anda `terraform apply` çalıştırırsa her ikisi de eski State üzerinden karar verebilir. Son yazan işlem diğerinin değişikliklerini ezebilir. Teorik olarak çakışma olasılığını şöyle düşünebiliriz:

$$
Risk \propto Eşzamanlı\ İşlem\ Sayısı \times İşlem\ Süresi
$$

Çözüm, uzak backend ile birlikte **State locking** kullanmaktır. Kilidi alan işlem tamamlanana kadar diğer işlemler bekler veya hata alır. AWS S3, Azure Blob Storage, Google Cloud Storage ve HCP Terraform gibi seçenekler sağlayıcıya özgü eş zamanlılık mekanizmaları sunar.

Örneğin S3 backend yapılandırması şöyle olabilir:

```hcl
terraform {
  backend "s3" {
    bucket       = "sirket-terraform-state"
    key          = "production/network/terraform.tfstate"
    region       = "eu-central-1"
    encrypt      = true
    use_lockfile = true
  }
}
```

Bu yapı State’i merkezi bir S3 nesnesinde saklar, sunucu tarafı şifrelemeyi etkinleştirir ve desteklenen Terraform sürümlerinde kilit dosyası kullanır. Kurumun sürümüne ve mevcut mimarisine göre DynamoDB tabanlı eski kilitleme düzenleriyle karşılaşmak da mümkündür.

## İkinci tehlike: State içindeki sırlar

Bir Terraform değişkenini `sensitive = true` yapmak yalnızca terminal çıktısını gizler; değerin State’e yazılmasını otomatik olarak engellemez. Veritabanı parolaları, erişim anahtarları ve sertifika içerikleri State içerisinde açık biçimde bulunabilir.

Bu nedenle aşağıdaki savunmalar birlikte uygulanmalıdır:

1. State deposunda aktarım ve disk şifrelemesini etkinleştirin.
2. IAM yetkilerini en az ayrıcalık ilkesine göre sınırlandırın.
3. State dosyalarını Git deposuna kesinlikle eklemeyin.
4. Bucket sürümleme, erişim günlüğü ve silme koruması kullanın.
5. Parolaları Vault veya bulut secret manager hizmetlerinden çalışma anında alın.
6. CI/CD çalışanlarına kalıcı anahtar yerine kısa ömürlü kimlik verin.

```gitignore
# Terraform çalışma dosyaları
*.tfstate
*.tfstate.*
.terraform/
crash.log
```

`.gitignore` önemli bir emniyet kemeridir; fakat daha önce Git’e gönderilmiş bir sırrı geçmişten silmez. Böyle bir durumda sır derhal döndürülmeli ve depo geçmişi ayrıca temizlenmelidir.

## Güvenli operasyon modeli

Her ortam için ayrı State kullanmak etki alanını küçültür. `dev`, `staging` ve `production` durumlarını yalnızca workspace adına güvenerek değil, mümkünse farklı anahtar yolları ve erişim politikalarıyla ayırın. `apply` işlemlerini geliştirici bilgisayarları yerine onay mekanizmalı CI/CD hattında çalıştırın.

Son olarak kilidi zorla açan `terraform force-unlock` komutunu refleks olarak kullanmayın. Önce kilidi oluşturan işlemin gerçekten sonlandığını doğrulayın. Sağlam State yönetimi; uzak depolama, kilitleme, şifreleme, sürümleme, denetim ve dikkatli yetkilendirmenin birlikte uygulanmasıdır. State sıradan bir JSON dosyası değil, altyapınızın hafızasıdır; hafıza bozulursa Terraform da geçmişi yanlış hatırlar.

![terraform-state-yonetimi-38](/img/terraform-state-yonetimi-38.svg)


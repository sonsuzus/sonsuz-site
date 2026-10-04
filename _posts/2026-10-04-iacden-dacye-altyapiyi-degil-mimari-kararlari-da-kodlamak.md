---
layout: post
title: "IaC’den DaC’ye: Altyapıyı Değil, Mimari Kararları da Kodlamak"
math: true
categories: 
  - Bilgi
tags: 
  - iac
  - dac
  - devsecops
  - policy-as-code
  - gitops
  - güvenlik
  - otomasyon
toc: true
image: /img/iacden-dacye-altyapiyi-78.png
---

Terraform ile sunucu kuruyor, Kubernetes manifestleriyle servis dağıtıyor ve Ansible ile yüzlerce makineyi aynı anda yapılandırıyoruz. Peki neden “Veritabanları internete açık olamaz” veya “Üretim ortamında tüm veriler şifrelenmelidir” gibi mimari kararları hâlâ toplantı notlarında saklıyoruz? Kod Olarak Kararlar, yani **Decisions as Code (DaC)**, organizasyon politikalarını okunabilir, test edilebilir ve Git üzerinden denetlenebilir kurallara dönüştürerek bu çelişkiyi ortadan kaldırıyor.
``

## IaC Neyi Çözdü, DaC Neyi Değiştiriyor?

**Infrastructure as Code (IaC)**, altyapının istenen durumunu kodla tanımlar. DaC ise bu altyapının ve yazılım sistemlerinin **hangi sınırlar içinde tasarlanabileceğini** belirtir. Başka bir ifadeyle IaC, “Ne kurulacak?” sorusuna; DaC, “Neye izin verilecek?” sorusuna yanıt verir.

| Yaklaşım | Kodlanan unsur | Temel soru | Örnek |
|---|---|---|---|
| IaC | Sunucu, ağ, veritabanı | Ne oluşturulacak? | Terraform ile PostgreSQL kurmak |
| Policy as Code | Güvenlik ve uyumluluk kuralı | Bu yapılandırmaya izin var mı? | Açık SSH portunu reddetmek |
| DaC | Mimari karar ve gerekçesi | Sistem hangi ilkelerle tasarlanmalı? | Hassas veriyi yalnızca belirli bölgelerde tutmak |

DaC, Policy as Code kavramını kapsar ancak onunla sınırlı değildir. Kararın kendisi, gerekçesi, sahibi, geçerlilik süresi ve uygulanmasını sağlayan politika birlikte sürümlenir.

Bir değişikliğin kabulünü basitçe şöyle modelleyebiliriz:

$$Kabul = KodTestleri \land GüvenlikPolitikaları \land MimariKararlar$$

Bu ifadede koşullardan biri yanlışsa değişiklik üretime ilerleyemez. Böylece mimari kurul, dağıtımdan üç hafta sonra “Bunu neden böyle yaptınız?” diyen bir dedektif ekibi olmaktan çıkar.

## Kararlar Git’e Nasıl Taşınır?

Her karar, Architecture Decision Record biçiminde bir Markdown dosyasıyla başlayabilir:

```yaml
id: ADR-042
status: accepted
owner: platform-team
decision: Genel erişime açık nesne deposu yasaktır.
expires: 2027-01-01
enforcement: policies/storage.rego
```

Bu kayıt yalnızca belge değildir. `enforcement` alanı, kararın çalıştırılabilir karşılığını gösterir. Open Policy Agent için yazılmış basitleştirilmiş bir Rego politikası şöyle olabilir:

```rego
package architecture.storage

deny[msg] {
  bucket := input.resource
  bucket.type == "object_storage"
  bucket.public == true
  msg := sprintf("%s herkese açık olamaz", [bucket.name])
}
```

Politika, planlanan kaynağı inceler ve herkese açık bir nesne deposu gördüğünde dağıtımı reddeder. Geliştirici yalnızca kırmızı bir pipeline değil, kararın nedenini açıklayan anlaşılır bir mesaj görür.

## Pull Request, Yeni Mimari Kurul

DaC düzeninde politika değişiklikleri de uygulama kodu gibi pull request üzerinden ilerler. Güvenlik, platform ve ilgili ürün ekipleri aynı değişiklik üzerinde yorum yapabilir. Onaylanan karar Git geçmişine girdiği için şu sorular kolayca yanıtlanır:

- Kuralı kim önerdi ve kim onayladı?
- Hangi gerekçeyle değiştirildi?
- Hangi sistemler bu karardan etkileniyor?
- İstisna ne zaman sona erecek?

| Eski güvenlik kültürü | DaC destekli güvenlik kültürü |
|---|---|
| Dağıtım sonrası denetim | Pull request sırasında doğrulama |
| Wiki’de unutulan kararlar | Git ile sürümlenen politikalar |
| Kişilere bağımlı bilgi | Makine tarafından uygulanabilir bilgi |
| Süresiz istisnalar | Sahibi ve bitiş tarihi olan istisnalar |
| Güvenlik ekibi kapı bekçisi | Güvenlik ekibi kural tasarım ortağı |

## Güvenlikte Asıl Devrim

DaC’nin amacı her mimari tercihi körü körüne engellemek değildir. İyi bir sistem; istisna mekanizması, açıklayıcı hata mesajları ve yerel test araçları sunar. Politika geliştirici bilgisayarında çalıştırılabiliyorsa geri bildirim süresi yaklaşık olarak

$$T_{geri\ bildirim} = T_{tespit} + T_{açıklama} + T_{düzeltme}$$

olur. Tespit pipeline’ın sonuna bırakılmadığında bu süre saatlerden dakikalara iner.

Sonuçta IaC altyapıyı tekrar üretilebilir yaptı; DaC ise organizasyonun mühendislik hafızasını tekrar üretilebilir hâle getiriyor. Sunucular kodla kurulurken kararların e-postalarda yaşaması artık makul değil. Güvenlik kültürü, insanlara sürekli “Dikkatli olun” demek yerine doğru davranışı otomatik olarak kolaylaştırdığında gerçekten ölçeklenebilir.

![iacden-dacye-altyapiyi-78](/img/iacden-dacye-altyapiyi-78.svg)


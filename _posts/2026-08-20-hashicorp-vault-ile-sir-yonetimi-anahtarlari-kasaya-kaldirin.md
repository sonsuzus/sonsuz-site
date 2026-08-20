---
layout: post
title: "HashiCorp Vault ile Sır Yönetimi: Anahtarları Kasaya Kaldırın"
math: true
categories: 
  - Bilgi
tags: 
  - hashicorp vault
  - siber güvenlik
  - devops
---

Bir uygulamanın Git deposunda unutulmuş API anahtarı, paylaşılan bir Excel dosyasındaki veritabanı parolası veya aylarca yenilenmeyen TLS sertifikası; güvenlik ihlalinin klasik başlangıç noktalarıdır. HashiCorp Vault, bu hassas değerleri uygulama kodundan ve kişisel hafızalardan ayıran merkezi bir sır yönetimi platformudur. Temel hedef yalnızca sırları şifrelemek değil; kimin, ne zaman, hangi sırra ve hangi koşulla eriştiğini denetlenebilir hâle getirmektir.
``

## Neden sır yönetimi gerekir?

“Sır” kavramı; parolaları, OAuth istemci gizlerini, bulut erişim anahtarlarını, SSH anahtarlarını ve sertifika özel anahtarlarını kapsar. Geleneksel yaklaşımda bu değerler `.env` dosyalarında, CI/CD değişkenlerinde veya yapılandırma dosyalarında yaşar. Bu yöntem ilk bakışta hızlıdır; fakat sır kopyalandıkça saldırı yüzeyi büyür. Basitçe, risk alanını şu şekilde düşünebiliriz:

$$Risk \approx Sır\ Sayısı \times Kopya\ Sayısı \times Geçerlilik\ Süresi$$

Vault, kopya sayısını azaltır ve geçerlilik süresini sınırlayarak bu çarpımı küçültür. Ayrıca erişimi uygulamanın kimliğine bağlar; yani “parolayı bilen herkes” yerine “bu iş yükü, bu politika kapsamında erişebilir” modeli uygulanır.

| Yaklaşım | Sırların yeri | Yenileme | Denetim | İhlal etkisi |
|---|---|---|---|---|
| `.env` dosyası | Sunucu veya depo | Genellikle manuel | Sınırlı | Uzun süreli erişim |
| CI/CD değişkeni | Pipeline platformu | Çoğunlukla manuel | Pipeline odaklı | Geniş kapsamlı olabilir |
| Vault | Merkezi şifreli kasa | Dinamik ve otomatik | Ayrıntılı audit log | TTL ile sınırlı |

## Vault’un temel mimarisi

Vault’ta **storage backend**, şifrelenmiş verinin kalıcı olarak tutulduğu katmandır. Ancak depolama katmanına erişen biri doğrudan sırları okuyamaz; Vault veriyi kendi anahtar hiyerarşisiyle şifreler. **Seal** durumu, kasanın kilitli olduğu anlamına gelir. Başlatma sonrasında kullanılan unseal anahtarları ise operasyonel güvenlik için birden fazla kişiye bölüştürülebilir.

Erişim kararını üç unsur verir: kimlik doğrulama yöntemi, policy ve secret engine. Kubernetes içindeki bir servis hesabı Kubernetes Auth ile, GitHub Actions iş akışı ise OIDC/JWT ile Vault’a giriş yapabilir. Ardından policy, örneğin yalnızca `kv/data/odeme` yolundan okuma izni tanımlar.

```hcl
path "kv/data/odeme" {
  capabilities = ["read"]
}

path "database/creds/raporlama" {
  capabilities = ["read"]
}
```

Bu HCL policy’si, ilgili iş yüküne iki farklı erişim verir: statik ödeme yapılandırmasını okuyabilir ve raporlama için dinamik veritabanı kimliği isteyebilir. Yazma, silme veya başka bir yol için otomatik olarak yetki oluşmaz; bu, en az ayrıcalık ilkesidir.

## Statik sırlar yerine dinamik kimlikler

KV secret engine, API anahtarı gibi mevcut ve statik değerleri saklamak için uygundur. Asıl güç ise Database, PKI ve Cloud secret engine’leriyle ortaya çıkar. Örneğin Vault, PostgreSQL’de isteğe bağlı kullanıcı üretir, kullanıcıya 30 dakikalık TTL tanımlar ve süre sonunda hesabı iptal eder.

| Secret engine | Ürettiği değer | Tipik kullanım | Yaşam döngüsü |
|---|---|---|---|
| KV v2 | Statik anahtar/değer | Üçüncü taraf API anahtarı | Rotasyon politikası |
| Database | Geçici kullanıcı/parola | PostgreSQL, MySQL | Lease ve revoke |
| PKI | X.509 sertifikası | mTLS, servis kimliği | Kısa sertifika ömrü |
| Transit | Şifreleme işlemi | Uygulama verisi | Anahtar Vault’tan çıkmaz |

Dinamik erişimde uygulama parolayı “bilmez”; ihtiyaç anında Vault’tan lease alır. Süre dolduğunda eski kimlik çalışmaz. Bu, sızan bir değerin kullanışlı kaldığı pencereyi dramatik biçimde daraltır.

## Uygulamaya güvenli entegrasyon

Vault token’ını kod içine gömmek de yeni bir sır problemi yaratır. Bunun yerine platformun yerel kimliği kullanılmalıdır: Kubernetes ServiceAccount, AWS IAM rolü veya OIDC iş yükü kimliği iyi seçeneklerdir. Vault Agent, alınan sırrı dosyaya şablonlayabilir ve lease yenilemeyi uygulama adına yapabilir.

```bash
vault login -method=jwt role=backend jwt="$CI_JOB_JWT"
vault read database/creds/raporlama
```

Bu komutlar, CI ortamının JWT kimliğiyle giriş yapar ve kısa ömürlü veritabanı bilgisi alır. Çıktıyı loglara yazdırmamak kritik bir ayrıntıdır; maskeleme tek başına yeterli değildir.

Son olarak audit device etkinleştirin, root token’ı günlük işlerde kullanmayın, production ve test için ayrı Vault alanları planlayın. Düzenli rotasyon, kısa TTL, geri alma prosedürü ve erişim gözden geçirmesi birlikte uygulandığında Vault sadece bir parola kasası değil, ihlal anında etki alanını sınırlayan aktif bir güvenlik kontrolü olur.

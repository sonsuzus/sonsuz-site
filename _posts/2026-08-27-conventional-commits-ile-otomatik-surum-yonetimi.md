---
layout: post
title: "Conventional Commits ile Otomatik Sürüm Yönetimi"
math: true
categories: 
  - Bilgi
tags: 
  - Conventional Commits
  - Semantic Versioning
  - Git
---

Git geçmişiniz yalnızca “neler değişti?” sorusunu değil, “bu değişiklik kullanıcıyı nasıl etkiler?” sorusunu da cevaplamalıdır. Conventional Commits, commit mesajlarını küçük ama anlamlı bir sözleşmeye bağlayarak bu cevabı makine tarafından okunabilir hâle getirir. Sonuç olarak changelog üretimi, sürüm numarası artırma ve yayın notu hazırlama gibi sıkıcı işler otomatikleşir.

``

Temel fikir basittir: Her commit, değişikliğin türünü ve kısa açıklamasını standart bir biçimde taşır. En yaygın şablon şöyledir:

```text
<type>(<scope>): <açıklama>

[isteğe bağlı gövde]

[isteğe bağlı dipnotlar]
```

Örneğin `feat(auth): Google ile giriş ekle` mesajı yeni bir özellik anlatır. `fix(cart): kupon toplamını yanlış hesaplama hatasını düzelt` ise kullanıcıya ulaşabilecek bir hatanın giderildiğini söyler. Buradaki `scope` zorunlu değildir; ancak büyük projelerde `api`, `ui`, `database` veya `auth` gibi alanları ayırt etmeyi kolaylaştırır.

Conventional Commits’in en güçlü yanı, **Semantic Versioning** (SemVer) ile doğal şekilde eşleşmesidir. SemVer sürümü `$MAJOR.MINOR.PATCH$` formunda ifade eder. Uyumlu otomasyon araçları commit türlerine bakarak hangi bölümün artacağını hesaplayabilir:

| Commit işareti | Anlamı | Tipik sürüm etkisi | Örnek |
|---|---|---:|---|
| `fix` | Geriye uyumlu hata düzeltmesi | `PATCH` | `fix(api): boş yanıt hatasını düzelt` |
| `feat` | Geriye uyumlu yeni özellik | `MINOR` | `feat(profile): avatar yükleme ekle` |
| `BREAKING CHANGE` veya `!` | Geriye uyumsuz değişiklik | `MAJOR` | `feat!: eski ödeme uç noktasını kaldır` |
| `docs`, `test`, `chore` | Genellikle kullanıcı etkisi yok | Artış yok | `docs: kurulum adımlarını güncelle` |

Bu ilişkiyi basitçe şöyle düşünebilirsiniz: `$v_{next} = v_{current} + 	ext{değişiklik etkisi}$`. Etki `PATCH`, `MINOR` veya `MAJOR` sınıflarından en büyüğüdür. Bir sürüm döngüsünde hem on hata düzeltmesi hem de bir özellik varsa, sonuç çoğunlukla yalnızca `MINOR` artışıdır; çünkü `MINOR`, `PATCH`ten daha büyük bir değişimdir.

Özellikle kırıcı değişiklikleri açıkça işaretlemek kritiktir. Ünlem işareti başlıkta hızlı görünürlük sağlar; dipnot ise nedenini ayrıntılandırır:

```text
feat(api)!: sipariş oluşturma yanıtını sadeleştir

BREAKING CHANGE: `order.items` alanı artık yanıtın kökünde değil,
`order.data.items` altında döndürülür.
```

Bu mesaj, otomatik yayın aracına major sürüm gerektiğini söylerken ekip arkadaşınıza geçiş maliyetini de anlatır. “Refactor yaptım, umarım bir şey bozulmamıştır” yaklaşımından çok daha güven vericidir.

Pratikte kaliteyi yalnızca iyi niyete bırakmayın. `commitlint` mesaj biçimini doğrulayabilir, `husky` ise doğrulamayı commit aşamasında çalıştırabilir. Örnek yapılandırma aşağıdaki gibi olabilir:

```json
{
  "extends": ["@commitlint/config-conventional"],
  "rules": {
    "subject-case": [2, "never", ["sentence-case", "start-case", "pascal-case"]],
    "header-max-length": [2, "always", 100]
  }
}
```

Bu yapılandırma, standart kuralları devralır; ayrıca başlığın 100 karakteri aşmasını engeller. Amaç geliştiriciyi cezalandırmak değil, commit geçmişini okunabilir ve araçlar için güvenilir tutmaktır. `semantic-release` gibi araçlar da bu geçmişi analiz ederek uygun sürümü yayımlar, Git etiketi oluşturur ve changelog günceller.

Başlangıç için ekibinizde `feat`, `fix`, `docs`, `refactor`, `test`, `chore` türlerinde uzlaşın. Ardından PR şablonlarına örnekler ekleyin ve lint kontrolünü CI hattına koyun. Birkaç hafta içinde commit mesajlarının yalnızca günlük notlar olmadığını; sürümleme stratejinizin çalıştırılabilir girdileri olduğunu göreceksiniz.

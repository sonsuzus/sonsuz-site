---
layout: post
title: "Semantic Release Otomasyonu: Commit Geçmişinden Akıllı Sürüm Yönetimi"
math: true
categories: 
  - Program
tags: 
  - semantic-release
  - git
  - ci-cd
---

Bir projenin sürümünü elle artırmak, değişiklik listesini yazmak ve paketi yayımlamak küçük ekiplerde bile sürpriz derecede hataya açıktır. Semantic Release, Git commit geçmişini okuyarak bu ritüelleri otomatikleştirir: doğru sürüm numarasını hesaplar, CHANGELOG üretir, etiketi oluşturur ve istenirse npm gibi kayıt depolarına paketi yollar. Böylece ekip, “hangi değişiklik major olmalıydı?” tartışmasını yayın gecesine bırakmaz.
``

Bu yaklaşımın temelinde **Semantic Versioning (SemVer)** bulunur. Sürüm numarası $MAJOR.MINOR.PATCH$ biçimindedir. Geriye uyumsuz bir API değişikliği `MAJOR`, geriye uyumlu yeni özellik `MINOR`, hata düzeltmesi ise `PATCH` değerini artırır. Örneğin $2.4.7 \rightarrow 2.5.0$, yeni bir yetenek eklendiğini; $2.4.7 \rightarrow 3.0.0$ ise tüketicilerin kodunu uyarlaması gerekebileceğini anlatır.

Semantic Release bu matematiği tek başına tahmin etmez; **Conventional Commits** sözleşmesine dayanır. Commit mesajının türü, otomasyonun sürüm etkisini anlamasını sağlar. Mesajların tutarlı olması burada bir estetik tercih değil, makinenin okuyacağı arayüzdür.

| Commit örneği | Sürüm etkisi | Notlarda görünümü |
|---|---:|---|
| `fix(api): boş kullanıcıyı doğrula` | PATCH | Hata düzeltmeleri |
| `feat(search): filtre ekle` | MINOR | Yeni özellikler |
| `feat!: eski endpointi kaldır` | MAJOR | Kırıcı değişiklikler |
| `docs: kurulum örneğini güncelle` | Yok | Genellikle yayın tetiklemez |

Kırıcı değişiklik yalnızca `!` ile belirtilmez. Commit gövdesindeki `BREAKING CHANGE:` bildirimi de major sürüm üretir. Bu ayrım önemlidir: başlık kısa kalırken, uyumsuzluğun nedenini ve geçiş yolunu açıklayan ayrıntı gövdede tutulabilir. Mantıksal olarak hesaplama şöyle özetlenebilir:

$$next(v, c)=\begin{cases}
MAJOR(v) & c\text{ kırıcıysa}\\
MINOR(v) & c\text{ bir özellikse}\\
PATCH(v) & c\text{ bir düzeltmeyse}\\
v & \text{aksi halde}
\end{cases}$$

Bir yayın aralığında birden fazla commit varsa en yüksek etki seçilir. Örneğin beş `fix` ve bir `feat` içeren sürüm, beş ayrı patch değil tek bir minor yayın üretir. Bu, sürüm numarasının değişiklik sayısını değil, dışarıdan görünen sözleşme riskini temsil etmesini sağlar.

JavaScript ekosisteminde kurulum için yaygın bir başlangıç şöyledir:

```bash
npm install --save-dev semantic-release \
  @semantic-release/changelog \
  @semantic-release/git
```

Ardından `.releaserc.json` dosyası, analiz ve yayın adımlarını tanımlar:

```json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    ["@semantic-release/changelog", {"changelogFile": "CHANGELOG.md"}],
    "@semantic-release/npm",
    ["@semantic-release/git", {"assets": ["CHANGELOG.md", "package.json"]}]
  ]
}
```

Bu yapılandırmada `commit-analyzer` sonraki sürümü belirler, `release-notes-generator` insan dostu notları üretir, changelog eklentisi dosyayı günceller. `npm` paketi yayımlar; Git eklentisi de oluşan dosyaları depoya geri işler. Elbette son iki adım, projenizin dağıtım biçimine göre kaldırılabilir veya GitHub Releases, Docker imajı ya da özel bir registry eklentisiyle değiştirilebilir.

CI/CD tarafında kritik ilke şudur: yayın işlemi geliştiricinin bilgisayarında değil, korumalı ana dalın başarılı işlem hattında çalışmalıdır. GitHub Actions için minimal bir iş akışı örneği:

```yaml
name: Release
on:
  push:
    branches: [main]
permissions:
  contents: write
  issues: write
  pull-requests: write
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

`fetch-depth: 0` ayrıntısı özellikle değerlidir; araç önceki etiketleri ve commitleri görmeden doğru karşılaştırma yapamaz. Token’lar ise yalnızca gerekli izinlerle tanımlanmalıdır. Commit doğrulamasını pull request aşamasında `commitlint` ve `husky` ile zorunlu kılmak, bozuk mesajın ancak yayın anında fark edilmesini önler.

Sonuçta Semantic Release, “sürüm yayınlamak” işini bir düğmeye basma operasyonundan test edilebilir bir kurala dönüştürür. Disiplinli commit mesajları, güvenilir CI ve küçük, anlaşılır değişiklikler birleştiğinde; sürüm numarası da CHANGELOG da ekibin gerçeğini otomatik biçimde anlatır.

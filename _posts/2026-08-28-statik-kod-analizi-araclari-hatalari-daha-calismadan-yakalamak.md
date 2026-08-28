---
layout: post
title: "Statik Kod Analizi Araçları: Hataları Daha Çalışmadan Yakalamak"
math: true
categories: 
  - Bilgi
tags: 
  - statik analiz
  - kod kalitesi
  - güvenlik
  - CI/CD
  - yazılım geliştirme
---

Kodunuz derleniyor, testler yeşil yanıyor ve uygulama ilk bakışta kusursuz görünüyor olabilir. Yine de kullanılmayan bir yetkilendirme kontrolü, yanlış bir null işlemi veya kullanıcı girdisini doğrudan SQL sorgusuna ekleyen tek satır; üretimde pahalı bir arızaya ya da güvenlik ihlaline dönüşebilir. Statik kod analizi araçları, programı çalıştırmadan kaynak kodu inceleyerek bu riskleri geliştirme sürecinin erken anlarında görünür kılar. Kısacası bunlar, kod incelemesinden önce çalışan yorulmayan birer ekip arkadaşıdır.

``

## Statik analiz tam olarak ne yapar?

Statik analiz, kaynak kodun sözdizimini, türlerini, kontrol akışını ve veri akışını inceler. Araç, kodun olası çalışma yollarını modelleyerek şüpheli desenleri kurallarla karşılaştırır. Örneğin bir değişkenin tanımlanmadan kullanılması, erişilemeyen kod, güvenli olmayan API çağrısı veya hata dönüş değerinin yok sayılması tespit edilebilir.

Temel fikir şudur: Bir programın durum uzayı çok büyük olabilir. Araçlar bu uzayı tamamen gezmek yerine soyutlama kullanır. Gerçek değerler yerine `null olabilir`, `kullanıcıdan geliyor` veya `doğrulanmış` gibi özellikler takip edilir. Analizin hedefi, mümkün olduğunca çok gerçek problemi bulurken geliştiriciyi yanlış alarmlara boğmamaktır.

Bu denge genellikle kesinlik ve kapsama kavramlarıyla açıklanır:

$$\text{Kesinlik} = \frac{TP}{TP + FP}$$

$$\text{Kapsama} = \frac{TP}{TP + FN}$$

Burada $TP$ gerçek tespit, $FP$ yanlış pozitif, $FN$ ise kaçırılan gerçek hatadır. Her aracı her projede “tüm uyarıları sıfırla” hedefiyle kullanmak yerine, kritik kuralları önceliklendirip zamanla kalite çıtasını yükseltmek daha sürdürülebilirdir.

## Statik analiz ve test arasındaki fark

Statik analiz testlerin alternatifi değildir; farklı hata sınıflarını yakalayan tamamlayıcı bir katmandır.

| Özellik | Statik kod analizi | Dinamik testler |
|---|---|---|
| Kod çalıştırılır mı? | Hayır | Evet |
| Güçlü olduğu alan | Desenler, güvenlik kuralları, tip hataları | Gerçek davranış ve entegrasyon |
| Hata yakalama zamanı | Commit ve derleme öncesi | Test senaryosu çalışırken |
| Sınırlaması | Yanlış pozitif üretebilir | Test edilmeyen yolu kaçırabilir |

Örneğin birim testi, belirli bir kullanıcı girişinde fonksiyonun doğru sonuç vermesini kanıtlar. Statik analiz ise uygulamanın başka bir noktasında bu girdinin SQL sorgusuna kontrolsüz biçimde aktığını fark edebilir.

## Hangi araçlar öne çıkar?

Dil ekosistemine göre araç seçimi değişir. JavaScript ve TypeScript projelerinde **ESLint**, stil ve olası mantık sorunları için güçlü bir başlangıçtır. Python tarafında **Ruff**, **Pylint** ve tip denetimi için **mypy** sık kullanılır. Java projelerinde **SpotBugs**, **PMD** ve **SonarQube**; C/C++ için **Clang-Tidy** ile **CodeQL** dikkat çeker. SonarQube, çoklu dil desteği ve kalite panosu sunarken, CodeQL kodu sorgulanabilir bir veritabanı gibi ele alarak özellikle güvenlik araştırmalarında derin analiz sağlar.

Aşağıdaki ESLint yapılandırması, yaygın hataları CI aşamasına taşımak için orta seviye bir örnektir:

```json
{
  "extends": ["eslint:recommended"],
  "rules": {
    "no-eval": "error",
    "eqeqeq": "error",
    "no-unused-vars": ["warn", { "argsIgnorePattern": "^_" }]
  }
}
```

Bu kurallar sırasıyla tehlikeli `eval` kullanımını engeller, tür dönüşümüne açık `==` karşılaştırmalarını yasaklar ve kullanılmayan değişkenleri uyarı olarak bildirir. Uyarı seviyesiyle başlamak, eski kod tabanlarında geçişi daha az sancılı hale getirir.

## Güvenlik kurallarını ciddiye alın

Güvenlik odaklı analizde en değerli yaklaşım veri akışı, yani *taint analysis*tir. Araç, HTTP isteği gibi güvenilmeyen bir kaynaktan gelen verinin SQL çalıştırma, kabuk komutu üretme veya HTML ekrana basma gibi hassas bir noktaya ulaşıp ulaşmadığını izler.

```python
# Riskli: kullanıcı girdisi sorguya birleştiriliyor
query = "SELECT * FROM users WHERE name = '" + name + "'"
cursor.execute(query)

# Güvenli: parametreli sorgu kullanılıyor
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
```

Analiz aracının uyarısı burada yalnızca bir stil tercihi değildir; SQL enjeksiyonu riskinin erken sinyalidir.

Son olarak aracı editöre, pre-commit kancasına ve CI/CD hattına ekleyin. Yeni kodda kritik güvenlik bulgularını derlemeyi başarısız kılan bir kalite kapısı belirleyin; eski borçlar içinse kademeli iyileştirme planı oluşturun. Statik analiz, mükemmel kod garantisi vermez; ancak hataların kullanıcılarınıza ulaşmadan önce yakalanma olasılığını dramatik biçimde artırır.

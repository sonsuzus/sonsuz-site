---
layout: post
title: "Static Code Analysis: Kod Çalışmadan Hataları Yakalamak"
math: true
categories: 
  - Bilgi
tags: 
  - static analysis
  - kod kalitesi
  - güvenlik
  - linting
  - cı/cd
---

Bir uygulamayı çalıştırmadan önce onun hakkında ne kadar çok şey öğrenebiliriz? Static Code Analysis (statik kod analizi), kaynak kodu derleme ya da çalıştırma aşamasına ihtiyaç duymadan inceleyerek olası hataları, standart ihlallerini ve güvenlik risklerini bulmaya çalışan yöntemlerin genel adıdır. Kısacası, kodunuzun içine el feneri tutar: Her gölge gerçek bir hata değildir ama araştırmaya değer olabilir.

``

Statik analiz araçları kodun **sözdizimini**, **kontrol akışını**, **veri akışını** ve bazen de bağımlılıklarını inceler. Örneğin bir değişkenin kullanılmadan önce atanıp atanmadığını, ulaşılamayan bir kod parçasını veya kullanıcıdan gelen verinin doğrudan SQL sorgusuna eklenip eklenmediğini tespit edebilir. Bu yaklaşımın temel hedefi, hatayı üretim ortamına ulaşmadan mümkün olan en erken aşamada yakalamaktır.

Teorik olarak analiz, programın tüm olası çalışma yollarını modellemeye çalışır. Bir fonksiyonun karmaşıklığı sıkça **Cyclomatic Complexity** ile anlatılır:

$$M = E - N + 2P$$

Burada $E$ kontrol akışı grafiğindeki kenarları, $N$ düğümleri, $P$ ise bağlı bileşen sayısını temsil eder. $M$ büyüdükçe fonksiyonun test edilmesi gereken bağımsız yol sayısı artar. Statik analiz aracı size doğrudan “bu kod bozuk” demese bile, karmaşıklığı yüksek fonksiyonları işaretleyerek bakım maliyetini görünür kılar.

| Yaklaşım | Kod çalışır mı? | Güçlü olduğu alan | Sınırlaması |
|---|---:|---|---|
| Statik analiz | Hayır | Erken hata, stil ve güvenlik tespiti | Çalışma zamanı verisini bilemez |
| Dinamik analiz | Evet | Bellek, performans ve gerçek davranış | Test senaryosuna bağımlıdır |
| Kod inceleme | Hayır | Tasarım ve iş mantığı | İnsan zamanı gerektirir |

Örneğin aşağıdaki JavaScript kodu, kullanıcı girdisini doğrudan sorguya eklediği için tehlikelidir:

```javascript
function findUser(db, username) {
  const query = `SELECT * FROM users WHERE name = '${username}'`;
  return db.query(query);
}
```

Bir SAST (Static Application Security Testing) aracı bu satırı SQL injection adayı olarak işaretleyebilir. Daha güvenli yaklaşım, sorgu parametrelerini veri olarak iletmektir:

```javascript
function findUser(db, username) {
  const query = 'SELECT * FROM users WHERE name = ?';
  return db.query(query, [username]);
}
```

İkinci örnekte `username`, SQL komutunun parçası olmak yerine parametre olarak değerlendirilir. Bu, analiz aracının izlediği önemli bir prensiple ilişkilidir: **taint analysis**. Araç, dışarıdan gelen “kirli” verinin (`request.body`, URL parametresi, dosya içeriği) güvenli bir temizleme veya parametreleme adımından geçmeden hassas bir noktaya ulaşıp ulaşmadığını takip eder.

\vert  Araç türü \vert  Örnekler \vert  Tipik kullanım \vert 
\vert ---\vert ---\vert ---\vert 
\vert  Linter \vert  ESLint, Pylint, RuboCop \vert  Stil, olası mantık hataları \vert 
\vert  Tip denetleyici \vert  TypeScript, mypy \vert  Tür uyuşmazlıkları \vert 
\vert  Güvenlik tarayıcısı \vert  Semgrep, SonarQube, CodeQL \vert  Zafiyet desenleri \vert 
\vert  Bağımlılık tarayıcısı \vert  Dependabot, Snyk \vert  Bilinen paket açıkları \vert 

Bu araçlardan verim almak için onları geliştiricinin düşmanı değil, hızlı geri bildirim sağlayan ekip arkadaşı olarak konumlandırın. IDE eklentileriyle anlık uyarı alın; CI/CD hattında ise kritik güvenlik kurallarını “build fail” koşulu yapın. Ancak her uyarıyı körü körüne hata kabul etmeyin. Statik analiz, programın niyetini her zaman tam anlayamaz ve **false positive** üretebilir. Ölçülebilir bir oranla düşünürsek, doğruluk kabaca $Precision = TP / (TP + FP)$ biçiminde ifade edilir; burada $TP$ doğru, $FP$ yanlış pozitif bulgulardır.

Başlangıç için küçük bir kural seti seçin: kullanılmayan değişkenler, gizli anahtarların repoya eklenmesi, tehlikeli API kullanımı ve karmaşık fonksiyonlar. Ardından mevcut teknik borcu tek seferde kapatmaya çalışmak yerine, yeni eklenen kod için kalite eşiği koyun. Böylece statik analiz, gürültülü bir alarm sistemi olmaktan çıkar; kod tabanınızın sürekli çalışan güvenlik kamerasına dönüşür.

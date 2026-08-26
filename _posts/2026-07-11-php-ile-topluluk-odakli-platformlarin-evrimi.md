---
layout: post
title: "PHP ile Topluluk Odaklı Platformların Evrimi"
math: true
categories: 
  - Bilgi
tags: 
  - php
  - forum mimarisi
  - veritabanı güvenliği
image: /img/php-ile-topluluk-27.png
---

Bir forum sitesine girdiğinizde gördüğünüz şey birkaç başlık, avatar ve cevap kutusundan ibaret gibi durur. Oysa arka planda PHP, HTTP isteğini yakalar, oturumu kontrol eder, veritabanından konuları çeker, izinleri hesaplar ve size dinamik bir HTML sayfası üretir. Topluluk odaklı platformların evrimi tam da burada başlar: statik sayfalardan, kullanıcı davranışına göre şekillenen yaşayan sistemlere geçiş.

![php-ile-topluluk-27](/img/php-ile-topluluk-27.svg)

``
PHP’nin forum dünyasındaki popülerliği tesadüf değildir. 2000’lerde phpBB, vBulletin ve SMF gibi yazılımlar, paylaşımlı hostinglerde kolay kurulabildiği için topluluk kültürünü hızla büyüttü. İlk dönemlerde mantık genellikle tek dosyada toplanırdı: `viewtopic.php` hem veriyi çeker, hem iş kurallarını uygular, hem de HTML basardı. Bugün ise daha katmanlı bir yaklaşım tercih edilir: yönlendirme, servis, veri erişimi ve şablonlama birbirinden ayrılır.

Dinamik sayfa oluşturmanın temel fikri basittir: kullanıcıdan gelen istek, sunucuda işlenir ve her kullanıcıya bağlama göre farklı bir çıktı döner. Bunu küçük bir formülle düşünebiliriz: $Sayfa = Veri + Yetki + Şablon$. Örneğin aynı konu sayfası, moderatöre silme butonu gösterirken normal üyeye sadece yanıtla butonu gösterebilir.

| Dönem | Yaklaşım | Avantaj | Risk |
|---|---|---|---|
| Statik HTML | Her sayfa elle hazırlanır | Hızlı ve basit | Etkileşim yok |
| Klasik PHP | PHP içinde HTML ve SQL birlikte | Kolay geliştirme | Bakım ve güvenlik zor |
| Modern PHP | MVC, ORM, şablon motoru | Ölçeklenebilir | Mimari disiplin ister |

![php-ile-topluluk-27](/img/php-ile-topluluk-27.svg)


Bir forumun veritabanı modeli genellikle birkaç ana tablo etrafında döner: kullanıcılar, konular, mesajlar, kategoriler ve roller. Basit ilişki şöyle kurulabilir: bir kullanıcının birçok mesajı vardır, bir konunun birçok mesajı vardır. Matematiksel olarak bunu $User \rightarrow Posts$ ve $Topic \rightarrow Posts$ ilişkileriyle düşünebiliriz. Trafik arttığında sorgu sayısı da önem kazanır; toplam maliyet kabaca $T_{toplam}=T_{sql}+T_{php}+T_{network}$ şeklinde okunabilir.

Güvenli iletişimin kalbi ise hazırlıklı sorgulardır. Kullanıcıdan gelen metni doğrudan SQL cümlesine eklemek, SQL injection davetiyesidir. PDO ile parametre bağlamak, veriyi komut olmaktan çıkarıp yalnızca veri haline getirir.

```php
<?php
$pdo = new PDO(
    'mysql:host=localhost;dbname=forum;charset=utf8mb4',
    'forum_user',
    'secret_password',
    [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
);

$title = trim($_POST['title'] ?? '');
$userId = $_SESSION['user_id'] ?? null;

if ($title === ''  \vert  \vert  !$userId) {
    http_response_code(400);
    exit('Geçersiz istek');
}

$stmt = $pdo->prepare(
    'INSERT INTO topics (user_id, title, created_at) VALUES (:user_id, :title, NOW())'
);
$stmt->execute([
    'user_id' => $userId,
    'title' => $title
]);
```

Bu kodun görevi yeni bir konu başlığı eklemektir. Dikkat ederseniz `$title` doğrudan SQL içine gömülmez; `:title` parametresine bağlanır. Böylece kullanıcı başlığa garip karakterler yazsa bile sorgunun yapısı bozulmaz.

\vert  Tehdit \vert  Kötü Uygulama \vert  Güvenli Yaklaşım \vert 
\vert ---\vert ---\vert ---\vert 
\vert  SQL Injection \vert  String birleştirme \vert  Prepared statement \vert 
\vert  XSS \vert  Ham HTML basmak \vert  `htmlspecialchars` kullanmak \vert 
\vert  CSRF \vert  Formsuz doğrulama \vert  CSRF token kontrolü \vert 
\vert  Yetki aşımı \vert  Sadece arayüzü gizlemek \vert  Sunucu tarafı rol kontrolü \vert 

Dinamik sayfa üretirken güvenlik sadece veritabanı ile bitmez. Mesaj içeriğini ekrana basarken HTML kaçışlama gerekir. Aksi halde biri konuya zararlı JavaScript yazabilir. Basit çıktı örneği:

```php
<p><?= htmlspecialchars($post['body'], ENT_QUOTES, 'UTF-8') ?></p>
```

Ayrıca forumlar sosyal sistemlerdir; teknik tasarım topluluk davranışını etkiler. Bildirimler, rozetler, beğeniler ve moderasyon kuyrukları sadece özellik değil, katılım mekanizmasıdır. Ancak her yeni özellik yeni veri ilişkileri ve yeni güvenlik kontrolleri demektir.

Modern PHP ekosisteminde Laravel veya Symfony gibi çatılar, yönlendirme, ORM, middleware ve CSRF koruması sunarak bu yükü azaltır. Yine de temeli anlamak önemlidir: istek gelir, kimlik doğrulanır, yetki kontrol edilir, güvenli sorgu çalışır, veri temizlenir ve şablona aktarılır. Kısacası iyi bir topluluk platformu, yalnızca konuşma alanı değil; veritabanı, güvenlik ve kullanıcı deneyiminin dengeli bir orkestrasıdır.


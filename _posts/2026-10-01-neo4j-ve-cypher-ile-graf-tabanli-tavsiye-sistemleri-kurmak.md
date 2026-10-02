---
layout: post
title: "Neo4j ve Cypher ile Graf Tabanlı Tavsiye Sistemleri Kurmak"
math: true
categories: 
  - Bilgi
tags: 
  - neo4j
  - cypher
  - graf veritabanı
  - tavsiye sistemi
  - veritabanı
  - backend
toc: true
image: /img/neo4j-ve-cypher-95.png
---

![neo4j-ve-cypher-95](/img/neo4j-ve-cypher-95.svg)


Bir arkadaşının beğendiği filmi sana önermek kolaydır; arkadaşının arkadaşlarının izlediği, senin tür tercihlerinle örtüşen ve benzer kullanıcıların yüksek puan verdiği filmi bulmak ise ilişkiler derinleştikçe zorlaşır. Neo4j, verileri satırlar yerine düğümler ve doğrudan bağlantılar biçiminde saklayarak bu tür soruları doğal şekilde modellememizi sağlar. Cypher sorgu dili de karmaşık ilişki ağlarında gezinmeyi, okunabilir desenler tarif etmeye dönüştürür.
``

## Graf yaklaşımının temel mantığı

Neo4j'de kullanıcılar, ürünler veya filmler birer **düğüm**; arkadaşlık, satın alma ve beğenme gibi etkileşimler ise **ilişki** olarak temsil edilir. Hem düğümler hem de ilişkiler özellik taşıyabilir. Örneğin `IZLEDI` ilişkisinde puan ve izlenme tarihi tutulabilir.

İlişkisel veritabanında kullanıcıdan filme ulaşmak için kullanıcı, arkadaşlık, izleme ve film tabloları arasında birden fazla `JOIN` gerekir. Graf veritabanında düğüm, komşu ilişkilerinin fiziksel referanslarını bildiğinden gezinme işlemi tekrar tekrar genel tablo taraması yapmak yerine ilgili bağlantıları takip eder.

| Özellik | SQL yaklaşımı | Neo4j yaklaşımı |
|---|---|---|
| Veri modeli | Tablo ve yabancı anahtar | Düğüm ve ilişki |
| Derin bağlantılar | Çok sayıda `JOIN` | Desen tabanlı gezinme |
| Şema değişikliği | Görece katı | Daha esnek |
| Güçlü olduğu alan | Toplu ve düzenli veriler | Bağlantı yoğun veriler |
| Sorgu okunabilirliği | Derinlikte karmaşıklaşabilir | Görsel desene benzer |

SQL ile bu işlemler imkânsız değildir; recursive CTE ve uygun indekslerle yapılabilir. Ancak bağlantı sayısı ve sorgu derinliği arttığında ara sonuç kümeleri büyüyebilir. Neo4j'nin avantajı, ilişki gezinmesini veri modelinin merkezine koymasıdır. Milisaniyelik sonuçlar da ancak uygun indeksler, sınırlı derinlik ve kontrollü bağlantı sayısıyla gerçekçidir.

## Basit bir tavsiye deseni

Önce kullanıcı ve film düğümlerini ilişkilendirelim:

```cypher
CREATE (u:User {id: 1, name: 'Ada'})
CREATE (f:Movie {id: 101, title: 'Matrix'})
CREATE (u)-[:WATCHED {rating: 5}]->(f)
```

Bu kod iki düğüm oluşturur ve Ada'nın filme verdiği puanı ilişkinin üzerinde saklar. Gerçek projelerde toplu veri eklemek için `CREATE` yerine çoğunlukla `MERGE`, benzersiz kısıtlar ve aktarım araçları kullanılır.

Bir kullanıcının arkadaşlarının sevdiği fakat kendisinin izlemediği filmleri şöyle bulabiliriz:

```cypher
MATCH (u:User {id: $userId})-[:FRIEND]->(friend:User)
MATCH (friend)-[w:WATCHED]->(movie:Movie)
WHERE w.rating >= 4
  AND NOT EXISTS {
    MATCH (u)-[:WATCHED]->(movie)
  }
RETURN movie.title AS film,
       count(DISTINCT friend) AS destek,
       avg(w.rating) AS ortalamaPuan
ORDER BY destek DESC, ortalamaPuan DESC
LIMIT 10
```

Sorgu önce hedef kullanıcıyı bulur, arkadaşlarına geçer, onların yüksek puan verdiği filmleri toplar ve kullanıcının izlediklerini eler. `$userId` parametresi sorgu planının yeniden kullanılmasına ve güvenli veri aktarımına yardımcı olur.

## Tavsiye skorunu geliştirmek

Yalnızca arkadaş sayısını kullanmak popüler içerikleri gereğinden fazla öne çıkarabilir. Ortak zevk ve puan gibi bileşenler ağırlıklandırılabilir:

$$
Skor(u,m)=\alpha C(u,m)+\beta R(m)+\gamma S(u,m)
$$

Burada $C$ filmi destekleyen bağlantı sayısını, $R$ ortalama puanı, $S$ ise kullanıcı ile filmi seven kişiler arasındaki benzerliği gösterir. Kullanıcı benzerliği için Jaccard katsayısı kullanılabilir:

$$
J(A,B)=\frac{\vert A\cap B\vert }{\vert A\cup B\vert }
$$

İki kullanıcının ortak izlediği filmler arttıkça benzerlik yükselir. Buna kategori yakınlığı, güncellik ve ilişki ağırlığı da eklenebilir. Örneğin eski bir etkileşimin etkisini $e^{-\lambda t}$ ile azaltmak, tavsiyeleri güncel tutar.

## Performans tuzakları

`MATCH (u)-[*]->(x)` gibi sınırsız yollar, yüksek bağlantılı ağlarda patlayıcı sayıda rota üretebilir. Bu nedenle ilişki türünü belirtmek, `*1..3` gibi derinlik sınırı koymak ve başlangıç düğümünü indeksli bir kimlikle bulmak önemlidir. Ayrıca çevrimleri, süper düğümleri ve gereksiz yönsüz eşleşmeleri kontrol etmek gerekir.

Neo4j, ilişkilerin bizzat ürün olduğu sosyal ağ, sahtekârlık analizi ve tavsiye sistemi projelerinde güçlüdür. Başarılı çözümün sırrı yalnızca Cypher yazmak değil; doğru graf modelini kurmak, anlamlı bir skor üretmek ve sorgunun dolaşacağı alanı bilinçli biçimde sınırlamaktır.

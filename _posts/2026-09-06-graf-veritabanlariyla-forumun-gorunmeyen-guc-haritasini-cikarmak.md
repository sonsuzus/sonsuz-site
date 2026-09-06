---
layout: post
title: "Graf Veritabanlarıyla Forumun Görünmeyen Güç Haritasını Çıkarmak"
math: true
categories: 
  - Proje
tags: 
  - graf-veritabanı
  - sosyal-ağ-analizi
  - neo4j
toc: true
---

Bir forum yalnızca mesajların sıralandığı dijital bir pano değildir; üyelerin cevap verdiği, tartıştığı, destek olduğu ve bazen küçük krallıklar kurduğu canlı bir ilişkiler ağıdır. Graf veritabanları sayesinde bu ağı çizge olarak modelleyebilir, topluluğun merkezindeki kullanıcıları ve görünmeyen hiyerarşisini matematiksel metriklerle ortaya çıkarabiliriz.
``

## Forumdan çizgeye: Düğümler ve kenarlar

Çizge modelinde kullanıcıları düğüm, aralarındaki etkileşimleri ise yönlü kenar olarak temsil ederiz. Örneğin A kullanıcısı, B’nin mesajına cevap verdiyse `(A)-[:REPLIED_TO]->(B)` ilişkisi oluşturulur. Aynı kullanıcılar birçok kez etkileşime girdiyse her olay için ayrı kenar açmak yerine ilişkiye `weight` özelliği eklemek daha verimlidir.

$$G=(V,E)$$

Burada $V$ kullanıcı kümesini, $E$ ise etkileşimleri gösterir. Ağırlıklı komşuluk matrisi içindeki $A_{ij}$ değeri, $i$ kullanıcısının $j$ kullanıcısıyla kaç kez etkileşime girdiğini ifade edebilir.

| Forum olayı | Graf karşılığı | Olası ağırlık |
|---|---|---:|
| Mesaja cevap | `REPLIED_TO` | 3 |
| Kullanıcıyı etiketleme | `MENTIONED` | 1 |
| Mesajı beğenme | `LIKED` | 0.5 |
| Çözüm olarak işaretleme | `SOLVED_FOR` | 5 |

Ağırlıklar ürün hedeflerine göre seçilmelidir. Bir “çözüm” etkileşiminin sıradan beğeniden değerli kabul edilmesi, uzman kullanıcıların daha doğru tanınmasını sağlar.

## Veriyi Neo4j’ye aktarmak

Aşağıdaki Cypher sorgusu iki kullanıcıyı oluşturur ve tekrar eden cevapları tek ilişkide toplar:

```cypher
MERGE (author:User {id: $authorId})
MERGE (target:User {id: $targetId})
MERGE (author)-[r:REPLIED_TO]->(target)
ON CREATE SET r.weight = 1
ON MATCH SET r.weight = r.weight + 1
```

`MERGE`, aynı kişinin veya ilişkinin yanlışlıkla tekrar oluşturulmasını engeller. Gerçek projede zaman damgası, kategori ve duygu skoru gibi özellikler de saklanabilir. Böylece yalnızca “kim kiminle konuştu?” değil, “hangi konuda ve ne zaman konuştu?” soruları da cevaplanır.

## Merkeziyet: Forumun yıldızları kim?

Her popüler kullanıcı aynı role sahip değildir. Merkeziyet algoritmaları farklı güç türlerini ölçer.

| Metrik | Ölçtüğü özellik | Forumdaki anlamı |
|---|---|---|
| Derece merkeziyeti | Doğrudan bağlantı sayısı | En çok etkileşen kişi |
| PageRank | Bağlantıların niteliği | Önemli üyelerin yöneldiği kişi |
| Arasındalık | En kısa yollardaki konum | Gruplar arasındaki köprü |
| Yakınlık | Diğerlerine erişim mesafesi | Bilgiyi hızlı yayabilen kişi |

Normalize edilmiş derece merkeziyeti şöyle hesaplanır:

$$C_D(v)=\frac{deg(v)}{\vert V\vert -1}$$

Ancak yalnızca dereceye bakmak yanıltıcıdır. Yüzlerce yüzeysel cevap veren bir kullanıcı, az fakat deneyimli üyelerle güçlü ilişkiler kuran başka bir kullanıcıdan daha yüksek puan alabilir. PageRank bu farkı, bağlantı kaynağının önemini hesaba katarak azaltır:

$$PR(v)=\frac{1-d}{N}+d\sum_{u\in B(v)}\frac{PR(u)}{L(u)}$$

## Neo4j Graph Data Science ile PageRank

Önce analiz için bellekte bir grafik izdüşümü oluşturur, ardından PageRank çalıştırırız:

```cypher
CALL gds.graph.project(
  'forumGraph',
  'User',
  {REPLIED_TO: {properties: 'weight'}}
);

CALL gds.pageRank.stream('forumGraph', {
  relationshipWeightProperty: 'weight'
})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).id AS user, score
ORDER BY score DESC
LIMIT 10;
```

Bu sorgu forumun en etkili on kullanıcısını döndürür. Sonuçlar moderatör seçimi, uzman rozeti veya öneri sistemi için kullanılabilir; fakat otomatik yetkilendirme kararı vermeden önce spam ve bot davranışı filtrelenmelidir.

## Hiyerarşiyi keşfetmek

Forum hiyerarşisi yalnızca “yönetici–üye” ayrımı değildir. Louvain veya Leiden algoritmasıyla topluluklar, k-core ile ağın dayanıklı çekirdeği bulunabilir. Yüksek `core` değerine sahip üyeler, birbirleriyle yoğun biçimde bağlı merkez katmanı oluşturur. PageRank yüksek, arasındalık düşükse kullanıcı kendi grubunun otoritesi olabilir. Her ikisi de yüksekse grupları birbirine bağlayan güçlü bir kanaat önderidir.

Son olarak metrikleri zaman pencereleriyle hesaplamak önemlidir. Tüm geçmişi tek grafikte toplamak, yıllar önce aktif olmuş “hayalet kralları” zirvede tutabilir. Son 30, 90 ve 365 günlük ağları karşılaştırmak; yükselen uzmanları, zayıflayan toplulukları ve bilgi akışındaki darboğazları çok daha erken gösterir.

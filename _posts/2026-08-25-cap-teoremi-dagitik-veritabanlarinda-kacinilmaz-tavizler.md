---
layout: post
title: "CAP Teoremi: Dağıtık Veritabanlarında Kaçınılmaz Tavizler"
math: true
categories: 
  - Bilgi
tags: 
  - CAP Teoremi
  - Dağıtık Sistemler
  - Veritabanı
  - Tutarlılık
---

Dağıtık veritabanları, veriyi birden fazla makineye yayarak ölçeklenebilirlik ve arıza toleransı sağlar. Ancak sistem farklı sunuculara, ağ bağlantılarına ve gecikmelere dağıldığında tek bir veritabanı gibi davranması zorlaşır. CAP Teoremi tam bu noktadaki temel gerçeği anlatır: Ağ bölünmesi yaşanırken **tutarlılık**, **erişilebilirlik** ve **bölünme toleransının** üçünü aynı anda eksiksiz sunamazsınız.

``

CAP, 2000 yılında Eric Brewer tarafından ortaya atılan ve daha sonra Gilbert ile Lynch tarafından matematiksel olarak kanıtlanan bir ilkedir. Buradaki kritik ayrım şudur: Teorem, sistem normal çalışırken her zaman yalnızca iki özellik seçilir demek değildir. Asıl iddia, ağdaki düğümler birbirleriyle haberleşemediğinde sistemin **Consistency** ile **Availability** arasında karar vermek zorunda kalacağıdır.

| Özellik | Anlamı | Kullanıcı açısından sonucu |
|---|---|---|
| **C — Consistency** | Her okuma, en güncel başarılı yazmayı veya açık bir hatayı döndürür. | Herkes aynı veriyi görür. |
| **A — Availability** | Hata almayan her düğüm, her isteğe yanıt üretir. | Sistem cevap vermeyi sürdürür. |
| **P — Partition Tolerance** | Düğümler arası iletişim kopsa bile sistem çalışmaya devam eder. | Ağ arızası sistemi tamamen durdurmaz. |

Tutarlılık, SQL dünyasında sık duyulan ACID tutarlılığıyla birebir aynı kavram değildir. CAP'teki C, daha çok **doğrusallaştırılabilirlik** (*linearizability*) fikrine yakındır: Bir yazma işleminden sonra yapılan okuma, bu yazmayı görmelidir. Örneğin hesabınıza $100$ TL yatırıldıysa, sonraki bakiye sorgusu eski değeri döndürmemelidir.

Ağ bölünmesini iki veri merkezi arasındaki kablonun kopması gibi düşünün. Başlangıçta iki kopya da aynı bakiyeyi taşısın:

$$B_{Ankara} = B_{İzmir} = 100$$

Ankara'da $+50$ TL yazılırken bağlantı koparsa, İzmir bu değişikliği öğrenemez. Ankara isteği kabul edip İzmir eski değeri döndürmeye devam ederse erişilebilirlik korunur, fakat tutarlılık bozulur. Ankara, İzmir'le konuşana kadar yazmayı ya da okumayı reddederse tutarlılık korunur; bu kez erişilebilirlikten ödün verilir.

| Bölünme anındaki tercih | Davranış | Tipik örnekler |
|---|---|---|
| **CP** | Bazı istekleri bekletir veya hata verir; yanlış veri döndürmez. | etcd, ZooKeeper, HBase |
| **AP** | Her düğüm yanıt verir; kopyalar daha sonra uzlaşır. | Cassandra, Riak, DynamoDB tasarımları |
| **CA** | Ağ bölünmesi yok varsayımında hem C hem A sağlar. | Tek düğümlü ilişkisel veritabanı |

Pratikte **CA** etiketi biraz yanıltıcıdır. Gerçek ağlarda paket kaybı ve bağlantı kopması kaçınılmazdır; yani üretim ortamındaki dağıtık bir sistem P'yi tamamen görmezden gelemez. Bu yüzden soru genellikle “CP mi, AP mi?” şeklinde sorulur. Elbette birçok ürün ayarlanabilir tutarlılık seviyeleri sunarak bu ikiliği iş gereksinimine göre yumuşatır.

Örneğin Cassandra'da okuma ve yazma için kaç replikanın onay vermesi gerektiğini seçebilirsiniz:

```sql
CONSISTENCY QUORUM;
INSERT INTO orders (id, status) VALUES (42, 'paid');
SELECT status FROM orders WHERE id = 42;
```

`QUORUM`, çoğunluk onayı ister. Toplam replika sayısı $N$ iken yazma onayı $W$, okuma onayı $R$ ise, genellikle

$$R + W > N$$

koşulu okuma ve yazma kümelerinin en az bir ortak replikada kesişmesini hedefler. Bu, güçlü görünürlük şansını artırır; ancak ağ sorunlarında gecikme ve hata oranı da yükselebilir.

Doğru seçim verinin değerine bağlıdır. Banka bakiyesi, stoktan son ürünün satışı veya dağıtık kilit gibi işlemler CP yaklaşımından yararlanır; yanlış bir cevap maliyetlidir. Sosyal medya beğeni sayısı, analiz sayaçları ya da öneri akışları ise kısa süreli eski veriyi tolere edebilir ve AP yaklaşımını tercih edebilir.

Sonuç olarak CAP Teoremi bir teknoloji sıralaması değil, tasarım pusulasıdır. “Her koşulda hızlı, kesintisiz ve tamamen güncel” vaadini sorgulatır. Önce ağ bölünmesinde hangi hatanın kabul edilebilir olduğunu belirleyin; ardından veritabanınızın çoğaltma, uzlaşma ve hata yönetimi ayarlarını bu karara göre şekillendirin.

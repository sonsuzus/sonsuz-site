---
layout: post
title: "Java Collections Framework: List, Set ve Map ile Veriyi Dizginlemek"
math: true
categories: 
  - Bilgi
tags: 
  - java
  - collections
  - list
  - set
  - map
  - veri-yapıları
toc: true
image: /img/java-collections-framework-11.png
---

Bir uygulamada verileri saklamak kolaydır; onları doğru sırada tutmak, tekrarları engellemek ve hızlıca bulmak ise asıl meseledir. Java Collections Framework, bu ihtiyaçlar için `List`, `Set` ve `Map` gibi hazır veri yapıları sunar. Böylece tekerleği yeniden icat etmek yerine doğru koleksiyonu seçip iş mantığına odaklanabiliriz.

![java-collections-framework-11](/img/java-collections-framework-11.svg)

``

## Collections Framework nedir?

Collections Framework; veri yapılarından, bunlarla çalışan arayüzlerden ve yardımcı algoritmalardan oluşan standart bir Java API’sidir. Hiyerarşinin merkezinde `Collection<E>` arayüzü bulunur. `List<E>` ve `Set<E>` bu arayüzden türetilirken `Map<K, V>`, anahtar-değer modeli nedeniyle ayrı bir hiyerarşide yer alır.

Buradaki `E`, koleksiyonda saklanan elemanın türünü belirten generic parametredir. Örneğin `List<String>`, yalnızca metin saklamayı amaçlar. Bu yaklaşım çalışma zamanında ortaya çıkabilecek tür hatalarını derleme aşamasına taşır.

| Yapı | Sıralama | Tekrar | Erişim biçimi | Tipik kullanım |
|---|---|---|---|---|
| `List` | Korunur | İzin verilir | İndeks | Alışveriş sepeti |
| `Set` | Uygulamaya bağlı | Engellenir | Eleman | Benzersiz kullanıcılar |
| `Map` | Uygulamaya bağlı | Anahtarlar benzersizdir | Anahtar | Kimlikten kayıt bulma |

## List: Sıralı veri dünyası

`List`, elemanların eklenme sırasını korur ve aynı değerin birden fazla kez bulunmasına izin verir. En yaygın uygulaması `ArrayList` sınıfıdır. İndeksle erişim ortalama $O(1)$ zaman karmaşıklığına sahiptir. Ancak listenin ortasına eleman eklemek, sonraki elemanların kaydırılmasını gerektirdiğinden $O(n)$ olabilir.

```java
List<String> diller = new ArrayList<>();
diller.add("Java");
diller.add("Python");
diller.add("Java");

System.out.println(diller.get(0)); // Java
diller.remove("Python");
```

Bu kod sıralı bir dil listesi oluşturur. İkinci `Java` kabul edilir çünkü `List` tekrarları yasaklamaz. Sıkça baştan veya ortadan ekleme yapılacaksa bağlantılı düğümler kullanan `LinkedList` düşünülebilir; fakat çoğu genel senaryoda `ArrayList` daha iyi başlangıç seçimidir.

## Set: Tekrarlara geçit yok

`Set`, her elemanın yalnızca bir kez bulunmasını sağlar. `HashSet`, elemanları hash değerleri üzerinden yönetir ve ekleme, silme, arama işlemlerinde ortalama $O(1)$ performans sunar.

```java
Set<String> roller = new HashSet<>();
roller.add("admin");
roller.add("editor");
roller.add("admin");

System.out.println(roller.size()); // 2
```

İkinci `admin` eklenmez. Ekleme sırası önemliyse `LinkedHashSet`, elemanların doğal veya özel bir kurala göre sıralanması gerekiyorsa `TreeSet` kullanılabilir. `TreeSet` işlemleri dengeli ağaç yapısı nedeniyle genellikle $O(\log n)$ maliyetindedir.

## Map: Anahtarı ver, değeri al

`Map`, verileri anahtar-değer çiftleri hâlinde saklar. Telefon rehberindeki isim-numara ilişkisi buna güzel bir örnektir. `HashMap`, benzersiz anahtarlar kullanır; aynı anahtarla yeniden değer eklenirse eski değer güncellenir.

```java
Map<Integer, String> kullanicilar = new HashMap<>();
kullanicilar.put(101, "Ayşe");
kullanicilar.put(102, "Mert");
kullanicilar.put(101, "Deniz");

String ad = kullanicilar.getOrDefault(101, "Bulunamadı");
System.out.println(ad); // Deniz
```

Harita üzerinde güvenli dolaşmak için `entrySet()` kullanılabilir:

```java
for (Map.Entry<Integer, String> kayit : kullanicilar.entrySet()) {
    System.out.println(kayit.getKey() + ": " + kayit.getValue());
}
```

## Yardımcı işlemler ve doğru seçim

`Collections` yardımcı sınıfı; sıralama, ters çevirme ve en küçük elemanı bulma gibi algoritmalar sağlar.

```java
List<Integer> puanlar = new ArrayList<>(List.of(70, 95, 82));
Collections.sort(puanlar);
Collections.reverse(puanlar);
```

Seçim kuralı basittir: Konum ve sıra önemliyse `List`, benzersizlik önemliyse `Set`, bir anahtardan değere ulaşılacaksa `Map` kullanılır. Ayrıca `HashMap` ve `HashSet` içinde özel nesneler saklanırken `equals()` ile `hashCode()` metotlarının tutarlı tanımlanması gerekir. Eşit kabul edilen iki nesne için şu ilişki korunmalıdır: $a.equals(b) \Rightarrow a.hashCode() = b.hashCode()$. Doğru koleksiyon seçimi hem kodu okunabilir kılar hem de uygulamanın gereksiz yere kaplumbağa moduna geçmesini engeller.

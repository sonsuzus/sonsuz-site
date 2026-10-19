---
layout: post
title: "Java Veri Tipleri, Değişkenler ve Diziler: Tip Güvenliğine Sağlam Bir Başlangıç"
math: true
categories: 
  - Bilgi
tags: 
  - java
  - veri tipleri
  - değişkenler
  - diziler
  - tip güvenliği
  - programlama
toc: true
image: /img/java-veri-tipleri-59.png
---

Java’da her verinin bir kimliği vardır: tipi! Bir değişkenin sayı mı, karakter mi yoksa mantıksal değer mi taşıyacağı önceden belirtilir. Bu yaklaşım başlangıçta biraz katı görünse de hataların daha kod çalışmadan yakalanmasını sağlar. Gelin Java’nın tip güvenliği dünyasına, değişkenlerine ve aynı türden verileri düzenleyen dizilerine yakından bakalım.
``

## Java Neden Katı Tipli Bir Dildir?

Java, **statik ve güçlü tipli** bir programlama dilidir. Statik tipleme, değişken tiplerinin derleme aşamasında bilinmesi anlamına gelir. Güçlü tipleme ise uyumsuz tipler arasında kontrolsüz işlem yapılmasını engeller.

Örneğin aşağıdaki kod derlenemez:

```java
int yas = 25;
yas = "yirmi beş"; // Hata: String, int değişkenine atanamaz
```

Derleyicinin bu itirazı aslında dostça bir uyarıdır. Aksi hâlde program, çalışma sırasında beklenmedik sonuçlarla karşılaşabilirdi. Tip güvenliği sayesinde bir değişkenin hangi değerleri taşıyabileceği ve üzerinde hangi işlemlerin uygulanabileceği bellidir.

## İlkel Veri Tipleri

Java’da doğrudan değer saklayan sekiz adet **primitive**, yani ilkel veri tipi bulunur. Bunlar nesne değildir ve genellikle hızlı, düşük maliyetli veri işlemleri için kullanılır.

| Tip | Boyut | Örnek | Kullanım amacı |
|---|---:|---|---|
| `byte` | 8 bit | `120` | Küçük tam sayılar |
| `short` | 16 bit | `30000` | Orta aralıklı tam sayılar |
| `int` | 32 bit | `42` | Genel tam sayı işlemleri |
| `long` | 64 bit | `9000L` | Büyük tam sayılar |
| `float` | 32 bit | `3.14F` | Düşük hassasiyetli ondalık sayılar |
| `double` | 64 bit | `3.14159` | Yüksek hassasiyetli ondalık sayılar |
| `char` | 16 bit | `'A'` | Tek bir Unicode karakteri |
| `boolean` | JVM’e bağlı | `true` | Doğru veya yanlış durumu |

![java-veri-tipleri-59](/img/java-veri-tipleri-59.svg)


$n$ bitlik işaretli bir tam sayının teorik değer aralığı şu şekilde hesaplanır:

$$-2^{n-1} \leq x \leq 2^{n-1}-1$$

Dolayısıyla 8 bitlik `byte`, $-128$ ile $127$ arasında değer alabilir. Daha büyük bir değer atamaya çalışmak derleme hatasına neden olur.

## Değişken Tanımlama ve Tür Dönüşümü

Bir değişken; tip, isim ve isteğe bağlı başlangıç değerinden oluşur:

```java
int ogrenciSayisi = 24;
double sicaklik = 21.5;
char seviye = 'A';
boolean aktifMi = true;
```

Küçük kapsamlı bir tipten daha geniş kapsamlı tipe geçiş çoğunlukla otomatik yapılır. Buna **widening conversion** denir. Tersi yönde ise veri kaybı oluşabileceği için açık dönüşüm gerekir.

```java
int puan = 95;
double ondalikliPuan = puan; // Otomatik dönüşüm

double fiyat = 49.99;
int tamFiyat = (int) fiyat;   // Açık dönüşüm: sonuç 49
```

| Dönüşüm | Örnek | Risk |
|---|---|---|
| Genişletme | `int` → `double` | Genellikle güvenli |
| Daraltma | `double` → `int` | Hassasiyet veya veri kaybı |

## Diziler: Aynı Tipten Verilerin Takımı

Dizi, aynı veri tipindeki birden fazla değeri sabit uzunlukta saklar. Java dizileri nesnedir; ancak içlerinde ilkel değerler veya nesne referansları bulunabilir.

```java
int[] notlar = {85, 90, 72, 100};

System.out.println(notlar[0]); // 85
System.out.println(notlar.length); // 4
```

Dizi indeksleri sıfırdan başlar. Uzunluğu $n$ olan bir dizinin geçerli indeks aralığı $0$ ile $n-1$ arasındadır. Bu sınırın dışına çıkılması `ArrayIndexOutOfBoundsException` üretir.

Diziler sonradan da oluşturulabilir:

```java
String[] diller = new String[3];
diller[0] = "Java";
diller[1] = "Kotlin";
diller[2] = "Python";

for (String dil : diller) {
    System.out.println(dil);
}
```

Buradaki geliştirilmiş `for` döngüsü, indeks yönetmeden her elemanı sırayla okur. Dizinin uzunluğu oluşturulduktan sonra değişmez; dinamik boyut gerekiyorsa `ArrayList` tercih edilir.

Sonuç olarak Java’nın katı tip sistemi, programcıyı kısıtlamak için değil güvenilir kod üretmeye yönlendirmek için vardır. Doğru veri tipini seçmek belleği ve niyeti netleştirirken diziler, benzer verileri düzenli biçimde yönetmenin temelini oluşturur.

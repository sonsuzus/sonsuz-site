---
layout: post
title: "ln Komutunda Sembolik ve Sabit Bağlar: Aynı Kapıya Çıkmayan İki Kısayol"
math: true
categories: 
  - Bilgi
tags: 
  - linux
  - shell
  - ln
  - sembolik-bağ
  - hard-link
  - dosya-sistemi
toc: true
image: /img/ln-komutunda-sembolik-19.png
---

`ln` komutuyla oluşturulan sembolik ve sabit bağlar ilk bakışta aynı işi yapıyor gibi görünür: Bir dosyaya başka bir ad üzerinden erişmek. Fakat dosya silindiğinde, taşındığında veya farklı bir disk bölümü kullanıldığında iki bağ türü bambaşka davranır. Bu ayrımı anlamanın anahtarı, dosya adı yerine inode kavramına odaklanmaktır.

``

## Önce inode mantığını anlayalım

Linux dosya sisteminde bir dosya adı, verinin kendisi değildir. Dizin içinde bulunan ad, dosyanın metadata bilgilerini ve disk bloklarını temsil eden bir **inode** numarasına işaret eder. Basitleştirilmiş ilişki şöyledir:

$$\text{Dosya adı} \rightarrow \text{inode} \rightarrow \text{veri blokları}$$

Bir sabit bağ, aynı inode'a işaret eden ikinci bir dosya adıdır. Sembolik bağ ise hedefin inode'unu değil, yolunu içeren özel bir dosyadır:

$$\text{Hard link} \rightarrow \text{aynı inode}$$

$$\text{Symlink} \rightarrow \text{hedef yol metni} \rightarrow \text{hedef inode}$$

Başka bir deyişle hard link dosyaya yeni bir isim kartı takar; symlink ise hedefin adresini yazan bir yön tabelası yerleştirir.

## Temel kullanım

Sabit bağ oluştururken `-s` seçeneği kullanılmaz:

```bash
ln rapor.txt rapor-yedek.txt
```

Bu komut `rapor-yedek.txt` adını, `rapor.txt` ile aynı inode'a bağlar. İki isim de eşit statüdedir; teknik olarak hangisinin “orijinal” olduğu önemli değildir.

Sembolik bağ oluşturmak için `-s` kullanılır:

```bash
ln -s rapor.txt rapor-kisayol.txt
```

Burada `rapor-kisayol.txt`, yalnızca `rapor.txt` yolunu saklar. `ls -l` çıktısındaki ok bunu görünür hâle getirir:

```bash
ls -li rapor*
```

`-i` seçeneği inode numaralarını gösterir. Hard linklerin inode numarası aynı, sembolik bağınki ise farklı olacaktır.

## Davranış farkları

| Özellik | Sabit bağ (hard link) | Sembolik bağ (symlink) |
|---|---|---|
| İşaret ettiği şey | Inode | Dosya yolu |
| Hedef silinirse | Veri erişilebilir kalır | Bağ kırılır |
| Farklı dosya sistemine geçebilir mi? | Hayır | Evet |
| Dizine bağlanabilir mi? | Genellikle hayır | Evet |
| Kendi inode'u var mı? | Hedefle aynıdır | Evet, farklıdır |
| Göreli yol kullanabilir mi? | Yol saklamaz | Evet |

![ln-komutunda-sembolik-19](/img/ln-komutunda-sembolik-19.svg)


En sık karıştırılan durum hedef dosyanın silinmesidir:

```bash
printf 'Merhaba Linux\n' > mesaj.txt
ln mesaj.txt mesaj-hard.txt
ln -s mesaj.txt mesaj-soft.txt
rm mesaj.txt
cat mesaj-hard.txt
cat mesaj-soft.txt
```

`mesaj-hard.txt` çalışmaya devam eder çünkü inode hâlâ en az bir ad tarafından kullanılmaktadır. `mesaj-soft.txt` ise artık var olmayan `mesaj.txt` yolunu arar ve hata verir.

Bir inode'un verisi, ona bağlı sabit adların sayısı sıfıra indiğinde ve hiçbir süreç dosyayı açık tutmadığında temizlenebilir. Bağ sayısını $L$ ile gösterirsek basit koşul şöyledir:

$$L = 0 \Rightarrow \text{dosya verisi silinmeye adaydır}$$

Bağ sayısını `stat mesaj-hard.txt` veya `ls -l` ile inceleyebilirsiniz.

## Taşıma tuzağı ve göreli yollar

Sembolik bağ hedef yolunu metin olarak sakladığı için hedef başka yere taşınırsa kırılabilir. Ayrıca göreli hedef, komutun çalıştırıldığı dizine değil, **sembolik bağın bulunduğu dizine göre** çözümlenir.

```bash
ln -s ../config/app.conf proje/app.conf
```

Buradaki `../config/app.conf`, `proje` dizininden başlanarak değerlendirilir. Bu ayrıntı dağıtım betiklerinde küçük ama sinir bozucu sürprizler üretebilir.

## Hangisini seçmelisiniz?

Yapılandırma dosyaları, sürüm klasörleri ve farklı disklerdeki hedefler için sembolik bağ daha esnektir. Aynı dosya sistemi içinde verinin bir ad silinse bile erişilebilir kalmasını istiyorsanız hard link uygundur. Ancak hard link bir yedek değildir: İçerik değiştirildiğinde aynı inode kullanıldığı için bütün adlardan görülen veri değişir. Kısacası `-s`, yalnızca küçük bir seçenek değil; bağın dosya sistemindeki kimliğini tamamen değiştiren seçimdir.

---
layout: post
title: "TLA+ ile Dağıtık Sistem Doğrulama: Yarış Koşullarını Matematikle Yakalamak"
math: true
categories: 
  - Bilgi
tags: 
  - tla+
  - dağıtık sistemler
  - formal metotlar
---

Dağıtık sistemlerde hata ayıklamak bazen sisli bir ormanda kaybolmaya benzer: Her servis tek başına doğru görünür, fakat belirli bir zamanlama gerçekleştiğinde sistem beklenmedik biçimde kilitlenir. TLA+, bu tür sorunları üretime taşınmadan önce durum uzayını matematiksel olarak incelemeye yarayan güçlü bir formal doğrulama dilidir. Özellikle yarış koşulları, lider seçimi ve karşılıklı dışlama gibi eşzamanlılık problemlerinde “bu hata hiç oluşamaz” iddiasını test edilebilir bir kanıta dönüştürür.
``

## TLA+ neyi modeller?

TLA+, sisteminizi sınıflar ve fonksiyonlar üzerinden değil, **durumlar** ve bu durumlar arasındaki **geçişler** üzerinden tanımlar. Bir durum; sayaçlar, kuyruklar, kilit sahipleri veya düğüm rolleri gibi değişkenlerin o andaki değeridir. Bir sonraki durum ise bir işlemin çalışmasıyla oluşur.

Temel fikir şu formülle ifade edilir:

$$Spec \equiv Init \land \Box[Next]_{vars}$$

Burada `Init`, sistemin geçerli başlangıç durumlarını; `Next`, izin verilen durum değişimlerini; $\Box$ ise bu davranışın zaman boyunca sürekli geçerli olması gerektiğini anlatır. Yani TLA+, “hangi kod satırı çalıştı?” sorusundan çok, “sistem hangi güvenli durumdan hangi diğer güvenli duruma geçebilir?” sorusunu sorar.

| Kavram | Geleneksel test | TLA+ model kontrolü |
|---|---|---|
| Zamanlama | Seçilmiş birkaç senaryo | Olası tüm küçük zamanlamalar |
| Hata bulma | Çalıştırma sırasında | Durum uzayını tarayarak |
| Sonuç | Hata görülmedi | Özellik doğrulandı veya karşı örnek bulundu |
| Çıktı | Log ve stack trace | Hatalı durumlara giden iz |

## Yarış koşulunu modellemek

İki iş parçacığının aynı sayacı artırdığını düşünelim. Her biri önce değeri okur, sonra artırılmış değeri yazar. Atomik olmayan bu işlemde iki süreç de `0` değerini okuyup `1` yazabilir. Beklenen değer `2`, gerçek değer ise `1` olur: klasik yarış koşulu.

Aşağıdaki küçük TLA+ modeli, iki sürecin kritik bölgeye aynı anda girmesini yasaklayan bir kilidi ifade eder:

```tla
---------------- MODULE Mutex ----------------
EXTENDS Naturals

CONSTANT Processes
VARIABLE lockOwner, inCritical

Init ==
  /\ lockOwner = None
  /\ inCritical = {}

Enter(p) ==
  /\ lockOwner = None
  /\ lockOwner' = p
  /\ inCritical' = inCritical \cup {p}

Exit(p) ==
  /\ lockOwner = p
  /\ lockOwner' = None
  /\ inCritical' = inCritical \ {p}

Next == \E p \in Processes : Enter(p) \/ Exit(p)

MutualExclusion == Cardinality(inCritical) <= 1
================================================
```

Bu modelde `Enter`, yalnızca kilit boşsa çalışabilir. `MutualExclusion` ise değişmezdir: Her durumda kritik bölgede en fazla bir süreç bulunmalıdır. Matematiksel karşılığı $|inCritical| \leq 1$ şeklindedir. TLC model denetleyicisi bu özelliği her erişilebilir durum için sınar. Eğer modelde bir geçiş unutulmuşsa ya da kilit yanlış güncellenmişse, TLC yalnızca “başarısız” demez; hataya götüren işlem sırasını da üretir.

## Güvenlik ve canlılık farkı

Dağıtık algoritmalarda yalnızca yanlış şeylerin olmaması yeterli değildir. Doğru şeylerin sonunda gerçekleşmesi de gerekir. Bu iki kavramı ayırmak çok değerlidir:

| Özellik türü | Soru | Örnek |
|---|---|---|
| Güvenlik (safety) | Kötü bir durum oluşabilir mi? | İki lider aynı anda seçilir mi? |
| Canlılık (liveness) | İyi bir olay sonunda olur mu? | Bekleyen istek sonunda yanıt alır mı? |
| Deadlock freedom | Sistem tamamen durabilir mi? | Hiçbir süreç ilerleyemez mi? |

Ölümcül kilitlenme, genellikle `Next` eylemlerinin hiçbirinin etkin olmadığı bir durumdur. Örneğin süreç A, B’nin tuttuğu kaynağı; B ise A’nın tuttuğu kaynağı bekliyorsa sistem ilerleyemez. TLA+ modelinde bu durum, erişilebilir bir durumda $\neg Enabled(Next)$ koşulunun sağlanmasıyla yakalanabilir.

Ancak küçük bir uyarı önemlidir: Model denetimi, modelinizin doğruluğunu kanıtlar; üretim kodunuzun doğrudan doğruluğunu değil. Bu nedenle ağ gecikmesi, mesaj kaybı, yeniden deneme ve çökme gibi varsayımları açıkça modele katmalısınız. İyi bir TLA+ spesifikasyonu, kodun kopyası değildir; kodun uyması gereken davranış sözleşmesidir. Böylece nadir görünen eşzamanlılık hataları, gece yarısı alarmı olmaktan çıkıp tasarım aşamasında yakalanan matematik problemlerine dönüşür.

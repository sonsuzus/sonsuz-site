---
layout: post
title: "Topolojik Sıralama ile Bağımlılık Çözümü ve Görev Zamanlama"
math: true
categories: 
  - Bilgi
tags: 
  - algoritmalar
  - graf teorisi
  - topolojik sıralama
---

Bir yazılım projesinde testleri çalıştırmadan önce kodu derlemek, derlemeden önce bağımlılıkları indirmek gerekir. Aynı mantık; ders ön koşullarında, üretim hattında, CI/CD süreçlerinde ve paket yöneticilerinde de karşımıza çıkar. İşte **topolojik sıralama**, “A tamamlanmadan B başlayamaz” türündeki kısıtları geçerli bir işlem dizisine dönüştüren graf algoritmasıdır.

``

Bu problemi yönlü grafikle modelliyoruz. Her görev bir **düğüm**dür; `A → B` kenarı ise A görevinin B'den önce bitmesi gerektiğini belirtir. Örneğin `derle → test` ilişkisi, testin derlemeye bağımlı olduğu anlamına gelir. Topolojik sıralama yalnızca **yönlü çevrimsiz graflarda** (DAG — Directed Acyclic Graph) mümkündür. Çünkü `A → B → C → A` gibi bir döngü varsa, her görev diğerini bekler: dijital bir “önce sen” çıkmazı!

Matematiksel olarak grafik $G=(V,E)$ olsun. Bir sıralama $\pi$, her yönlü kenar için aşağıdaki koşulu sağlamalıdır:

$$
(u,v) \in E \Rightarrow \pi(u) < \pi(v)
$$

Buradaki $\pi(u)$, u görevinin çıktıda bulunduğu konumdur. Birden fazla geçerli sıralama olabilir. Bağımsız iki görevin göreli yerleri çoğu zaman önemsizdir.

| Kavram | Anlamı | Zamanlama yorumu |
|---|---|---|
| Düğüm | İşlem veya görev | `lint`, `build`, `deploy` |
| Yönlü kenar | Önce-sonra kısıtı | `build → deploy` |
| Giriş derecesi | Göreve gelen kenar sayısı | Beklenen bağımlılık sayısı |
| DAG | Döngüsüz yönlü grafik | Çözülebilir plan |
| Döngü | Karşılıklı/kapalı bağımlılık | Hata veya tasarım sorunu |

En pratik yaklaşımlardan biri **Kahn algoritmasıdır**. Algoritma, giriş derecesi sıfır olan yani hiçbir şeyi beklemeyen görevleri bir kuyruğa koyar. Kuyruktan alınan her görev plana eklenir; onun çıkış kenarları kaldırılmış gibi davranılır ve komşularının giriş dereceleri azaltılır. Derecesi sıfıra düşen komşu artık çalışmaya hazırdır.

```python
from collections import defaultdict, deque

def topolojik_sirala(gorevler, bagimliliklar):
    # bagimliliklar: (onceki_gorev, sonraki_gorev) çiftleri
    grafik = defaultdict(list)
    giris_derecesi = {gorev: 0 for gorev in gorevler}

    for once, sonra in bagimliliklar:
        grafik[once].append(sonra)
        giris_derecesi[sonra] += 1

    kuyruk = deque(g for g in gorevler if giris_derecesi[g] == 0)
    plan = []

    while kuyruk:
        gorev = kuyruk.popleft()
        plan.append(gorev)

        for sonraki in grafik[gorev]:
            giris_derecesi[sonraki] -= 1
            if giris_derecesi[sonraki] == 0:
                kuyruk.append(sonraki)

    if len(plan) != len(gorevler):
        raise ValueError("Döngüsel bağımlılık tespit edildi!")

    return plan

print(topolojik_sirala(
    ["bagimliliklari_indir", "derle", "test", "paketle", "dagit"],
    [("bagimliliklari_indir", "derle"), ("derle", "test"),
     ("test", "paketle"), ("paketle", "dagit")]
))
```

Kodun kritik kontrolü `len(plan) != len(gorevler)` satırıdır. Döngüdeki düğümlerin giriş derecesi hiçbir zaman sıfıra inmez; dolayısıyla kuyruk erken boşalır. Bu durum sessizce yanlış bir plan üretmek yerine açık bir hata vermemizi sağlar.

| Yaklaşım | Ana fikir | Karmaşıklık | Güçlü yön |
|---|---|---:|---|
| Kahn | Giriş derecesi sıfır düğümleri seçilir | $O(|V|+|E|)$ | Döngü tespiti çok nettir |
| DFS tabanlı | Ziyaret sonrası düğüm yığına eklenir | $O(|V|+|E|)$ | Özyinelemeli ve kısa olabilir |

Gerçek zamanlama sistemlerinde topolojik sıra yalnızca başlangıçtır. Hazır görevler arasından en kısa süreni, en yüksek öncelikliyi veya kaynak tüketimi en düşük olanı seçebilirsiniz. Ancak hangi politika uygulanırsa uygulansın, topolojik sıralama bağımlılık ihlallerini engelleyen temel güvenlik ağıdır: önce temel, sonra katlar; önce derleme, sonra kutlama!

---
layout: post
title: "Git Rebase ve Merge Farkları: Geçmişinizi Şekillendiren Stratejiler"
math: true
categories: 
  - Bilgi
tags: 
  - git
  - rebase
  - merge
  - versiyon kontrol
toc: true
image: /img/git-rebase-ve-29.png
---

Git'te iki dalı bir araya getirmek yalnızca dosya değişikliklerini toplamak değildir; aynı zamanda projenin hikâyesini nasıl anlatacağınıza karar vermektir. `merge`, geçmişte yaşanan işbirliğini görünür tutan güvenli bir birleşim yaparken, `rebase` commit'leri başka bir başlangıç noktasına taşıyarak daha doğrusal bir tarihçe üretir. Doğru seçim; ekip düzenine, dalın paylaşılıp paylaşılmadığına ve hata ayıklama alışkanlıklarınıza bağlıdır.
``

## Git geçmişi bir grafik yapısıdır

Git commit geçmişini çoğu zaman liste gibi görsek de teknik olarak yönlendirilmiş çevrimsiz bir grafik (DAG) olarak saklar. Her commit, önceki commit'e işaret eder. Bir özellik dalı ana daldan ayrıldığında iki farklı gelişim yolu oluşur.

Basitçe, `main` dalındaki son commit'i $M$, özellik dalındaki son commit'i $F$ olarak düşünelim. Merge işlemi, iki ebeveyne sahip yeni bir $C_m$ commit'i üretir:

$$parents(C_m) = \{M, F\}$$

Rebase ise özellik dalındaki commit'leri kopyalayarak yeni commit kimlikleri oluşturur. Commit içeriği benzer kalsa bile ebeveyn işaretçisi değiştiği için hash de değişir. Yani rebase, geçmişi gerçekten **yeniden yazar**.

| Özellik | `git merge` | `git rebase` |
|---|---|---|
| Geçmiş yapısı | Dallanmayı korur | Doğrusal görünür |
| Yeni merge commit | Gerekebilir | Genellikle gerekmez |
| Commit hash'leri | Korunur | Değişir |
| Paylaşılan dal güvenliği | Yüksek | Dikkat gerektirir |
| Log okunabilirliği | Gerçekçi ama yoğun | Temiz ama yeniden yazılmış |

## Merge: İşbirliğinin tarihçesi

Özellik dalınızı `main` ile birleştirmek için tipik komut şöyledir:

```bash
git switch main
git pull origin main
git merge feature/login
```

Bu yaklaşım, `feature/login` dalının ne zaman ve hangi bağlamda entegre edildiğini saklar. Eğer `main` ve özellik dalı ayrıştıysa Git bir merge commit oluşturur. Bu commit, ekip içi kararların ve paralel geliştirmenin izini sürmek isteyen projeler için değerlidir.

Özellikle sürüm dalları, açık kaynak projeleri ve çok sayıda geliştiricinin aynı alanlarda çalıştığı depolarda merge güvenli bir varsayımdır. Çünkü başka birinin zaten çektiği commit'lerin kimliği değişmez. Çatışma varsa Git bunu birleşim anında çözdürür; çözüm de ayrı bir tarihsel olay olarak kayda geçer.

## Rebase: Temiz çizgi, güçlü sorumluluk

Özellik dalınızı güncel `main` üzerine taşımak için şunu kullanabilirsiniz:

```bash
git switch feature/login
git fetch origin
git rebase origin/main
```

Bu komut, özellik dalındaki commit'leri sırayla alır ve güncel `main` commit'inin üzerine yeniden uygular. Ortaya çıkan log, sanki özellik geliştirmesi `main`in en güncel hâlinden itibaren başlamış gibi görünür. Pull request incelemelerinde her commit'in mantıksal sırasını takip etmek bu nedenle kolaylaşır.

Rebase sırasında çatışma yaşarsanız akış nettir:

```bash
# Çatışan dosyaları düzenleyin
git add src/auth.js
git rebase --continue

# Gerekirse işlemi tamamen geri alın
git rebase --abort
```

Ancak altın kural şudur: **Başkalarının kullandığı ortak bir dalı rebase etmeyin.** Çünkü eski commit $C$ yerine yeni $C'$ oluşur ve $hash(C) \neq hash(C')$ olur. Uzak depoya gönderirken zorunlu push ihtiyacı doğabilir:

```bash
git push --force-with-lease origin feature/login
```

`--force-with-lease`, düz `--force` seçeneğine göre daha emniyetlidir; uzaktaki dal siz son gördüğünüz andan sonra değiştiyse gönderimi reddeder.

## Pratik karar rehberi

| Senaryo | Öneri | Neden |
|---|---|---|
| Kişisel, henüz paylaşılmamış özellik dalı | Rebase | Commit'leri temizlemek ve güncellemek kolaydır |
| Ana dal veya korumalı dal | Merge | Ortak geçmiş değişmeden kalır |
| Pull request öncesi hazırlık | Interactive rebase | Küçük commit'leri birleştirme imkânı verir |
| Karmaşık ekip entegrasyonu | Merge | Paralel çalışmanın bağlamını korur |

Sonuçta merge ve rebase rakip değil, farklı hikâye anlatım araçlarıdır. Yerel dalınızda rebase ile düzen kurup, paylaşılan dallarda merge ile güvenliği korumak çoğu ekip için dengeli bir stratejidir. En iyi Git geçmişi en düz olan değil; ekibin gerektiğinde anlayabildiği, geri alabildiği ve güvenle geliştirebildiği geçmişidir.

![git-rebase-ve-29](/img/git-rebase-ve-29.svg)


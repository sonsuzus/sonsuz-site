---
layout: post
title: "Git’te İleri Seviye Conflict Çözümü: Lineer ve Güvenli Bir Zaman Çizelgesi"
math: true
categories: 
  - Bilgi
tags: 
  - git
  - versiyon kontrol
  - conflict çözümü
toc: true
---

Birden fazla dal aynı dosyaların aynı bölgelerine dokunduğunda Git, hangi değişikliğin doğru olduğuna karar veremez ve conflict üretir. İleri seviye çözümün amacı yalnızca kırmızı uyarıları susturmak değildir; değişikliklerin anlamını korumak, geçmişi okunabilir tutmak ve hatalı kodun ana dala sızmasını engellemektir. Bunun için küçük commit’ler, kontrollü rebase ve otomatik testlerden oluşan güvenli bir iş akışı gerekir.
``
Git geçmişini yönlü ve döngüsüz bir grafik, yani DAG olarak düşünmek faydalıdır. Her commit bir düğüm, parent bağlantıları ise kenarlardır. Bir dalın ana daldan uzaklığını kabaca

$$D = A + B$$

şeklinde modelleyebiliriz. Burada $A$, yalnızca ana dalda; $B$ ise yalnızca özellik dalında bulunan commit sayısıdır. $D$ büyüdükçe aynı kodun farklı yönlerde değişme olasılığı ve conflict maliyeti artar. Bu yüzden uzun ömürlü dalları düzenli olarak güncellemek önemlidir.

## Merge mi, Rebase mi?

| Yöntem | Geçmiş | Güçlü yanı | Temel risk |
|---|---|---|---|
| `merge` | Dallanmayı açıkça gösterir | Paylaşılan dallarda güvenlidir | Fazla merge commit’i oluşturabilir |
| `rebase` | Commit’leri lineer sıralar | İnceleme ve `git bisect` kolaylaşır | Commit kimliklerini yeniden yazar |
| `squash merge` | Tek commit üretir | Gürültülü özellik dallarını temizler | Ara commit bağlamını kaybettirir |
| `cherry-pick` | Seçili commit’i taşır | Hedefli düzeltmeler için idealdir | Aynı değişiklik farklı kimliklerle çoğalabilir |

Lineer geçmiş isteniyorsa özellik dalı, birleştirmeden hemen önce güncel ana dalın üzerine taşınabilir:

```bash
git fetch origin
git switch feature/payment
git rebase origin/main
```

`fetch`, uzak durumun güncel görüntüsünü alır; `rebase` ise özellik commit’lerini `main` dalının sonuna sırayla uygular. Conflict oluşursa önce problemli dosyalar düzeltilir, ardından işlem sürdürülür:

```bash
git status
git diff --name-only --diff-filter=U
# Dosyaları düzenle ve test et
git add src/payment.ts
git rebase --continue
```

Buradaki kritik nokta, `<<<<<<<`, `=======` ve `>>>>>>>` işaretlerini mekanik biçimde silmemektir. “Bizim sürüm” ve “onların sürümü” ifadeleri rebase sırasında sezgisel anlamını değiştirebilir. Önce `git status` çıktısını okuyun; ardından iki değişikliğin iş kuralını birlikte değerlendirin.

## Conflict’i Commit Commit Çözmek

Büyük bir dalı tek seferde merge etmek yerine rebase ile her commit’i ayrı uygulamak, hatanın kaynağını küçültür. Gerekirse süreç güvenle geri alınabilir:

```bash
git rebase --abort
```

Commit sırasını düzeltmek, gereksiz commit’leri birleştirmek veya problemli bir commit’i parçalamak için etkileşimli rebase kullanılabilir:

```bash
git rebase -i origin/main
```

Listede `pick`, `reword`, `squash`, `fixup` ve `edit` komutları bulunur. Ancak bu işlem yalnızca kişisel veya ekipçe yeniden yazılacağı kararlaştırılmış dallarda yapılmalıdır. Paylaşılan bir dalı sessizce rebase etmek, ekip arkadaşlarının geçmişini koparır.

## Tekrarlanan Çakışmaları Git’e Öğretmek

Aynı conflict birkaç rebase sırasında yeniden ortaya çıkıyorsa `rerere`, önceki çözümü kaydedip tekrar uygulayabilir:

```bash
git config --global rerere.enabled true
```

Bu özellik özellikle uzun süren dal geçişlerinde zaman kazandırır; yine de önerilen çözüm test edilmeden kabul edilmemelidir. Git metinsel benzerliği hatırlar, iş mantığını değil.

## Güvenli Doğrulama Zinciri

Conflict çözüldükten sonra yalnızca projenin derlenmesi yeterli değildir. Güvenli sıra şöyledir:

1. Conflict işaretlerini `git grep -n '<<<<<<<'` ile ara.
2. Formatter, linter ve birim testlerini çalıştır.
3. Entegrasyon testleriyle dalların birlikte davranışını doğrula.
4. Değişen commit dizisini `git range-diff origin/main...feature@{1} origin/main...feature` ile karşılaştır.
5. Yeniden yazılmış dalı yalnızca `git push --force-with-lease` ile gönder.

`--force-with-lease`, uzaktaki dal beklenmedik biçimde değişmişse push işlemini reddeder; çıplak `--force` ise başkasının commit’lerini ezebilir. Son aşamada korumalı ana dal, zorunlu kod incelemesi ve başarılı CI kontrolleri kullanılmalıdır. Böylece lineer zaman çizelgesi estetik bir tercih olmaktan çıkar; geri alınabilir, denetlenebilir ve hataya dayanıklı bir teslimat mekanizmasına dönüşür.

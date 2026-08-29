---
layout: post
title: "Git Bisect: Hatayı Getiren Commit’i Dedektif Gibi Bulun"
math: true
categories: 
  - Bilgi
tags: 
  - git
  - git bisect
  - hata ayıklama
toc: true
---

Bir projenin dün çalışan, bugün ise gizemli biçimde çöken bir sürümünü düşünün. Yüzlerce commit arasından “suçlu” değişikliği tek tek incelemek hem sabır hem de kahve tüketimi gerektirir. `git bisect`, bu işi ikili arama algoritmasıyla otomatikleştirir: Bildiğiniz iyi ve kötü commit’ler arasındaki geçmişi bölerek hatayı oluşturan ilk commit’i bulur.
``

## Temel fikir: Commit geçmişinde ikili arama

`git bisect` için iki başlangıç noktası yeterlidir:

- **Good (iyi):** Hatanın kesinlikle olmadığı bir commit.
- **Bad (kötü):** Hatanın kesinlikle bulunduğu bir commit.

Araç, bu iki nokta arasındaki commit’lerden ortalara yakın birini seçer. Siz bu sürümü test edip sonucu `good` veya `bad` diye işaretlersiniz. Sonra arama alanı yarıya iner. Bu yaklaşım klasik ikili aramanın Git geçmişine uygulanmış hâlidir.

Arada $n$ commit varsa, doğrusal incelemede en kötü durumda $n$ test gerekir. Bisect ile gereken test sayısı yaklaşık olarak şudur:

$$T \approx \lceil \log_2(n) \rceil$$

Örneğin 1.024 commit’lik bir aralık için yaklaşık 10 test yeterlidir. 1.024 farklı değişikliği sırayla kontrol etmek yerine, yalnızca 10 kez “hata var mı?” sorusunu yanıtlamak oldukça iyi bir anlaşmadır.

| Yöntem | Yaklaşık test sayısı | Ne zaman tercih edilir? |
|---|---:|---|
| Tek tek commit inceleme | $n$ | Çok küçük geçmişler, bağlamsal kod incelemesi |
| `git bisect` | $\log_2(n)$ | Tekrarlanabilir hata, geniş commit aralığı |
| `git blame` | Dosya/satır odaklı | Hatalı satır zaten biliniyorsa |

## Manuel bisect akışı

Önce çalışma alanınızın temiz olduğundan emin olun; gerekirse değişiklikleri commit edin veya `git stash` kullanın. Ardından bisect oturumunu başlatın ve kötü/iyi commit’leri tanımlayın:

```bash
# İkili arama oturumunu başlatır
git bisect start

# Mevcut HEAD sürümünde hata olduğunu belirtir
git bisect bad

# Hatanın olmadığı bilinen eski commit'i işaretler
git bisect good a1b2c3d
```

Git şimdi test etmeniz için bir orta commit’e geçer. Uygulamayı çalıştırın, testi yapın ve sonucu bildirin:

```bash
# Bu commit'te hata hâlâ varsa
git bisect bad

# Bu commit'te hata yoksa
git bisect good
```

Her komuttan sonra Git yeni bir aday commit seçer. Sonunda “is the first bad commit” mesajıyla sorumlu commit’i, yazarını ve değişen dosyaları gösterir. İnceleme bittiğinde normal dalınıza dönmek için mutlaka şunu çalıştırın:

```bash
# Bisect durumunu kapatır ve başlangıçtaki HEAD'e döner
git bisect reset
```

## Otomasyon: Test komutunu Git’e devretmek

Manuel yöntemde her adımda uygulamayı siz test edersiniz. Ancak hata bir test komutuyla güvenilir biçimde yakalanabiliyorsa `git bisect run` çok daha etkilidir. Git, her aday commit’te komutu çalıştırır ve çıkış koduna göre karar verir:

```bash
# 0: iyi commit, 1-127 arası: kötü commit
# Test paketi başarısızsa ilgili commit kötü kabul edilir
git bisect start HEAD v2.3.0
git bisect run npm test -- --runInBand
```

Burada `v2.3.0`, testlerin geçtiği etikettir; `HEAD` ise hatalı sürümdür. Genel kural basittir: çıkış kodu `0` ise iyi, `1` ile `127` arasındaysa kötü kabul edilir. Derlenmeyen veya bağımlılığı eksik bir commit’i aramadan hariç tutmak için `git bisect skip` kullanabilirsiniz.

| Durum | Kullanılacak komut | Anlamı |
|---|---|---|
| Test geçti | `git bisect good` | Hata bu commit’te yok |
| Test başarısız | `git bisect bad` | Hata bu commit’te var |
| Test edilemiyor | `git bisect skip` | Commit hakkında güvenilir karar yok |

Sonuç olarak `git bisect`, “hangi commit bozdu?” sorusunu tahminden ölçülebilir bir sürece dönüştürür. En iyi sonucu almak için testinizin deterministik olmasına dikkat edin: Ağ, saat, rastgele veri veya paylaşılan veritabanı gibi değişkenler yanlış sınıflandırmaya yol açabilir. Güvenilir bir test ve doğru iyi-kötü sınırlarıyla Git, tarihçenizdeki suçluyu dakikalar içinde bulur.

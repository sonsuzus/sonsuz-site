---
layout: post
title: "Git Hooks ile Otomasyon: Commit ve Push İşlemlerini Güvenceye Alın"
math: true
categories: 
  - Bilgi
tags: 
  - git
  - git hooks
  - otomasyon
---

Bir projede hatalı biçimlendirilmiş kodun, çalışmayan testlerin veya yanlışlıkla eklenmiş gizli anahtarların depoya ulaşması oldukça can sıkıcıdır. Kod incelemesi bu sorunların bir kısmını yakalasa da insan dikkati sınırlıdır. Git Hooks, Git olayları gerçekleştiğinde çalışan küçük betiklerle bu kontrolü otomatikleştirir. Böylece commit ve push süreci yalnızca bir kayıt işlemi değil, kalite kapısından geçen kontrollü bir akış hâline gelir.


Git hook’ları, yerel depodaki `.git/hooks` dizininde bulunan çalıştırılabilir dosyalardır. Git belirli bir olayı algıladığında ilgili dosyayı çağırır. Örneğin `pre-commit`, commit nesnesi oluşturulmadan hemen önce; `pre-push` ise uzak depoya veri gönderilmeden önce çalışır. Temel fikir basittir: betik `0` ile çıkarsa işlem sürer, sıfır dışı bir çıkış kodu üretirse Git işlemi durdurur.

`` 

Bu davranışı mantıksal olarak şöyle ifade edebiliriz:

$$
İşlem = \begin{cases}
Devam & \text{eğer } exit\_code = 0 \\
Engelle & \text{eğer } exit\_code \neq 0
\end{cases}
$$

Bu küçük kural, ekip standartlarını tekrarlanabilir bir sözleşmeye dönüştürür. Geliştirici, “testleri çalıştırmayı unutmuş olabilir miyim?” diye düşünmek yerine, Git’in bunu hatırlatmasına güvenebilir.

| Hook | Ne zaman çalışır? | Tipik kullanım |
|---|---|---|
| `pre-commit` | Commit oluşmadan önce | Lint, biçimlendirme, gizli anahtar taraması |
| `commit-msg` | Commit mesajı yazıldıktan sonra | Conventional Commits doğrulaması |
| `pre-push` | Push başlamadan önce | Test paketi, tür kontrolü, derleme |
| `post-commit` | Commit tamamlandıktan sonra | Bildirim veya yerel kayıt güncelleme |

Örneğin JavaScript projesinde `pre-commit` hook’u ile yalnızca stage alanındaki dosyaları denetlemek, tüm projeyi her seferinde taramaktan daha hızlıdır. Aşağıdaki Bash betiği, staged JavaScript ve TypeScript dosyalarında ESLint çalıştırır:

```bash
#!/usr/bin/env bash

FILES=$(git diff --cached --name-only --diff-filter=ACM \vert  grep -E '\.(js\vert ts)$')

if [ -z "$FILES" ]; then
  exit 0
fi

npx eslint $FILES
STATUS=$?

if [ $STATUS -ne 0 ]; then
  echo "Commit engellendi: Lint hatalarını düzeltin."
  exit 1
fi
```

Bu dosyayı `.git/hooks/pre-commit` adıyla kaydedip çalıştırılabilir yapmak gerekir:

```bash
chmod +x .git/hooks/pre-commit
```

Betik önce stage alanındaki uygun dosyaları bulur. Dosya yoksa boşuna araç çalıştırmadan başarıyla çıkar. ESLint hata üretirse `exit 1` sayesinde Git commit’i iptal eder. Buradaki amaç geliştiriciyi cezalandırmak değil, hatayı en ucuz aşamada yakalamaktır. Bir hata uzak depoya, CI kuyruğuna ve takım arkadaşlarının çalışma alanına ulaşmadan çözülür.

`pre-push` için denetimler daha kapsamlı olabilir. Örneğin birim testleri ve tür kontrolü çalıştırılabilir:

```bash
#!/usr/bin/env bash

echo "Push öncesi kontroller çalışıyor..."
npm run typecheck && npm test

if [ $? -ne 0 ]; then
  echo "Push engellendi: Test veya tür kontrolü başarısız."
  exit 1
fi
```

| Yaklaşım | Avantaj | Dikkat edilmesi gereken |
|---|---|---|
| Yerel hook | Hızlı geri bildirim, düşük CI maliyeti | Hook dosyaları varsayılan olarak Git ile paylaşılmaz |
| CI denetimi | Merkezi ve zorunlu doğrulama | Sonuç için uzak sunucu beklenir |
| İkisini birlikte kullanmak | Erken uyarı ve güçlü güvence | Aynı kontrollerin süresi yönetilmelidir |

Önemli bir ayrıntı: `.git/hooks` dizini normalde sürüm kontrolüne dahil değildir. Ekip genelinde aynı kuralları uygulamak için Husky, Lefthook gibi araçlar kullanılabilir veya hook betikleri proje içinde örneğin `.githooks/` altında tutulup `git config core.hooksPath .githooks` komutuyla etkinleştirilebilir. Ayrıca hook’ların atlanabileceğini unutmayın: `git commit --no-verify` yerel kontrolleri geçebilir. Bu nedenle kritik kuralların CI tarafında da doğrulanması gerekir.

İyi bir hook hızlı, anlaşılır ve eyleme dönük hata mesajları verir. Biçimlendirme için otomatik düzeltme, commit mesajı için açık örnekler ve ağır testler için `pre-push` tercihi geliştirici deneyimini korur. Doğru tasarlandığında Git Hooks, görünmez ama disiplinli bir takım arkadaşı gibi çalışır: yanlışları erkenden yakalar, standartları korur ve daha güvenli bir teslimat hattı oluşturur.

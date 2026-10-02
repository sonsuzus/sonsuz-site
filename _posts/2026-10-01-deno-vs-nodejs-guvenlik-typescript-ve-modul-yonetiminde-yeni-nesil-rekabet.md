---
layout: post
title: "Deno vs Node.js: Güvenlik, TypeScript ve Modül Yönetiminde Yeni Nesil Rekabet"
math: true
categories: 
  - Bilgi
tags: 
  - deno
  - nodejs
  - typescript
  - javascript
  - güvenlik
  - backend
  - modül-yönetimi
toc: true
image: /img/deno-vs-nodejs-25.png
---

Node.js’in yaratıcısı Ryan Dahl, yıllar sonra bazı tasarım kararlarından pişman olduğunu açıkladı ve bu deneyimden doğan fikirlerle Deno’yu geliştirdi. Deno; varsayılan güvenlik kısıtlamaları, yerleşik TypeScript desteği ve URL tabanlı modül sistemiyle JavaScript çalışma ortamlarına daha modern bir yaklaşım getiriyor. Peki bunlar gerçek projelerde ne kadar fark yaratıyor?

``

## Aynı motor, farklı felsefe

Node.js ve Deno, JavaScript kodunu çalıştırmak için Google’ın geliştirdiği V8 motorundan yararlanır. Bununla birlikte çalışma ortamının sunduğu API’ler ve güvenlik modeli farklıdır.

Bir çalışma ortamını basitçe şu bileşenlerle düşünebiliriz:

$$
R = V8 + API + I/O + M
$$

Burada $R$ çalışma ortamını, $I/O$ dosya ve ağ işlemlerini, $M$ ise modül yönetimini temsil eder. İki platform aynı V8 motorunu kullansa da denklemin diğer parçalarını farklı biçimde tasarlar.

| Özellik | Node.js | Deno |
|---|---|---|
| Varsayılan dosya erişimi | Serbest | Engelli |
| TypeScript | Genellikle ek araç gerekir | Yerleşik destek |
| Klasik modül yaklaşımı | npm ve `node_modules` | URL, JSR ve npm uyumluluğu |
| Paket yapılandırması | Çoğunlukla `package.json` | İsteğe bağlı `deno.json` |
| Standart web API’leri | Giderek genişliyor | Tasarımın merkezinde |

## Güvenlik: Önce izin iste

Node.js uygulamaları geleneksel olarak çalıştırıldıkları kullanıcının yetkileri kapsamında dosyalara, çevre değişkenlerine ve ağa erişebilir. Bu yaklaşım kullanışlıdır; ancak güvenilmeyen bir bağımlılık kötü niyetliyse risk oluşturabilir.

Deno ise varsayılan olarak korumalı bir alanda çalışır. Aşağıdaki program bir dosyayı okumayı dener:

```typescript
const text = await Deno.readTextFile("notlar.txt");
console.log(text);
```

Program normal biçimde başlatılırsa izin hatası verir. Yalnızca gerekli dosya için erişim tanımlanabilir:

```bash
deno run --allow-read=notlar.txt uygulama.ts
```

Ağ erişimi için `--allow-net`, çevre değişkenleri için `--allow-env` kullanılır. Teorik olarak saldırı yüzeyini $A$, verilen yetki sayısını $P$ ile gösterirsek kabaca $A \propto P$ diyebiliriz. Daha az izin, daha küçük bir saldırı yüzeyi demektir. Elbette geliştirici her şeyi açan izinler verirse bu avantaj büyük ölçüde kaybolur.

## TypeScript deneyimi

Node.js ekosisteminde TypeScript projeleri tarihsel olarak `typescript`, `ts-node` veya bir derleme aracı yapılandırmayı gerektirir. Modern Node.js sürümleri belirli TypeScript sözdizimlerini doğrudan çalıştırabilse de tam özellik desteği ve sürüm uyumluluğu dikkat ister.

Deno’da `.ts` dosyaları doğal iş akışının parçasıdır:

```typescript
interface User {
  name: string;
  score: number;
}

const formatUser = (user: User): string =>
  `${user.name}: ${user.score}`;

console.log(formatUser({ name: "Ada", score: 95 }));
```

Bu kod `deno run app.ts` komutuyla çalıştırılabilir. Ayrıca `deno check`, kodu çalıştırmadan tür denetimi yapar. Böylece küçük projelerde yapılandırma yükü azalır.

## Modül yönetimi: Klasör mü, adres mi?

Node.js’in başarısında npm’in dev paket ekosistemi kritik rol oynar. Ancak büyük `node_modules` klasörleri, dolaylı bağımlılıklar ve sürüm çakışmaları meşhur sorunlardır.

Deno başlangıçta tarayıcıları andıran URL tabanlı içe aktarmayı benimsedi:

```typescript
import { serve } from "https://deno.land/std/http/server.ts";

serve(() => new Response("Merhaba Deno!"));
```

URL yaklaşımı kaynağı açıkça gösterir, fakat uzun adresler ve kaynağın değişmezliğini doğrulama ihtiyacı yönetimi zorlaştırabilir. Güncel Deno; JSR paket kayıt sistemini, kilit dosyalarını ve `npm:` belirteci üzerinden npm paketlerini de destekler. Yani rekabet artık “npm veya URL” kadar keskin değildir.

## Hangisini seçmeli?

Node.js; dev ekosistemi, olgun araçları ve geniş barındırma desteğiyle mevcut kurumsal projelerde güçlü seçimdir. Deno ise güvenli varsayımlar, sade TypeScript deneyimi ve web standartlarına yakın API’ler isteyen yeni projelerde parlar. Kısacası Node.js köklü metropol, Deno ise güvenlik kapıları baştan kurulmuş modern bir şehir gibidir. Seçim, projenin ihtiyaçları ve ekibin alışkanlıklarıyla yapılmalıdır.

![deno-vs-nodejs-25](/img/deno-vs-nodejs-25.svg)


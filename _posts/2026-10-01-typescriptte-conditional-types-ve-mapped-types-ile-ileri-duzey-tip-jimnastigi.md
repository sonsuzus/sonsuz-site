---
layout: post
title: "TypeScript’te Conditional Types ve Mapped Types ile İleri Düzey Tip Jimnastiği"
math: true
categories: 
  - Bilgi
tags: 
  - typescript
  - conditional-types
  - mapped-types
  - tip-sistemi
  - yazılım-geliştirme
  - statik-analiz
toc: true
image: /img/typescriptte-conditional-types-79.png
---

TypeScript’in tip sistemi yalnızca `string` veya `number` yazıp hataları erkenden yakalamaktan ibaret değildir. Conditional Types ve Mapped Types sayesinde tipler üzerinde koşul çalıştırabilir, koleksiyonları dönüştürebilir ve API sözleşmelerini otomatik üretebiliriz. Başka bir deyişle derleyiciye küçük ama son derece titiz bir program yazdırırız; üstelik bu program çalışma zamanında değil, kod daha çalışmadan önce görev yapar.

``

## Tip seviyesinde programlama mantığı

Normal bir programda değerler girdi, fonksiyonlar ise dönüşüm aracıdır. Tip seviyesinde programlamada girdiler türlerdir ve sonuç yine bir türdür. Bunu matematiksel olarak $f(T) = U$ biçiminde düşünebiliriz. Conditional Type bir `if-else`, Mapped Type ise anahtarlar üzerinde çalışan bir `for` döngüsü gibi davranır.

| Çalışma zamanı yapısı | Tip sistemi karşılığı | Amaç |
|---|---|---|
| `if / else` | Conditional Type | Tür seçmek |
| `for...in` | Mapped Type | Özellikleri dönüştürmek |
| Geçici değişken | `infer` | Tür parçasını çıkarmak |
| Fonksiyon zinciri | İç içe tipler | Dönüşümleri birleştirmek |

![typescriptte-conditional-types-79](/img/typescriptte-conditional-types-79.svg)


Bu benzetme birebir uygulama değildir; tipler JavaScript çıktısında silinir. Kazancımız çalışma zamanı performansı değil, güçlü statik doğrulamadır.

## Conditional Types: Derleyicinin karar mekanizması

Temel sözdizimi şöyledir:

```ts
type IsString<T> = T extends string ? true : false;

type A = IsString<"merhaba">; // true
type B = IsString<42>;         // false
```

Buradaki `extends`, sınıf kalıtımından çok “bu tipe atanabilir mi?” sorusunu sorar. Genel formülümüz $T \subseteq U$ ise birinci dal, değilse ikinci daldır.

`infer` anahtar sözcüğü ise eşleşen yapının içinden tür çıkarmamızı sağlar:

```ts
type FunctionResult<T> =
  T extends (...args: any[]) => infer R ? R : never;

const loadUser = () => ({ id: 1, name: "Ada" });
type User = FunctionResult<typeof loadUser>;
// { id: number; name: string }
```

Bu tip, fonksiyonun dönüş değerini elle tekrar yazma ihtiyacını ortadan kaldırır. Fonksiyon değiştiğinde sözleşme de otomatik güncellenir.

Conditional Types birleşim tiplerine dağıtılabilir. `T = A | B` için dönüşüm kabaca $F(A \vert  B) = F(A) \vert  F(B)$ şeklinde gerçekleşir:

```ts
type OnlyStrings<T> = T extends string ? T : never;
type Result = OnlyStrings<string | number | boolean>;
// string
```

Dağılım istenmiyorsa iki tarafı tuple içine alabiliriz: `[T] extends [U]`. Bu küçük köşeli parantezler bazen saatlerce sürecek bir tip bulmacasını saniyeler içinde çözer.

## Mapped Types: Özellikler üzerinde döngü

Mapped Types, `keyof` ile elde edilen anahtarları dolaşır:

```ts
type Nullable<T> = {
  [K in keyof T]: T[K] | null;
};

type User = { id: number; name: string };
type NullableUser = Nullable<User>;
```

`K`, her turdaki özellik anahtarıdır; `T[K]` ise o özelliğin türüdür. `readonly`, opsiyonellik ve anahtar adları da değiştirilebilir.

| Operatör | Etki |
|---|---|
| `+?` veya `?` | Özelliği opsiyonel yapar |
| `-?` | Opsiyonelliği kaldırır |
| `readonly` | Değiştirmeyi engeller |
| `-readonly` | Değiştirilebilir yapar |
| `as` | Anahtarı yeniden adlandırır veya eler |

Örneğin yalnızca fonksiyon özelliklerini seçebiliriz:

```ts
type MethodsOnly<T> = {
  [K in keyof T as T[K] extends Function ? K : never]: T[K]
};

type Service = {
  url: string;
  start(): void;
  stop(): void;
};

type ServiceMethods = MethodsOnly<Service>;
// { start(): void; stop(): void }
```

Burada Conditional Type filtreyi, Mapped Type döngüyü gerçekleştirir. `never` üreten anahtarlar sonuçtan çıkarılır.

## Kırılmaz API sözleşmesi örneği

Bir modelden otomatik güncelleme girdisi üretelim; `id` değiştirilemesin, diğer alanlar opsiyonel olsun:

```ts
type UpdatePayload<T extends { id: unknown }> = {
  [K in keyof T as K extends "id" ? never : K]?: T[K]
};

type Product = {
  id: number;
  title: string;
  price: number;
  active: boolean;
};

type ProductUpdate = UpdatePayload<Product>;
// { title?: string; price?: number; active?: boolean }
```

Model genişlediğinde güncelleme tipi de genişler; unutulmuş alanlar ve kopyala-yapıştır hataları azalır. Yine de aşırı karmaşık tipler derleyiciyi yavaşlatabilir ve hata mesajlarını okunmaz hâle getirebilir. İyi tip jimnastiğinin amacı en kısa akrobatik çözüm değil, değişikliklere dayanıklı ve ekipçe anlaşılabilir bir sözleşme kurmaktır.

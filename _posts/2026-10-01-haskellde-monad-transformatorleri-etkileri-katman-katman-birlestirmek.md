---
layout: post
title: "Haskell'de Monad Transformatörleri: Etkileri Katman Katman Birleştirmek"
math: true
categories: 
  - Bilgi
tags: 
  - haskell
  - monad
  - monad-transformer
  - fonksiyonel-programlama
  - state
  - either
  - io
toc: true
image: /img/haskellde-monad-transformatorleri-62.png
---

![haskellde-monad-transformatorleri-62](/img/haskellde-monad-transformatorleri-62.svg)


Bir program aynı anda durum tutmak, hata üretmek ve dış dünyayla konuşmak isteyebilir. Haskell ise bu etkileri görünmez mutasyonlarla birbirine karıştırmak yerine açıkça modellemeyi tercih eder. Monad transformatörleri, farklı etkileri LEGO parçaları gibi üst üste koyarak tek bir hesaplama bağlamında kullanmamızı sağlar.

``

## Neden tek bir monad yetmiyor?

`State s a`, durum taşıyan ve sonunda `a` üreten bir hesaplamadır. `Either e a`, başarısız olabilen bir sonucu; `IO a` ise dış dünyayla etkileşimi temsil eder. Bunların sadeleştirilmiş matematiksel görünümleri şöyledir:

$$
State\ s\ a \cong s \rightarrow (a, s)
$$

$$
Either\ e\ a \cong Left\ e \mid Right\ a
$$

Bir işlevin hem durum hem hata hem de IO kullanması gerektiğinde şu türde özel bir yapı yazabiliriz:

$$
s \rightarrow IO\,(Either\ e\,(a,s))
$$

Fakat her etki birleşimi için yeni bir monad ve yeni `Functor`, `Applicative`, `Monad` örnekleri yazmak sıkıcıdır. Monad transformatörleri bu mekanik işi genelleştirir.

| Etki | Temel monad | Transformatör | Temel işlem |
|---|---|---|---|
| Durum | `State s` | `StateT s m` | `get`, `put`, `modify` |
| Hata | `Either e` | `ExceptT e m` | `throwError`, `catchError` |
| IO | `IO` | Genellikle en altta | `liftIO` |

## Katmanların matematiği

`StateT` kabaca aşağıdaki yapıya sahiptir:

$$
StateT\ s\ m\ a \cong s \rightarrow m\,(a,s)
$$

Buradaki `m`, başka bir monaddır. Onu `ExceptT String IO` seçersek durum sonucumuz hata ve IO katmanlarının içine yerleşir:

```haskell
type AppM = StateT Int (ExceptT String IO)
```

Böylece `AppM a`, sezgisel olarak şu anlama gelir:

$$
Int \rightarrow IO\,(Either\ String\,(a,Int))
$$

`StateT`, durumu; `ExceptT`, hatayı; `IO` ise gerçek dünya etkileşimini yönetir. Dış katmandaki işlemler doğrudan kullanılabilirken alt katmana ulaşmak için kaldırma, yani `lift` gerekir. IO işlemleri için `liftIO` bu işi daha okunaklı yapar.

## Çalışan bir örnek

Aşağıdaki program bakiyeyi durum olarak tutuyor, geçersiz harcamalarda hata veriyor ve işlemleri ekrana yazıyor:

```haskell
{-# LANGUAGE FlexibleContexts #-}

import Control.Monad.State
import Control.Monad.Except
import Control.Monad.IO.Class

type AppM = StateT Int (ExceptT String IO)

harca :: Int -> AppM ()
harca miktar = do
  bakiye <- get
  if miktar <= 0
    then throwError "Miktar pozitif olmalı"
    else if miktar > bakiye
      then throwError "Yetersiz bakiye"
      else do
        put (bakiye - miktar)
        liftIO $ putStrLn (show miktar ++ " TL harcandı")

program :: AppM ()
program = do
  harca 30
  harca 50
  kalan <- get
  liftIO $ putStrLn ("Kalan: " ++ show kalan)

main :: IO ()
main = do
  sonuc <- runExceptT (runStateT program 100)
  print sonuc
```

`runStateT program 100`, hesaplamaya başlangıç durumu olarak `100` verir. Sonuç hâlâ `ExceptT` içinde olduğu için `runExceptT` ile hata katmanı da açılır. Başarılı çıktı yaklaşık olarak `Right ((),20)` olur.

## Katman sırası neden önemli?

Transformatörler genel olarak değişmeli değildir:

$$
StateT\ s\,(ExceptT\ e\,IO) \not\cong ExceptT\ e\,(StateT\ s\,IO)
$$

| Yığın | Hata oluştuğunda durum |
|---|---|
| `StateT s (ExceptT e IO)` | Son durum genellikle kaybolur |
| `ExceptT e (StateT s IO)` | Hata yanında son durum korunabilir |

İlk düzende hata oluşursa `(a, s)` çifti üretilemez. İkinci düzende ise `StateT`, `Left e` sonucunu da durumla birlikte taşıyabilir. Dolayısıyla katman sırası yalnızca sözdizimi değil, programın anlamıdır.

Monad transformatörlerinin zarafeti, etkileri yok etmekte değil, sınırlarını görünür kılmaktadır. Tür imzası programın hangi güçlere sahip olduğunu söyler; çalıştırıcı fonksiyonlar da bu etkileri kontrollü biçimde katman katman açar.

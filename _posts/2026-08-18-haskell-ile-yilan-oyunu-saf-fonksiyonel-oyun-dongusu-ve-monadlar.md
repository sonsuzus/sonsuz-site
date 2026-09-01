---
layout: post
title: "Haskell ile Yılan Oyunu: Saf Fonksiyonel Oyun Döngüsü ve Monadlar"
math: true
categories: 
  - Proje
tags: 
  - haskell
  - fonksiyonel programlama
  - oyun geliştirme
toc: true
image: /img/haskell-ile-yilan-99.png
---

Yılan oyunu, küçük görünmesine rağmen oyun programlamasının en önemli sorularını barındırır: Zaman nasıl ilerler, klavye girdisi nasıl alınır, rastgele yem nereye çıkar ve ekran nasıl çizilir? Haskell bu sorulara ilginç bir ayrım getirir: Oyunun **kuralları** saf fonksiyonlarda yaşar; klavye, saat, rastgelelik ve terminal gibi dış dünya ayrıntıları ise kontrollü biçimde `IO` içinde tutulur. Böylece test edilebilir, tahmin edilebilir ve genişletilebilir bir oyun döngüsü elde ederiz.
``

## Önce durum: Oyunun tamamı bir değer

Saf fonksiyonel tasarımda gizli, değiştirilebilir global değişkenler yerine oyunun tüm anlık bilgisi tek bir veri yapısında tutulur. Her karede eski durum alınır, yeni durum üretilir. Matematiksel olarak oyun adımı şöyle düşünülebilir:

$$S_{t+1} = \operatorname{update}(I_t, R_t, S_t)$$

Burada $S_t$ oyun durumu, $I_t$ kullanıcı girdisi ve $R_t$ ise rastgelelikten gelen bilgidir. Kritik nokta şudur: `update`, dış dünyaya dokunmadan sonuç üretirse aynı girdiler için her zaman aynı sonucu verir.

```haskell
type Pos = (Int, Int)

data Direction = Up | Down | Left | Right
  deriving (Eq, Show)

data Game = Game
  { snake     :: [Pos]
  , direction :: Direction
  , food      :: Pos
  , alive     :: Bool
  } deriving Show
```

Bu modelde listenin başı yılanın kafasıdır. `Game` değeri, ekran çizimi için gereken her şeyi taşır; dolayısıyla bir hata oluştuğunda belirli bir durumu kaydedip sonradan yeniden oynatmak da mümkündür.

| Yaklaşım | Durum nerede yaşar? | Test etme | Hata ayıklama |
|---|---|---|---|
| Değişken tabanlı döngü | Global veya mutable nesnelerde | Zor | Geçmiş durum kaybolabilir |
| Saf durum dönüşümü | `Game` değerinde | Kolay | Durumlar kaydedilebilir |

## Saf hareket ve çarpışma kuralları

Yılanın bir hücre ilerlemesi, tamamen saf bir dönüşümdür. Yem yenirse kuyruk korunur; yenmezse son eleman atılır. Bu kararın içinde ne terminal ne de `IO` bulunur.

```haskell
nextPos :: Direction -> Pos -> Pos
nextPos Up    (x, y) = (x, y - 1)
nextPos Down  (x, y) = (x, y + 1)
nextPos Left  (x, y) = (x - 1, y)
nextPos Right (x, y) = (x + 1, y)

step :: Game -> Game
step game = game { snake = newSnake, alive = safe }
  where
    head'    = nextPos (direction game) (head $ snake game)
    ateFood  = head' == food game
    body'    = if ateFood then snake game else init (snake game)
    newSnake = head' : body'
    safe     = head' `notElem` body' && insideBoard head'

insideBoard :: Pos -> Bool
insideBoard (x, y) = x >= 0 && x < 30 && y >= 0 && y < 20
```

`step` fonksiyonunun güzelliği, örnek bir `Game` verip doğrudan sonuç bekleyebilmemizdir. Örneğin "duvara yaklaşınca `alive` yanlış olur mu?" sorusu terminal açmadan test edilir. Fonksiyonel programlamadaki referans şeffaflığı tam olarak bu rahatlıktır.

## Monadlar: Saf çekirdek ile dış dünyayı ayırmak

Peki yem için rastgele koordinat nasıl üretilecek? Rastgelelik dış dünyaya ait olduğundan `IO` kullanabiliriz. Ancak `IO`yu oyun kurallarına yaymak yerine yalnızca sınırda tutmak iyi bir mimaridir.

```haskell
spawnFood :: [Pos] -> IO Pos
spawnFood occupied = do
  x <- randomRIO (0, 29)
  y <- randomRIO (0, 19)
  let candidate = (x, y)
  if candidate `elem` occupied
    then spawnFood occupied
    else pure candidate

loop :: Game -> IO ()
loop game = do
  render game
  input <- readDirection
  let moved = step (game { direction = input })
  next <- if head (snake moved) == food game
          then do f <- spawnFood (snake moved)
                  pure moved { food = f }
          else pure moved
  when (alive next) $ loop next
```

`do` gösterimi sihir değildir; `IO` eylemlerini sıraya koyan monadik bir bağlama biçimidir. `render`, `readDirection` ve `spawnFood` etkili işlemler yaparken, `step` saf kalır. Daha gelişmiş bir sürümde rastgelelik `State StdGen` ile taşınabilir; terminal erişimi için de `ReaderT` benzeri katmanlar kurulabilir.

| Katman | Sorumluluk | Örnek |
|---|---|---|
| Saf çekirdek | Kurallar ve çarpışma | `step`, `nextPos` |
| Etki sınırı | Girdi, çizim, zaman | `IO` |
| Durum monadı | Ek oyun verisini taşıma | `State Game` |

Sonuçta Haskell ile yılan oyunu, "durumu değiştir" yaklaşımından "yeni bir dünya üret" yaklaşımına geçiştir. Bu ayrım yalnızca şık değildir: testleri kolaylaştırır, tekrar oynatma özelliğini mümkün kılar ve oyunun büyümesini daha az korkutucu hale getirir.

![haskell-ile-yilan-99](/img/haskell-ile-yilan-99.svg)


---
layout: post
title: "Elixir ve Akka’da Actor Modeli: Mesajlarla Gelen Eşzamanlılık"
math: true
categories: 
  - Bilgi
tags: 
  - elixir
  - akka
  - scala
  - actor-modeli
  - eşzamanlılık
  - dağıtık-sistemler
toc: true
image: /img/elixir-ve-akkada-59.png
---

Geleneksel nesne yönelimli programlamada bir nesne diğerinin metodunu çağırır ve çoğu zaman aynı belleği paylaşır. Actor modelinde ise bağımsız aktörler birbirlerine mesaj gönderir. Böylece kilitler, yarış koşulları ve hata yayılımı daha yönetilebilir hâle gelir. Elixir ile Akka bu fikri farklı araçlarla uygular; biri Erlang VM’nin doğal yeteneklerine, diğeri JVM ve Scala ekosistemine yaslanır.

![elixir-ve-akkada-59](/img/elixir-ve-akkada-59.svg)

``

## Actor modeli nasıl çalışır?

Bir aktör; özel duruma, mesaj kutusuna ve davranışa sahip hesaplama birimidir. Aktörler doğrudan birbirlerinin durumuna erişmez. Her aktör sırayla bir mesaj işler ve sonuç olarak durumunu değiştirebilir, başka aktörlere mesaj gönderebilir veya yeni aktörler oluşturabilir.

Aktörleri gerçekten birbirinden tamamen bağımsız işletim sistemi iş parçacıkları sanmamak gerekir. Genellikle çok sayıda hafif aktör, daha küçük bir thread havuzu üzerinde zamanlanır. Basitçe:

$$N_{actor} \gg N_{thread}$$

Bu ayrım sayesinde yüz binlerce aktör oluşturmak mümkün olabilir. Mesajların sırayla işlenmesi de aktörün kendi durumu için kilit ihtiyacını azaltır. Ancak farklı aktörlerden gelen mesajların küresel sırası garanti edilmez.

| Özellik | Elixir | Akka Typed (Scala) |
|---|---|---|
| Çalışma ortamı | BEAM | JVM |
| Mesaj biçimi | Dinamik Elixir terimleri | Tip güvenli protokoller |
| Temel soyutlama | Process, GenServer | Actor, Behavior |
| Hata yaklaşımı | Supervisor ve bağlantılar | Supervision stratejileri |
| Dağıtık çalışma | Dil ve VM ile bütünleşik | Cluster modülleriyle |
| Ekosistem | OTP merkezli | JVM ve Reactive ekosistemi |

## Elixir: süreçler ve OTP

Elixir’de aktör fikrinin karşılığı BEAM süreçleridir. Bunlar işletim sistemi process’i değil, VM tarafından yönetilen hafif yürütme birimleridir. Üretim uygulamalarında ham süreçler yerine çoğunlukla `GenServer` kullanılır.

```elixir
defmodule Counter do
  use GenServer

  def start_link(initial) do
    GenServer.start_link(__MODULE__, initial, name: __MODULE__)
  end

  def increment, do: GenServer.cast(__MODULE__, :increment)
  def value, do: GenServer.call(__MODULE__, :value)

  def init(initial), do: {:ok, initial}
  def handle_cast(:increment, state), do: {:noreply, state + 1}
  def handle_call(:value, _from, state), do: {:reply, state, state}
end
```

Bu sayaçta durum yalnızca `Counter` sürecindedir. `cast` yanıt beklemeyen, `call` ise yanıt bekleyen mesajlaşmayı temsil eder. Süreç çökerse bir supervisor onu yeniden başlatabilir. OTP’nin meşhur yaklaşımı, hatayı saklamak yerine kontrollü biçimde çöküp toparlanmaktır: *Let it crash!*

## Akka Typed: tip güvenli mesajlar

Akka Typed, aktörün kabul edebileceği mesajları Scala türleriyle tanımlar. Böylece yanlış mesajların önemli bir bölümü derleme sırasında yakalanır.

```scala
import akka.actor.typed.{ActorSystem, Behavior}
import akka.actor.typed.scaladsl.Behaviors

object Counter {
  sealed trait Command
  final case object Increment extends Command
  final case class GetValue(replyTo: akka.actor.typed.ActorRef[Int]) extends Command

  def apply(value: Int = 0): Behavior[Command] =
    Behaviors.receiveMessage {
      case Increment => apply(value + 1)
      case GetValue(replyTo) =>
        replyTo ! value
        Behaviors.same
    }
}

val system = ActorSystem(Counter(), "counter")
system ! Counter.Increment
```

Burada `Behavior[Command]`, aktör protokolünü açıkça sınırlar. Değişmez durum her mesajdan sonra yeni bir davranış üretilerek taşınır. Bu yaklaşım, büyük Scala projelerinde güçlü derleyici denetimi sağlar.

## Hangisini seçmeli?

Elixir; yüksek bağlantı sayısı, düşük gecikmeli mesajlaşma ve hata toleransı gereken sohbet, telekomünikasyon veya gerçek zamanlı sistemlerde son derece doğaldır. Akka ise JVM kütüphaneleriyle bütünleşmesi, güçlü tip sistemi ve mevcut Scala altyapısı nedeniyle kurumsal dağıtık sistemlerde öne çıkar.

Actor modeli bütün eşzamanlılık sorunlarını sihirli biçimde çözmez. Mesaj kutusunun sınırsız büyümesi, teslim garantileri, tekrar işleme ve ağ bölünmeleri yine tasarlanmalıdır. Seçim yaparken sözdiziminden çok ekosistem, operasyon bilgisi ve hata modelini değerlendirmek gerekir.

---
layout: post
title: "İlaç Keşfinde Moleküler Simülasyon: Proteinlerle Dijital Prova"
math: true
categories: 
  - Bilgi
tags: 
  - ilaç keşfi
  - moleküler simülasyon
  - moleküler dinamik
  - biyoinformatik
  - python
  - hesaplamalı kimya
toc: true
image: /img/ilac-kesfinde-molekuler-40.png
---

Bir ilaç adayını laboratuvarda sınamadan önce, hedef proteinle bilgisayar ortamında buluşturabilir miyiz? Evet; üstelik yalnızca birbirlerine yakışıp yakışmadıklarına değil, nasıl hareket ettiklerine de bakabiliriz. Moleküler simülasyon, ilaç keşfinin dijital prova sahnesidir. Ancak alkış alan bir prova, gerçek gösterinin mutlaka başarılı olacağı anlamına gelmez.


![ilac-kesfinde-molekuler-40](/img/ilac-kesfinde-molekuler-40.svg)

``

## Önce hedefi ve molekülü tanıyalım

İlaç adayının bağlandığı moleküle **hedef**, aday küçük moleküle ise çoğunlukla **ligand** denir. Protein üzerindeki bağlanma cebi; geometrisi, elektrik yükleri ve suyla ilişkisi nedeniyle bazı ligandları diğerlerinden daha iyi karşılar. Buradaki mesele yalnızca anahtarın kilide sığması değildir: Kilit esner, anahtar döner ve aradaki su molekülleri pazarlığa katılır.

Önce deneysel veya tahmini bir protein yapısı hazırlanır. Eksik atomlar, protonlanma durumları, önemli su molekülleri ve gerekiyorsa metal iyonları değerlendirilir. Ligandın üç boyutlu geometrisi ve yükleri hazırlanır. Yanlış protonlanma, hesaplamanın sonucunu değiştirebilir; bilgisayar, yanlış hazırlanmış girdiyi büyük bir özgüvenle işlemekten çekinmez.

## İlk eleme: Moleküler kenetlenme

**Moleküler kenetlenme**, yani docking, ligandın bağlanma cebindeki olası yerleşimlerini araştırır. Arama algoritması konum, yönelim ve dönebilen bağları değiştirir; puanlama fonksiyonu ise temasları değerlendirir. Hidrojen bağları, hidrofobik etkileşimler ve sterik çakışmalar bu değerlendirmede rol oynar.

Docking, binlerce adayı hızla daraltabilir. Fakat verdiği skor, ölçülmüş bağlanma afinitesi veya kesin bir serbest enerji değildir. Farklı yazılımların skorlarını doğrudan aynı terazide tartmak da güvenilir olmaz.

| Yöntem | Temel soru | Başlıca sınır |
|---|---|---|
| Docking | Ligand nereye yerleşebilir? | Esneklik ve çözücü yaklaşık ele alınır |
| Moleküler dinamik | Kompleks zamanla nasıl davranır? | Örnekleme pahalıdır |
| Serbest enerji hesabı | Bağlanma ne kadar elverişlidir? | Yakınsama dikkatle sınanmalıdır |
| Deney | Gerçekte ne oluyor? | Zaman ve kaynak gerektirir |

## Hareket başlasın: Moleküler dinamik

Moleküler dinamikte atomlar, bir **kuvvet alanının** tanımladığı potansiyel enerjiye göre hareket eder. Bağların gerilmesi, açıların değişmesi, elektrostatik ve van der Waals etkileşimleri birlikte hesaplanır. Kuvvet, enerjinin konuma göre değişiminden elde edilir:

$$\mathbf{F}_i=-\nabla_i U$$

Newton denklemleri küçük zaman adımlarıyla çözülür. Böylece tek bir görüntü yerine bir yörünge oluşur. Protein nefes alır gibi kıpırdar; ligand bazı temasları kaybederken yenilerini kurabilir. Termostat, sistemin sıcaklığını hedef değer çevresinde tutmaya yardımcı olur.

Aşağıdaki OpenMM örneği, önceden hazırlanmış, su ve iyon içeren periyodik bir AMBER kompleksini çalıştırır. Protein ve ligandın uyumlu kuvvet alanı parametreleri dosyalarda bulunmalıdır; kod parametre üretmez.

```python
from openmm import LangevinMiddleIntegrator
from openmm.app import (
    AmberPrmtopFile, AmberInpcrdFile, Simulation,
    PME, HBonds, DCDReporter
)
from openmm.unit import kelvin, picosecond, nanometer

prmtop = AmberPrmtopFile("complex.prmtop")
inpcrd = AmberInpcrdFile("complex.inpcrd")
system = prmtop.createSystem(
    nonbondedMethod=PME,
    nonbondedCutoff=1.0 * nanometer,
    constraints=HBonds
)
integrator = LangevinMiddleIntegrator(
    300 * kelvin, 1 / picosecond, 0.002 * picosecond
)
sim = Simulation(prmtop.topology, system, integrator)
sim.context.setPositions(inpcrd.positions)
sim.context.setPeriodicBoxVectors(*inpcrd.boxVectors)
sim.minimizeEnergy()
sim.context.setVelocitiesToTemperature(300 * kelvin)
sim.step(10000)
sim.reporters.append(DCDReporter("trajectory.dcd", 1000))
sim.step(250000)
```

Enerji minimizasyonu kötü temasları azaltır; ardından kısa bir ön dengeleme yapılır. Son bölüm, iki femtosaniyelik adımlarla **0,5 nanosaniyelik** yörünge üretir. Bu yalnızca teknik bir başlangıçtır; güvenilir analiz için daha kapsamlı dengeleme, daha uzun koşular ve bağımsız tekrarlar gerekir.

## Yörüngeden karar çıkarmak

Ligandın yer değiştirmesi, hidrojen bağlarının devamlılığı ve cebin şekil değişimleri incelenebilir. Ancak düşük RMSD, tek başına güçlü bağlanmanın kanıtı değildir. Ayrıca proteinin genel hareketini ayırmadan hesaplanan ligand RMSD değerleri yanıltıcı olabilir.

Bağlanma termodinamiği için standart serbest enerji önemlidir:

$$\Delta G^\circ=RT\ln(K_d/C^\circ)$$

Burada $K_d$ ayrışma sabiti, $C^\circ$ standart derişimdir. Daha küçük $K_d$, daha elverişli bağlanmaya karşılık gelir. Benzer adayların farklarını inceleyen FEP gibi yöntemler güçlüdür; fakat yeterli örnekleme ve belirsizlik analizi şarttır.

## Son söz laboratuvarın

İyi bağlanmak, mutlaka iyi ilaç olmak değildir. Adayın proteini gerçekten baskılayıp baskılamadığı, başka hedeflere bağlanması, hücreye erişmesi, metabolizması ve toksisitesi ayrıca değerlendirilir. Simülasyon sonuçları biyokimyasal, hücresel ve gerektiğinde ileri deneylerle doğrulanmalıdır.

En verimli yaklaşım, docking ile elemek, dinamikle davranışı incelemek ve uygun adaylarda serbest enerji hesaplarına ilerlemektir. Parametreleri, yazılım sürümlerini ve tekrar koşullarını kaydetmek de sonuçları yeniden üretilebilir kılar. Bilgisayar burada sihirli ilaç makinesi değil; yanlış adaylara harcanan emeği azaltan, doğru deneyleri tasarlamaya yardımcı olan meraklı bir araştırma ortağıdır.

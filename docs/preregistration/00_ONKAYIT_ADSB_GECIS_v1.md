# A makalesi — gerçek ADS-B akışı altında geçiş fonksiyonu ön kaydı

Tarih 10 Eylül 2026

Durum **veri indirilmeden ve görülmeden donduruldu**

Görev KKT-20260910-ADSB

---

## Bu çalışmanın ne OLMADIĞI, en başa yazılıyor

Bu kol, A makalesinin *"bütün koşular sentetiktir"* sınırlılığını **kapatmaz**
ve kapatacakmış gibi sunulmayacaktır. Nedeni yayımlanmış tasarımın kendisinde
yazılıdır. `docs/ads_b_fusion_design.md` belgesinde ADS-B akışı yalnız **uçak
durum verisini** yani konum, hız, irtifa ve bunlardan türeyen uçak
yoğunluğunu sağlar. Karar sınıflarının kendisi, yani ayrılma kaybı, ATCO iş
yükü ve siber emniyet olayları, ANSP kayıtlarına erişilemediği için
**tasarım gereği sentetik olarak enjekte edilmeye devam eder**. Gözlem
uzayının bileşenleri belgede şöyle sıralanmıştır: uçak yoğunluğu (açık),
olay bayrakları (sentetik), siber uyarılar (sentetik).

Bunun anlamı şudur. Etiketler, ödül ve doğru eylem eşlemesi sentetik
üreticiden gelmeye devam eder. Gerçek olan tek şey gözlem vektörünün dışsal
bileşenidir. Dolayısıyla bu kol **karar görevini gerçek yapmaz**.

Bu ön kayıt, bir önceki turda tarafımdan yapılan yanlış bir savı da kayda
geçirir. ADS-B koşusunun *"A'nın en büyük zaafına doğrudan cevap vereceği"*
söylenmişti. Tasarım belgesi okunduğunda bu savın dayanaksız olduğu
görülmüştür ve sav geri çekilmiştir.

## Bu çalışmanın ne OLDUĞU

Bölüm 5.8.2'de raporlanan bulgu şudur. Yayımlanmış üç ortamın hepsinde
sonraki durum, ajanın seçtiği eylemden bağımsız çekilmektedir, yani
P(s′ | s, a) = P(s′). Bu bulguya karşı akla gelen ilk itiraz, özelliğin
sentetik üreticinin bir kusuru olabileceğidir.

Bu kol o itirazı sınar. Dışsal akış sentetik üreticiden alınıp **gerçek bir
ADS-B akışına** çevrildiğinde özelliğin sürüp sürmediği ölçülür. Yani bu bir
**sağlamlık sınamasıdır**, gerçek veriyle doğrulama değildir.

Sonuç iki yönde de bilgi taşır. Özellik sürüyorsa 5.8.2'nin bulgusu
üreticinin bir artefaktı olmadığı için güçlenir. Sürmüyorsa bulgu sentetik
ortamlarla sınırlanmış olur ve makale bunu yazar.

## Veri kaynağı

OpenSky Network REST arayüzü `https://opensky-network.org/api/states/all`,
`EU` sınır kutusu (lamin 35.0, lamax 71.0, lomin −10.0, lomax 40.0), depoda
yayımlanmış `examples/fetch_opensky.py` betiğinin kullandığı uçlar.

Anonim erişimin sınırı on saniyede bir istektir. **Geçmişe dönük sorgu anonim
erişimde yoktur**, yalnız anlık görüntü alınır. Bu yüzden veri, sabit aralıkla
toplanan anlık görüntülerden oluşacaktır.

**Toplanacak miktar** 180 anlık görüntü, 15 saniye aralıkla, yani kesintisiz
45 dakika. Toplama başlangıç zamanı UTC olarak kaydedilecektir.

## Tekrarlanabilirlik, canlı veri sorunu

Canlı veri bir tohumdan yeniden üretilemez. Bu yüzden tekrarlanabilirlik
artefaktı tohum değil **arşivin kendisidir**. Aşama 0'da uygulanan aynı
disiplin geçerlidir. Her anlık görüntünün ham JSON yanıtı değiştirilmeden
saklanacak, her dosyanın indirme zamanı, bayt boyutu ve SHA-256 özeti sonuç
kaydına yazılacaktır. Analiz yalnız arşivlenmiş dosyalardan koşacak, koşum
sırasında ağa gidilmeyecektir.

Sentetik bileşenlerin tohumu `20260910` olarak sabitlenmiştir.

## Ölçülecek şey ve nasıl ölçüleceği

Sınama, 5.8.2'de betimlenen yordamın gerçek akış üzerinde uygulanmasıdır.
Durum sabit tutulur, eylem değiştirilir, sonraki durum dağılımının değişip
değişmediğine bakılır.

1. Arşivlenmiş akıştan **K = 30** durum, sabit aralıklarla seçilir.
2. Her durum için eylem uzayının tamamı, yani beş eylem, ayrı ayrı uygulanır.
3. Her (durum, eylem) çifti için **M = 200** sonraki durum örneklenir.
4. Sonraki durumun skaler özeti olarak gözlem vektöründeki **uçak yoğunluğu**
   bileşeni alınır.
5. Her durum için beş eylemin ürettiği dağılımlar **Kruskal-Wallis** sınamasıyla
   karşılaştırılır.
6. Anlamlılık düzeyi **α = 0,01**, K durum boyunca **Bonferroni** düzeltmesi
   uygulanır. Etki büyüklüğü olarak epsilon-kare de raporlanır.

## Pozitif denetim, zorunludur

Sınamanın bağımlılığı *saptayabildiğini* göstermek zorunludur, aksi hâlde
olumsuz sonuç sınamanın körlüğünden de kaynaklanabilir. Bu yüzden aynı yordam
üçüncü bir kolda, sonraki durumun eyleme **kasten bağlandığı** bir ortam
üzerinde koşulacaktır. Enjekte edilen bağımlılık, seçilen eylemin sonraki
uçak yoğunluğunu yüzde on kaydırması olacaktır.

Pozitif denetim kolunda sınama bağımlılığı saptamazsa **çalışma
geçersizdir** ve hiçbir sonuç raporlanmaz.

## Ön kayıtlı karar kuralı ve başarısızlıkta yazılacak cümle

**Kural ADSB.1.** Pozitif denetim kolu bağımlılığı saptamalıdır. Saptamazsa
çalışma geçersiz sayılır.

**Kural ADSB.2.** Gerçek akış kolunda, Bonferroni düzeltmesinden sonra K
durumun **hiçbirinde** sıfır hipotezi reddedilmezse şu cümle yazılır:

> Bölüm 5.8.2'de raporlanan geçiş fonksiyonu özelliği, dışsal akış gerçek bir
> ADS-B akışıyla değiştirildiğinde de sürmektedir; dolayısıyla özellik sentetik
> üreticinin bir artefaktı değildir.

**Kural ADSB.3.** K durumun **bir veya daha fazlasında** sıfır hipotezi
reddedilirse şu cümle yazılır:

> Bölüm 5.8.2'de raporlanan geçiş fonksiyonu özelliği, gerçek bir dışsal akış
> altında sürmemektedir; bulgu bu makalenin sentetik ortamlarıyla sınırlıdır ve
> genel bir sav olarak sunulamaz.

Reddedilen durum sayısı ve her durumun p değeri ile etki büyüklüğü, hangi
cümle yazılırsa yazılsın raporlanacaktır.

## Sonuç görüldükten sonra değiştirilmeyecekler

K, M, α, Bonferroni düzeltmesi, skaler özet seçimi, sınama istatistiği,
anlık görüntü sayısı ve aralığı, tohum, pozitif denetimin kaydırma oranı.

## Yorum sınırı

Başarılı sonuç yalnız şunu gösterir. Gözlem vektörünün dışsal bileşeni gerçek
olduğunda da sonraki durum eylemden bağımsız çekilmektedir. Bu sonuç, öğrenme
görevinin gerçek olduğu, etiketlerin gerçek olduğu, PPO'nun daha iyi
çalışacağı, ya da A makalesinin sentetiklik sınırlılığının kapandığı biçiminde
okunamaz. Kapanmaz.

---

*Bu metin veri indirilmeden yazılmış ve dondurulmuştur. Sonuçlar bu dosyaya
dokunulmadan ayrı dosyalara yazılacaktır.*

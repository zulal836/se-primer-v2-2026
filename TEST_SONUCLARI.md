# Gerçekte çalıştırılan kontroller

## Sabit HF commit'ine bağlı SENTETİK DEMO yayını

0.1.0-demo, `zulalertrk/se-primer-v2-synthetic-demo` deposuna tam `d79adb407da3be479d77fe4a909b932bc1b77a8a` commit'inde yüklendi. Model/config/kart/şema aynı commit'te; dördü de anonim indirilerek byte hash'leri doğrulandı. `release-demo.json` makbuzdur. Model SHA-256 `5a08f081cdf16ec82365879e2cad5479575481de0a3eb59e1313a1f8a1982938`, config SHA-256 `34e56b8aafcad402df7e1f85c7b93883ec6d45b5f75298e18eb1a363a067137c`. Model/config değişmedi; `publishable=false` korundu. Gerçek modelin BA=0.25/recall=0.50 ret kararı değiştirilmedi.

Bu yayında **15/15 Python unittest**, beş Python ONNX referansı ve üretim build'i geçti. Sabit HF manifestiyle **15/15 yerel Cypress testi** yaklaşık 26 saniyede geçti; tarayıcı HF commit'inden gerçek ONNX/config indirdi, model dosyası hash'ini Python referansına karşı denetledi ve beş olasılıkta <1e-4 pariteyi doğruladı. Bu testler sentetik demo dosyasına aittir; gerçek kullanıcı başarımı iddiası yoktur. Mevcut video aynı dosyayı gösterdiğinden yeniden çekilmedi.

## Teslim için son eğitim karşılaştırması

Son bulut koşusu 42281454788, kaynak `1fd3e31`: 15 Cypress testi/build/Pages deploy başarılı. Ayrıca bu oturumda 2/2 girişsiz canlı test yaklaşık 65 saniyede geçti: mevcut sentetik ONNX'in beş referansı, oyun sonu ve herkese açık MP4. Bu sonuçlar gerçek adayın başarısız kabul sonucunu değiştirmez.

`MODEL_SECIMI.md`, karşılaştırma çalıştırılmadan önce `edb0a9e` commit'inde sabitlendi. Önce etiket/girdi akışı incelendi: UI/CSV `0=kısa`, `1=ayrıntılı`; boş hedefler eğitim dışında; özellikler yalnız süre/değiştirme/ipucu. `secim` veya ihtiyaç etiketi özelliklere girmez. sklearn sınıf sırası `[0,1]`, ONNX/Python/web ikinci sütunu p(ayrıntılı) olarak kullanır. Veri sınıflarında terslik bulunmadı. Sınır durumu düzeltildi: sklearn `predict` eşit olasılıkta ilk sınıfı seçebildiğinden CV/test kararı da web/spec gibi açık `p>=0.5` kullanıyor; eşik değişmedi.

Yalnız dış eğitim verisinde beş katlı StratifiedGroupKFold(seed=42) ile iki sabit aday karşılaştırıldı. Katlar arasında oturum sızıntısı 0; StandardScaler her eğitim katında fit edilir.

| Aday | Ortalama CV dengeli doğruluk | Ortalama CV ayrıntılı recall |
|---|---:|---:|
| Sınıf ağırlıklı lojistik regresyon | 0.470000 | 0.500000 |
| Küçük sınıf ağırlıklı ağaç (derinlik 3, min yaprak 3) | 0.413333 | 0.500000 |

CV ile **lojistik regresyon** seçildi; seçim dış test okunmadan rapora yazıldı. Aynı sabit dış testte yalnız bu aday **bir kez** değerlendirildi: **BA=0.25, ayrıntılı recall=0.50**, confusion matrix `[[0,5],[3,3]]` (satırlar gerçek, sütunlar tahmin; sınıf sırası kısa/ayrıntılı). Eşikler >=0.70/>=0.65 korunarak aday reddedildi. Test sonucuyla ağaca geçilmedi, tekrar tarama yapılmadı. Dış test daha önce temel lojistik regresyonda görüldüğünden tüm süreç bağımsız, hiç görülmemiş test gibi sunulmaz. Rapor `test-results/final-model-selection.json`; tekrar aynı veri/protokolle test değerlendirmesi kodda engellenir.

Nihai gerçek paket/HF/video oluşturulmadı; mevcut sentetik model korunuyor. 20 tutor insan değerlendirmesi bu v2 tesliminin kapısı değildir. Önceki veri denetimi ve temel model sonuçları aşağıda tarihçe olarak yer alır.

Son teslim doğrulaması gerçekten çalıştırıldı: **9/9 Python unittest**, beş Python ONNX referansı, **15/15 Cypress** (yaklaşık 40 sn) ve üretim build'i geçti. Yeni protokol testleri seçim sonucunun yalnız CV sıralamasından geldiğini, dış test değerlendirme sayısının bir olduğunu, aynı veri/protokol tekrarının fit öncesi reddedildiğini ve aday parametrelerinin sabitliğini doğrular. ONNX/parite/E2E başarıları korunmuş **sentetik** yayımlanmış artefakta aittir; başarısız gerçek aday için ONNX başarısı iddiası yoktur. Model/config/manifest/oracle/video üzerinde Git farkı bulunmadı. Veri/protokol raporu yalnız toplamlar ve hash içerir, ham insan kayıtları public değildir.

## Güncel CSV sonrası gerçek eğitim ve eval sonucu

Beş CSV yeniden denetlendi/birleştirildi: 123 kaynak satırında 24 tekrar, **99 benzersiz karar**, 32 tamamlanmış/2 yarım oturum. Yeni dosyadan 30 yeni karar geldi. Ham dosya hash'leri değişmedi. Tamamlanmış kararlarda 49 kullanılabilir etiket (28 kısa/21 ayrıntılı), 47 boş hedef var. Yarım oturumdaki etiketler ve boş hedefler eğitim dışında tutuldu.

`python train.py` gerçekten çalıştırıldı. Oturum bazlı sabit split: eğitim 17 oturum/38 karar (23 kısa/15 ayrıntılı), test 6 oturum/11 karar (5 kısa/6 ayrıntılı), kesişen oturum 0. Veri sayısı koşulları geçti. **Balanced accuracy 0.50**, **ayrıntılı recall 0.00**, confusion matrix `[[5,0],[6,0]]`. Gerçek eğitim sonucu önceden belirlenen 0.70 ve 0.65 eşiklerinin altında kaldı; betik exit code 1 ile durdu. Aynı test bölümünü geçene kadar model/seed/eşik ayarlanmadı.

Artefakt koruması gerçek önce/sonra SHA-256 karşılaştırmasıyla doğrulandı: model, config, model kartı, public kopyalar, manifest, Python oracle ve demo eğitim tarafından değiştirilmedi. Model kartına güncel durum notu sonradan belge değişikliği olarak eklendi. Kabul kapısında durulduğundan yeni gerçek ONNX, sklearn–ONNX/parite sonucu, yeni regresyon koşusu veya yayın yapılmış gibi gösterilmez. Eski ONNX/sentetik test sonuçları aşağıdaki tarihçededir.

Tanı: kullanılabilir 49 kararda seçenek değiştirme sayısı hep 0; ipucu sayısı yalnız dört kararda >0. Süre aralığı yaklaşık 1.417–18.973 sn. Bu, model başarısının kanıtı değil, sonraki veri tasarımına yönelik gözlemdir. Güncel sayısal raporlar `test-results/real-data-audit.json`, `real-training-attempt.json`, `real-split-readiness.json` içinde.

## primer-oturumlar3.csv sonrası güncel veri kapısı

Dört CSV denetlendi ve birleştirildi: 69 benzersiz karar, kaynaklar arasında 0 tekrar. Eski 45 kayıt yeniden sayılmadı. 22 tamamlanmış/2 yarım oturum var. Tamamlanmış 66 kararda hedefler 11 kısa, 8 ayrıntılı, 47 boş; **19 etiket kullanılabilir**. Tüm kararlarda 11 kısa, 9 ayrıntılı, 49 boş. Ham dosya hash'leri değişmedi.

Gerçek `train.py` exit code 1: “Her sınıfta en az 10 etiketli karar gerekli”. Fit başlamadı; gerçek eval metriği yok. Model/config/manifest/oracle/demo dosyaları eğitim denemesinde aynı hash'leri korudu. Model kartına sonraki belge notu ayrı değişikliktir.

Eğitim yapmayan ayrı split tanısı aynı `GroupShuffleSplit(n_splits=1,test_size=.25,random_state=42)` ile çalıştırıldı. Boş hedefler ve tamamlanmamış oturumlar önce çıkarıldı. Eğitim: 9 oturum, 12 etiket (5 kısa/7 ayrıntılı); test: 4 oturum, 7 etiket (6 kısa/1 ayrıntılı); kesişim 0 oturum. Testte ayrıntılı sınıfta en az beşe karşı yalnız bir örnek var. Bu, ölçülmüş bir model performansı değildir.

Bu veri güncellemesinde uygulama kodu/model değişmediğinden önceki regresyonları yeniden çalıştırılmış gibi raporlamıyoruz. Yeni gerçek model/parite, HF yayını ve nihai video bu veri kapısına bağlı olarak bekliyor. Güncel raporlar `real-data-audit.json`, `real-training-attempt.json`, `real-split-readiness.json` altında; aşağıdaki test koşuları önceki oturumlara aittir.

## 6 Kasım 2026 gerçek CSV denetimi ve eğitim kapısı

Üç kaynak CSV: 45 satır, 45 benzersiz karar, kaynaklar arasında 0 tekrar. Mevcut birleşik dosyayla yeniden birleştirme 45 kaydı yeniden eklemedi. Ham dosya hash'leri değişmedi. 16 farklı oturumun 14'ü tamamlanmış, 2'si yarım. Tamamlanmış 42 kararda kısa=4, ayrıntılı=3, eksik=35; bütün 45 kararda kısa=4, ayrıntılı=4, eksik=37. Oturum kimlikleri ve ham satırlar public rapora yazılmadı.

`python train.py` gerçek veriyle denendi: **exit code 1**, 15 tamamlanmış oturum koşulunda durdu (bulunan 14). Fit, split ve dönüşüm başlamadı; gerçek eval metriği yok. Eğitim sırasında önceki model/config/kart/oracle/demo dosyalarının hash'leri değişmedi. Model kartındaki sonraki durum notu ayrı belge güncellemesidir. `test-results/real-training-attempt.json` ölçülen önce/sonra hash'lerini saklar. Eğitim eşiği, random_state ve değerlendirme yöntemi değiştirilmedi.

Boş gerçek veri testinin artık kullanıcının gerçek dosyasına bağlı olmaması için test, yalnız geçici başlık içeren CSV ile gerçek `train.py --data` komutunu çalıştıracak şekilde düzeltildi. Boş veriyi reddetme ve artefakt koruma beklentileri korundu. Yeni gerçek model üretilmediği için aşağıdaki tekrar kontrolleri önceki sentetik artefakt içindir; gerçek model başarısı olarak okunmamalıdır.

| Bu oturumda yeniden çalıştırılan kontrol | Sonuç |
|---|---|
| Python unittest | 6/6 geçti |
| Python ONNX oracle | 5/5 referans, <1e-4 tolerans geçti |
| Gerçek tarayıcı ONNX + oyun regresyonu | 15/15 Cypress testi geçti, yaklaşık 24 sn |
| Üretim build'i `--base=./` | Vite 6.4.5 ile başarılı |
| Gerçek veriyle eğitim ön koşulu | Beklendiği gibi ret; model üretilmedi |
| Bulut regresyonu / Pages | Koşu 42272543090: 15 test, build, deploy başarılı |
| Canlı uygulama, girişsiz yeni tarayıcı | 2/2 geçti, yaklaşık 13 sn; gerçek ONNX referansları, oyun sonu, MP4 |

### Önceki doğrulanmış sürümün tarihçesi

5 Kasım 2026, Windows 11 · Node 24.20.0 · Python 3.12.10 · Cypress 15.21.1 / Electron 138. Model verisi yalnız sentetik; gerçek oturumlar 0. İnsan tutor incelemesi yapılmadı.

| Kontrol | Gerçek sonuç |
|---|---|
| Model öncesi temel oyun `npm run test:base` | 11/11 geçti; artefakt henüz yokken çalıştırıldı |
| ONNX sonrası tüm Cypress suite | 15/15 geçti: 12 oyun, 3 model/parite testi |
| Üretim build'i, localhost:5175 | 15/15 geçti; tarayıcı gerçek WASM+ONNX kullandı |
| Python `unittest discover` | 6/6 geçti |
| Python `tests/parite.py` | 5/5 referans girdisi geçti, mutlak hata <1e-4 |
| `train.py --demo` | Eval kapısı geçti; balanced accuracy 0.9260651629, ayrıntılı recall 0.9047619048 |
| sklearn/ONNX en büyük fark, tüm 480 sentetik karar | 1.0823183327e-7, sınır 1e-4 |
| Eğitim tekrarı | Sabit ONNX graph adıyla model, config, oracle dosyaları bayt düzeyinde aynı |
| `npm run build -- --base=./` | Başarılı, Vite 6.4.5; WASM 11.9 MB, uygulama JS yaklaşık 82 KB |
| `npm audit --audit-level=moderate` | 0 güvenlik açığı |
| Gerçek tarayıcı demo kaydı | Cypress otomatik oynatımı 70.85 saniye; kısa/ayrıntılı ONNX kararları ve oyun sonu doğrulandı; public/demo.mp4 |
| GitHub Actions / Ubuntu 24.04 | 15 tarayıcı testi, build ve Pages deploy başarılı; koşu 42100198789 |
| Canlı HTTP, kimlik bilgisi gönderilmeden | HTML 200, model SHA-256 aynı, MP4 HEAD 200; MP4 süresi 73.040 sn |
| Canlı sitede yeni Cypress tarayıcı oturumu | 2/2 geçti: gerçek ONNX ile beş referans girdisi, üç karar ve iyi son; public MP4. Son koşu 48 sn |

Python testleri şunları doğrular: boş gerçek veri eğitimi reddedilir ve önceki model korunur; sentetik model nihai yayına kabul edilmez; oturum split'i kesişmez; bağımsız gürültülü etiketler eval kapısında durur ve model korunur; CSV yinelenmez, tamamlanma güncellenir ve çelişki reddedilir; tek sınıf/karışık kaynak reddedilir.

Tarayıcı suite sekiz yolu, iki sonu, rol/hedef anlatımını, katılım olmadan kayıt yapılmamasını, CSV'yi, yeni kimliği, temizlemeyi, yükleme hatasında kural yedeğini, beş sayısal parite girdisini ve gerçek model yardım değişimini sınar. `test-results/browser-parity.json` gerçek ölçülen farkları, `test-results/reproducibility.json` hash karşılaştırmasını saklar. Cypress'in geçici yerel kayıtları test girdileridir; gerçek veri dosyasına eklenmedi.

İlk model sonrası tarayıcı koşusu Vite'ın public mjs import sınırı nedeniyle başarısız oldu. WASM-only paket ve Vite `?url` ile düzeltildi; başarı sonuçları düzeltmeden sonraki koşulara aittir. İlk tekrar denemesinde ONNX'in otomatik rastgele graph adı dosya hash'ini değiştirdi; sabit graph adıyla giderildi. Sonuçları geçsin diye metrik eşiği değiştirilmedi. SciPy'nin `iprint` seçenek uyarısı hesaplanan metrikleri veya testleri başarısız kılmadı; tam bağımlılık sürümleri requirements-lock.txt içinde.

Canlı tarayıcının ilk koşusu 60 sn yükleme sınırında kaldı; ilk WASM indirmesine 180 sn sınırı tanınan ikinci koşu 48 sn'de 2/2 geçti. Çıkarım taklit edilmedi. İlk yüklemede yaklaşık 12 MB WASM indirilir; model hazır olana kadar oyun görünür kural yedeğiyle çalışabilir.

Henüz doğrulanmayanlar: gerçek kullanıcı ihtiyacına genelleme, insan tutor puanları, nihai HF commit'i ve gerçek dağıtımda Shadow/Canary. Yerel ağdan fiziksel telefon erişimi ayrıca denenmedi; mobil viewport 390×844 ve demo 430×932 ile tarayıcıda sınandı. Yayın ve demo kayıt sonuçları RELEASE.md/DEMO.md içindedir.

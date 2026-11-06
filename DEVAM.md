# Devam notu — 6 Kasım 2026 gerçek veri denetimi

## En güncel durum

**primer-guncel.csv dahil edildi — veri kapısı geçti, model eval kapısında kaldı.** Beş CSV 123 satır içeriyor; kaynaklar arasındaki 24 tekrar ayıklanınca 99 benzersiz karar kaldı. Yeni dosya 30 yeni karar/10 tamamlanmış oturum ekledi; önceki kayıtlar çift sayılmadı. 34 farklı oturumun 32'si tamamlanmış, 2'si yarım. Ham dosyalar/cevaplar değişmedi, Git'ten hariç tutuldu.

- Tamamlanmış 96 karar: **28 kısa, 21 ayrıntılı, 47 boş**. Eğitimde kullanılabilir **49 etiket**, herhangi bir etiketi olan 23 tamamlanmış oturum var. Tüm 99 kararda 28 kısa/22 ayrıntılı/49 boş; yarım oturumdaki bir etiket ve boşlar eğitim dışında.
- Mevcut GroupShuffleSplit(seed=42, test_size=.25): eğitim 17 oturum/38 etiket (23 kısa/15 ayrıntılı); test 6 oturum/11 etiket (5 kısa/6 ayrıntılı); kesişim 0. Bütün veri sayısı koşulları sağlandı.
- Gerçek `train.py` eğitimi çalıştı, **balanced accuracy=0.50, ayrıntılı recall=0.00**. Confusion matrix (satır gerçek, sütun tahmin; kısa/ayrıntılı): `[[5,0],[6,0]]`. Kabul eşikleri BA>=0.70, recall>=0.65 değişmedi. Exit code 1: eval kapısı geçilemedi.
- ONNX/config/model kartı/oracle/manifest/video eğitim çalışmasında korunmuştu; mevcut ONNX hâlâ sentetik sürümdür. Model kartına sonraki durum notu belge değişikliğidir. HF gerçek model yayını ve nihai demo yenilemesi yapılmadı.
- Tanısal bulgu: 49 kullanılabilir kararın **tamamında seçenek değiştirme=0**, yalnız **4 kararda ipucu sayısı>0**; süre aralığı yaklaşık 1.417–18.973 sn. Bu özelliklerdeki davranış çeşitliliği sınırlı. İnsanları belli sınıfı veya davranışı üretmeye yönlendirme; etiketleri/seed'i/eşiği değiştirip geçirmeye çalışma.
- Sonraki veri adımı: doğal farklı oyuncu ve ihtiyaçların gözlendiği yeni gerçek, yardım öncesi etiketli tam oturumlar. Daha fazla veri başarı garantisi değildir. Özellik/model tasarımı değişecekse mevcut test bölümünde tekrar tekrar ayarlamak yerine yeni bir önceden tanımlanmış değerlendirme ve bağımsız yeni holdout gerekir.
- Güncel makbuzlar `test-results/real-data-audit.json`, `real-training-attempt.json`, `real-split-readiness.json`. Yeni uygulama/model olmadığı için eski regresyonları yeniden çalışmış gibi yazma. Eski yayın ve 73 sn sentetik demo açık kalır.

## Önceki dördüncü CSV denetimi

**primer-oturumlar3.csv dahil edildi:** dört CSV'deki 69 satır, 69 benzersiz karar içeriyor; kaynaklar arasında tekrar yok. Önceden birleştirilen 45 karar yeniden eklenmedi; yeni dosya 24 karar/8 tamamlanmış oturum ekledi. 24 farklı oturumun 22'si tamamlanmış, 2'si yarım. Ham dosyalar ve insan cevapları değişmedi, Git'ten hariç kalıyor.

- Tamamlanmış 66 karar: **11 kısa, 8 ayrıntılı, 47 boş**. Kullanılabilir hedef sayısı **19**, etiketli tamamlanmış oturum sayısı **13**.
- Bütün 69 karar: 11 kısa, 9 ayrıntılı, 49 boş. Yarım oturumdaki bir ayrıntılı etiket ve boş hedefler eğitimde kullanılmaz.
- `train.py` exit code 1: **her sınıfta en az 10 etiket** koşulunda fit başlamadan durdu. Ayrıntılı sınıfta 8 var (en az 2 eksik). Oturum sayısı 22>=15 koşulu artık geçti.
- Aynı GroupShuffleSplit(test_size=.25, random_state=42) ayrı tanısal kontrolde: eğitim 9 oturum, sınıflar 5/7; test 4 oturum, sınıflar **6/1**. Testte her sınıfta en az beş gerekiyor; ayrıntılı test sınıfında 4 eksik. Oturum kesişimi 0. Bu tanı model eğitimi veya eval metriği değildir.
- Yeni veri split'i değiştirebilir; yalnız iki ek ayrıntılı etiket yeterlilik garantisi vermez. Her üç kararda yardım öncesi gerçek ihtiyacın seçildiği yeni tamamlanmış oturumlar gerekir. Eski boşları doldurma, yanıtları sınıf elde etmek için yönlendirme, seed/eşik değiştirme.
- Model/config/ONNX oracle/demo eğitim denemesinde değişmedi. Model kartına güncel durum notu ayrı belge değişikliği olarak eklendi. Gerçek model/HF yayını/nihai demo yok; önceki sentetik Pages yayını korunuyor.
- Raporlar: `test-results/real-data-audit.json`, `test-results/real-training-attempt.json`, `test-results/real-split-readiness.json`. Sonraki denetimde aynı script/kapı kullanılmalı.

## Önceki üç CSV denetimi

Kullanıcı çalışmayı sürdürdü ve `private-data/` altında üç gerçek CSV sağladı. Proje yeniden kurulmadı. `scripts/audit_real_data.py`, mevcut birleştiriciyi kullanarak 45 benzersiz kararı `data/oturumlar.csv` içine birleştirdi. Ham dosyalar/cevaplar değiştirilmedi. Kaynak CSV'ler arasında tekrar yok; yeniden çalıştırmada var olan 45 kayıt çift sayılmadı. Ham CSV'ler ve birleşik gerçek veri Git'ten hariç.

- 16 farklı oturum: **14 tamamlanmış, 2 yarım**.
- Tamamlanmış 42 karar: **4 kısa, 3 ayrıntılı, 35 eksik hedef**.
- Bütün 45 karar: **4 kısa, 4 ayrıntılı, 37 eksik hedef**.
- Yalnız beş tamamlanmış oturumda herhangi bir etiket var.
- `train.py`, exit code 1 ile “en az 15 tamamlanmış gerçek oturum, bulunan 14” nedeniyle fit başlamadan durdu. Eşik/split/seed değiştirilmedi. Eğitim denemesinde model/config/oracle/demo hash'leri korunmuştu; model kartına sonradan bu durum notu eklendi.
- HF girişi yok. Kullanıcının giriş komutu: `.venv/Scripts/hf.exe auth login`. Veri de yetersiz olduğundan nihai HF yayını, gerçek model manifesti ve nihai demo yenilemesi yapılmadı.
- Veri raporu: `test-results/real-data-audit.json`; eğitim ret/artefakt makbuzu: `test-results/real-training-attempt.json`.
- Önceki sentetik demo uygulaması ve 73.040 saniyelik video açık kalıyor. İnsan tutor etiketleri bekliyor.
- Bu oturumda 6 Python testi, 5 Python ONNX referansı, 15 yerel Cypress testi ve üretim build'i geçti. Bulutta 15 test/build/Pages dağıtımı da geçti; canlı sitede 2 girişsiz test yaklaşık 13 saniyede geçti. Yeni gerçek model değil, korunmuş sentetik artefakt doğrulandı.
- Son yayımlanan kaynak commit'i `b0ce348a6c6724edfe59501a3f3d16b0ad65a91a`; başarılı koşu https://github.com/zulal836/se-primer-v2-2026/actions/runs/42272543090 . Aşağıdaki eski commit bilgileri önceki yayınların tarihçesidir. `publication.json` günceldir.

**En küçük sonraki adım:** eski boş yanıtları sonradan doldurmak yerine her üç kararda model yardımı görülmeden gerçek ihtiyacın seçildiği yeni, tamamlanmış gönüllü oturumlar toplanmalı. Etiketli oturum/test sınıf sayıları nedeniyle en az sekiz yeni tam etiketli oturum kuramsal alt sınırdır; sabit split ve doğal sınıf dağılımı daha fazla veri gerektirebilir. En az 15 tamamlanmış oturum, her sınıfta toplam en az 10 ve testte en az beş örnek; ardından BA>=0.70, recall>=0.65 kapısı korunacak. Sınıf elde etmek için insan yanıtlarını yönlendirme veya değiştirme.

Aşağıdaki notlar önceki duraklatma kaydının tarihçesidir; “gerçek veri yok” ifadeleri o eski duruma aittir. Sonraki oturum en üstteki bu durumdan devam etmeli.

## Önceki duraklatma kaydı

6 Kasım 2026, Europe/Istanbul. Kullanıcı şimdilik ara verdi; bu dosya sonraki oturum için devir notudur.

## Kullanıcının devam eden sınırları

- **Gerçek veriler gelmeden nihai eğitim veya nihai model yayını yapma.** Mevcut model sentetik geliştirme demosudur; gerçek kullanıcı ihtiyacıyla doğrulanmış gibi sunulamaz.
- Başka projeleri ve sistem/güvenlik ayarlarını değiştirme; ücretli hizmet kullanma.
- GitHub Pages yayını açık kalacak. Teslim formunu kullanıcı adına gönderme.
- İnsan oturumu, değerlendirme, metrik veya yayın bağlantısı uydurma. Eksik insan/hesap katkısını açıkça belirt.

## Kaydedilen mevcut durum

- Proje klasörü: `C:\Users\bjkzl\Desktop\SE-Primer-v2`.
- Duraklatma öncesindeki son Git commit'i: `99df60e` (belgeler ve canlı kontrol sonuçları). Çalışma ağacı bu not yazılmadan önce temizdi.
- Yayımlanan uygulama kaynak commit'i: `ebb2b9126714e54e1d26839e652657a903bff246`.
- Eğitim öncesi kabul eşikleri ayrı commit'te kaydedildi: `5e9008e`.
- GitHub: https://github.com/zulal836/se-primer-v2-2026
- Açık kalacak uygulama: https://zulal836.github.io/se-primer-v2-2026/
- Demo: https://zulal836.github.io/se-primer-v2-2026/demo.mp4
- Başarılı bulut test/build/deploy koşusu: https://github.com/zulal836/se-primer-v2-2026/actions/runs/42100198789
- HF nihai model deposu/commit bağlantısı **yok**. Son kontrolde yerel HF girişi bulunmadı; GitHub kimliği kullanılabildi.

## Tamamlananlar

- Türkçe, mobil ekrana uyumlu Vite web oyunu: üç profil sorusu, çift rezervasyon senaryosu, üç karar, sekiz yol, iki son, teknik sonuçlar ve sabit Sokratik tutor metinleri. Üretim sırasında LLM/API çağrısı yok.
- Kural modu, gerçek `onnxruntime-web` çıkarımı ve görünür kural yedeği. Model açıklama derinliğini gerçekten değiştiriyor.
- Açık katılım, rastgele oturum kimliği, karar bazlı yerel kayıt, model yardımından önce öz bildirim etiketi, CSV indirme, yeni oturum ve silme akışı.
- `data/oturumlar.csv` yalnız başlık içeriyor; gerçek insan oturumu eklenmedi. Gerçek CSV Git'ten hariç tutuluyor. Kurulum, eksikse `data/oturumlar.example.csv` üzerinden boş dosyayı oluşturur.
- Veri sözlüğü ve CSV birleştirme aracı. Sentetik veri ayrı dosyada, üretici ve seed=42 belgeli.
- Oturum bazlı split, önceden belirlenen eval kapısı, sklearn→ONNX dönüşümü, JSON şeması, model kartı, hash'ler, beş Python oracle girdisi ve tarayıcı paritesi.
- Model/config/oracle, eğitim tekrarında bayt düzeyinde aynı üretildi; ONNX graph adı sabitlendi.
- GitHub ve ücretsiz Pages yayını; HF için gerçek-veri kapısı olan yayın betiği ve sabit commit manifest akışı hazır.
- README, RELEASE, TEST_SONUCLARI, SINAV_TASARIMI, 20 örneklik tutor değerlendirme taslağı ve demo belgeleri hazır.
- `public/demo.mp4` gerçek tarayıcı kaydıdır: **73.040 saniye**. Cypress otomatik oynatımıdır, insan oturumu değildir; seslendirme yoktur. Sentetik demo etiketi görünür.

## Gerçekte doğrulananlar

- Model eklenmeden temel oyun: 11/11 Cypress testi.
- Son suite: 15/15 Cypress testi (12 oyun + 3 model/parite); yerel geliştirme, üretim paketi ve bulut ortamında geçti.
- Python: 6/6 test; beş ONNX referans girdisi geçti.
- Canlı sitede giriş yapılmamış yeni tarayıcı oturumu: 2/2 test; gerçek ONNX, beş referans olasılığı, oyun sonu ve public MP4 doğrulandı.
- Tarayıcı/Python en büyük ölçülen olasılık farkı yaklaşık `1.1920928955e-7`; kabul sınırı `<1e-4`.
- Sentetik eval: balanced accuracy `0.9260651629`, ayrıntılı recall `0.9047619048`. Bunlar gerçek insan sonuçları değildir.
- sklearn/ONNX en büyük fark: `1.0823183327e-7`.
- Build ve GitHub Pages deploy başarılı; npm audit: 0 güvenlik açığı.
- Yayımlanan model SHA-256: `5a08f081cdf16ec82365879e2cad5479575481de0a3eb59e1313a1f8a1982938`.
- Ayrıntılar: `TEST_SONUCLARI.md`, `test-results/`, `publication.json`.

İlk WASM indirmesi yaklaşık 12 MB ve onlarca saniye sürebiliyor. İlk canlı test 60 saniyede zaman aşımına uğradı; 180 saniyelik sınırla ikinci koşu 48 saniyede geçti. Model hazır olana kadar oyun kural yedeğiyle çalışabilir. Fiziksel telefondan erişim ayrıca denenmedi; mobil viewport test edildi.

## Yerel sunucular

Bu proje için açılan Vite geliştirme sunucusu 5173 portunda, PID 3912 ve proje içindeki `vite.js` komutuyla doğrulandıktan sonra durduruldu. 5175 önizleme ve 5180 test sunucuları da kapanmıştı. Son port kontrolünde 5173/5175/5180 üzerinde dinleyen sunucu kalmadı. Başka projelerin süreçleri durdurulmadı. GitHub Pages'e kapatma/değiştirme işlemi yapılmadı.

## Kalan zorunlu işler ve önerilen sıra

1. Gönüllülerden **en az 15 tamamlanmış gerçek oturum** topla (ör. üç kişi beşer oyun). Her oturum üç karar içersin; kaynak `gerçek` olsun. Oyuncu model yardımını görmeden kısa/ayrıntılı ihtiyacını kendisi bildirsin. Katılım ve kişisel bilgi toplamama koşulları korunsun.
2. CSV'leri `private-data/` altında tut; `scripts/merge_csv.py` ile birleştir. Yinelenen/çelişen kayıtları, tamamlanmış farklı oturum sayısını ve sınıf sayılarını kontrol et. Ham gerçek veriyi public depoya gönderme.
3. `eval/tutor_eval.csv` içindeki 20 örneği insan değerlendirsin. Şu an insan etiketleri boş ve durum `bekliyor`; başarı oranı hesaplanmadı.
4. **Ancak gerçek veriler geldikten sonra** varsayılan `train.py` komutuyla gerçek veri eğitimini çalıştır. En az 15 tamamlanmış oturum, her sınıfta en az 10 etiket ve testte her sınıftan en az beş örnek aranıyor. Daha fazla veri gerekebilir. Balanced accuracy >=0.70 ve ayrıntılı recall >=0.65 eşiklerini sırf geçsin diye düşürme. Başarısız model yeni sürüm olarak yayımlanmasın.
5. Python/ONNX paritesi, sözleşme, tüm E2E ve regresyon testlerini gerçek model adayıyla yeniden çalıştır. Mevcut bazı testler sentetik demo durumuna göre yazıldı; gerçek modele geçerken beklentileri dürüstçe gözden geçir, kapıları gevşetme veya çıkarımı taklit etme.
6. Kullanıcı HF girişini tamamlasın (`.venv/Scripts/hf.exe auth login`). Uygun gerçek model için `scripts/publish_model.py` ile yeni public model deposu oluştur; model/config aynı commit'te yüklensin. Web manifestini o tam commit'e sabitle; tekrar test edip Pages'e yayınla.
7. Gerekirse demoyu nihai modelle yenile. Mevcut video sentetik demo içindir. Shadow/Canary/Progressive Rollout RELEASE.md'de **plan** durumundadır, uygulanmış trafik yönlendirmesi gibi anlatılmasın.
8. Dört teslim bağlantısını tamamla: GitHub, commit'e sabit HF modeli, girişsiz uygulama, video. HF bağlantısı şu an eksik. Formu kullanıcı göndersin.

## Sonraki oturumda başlama

Önce bu dosyayı ve `git status` çıktısını oku; mevcut durumu sıfırdan kurma. Yerel bağımlılıklar kurulu ve model dosyaları mevcut.

```powershell
npm run dev
```

Kurulum eksik bir kopyadaysa `node scripts/setup.mjs` kullanılır. Oturum CSV'leri gelmediyse nihai eğitim/yayına geçilmez. Gerçek veri geldikten sonraki komutlar:

```powershell
.venv/Scripts/python.exe scripts/merge_csv.py private-data/oyun1.csv private-data/oyun2.csv
.venv/Scripts/python.exe train.py
```

Yalnız yerel test gerektiğinde `node scripts/test_e2e.mjs` kendi test sunucusunu açıp kapanışta durdurur. Python kontrolleri ve yayın ayrıntıları README'de. `scripts/publication_status.py` mevcut public GitHub Actions durumunu okur; yeni depo oluşturmak için kullanılan `publish_github.py --push` mevcut depo üzerinde yeniden çalıştırılmaz.

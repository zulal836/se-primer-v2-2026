# SE Primer v2 — Son Boş Randevu

Türkçe, telefona uyumlu üç kararlı yazılım mühendisliği oyunu. Çift rezervasyon olayında sürüm geri alma, eşzamanlılık testi ve kişisel veriyi koruma ele alınır. Üç profil sorusu anlatımı uyarlar. Kural modu ile gerçek ONNX kullanan davranış modeli karşılaştırılabilir. Sunucu, kullanıcı hesabı veya ücretli API gerekmez.

**Durum:** gerçek katılımcı verisi henüz yok. Model, açıkça işaretlenmiş sentetik geliştirme demosudur. Nihai gerçek-veri değerlendirmesi, HF yayını ve insan tutor değerlendirmesi bekler. Yaklaşık 71 saniyelik gerçek tarayıcı demo kaydı `public/demo.mp4` içinde hazırdır; otomatik oynatılmıştır, insan oturumu değildir. Güncel test sonuçları `TEST_SONUCLARI.md`, yayın durumu `RELEASE.md` içindedir.

## Başlangıç: en fazla üç komut (Windows PowerShell)

Node 22+ ve Python 3.12 kurulu olmalı. Proje klasöründe:

```powershell
node scripts/setup.mjs
npm run dev
```

Bilgisayarda http://localhost:5173 açılır. Telefon aynı Wi-Fi'deyken Vite'ın terminalde verdiği Network adresini kullanır. Yerel ağ erişimi cihaz/güvenlik duvarı koşullarına bağlıdır; bu proje sistem ayarlarını değiştirmez. HTTPS public yayın, telefon paylaşımını kolaylaştırır. Sayfa yalnız yerel depolama kullanır, arka uca veri göndermez. Tarayıcı gizli modda da oyun çalışır, pencere kapanınca yerel kayıtlar silinebilir.

Linux/macOS: `python3 -m venv .venv` sonrasında `.venv/bin/python -m pip install -r requirements.txt`, `npm ci`, `node scripts/copy_runtime.mjs`; model hazır değilse `.venv/bin/python scripts/generate_demo.py` ve `.venv/bin/python train.py --demo`. Windows yolu `.venv/Scripts/python.exe` biçimindedir.

## Veri toplama

Girişte açık katılım seçeneği var; katılmadan oynanabilir. Her sahnede model sonucu görülmeden kısa/ayrıntılı açıklama isteği sorulur. Yanıt vermemek mümkündür; boş etiket eğitim dışıdır. Süre, seçenek değiştirme ve ipucu isteme yalnız o kararda ölçülür. Model geri bildirim yanıtını, seçimin doğruluğunu veya geleceği girdi almaz.

En az **15 tamamlanmış gerçek oturum** toplayın (ör. üç gönüllü × beş oyun). Her oyun üç karar ve yeni rastgele kimlik üretir. Oturum sayısı kişi sayısı değildir; aynı insan iki eval grubunda olabilir. Bu sınırlama model kartında yazılıdır. Oyun bitince telefondan CSV indirilir. Her cihazın CSV'sini `private-data/` içine koyun:

```powershell
.venv/Scripts/python.exe scripts/merge_csv.py private-data/oyun1.csv private-data/oyun2.csv
.venv/Scripts/python.exe train.py
```

Eğitim varsayılan olarak yalnız `data/oturumlar.csv` gerçek verisini okur. Başlangıç dosyası boş; gerçek kayıt uydurulmamıştır. Veri sözlüğü, saklama/silme ve birleştirme ayrıntıları `data/SOZLUK.md` içindedir. Kimlik ya da hasta verisi toplamayın. Toplanan gerçek CSV'yi public depoya göndermeyin.

## Eğitim ve sözleşme

`spec.md` eğitimden önce yazıldı: balanced accuracy >=0.70, ayrıntılı sınıf recall >=0.65. Sabit seed=42 ile oturum bazında %25 test ayrılır. Aynı oturum iki tarafta bulunmaz. Her sınıfın testte en az beş örneği gerekir. Kapı başarısızsa önceki artefakt korunur. Yetersiz veriyle eşik düşürmek yerine veri toplanır ve sorun araştırılır.

Model: StandardScaler → LogisticRegression. Girdi `features`, float32 `[n,3]`; sıra bekleme_sn, degistirme_sayisi, ipucu_sayisi. Çıkış `probabilities` `[n,2]`; sınıf sırası kısa, ayrıntılı. p>=0.5 ise ayrıntılı yardım. `config.json` özellikler, tipler, sınıflar, metrikler, eşikler, split ve SHA-256 içerir; JSON şeması eğitimde doğrulanır. `model/README.md` model kartıdır. Python sklearn/ONNX farkı 1e-4'ü aşarsa eğitim durur.

Sentetik geliştirme için ayrı komutlar:

```powershell
.venv/Scripts/python.exe scripts/generate_demo.py
.venv/Scripts/python.exe train.py --demo
```

Üretici seed=42, 160 kurgusal oturum, her biri üç karar. Süre 1–130 saniye, değişim 0–6, ipucu 0–3; gizli skor `süre/65 + değişim/2 + ipucu*0.9 > 3.8`, %8 etiket gürültüsü. Bu, insan ihtiyacının ölçülmesi değildir. Geliştirme modeli `publishable=false` işaretlenir. `train.py` aynı veri ve ortamda aynı split ve metrikleri üretir. Tekrarlanabilir tam ortam için kurulumdan sonra alınan `requirements-lock.txt` de mevcuttur.

## Doğrulama

Vite çalışırken:

```powershell
.venv/Scripts/python.exe -m unittest discover -s tests -p "test_*.py"
.venv/Scripts/python.exe tests/parite.py
npm run test:e2e
npm run build -- --base=./
```

Temel oyun testleri model üretilmeden önce `npm run test:base` ile çalıştırılır, modelden sonra tüm suite regresyon olarak tekrar çalıştırılır. Sekiz yol, iki son, profil, katılım, yeniden başlatma, CSV, yerel silme ve yükleme hatasında yedek test edilir. Python oracle beş sabit girdinin gerçek ONNX olasılıklarını verir; Cypress aynı gerçek dosyada toleransı kontrol eder. Model yardım derinliğini DOM üzerinde değiştirmelidir. Test yüzeyi `window.primer.predict` yalnız gerçek üretim çıkarımını çağırır. Model testinde inference taklidi yoktur; yedek testinde yalnız başarısız indirme simüle edilir.

Tutor sabit Sokratik metinlerden oluşur, LLM çıktısı diye sunulmaz. `eval/tutor_eval.csv` 20 değerlendirme örneği ve boş insan etiketlerini içerir. Henüz insan başarım oranı hesaplanmamıştır. `SINAV_TASARIMI.md` ayrı klasik vize sorusudur; oyuna eklenmez. `DEMO.md` 75 saniyelik çekim planıdır.

## Yayın

Hesap erişimiyle yeni GitHub public reposu oluşturup bu klasörü main dalına gönderin; Settings → Pages → GitHub Actions seçin. `.github/workflows/pages.yml` gerçek Cypress testlerinden sonra ücretsiz Pages yayını yapar. Ortak dizin altında çalışabilmesi için build `--base=./` kullanır. Repo kurulumu otomasyonu `scripts/publish_github.py` içindedir.

Gerçek veri modeli kapıyı geçtikten sonra:

```powershell
.venv/Scripts/hf.exe auth login
.venv/Scripts/python.exe scripts/publish_model.py KULLANICI/YENI_PRIMER_MODEL --push
```

Betik mevcut depoları değiştirmez; yeni public HF reposu açar, model+config aynı commit'te yüklenir, indirilen içerikler doğrulanır. Manifestte 40 haneli commit sabitlenir; web değişken main URL'sini kullanmaz. Demo yerelde paketlenmiş dosyayı kullanır. Model indirme başarısızsa durum görünür ve kural yedeği oyunu sürdürür. HF sonrası parite/build çalıştırıp yeni web sürümünü yayınlayın. Rollout ve geri alma `RELEASE.md` içindedir.

Teslim için dört gerçek bağlantı: GitHub reposu, commit'e sabit HF modeli, girişsiz uygulama, 60–90 sn demo video. Form kullanıcı tarafından gönderilir.

## Ürün kararları

- Native mobil yapılmadı: tek web uygulaması dersin uçtan uca çıkarım koşulunu karşılıyor.
- Serbest sohbet eklenmedi: sabit Sokratik sorular, ücretsiz ve denetlenebilir bir tutor sağlıyor.
- Sunucu ve hesap eklenmedi: davranış verisi cihazda kalıyor, kurulum ve gizlilik yükü azalıyor.

## İncelenen kaynaklar

- [Başlangıç reposu README ve AGENTS](https://github.com/seyyah/huggingface-hello-web): sözleşme, yerel eğitim, model paketleme. `hf_cli.py` içindeki `onnx_aktar` ve `web/index.html` incelendi; zipmap=false olasılık tensörü ve sklearn/ONNX tolerans kontrolü yaklaşımından yararlanıldı. Bu projede bağımsız üç özellik, seed=42 ve `features` girdi adı kullanılıyor; tüm tüketiciler buna uyarlanmıştır. Mobil/Rails/diyabet verisi taşınmadı.
- [ONNX Runtime Web deployment](https://onnxruntime.ai/docs/tutorials/web/deploy.html): WASM dosyaları npm sürümüyle birlikte yerelden sunulur; CDN sürüm uyuşmazlığı önlenir.
- [scikit-learn GroupShuffleSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html): oturumları gruplar halinde ayırma. StandardScaler yalnız eğitim bölümünde fit edilir.
- [Hugging Face Hub upload](https://huggingface.co/docs/huggingface_hub/guides/upload): dosyaları tek commit'te yükleme ve commit'ten indirme.
- [Model Cards for Model Reporting, Mitchell vd. 2019](https://arxiv.org/abs/1810.03993): amaç, değerlendirme ve kullanım sınırlarını görünür kılan model kartı yapısı.

## AI araç kullanımı beyanı

1. OpenAI Codex; oyun, spec ve veri toplama akışının ilk sürümünü oluşturdu.
2. Codex; eğitim, ONNX, yayın betikleri ve testleri yazıp komutlarla doğruladı; gerçek sonuçlar test raporunda yer alır.
3. Codex; belgeler, tutor değerlendirme taslağı ve demo planını hazırladı. Tutor metinleri üretim sırasında LLM ile oluşturulmaz.
4. Kullanıcıya yapılmamış manuel düzeltme, insan değerlendirmesi veya gerçek oturum katkısı atfedilmemiştir. Gerçek veri ve insan incelemesi beklemektedir.

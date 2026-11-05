---
license: mit
library_name: sklearn
tags: [onnx, education, tabular-classification]
---
# Son Boş Randevu model kartı

Amaç: üç davranış girdisinden kısa/ayrıntılı açıklama seçmek; klinik karar veya öğrenci notu değildir.

Sürüm: 0.1.0-demo. Kaynak: **sentetik**. SENTETİK DEMO: gerçek insan ihtiyacıyla doğrulanmamıştır; nihai yayına uygun değildir.

Değerlendirme: oturum bazlı %25 holdout, seed=42; 120 eğitim / 40 test oturumu. Balanced accuracy=0.926065, ayrıntılı recall=0.904762. ONNX maksimum fark=1.082318333e-07.

Kabul eşiği: balanced accuracy >=0.70 ve recall >=0.65. Eşik önceden spec.md'de tanımlıdır. Olasılık eşiği 0.5; kalibrasyon garantisi yoktur. Kural tabanlı yedek kullanılabilir.

Sınırlar: öz bildirim yanlılığı, küçük örneklem, farklı cihazların süre ölçümü ve tekrar oynama etkisi. Sentetik veri üreticisi davranış ile etiket ilişkisini kurgular; yüksek puan insan genellemesini göstermez. Oturum ayrımı kişi ayrımı değildir, aynı insan iki split'te bulunabilir. Arayüz beklenti etkisi yaratabilir. İnsan öğrenme çıktısını ayrıca ölçmek gerekir.

Kullanılmaması gereken durumlar: sağlık/klinik karar, kişilik çıkarımı, sınav puanlama, öğrenci eleme, hassas veri işleme. Model ve eğitim kodu public olabilir; kişiler hakkında hüküm verilemez.

Özellik sırası/tipi, sınıflar ve veri/model hash'leri config.json sözleşmesindedir. JSON şeması eğitimde doğrulanır. Kaynak yaklaşım: https://github.com/seyyah/huggingface-hello-web ; yeni oyun ve eğitim bağımsız hazırlanmıştır.

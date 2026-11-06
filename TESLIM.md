# Teslim bağlantıları ve dürüst durum açıklaması

1. GitHub: https://github.com/zulal836/se-primer-v2-2026
2. Commit'e sabit **nihai gerçek HF modeli yoktur**: kabul kapısı geçilmediği için yayımlanmadı. Bağlantı uydurulamaz. HF girişi de mevcut değil.
3. Girişsiz uygulama: https://zulal836.github.io/se-primer-v2-2026/
4. 73.040 saniyelik demo: https://zulal836.github.io/se-primer-v2-2026/demo.mp4

Uygulama ve video açıkça etiketlenmiş **sentetik geliştirme demosunu** gösterir; başarısız gerçek model kullanılıyormuş gibi sunulmaz. Video gerçek tarayıcı kaydı, otomatik oynatım ve sessizdir.

## Forma yazılabilecek kısa açıklama

> Türkçe web oyunu, gönüllü anonim veri toplama, ONNX tarayıcı çıkarımı, Python/web paritesi ve E2E regresyon testleri tamamlandı. Gerçek CSV'ler tekrarlar ayıklanarak birleştirildi: 32 tamamlanmış oturum, 49 kullanılabilir etiket. Sabit dış test korunarak yalnız eğitim oturumlarında beş katlı grup çapraz doğrulamasıyla sınıf ağırlıklı lojistik regresyon ve küçük karar ağacı karşılaştırıldı. Eğitim doğrulamasında seçilen lojistik regresyon dış testte bir kez değerlendirildi: dengeli doğruluk 0,25 ve ayrıntılı yardım recall 0,50. Önceden belirlenen 0,70/0,65 kabul kapısı geçilemediği için nihai gerçek model yayımlanmadı. Mevcut canlı uygulama ve 73 saniyelik video sentetik demo olarak etiketlidir. Başarısız gerçek eğitim sonuçları, model seçim protokolü ve test raporları depodadır.

## Tamamlanmayan v2 koşulları

- Kabul eşiğini geçen gerçek model ve ona ait ONNX/config/model kartı paketi.
- Aynı HF commit'ine sabitlenmiş nihai model/config bağlantısı ve o modelle çalışan web yayını.
- Nihai gerçek modelle yenilenmiş 60–90 saniyelik video. Mevcut sentetik demo videosu hazırdır.

Önceki ödevden kalan 20 tutor değerlendirmesi **bu v2 tesliminin engeli değildir**. Dosya taslak/bekliyor olarak korunur, yapılmış insan değerlendirmesi iddiası yoktur. Form kullanıcı tarafından gönderilir; formun HF alanı zorunluysa mevcut eksik link için gerçek durum açıklanmalı, sentetik link nihai model diye yazılmamalıdır.

## İnceleme için dosyalar

Son doğrulamalar: 9 Python testi, 15 Cypress testi, beş Python ONNX referansı ve üretim build'i geçti. Parite ve oyun testleri mevcut sentetik demo artefaktına aittir. Nihai gerçek aday eval kapısında reddedildi. [Son Pages koşusu](https://github.com/zulal836/se-primer-v2-2026/actions/runs/42281454788) 15 test/build/deploy ile başarılı. Ayrıca 2/2 girişsiz canlı test geçti: ONNX, oyun sonu ve MP4. Yayımlanan kaynak commit'i `1fd3e31615e56d153d64fd5ea81d2fd79ec8d6da`; makbuz `publication.json`.

`MODEL_SECIMI.md`: karşılaştırma öncesi sabitlenmiş yöntem. `test-results/final-model-selection.json`: beş katın gerçek sonuçları, yalnız CV ile aday seçimi, tek dış test sonucu ve ret. `TEST_SONUCLARI.md`: testler. `RELEASE.md`: dağıtım ve geri alma. `model/README.md`: mevcut sentetik artefaktın kartı ve başarısız gerçek adayın ayrımı. Ham CSV'ler public depoda yoktur.

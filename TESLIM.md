# Teslim bağlantıları ve dürüst durum açıklaması

1. GitHub: https://github.com/zulal836/se-primer-v2-2026
2. Commit'e sabit **HF SENTETİK DEMO modeli**: https://huggingface.co/zulalertrk/se-primer-v2-synthetic-demo/resolve/d79adb407da3be479d77fe4a909b932bc1b77a8a/model.onnx
3. Girişsiz uygulama: https://zulal836.github.io/se-primer-v2-2026/
4. 73.040 saniyelik demo: https://zulal836.github.io/se-primer-v2-2026/demo.mp4

Uygulama ve video açıkça etiketlenmiş **sentetik geliştirme demosunu** gösterir; başarısız gerçek model kullanılıyormuş gibi sunulmaz. Video gerçek tarayıcı kaydı, otomatik oynatım ve sessizdir.

HF deposu public ve yalnız `0.1.0-demo` modelidir. Model/config/kart/şema **aynı** `d79adb407da3be479d77fe4a909b932bc1b77a8a` commit'inde; [config](https://huggingface.co/zulalertrk/se-primer-v2-synthetic-demo/resolve/d79adb407da3be479d77fe4a909b932bc1b77a8a/config.json) ve [model kartı](https://huggingface.co/zulalertrk/se-primer-v2-synthetic-demo/blob/d79adb407da3be479d77fe4a909b932bc1b77a8a/README.md). Bu HF DEMO bağlantısı nihai kabul edilmiş gerçek model bağlantısı değildir. `publishable=false` ve gerçek model ret kararı korunur.

## Forma yazılabilecek kısa açıklama

> 32 tamamlanmış gerçek oturumdan 49 kullanılabilir etiketle yapılan gerçek eğitim, sabit testte BA=0,25 ve ayrıntılı yardım recall=0,50 vererek önceden belirlenen 0,70/0,65 kabul kapısını geçemedi. Bu nedenle nihai gerçek model yayımlanmadı. Paylaşılan HF modeli açıkça SENTETİK GELİŞTİRME DEMOSU olan 0.1.0-demo sürümüdür; model/config/kart aynı commit'e, web uygulaması bu commit'e sabitlenmiştir. Sentetik değerlendirme sonuçları gerçek kullanıcı başarımı değildir. Canlı uygulama ve 73 saniyelik video aynı sentetik modeli gösterir. Parite, regresyon ve gerçek modelin başarısızlık sonuçları depoda belgelenmiştir.

## Tamamlanmayan v2 koşulları

- Kabul eşiğini geçen gerçek model ve ona ait ONNX/config/model kartı paketi.
- Aynı HF commit'ine sabitlenmiş nihai model/config bağlantısı ve o modelle çalışan web yayını.
- Nihai gerçek modelle yenilenmiş 60–90 saniyelik video. Mevcut sentetik demo videosu hazırdır.

Önceki ödevden kalan 20 tutor değerlendirmesi **bu v2 tesliminin engeli değildir**. Dosya taslak/bekliyor olarak korunur, yapılmış insan değerlendirmesi iddiası yoktur. Form kullanıcı tarafından gönderilir; HF alanına bu demo linki yazılırsa açıklamada SENTETİK DEMO olduğu ve gerçek modelin kabul edilmediği mutlaka belirtilir.

## İnceleme için dosyalar

Son doğrulamalar: 9 Python testi, 15 Cypress testi, beş Python ONNX referansı ve üretim build'i geçti. Parite ve oyun testleri mevcut sentetik demo artefaktına aittir. Nihai gerçek aday eval kapısında reddedildi. [Son Pages koşusu](https://github.com/zulal836/se-primer-v2-2026/actions/runs/42281454788) 15 test/build/deploy ile başarılı. Ayrıca 2/2 girişsiz canlı test geçti: ONNX, oyun sonu ve MP4. Yayımlanan kaynak commit'i `1fd3e31615e56d153d64fd5ea81d2fd79ec8d6da`; makbuz `publication.json`.

`MODEL_SECIMI.md`: karşılaştırma öncesi sabitlenmiş yöntem. `test-results/final-model-selection.json`: beş katın gerçek sonuçları, yalnız CV ile aday seçimi, tek dış test sonucu ve ret. `TEST_SONUCLARI.md`: testler. `RELEASE.md`: dağıtım ve geri alma. `model/README.md`: mevcut sentetik artefaktın kartı ve başarısız gerçek adayın ayrımı. Ham CSV'ler public depoda yoktur.

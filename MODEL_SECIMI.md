# Son karşılaştırma protokolü — 6 Kasım 2026

Kullanıcı isteğiyle, bu karşılaştırma çalıştırılmadan önce sabitlendi.

- Veri ve etiketler değiştirilmez. 0=kısa, 1=ayrıntılı; boş hedefler ve yarım oturumlar hariç. Özellik sırası süre, seçenek değiştirme sayısı, ipucu sayısıdır.
- Mevcut dış test bölümü aynen korunur: GroupShuffleSplit(test_size=0.25, random_state=42). Dış test daha önce temel lojistik regresyonda görülmüştür; tüm süreci hiç görülmemiş bağımsız test olarak tanımlamayız.
- Yalnız dış eğitim oturumlarında beş katlı StratifiedGroupKFold(shuffle=True, random_state=42). Aynı oturum bir katın eğitim ve doğrulamasında birlikte bulunamaz. Ölçekleyici yalnız katın eğitiminde fit edilir.
- Aday 1: StandardScaler + LogisticRegression(class_weight=balanced, C=1, max_iter=1000, random_state=42).
- Aday 2: DecisionTreeClassifier(max_depth=3, min_samples_leaf=3, class_weight=balanced, random_state=42).
- Başka hiperparametre/aday taraması yok. Seçim: ortalama kat balanced accuracy; eşitse ortalama ayrıntılı recall; hâlâ eşitse lojistik regresyon. Seçim raporu dış test değerlendirilmeden diske yazılır.
- CV, test ve web aynı kararı kullanır: p(ayrıntılı)>=0.5 ise 1. sklearn `predict` eşit olasılıkta ilk sınıfı seçebildiği için değerlendirme açık olasılık eşiğiyle yapılır; önceden yazılı 0.5 eşiği değişmez.
- Tek seçilen aday tüm dış eğitim verisine fit edilir, mevcut dış testte bir kez değerlendirilir. Teste göre başka adaya geçilmez. Aynı veri/protokolle yeniden çalıştırma ikinci test değerlendirmesini reddeder.
- Kabul eşiği değiştirilmez: balanced accuracy>=0.70, ayrıntılı recall>=0.65; testte her sınıf en az beş örnek. Eşik geçilmezse model paketlenmez/yayımlanmaz.
- 20 tutor değerlendirmesi bu v2 tesliminin kabul/yayın kapısı değildir. Yapılmamış insan değerlendirmesi yapılmış gösterilmez.

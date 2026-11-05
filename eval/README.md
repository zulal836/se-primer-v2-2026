# Tutor değerlendirmesi — insan incelemesi bekliyor

20 örnek `tutor_eval.csv` içindedir. Yanıtlar sabit tutor politikasının taslak örnekleridir, çevrimiçi LLM çağrısı veya insan puanı değildir. İnsan etiketleri boş ve durum “bekliyor”.

Bir değerlendirici her yanıtı okuyup `cevabi_soyluyor` (0/1), `teknik_hata` (0/1), `soru_yararli` (0/1) alanlarını doldurur. Cevabı ele verme oranı = 1 sayısı / incelenen örnek sayısı; teknik hata ve yararlı soru oranları da aynı payda ile raporlanır. Bekleyen örnekler paydaya eklenmez. Örneklem küçük olduğundan sayıları oranla birlikte yazın (ör. 1/20). İkinci bağımsız değerlendirici varsa uyuşmazlıkları gerekçeleriyle çözün. İnsan incelemesi yapılmadan başarı oranı yayımlamayın.

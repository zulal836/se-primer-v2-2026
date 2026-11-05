import "./style.css";
import { loadModel, predict } from "./model.js";
const app = document.querySelector("#app");
const scenes = [
  {
    title: "Önce hasarı sınırla",
    text: "08.00. Yeni sürümden sonra aynı randevu saati iki kez satıldı. Yazma trafiği sürüyor. Önce hangi yolu seçersin?",
    options: [
      "Yeni rezervasyonları durdur; şema uyumunu kontrol edip önceki sürüme dön.",
      "Canlıda hızlı bir yama yap; yeni rezervasyonları açık tut.",
    ],
    hint: "Bir değişikliği geri almak, veritabanındaki değişiklikleri de geri alır mı?",
    detail:
      "Sürüm ve veritabanı şeması ayrı değişir. Önce etkilenen yazmaları sınırlamak gerekir. Şema uyumluluğu, yedek ve ileri/geri migrasyon planı olmadan geri dönüş de risklidir.",
    results: [
      "Yazmalar sınırlandı. Şema uyumluluğu doğrulanarak önceki sürüme dönüldü; tutarsız randevular uzlaştırma kuyruğunda.",
      "Yama sırasında yeni çift kayıtlar oluştu. İncelenmemiş canlı değişiklik etki alanını büyüttü.",
    ],
  },
  {
    title: "Tek kullanıcı yeter mi?",
    text: "Yama hazır. Hata, iki isteğin aynı boş saati aynı anda görmesiyle oluşuyor. Hangi kanıtı toplarsın?",
    options: [
      "Eşzamanlı iki isteği çalıştır; tek rezervasyon oluştuğunu ve eski akışları doğrula.",
      "Tek kullanıcıyla başarılı rezervasyon yap; doğrudan tüm trafiğe aç.",
    ],
    hint: "İki istek aynı bilgiyi aynı anda okursa, tek kullanıcılı test neyi kaçırır?",
    detail:
      "Eşzamanlılık testi yarış koşulunu tetikler. Veritabanı benzersizlik kısıtı veya atomik işlem korunmalıdır. Regresyon testleri mevcut iptal ve yeniden rezervasyon davranışını da korur.",
    results: [
      "İki istekten yalnız biri kabul edildi. İptal ve yeniden rezervasyon testleri de geçti; kapsamlı kanıtla sınırlı dağıtıma hazırsın.",
      "Tek kullanıcı testi yarış koşulunu tetiklemedi. Başarı mesajı eşzamanlılık hatasının düzeldiğine kanıt değildir.",
    ],
  },
  {
    title: "Olay kaydı neyi taşımalı?",
    text: "Ekip hata kaydını istiyor. Ham kayıtta hasta adı ve iletişim bilgisi bulunabileceğini fark ettin. Ne yaparsın?",
    options: [
      "Kişisel alanları çıkar; yalnız anonim olay kodu, zaman aralığı ve teknik hata türünü paylaş.",
      "Ham logu ekip kanalına gönder; herkes sorunu hızlıca görsün.",
    ],
    hint: "Sorunu yeniden üretmek için gerçekten hangi alanlar gerekli?",
    detail:
      "Veri minimizasyonu ve erişim sınırı hata incelemesinin parçasıdır. Rastgele teknik olay kodu yeterliyse isim ya da iletişim bilgisi taşınmamalı; anonimleştirme yeniden tanımlamayı da değerlendirmelidir.",
    results: [
      "Teknik kanıt kişisel alanlar olmadan paylaşıldı. Erişim ve saklama süresi sınırlandı.",
      "Gereksiz kişisel alanlar yayıldı. Sistem çalışsa bile veri sızıntısı ayrı bir olay incelemesi gerektirir.",
    ],
  },
];
const columns = [
  "oturum_id",
  "karar_no",
  "bekleme_sn",
  "degistirme_sayisi",
  "ipucu_sayisi",
  "ayrinti_istegi",
  "secim",
  "seviye",
  "rol",
  "hedef",
  "kaynak",
  "tamamlandi",
];
let rows = JSON.parse(localStorage.getItem("primer-rows") || "[]");
let s,
  ready = false,
  modelStatus = "Model yükleniyor…",
  modelConfig;
const esc = (v) =>
  String(v).replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
function reset() {
  s = {
    id: crypto.randomUUID(),
    step: 0,
    choices: [],
    selected: null,
    changes: 0,
    hints: 0,
    start: performance.now(),
    consent: false,
    mode: "model",
  };
  home();
}
function shell(content) {
  app.innerHTML = `<main><header><span class="brand">SE / PRIMER <small>v2</small></span><span class="tag">3 karar · 1 nöbet</span></header>${content}<footer><div class="status" data-cy="status">${esc(modelStatus)}</div><p>Veriler yalnız bu tarayıcıda saklanır. Gerçek hasta bilgisi girilmez. Tutor: sabit, Sokratik metinler; LLM kullanılmaz.</p><div class="actions"><button id="export">CSV indir (${rows.length} karar)</button><button id="clear">Yerel veriyi temizle</button><button id="restart">Yeni oturum</button></div><p id="toast" role="status"></p></footer></main>`;
  document.querySelector("#export").onclick = download;
  document.querySelector("#clear").onclick = () => {
    if (confirm("Bu tarayıcıdaki tüm karar kayıtları silinsin mi?")) {
      rows = [];
      save();
      reset();
    }
  };
  document.querySelector("#restart").onclick = reset;
}
function home() {
  shell(
    `<p class="eyebrow">BİR YAZILIM MÜHENDİSLİĞİ HİKÂYESİ</p><h1>Son boş randevu.<br>İki ayrı rezervasyon.</h1><p class="outcome">Yeni sürüm çıktı. Hastane randevu sisteminde bir yarış koşulu var. Nöbet sende: sistemi toparla, kanıtını topla, veriyi koru.</p><form id="profile" class="card"><div class="grid"><label>Seviye<select name="level"><option value="yeni">Yeni başladım</option><option value="deneyimli">Deneyimliyim</option></select></label><label>Rol<select name="role"><option>Geliştirici</option><option>Test mühendisi</option><option>Teknik lider</option></select></label><label>Öğrenme hedefi<select name="goal"><option>Güvenli sürüm</option><option>Test stratejisi</option><option>Veri gizliliği</option></select></label></div><label>Yardım yöntemi<select name="mode"><option value="model">Davranıştan öğrenen model (sentetik demo)</option><option value="rule">Temel kural: seviye / ipucu</option></select></label><p class="muted">İsteğe bağlı veri toplama: karar başına süre, seçenek değiştirme, ipucu sayısı ve istediğiniz açıklama derinliği kaydedilir. Rastgele oturum kimliği kullanılır. Kimlik, iletişim veya cihaz bilgisi toplanmaz. Katılmadan da oynayabilirsiniz. Dışa aktarmadıkça veri cihazınızdan çıkmaz. Her kararda model yardımını görmeden önce kendi ihtiyacınızı belirtin.</p><label class="consent"><input name="consent" type="checkbox">Bu anonim davranış verilerinin bu cihazda kaydedilmesine ve dışa aktardığım CSV'nin ders projesinde kullanılmasına katılıyorum.</label><div class="actions"><button class="primary" data-cy="start">Nöbeti devral →</button></div></form>`,
  );
  document.querySelector("#profile").onsubmit = (e) => {
    e.preventDefault();
    const f = new FormData(e.target);
    Object.assign(s, {
      level: f.get("level"),
      role: f.get("role"),
      goal: f.get("goal"),
      mode: f.get("mode"),
      consent: f.has("consent"),
    });
    scene();
  };
}
function scene() {
  s.selected = null;
  s.changes = 0;
  s.hints = 0;
  s.start = performance.now();
  const c = scenes[s.step];
  shell(
    `<div class="progress">${scenes.map((_, i) => `<span class="${i <= s.step ? "active" : ""}"></span>`).join("")}</div><p class="eyebrow">KARAR ${s.step + 1} / 3 · ${esc(s.role)} · ${esc(s.goal)}</p><h1 style="font-size:42px">${c.title}</h1><p>${c.text}</p><p class="muted">${s.level === "yeni" ? "Önce riski düşün. Bir seçeneği işaretleyebilir, göndermeden değiştirebilirsin." : "Etki alanını, kanıtı ve geri dönüş koşullarını birlikte değerlendir."}</p><div class="options">${c.options.map((v, i) => `<button class="option" data-cy="choice-${i}" data-choice="${i}">${String.fromCharCode(65 + i)} · ${v}</button>`).join("")}</div><div class="actions"><button id="hint" data-cy="hint">Düşündüren ipucu</button></div><div id="hint-text" aria-live="polite"></div><fieldset><legend>Bu anda ne kadar açıklama istersin?</legend><p class="muted">Model kararını görmeden bildir. Yanıtın modelin girdisi değildir.</p><div class="rating"><label><input type="radio" name="need" value="0"> Kısa ipucu yeter</label><label><input type="radio" name="need" value="1"> Ayrıntı isterim</label><label><input type="radio" name="need" value="skip" checked> Yanıtlamak istemiyorum</label></div></fieldset><button id="submit" class="primary" data-cy="submit" disabled>Kararı uygula →</button>`,
  );
  const roleFocus = {
    Geliştirici: "Kodun ve veritabanı işleminin hangi garantiyi verdiğini sorgula.",
    "Test mühendisi": "İddianı hangi gözlemlenebilir testin çürütebileceğini düşün.",
    "Teknik lider": "Ekibin etki alanını, sorumluluklarını ve durdurma koşullarını belirle.",
  }[s.role];
  const goalFocus = {
    "Güvenli sürüm": "Öğrenme odağın: geri dönüşü mümkün ve etkisi sınırlı bir değişiklik.",
    "Test stratejisi": "Öğrenme odağın: başarısızlığı görünür kılan bağımsız kanıt.",
    "Veri gizliliği": "Öğrenme odağın: teknik sorunu çözerken gereksiz kişisel veri taşımamak.",
  }[s.goal];
  document.querySelector('.options').insertAdjacentHTML('beforebegin',
    `<p class="muted" data-cy="profile-focus">${roleFocus} ${goalFocus}</p>`);
  document.querySelectorAll("[data-choice]").forEach(
    (b) =>
      (b.onclick = () => {
        const n = Number(b.dataset.choice);
        if (s.selected !== null && n !== s.selected)
          s.changes = Math.min(20, s.changes + 1);
        s.selected = n;
        document
          .querySelectorAll("[data-choice]")
          .forEach((x) => x.classList.toggle("selected", x === b));
        document.querySelector("#submit").disabled = false;
      }),
  );
  document.querySelector("#hint").onclick = () => {
    s.hints = Math.min(10, s.hints + 1);
    document.querySelector("#hint-text").innerHTML =
      `<p class="tutor">${c.hint}</p>`;
  };
  document.querySelector("#submit").onclick = submit;
}
async function submit() {
  document.querySelector("#submit").disabled = true;
  const x = [
    Math.min(300, (performance.now() - s.start) / 1000),
    s.changes,
    s.hints,
  ];
  const need = document.querySelector("[name=need]:checked").value;
  let p = null,
    detail = s.level === "yeni" || s.hints > 0,
    mode = "Kural tabanlı";
  if (s.mode === "model" && ready) {
    try {
      p = await predict(x);
      detail = p >= modelConfig.decision_threshold;
      mode =
        modelConfig.data_source === "sentetik"
          ? "ONNX · sentetik demo"
          : "ONNX · gerçek veri modeli";
    } catch {
      mode = "Kural yedeği · çıkarım hatası";
    }
  } else if (s.mode === "model") mode = "Kural yedeği · model hazır değil";
  s.choices.push(s.selected);
  if (s.consent) {
    rows.push({
      oturum_id: s.id,
      karar_no: s.step + 1,
      bekleme_sn: Number(x[0].toFixed(3)),
      degistirme_sayisi: x[1],
      ipucu_sayisi: x[2],
      ayrinti_istegi: need === "skip" ? "" : need,
      secim: s.selected,
      seviye: s.level,
      rol: s.role,
      hedef: s.goal,
      kaynak: "gerçek",
      tamamlandi: 0,
    });
    if (s.step === 2)
      rows
        .filter((r) => r.oturum_id === s.id)
        .forEach((r) => (r.tamamlandi = 1));
    save();
  }
  const c = scenes[s.step];
  shell(
    `<p class="eyebrow">TEKNİK SONUÇ · KARAR ${s.step + 1}</p><h2>${s.selected === 0 ? "Riski sınırladın." : "Bir risk açık kaldı."}</h2><p class="outcome" data-cy="consequence">${c.results[s.selected]}</p><div class="card"><span class="pill" data-cy="help-mode">${mode}</span><h2 data-cy="depth">${detail ? "Ayrıntılı açıklama" : "Kısa ipucu"}</h2><p class="tutor">${c.hint}</p>${detail ? `<p data-cy="detail">${c.detail}</p>` : ""}${p !== null ? `<p class="muted">p(ayrıntılı) = <span data-cy="p">${p.toFixed(7)}</span> · eşik 0.50</p>` : ""}<small>İpucu seçeneği söylemez. Teknik sonuç, karar uygulandıktan sonra açıklanır.</small></div><button id="next" data-cy="next" class="primary">${s.step === 2 ? "Nöbet raporunu gör" : "Sonraki karar →"}</button>`,
  );
  document.querySelector("#next").onclick = () => {
    s.step++;
    s.step === 3 ? end() : scene();
  };
}
function end() {
  const good = s.choices.every((x) => x === 0);
  shell(
    `<p class="eyebrow">NÖBET RAPORU</p><h1 data-cy="ending">${good ? "Kontrollü toparlanma" : "Olay incelemesi"}</h1><p>${good ? "Sistem kontrollü geri döndü, yarış koşulu sınandı ve kişisel veri taşınmadı. Sınırlı dağıtım ve izleme ile devam edebilirsin." : "Sistemi ayağa kaldırmak tek başına yeterli değil. Açık kalan teknik veya gizlilik risklerini incele; kanıtla doğrulanmış bir düzeltme planla."}</p><div class="card"><h2>Üç kararın izi</h2>${s.choices.map((v, i) => `<p>${i + 1}. ${scenes[i].title}: ${v === 0 ? "risk sınırlandı" : "inceleme gerekli"}</p>`).join("")}<p>${s.consent ? "Oturum tamamlandı; üç karar CSV indirmeye hazır." : "Katılım seçilmedi; bu oturum kaydedilmedi."}</p><button id="again" class="primary" data-cy="again">Yeniden oyna</button></div>`,
  );
  document.querySelector("#again").onclick = reset;
}
function save() {
  localStorage.setItem("primer-rows", JSON.stringify(rows));
}
function download() {
  const csv =
    "\uFEFF" +
    columns.join(",") +
    "\n" +
    rows
      .map((r) =>
        columns
          .map((k) => '"' + String(r[k] ?? "").replaceAll('"', '""') + '"')
          .join(","),
      )
      .join("\n");
  const url = URL.createObjectURL(
    new Blob([csv], { type: "text/csv;charset=utf-8" }),
  );
  const a = document.createElement("a");
  a.href = url;
  a.download = "primer-oturumlar.csv";
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  document.querySelector("#toast").textContent =
    `${rows.length} karar dışa aktarıldı.`;
}
reset();
loadModel()
  .then((c) => {
    ready = true;
    modelConfig = c;
    modelStatus = `ONNX hazır · ${c.version} · ${c.data_source === "sentetik" ? "SENTETİK DEMO; nihai model değil" : "gerçek veri modeli"}`;
  })
  .catch((e) => {
    modelStatus = `Kural yedeği etkin · ${e.message}`;
  })
  .finally(() => {
    document.querySelector("[data-cy=status]").textContent = modelStatus;
  });
// Gerçek modelin parite test yüzeyi; sayısal girdi testi, üretim davranışı aynıdır.
window.primer = { predict, ready: () => ready };

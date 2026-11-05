describe("Gerçek tarayıcı ONNX çıkarımı", () => {
  beforeEach(() => {
    cy.visit("/");
    cy.get("[data-cy=status]", { timeout: 30000 }).should(
      "contain",
      "ONNX hazır",
    );
  });
  it("Python oracle ile beş girdide <1e-4 parite", () => {
    cy.readFile("tests/parite.json").then((refs) =>
      cy.window().then(async (w) => {
        const source=await w.fetch(new URL('model/source.json',w.location.href)).then(r=>r.json());
        const modelUrl=source.repo?`https://huggingface.co/${source.repo}/resolve/${source.commit}/model.onnx`:new URL('model/model.onnx',w.location.href);
        const bytes=await w.fetch(modelUrl).then(r=>r.arrayBuffer());
        const hash=Array.from(new Uint8Array(await w.crypto.subtle.digest('SHA-256',bytes))).map(v=>v.toString(16).padStart(2,'0')).join('');
        expect(hash,'Python ve tarayıcı aynı ONNX dosyası').eq(refs.model_sha256);
        const results = [];
        for (const c of refs.cases) {
          const p = await w.primer.predict(c.input);
          expect(Math.abs(p - c.probability)).lessThan(1e-4);
          results.push({input:c.input,python:c.probability,browser:p,absolute_difference:Math.abs(p-c.probability)});
        }
        return results;
      }).then(results=>cy.writeFile('test-results/browser-parity.json',results)),
    );
  });
  it("Aynı sahnede davranış model kararını ve açıklamayı değiştirir", () => {
    cy.get("[name=level]").select("deneyimli");
    cy.get("[data-cy=start]").click();
    cy.get("[data-cy=choice-0]").click();
    cy.get('[name=need][value=1]').check();
    cy.get("[data-cy=submit]").click();
    cy.get("[data-cy=depth]").should("have.text", "Kısa ipucu");
    cy.get("[data-cy=detail]").should("not.exist");
    cy.get("#restart").click();
    cy.get("[data-cy=start]").click();
    for (let i = 0; i < 6; i++) cy.get(`[data-cy=choice-${i % 2}]`).click();
    for (let i = 0; i < 3; i++) cy.get("[data-cy=hint]").click();
    cy.get("[data-cy=choice-0]").click();
    cy.get('[name=need][value=0]').check();
    cy.get("[data-cy=submit]").click();
    cy.get("[data-cy=depth]").should("have.text", "Ayrıntılı açıklama");
    cy.get("[data-cy=detail]").should("be.visible");
    cy.get("[data-cy=help-mode]").should("contain", "ONNX");
  });
  it("Sözleşme sınırı dışındaki girdi reddedilir", () => {
    cy.window().then(async (w) => {
      let rejected = false;
      try {
        await w.primer.predict([3000, 1, 0]);
      } catch {
        rejected = true;
      }
      expect(rejected).eq(true);
    });
  });
});

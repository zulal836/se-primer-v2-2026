// Gerçek tarayıcı kaydı; saat/model/inference taklidi yok. İnsan oturumu sayılmaz.
describe("75 saniye: iki davranış, aynı sahne", () => {
  it("Sentetik ONNX demo kaydı", () => {
    cy.viewport(430, 932);
    cy.visit("/");
    cy.get("[data-cy=status]", { timeout: 30000 }).should(
      "contain",
      "ONNX hazır",
    );
    cy.screenshot("01-giris", { capture: "viewport" });
    cy.wait(6000);
    cy.get("[name=level]").select("deneyimli");
    cy.get("[data-cy=start]").click();
    cy.get("[data-cy=choice-0]").click();
    cy.get("[name=need][value=0]").check();
    cy.get("[data-cy=submit]").click();
    cy.get("[data-cy=depth]").should("have.text", "Kısa ipucu");
    cy.get("[data-cy=p]").scrollIntoView();
    cy.screenshot("02-kisa", { capture: "viewport" });
    cy.wait(11000);
    cy.get("#restart").click();
    cy.get("[name=level]").select("deneyimli");
    cy.get("[data-cy=start]").click();
    for (let i = 0; i < 6; i++) cy.get(`[data-cy=choice-${i % 2}]`).click();
    for (let i = 0; i < 3; i++) cy.get("[data-cy=hint]").click();
    cy.get("[data-cy=choice-0]").click();
    cy.get("[name=need][value=1]").check();
    cy.wait(5000);
    cy.get("[data-cy=submit]").click();
    cy.get("[data-cy=depth]").should("have.text", "Ayrıntılı açıklama");
    cy.get("[data-cy=depth]").scrollIntoView();
    cy.screenshot("03-ayrintili", { capture: "viewport" });
    cy.wait(11000);
    cy.get("[data-cy=next]").click();
    cy.wait(4000);
    cy.get("[data-cy=choice-0]").click();
    cy.get("[data-cy=submit]").click();
    cy.wait(4000);
    cy.get("[data-cy=next]").click();
    cy.wait(4000);
    cy.get("[data-cy=choice-0]").click();
    cy.get("[data-cy=submit]").click();
    cy.wait(4000);
    cy.get("[data-cy=next]").click();
    cy.get("[data-cy=ending]").should("have.text", "Kontrollü toparlanma");
    cy.wait(5000);
    cy.get("#restart").click();
    cy.get("[name=mode]").select("rule");
    cy.get("[name=consent]").scrollIntoView();
    cy.wait(8000);
    cy.get("#export").scrollIntoView();
    cy.wait(5000);
  });
});

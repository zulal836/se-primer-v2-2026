const start = (consent = false) => {
  cy.visit("/");
  if (consent) cy.get("[name=consent]").check();
  cy.get("[name=mode]").select("rule");
  cy.get("[data-cy=start]").click();
};
describe("Temel oyun regresyonu", () => {
  it('Rol ve hedef anlatımın odağını değiştirir',()=>{
    cy.visit('/');cy.get('[name=role]').select('Test mühendisi');
    cy.get('[name=goal]').select('Veri gizliliği');cy.get('[data-cy=start]').click();
    cy.get('[data-cy=profile-focus]').should('contain','gözlemlenebilir test').and('contain','gereksiz kişisel veri');
  });
  for (let path = 0; path < 8; path++) {
    it(`Üç karar yolu ${path.toString(2).padStart(3, "0")}`, () => {
      start(true);
      for (let scene = 0; scene < 3; scene++) {
        cy.get(`[data-cy=choice-${(path >> scene) & 1}]`).click();
        cy.get("[name=need][value=1]").check();
        cy.get("[data-cy=submit]").click();
        cy.get("[data-cy=consequence]").should("be.visible");
        cy.get("[data-cy=next]").click();
      }
      cy.get("[data-cy=ending]").should(
        "have.text",
        path === 0 ? "Kontrollü toparlanma" : "Olay incelemesi",
      );
      cy.window().then((w) => {
        const rows = JSON.parse(w.localStorage.getItem("primer-rows"));
        expect(rows).to.have.length(3);
        expect(new Set(rows.map((r) => r.oturum_id)).size).eq(1);
        expect(
          rows.every((r) => r.kaynak === "gerçek" && r.tamamlandi === 1),
        ).eq(true);
      });
      cy.get("#export").click();
      cy.readFile("cypress/downloads/primer-oturumlar.csv").should(
        "contain",
        "ayrinti_istegi",
      );
      cy.get("[data-cy=again]").click();
      cy.get("[data-cy=start]").should("be.visible");
    });
  }
  it("Katılım yokken kayıt yok; profil anlatımı ve ipucu", () => {
    start();
    cy.contains("Geliştirici · Güvenli sürüm");
    cy.get("[data-cy=hint]").click();
    cy.get("#hint-text").should("contain", "veritabanındaki");
    cy.get("[data-cy=choice-0]").click();
    cy.get("[data-cy=submit]").click();
    cy.window().then((w) =>
      expect(w.localStorage.getItem("primer-rows")).eq(null),
    );
  });
  it("Yeni oturum kimliği yenilenir; veri temizlenebilir", () => {
    start(true);
    cy.get("[data-cy=choice-0]").click();
    cy.get("[data-cy=submit]").click();
    cy.window().then((w) => {
      const first = JSON.parse(w.localStorage.getItem("primer-rows"))[0]
        .oturum_id;
      cy.get("#restart").click();
      cy.get("[name=consent]").check();
      cy.get("[data-cy=start]").click();
      cy.get("[data-cy=choice-1]").click();
      cy.get("[data-cy=submit]").click();
      cy.window().then((w2) =>
        expect(
          JSON.parse(w2.localStorage.getItem("primer-rows"))[1].oturum_id,
        ).not.eq(first),
      );
    });
    cy.on("window:confirm", () => true);
    cy.get("#clear").click();
    cy.window().then((w) =>
      expect(JSON.parse(w.localStorage.getItem("primer-rows"))).deep.eq([]),
    );
  });
  it("Model erişilemediğinde görünür kural yedeği", () => {
    cy.intercept("**/model/source.json", { statusCode: 404 });
    cy.visit("/");
    cy.get("[data-cy=status]").should("contain", "Kural yedeği etkin");
    cy.get("[data-cy=start]").click();
    cy.get("[data-cy=choice-0]").click();
    cy.get("[data-cy=submit]").click();
    cy.get("[data-cy=help-mode]").should("contain", "Kural yedeği");
  });
});

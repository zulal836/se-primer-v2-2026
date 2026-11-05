describe('Giriş yapılmadan canlı yayın',()=>{
 it('Modeli yükler, gerçek çıkarım yapar ve oyunu bitirir',()=>{
  cy.visit(Cypress.config('baseUrl'));
  cy.get('[data-cy=status]',{timeout:180000}).should(el=>{
    expect(el.text(),'Canlı model yükleme durumu').contain('ONNX hazır');
    expect(el.text()).contain('SENTETİK DEMO');
  });
  cy.readFile('tests/parite.json').then(refs=>cy.window().then(async w=>{
    for(const c of refs.cases)expect(Math.abs(await w.primer.predict(c.input)-c.probability)).lessThan(1e-4);
  }));
  cy.get('[data-cy=start]').click();
  for(let i=0;i<3;i++){
    cy.get('[data-cy=choice-0]').click();cy.get('[data-cy=submit]').click();
    cy.get('[data-cy=help-mode]').should('contain','ONNX');cy.get('[data-cy=next]').click();
  }
  cy.get('[data-cy=ending]').should('have.text','Kontrollü toparlanma');
 });
 it('Video herkese açık MP4 olarak sunulur',()=>{
  cy.request({url:new URL('demo.mp4',Cypress.config('baseUrl')).href,method:'HEAD'}).then(r=>{
    expect(r.status).eq(200);expect(r.headers['content-type']).contain('video/mp4');
  });
 });
});

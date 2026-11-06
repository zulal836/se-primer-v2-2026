describe('Giriş yapılmadan canlı yayın',()=>{
 it('Modeli yükler, gerçek çıkarım yapar ve oyunu bitirir',()=>{
  cy.visit(Cypress.config('baseUrl'));
  cy.get('[data-cy=status]',{timeout:180000}).should(el=>{
    expect(el.text(),'Canlı model yükleme durumu').contain('ONNX hazır');
    expect(el.text()).contain('SENTETİK DEMO');
  });
  cy.readFile('release-demo.json').then(release=>cy.window().then(async w=>{
    const source=await w.fetch(new URL('model/source.json',w.location.href),{cache:'no-store'}).then(r=>r.json());
    expect(source.repo).eq(release.repo);
    expect(source.commit).eq(release.commit);
    expect(source.mode).eq('hf-pinned-synthetic-demo');
    const root=`https://huggingface.co/${source.repo}/resolve/${source.commit}/`;
    const config=await w.fetch(root+'config.json').then(r=>r.json());
    expect(config.data_source).eq('sentetik');expect(config.publishable).eq(false);
    const bytes=await w.fetch(root+'model.onnx').then(r=>r.arrayBuffer());
    const sha=Array.from(new Uint8Array(await w.crypto.subtle.digest('SHA-256',bytes))).map(n=>n.toString(16).padStart(2,'0')).join('');
    expect(sha).eq(release.files_sha256['model.onnx']);
  }));
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

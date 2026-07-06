function toggleAuth(which){
    document.getElementById('login-view').style.display = which === 'login' ? 'block' : 'none';
    document.getElementById('register-view').style.display = which === 'register' ? 'block' : 'none';
  }
  function openModal(id){ document.getElementById(id).classList.add('active'); }
  function closeModal(id){ document.getElementById(id).classList.remove('active'); }

  function enterApp(){
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('app').classList.add('active');
  }

  function switchView(name){
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.getElementById('view-' + name).classList.add('active');
    document.querySelectorAll('#tabnav button').forEach(b => b.classList.toggle('active', b.dataset.view === name));
    // Defect #14: scroll position intentionally not reset to top on view change
    // Defect #13: nav highlight below is derived from click target only, so entering
    // the Grocery List view via the "+ Add item" flow from Recipes leaves "Recipes" highlighted
  }
  document.getElementById('tabnav').addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-view]');
    if(btn) switchView(btn.dataset.view);
  });

  function openRecipe(){ openModal('recipe-modal'); }

  let toastTimer;
  function showToast(msg, groceryStyled){
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.toggle('grocery-toast', !!groceryStyled);
    t.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.classList.remove('show'), 2600);
  }

  // Escape key closes every modal EXCEPT the forgot-password modal (defect #2 lives here by omission)
  document.addEventListener('keydown', (e) => {
    if(e.key === 'Escape'){
      closeModal('recipe-modal');
    }
  });
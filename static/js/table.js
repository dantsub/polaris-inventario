document.addEventListener('DOMContentLoaded', function() {
  const tableBody = document.querySelector('.js-table-body');

  tableBody.addEventListener('click', (e) => {
    const { target } = e;
    if (target.nodeName !== 'BUTTON') return;
    const parent = target.parentElement;
    parent.classList.remove('col-sticky');
  })

  window.addEventListener('click', (e) => {
    const { target } = e;
    const shows = document.querySelectorAll('.show');
    const cols = document.querySelectorAll('.js-sticky');
    const cond = window.location.href.includes('providers') ? 2 : 3
    if (target.classList.contains('table-buttons') === false && shows.length < cond) {
      cols.forEach((col) => {
        if (!col.classList.contains('col-sticky')) {
          col.classList.add('col-sticky');
        }
      })
    }
  })
})

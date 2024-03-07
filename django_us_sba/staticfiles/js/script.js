'use strict'

const hamburger = document.querySelector("#hamburger");
const menu = document.querySelector('#menu');

hamburger.addEventListener('click', function () {
    menu.classList.toggle('hidden')
})

function confirmDeletion() {
    if (confirm("Are you sure you want to delete this item?")) {
        main_form.submit();
    }
}

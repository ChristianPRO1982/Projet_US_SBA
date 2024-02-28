'use strict'

const hamburger = document.querySelector("#hamburger");
const menu = document.querySelector('#menu');

hamburger.addEventListener('click', function () {
    menu.classList.toggle('hidden')
})

document.addEventListener("DOMContentLoaded", function() {
    var overlay = document.getElementById("overlay");
    setTimeout(function() {
        overlay.classList.add('hidden'); // Ajoute la classe 'hidden' après une seconde
    }, 1000);
});
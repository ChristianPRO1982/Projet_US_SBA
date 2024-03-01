'use strict'

const hamburger = document.querySelector("#hamburger");
const menu = document.querySelector('#menu');

hamburger.addEventListener('click', function () {
    menu.classList.toggle('hidden')
})

document.addEventListener('DOMContentLoaded', function () {
    const mainImage = document.getElementById('main-image');
    const imageContainer = document.getElementById('image-container');

    // Définir une classe pour l'effet de rétrécissement
    mainImage.classList.add('transition-all', 'duration-1000');

    // Appliquer une classe supplémentaire pour déclencher l'animation
    setTimeout(function () {
        mainImage.classList.add('scale-0', 'opacity-0'); // Modifier la valeur de l'échelle selon vos besoins
    }, 750); // Définir le délai avant le début de l'animation (en millisecondes)
    setTimeout(function () {
        imageContainer.classList.add('hidden'); // Masquer la div image-container
    }, 2000); // Définir le délai avant le début de l'animation (en millisecondes)
});

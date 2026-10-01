(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        const burger = document.querySelector('.header__burger');
        const nav = document.getElementById('headerNav');

        if (!burger || !nav) return;

        burger.addEventListener('click', function () {
            const isOpen = nav.classList.toggle('header__nav--open');
            burger.classList.toggle('header__burger--open', isOpen);
            burger.setAttribute('aria-expanded', String(isOpen));
        });

        nav.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                nav.classList.remove('header__nav--open');
                burger.classList.remove('header__burger--open');
                burger.setAttribute('aria-expanded', 'false');
            });
        });

        document.addEventListener('click', function (e) {
            if (!nav.contains(e.target) && !burger.contains(e.target)) {
                nav.classList.remove('header__nav--open');
                burger.classList.remove('header__burger--open');
                burger.setAttribute('aria-expanded', 'false');
            }
        });
    });
})();
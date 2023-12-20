// JavaScript *

var openMenu = document.getElementById('openMenu');
var closeMenu = document.getElementById('closeMenu');
var menu = document.getElementById('menu');

openMenu.addEventListener('click', () => {
    openMenu.style.display = 'none'
    menu.style.display = 'flex';
    menu.style.right = (menu.offsetWidth * -1) + 'px';
    setTimeout(() => {
        menu.style.opacity = '1';
        menu.style.right = '0';
    }, 80);
    
});
closeMenu.addEventListener('click', () => {
    menu.style.opacity = '0';
    menu.style.right = (menu.offsetWidth * -1) + 'px';
    setTimeout(() => {
        menu.removeAttribute('style');
    }, 500);
    openMenu.removeAttribute('style')
    
});

const limpar = document.getElementById('limpar');
limpar.addEventListener('click', () => {
    document.getElementById('topico').value = "";
    document.getElementById('date_and_time').value = "";
    document.getElementById('title1').value = "";
    document.getElementById('conteudo1').value = "";
    document.getElementById('title2').value = "";
    document.getElementById('conteudo2').value = "";
    document.getElementById('title3').value = "";
    document.getElementById('conteudo3').value = "";
    document.getElementById('primeira_imagem').value = "";
    document.getElementById('segunda_imagem').value = "";
    document.getElementById('terceira_imagem').value = "";
})

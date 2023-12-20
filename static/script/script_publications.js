const limpar_ = document.getElementById('limpar_');
limpar_.addEventListener('click', () => {
    document.getElementById('data_de_entrega').value = "";
    document.getElementById('title1').value = "";
    document.getElementById('conteudo1').value = "";
    document.getElementById('name').value = "";
    const input_radius = document.getElementsByName('genero');
    input_radius.forEach(function(genero) {
        genero.checked = false;
    })
    document.getElementById('idade').value = "";
    document.getElementById('email').value = "";
    document.getElementById('telefone').value = "";
    document.getElementById('contry').value = "";
})

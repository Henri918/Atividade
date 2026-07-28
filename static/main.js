console.log("MAIN.JS CARREGOU")

function editarProduto(id){

console.log("EDITAR", id)

Swal.fire({
title:'Editar Quantidade',
input:'number',
showCancelButton:true

}).then((result)=>{

if(result.isConfirmed){

window.location.href =
`/editarquantidade/${id}/${result.value}`

}

})

}

function deletarProduto(id){

console.log("DELETAR", id)

window.location.href =
`/deletar/${id}`


}

function verImagem(foto2) {

    console.log(foto2.length);
    console.log(foto2.substring(0, 50));

    Swal.fire({
        html: `<img src="${foto2}" style="max-width:100%">`
    });

}

function mostrarFormulario(){
                
                document.getElementById(
                "formulario"
                ).style.display="block"
                
                }
                
                function editarProduto(id){
                
                Swal.fire({
                
                title:'Nova Quantidade',
                
                input:'number',
                
                showCancelButton:true,
                
                confirmButtonText:'Salvar'
                
                }).then((result)=>{
                
                if(result.isConfirmed){
                
                window.location.href=
                `/editarquantidade/${id}/${result.value}`
                
                }
                
                })
                
                }
                
                function deletarProduto(id){
                
                Swal.fire({
                
                title:'Excluir item?',
                
                icon:'warning',
                
                showCancelButton:true,
                
                confirmButtonText:'Excluir'
                
                }).then((result)=>{
                
                if(result.isConfirmed){
                
                window.location.href=
                `/deletar/${id}`
                
                }
                
                })
                
                }
                
function abrirPopup(id,nome){

Swal.fire({

title:nome,

html:`
<input
id="quantidade"
type="number"
class="swal2-input"
placeholder="Quantidade">
`,

showCancelButton:true,

confirmButtonText:'Retirar'

}).then((result)=>{

if(result.isConfirmed){

let qtd=document.getElementById("quantidade").value;

window.location.href=`/retirar/${id}/${qtd}`;

}

});

}

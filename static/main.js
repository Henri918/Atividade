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
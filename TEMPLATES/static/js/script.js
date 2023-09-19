document.addEventListener("DOMContentLoaded", function () {
    // Obtém o conteúdo original do textarea
    const originalContent = document.getElementById("chordsTextarea").value;
    
    // Obtém o textarea
    const textarea = document.getElementById("chordsTextarea");

    // Adiciona um evento de input ao textarea para verificar alterações
    textarea.addEventListener("input", function () {
        // Obtém o novo conteúdo do textarea
        const newContent = textarea.value;
        
        // Encontra as diferenças entre o conteúdo original e o novo conteúdo
        let differences = "";

        for (let i = 0; i < newContent.length; i++) {
            if (newContent[i] !== originalContent[i]) {
                differences += `<span class="added-letter">${newContent[i]}</span>`;
            } else {
                differences += newContent[i];
            }
        }
        
        // Define o conteúdo do textarea com as letras destacadas
        textarea.innerHTML = differences;
    });
});


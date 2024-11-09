window.addEventListener('load', () => {
    const $dismissButtons = document.querySelectorAll('[data-dismiss="alert"');

    [...$dismissButtons].forEach(button => {
        button.addEventListener('click', () => {
            const $alert = button.closest('[role="alert"]')

            $alert.classList.add('hide')
        })
    })    
})
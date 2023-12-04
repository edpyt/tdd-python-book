var initialize = () => {
    errElement = document.getElementsByClassName('has-error')[0];
    inputEl = document.getElementsByName('text')[0];

    inputEl.addEventListener('keypress', (event) => {
    
        errElement.hidden = true;
    })
}
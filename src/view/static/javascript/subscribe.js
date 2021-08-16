function animateSubscribe() {
    gsap.to(
        document.querySelector('main h1'),
        {
            x: 0,
            duration: 2,
            opacity: 1,
            ease: 'power4'
        }
    )

    gsap.to(
        document.querySelector('.subscribe-container'),
        {
            x: 0,
            opacity: 1,
            ease: 'power4',
            duration: 2
        }
    )
}

function animateClouds(){
    let clouds = document.querySelectorAll('.cloud');
    clouds.forEach( (cloud, index) => {
        gsap.from( cloud, {
            y: 400,
            opacity: 0.5,
            duration: 0.5 * index + 1
        });
    });
}

function subscribeUser() {
    let form = document.querySelector('.subscribe-form')
    form.addEventListener('submit', (event) => {
        event.preventDefault(); //prevents autosubmiting

        let name = document.querySelector('#name');
        let lastName = document.querySelector('#last-name');
        let email = document.querySelector('#email');
        let city = document.querySelector('#city');

        addUser(name.value, lastName.value, email.value, city.value)
        .then( (code) => {
            let responseCode = code;

            let successPopup = document.querySelector('.user-okey');
            let deniedPopup = document.querySelector('.user-exists');
            let errorPopup = document.querySelector('.error');

            switch(responseCode){
                case -1: 
                    showPopup(deniedPopup);
                    break;
                case 1:                    
                    showPopup(successPopup);
                    form.reset();
                    break;
                case -2: 
                    showPopup(errorPopup);
                    break;
            }
        });
    })
}

function popupWindowConfig() {
    let popups = document.querySelectorAll('.popup')
    popups.forEach((popup) => {
        let closeButton = popup.querySelector('.close-popup')
        closeButton.addEventListener('click', () => {
            closePopup(popup);
        });

        window.addEventListener('click', (event) => {
            if(event.target != popup) {
                closePopup(popup);
            }
        })
    })
}

animateClouds();
animateSubscribe();
subscribeUser();
popupWindowConfig();
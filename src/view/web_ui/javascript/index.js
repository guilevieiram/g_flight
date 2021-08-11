function gotoSubscribe () {
    const scrollableContainer = document.querySelector('.pages-container');
    const subscribePage = document.querySelector('.page-3');
    const height = subscribePage.getBoundingClientRect().top;
    scrollableContainer.scrollTo({ top: height, behavior: 'smooth'});
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

function animatePages () {
    // landing page clouds
    let clouds = document.querySelectorAll('.cloud');
    clouds.forEach( (cloud, index) => {
        gsap.from( cloud, {
            y: 200,
            opacity: 0.5,
            duration: 0.5 * index + 1
        });
    });

    // landing page plane
    let plane = document.querySelector('.plane')
    gsap.from( plane, {
        y: 500,
        x:-400,
        ease: 'power2',
        duration: 5
    });

    // landing page text
    gsap.from(document.querySelector('.page-1 h1'), {
        x: 400, 
        opacity:0, 
        duration: 2,
        ease: 'power2'
    });
    gsap.from(document.querySelector('.page-1 h2'), {
        x: 200, 
        opacity:0, 
        duration: 1.5,
        ease: 'power2'
    });
    gsap.from(document.querySelector('.page-1 button'), {
        opacity:0, 
        duration: 1,
        ease: 'power2'
    });

    // second page clouds
    let cloudsUpsidedown = document.querySelectorAll('.cloud-upsidedown');
    cloudsUpsidedown.forEach( (cloud, index) => {
        loadOnReach( cloud, 
            animation = gsap.from,
            parameters = {
            y: -200,
            duration: 0.5 * index + 3,
            ease: 'power2'
            }
        );
    });

    // rain 
    let rain1 = document.querySelector('.page-2 .background .rain');
    loadOnReach(rain1, 
        animation = gsap.from,
        parameters = {
        y: -300,
        duration: 10,
        ease: 'power1'
        }
    );
    let rain2 = document.querySelector('.page-3 .background .rain');
    loadOnReach(rain2, 
        animation = gsap.from,
        parameters = {
        y: -300,
        duration: 10,
        ease: 'power1'
        }
    );

    // text clouds
    let textClouds = document.querySelectorAll('.text-cloud');
    textClouds.forEach( (cloud, index) => {
        loadOnReach(cloud ,
            animation = gsap.to,
            parameters = {
            x: 0,
            opacity: 1,
            duration: 0.5 * index + 2
            }
        );
    });
    
    //page 2 main text
    loadOnReach( document.querySelector('.page-2 h1'), 
        animation = gsap.to,
        parameters = {
        x: 0, 
        opacity: 1, 
        duration: 4, 
        ease: 'power2'
        }
    );
    
    // page 3 
    loadOnReach( document.querySelector('.page-3 h1'), 
        animation = gsap.to,
        parameters = {
        x: 0, 
        opacity: 1, 
        duration: 3, 
        ease: 'power4'
        }
    );
    loadOnReach( document.querySelector('.subscribe-container'), 
        animation = gsap.to,
        parameters = {
        x: 0, 
        opacity: 1, 
        duration: 3, 
        ease: 'power4'
        }
    );
}


animatePages();
popupWindowConfig();
subscribeUser();

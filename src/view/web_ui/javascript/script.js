function gotoTop () {
    const scrollableContainer = document.querySelector('.pages-container');
    const subscribePage = document.querySelector('main');
    const height = subscribePage.getBoundingClientRect().top;
    scrollableContainer.scrollTo({ top: height, behavior: 'smooth'});
}

function loadOnReach (element, animation, parameters) {
    const scrollableContainer = document.querySelector('.pages-container');
    var elementNotCalled = true;
    scrollableContainer.addEventListener('scroll', () => {
        if (scrollableContainer.scrollTop > element.getBoundingClientRect().top && elementNotCalled){
            elementNotCalled = false;
            animation(element, parameters);
        };
      });
}

function showPopup(element) {
    gsap.to(element, {
        display: 'block',
        opacity: 1,
        ease: 'power1',
        duration: 0.3
    })
}
function closePopup(element) {
    gsap.to(element, {
        display: 'none',
        opacity: 0,
        ease: 'power1',
        duration: 0.3
    })
}


function navSlider () {
    const burguer = document.querySelector('.hamburguer');
    const nav = document.querySelector('.nav-links');
    const navLinks = document.querySelectorAll('.nav-link');
    let open = false;

    let toggleNavBar = () => {
        nav.classList.toggle('nav-active');
        navLinks.forEach( (link, index) => {
            if (open) {
                gsap.to(link, {
                    opacity: 0,
                    x: 100,
                    duration: 0.3* index + 1,
                    ease: 'power2'
                });
            }else {
                gsap.to(link, {
                    opacity: 1,
                    x: 0,
                    duration: 0.3* index + 1,
                    ease: 'power2'
                });
            };

        });
        open = !open;
    };
    
    burguer.addEventListener('click', () => {
        toggleNavBar();
    });

    navLinks.forEach((navLink) => {
        navLink.addEventListener('click', () =>{
            if(window.getComputedStyle(burguer, null).display != 'none'){
                toggleNavBar();
            }
        })
    });
}

function animateNav() {
        // navbar
        gsap.to( document.querySelector('nav'), {
            y: 0, 
            opacity: 1,
            duration: 1
        });
};

navSlider();
animateNav();

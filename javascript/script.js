function navSlider () {
    const burguer = document.querySelector('.hamburguer');
    const nav = document.querySelector('.nav-links');
    const navLinks = document.querySelectorAll('.nav-links li');
    let open = false;

    burguer.addEventListener('click', () => {
        console.log('burger clicked');
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
    });
}

function loadOnReach (element, from) {
    let scrollableContainer = document.querySelector('.pages-container');
    var elementNotCalled = true;
    scrollableContainer.addEventListener('scroll', () => {
        if (scrollableContainer.scrollTop > element.getBoundingClientRect().top && elementNotCalled){
            elementNotCalled = false;
            gsap.from(element, from);
        };
      });
}

function animatePages () {
    // navbar
    gsap.from( document.querySelector('nav'), {
        y: '-100%', 
        duration: 1
    });

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
        loadOnReach( cloud, {
            y: -200,
            duration: 0.5 * index + 3,
            ease: 'power2'
        });
    });

    // rain 
    let rain1 = document.querySelector('.page-2 .background .rain');
    loadOnReach(rain1, {
        y: -300,
        duration: 5,
        ease: 'power1'
    });
    let rain2 = document.querySelector('.page-3 .background .rain');
    loadOnReach(rain2, {
        y: -300,
        duration: 5,
        ease: 'power1'
    });

    // text clouds
    let textClouds = document.querySelectorAll('.text-cloud');
    textClouds.forEach( (cloud, index) => {
        loadOnReach(cloud ,{
            x: 100*index + 100,
            opacity: 0,
            duration: 0.5 * index + 2
        });
    });
    
    //page 2 main text
    loadOnReach( document.querySelector('.page-2 h1'), {
        x: 200, 
        opacity: 0, 
        duration: 4, 
        ease: 'power2'
    });

    // page 3 
    loadOnReach( document.querySelector('.page-3 h1'), {
        x: -200, 
        opacity: 0, 
        duration: 3, 
        ease: 'power2'
    });
    loadOnReach( document.querySelector('.subscribe-form'), {
        x: 200, 
        opacity: 0, 
        duration: 3, 
        ease: 'power2'
    });
}

function init () {
    navSlider();
    animatePages();
}
init();
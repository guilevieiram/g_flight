function animateAboutParagraph() {
    const paragraphs = document.querySelectorAll('.about-paragraph');

    // animate the first
    gsap.to(paragraphs[0], {
        y:0,
        opacity: 1
    });

    paragraphs.forEach((paragraph) => {
        loadOnReach(
            element = paragraph,
            animation = gsap.to,
            parameters = {
                y: 0,
                opacity: 1,
                duration: 3,
                ease: 'power2'
            }
        );
    });
}

animateAboutParagraph();
let clouds = document.querySelectorAll('.cloud');
clouds.forEach( (cloud, index) => {
    gsap.from( cloud, {
        y: 200,
        opacity: 0.5,
        duration: 0.5 * index + 1
    });
});
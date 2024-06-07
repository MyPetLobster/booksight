// Layout scripts -- NavLogo and Footer
const logoLink = document.getElementById('logo-link');
const footer = document.getElementById('footer');
const pageIdentifier = document.querySelector('.page-identifier').textContent;
const toPageNavItem = document.getElementById('to-page-nav-item');
const owlLogoNavItem = document.getElementById('owl-logo-nav-item');

// If user is not at the top of the page, hide the nav logo/link
document.addEventListener('scroll', () => {
    if (window.scrollY > 0) {
        owlLogoNavItem.style.transition = '1s';
        owlLogoNavItem.style.opacity = 0;
    } else {
        owlLogoNavItem.style.transition = '2s';
        owlLogoNavItem.style.opacity = 1;
    }
});

if (pageIdentifier === 'index') {
    logoLink.href = "{% url 'about' %}";
    toPageNavItem.innerHTML = 'About';
    footer.style.display = 'block';
} else if (pageIdentifier === 'about' || pageIdentifier === 'tips' || pageIdentifier === 'vision-complete') {
    logoLink.href = "{% url 'index' %}";
    toPageNavItem.innerHTML = 'Home';
    footer.style.display = 'block';
} else if (pageIdentifier === 'vision') {
    logoLink.style.display = 'none';
    footer.style.display = 'none';
} 

// Darken the owl logo nav link on hover
const darkOwlLogo = document.getElementById('owl-logo-img');
owlLogoNavItem.addEventListener('mouseover', () => {
    if (screen.width > 600) {
        darkOwlLogo.style.opacity = 1;
        toPageNavItem.style.opacity = 1;
    }
});
owlLogoNavItem.addEventListener('mouseout', () => {
    darkOwlLogo.style.opacity = 0.15;
    toPageNavItem.style.opacity = 0;
});

// Hide footer link if not scrolled to bottom of the page
window.onscroll = function(ev) {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
        footer.style.display = 'block';
    } else {
        footer.style.display = 'none';
    }
};


// Small logo animation (Tips, About pages)
const pageIdentifierText = document.querySelector(".page-identifier").textContent;

if (pageIdentifierText === "tips" || pageIdentifierText === "about") {
    const logoEyes = document.querySelector("#logo-eyes-vision");
    const logoText = document.querySelector("#logo-text-vision");
    const smallLogoElements = [logoEyes, logoText];
    smallLogoElements.forEach((element) => {
        element.style.cursor = "pointer";  
        element.addEventListener("mouseover", () => {
            logoEyes.style.transition = "3s";
            logoEyes.style.transform = "scale(1.7)";
            logoEyes.style.position = "relative";

            logoText.style.transition = "3s";
            logoText.style.transform = "scale(0.1)";
            logoText.style.opacity = 0;
        })
        element.addEventListener("mouseout", () => {
            logoEyes.style.transition = "0.8s";
            logoText.style.transition = "0.8s";
            logoEyes.style.transform = "scale(1)";
            logoText.style.transform = "scale(1)";
            logoText.style.opacity = 1;
        });
        element.addEventListener("click", () => {
            window.location.href = "/";
        });
    });
}
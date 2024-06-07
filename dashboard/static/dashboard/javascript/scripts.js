/// LAYOUT -- NavLogo and Footer

// Alert message auto-hide
const alertDiv = document.querySelector('.alert');
if (alertDiv) {
    setTimeout(() => {
        alertDiv.style.display = 'none';
    }, 5000);
}

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




/// TIPS/ABOUT - Small logo interactivity
const animatedPages = ["tips", "about", "vision-complete", "vision-failed"];

if (animatedPages.includes(pageIdentifier)) {
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




/// INDEX PAGE SCRIPTS

if (pageIdentifier === 'index') {
    // Checkboxes for export formats - index form
    const selectAll = document.getElementById('all');
    const csv = document.getElementById('csv');
    const json = document.getElementById('json');
    const xml = document.getElementById('xml');
    const txt = document.getElementById('txt');

    selectAll.addEventListener('change', () => {
        if (selectAll.checked) {
            csv.checked = true;
            json.checked = true;
            xml.checked = true;
            txt.checked = true;
        } else {
            csv.checked = false;
            json.checked = false;
            xml.checked = false;
            txt.checked = false;
        }
    })

    options = [csv, json, xml, txt];

    for (let option of options) {
        option.addEventListener('change', () => {
            if (csv.checked && json.checked && xml.checked && txt.checked) {
                selectAll.checked = true;
            } else {
                selectAll.checked = false;
            }
        })
    }


    // Index Form and Landing Logo Interplay, Form Handling
    const logoEyes = document.getElementById('logo-eyes');
    const logoText = document.getElementById('logo-text');
    const hiddenSubtitle = document.querySelector('.hidden-subtitle');
    const floatingForm = document.querySelector('.upload-form-div');
    const landingLogoDiv = document.querySelector('.landing-logo-div');
    const cancelBtn = document.querySelector('.btn-box button');
    const advOptionsButton = document.getElementById('adv-options-button');
    const advOptionsDiv = document.getElementById('adv-options-div');
    const advOptionsClose = document.getElementById('adv-options-close');
    const screenWidth = window.innerWidth;

    if (screenWidth > 600) {
        // Desktop behavior
        [logoEyes, logoText].forEach((element) => {
            element.addEventListener('mouseover', () => {
                logoText.style.maxWidth = "110%";
                logoText.style.opacity = 1;
                logoEyes.style.maxWidth = "70%";
                logoEyes.style.opacity = 1;
                hiddenSubtitle.style.opacity = 1;
                hiddenSubtitle.style.transition = "10s";
            })
            element.addEventListener('mouseout', () => {
                logoText.style.maxWidth = "100%";
                logoText.style.opacity = 0.15;
                logoEyes.style.maxWidth = "60%";
                logoEyes.style.opacity = 0.15;
                hiddenSubtitle.style.opacity = 0;
                hiddenSubtitle.style.transition = "2s";
            })
        })
        landingLogoDiv.addEventListener('click', () => {
            floatingForm.style.opacity = 1;
            floatingForm.style.zIndex = 999;
            landingLogoDiv.style.opacity = 0;
        })
    } else {
        // Mobile behavior
        landingLogoDiv.addEventListener('click', () => {
            logoEyes.style.transition = "2s";
            logoEyes.style.opacity = 1;
            logoText.style.transition = "2s";
            logoText.style.opacity = 1;
            hiddenSubtitle.style.transition = "2s";
            hiddenSubtitle.style.opacity = 1;

            const footer = document.getElementById('footer');
            footer.style.opacity = 0;

            const owlLogoNavItem = document.getElementById('owl-logo-nav-item');
            if (owlLogoNavItem) {
                owlLogoNavItem.style.transition = "2s";
                owlLogoNavItem.style.opacity = 0;
                owlLogoNavItem.style.zIndex = -1;
            }

            setTimeout(() => {
                logoEyes.style.transition = "2s";
                logoEyes.style.opacity = 0.15;
                logoText.style.transition = "2s";
                logoText.style.opacity = 0.15;
                hiddenSubtitle.style.transition = "2s";
                hiddenSubtitle.style.opacity = 0;
                floatingForm.style.opacity = 1;
                floatingForm.style.zIndex = 999;
                landingLogoDiv.style.opacity = 0;
            }, 2000)
        })
    }

    cancelBtn.addEventListener('click', () => {
        floatingForm.style.opacity = 0;
        floatingForm.style.zIndex = -1;
        landingLogoDiv.style.transition = "2s";
        landingLogoDiv.style.opacity = 1;
        logoEyes.style.transition = "2s";
        logoEyes.style.opacity = 0.15;
        logoText.style.transition = "2s";
        logoText.style.opacity = 0.15;

        window.scrollTo(0, 0);

        const footer = document.getElementById('footer');
        footer.style.opacity = 1;
        const owlLogoNavItem = document.getElementById('owl-logo-nav-item');
        if (owlLogoNavItem) {
            owlLogoNavItem.style.transition = "2s";
            owlLogoNavItem.style.opacity = 1;
            owlLogoNavItem.style.zIndex = 1;
        }
    })
    advOptionsButton.addEventListener('click', () => {
        advOptionsDiv.style.display = 'flex';
        advOptionsClose.style.display = 'block';
        advOptionsButton.style.display = 'none';
        window.scrollTo(0, document.body.scrollHeight);
    })
    advOptionsClose.addEventListener('click', () => {
        advOptionsDiv.style.display = 'none';
        advOptionsClose.style.display = 'none';
        advOptionsButton.style.display = 'block';
        window.scrollTo(0, 0);
    })     
}
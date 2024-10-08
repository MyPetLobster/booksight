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
        owlLogoNavItem.style.transition = '0.5s';
        owlLogoNavItem.style.opacity = 0;
    } else {
        owlLogoNavItem.style.transition = '2s';
        owlLogoNavItem.style.opacity = 1;
    }
});

if (pageIdentifier === 'index') {
    logoLink.href = "/about";
    toPageNavItem.innerHTML = 'About';
    footer.style.display = 'block';
} else if (pageIdentifier === 'about' || pageIdentifier === 'tips' || pageIdentifier === 'vision-complete') {
    logoLink.href = "/";
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
        if (window.scrollY === 0){
            toPageNavItem.style.opacity = 1;
        }
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


// TIPS/ABOUT - Small logo interactivity
const animatedPages = ["tips", "about", "vision-complete", "vision-failed"];

if (animatedPages.includes(pageIdentifier)) {
    const logoEyes = document.querySelector("#logo-eyes-vision");
    const logoText = document.querySelector("#logo-text-vision");
    const smallLogoElements = [logoEyes, logoText];

    // If screen width is greater than 600px 
    if (screen.width > 600) {
        smallLogoElements.forEach((element) => {
            element.style.cursor = "pointer";  
            element.addEventListener("mouseover", () => {
                logoEyes.style.transition = "3s";
                logoEyes.style.transform = "scale(1.7)";

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
    } else {
        smallLogoElements.forEach((element) => {
            element.style.cursor = "pointer";  
            element.addEventListener("click", () => {
                logoEyes.style.transition = "1.5s";
                logoEyes.style.transform = "scale(1.7)";

                logoText.style.transition = "1.5s";
                logoText.style.transform = "scale(0.1)";
                logoText.style.opacity = 0;

                setTimeout(() => {
                    window.location.href = "/";
                }, 1500);
            });
        });
    }
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
            logoEyes.style.transition = "1.5s";
            logoEyes.style.opacity = 1;
            logoText.style.transition = "1.5s";
            logoText.style.opacity = 1;
            hiddenSubtitle.style.transition = "1.5s";
            hiddenSubtitle.style.opacity = 1;

            const footer = document.getElementById('footer');
            footer.style.opacity = 0;

            const owlLogoNavItem = document.getElementById('owl-logo-nav-item');
            if (owlLogoNavItem) {
                owlLogoNavItem.style.transition = "1.5s";
                owlLogoNavItem.style.opacity = 0;
                owlLogoNavItem.style.zIndex = -1;
            }

            setTimeout(() => {
                logoEyes.style.transition = "1.5s";
                logoEyes.style.opacity = 0.15;
                logoText.style.transition = "1.5s";
                logoText.style.opacity = 0.15;
                hiddenSubtitle.style.transition = "1.5s";
                hiddenSubtitle.style.opacity = 0;
                floatingForm.style.opacity = 1;
                floatingForm.style.zIndex = 999;
                landingLogoDiv.style.opacity = 0;
            }, 1500)
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


// TIPS PAGE SCRIPTS
if (pageIdentifier === 'tips') {
    // Add event listener to each example image to show full size image on click
    const exampleImages = document.querySelectorAll('.example-image');
    exampleImages.forEach(item => {
        item.addEventListener('click', event => {
            const hiddenFullsize = document.getElementById(`hidden-${item.classList[1]}`);
            hiddenFullsize.classList.toggle('show-fullsize');
        
            document.addEventListener('click', (event) => {
                if (!hiddenFullsize.contains(event.target) && !item.contains(event.target)) {
                    hiddenFullsize.classList.remove('show-fullsize');
                }
            });
        });
    });

    // Add event listener to each full size image to hide on click
    document.querySelectorAll('.hidden-fullsize').forEach(item => {
        item.addEventListener('click', event => {
            item.classList.toggle('show-fullsize');
        });
    });

    // Add event listener to each example image to make it a bit bigger on hover
    const exampleImageDivs = document.querySelectorAll('.example-img-div');
    exampleImageDivs.forEach(item => {
        item.addEventListener('mouseover', event => {
            item.style.transform = 'scale(1.1)';
            if (item.classList.contains('good-example')) {
                item.nextElementSibling.style.transform = 'scale(0.9)';
                item.nextElementSibling.style.opacity = '0.6';
            } else {
                item.previousElementSibling.style.transform = 'scale(0.9)';
                item.previousElementSibling.style.opacity = '0.6';
            }
            if (item.parentElement.nextElementSibling) {
                item.parentElement.nextElementSibling.style.transform = 'scale(0.9)';
                item.parentElement.nextElementSibling.style.opacity = '0.6';
                if (item.parentElement.nextElementSibling.nextElementSibling) {
                    item.parentElement.nextElementSibling.nextElementSibling.style.transform = 'scale(0.9)';
                    item.parentElement.nextElementSibling.nextElementSibling.style.opacity = '0.6';
                }
            }
            if (item.parentElement.previousElementSibling) {
                item.parentElement.previousElementSibling.style.transform = 'scale(0.9)';
                item.parentElement.previousElementSibling.style.opacity = '0.6';
                if (item.parentElement.previousElementSibling.previousElementSibling) {
                    item.parentElement.previousElementSibling.previousElementSibling.style.transform = 'scale(0.9)';
                    item.parentElement.previousElementSibling.previousElementSibling.style.opacity = '0.6';
                }
            }
        });
        item.addEventListener('mouseout', event => {
            item.style.transform = 'scale(1)';
            if (item.classList.contains('good-example')) {
                item.nextElementSibling.style.transform = 'scale(1)';
                item.nextElementSibling.style.opacity = '1';
            } else {
                item.previousElementSibling.style.transform = 'scale(1)';
                item.previousElementSibling.style.opacity = '1';
            }
            if (item.parentElement.nextElementSibling) {
                item.parentElement.nextElementSibling.style.transform = 'scale(1)';
                item.parentElement.nextElementSibling.style.opacity = '1';
                if (item.parentElement.nextElementSibling.nextElementSibling) {
                    item.parentElement.nextElementSibling.nextElementSibling.style.transform = 'scale(1)';
                    item.parentElement.nextElementSibling.nextElementSibling.style.opacity = '1';
                }
            }
            if (item.parentElement.previousElementSibling) {
                item.parentElement.previousElementSibling.style.transform = 'scale(1)';
                item.parentElement.previousElementSibling.style.opacity = '1';
                if (item.parentElement.previousElementSibling.previousElementSibling) {
                    item.parentElement.previousElementSibling.previousElementSibling.style.transform = 'scale(1)';
                    item.parentElement.previousElementSibling.previousElementSibling.style.opacity = '1';
                }
            }
        });

    });
}
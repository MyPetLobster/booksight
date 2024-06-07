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
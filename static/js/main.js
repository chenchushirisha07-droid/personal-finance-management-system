// Mobile Menu Toggle
function toggleMenu() {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
}

// Contact Form Validation
document.addEventListener("DOMContentLoaded", () => {
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = e.target.querySelector('button[type="submit"]');
            const originalText = btn.innerText;
            
            btn.innerText = "Sending Securely...";
            btn.disabled = true;
            btn.classList.add('opacity-75');

            setTimeout(() => {
                alert("Thank you! Your message has been sent to the Finora support team.");
                btn.innerText = originalText;
                btn.disabled = false;
                btn.classList.remove('opacity-75');
                e.target.reset();
            }, 1500);
        });
    }
});
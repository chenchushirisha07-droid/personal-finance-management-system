import os

# 1. Create the exact folder structure FastAPI expects
os.makedirs(os.path.join("static", "js"), exist_ok=True)

# 2. Write the JavaScript code directly into the correct file
js_content = """
function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    if (menu) menu.classList.toggle('hidden');
}

function handleContactSubmit(e) {
    e.preventDefault();
    const btn = e.target.querySelector('button[type="submit"]');
    if (!btn) return;

    const originalText = btn.innerText;
    btn.innerText = "Sending...";
    btn.disabled = true;

    setTimeout(() => {
        btn.innerText = originalText;
        btn.disabled = false;
        e.target.reset();
        alert("Success! Your message has been sent to the Finora team.");
    }, 1500);
}
"""

file_path = os.path.join("static", "js", "main.js")
with open(file_path, "w") as file:
    file.write(js_content)

print(f"Success! The file has been created exactly at: {os.path.abspath(file_path)}")
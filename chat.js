
// Papar mesej pengguna
const userDiv = document.createElement("div");
userDiv.textContent = "🧍: " + userMessage;
messages.appendChild(userDiv);
input.value = "";

try {
    const response = await fetch("https://tasdar-coach.onrender.com/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userMessage })
    });

    const contentType = response.headers.get("content-type") || "";
    if (!contentType.includes("application/json")) {
        throw new Error("Gagal sambung: Respons bukan JSON dari backend.");
    }

    const data = await response.json();

    const botDiv = document.createElement("div");
    botDiv.textContent = "🤖 TAS.DAR: " + data.reply;
    messages.appendChild(botDiv);
} catch (error) {
    const errorDiv = document.createElement("div");
    errorDiv.textContent = "❌ Ralat sambungan: " + error.message;
    messages.appendChild(errorDiv);
}

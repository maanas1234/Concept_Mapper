// Chat UI logic. Keeps the original sendMessage entry point used by the template button.

const messagesEl = document.getElementById("messages");
const inputEl = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const typingEl = document.getElementById("typing-indicator");

let isSending = false;

function appendMessage(role, text) {
    const bubble = document.createElement("div");
    bubble.className = `message ${role}`;
    bubble.textContent = text;
    messagesEl.appendChild(bubble);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

function setLoading(state) {
    isSending = state;
    sendBtn.disabled = state;
    typingEl.classList.toggle("hidden", !state);
    sendBtn.textContent = state ? "Sending…" : "Send";
}

async function sendMessage() {
    if (isSending) return;
    const text = (inputEl.value || "").trim();
    if (!text) return;

    appendMessage("user", text);
    inputEl.value = "";
    setLoading(true);

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_input_field_name: text })
        });

        const data = await res.json();
        console.log("SERVER RESPONSE:", data);
        const type = data.type || "text";

        if (type === "graph") {
            appendMessage("ai", "Got it — rendering your graph…");
            if (typeof window.renderGraph === "function") {
                window.renderGraph(data.graph);
            }
        } else {
            const reply = data.reply ?? data.message ?? "Received.";
            appendMessage("ai", reply);
        }
    } catch (err) {
        appendMessage("ai", `Error: ${err.message || err}`);
    } finally {
        setLoading(false);
        inputEl.focus();
    }
}

function handleKey(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

inputEl.addEventListener("keydown", handleKey);

// expose for inline onclick
window.sendMessage = sendMessage;


// Solves the proof-of-work challenge of forms marked data-proof-of-work.
// Progressive enhancement: without JavaScript the form is submitted without a
// solution, and the server applies a stricter rate limit (ADR 0003, ADR 0017).
const encoder = new TextEncoder();

function leadingZeroBits(bytes) {
  let bits = 0;
  for (const byte of bytes) {
    if (byte === 0) {
      bits += 8;
      continue;
    }
    return bits + Math.clz32(byte) - 24;
  }
  return bits;
}

async function solve(challenge, difficulty) {
  for (let nonce = 0; ; nonce += 1) {
    const message = encoder.encode(`${challenge}:${nonce}`);
    const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", message));
    if (leadingZeroBits(digest) >= difficulty) {
      return String(nonce);
    }
  }
}

for (const form of document.querySelectorAll("form[data-proof-of-work]")) {
  form.addEventListener("submit", async (event) => {
    const nonce = form.elements.pow_nonce;
    if (nonce.value !== "") {
      return;
    }
    event.preventDefault();
    nonce.value = await solve(
      form.elements.pow_challenge.value,
      Number(form.dataset.difficulty),
    );
    form.requestSubmit();
  });
}

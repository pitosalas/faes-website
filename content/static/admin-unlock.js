// admin-unlock.js — handles admin password prompt and content reveal
// Author: Pito Salas and Claude Code
// Open Source Under MIT license

(function () {
  var HASH = document.body.dataset.adminHash;
  var KEY = "faes-admin-unlocked";

  function sha256(str) {
    return crypto.subtle.digest("SHA-256", new TextEncoder().encode(str)).then(function (buf) {
      return Array.from(new Uint8Array(buf)).map(function (b) { return b.toString(16).padStart(2, "0"); }).join("");
    });
  }

  function unlock() {
    document.body.classList.add("admin-unlocked");
    localStorage.setItem(KEY, "true");
    document.getElementById("admin-btn").textContent = "Lock";
  }

  function lock() {
    document.body.classList.remove("admin-unlocked");
    localStorage.removeItem(KEY);
    document.getElementById("admin-btn").textContent = "Admin";
  }

  if (localStorage.getItem(KEY) === "true") {
    unlock();
  }

  document.getElementById("admin-btn").addEventListener("click", function () {
    if (document.body.classList.contains("admin-unlocked")) {
      lock();
      return;
    }
    var pw = prompt("Admin password:");
    if (!pw) return;
    sha256(pw).then(function (hash) {
      if (hash === HASH) {
        unlock();
      } else {
        alert("Incorrect password.");
      }
    });
  });
}());

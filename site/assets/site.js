const button = document.getElementById("copy-install");
const command = document.getElementById("install-command");
const status = document.getElementById("copy-status");
const labels = button.dataset;

button.addEventListener("click", async () => {
  button.disabled = true;
  button.dataset.state = "loading";
  button.textContent = labels.pending;
  status.textContent = "";
  status.removeAttribute("data-state");

  try {
    await navigator.clipboard.writeText(command.textContent);
    button.dataset.state = "success";
    button.textContent = labels.success;
    status.textContent = labels.successStatus;
  } catch {
    button.dataset.state = "error";
    button.textContent = labels.error;
    status.dataset.state = "error";
    status.textContent = labels.errorStatus;
  } finally {
    button.disabled = false;
  }
});

button.hidden = false;

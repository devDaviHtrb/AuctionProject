import { signIn } from "../interactivity/SignUp.js";

document.addEventListener("DOMContentLoaded", () => {
  const signUpBtn = document.getElementById("signUpBtn");
  document.getElementById("openLogin").href = window.location.href;

  signUpBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    await signIn();
  });

  const steps = [
    document.getElementById("step-1"),
    document.getElementById("step-2"),
    document.getElementById("step-3"),
  ];

  const stepLabels = [
    document.getElementById("step-1-label"),
    document.getElementById("step-2-label"),
    document.getElementById("step-3-label"),
  ];

  const progressBar = document.getElementById("progress-bar");
  const nextButtons = document.querySelectorAll(".next-step");
  const prevButtons = document.querySelectorAll(".prev-step");

  let currentStep = 0;

  function updateSteps() {
    steps.forEach((step, index) => {
      step.classList.toggle("active-step-content", index === currentStep);
      step.classList.toggle("hidden-step", index !== currentStep);
    });

    stepLabels.forEach((label, index) => {
      label.classList.toggle("active-step", index === currentStep);
    });

    const progress = ((currentStep + 1) / steps.length) * 100;
    progressBar.style.width = `${progress}%`;
  }

  nextButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      if (currentStep < steps.length - 1) {
        currentStep++;
        updateSteps();
      }
    });
  });

  prevButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      if (currentStep > 0) {
        currentStep--;
        updateSteps();
      }
    });
  });

  const radios = document.querySelectorAll("input[name='account_type']");
  const userTypeInput = document.getElementById("userType");
  const pfFields = document.querySelectorAll(".pp_field");
  const pjFields = document.querySelectorAll(".lp_field");

  function toggleTypeFields() {
    const selected = document.querySelector(
      "input[name='account_type']:checked"
    ).value;
    userTypeInput.value = selected;

    pfFields.forEach(
      (el) =>
        (el.style.display = selected === "physical_person" ? "block" : "none")
    );
    pjFields.forEach(
      (el) =>
        (el.style.display = selected === "legal_person" ? "block" : "none")
    );

    const typeOptions = document.querySelectorAll(".type-option");
    typeOptions.forEach((opt) => {
      const input = opt.querySelector("input[name='account_type']");
      opt.classList.toggle("active", input.checked);
    });
  }

  radios.forEach((radio) => {
    radio.addEventListener("change", toggleTypeFields);
  });

  toggleTypeFields();
  updateSteps();
});

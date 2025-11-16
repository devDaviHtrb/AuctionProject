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
    document.getElementById("step-4"),
    document.getElementById("step-5")
  ];

  const stepLabels = [
    document.getElementById("step-1-label"),
    document.getElementById("step-2-label"),
    document.getElementById("step-3-label"),
    document.getElementById("step-4-label"),
    document.getElementById("step-5-label")
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

    const currentStepElement = steps[currentStep];


    const requiredFields = currentStepElement.querySelectorAll("input[required], select[required], textarea[required]");

    let isValid = true;
    console.log("STEP:", currentStep);
console.log("FIELDS:", requiredFields);
requiredFields.forEach(f => console.log(f.id, f.value));

    requiredFields.forEach((field) => {
      if (!field.value.trim()) {
        field.reportValidity();
        isValid = false;
      } else if (!field.checkValidity()) {
        field.reportValidity();
        isValid = false;
      }
    });
    alert(isValid)

    if (!isValid) {
      return; 
    }


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


  pfFields.forEach((el) => {
    el.style.display = selected === "physical_person" ? "block" : "none";

    const input = el.querySelector("input, select, textarea");
    if (input) {
      if (selected === "physical_person") {
        input.setAttribute("required", "true");
      } else {
        input.removeAttribute("required");
      }
    }
  });


  pjFields.forEach((el) => {
    el.style.display = selected === "legal_person" ? "block" : "none";

    const input = el.querySelector("input, select, textarea");
    if (input) {
      if (selected === "legal_person") {
        input.setAttribute("required", "true");
      } else {
        input.removeAttribute("required");
      }
    }
  });

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


const tabLogin = document.getElementById("tab-login");
const tabSignup = document.getElementById("tab-register");
const loginContainer = document.getElementById("pills-login");
const signupContainer = document.getElementById("pills-register");

tabLogin.addEventListener("click", (e) => {
  if (tabLogin.classList.contains("active")) return;
  tabLogin.classList.add("active");
  tabSignup.classList.remove("active");
  loginContainer.classList.toggle("show");
  loginContainer.classList.toggle("active");
  signupContainer.classList.toggle("show");
  signupContainer.classList.toggle("active");
});
tabSignup.addEventListener("click", (e) => {
  if (tabSignup.classList.contains("active")) return;
  tabSignup.classList.add("active");
  tabLogin.classList.remove("active");
  signupContainer.classList.toggle("show");
  signupContainer.classList.toggle("active");
  loginContainer.classList.toggle("show");
  loginContainer.classList.toggle("active");
});

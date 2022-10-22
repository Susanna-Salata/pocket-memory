const buttons = document.querySelectorAll("button");
const sections = document.querySelectorAll(".content");

buttons.forEach((btn) => {
  btn.addEventListener("click", () => {
    buttons.forEach((btn) => {
      btn.classList.remove("active");
    });
    btn.classList.add("active");
    const id = btn.id;
    sections.forEach((section) => {
      section.classList.remove("active");
    });
    const req = document.getElementsByClassName(`content${id}`);
    req[0].classList.add("active");
  });
});

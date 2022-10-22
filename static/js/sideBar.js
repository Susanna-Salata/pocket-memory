const toggleBtn = document.getElementById("sidebarBtn");
const sideBar = document.getElementById("sidebar-wrapper");
const mainContainer = document.getElementById("wrapper");

toggleBtn.addEventListener("click", (e) => {
  mainContainer.classList.toggle("toggled");
  sideBar.classList.toggle("toggled");
});

// for home page scroll effect 
const header = document.getElementById("mainHeader");
      
window.addEventListener("scroll", function () {
  if (window.scrollY > 50) {
    header.classList.add("bg-slate-400");
  } else {
    header.classList.remove("bg-slate-400");
  }
});


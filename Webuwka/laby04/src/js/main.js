import "../scss/styles.scss";
import * as bootstrap from "bootstrap";
import * as mdb from "mdb-ui-kit"; // lib
import AOS from "aos";
import "aos/dist/aos.css";

window.bootstrap = bootstrap;
window.mdb = mdb;

AOS.init({
  duration: 300,
  easing: "ease-in-out",
  once: true,
  mirror: false,
});

document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      window.scrollTo({
        top: target.offsetTop - 70,
        behavior: "smooth",
      });
    }
  });
});

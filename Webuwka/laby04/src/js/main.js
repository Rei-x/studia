import "../scss/styles.scss";
import * as bootstrap from "bootstrap";
import * as mdb from "mdb-ui-kit"; // lib
import AOS from "aos";
import "aos/dist/aos.css";
import Chart from "chart.js/auto";

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

document.addEventListener("DOMContentLoaded", () => {
  const chartElement = document.getElementById("destinationsChart");

  if (chartElement) {
    const data = {
      labels: [
        "Włochy",
        "Hiszpania",
        "Grecja",
        "Tajlandia",
        "Japonia",
        "Egipt",
        "Meksyk",
      ],
      datasets: [
        {
          label: "Popularność kierunków (tysiące rezerwacji)",
          data: [78, 65, 59, 48, 42, 38, 35],
          backgroundColor: [
            "rgba(255, 99, 132, 0.7)",
            "rgba(54, 162, 235, 0.7)",
            "rgba(255, 206, 86, 0.7)",
            "rgba(75, 192, 192, 0.7)",
            "rgba(153, 102, 255, 0.7)",
            "rgba(255, 159, 64, 0.7)",
            "rgba(99, 255, 132, 0.7)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
            "rgba(99, 255, 132, 1)",
          ],
          borderWidth: 1,
        },
      ],
    };

    new Chart(chartElement, {
      type: "bar",
      data: data,
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: "Najpopularniejsze kierunki podróży",
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: "Liczba rezerwacji (w tysiącach)",
            },
          },
          x: {
            title: {
              display: true,
              text: "Kraje",
            },
          },
        },
      },
    });
  }
});

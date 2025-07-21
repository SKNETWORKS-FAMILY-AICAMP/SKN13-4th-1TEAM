function filterJobs() {
  const input = document.getElementById("search-input").value.toLowerCase();
  const cards = document.querySelectorAll(".job-card");
  let matchCount = 0;

  cards.forEach(card => {
    const text = card.textContent.toLowerCase();
    const match = text.includes(input);
    card.style.display = match ? "block" : "none";
    if (match) matchCount++;
  });

  document.getElementById("no-result").style.display = (matchCount === 0) ? "block" : "none";
}

function filterByCategory(category, element) {
  const cards = document.querySelectorAll(".job-card");
  let matchCount = 0;

  cards.forEach(card => {
    const jobCat = card.getAttribute("data-category");
    const match = (category === "전체" || jobCat === category);
    card.style.display = match ? "block" : "none";
    if (match) matchCount++;
  });

  document.getElementById("no-result").style.display = (matchCount === 0) ? "block" : "none";

  const buttons = document.querySelectorAll(".category-btn");
  buttons.forEach(btn => btn.classList.remove("active"));
  element.classList.add("active");

  document.getElementById("search-input").value = "";
}

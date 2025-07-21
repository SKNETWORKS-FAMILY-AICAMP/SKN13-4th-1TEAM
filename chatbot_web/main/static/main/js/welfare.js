const welfareCategories = [
  "청년",
  "노인",
  "장애인",
  "임신출산",
  "저소득층",
  "다문화",
  "북한이탈주민",
  "한부모가정",
  "중장년",
  "기타"
];

// 샘플 복지 데이터 (추후 API 대체)
const welfareData = [
  { title: "청년 주거 지원", category: "청년", target: "서울시 거주 청년", benefit: "월세 지원", period: "상시" },
  { title: "노인 건강 검진", category: "노인", target: "65세 이상", benefit: "무료 건강 검진", period: "2024.12까지" },
  { title: "장애인 보조기기 지원", category: "장애인", target: "등록 장애인", benefit: "보조기기 대여 및 수리", period: "예산 소진 시까지" },
  { title: "출산 축하금", category: "임신출산", target: "신생아 가정", benefit: "현금 100만원 지급", period: "상시" },
  { title: "한부모 가족 돌봄비 지원", category: "한부모가정", target: "한부모 가정", benefit: "월 최대 30만원 돌봄비", period: "신청 후 3개월 내 지급" },
];

// DOM 로드 후 실행
window.addEventListener("DOMContentLoaded", () => {
  renderWelfareCategories();
  renderWelfareList(welfareData);
});

function renderWelfareCategories() {
  const container = document.querySelector(".category-filter");
  container.innerHTML = "";

  const allBtn = document.createElement("span");
  allBtn.className = "category-btn active";
  allBtn.textContent = "전체";
  allBtn.onclick = () => filterByCategory("전체", allBtn);
  container.appendChild(allBtn);

  welfareCategories.forEach(category => {
    const btn = document.createElement("span");
    btn.className = "category-btn";
    btn.textContent = category;
    btn.onclick = () => filterByCategory(category, btn);
    container.appendChild(btn);
  });
}

function renderWelfareList(data) {
  const list = document.getElementById("welfare-list");
  list.innerHTML = "";

  data.forEach(item => {
    const card = document.createElement("div");
    card.className = "welfare-card";
    card.setAttribute("data-category", item.category);
    card.innerHTML = `
      <h4>${item.title}</h4>
      <p><strong>대상:</strong> ${item.target}</p>
      <p><strong>지원내용:</strong> ${item.benefit}</p>
      <p><strong>신청기간:</strong> ${item.period}</p>
    `;
    list.appendChild(card);
  });
}

function filterWelfare() {
  const input = document.getElementById("welfare-search").value.toLowerCase();
  const cards = document.querySelectorAll(".welfare-card");
  let visibleCount = 0;

  cards.forEach(card => {
    const text = card.textContent.toLowerCase();
    const isMatch = text.includes(input);
    card.style.display = isMatch ? "block" : "none";
    if (isMatch) visibleCount++;
  });

  document.getElementById("no-result").style.display = visibleCount === 0 ? "block" : "none";
}

function filterByCategory(category, element) {
  const cards = document.querySelectorAll(".welfare-card");
  let visibleCount = 0;

  cards.forEach(card => {
    const jobCat = card.getAttribute("data-category");
    const isVisible = category === "전체" || jobCat === category;
    card.style.display = isVisible ? "block" : "none";
    if (isVisible) visibleCount++;
  });

  document.querySelectorAll(".category-btn").forEach(btn => btn.classList.remove("active"));
  element.classList.add("active");

  document.getElementById("welfare-search").value = "";
  document.getElementById("no-result").style.display = visibleCount === 0 ? "block" : "none";
}

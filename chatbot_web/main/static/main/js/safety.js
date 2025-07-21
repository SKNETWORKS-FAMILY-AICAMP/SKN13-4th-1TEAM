// 구 path 클릭 시 동작
document.querySelectorAll('.land').forEach((el) => {
  el.addEventListener('click', function () {
    const alreadyFocused = el.classList.contains('focused');

    // 모두 초기화
    document.querySelectorAll('.land').forEach(p => {
      p.classList.remove('focused', 'dimmed');
    });

    if (!alreadyFocused) {
      el.classList.add('focused');
      document.querySelectorAll('.land').forEach(p => {
        if (p !== el) {
          p.classList.add('dimmed');
        }
      });
    }

    const guName = el.getAttribute('title') || '선택된 구';
    showInfo(
      guName,
      '재난 정보',
      `${guName}의 대피소 또는 피해 정보`,
      new Date().toLocaleString('ko-KR'),
      '해당 구를 클릭하셨습니다. 관련 정보가 여기에 표시됩니다.'
    );
  });
});

// 이모지/아이콘 클릭 시 정보 출력
function showInfo(name, type, address, time, memo) {
  const panel = document.getElementById('info-panel');
  panel.innerHTML = `
    <h3>${name}</h3>
    <p><strong>종류:</strong> ${type}</p>
    <p><strong>주소:</strong> ${address}</p>
    <p><strong>업데이트:</strong> ${time}</p>
    <p><strong>메모:</strong> ${memo}</p>
  `;
  panel.style.display = 'block';
  panel.scrollIntoView({ behavior: 'smooth' });
}

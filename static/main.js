function startTimer(duration) {
  let timer = duration * 60; // 초 단위로 변환
  const timerElement = document.getElementById("clock");

  function updateTimer() {
    const minutes = Math.floor(timer / 60);
    const seconds = timer % 60;

    timerElement.innerHTML = `${minutes}<span>:</span>${
      seconds < 10 ? "0" : ""
    }${seconds}`;

    if (--timer < 0) {
      clearInterval(intervalId);
      timerElement.innerHTML = "시간 종료";
    }
  }

  updateTimer(); // 초기 호출

  const intervalId = setInterval(updateTimer, 1000); // 1초마다 updateTimer 함수 호출
}

startTimer(5);

document
  .getElementById("file-input")
  .addEventListener("change", function (event) {
    const selectedImage = event.target.files[0];

    if (selectedImage) {
      const reader = new FileReader();

      // 이미지 읽기 완료 시 실행되는 콜백 함수
      reader.onload = function (event) {
        // 읽은 이미지 데이터를 화면에 표시
        const imageData = event.target.result;
        const imgElement = document.getElementById("image-upload");
        imgElement.src = imageData;

        document.getElementById("filebox").style.display = "none";
        document.getElementById("result").style.display = "flex";
      };

      // 이미지 읽기 시작
      reader.readAsDataURL(selectedImage);
    }
  });

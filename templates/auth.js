// 토큰 만료 여부를 확인하고, 필요할 경우 새로운 토큰을 얻는 함수
function checkTokenExpiration() {
    var accessToken = localStorage.getItem('access_token'); // 로컬 스토리지에서 액세스 토큰을 가져옴

    if (!accessToken) {
        // 액세스 토큰이 없으면 로그인 페이지로 이동하거나 다른 로그인 처리 로직을 수행
        window.location.href = '/login';
        return;
    }

    // 액세스 토큰을 해독하여 만료 시간 확인
    var tokenPayload = JSON.parse(atob(accessToken.split('.')[1]));
    var expirationTime = tokenPayload.exp * 1000; // 만료 시간(밀리초 단위)

    if (Date.now() >= expirationTime) {
        // 토큰이 만료되었으면 리프레시 토큰을 사용하여 새로운 액세스 토큰을 요청
        refreshAccessToken();
    }
}

// 리프레시 토큰을 사용하여 새로운 액세스 토큰을 요청하는 함수
function refreshAccessToken() {
    var refreshToken = localStorage.getItem('refresh_token'); // 로컬 스토리지에서 리프레시 토큰을 가져옴

    // 리프레시 토큰을 사용하여 서버에 POST 요청을 보냄
    fetch('/refresh', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + refreshToken
        }
    })
    .then(response => response.json())
    .then(data => {
        // 새로운 액세스 토큰을 받았을 경우 로컬 스토리지에 저장하거나 필요한 처리를 수행
        localStorage.setItem('access_token', data.access_token);
        // 요청 재시도 또는 다른 작업 수행
    })
    .catch(error => {
        console.error('Error refreshing access token:', error);
        // 에러 처리 로직 추가
    });
}

// 페이지 로드 시 토큰 만료 여부 확인
checkTokenExpiration();

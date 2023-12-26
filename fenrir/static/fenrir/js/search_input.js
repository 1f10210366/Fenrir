let API_KEY_HOTPEPPER = '7699907c06980421';
let map;
let currentPosition;

function initMap() {
  // Google Mapを初期化
  map = new google.maps.Map(document.getElementById('map'), {
      center: currentPosition,
      zoom: 15
  });

  // 現在地にマーカーを表示
  new google.maps.Marker({
      position: currentPosition,
      map: map,
      title: 'Your Location'
  });
}


function getCurrentLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function (position) {
        document.getElementById('latitude').value = position.coords.latitude;
        document.getElementById('longitude').value = position.coords.longitude;
      },
      function (error) {
        console.error('位置情報の取得に失敗しました', error);
      }
    );
  } else {
    console.error('Geolocationがサポートされていません');
  }
}


function searchNearbyRestaurants() {
    // 入力から検索半径を取得
    let radius = document.getElementById('radius').value;

    // Hot Pepper APIを使用してレストランを検索
    fetch(`https://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=${API_KEY_HOTPEPPER}&lat=${currentPosition.lat}&lng=${currentPosition.lng}&range=${radius}`)
        .then(response => response.json())
        .then(displaySearchResults)
        .catch(apiError);
}

// 現在地の緯度と経度をフォームにセット
document.getElementById('latitude').value = currentPosition.lat;
document.getElementById('longitude').value = currentPosition.lng;


function displaySearchResults(results) {
    let resultsDiv = document.getElementById('search-results');
    resultsDiv.innerHTML = ''; // 以前の結果をクリア

    results.results.shop.forEach(shop => {
        // 各レストランの関連情報を表示
        let shopDiv = document.createElement('div');
        shopDiv.innerHTML = `
            <h3>${shop.name}</h3>
            <p>アクセス: ${shop.access}</p>
            <img src="${shop.photo.mobile.l}" alt="サムネイル">
            <button onclick="showRestaurantDetails('${shop.id}')">詳細を表示</button>
        `;
        resultsDiv.appendChild(shopDiv);
    });
}


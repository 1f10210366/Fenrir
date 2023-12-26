let API_KEY_HOTPEPPER = '7699907c06980421';
let API_KEY_Google = 'AIzaSyBhg8RBbcrfWT_R3E2dISbpqHtSC7LLUwY';
let map;
let currentPosition;  // currentPosition を宣言


// ページがロードされたときに getCurrentLocation 関数を呼び出す
document.addEventListener('DOMContentLoaded', function () {
  getCurrentLocation();
});


function getCurrentLocation() {
  if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
          function (position) {
              currentPosition = { lat: position.coords.latitude, lng: position.coords.longitude };
              document.getElementById('latitude').value = position.coords.latitude;
              document.getElementById('longitude').value = position.coords.longitude;
              initMap();  // getCurrentLocation の中で位置情報を取得したら initMap を呼び出す
          },
          function (error) {
              console.error('位置情報の取得に失敗しました', error);
          }
      );
  } else {
      console.error('Geolocationがサポートされていません');
  }
}


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


